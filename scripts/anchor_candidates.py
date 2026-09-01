"""Filter the corpus index down to the safe pool for gold-anchor selection.

Dev/analysis tool. Reads `analysis/benchmark_authoring/corpus_index.json` and keeps only the
figure-sentences that sit **fully inside a single chunk under BOTH the 200- and
500-token configs**, grouped by ticker then quarter, preserving the index's
salience ranking.

Why this filter
---------------
A gold anchor is scored by substring containment against retrieved chunk text
(README.md, "Design"). If a sentence straddles a chunk boundary, an anchor
taken from it can fail the substring test under one chunk size while passing
under the other -- manufacturing a difference between conditions that has
nothing to do with retrieval quality. Restricting the candidate pool to
sentences contained under both configs removes that failure mode up front:
15.33% of sentences straddle at 200 tokens and 6.17% at 500, so roughly one in
five is unsafe to draw from.

This does NOT author anything. It selects and reorders material already in the
index; the questions, the anchors and the reference answers are the
researcher's.

Outputs (both carry the full, untruncated, unescaped sentence):
  analysis/benchmark_authoring/anchor_candidates.md   browsable, grouped by ticker then quarter
  analysis/benchmark_authoring/anchor_candidates.csv  same rows, for sorting/filtering elsewhere
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = REPO_ROOT / "analysis" / "benchmark_authoring" / "corpus_index.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "analysis" / "benchmark_authoring"

CHUNK_SIZES = (200, 500)

CSV_COLUMNS = [
    "ticker", "transcript_id", "year", "quarter", "date", "rank", "salient",
    "figure", "kind", "corpus_doc_freq", "section", "speaker", "turn_index",
    "chunk_id@200", "chunk_id@500", "sentence_char_start", "sentence_char_end",
    "sentence",
]


def is_contained_in_both(figure: dict) -> bool:
    """True when the sentence sits inside exactly one chunk under every config."""
    return all(len(figure.get(f"chunk_ids@{size}", [])) == 1 for size in CHUNK_SIZES)


def collect(index: dict, salient_only: bool, max_doc_freq: int | None) -> list[dict]:
    """Flatten the index into candidate rows, preserving per-transcript order.

    `entry["figures"]` is already ordered salient-first then by position, so
    enumerating it in place is what preserves the salience ranking.
    """
    rows: list[dict] = []
    for entry in index["transcripts"]:
        rank = 0
        for figure in entry["figures"]:
            if not is_contained_in_both(figure):
                continue
            if salient_only and not figure["salient"]:
                continue
            if max_doc_freq is not None and figure["corpus_doc_freq"] > max_doc_freq:
                continue
            rank += 1
            rows.append(
                {
                    "ticker": entry["ticker"],
                    "company": entry["company"],
                    "transcript_id": entry["transcript_id"],
                    "year": entry["year"],
                    "quarter": entry["quarter"],
                    "date": entry["date"][:10],
                    "rank": rank,
                    "salient": figure["salient"],
                    "figure": figure["figure"],
                    "kind": figure["kind"],
                    "corpus_doc_freq": figure["corpus_doc_freq"],
                    "section": figure["section"],
                    "speaker": figure["speaker"],
                    "turn_index": figure["turn_index"],
                    "chunk_id@200": figure["chunk_ids@200"][0],
                    "chunk_id@500": figure["chunk_ids@500"][0],
                    "sentence_char_start": figure["sentence_char_start"],
                    "sentence_char_end": figure["sentence_char_end"],
                    "sentence": figure["sentence"],
                }
            )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    """Write the rows with proper quoting.

    utf-8-sig so Excel reads the curly apostrophes correctly; the BOM sits at the
    start of the file only, so a sentence copied out of a cell is still exact.
    """
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(rows: list[dict], index: dict, filters: dict) -> str:
    """Group into ticker -> transcript sections, sentences verbatim in blockquotes.

    Blockquotes rather than table cells on purpose: this file exists to be copied
    from, and a table would force truncating long sentences and escaping pipes.
    No sentence in the pool contains a newline or a pipe, so every line below is
    the exact source text.
    """
    total_figures = sum(len(e["figures"]) for e in index["transcripts"])
    by_ticker: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_ticker[row["ticker"]].append(row)

    lines = [
        "# Gold-anchor candidates",
        "",
        f"{len(rows)} of {total_figures} figure-sentences from `corpus_index.json`, keeping only",
        "those contained **inside a single chunk under both the 200- and 500-token configs**.",
        "",
        "**Why filtered.** An anchor is scored by substring containment against retrieved chunk",
        "text. A sentence straddling a chunk boundary can fail that test under one chunk size",
        "while passing under the other, inventing a difference between conditions that has",
        "nothing to do with retrieval quality. About one sentence in five is unsafe that way",
        "(15.33% straddle at 200 tokens, 6.17% at 500); none of them are below.",
        "",
        "**Sentences here are exact.** Not truncated, not escaped — unlike the tables in",
        "`corpus_index.md`. Copy anchor text from here, from the CSV, or from the JSON.",
        "",
        "**Picking an anchor.** Take roughly 5–15 words from *within* a sentence rather than the",
        "whole thing, and avoid its very first and last few words — that leaves headroom so the",
        "anchor stays clear of the chunk edges even though the sentence already does.",
        "",
        f"**Ordering.** Salience ranking is preserved from the index: within each transcript, "
        "figures whose sentence (or its predecessor) carries a finance term come first. Entries "
        "marked `context-only` did not, and are ranked below.",
        "",
        "`df` = how many transcripts corpus-wide state this same value; **`df 1` means the value",
        "is unique to this transcript**, which is what makes a clean single-source factual question.",
        "",
        f"**Filters applied.** salient only: `{filters['salient_only']}` · "
        f"max corpus df: `{filters['max_doc_freq'] or 'none'}`",
        "",
        "---",
        "",
    ]

    for ticker in sorted(by_ticker):
        ticker_rows = by_ticker[ticker]
        lines += [f"## {ticker} — {ticker_rows[0]['company']} ({len(ticker_rows)} candidates)", ""]

        by_transcript: dict[str, list[dict]] = defaultdict(list)
        for row in ticker_rows:
            by_transcript[row["transcript_id"]].append(row)

        for transcript_id in sorted(by_transcript, key=lambda t: (by_transcript[t][0]["year"], by_transcript[t][0]["quarter"])):
            group = by_transcript[transcript_id]
            head = group[0]
            lines += [
                f"### {transcript_id} · {head['year']} Q{head['quarter']} · {head['date']} "
                f"({len(group)} candidates)",
                "",
            ]
            for row in group:
                flags = [row["section"] == "qa" and "Q&A" or "prep", f"df {row['corpus_doc_freq']}"]
                if not row["salient"]:
                    flags.append("context-only")
                lines += [
                    f"{row['rank']}. **{row['figure']}** · {' · '.join(flags)} · "
                    f"`{row['chunk_id@200']}` / `{row['chunk_id@500']}`",
                    f"   > {row['sentence']}",
                    "",
                ]

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--salient-only",
        action="store_true",
        help="drop candidates whose sentence carries no finance term",
    )
    parser.add_argument(
        "--max-doc-freq",
        type=int,
        help="keep only values stated in at most N transcripts corpus-wide (1 = unique)",
    )
    args = parser.parse_args()

    if not args.index.exists():
        raise SystemExit(f"missing {args.index} -- run scripts/build_corpus_index.py first")
    index = json.loads(args.index.read_text(encoding="utf-8"))

    rows = collect(index, args.salient_only, args.max_doc_freq)
    if not rows:
        raise SystemExit("no candidates matched the given filters")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    md_path = args.out_dir / "anchor_candidates.md"
    csv_path = args.out_dir / "anchor_candidates.csv"
    filters = {"salient_only": args.salient_only, "max_doc_freq": args.max_doc_freq}
    md_path.write_text(render_markdown(rows, index, filters), encoding="utf-8")
    write_csv(rows, csv_path)

    total = sum(len(e["figures"]) for e in index["transcripts"])
    unique = sum(1 for r in rows if r["corpus_doc_freq"] == 1)
    salient = sum(1 for r in rows if r["salient"])
    print(
        f"{len(rows)} candidates of {total} figure-sentences "
        f"({len(rows) / total:.1%} contained under both configs)\n"
        f"  {salient} salient, {len(rows) - salient} context-only\n"
        f"  {unique} state a value unique to their transcript (df 1)\n"
        f"  across {len({r['transcript_id'] for r in rows})} transcripts, "
        f"{len({r['ticker'] for r in rows})} tickers"
    )
    print(f"Wrote {md_path} and {csv_path}")


if __name__ == "__main__":
    main()
