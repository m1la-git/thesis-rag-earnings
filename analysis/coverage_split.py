"""Case C conversion split by anchor coverage: conjunctive vs disjunctive questions.

The hypothesis
--------------
The benchmark's categories differ on two dimensions at once, and the second one
is not part of the experimental design:

  factual      names 1 company, 1 anchor.
  thematic     names no company ("how did banks describe..."), 2-3 anchors, any
               subset of which supports a valid answer -- DISJUNCTIVE.
  comparative  names 2 companies, 2 anchors, and BOTH are needed. A comparison
               cannot be made from one side -- CONJUNCTIVE.

Case C membership is verified below to be `coverage_at_5 > 0` -- ANY anchor, not
all. So a comparative item holding 1 of 2 anchors is Case C while being
genuinely unanswerable from what was retrieved, and an abstention there may be
correct behaviour being scored as a conversion failure.

Verified from the code, not assumed
-----------------------------------
`evaluate.classify_case`: `CASE_B if coverage_at_5 == 0 else CASE_C`, where
`evaluate.anchor_coverage_at_5` returns `matched / len(gold_anchors)`. So Case C
is the ANY-anchor condition. If that ever becomes an ALL-anchor condition this
whole analysis changes shape, so it is asserted at run time rather than trusted.

Coverage groups
---------------
  full       coverage_at_5 == 1.0 and the question has >= 2 anchors
  partial    0 < coverage_at_5 < 1.0
  single     the question has exactly 1 anchor -- full by definition, reported
             SEPARATELY so it distorts neither of the other two groups

Read-only. Writes analysis/qwen3.8-27b_q4_k_xl/coverage_split.md.

Usage
-----
    python analysis/coverage_split.py
    python analysis/coverage_split.py --model qwen3.8-27b@q8_k_xl
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import (  # noqa: E402
    analysis_path, ensure_analysis_dir, generation_outcomes_path,
)

import evaluate  # noqa: E402

RETRIEVAL_DIR = REPO_ROOT / "results" / "retrieval"

# Model-scoped: results/tables/{model_slug}/generation_outcomes.csv
# Resolved per --model so a q8 table is never read under a q4 label.
BENCHMARK = REPO_ROOT / "benchmark" / "questions.jsonl"
# Model-scoped via analysis_path(): q4 resolves to the existing
# analysis/qwen3.8-27b_q4_k_xl/coverage_split.md; any other generator writes into its own analysis/{slug}/
# subdirectory, so a run under one generator cannot overwrite another's
# document. Resolved in main() from --model.
OUT_MD_NAME = "coverage_split.md"

DEFAULT_MODEL = "qwen3.8-27b@q4_k_xl"
CORRECT = "answered_grounded_correct"
OUTCOMES = ["abstained", CORRECT, "answered_grounded_offtarget", "answered_ungrounded"]
CATEGORIES = ["factual", "thematic", "comparative"]
GROUPS = ["single (1 anchor)", "full (>=2 anchors, all matched)", "partial (some but not all)"]
MIN_N = 5


def assert_case_c_is_any_anchor() -> str:
    """Confirm Case C is the ANY-anchor condition before anything is computed."""
    q = {"id": "x", "category": "factual", "question": "q",
         "transcript_ids": ["T"], "gold_anchors": ["a", "b"], "reference_answer": "r"}
    partial = evaluate.classify_case(q, 0.5)
    zero = evaluate.classify_case(q, 0.0)
    full = evaluate.classify_case(q, 1.0)
    if not (partial == evaluate.CASE_C and full == evaluate.CASE_C and zero == evaluate.CASE_B):
        raise SystemExit(
            "STOP: evaluate.classify_case does not treat partial coverage as Case C "
            f"(coverage 0.5 -> {partial!r}, 1.0 -> {full!r}, 0.0 -> {zero!r}). "
            "This analysis assumes Case C is the ANY-anchor condition; it changes shape "
            "if Case C requires all anchors. Reporting rather than adapting."
        )
    return ("`evaluate.classify_case` returns Case C for coverage 0.5 and 1.0, Case B for "
            "0.0 -- Case C is the **ANY-anchor** condition, asserted at run time.")


def anchor_counts() -> dict[str, int]:
    out = {}
    for line in BENCHMARK.read_text(encoding="utf-8").splitlines():
        if line.strip():
            q = json.loads(line)
            out[q["id"]] = len(evaluate.anchor_strings(q))
    return out


_rank_cache: dict[str, dict] = {}


def top5_chunk_ids(condition_id: str, question_id: str) -> list[str]:
    """The five chunk_ids that entered the context for one observation."""
    if condition_id not in _rank_cache:
        recs = {}
        for line in (RETRIEVAL_DIR / f"{condition_id}.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec.get("_type") == "question_result":
                recs[rec["question_id"]] = rec
        _rank_cache[condition_id] = recs
    return [c["chunk_id"] for c in _rank_cache[condition_id][question_id]["ranking"][:5]]


def distractor_counts(rows: list[dict], transcript_ids: dict[str, list[str]]) -> dict:
    """Per arm, how many of the top-5 belong to neither named company.

    Two granularities, because they answer different questions:

      company-level     the chunk's TICKER is neither of the two the question
                        names. A chunk from the right bank's wrong quarter is
                        NOT a distractor here.
      transcript-level  the chunk is not from one of the question's own
                        transcript_ids, so the right bank's wrong quarter DOES
                        count. Stricter, and closer to what the answer actually
                        needs, since a comparison is quarter-specific.
    """
    out = {}
    for arm in ("text_only", "enriched"):
        co, tr = [], []
        for r in rows:
            if r["arm"] != arm:
                continue
            tids = set(transcript_ids[r["question_id"]])
            tickers = {t.split("_")[0] for t in tids}
            ids = top5_chunk_ids(r["condition_id"], r["question_id"])
            co.append(sum(1 for c in ids
                          if evaluate.transcript_id_from_chunk_id(c).split("_")[0] not in tickers))
            tr.append(sum(1 for c in ids
                          if evaluate.transcript_id_from_chunk_id(c) not in tids))
        out[arm] = {
            "n": len(co),
            "company_mean": sum(co) / len(co) if co else 0.0,
            "company_median": sorted(co)[len(co) // 2] if co else 0,
            "transcript_mean": sum(tr) / len(tr) if tr else 0.0,
            "transcript_median": sorted(tr)[len(tr) // 2] if tr else 0,
        }
    return out


def group_of(n_anchors: int, coverage: float) -> str:
    if n_anchors <= 1:
        return GROUPS[0]
    return GROUPS[1] if coverage >= 1.0 else GROUPS[2]


def rate(n_correct: int, n: int) -> str:
    return f"{n_correct / n:.0%}" if n else "n/a"


def cell(rows: list[dict]) -> str:
    if not rows:
        return "—"
    n = len(rows)
    k = sum(1 for r in rows if r["outcome"] == CORRECT)
    flag = " ⚠" if n < MIN_N else ""
    return f"{rate(k, n)} ({k}/{n}){flag}"


def main() -> int:
    # The document text contains non-ASCII characters (a warning sign in the
    # full-vs-partial table). write_text() encodes UTF-8 explicitly and always
    # succeeded, but echoing the same text to a default Windows console encodes
    # with cp1252 and raised UnicodeEncodeError -- after the file was written,
    # so the document was correct and the process still exited non-zero.
    #
    # Fixed on the PRINT PATH only. The characters themselves are unchanged:
    # they are byte-identical in all three arms' committed documents, and
    # editing them to suit a console encoding would dirty tracked files for a
    # terminal's benefit. errors="replace" so a console that still cannot
    # represent a character degrades that character rather than the exit code.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):  # non-reconfigurable stream (pipe, capture)
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"generator model to analyse (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    case_c_note = assert_case_c_is_any_anchor()
    n_anchors = anchor_counts()

    with generation_outcomes_path(args.model).open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["model"] == args.model]
    if not rows:
        raise SystemExit(f"no rows for model {args.model!r}")

    case_c = []
    for r in rows:
        if r["case"] != "C":
            continue
        r = dict(r)
        r["n_anchors"] = n_anchors[r["question_id"]]
        r["coverage"] = float(r["coverage_at_5"])
        r["group"] = group_of(r["n_anchors"], r["coverage"])
        r["arm"] = "enriched" if r["condition_id"].endswith("_enriched") else "text_only"
        case_c.append(r)

    def sel(**kw):
        return [r for r in case_c if all(r[k] == v for k, v in kw.items())]

    lines = [
        "# Case C conversion by anchor coverage: conjunctive vs disjunctive questions",
        "",
        f"Model: `{args.model}`. Population: every Case C observation across all 12 conditions "
        f"(**n={len(case_c)}**).",
        "",
        "## How Case C is determined — verified, not assumed",
        "",
        f"{case_c_note}",
        "",
        "`evaluate.anchor_coverage_at_5` returns `matched / len(gold_anchors)`, and",
        "`evaluate.classify_case` is `CASE_B if coverage_at_5 == 0 else CASE_C`. So a",
        "**comparative item holding 1 of 2 anchors is Case C** while being unanswerable from",
        "what was actually retrieved: a comparison cannot be made from one side. An abstention",
        "there is arguably correct behaviour scored as a conversion failure.",
        "",
        "## Coverage groups",
        "",
        "| group | definition |",
        "|---|---|",
        "| single | the question has exactly 1 gold anchor — full by definition, reported separately |",
        "| full | >= 2 anchors, all matched within top-5 (coverage = 1.0) |",
        "| partial | >= 2 anchors, some but not all matched (0 < coverage < 1.0) |",
        "",
        f"Cells with n < {MIN_N} are flagged ⚠.",
        "",
        "## Anchor structure of the benchmark",
        "",
        "| category | questions | anchors per question |",
        "|---|--:|---|",
    ]
    bench_cat = {}
    for r in rows:
        bench_cat.setdefault(r["category"], {})[r["question_id"]] = n_anchors[r["question_id"]]
    for cat in CATEGORIES:
        d = bench_cat.get(cat, {})
        dist = collections.Counter(d.values())
        lines.append(f"| {cat} | {len(d)} | " +
                     ", ".join(f"{k} anchor{'s' if k > 1 else ''}: {v} q" for k, v in sorted(dist.items())) + " |")

    lines += [
        "",
        "## Conversion rate by coverage group, per category, per arm",
        "",
        "Cell = conversion rate (correct / n).",
        "",
        "| category | arm | " + " | ".join(GROUPS) + " |",
        "|---|---|---|---|---|",
    ]
    for cat in CATEGORIES:
        for arm in ("text_only", "enriched"):
            cells = [cell(sel(category=cat, arm=arm, group=g)) for g in GROUPS]
            lines.append(f"| {cat} | {arm} | " + " | ".join(cells) + " |")
    lines += ["", "Both arms pooled (the coverage effect is not about representation):", "",
              "| category | " + " | ".join(GROUPS) + " |", "|---|---|---|---|"]
    for cat in CATEGORIES:
        lines.append(f"| {cat} | " + " | ".join(cell(sel(category=cat, group=g)) for g in GROUPS) + " |")

    lines += [
        "",
        "## The key contrast: coverage sensitivity, thematic vs comparative",
        "",
        "Both have >= 2 anchors, so both have a meaningful full/partial split. Thematic is",
        "disjunctive (any subset supports an answer); comparative is conjunctive (both sides",
        "needed).",
        "",
        "| category | full | partial | difference (full − partial) |",
        "|---|---|---|---|",
    ]
    for cat in ("thematic", "comparative"):
        full_rows, part_rows = sel(category=cat, group=GROUPS[1]), sel(category=cat, group=GROUPS[2])
        fk = sum(1 for r in full_rows if r["outcome"] == CORRECT)
        pk = sum(1 for r in part_rows if r["outcome"] == CORRECT)
        if full_rows and part_rows:
            diff = f"{fk/len(full_rows) - pk/len(part_rows):+.0%}"
        else:
            diff = "n/a"
        lines.append(f"| {cat} | {cell(full_rows)} | {cell(part_rows)} | {diff} |")

    lines += [
        "",
        "## Comparative partial-coverage items — outcome breakdown",
        "",
        "These are the items the hypothesis says may be unanswerable-by-construction: a",
        "comparison with only one side retrieved. Does the model abstain (arguably correct) or",
        "answer off-target?",
        "",
        "| arm | n | " + " | ".join(o.replace("answered_grounded_", "").replace("answered_", "")
                                    for o in OUTCOMES) + " |",
        "|---|--:|--:|--:|--:|--:|",
    ]
    for arm in ("text_only", "enriched", None):
        rr = sel(category="comparative", group=GROUPS[2]) if arm is None else \
            sel(category="comparative", group=GROUPS[2], arm=arm)
        counts = [sum(1 for r in rr if r["outcome"] == o) for o in OUTCOMES]
        label = "both pooled" if arm is None else arm
        lines.append(f"| {label} | {len(rr)} | " + " | ".join(str(c) for c in counts) + " |")

    lines += [
        "",
        "For contrast, the same breakdown for **thematic** partial-coverage items:",
        "",
        "| arm | n | " + " | ".join(o.replace("answered_grounded_", "").replace("answered_", "")
                                    for o in OUTCOMES) + " |",
        "|---|--:|--:|--:|--:|--:|",
    ]
    for arm in ("text_only", "enriched", None):
        rr = sel(category="thematic", group=GROUPS[2]) if arm is None else \
            sel(category="thematic", group=GROUPS[2], arm=arm)
        counts = [sum(1 for r in rr if r["outcome"] == o) for o in OUTCOMES]
        label = "both pooled" if arm is None else arm
        lines.append(f"| {label} | {len(rr)} | " + " | ".join(str(c) for c in counts) + " |")
    lines.append("")

    # --- Distractor displacement -------------------------------------------
    tids = {}
    for line in BENCHMARK.read_text(encoding="utf-8").splitlines():
        if line.strip():
            q = json.loads(line)
            tids[q["id"]] = q["transcript_ids"]
    comp_c = [r for r in case_c if r["category"] == "comparative"]
    dc = distractor_counts(comp_c, tids)

    lines += [
        "## Distractor displacement in comparative Case C top-5s",
        "",
        "Mean number of the five retrieved chunks belonging to **neither named company**, over",
        "every comparative Case C observation. If enrichment clears off-company chunks out of",
        "the context window, this falls.",
        "",
        "Two granularities, because they answer different questions. **Company-level** counts a",
        "chunk as a distractor only if its ticker is neither of the two the question names — a",
        "chunk from the right bank's wrong quarter is not a distractor. **Transcript-level**",
        "counts anything outside the question's own `transcript_ids`, so the right bank's wrong",
        "quarter does count; that is stricter and closer to what a quarter-specific comparison",
        "actually needs.",
        "",
        "| granularity | arm | n | mean of 5 | median |",
        "|---|---|--:|--:|--:|",
    ]
    for arm in ("text_only", "enriched"):
        d = dc[arm]
        lines.append(f"| company-level | {arm} | {d['n']} | {d['company_mean']:.2f} | {d['company_median']} |")
    for arm in ("text_only", "enriched"):
        d = dc[arm]
        lines.append(f"| transcript-level | {arm} | {d['n']} | {d['transcript_mean']:.2f} | {d['transcript_median']} |")

    d_co = dc["enriched"]["company_mean"] - dc["text_only"]["company_mean"]
    d_tr = dc["enriched"]["transcript_mean"] - dc["text_only"]["transcript_mean"]
    lines += [
        "",
        f"Difference (enriched − text_only): **{d_co:+.2f}** chunks company-level, "
        f"**{d_tr:+.2f}** chunks transcript-level.",
        "",
        "**Read the company-level figure cautiously.** The median is 0 in both arms, so most",
        "comparative Case C observations already had no off-company chunk under `text_only`;",
        f"the {abs(d_co):.2f}-chunk mean difference comes from a minority of observations and is",
        "small in absolute terms. The transcript-level figure is the larger movement",
        f"({abs(d_tr):.2f} of 5 slots), and is the one that would carry a distractor-displacement",
        "claim if one is made. Neither is a significance test.",
        "",
    ]

    lines.insert(0, "> **No validation surface.** This script has no expectation set and validates nothing, under any model -- there is no pinned figure for it to reproduce and no reference document to diff against. Every figure below is computed and unchecked. This is a permanent property of this script, not a first-run state, and pinning a model does not change it.")
    lines.insert(1, "")
    ensure_analysis_dir(args.model)
    out_md = analysis_path(args.model, OUT_MD_NAME)
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"-> {out_md.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
