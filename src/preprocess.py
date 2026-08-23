"""Clean transcripts, split sections, and attach metadata.

ThisTakes raw transcripts from ingest.py and produces per-turn records with
prepared-remarks vs. Q&A sections split out (via `structured_content`) and
per-record metadata attached: company, ticker, date, year, quarter, sector,
section, speaker. Output feeds chunking.py.

Section split heuristic: the Q&A section is assumed to start at the first
post-welcome Operator turn that either mentions "operator instruction(s)"
or hands off to the first analyst question (e.g. "our first question comes
from..."). The welcome turn (index 0) is always skipped, since it commonly
repeats the "operator instructions" boilerplate without being the actual
handoff. If no such turn is found, the whole transcript is treated as
prepared remarks. Validated against all 128 transcripts in the frozen
corpus (data/corpus_manifest.json) with zero anomalies (no missing split,
no zero-length section either side).
"""

import pandas as pd

SECTOR = "banks"

SECTION_PREPARED = "prepared_remarks"
SECTION_QA = "qa"

QA_MARKER = "operator instruction"


def find_qa_start_index(structured_content) -> int | None:
    """First post-welcome Operator turn carrying the marker, else None."""
    for i, turn in enumerate(structured_content):
        if i == 0 or turn["speaker"] != "Operator":
            continue
        text = turn["text"].lower()
        if QA_MARKER in text:
            return i
        if "first question" in text and any(w in text for w in ("from", "with", "go")):
            return i
    return None


def preprocess_transcript(row: pd.Series) -> list[dict]:
    """Turn one transcripts.parquet row into a list of per-turn records.

    Each record carries the turn's speaker/text plus the metadata required
    downstream: company, ticker, date, year, quarter, sector,
    section, speaker.
    """
    structured_content = row["structured_content"]
    qa_start = find_qa_start_index(structured_content)

    records = []
    for i, turn in enumerate(structured_content):
        section = SECTION_QA if qa_start is not None and i >= qa_start else SECTION_PREPARED
        records.append(
            {
                "transcript_id": row["transcript_id"],
                "company": row["company_name"],
                "ticker": row["symbol"],
                "date": row["date"],
                "year": int(row["year"]),
                "quarter": int(row["quarter"]),
                "sector": SECTOR,
                "section": section,
                "speaker": turn["speaker"],
                "turn_index": i,
                "text": turn["text"],
            }
        )
    return records
