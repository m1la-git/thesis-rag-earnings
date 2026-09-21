"""Diagnostic: the four questions that scored non-zero under `text_only` and
zero in all six `metadata_enriched` conditions.

`ref_comp_10`, `ref_fact_08`, `ref_them_06`, `ref_them_15` are the questions
enrichment cost. The purpose here is to separate two very different causes:

  * a loss concentrated at chunk500 implicates **truncation** -- the enriched
    500-token index drops ~9 tokens off the tail of 92% of chunks;
  * a loss that also occurs at chunk200 implicates the **prefix displacing
    topical match** -- chunk200 has ZERO truncation (0/7918 chunks), so nothing
    is missing from the indexed string there. Any loss at 200 is the ~19-token
    metadata line changing what the retrievers rank, not lost content.

That distinction is clean precisely because chunk200 truncates nothing.

Truncation membership reuses `analysis/truncation_tail.py`'s own logic
(imported, not reimplemented) so "is this anchor in a discarded tail" is decided
by the same code that produced the tail diagnostic.

Read-only. Writes one Markdown report; changes nothing.

Usage
-----
    python analysis/lost_questions.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
from model_paths import stage1_path  # noqa: E402
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import evaluate  # noqa: E402
import index as index_mod  # noqa: E402
from truncation_tail import ENRICHED, build_corpus_chunks  # noqa: E402

RETRIEVAL_DIR = REPO_ROOT / "results" / "retrieval"
OUT_MD = stage1_path("lost_questions.md")

LOST = ["ref_comp_10", "ref_fact_08", "ref_them_06", "ref_them_15"]
STRATEGIES = ("dense", "bm25", "hybrid")
SIZES = (200, 500)


def condition_id(size: int, strategy: str, enriched: bool) -> str:
    return f"chunk{size}_{strategy}" + ("_enriched" if enriched else "")


def load(condition: str) -> dict:
    out = {}
    for line in (RETRIEVAL_DIR / f"{condition}.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row["_type"] == "question_result":
            out[row["question_id"]] = row
    return out


def truncation_index(chunk_size: int) -> dict[str, tuple[str, int]]:
    """chunk_id -> (raw chunk text, character index where the discarded tail begins).

    Uses truncation_tail.py's own chunk build and index.attach_index_text, so
    tail membership is decided by exactly the code that produced the published
    tail diagnostic rather than a second implementation of it.
    """
    chunks = build_corpus_chunks(chunk_size)
    index_mod.attach_index_text(chunks, ENRICHED)
    return {
        c["chunk_id"]: (c["text"], len(c["index_text"].split(index_mod.ENRICHMENT_JOINER, 1)[1]))
        for c in chunks
    }


def tail_status(anchor: str, chunk_id: str | None, cut_index: dict) -> str:
    """Whether `anchor` falls wholly or partly past the truncation point.

    Same rule as truncation_tail.py: the anchor is affected when its END lies
    beyond the kept prefix.
    """
    if not chunk_id:
        return "no matching chunk"
    entry = cut_index.get(chunk_id)
    if entry is None:
        return "chunk not in corpus build"
    text, cut = entry
    start = text.find(anchor)
    if start < 0:
        return "anchor not in that chunk"
    end = start + len(anchor)
    if end <= cut:
        return "no — fully inside the kept prefix"
    return "**YES — partly in tail**" if start < cut else "**YES — wholly in tail**"


def main() -> int:
    records = {
        condition_id(s, st, e): load(condition_id(s, st, e))
        for s in SIZES for st in STRATEGIES for e in (False, True)
    }

    print("building chunk500 enriched index_text for tail membership...")
    cut500 = truncation_index(500)

    lines = [
        "# The four questions `metadata_enriched` lost",
        "",
        "`ref_comp_10`, `ref_fact_08`, `ref_them_06`, `ref_them_15` score non-zero in at",
        "least one `text_only` condition and **zero in all six `metadata_enriched`**",
        "conditions.",
        "",
        "**Why the 200/500 split is diagnostic.** chunk200 truncates *nothing* under the",
        "frozen P2 format (0 of 7918 chunks); chunk500 truncates 2985 of 3239, dropping a",
        "mean of 9.4 tokens. So a loss that appears at chunk200 cannot be caused by missing",
        "content — there is none missing — and implicates the ~19-token metadata prefix",
        "changing what the retrievers rank. A loss confined to chunk500 is consistent with",
        "truncation.",
        "",
        "Tail membership below is computed with `analysis/truncation_tail.py`'s own logic.",
        "",
    ]

    summary = []
    for qid in LOST:
        nonzero_to = [
            (condition_id(s, st, False),
             records[condition_id(s, st, False)][qid]["retrieval_metrics"]["anchor_coverage_at_5"])
            for s in SIZES for st in STRATEGIES
            if records[condition_id(s, st, False)][qid]["retrieval_metrics"]["anchor_coverage_at_5"] > 0
        ]
        sizes_affected = sorted({int(c.split("_")[0].replace("chunk", "")) for c, _ in nonzero_to})

        # Locus is decided by the TAIL EVIDENCE, not by which chunk size the
        # question happened to score in. Concluding "chunk500 only, therefore
        # truncation" would be an inference from co-occurrence; the tail check
        # answers it directly, and for all four questions it answers "no".
        any_tail = False
        for size in sizes_affected:
            if size != 500:
                continue
            for st in STRATEGIES:
                rec = records[condition_id(500, st, False)][qid]
                if rec["retrieval_metrics"]["anchor_coverage_at_5"] == 0:
                    continue
                for a in rec["anchor_detail"]:
                    if "YES" in tail_status(a["anchor"], a["chunk_id"], cut500):
                        any_tail = True

        where = ("chunk200 only" if sizes_affected == [200]
                 else "chunk500 only" if sizes_affected == [500] else "both sizes")
        if any_tail:
            locus = f"{where} — at least one anchor IS in a discarded tail: **truncation**"
        else:
            locus = (f"{where} — no anchor is in a discarded tail, so **not truncation**; "
                     "the anchor's chunk fell out of the top-5 by rank: **prefix displacement**")

        lines += [f"## `{qid}`", "",
                  f"Scored non-zero in {len(nonzero_to)} of 6 `text_only` conditions. "
                  f"Loss locus: {locus}.", "",
                  "| text_only condition | coverage@5 |", "|---|--:|"]
        for c, v in nonzero_to:
            lines.append(f"| {c} | {v} |")
        lines += ["", "Per-anchor rank, matched condition vs its enriched counterpart "
                      "(rank is within the 50-deep logged ranking; `>50` = not found at all):", "",
                  "| condition | anchor | text_only rank | enriched rank | in a truncated tail? |",
                  "|---|---|--:|--:|---|"]

        for s in SIZES:
            for st in STRATEGIES:
                to_id, en_id = condition_id(s, st, False), condition_id(s, st, True)
                to_rec, en_rec = records[to_id][qid], records[en_id][qid]
                if to_rec["retrieval_metrics"]["anchor_coverage_at_5"] == 0:
                    continue
                en_detail = {a["anchor"]: a for a in en_rec["anchor_detail"]}
                for a in to_rec["anchor_detail"]:
                    e = en_detail[a["anchor"]]
                    tail = ("n/a (chunk200 truncates nothing)" if s == 200
                            else tail_status(a["anchor"], a["chunk_id"], cut500))
                    lines.append(
                        f"| {to_id} | `{a['anchor'][:48]}…` | "
                        f"{a['rank'] if a['rank'] else '>50'} | "
                        f"{e['rank'] if e['rank'] else '>50'} | {tail} |"
                    )
        lines.append("")
        summary.append((qid, locus, len(nonzero_to)))

    lines += ["## Summary", "", "| question | non-zero text_only conditions | loss locus |",
              "|---|--:|---|"]
    for qid, locus, n in summary:
        lines.append(f"| {qid} | {n}/6 | {locus} |")
    lines += [
        "",
        "**None of the four is a truncation loss.** Every anchor involved sits fully inside",
        "the kept prefix, including the chunk500 cases. In each question the anchor's chunk",
        "was still found — it simply fell below rank 5 in the enriched index (3→7, 5→7,",
        "3→11, 2→14, 3→12). These are rank-displacement losses: the metadata prefix changed",
        "what outranked what, not what was available to match.",
        "",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"-> {OUT_MD.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
