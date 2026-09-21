"""Diagnostic: do the corpus's tickers actually work as BM25 search terms?

Motivation
----------
The `metadata_enriched` indexing representation (README.md,
"Variables") prepends a company/ticker/period/section line to every chunk's
indexed string. That treatment is only as strong as the discriminating power of
the tokens it adds. A ticker that BM25 cannot distinguish from ordinary English
prose adds noise, not signal -- and the corpus contains at least one
single-letter ticker (`C`, Citigroup), which is exactly that hazard.

This script measures, per ticker, using the pipeline's OWN tokenizer
(`index.tokenize_for_bm25`) and the pipeline's own BM25 implementation
(`rank_bm25.BM25Okapi`, the class `index.build_bm25_index` instantiates):

  * whether the ticker survives tokenization at all;
  * how often the resulting token occurs in the transcript BODY text (the
    prose the retrievers currently index), and in how many distinct companies'
    transcripts;
  * the BM25 IDF of that token over the chunk collection, at BOTH chunk sizes.

Read-only. Touches no config, no results file, no frozen artifact. Writes one
CSV + one Markdown table under analysis/.

Usage
-----
    python analysis/ticker_collision.py
"""

from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
from model_paths import stage1_path  # noqa: E402

import pandas as pd  # noqa: E402
from rank_bm25 import BM25Okapi  # noqa: E402

import ingest  # noqa: E402
from chunking import chunk_transcript  # noqa: E402
from index import tokenize_for_bm25  # noqa: E402
from preprocess import preprocess_transcript  # noqa: E402

CHUNK_SIZES = (200, 500)
OUT_CSV = stage1_path("ticker_collision.csv")
OUT_MD = stage1_path("ticker_collision.md")

# Tickers that are also ordinary English words or common abbreviations in this
# corpus. Flagged, never filtered: the point of the diagnostic is to surface the
# collision, not to hide it.
COMMON_ENGLISH_WORDS = {"c", "ms", "bk", "gs", "all", "on", "it", "are", "for", "so", "one", "key", "see", "big"}


def load_corpus() -> pd.DataFrame:
    return pd.read_parquet(ingest.TRANSCRIPTS_PATH)


def body_token_stats(df: pd.DataFrame) -> tuple[Counter, dict[str, set[str]], int]:
    """Token counts over the transcript BODY text, plus which companies each
    token appears in.

    "Body text" is the same prose the current `text_only` pipeline indexes: the
    per-turn `speaker: text` records produced by preprocess.py. Metadata fields
    are deliberately excluded -- the whole premise of the enriched arm is that
    they are absent from what the retrievers currently see.
    """
    counts: Counter = Counter()
    token_companies: dict[str, set[str]] = {}
    n_turns = 0
    for _, row in df.iterrows():
        for record in preprocess_transcript(row):
            n_turns += 1
            tokens = tokenize_for_bm25(f"{record['speaker']}: {record['text']}")
            counts.update(tokens)
            for tok in set(tokens):
                token_companies.setdefault(tok, set()).add(record["ticker"])
    return counts, token_companies, n_turns


def bm25okapi_idf(n_docs: int, doc_freq: int) -> float:
    """`BM25Okapi`'s own IDF formula, before its negative-IDF epsilon floor.

    Reproduced here (rather than imported) only so the *predicted* enriched-arm
    IDF can be computed for a document frequency that does not exist on disk
    yet. Asserted against the fitted `BM25Okapi.idf` for every observed token in
    `main`, so a change in rank_bm25's formula fails loudly instead of silently
    producing a wrong prediction.
    """
    return math.log(n_docs - doc_freq + 0.5) - math.log(doc_freq + 0.5)


def chunk_idfs(
    df: pd.DataFrame, chunk_size: int
) -> tuple[dict[str, float], dict[str, int], int, dict[str, int], dict[str, set[int]]]:
    """BM25 IDF and document frequency per token over the chunk collection.

    Fits the same `BM25Okapi` class `index.build_bm25_index` instantiates, over
    the same tokenization, so the IDF reported here is the value the retriever
    actually uses rather than a reimplementation of the formula. Built from
    `chunk["text"]` directly because the baseline in question is the current
    `text_only` index.

    Also returns the per-ticker chunk counts and the set of chunk indices whose
    raw text already contains each ticker token -- both needed to predict what
    that token's document frequency becomes once the enriched prefix puts it in
    every one of its company's chunks.
    """
    chunks: list[dict] = []
    for _, row in df.iterrows():
        chunks.extend(chunk_transcript(preprocess_transcript(row), chunk_size))

    tokenized = [tokenize_for_bm25(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)

    df_counts: Counter = Counter()
    for toks in tokenized:
        df_counts.update(set(toks))

    chunks_per_ticker: Counter = Counter(c["ticker"] for c in chunks)
    token_doc_ids: dict[str, set[int]] = {}
    for i, toks in enumerate(tokenized):
        for tok in set(toks):
            token_doc_ids.setdefault(tok, set()).add(i)

    company_doc_ids: dict[str, set[int]] = {}
    for i, c in enumerate(chunks):
        company_doc_ids.setdefault(c["ticker"], set()).add(i)

    # Predicted enriched document frequency: the union of "chunks whose prose
    # already contains the token" and "every chunk of that ticker's company",
    # since the enriched prefix adds the ticker to all of the latter.
    predicted_df = {
        ticker: len(token_doc_ids.get(ticker.lower(), set()) | company_doc_ids.get(ticker, set()))
        for ticker in chunks_per_ticker
    }
    return dict(bm25.idf), dict(df_counts), len(chunks), predicted_df, dict(chunks_per_ticker)


def main() -> int:
    df = load_corpus()
    tickers = sorted(df["symbol"].unique().tolist())
    company_by_ticker = dict(zip(df["symbol"], df["company_name"]))
    print(f"corpus: {len(df)} transcripts, {len(tickers)} tickers")

    print("tokenizing body text...")
    body_counts, token_companies, n_turns = body_token_stats(df)
    print(f"  {n_turns} turns, {len(body_counts)} distinct body tokens")

    idf_by_size: dict[int, dict[str, float]] = {}
    df_by_size: dict[int, dict[str, int]] = {}
    n_chunks_by_size: dict[int, int] = {}
    predicted_df_by_size: dict[int, dict[str, int]] = {}
    for size in CHUNK_SIZES:
        print(f"chunking + BM25 at chunk_size={size}...")
        (
            idf_by_size[size],
            df_by_size[size],
            n_chunks_by_size[size],
            predicted_df_by_size[size],
            _,
        ) = chunk_idfs(df, size)
        print(f"  {n_chunks_by_size[size]} chunks")

        # Guard the prediction: our reproduction of BM25Okapi's IDF formula must
        # match the fitted values it will be compared against.
        #
        # Checked only where the raw formula is positive. BM25Okapi replaces a
        # negative IDF -- a token in more than about half the collection, e.g.
        # "and" -- with `epsilon * average_idf`, and that floor is not
        # reproducible from (n_docs, doc_freq) alone. Every ticker, and every
        # predicted enriched document frequency (about 1/16 of the collection),
        # sits far inside the positive regime, so the floor is irrelevant to
        # this diagnostic; asserting over the floored tokens too would only
        # test rank_bm25's epsilon handling.
        n_checked = 0
        for tok, fitted in idf_by_size[size].items():
            ours = bm25okapi_idf(n_chunks_by_size[size], df_by_size[size][tok])
            if ours <= 0:
                continue
            n_checked += 1
            if abs(ours - fitted) > 1e-9:
                raise AssertionError(
                    f"bm25okapi_idf does not reproduce BM25Okapi.idf for {tok!r} at "
                    f"chunk_size={size}: {ours} vs {fitted} -- rank_bm25's IDF formula "
                    "changed, so the enriched-IDF prediction is unsafe"
                )
        print(f"  IDF formula verified against {n_checked} fitted tokens")

    rows = []
    for ticker in tickers:
        tokens = tokenize_for_bm25(ticker)
        survives = len(tokens) == 1 and tokens[0] == ticker.lower()
        token = tokens[0] if tokens else ""

        flags = []
        if len(token) == 1:
            flags.append("single_letter")
        if token in COMMON_ENGLISH_WORDS:
            flags.append("common_english_word")
        if len(token_companies.get(token, set())) > 1:
            flags.append("appears_in_multiple_companies")

        row = {
            "ticker": ticker,
            "company": company_by_ticker[ticker],
            "bm25_token": token,
            "survives_tokenization": survives,
            "token_len": len(token),
            "body_occurrences": body_counts.get(token, 0),
            "n_distinct_companies_in_body": len(token_companies.get(token, set())),
            "companies_in_body": ";".join(sorted(token_companies.get(token, set()))),
            "flags": ";".join(flags) or "-",
        }
        for size in CHUNK_SIZES:
            row[f"chunk_df_{size}"] = df_by_size[size].get(token, 0)
            row[f"n_chunks_{size}"] = n_chunks_by_size[size]
            idf = idf_by_size[size].get(token)
            # Absent from the fitted vocabulary entirely: BM25Okapi scores an
            # unknown query term at 0 for every chunk, so the ticker contributes
            # nothing at all under text_only -- reported as OOV, not as 0.0 IDF.
            row[f"bm25_idf_{size}"] = "OOV" if idf is None else round(idf, 4)
            pred_df = predicted_df_by_size[size][ticker]
            row[f"predicted_enriched_df_{size}"] = pred_df
            row[f"predicted_enriched_idf_{size}"] = round(bm25okapi_idf(n_chunks_by_size[size], pred_df), 4)
        rows.append(row)

    def idf_key(r: dict) -> float:
        v = r[f"bm25_idf_{CHUNK_SIZES[0]}"]
        return 1e9 if v == "OOV" else float(v)

    rows.sort(key=idf_key)

    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    cols = [
        "ticker", "company", "bm25_token", "survives_tokenization", "body_occurrences",
        "n_distinct_companies_in_body", "chunk_df_200", "bm25_idf_200", "chunk_df_500",
        "bm25_idf_500", "predicted_enriched_idf_200", "predicted_enriched_idf_500", "flags",
    ]
    tokenizer_src = 're.findall(r"[a-z0-9]+", text.lower())'
    lines = [
        "# Ticker collision diagnostic",
        "",
        f"Corpus: {len(df)} transcripts, {len(tickers)} tickers, "
        f"{n_chunks_by_size[200]} chunks @200 / {n_chunks_by_size[500]} chunks @500.",
        "",
        f"Tokenizer: `index.tokenize_for_bm25` = `{tokenizer_src}`.",
        "**There is no stopword list and no minimum token length** anywhere in the",
        "pipeline, and `rank_bm25.BM25Okapi` adds none -- so every ticker survives",
        "tokenization, including the single-letter one. IDF is read from the fitted",
        "`BM25Okapi.idf`, not reimplemented. Sorted by IDF@200 ascending (least",
        "discriminating first).",
        "",
        "`bm25_idf_*` = **OOV** means the token is absent from the text_only",
        "vocabulary entirely; `BM25Okapi` scores an unknown query term at 0 against",
        "every chunk, so under `text_only` that ticker contributes nothing at all as",
        "a search term.",
        "",
        "`predicted_enriched_idf_*` is what that token's IDF becomes once the",
        "enriched prefix puts the ticker in every chunk of its own company: document",
        "frequency rises to the union of (chunks whose prose already contains it) and",
        "(all of that company's chunks), which is ~1/16 of the collection. It is a",
        "prediction from chunk counts, not a measurement of a built enriched index --",
        "computed with `BM25Okapi`'s own IDF formula, asserted at run time to",
        "reproduce the fitted values exactly.",
        "",
        "| " + " | ".join(cols) + " |",
        "|" + "|".join(["---"] * len(cols)) + "|",
    ]
    for r in rows:
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n-> {OUT_CSV.relative_to(REPO_ROOT)}")
    print(f"-> {OUT_MD.relative_to(REPO_ROOT)}")
    print()
    for r in rows:
        if r["flags"] != "-":
            print(
                f"  FLAG {r['ticker']:>5} ({r['flags']}): body_occ={r['body_occurrences']}, "
                f"companies={r['n_distinct_companies_in_body']}, "
                f"idf200={r['bm25_idf_200']}, idf500={r['bm25_idf_500']}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
