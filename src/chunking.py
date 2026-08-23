"""Split preprocessed transcript sections into chunks.

`chunk_size` (200 or 500 tokens) is a config parameter, never hardcoded --
this module supports both settings from the same code path so the
6-condition experiment grid stays valid. Chunks are non-overlapping,
fixed-size token windows measured with `bge-small-en-v1.5`'s own tokenizer
(the same tokenizer used to embed them in index.py), sliced per section
(prepared remarks vs. Q&A) so a chunk never spans both.

Each output chunk retains the metadata attached in preprocess.py (company,
ticker, date, year, quarter, sector, section) plus the set of speakers
whose turns it overlaps and a stable chunk_id.
"""

from transformers import AutoTokenizer, PreTrainedTokenizerBase

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

_tokenizer: PreTrainedTokenizerBase | None = None


def get_tokenizer() -> PreTrainedTokenizerBase:
    """Lazily load and cache the embedding model's tokenizer."""
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)
    return _tokenizer


def _build_section_text(turns: list[dict]) -> tuple[str, list[tuple[int, int, dict]]]:
    """Concatenate a section's turns into one string.

    Returns the full text plus, for each turn, the (start_char, end_char)
    span it occupies in that text -- used to map token windows back to the
    turns they overlap.
    """
    pieces = []
    spans = []
    cursor = 0
    for turn in turns:
        piece = f"{turn['speaker']}: {turn['text']}"
        start = cursor
        end = start + len(piece)
        spans.append((start, end, turn))
        pieces.append(piece)
        cursor = end + 2  # matches the "\n\n" separator below
    return "\n\n".join(pieces), spans


def chunk_section(turns: list[dict], chunk_size: int) -> list[dict]:
    """Chunk one section's turns (all from the same transcript+section) into
    non-overlapping windows of `chunk_size` tokens.
    """
    if not turns:
        return []

    tokenizer = get_tokenizer()
    text, spans = _build_section_text(turns)
    encoding = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    offsets = encoding["offset_mapping"]

    meta = turns[0]
    chunks = []
    for chunk_index, token_start in enumerate(range(0, len(offsets), chunk_size)):
        token_end = min(token_start + chunk_size, len(offsets))
        char_start = offsets[token_start][0]
        char_end = offsets[token_end - 1][1]
        chunk_text = text[char_start:char_end]

        overlapping_speakers = sorted(
            {turn["speaker"] for span_start, span_end, turn in spans if span_start < char_end and span_end > char_start}
        )

        chunks.append(
            {
                "chunk_id": f"{meta['transcript_id']}_{meta['section']}_{chunk_size}_{chunk_index:03d}",
                "transcript_id": meta["transcript_id"],
                "company": meta["company"],
                "ticker": meta["ticker"],
                "date": meta["date"],
                "year": meta["year"],
                "quarter": meta["quarter"],
                "sector": meta["sector"],
                "section": meta["section"],
                "speakers": overlapping_speakers,
                "chunk_size": chunk_size,
                "chunk_index": chunk_index,
                "n_tokens": token_end - token_start,
                "text": chunk_text,
            }
        )
    return chunks


def chunk_transcript(records: list[dict], chunk_size: int) -> list[dict]:
    """Chunk a full transcript's preprocess.py output (all sections) into chunks."""
    sections: dict[str, list[dict]] = {}
    for record in records:
        sections.setdefault(record["section"], []).append(record)

    chunks = []
    for section_turns in sections.values():
        chunks.extend(chunk_section(section_turns, chunk_size))
    return chunks
