"""Build the dense (FAISS) and sparse (BM25) indexes over chunked transcripts.

Both index types are built from the same frozen chunk set so that
retrieve.py can query either -- or both, for the hybrid strategy -- without
re-chunking. The embedding model (`bge-small-en-v1.5`) is held constant
across all conditions; the query prefix is
defined in configs/base.json and cross-checked at startup.

Chunks are embedded with no prefix; queries get BGE's documented retrieval
instruction prefix (applied in embed_query, not here). Embeddings are
L2-normalized so FAISS's inner-product index behaves as cosine similarity.

Indexing representation (the third independent variable)
--------------------------------------------------------
What string the two retrievers actually index is a manipulated variable, not
a constant. `build_index_text` is the single place that decides it:

- `text_only`        -- the raw chunk text, byte for byte. What every existing
                        result was produced under.
- `metadata_enriched`-- one metadata line, a blank line, then the chunk text,
                        with the transcript text truncated so the whole string
                        fits the encoder's content budget.

Three invariants from README.md's "Invariants" section are
load-bearing here and are enforced in code, not by discipline:

1. Anchor matching never reads the enriched string. It lives under the key
   `index_text`; `evaluate.chunk_matches_anchor` keeps reading `chunk["text"]`.
2. The format is frozen in exactly one place per constant, and cross-checked
   against configs/base.json by `run_experiment.validate_config_matches_code`
   the same way `query_prefix` already is.
3. Dense and BM25 index the identical string. That is why truncation happens
   HERE, at build time, rather than being left to the encoder: the encoder
   silently drops tokens past its limit while BM25 has no limit at all, so an
   untruncated enriched string would hand the two retrievers the same bytes but
   feed them different content -- indexing representation confounded with
   retrieval strategy, in the 500-token enriched cell only.
"""

import re

import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from chunking import EMBEDDING_MODEL_NAME, get_tokenizer

QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# The encoder's sequence budget. bge-small-en-v1.5's max_seq_length is 512
# (measured, and asserted against the loaded model in get_embedding_model
# rather than assumed here), of which [CLS] and [SEP] consume two -- leaving
# MAX_CONTENT_TOKENS for the indexed string itself.
MAX_SEQ_LENGTH = 512
N_SPECIAL_TOKENS = 2
MAX_CONTENT_TOKENS = MAX_SEQ_LENGTH - N_SPECIAL_TOKENS  # 510

REPRESENTATION_TEXT_ONLY = "text_only"
REPRESENTATION_METADATA_ENRICHED = "metadata_enriched"
INDEXING_REPRESENTATIONS = (REPRESENTATION_TEXT_ONLY, REPRESENTATION_METADATA_ENRICHED)

# --- The frozen enrichment format (format "P2", signed off 2026-09-05) -------
#
# One prepended line, a blank line, then the chunk text. Carries the full legal
# company name AND the ticker (27 of 45 benchmark questions name companies in
# prose, only 5 use tickers -- so the prose name is the load-bearing half), the
# fiscal period in BOTH prose and shorthand form, and the section label.
#
# "earnings call" is deliberately absent: it would appear on 100% of chunks, so
# its IDF is ~0 and it cannot discriminate between them. Same reasoning rules
# out field labels like "Company:" / "Section:".
#
# Frozen before any metadata_enriched run, per invariant 2. Not to be revised
# after seeing results.
ENRICHMENT_PREFIX_TEMPLATE = "{company} ({ticker}) {quarter_prose} {year} Q{quarter} {year} {section}"
ENRICHMENT_JOINER = "\n\n"
QUARTER_PROSE = {1: "first quarter", 2: "second quarter", 3: "third quarter", 4: "fourth quarter"}
SECTION_LABELS = {"prepared_remarks": "prepared remarks", "qa": "question and answer"}

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Lazily load and cache the embedding model.

    Asserts the model's actual max sequence length is the MAX_SEQ_LENGTH this
    module budgets against. Under `text_only` a smaller value would silently
    truncate the 500-token condition; under `metadata_enriched` it would make
    `build_index_text`'s truncation arithmetic wrong, which is worse -- the
    string would be truncated to a budget the encoder does not actually have,
    so BM25 and the encoder would again consume different content.
    """
    global _model
    if _model is None:
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        if model.max_seq_length != MAX_SEQ_LENGTH:
            raise AssertionError(
                f"{EMBEDDING_MODEL_NAME} max_seq_length={model.max_seq_length}, but index.py "
                f"budgets against MAX_SEQ_LENGTH={MAX_SEQ_LENGTH} (MAX_CONTENT_TOKENS="
                f"{MAX_CONTENT_TOKENS}). Reconcile the constant with the model before running."
            )
        _model = model
    return _model


# ---------------------------------------------------------------------------
# Indexing representation
# ---------------------------------------------------------------------------


def _n_tokens(text: str) -> int:
    return len(get_tokenizer()(text, add_special_tokens=False)["input_ids"])


def _truncate_to_tokens(text: str, max_tokens: int) -> tuple[str, int, int]:
    """Cut `text` to at most `max_tokens` tokens.

    Returns (text, n_tokens_kept, n_tokens_total), where `n_tokens_total` is
    the token count of the WHOLE input as tokenized here. That third value
    exists because it is not always `chunk["n_tokens"]`: chunking.py counts a
    chunk's tokens inside its section's tokenization, and re-tokenizing the same
    substring on its own can differ by a token or two where the chunk boundary
    fell mid-word. Truncation must be judged against the standalone count --
    the one that actually governs what fits -- or a chunk that was not cut at
    all gets reported as having lost a token.

    Slices on the tokenizer's own character offsets -- the same mechanism
    chunking.py uses to cut chunks -- so the result is a real prefix of the
    original string rather than a detokenized approximation of one.
    """
    encoding = get_tokenizer()(text, return_offsets_mapping=True, add_special_tokens=False)
    offsets = encoding["offset_mapping"]
    total = len(offsets)
    if max_tokens <= 0:
        return "", 0, total
    if total <= max_tokens:
        return text, total, total
    return text[: offsets[max_tokens - 1][1]], max_tokens, total


def build_enrichment_prefix(chunk: dict) -> str:
    """The frozen metadata line for one chunk (without the blank-line joiner)."""
    quarter = int(chunk["quarter"])
    section = chunk["section"]
    if quarter not in QUARTER_PROSE:
        raise ValueError(f"no frozen prose form for quarter {quarter!r} (chunk {chunk['chunk_id']})")
    if section not in SECTION_LABELS:
        raise ValueError(f"no frozen label for section {section!r} (chunk {chunk['chunk_id']})")
    return ENRICHMENT_PREFIX_TEMPLATE.format(
        company=chunk["company"],
        ticker=chunk["ticker"],
        quarter_prose=QUARTER_PROSE[quarter],
        year=int(chunk["year"]),
        quarter=quarter,
        section=SECTION_LABELS[section],
    )


def build_index_text_with_stats(chunk: dict, representation: str) -> tuple[str, dict]:
    """`build_index_text`, plus the truncation bookkeeping it performs.

    Truncation has to be recorded, not merely performed: under
    `metadata_enriched` at chunk_size=500 the prefix pushes the string past the
    encoder's 510-token content budget, so some transcript tokens are dropped
    from what is *indexed*. That reduces retrievability and is a reportable
    limitation, so every run persists per-chunk `prefix_tokens`, whether
    truncation occurred, and how many transcript tokens were dropped.

    Note this reduces retrievability only, never scorability: anchor matching
    runs against raw `chunk["text"]`, which is untouched, so an anchor sitting
    in a discarded tail still counts as a hit if its chunk is retrieved -- it
    is simply less likely to be retrieved on that anchor's own terms.
    """
    if representation == REPRESENTATION_TEXT_ONLY:
        n_tokens = _n_tokens(chunk["text"])
        return chunk["text"], {
            "chunk_id": chunk["chunk_id"],
            "indexing_representation": representation,
            "prefix_tokens": 0,
            "truncated": False,
            "transcript_tokens_total": n_tokens,
            "transcript_tokens_kept": n_tokens,
            "transcript_tokens_dropped": 0,
            "chunk_n_tokens": chunk["n_tokens"],
        }

    if representation != REPRESENTATION_METADATA_ENRICHED:
        raise ValueError(
            f"unknown indexing_representation {representation!r}; expected one of {INDEXING_REPRESENTATIONS}"
        )

    head = build_enrichment_prefix(chunk) + ENRICHMENT_JOINER
    prefix_tokens = _n_tokens(head)

    # WordPiece can in principle merge across the prefix/text boundary, which
    # would make the assembled string cost more than prefix_tokens + text
    # tokens. Rather than assume it never does, measure the assembled string and
    # shrink the budget by however much it actually overflowed. Converges in one
    # pass in practice; the bound exists so a pathological input cannot spin.
    budget = MAX_CONTENT_TOKENS - prefix_tokens
    for _ in range(8):
        body, kept, total = _truncate_to_tokens(chunk["text"], budget)
        index_text = head + body
        overflow = _n_tokens(index_text) - MAX_CONTENT_TOKENS
        if overflow <= 0:
            break
        budget -= overflow
    else:
        raise AssertionError(
            f"could not fit chunk {chunk['chunk_id']} within {MAX_CONTENT_TOKENS} content tokens"
        )

    return index_text, {
        "chunk_id": chunk["chunk_id"],
        "indexing_representation": representation,
        "prefix_tokens": prefix_tokens,
        # Judged against the standalone token count, not chunk["n_tokens"]:
        # see _truncate_to_tokens. Using n_tokens here reported ~20 chunks per
        # corpus as truncated at chunk_size=200, where the prefix leaves ~290
        # tokens of headroom and nothing is cut at all.
        "truncated": kept < total,
        "transcript_tokens_total": total,
        "transcript_tokens_kept": kept,
        "transcript_tokens_dropped": total - kept,
        "chunk_n_tokens": chunk["n_tokens"],
    }


def build_index_text(chunk: dict, representation: str) -> str:
    """The string the retrievers index for `chunk` under `representation`.

    Under `text_only` this is `chunk["text"]` returned unchanged, byte for
    byte -- the property that keeps the six existing conditions valid without
    re-running them, asserted by a regression test.
    """
    return build_index_text_with_stats(chunk, representation)[0]


def attach_index_text(chunks: list[dict], representation: str) -> list[dict]:
    """Attach `index_text` to every chunk in place; return the per-chunk stats.

    Called once per (chunk_size, representation) by the runners, so the
    enriched string is computed once and shared by both retrievers -- the
    mechanical form of "both retrievers receive the identical enriched string".
    """
    stats = []
    for chunk in chunks:
        chunk["index_text"], chunk_stats = build_index_text_with_stats(chunk, representation)
        stats.append(chunk_stats)
    return stats


def _index_texts(chunks: list[dict]) -> list[str]:
    """The indexed strings, refusing to guess if the representation never ran.

    Falling back to `chunk["text"]` when `index_text` is missing would produce a
    `text_only` index mislabeled as enriched -- a run that looks like a result
    and is a control. That is the worst failure available here, so it raises.
    """
    missing = [c["chunk_id"] for c in chunks if "index_text" not in c][:5]
    if missing:
        raise KeyError(
            f"{len(missing)}+ chunk(s) have no 'index_text' (e.g. {missing}) -- call "
            "index.attach_index_text(chunks, representation) first. There is deliberately "
            "no fallback to chunk['text']: it would silently index a text_only run under "
            "an enriched label."
        )
    return [c["index_text"] for c in chunks]


def assert_control_arm_unenriched(chunks: list[dict]) -> None:
    """Under `text_only`, `index_text` must equal `chunk["text"]` byte for byte.

    Guards the control arm the way `_index_texts` guards the treatment arm: a
    config typo must not be able to quietly enrich the baseline, which would
    make the `text_only` half of the grid stop matching the six persisted
    conditions while still carrying their names.
    """
    for chunk in chunks:
        if chunk.get("index_text") != chunk["text"]:
            raise AssertionError(
                f"chunk {chunk['chunk_id']}: index_text differs from text under "
                "indexing_representation='text_only' -- the control arm has been enriched"
            )


# ---------------------------------------------------------------------------
# Index construction
# ---------------------------------------------------------------------------


def embed_chunks(chunks: list[dict]) -> np.ndarray:
    """Embed the chunks' `index_text` with no prefix, L2-normalized for cosine."""
    model = get_embedding_model()
    return model.encode(_index_texts(chunks), normalize_embeddings=True, convert_to_numpy=True)


def embed_query(query: str) -> np.ndarray:
    """Embed a query with BGE's retrieval instruction prefix, L2-normalized."""
    model = get_embedding_model()
    return model.encode(QUERY_PREFIX + query, normalize_embeddings=True, convert_to_numpy=True)


def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """Build a flat inner-product FAISS index (cosine similarity, since
    embeddings are pre-normalized).
    """
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def tokenize_for_bm25(text: str) -> list[str]:
    """Lowercase, alphanumeric-word tokenization for BM25."""
    return re.findall(r"[a-z0-9]+", text.lower())


def build_bm25_index(chunks: list[dict]) -> BM25Okapi:
    """Build a BM25Okapi index over the chunks' `index_text`."""
    return BM25Okapi([tokenize_for_bm25(t) for t in _index_texts(chunks)])
