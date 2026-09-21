"""Diagnostic: how much transcript text does enrichment push out of the index?

Under `metadata_enriched` the P2 prefix is prepended to every chunk's indexed
string, and the combined string is truncated at build time to the encoder's
510-token content budget (`index.MAX_CONTENT_TOKENS`). At chunk_size=500 the
prefix therefore costs the tail of the chunk: some transcript tokens are
dropped from what the retrievers see.

Semantics, so the numbers are read correctly
--------------------------------------------
**Truncation reduces retrievability, not scorability.** Anchor matching runs
against raw `chunk["text"]`, which truncation never touches
(README.md invariant 1). An anchor sitting in a discarded tail therefore still
counts as a hit whenever its chunk is retrieved -- it is simply less likely to
be retrieved *on that anchor's own terms*, because the words the anchor is made
of are no longer in the indexed string.

So this measures EXPOSURE, not lost score: how many gold anchors sit in text
that the retrievers can no longer match against. A single-anchor question whose
only anchor lands in a tail is the case to worry about; a multi-anchor question
with one anchor in a tail is largely insulated.

Read-only. Touches no config, no results file, no frozen artifact.

Usage
-----
    python analysis/truncation_tail.py
"""

from __future__ import annotations

import csv
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
from model_paths import stage1_path  # noqa: E402

import pandas as pd  # noqa: E402

import evaluate  # noqa: E402
import index as index_mod  # noqa: E402
import ingest  # noqa: E402
from chunking import chunk_transcript  # noqa: E402
from preprocess import preprocess_transcript  # noqa: E402
from run_experiment import CHUNK_SIZES, load_questions, scored_questions  # noqa: E402

ENRICHED = index_mod.REPRESENTATION_METADATA_ENRICHED
OUT_CSV = stage1_path("truncation_tail.csv")
OUT_MD = stage1_path("truncation_tail.md")


def build_corpus_chunks(chunk_size: int) -> list[dict]:
    df = pd.read_parquet(ingest.TRANSCRIPTS_PATH)
    chunks: list[dict] = []
    for _, row in df.iterrows():
        chunks.extend(chunk_transcript(preprocess_transcript(row), chunk_size))
    return chunks


def analyse(chunk_size: int, questions: list[dict]) -> dict:
    chunks = build_corpus_chunks(chunk_size)
    stats = index_mod.attach_index_text(chunks, ENRICHED)

    # The kept prefix of the transcript text, in CHARACTERS: everything after
    # the blank-line joiner in the enriched string. Anything past this index in
    # chunk["text"] is the discarded tail.
    kept_chars = {}
    for c in chunks:
        body = c["index_text"].split(index_mod.ENRICHMENT_JOINER, 1)[1]
        kept_chars[c["chunk_id"]] = len(body)

    by_id = {c["chunk_id"]: c for c in chunks}
    truncated = [s for s in stats if s["truncated"]]
    dropped = [s["transcript_tokens_dropped"] for s in truncated]
    prefix_tokens = [s["prefix_tokens"] for s in stats]

    # Per-anchor exposure, over the WHOLE corpus rather than only each
    # question's own transcripts: retrieval is corpus-scoped, so an anchor can
    # in principle be matched by any chunk that contains it.
    anchor_rows = []
    for q in questions:
        own = set(q["transcript_ids"])
        for anchor in evaluate.anchor_strings(q):
            occurrences = 0
            in_tail = 0
            occurrences_own = 0
            in_tail_own = 0
            partial = 0
            for c in chunks:
                start = c["text"].find(anchor)
                if start < 0:
                    continue
                end = start + len(anchor)
                cut = kept_chars[c["chunk_id"]]
                touched = end > cut  # wholly or partly inside the discarded tail
                occurrences += 1
                in_tail += int(touched)
                if touched and start < cut:
                    partial += 1
                if c["transcript_id"] in own:
                    occurrences_own += 1
                    in_tail_own += int(touched)
            anchor_rows.append(
                {
                    "chunk_size": chunk_size,
                    "question_id": q["id"],
                    "category": q["category"],
                    "anchor": anchor,
                    "occurrences_corpus": occurrences,
                    "occurrences_in_tail": in_tail,
                    "occurrences_partially_in_tail": partial,
                    "occurrences_own_transcripts": occurrences_own,
                    "occurrences_own_in_tail": in_tail_own,
                    # An anchor is LOST to the index only if EVERY chunk that
                    # contains it has it (at least partly) in a discarded tail.
                    "fully_lost_to_index": occurrences > 0 and in_tail == occurrences,
                }
            )

    n_anchors = len(anchor_rows)
    lost = [r for r in anchor_rows if r["fully_lost_to_index"]]
    touched_any = [r for r in anchor_rows if r["occurrences_in_tail"] > 0]

    # Questions whose retrieval could actually change: at least one anchor
    # fully lost to the index.
    lost_by_q = Counter(r["question_id"] for r in lost)
    single_anchor_lost = [
        q["id"]
        for q in questions
        if len(evaluate.anchor_strings(q)) == 1 and lost_by_q.get(q["id"], 0) == 1
    ]

    return {
        "chunk_size": chunk_size,
        "n_chunks": len(chunks),
        "n_truncated": len(truncated),
        "pct_truncated": 100.0 * len(truncated) / len(chunks),
        "prefix_tokens_min": min(prefix_tokens),
        "prefix_tokens_mean": statistics.mean(prefix_tokens),
        "prefix_tokens_max": max(prefix_tokens),
        "dropped_mean": statistics.mean(dropped) if dropped else 0.0,
        "dropped_max": max(dropped) if dropped else 0,
        "dropped_total": sum(dropped),
        "n_anchors": n_anchors,
        "n_anchors_touching_a_tail": len(touched_any),
        "n_anchors_fully_lost": len(lost),
        "n_questions_with_a_lost_anchor": len(lost_by_q),
        "single_anchor_questions_lost": single_anchor_lost,
        "anchor_rows": anchor_rows,
    }


def main() -> int:
    questions = scored_questions(load_questions())
    print(f"{len(questions)} retrieval-scored questions, "
          f"{sum(len(evaluate.anchor_strings(q)) for q in questions)} anchors\n")

    results = []
    for size in CHUNK_SIZES:
        print(f"chunk_size={size}: chunking + enriching full corpus...")
        r = analyse(size, questions)
        results.append(r)
        print(f"  {r['n_truncated']}/{r['n_chunks']} chunks truncated ({r['pct_truncated']:.1f}%)")

    all_anchor_rows = [row for r in results for row in r["anchor_rows"]]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_anchor_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_anchor_rows)

    lines = [
        "# Truncated-tail diagnostic (`metadata_enriched`, format P2)",
        "",
        "How much transcript text the enrichment prefix pushes out of the indexed",
        f"string, at both chunk sizes. Budget: `index.MAX_CONTENT_TOKENS` = "
        f"{index_mod.MAX_CONTENT_TOKENS} content tokens "
        f"({index_mod.MAX_SEQ_LENGTH} max_seq_length - {index_mod.N_SPECIAL_TOKENS} special tokens).",
        "",
        "**Truncation reduces retrievability, not scorability.** Anchor matching runs",
        "against raw `chunk[\"text\"]`, which is never truncated, so an anchor in a",
        "discarded tail still counts as a hit if its chunk is retrieved -- it is just",
        "less likely to be retrieved on that anchor's own terms. These are exposure",
        "numbers, not lost score.",
        "",
        "## Chunks",
        "",
        "| chunk_size | chunks | truncated | % truncated | prefix tokens (min/mean/max) | dropped tokens among truncated (mean/max) | total dropped |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for r in results:
        lines.append(
            f"| {r['chunk_size']} | {r['n_chunks']} | {r['n_truncated']} | "
            f"{r['pct_truncated']:.1f}% | "
            f"{r['prefix_tokens_min']}/{r['prefix_tokens_mean']:.1f}/{r['prefix_tokens_max']} | "
            f"{r['dropped_mean']:.1f}/{r['dropped_max']} | {r['dropped_total']} |"
        )

    lines += [
        "",
        "## Gold anchors",
        "",
        "`touching a tail` = at least one chunk containing the anchor has it wholly or",
        "partly past the truncation point. `fully lost to the index` = EVERY chunk",
        "containing that anchor does, so no chunk's indexed string carries it any more.",
        "",
        "| chunk_size | anchors | touching a tail | fully lost to the index | questions with >=1 lost anchor | single-anchor questions fully lost |",
        "|---|--:|--:|--:|--:|--:|",
    ]
    for r in results:
        lines.append(
            f"| {r['chunk_size']} | {r['n_anchors']} | {r['n_anchors_touching_a_tail']} | "
            f"{r['n_anchors_fully_lost']} | {r['n_questions_with_a_lost_anchor']} | "
            f"{len(r['single_anchor_questions_lost'])} "
            f"{sorted(r['single_anchor_questions_lost']) if r['single_anchor_questions_lost'] else ''} |"
        )
    lines += ["", f"Per-anchor detail: `{OUT_CSV.name}`.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "\n".join(lines[lines.index("## Chunks"):]))
    print(f"-> {OUT_CSV.relative_to(REPO_ROOT)}")
    print(f"-> {OUT_MD.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
