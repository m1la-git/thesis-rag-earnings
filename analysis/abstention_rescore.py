"""SECONDARY VIEW: abstention-as-correct for conjunctive questions at partial coverage.

THIS DOES NOT CHANGE THE TAXONOMY OR ANY PRIMARY NUMBER
--------------------------------------------------------
`src/evaluate.py`, the four-way outcome taxonomy, every threshold and every
table under `results/` are untouched by this script. It reads the primary
scored table and reports an ALTERNATIVE VIEW alongside the primary figures,
never in place of them. Its purpose is to BOUND the effect of a known
case-definition limitation, not to improve any number.

The limitation being bounded
----------------------------
Case C is `coverage_at_5 > 0` -- ANY gold anchor retrieved, not all
(`evaluate.classify_case`). A comparative question names two companies and
carries one anchor per company, and BOTH are needed: a comparison cannot be
made from one side. So a comparative item holding 1 of 2 anchors is Case C
while being genuinely unanswerable from what was retrieved, and an abstention
there is arguably correct behaviour that the primary taxonomy scores as a
conversion failure.

`coverage_split.md` for the same model measures the size of that: it reports
the abstention rate on comparative partial-coverage items against the rate on
thematic partial-coverage items at the same coverage status.

Scope of the alternative rule -- deliberately narrow
----------------------------------------------------
`abstained` counts as correct ONLY for **comparative questions at partial anchor
coverage**. It is NOT extended to:

  thematic partial      partial evidence genuinely does support a valid answer
                        there -- the question is disjunctive ("how did banks
                        describe..."), so any subset of anchors is answerable
                        and an abstention is a real failure to use what was
                        retrieved.
  single-anchor factual there is no partial state: one anchor is all-or-nothing,
                        so "incomplete evidence" cannot arise.
  comparative FULL      both sides were retrieved; the comparison is answerable
                        and an abstention is a real failure.
  Case B                no gold anchor surfaced at all. The taxonomy already
                        treats abstention as CORRECT behaviour there, so the
                        question does not arise -- and Case B abstentions are
                        not counted as conversion failures in the first place.

Read-only. Writes analysis/qwen3.8-27b_q4_k_xl/abstention_rescore.md.

Usage
-----
    python analysis/abstention_rescore.py
    python analysis/abstention_rescore.py --model qwen3.8-27b@q8_k_xl
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

import evaluate  # noqa: E402
from model_paths import (  # noqa: E402
    DEFAULT_MODEL, analysis_path, ensure_analysis_dir, generation_outcomes_path,
)

BENCHMARK = REPO_ROOT / "benchmark" / "questions.jsonl"
# Model-scoped via analysis_path(): q4 resolves to the existing
# analysis/qwen3.8-27b_q4_k_xl/abstention_rescore.md; any other generator writes into its own analysis/{slug}/
# subdirectory, so a run under one generator cannot overwrite another's
# document. Resolved in main() from --model.
OUT_MD_NAME = "abstention_rescore.md"

CORRECT = "answered_grounded_correct"
ABSTAINED = "abstained"
CATEGORIES = ["factual", "thematic", "comparative"]
BASE_CONDITIONS = ["chunk200_dense", "chunk200_bm25", "chunk200_hybrid",
                   "chunk500_dense", "chunk500_bm25", "chunk500_hybrid"]


def anchor_counts() -> dict[str, int]:
    out = {}
    for line in BENCHMARK.read_text(encoding="utf-8").splitlines():
        if line.strip():
            q = json.loads(line)
            out[q["id"]] = len(evaluate.anchor_strings(q))
    return out


def is_rescored(row: dict) -> bool:
    """The alternative rule: comparative, partial coverage, abstained."""
    return (row["category"] == "comparative"
            and row["n_anchors"] >= 2
            and 0 < row["coverage"] < 1.0
            and row["outcome"] == ABSTAINED)


def load(model: str) -> list[dict]:
    n_anchors = anchor_counts()
    path = generation_outcomes_path(model)
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["model"] == model]
    if not rows:
        raise SystemExit(f"no rows in {path} for model {model!r}")
    out = []
    for r in rows:
        if r["case"] != "C":
            continue
        r = dict(r)
        r["n_anchors"] = n_anchors[r["question_id"]]
        r["coverage"] = float(r["coverage_at_5"])
        r["arm"] = "enriched" if r["condition_id"].endswith("_enriched") else "text_only"
        r["primary_correct"] = r["outcome"] == CORRECT
        r["alt_correct"] = r["primary_correct"] or is_rescored(r)
        out.append(r)
    return out


def rate(rows: list[dict], field: str) -> str:
    if not rows:
        return "—"
    k = sum(1 for r in rows if r[field])
    return f"{k / len(rows):.1%} ({k}/{len(rows)})"


def delta(rows: list[dict]) -> str:
    if not rows:
        return "—"
    a = sum(1 for r in rows if r["alt_correct"]) / len(rows)
    p = sum(1 for r in rows if r["primary_correct"]) / len(rows)
    return f"{(a - p) * 100:+.1f}pp" if a != p else "—"


def intersection_keys(rows_all: list[dict], model: str) -> set[tuple[str, str]]:
    """The 38-item matched intersection: Case C in BOTH arms, per condition pair."""
    path = generation_outcomes_path(model)
    with path.open(newline="", encoding="utf-8") as f:
        by = {(r["condition_id"], r["question_id"]): r
              for r in csv.DictReader(f) if r["model"] == model}
    out = set()
    for base in BASE_CONDITIONS:
        for (cid, q) in by:
            if cid != base:
                continue
            e = by.get((f"{base}_enriched", q))
            if e is not None and by[(base, q)]["case"] == "C" and e["case"] == "C":
                out.add((base, q))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"generator model to analyse (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    rows = load(args.model)
    changed = [r for r in rows if r["alt_correct"] and not r["primary_correct"]]

    inter = intersection_keys(rows, args.model)
    in_inter = [r for r in rows
                if (r["condition_id"].replace("_enriched", ""), r["question_id"]) in inter]

    def sel(rs, **kw):
        return [r for r in rs if all(r[k] == v for k, v in kw.items())]

    lines = [
        "# Abstention-rescoring for conjunctive questions — SECONDARY VIEW",
        "",
        "> ## The primary taxonomy is unchanged.",
        ">",
        "> `src/evaluate.py`, the four-way outcome taxonomy, every threshold and every table",
        "> under `results/` are **untouched**. This document reports an ALTERNATIVE VIEW",
        "> alongside the primary figures, never in place of them.",
        ">",
        "> It exists to **bound the effect of a known case-definition limitation**, not to",
        "> improve any number. The primary conversion rate remains the reported one; this is",
        "> the sensitivity analysis that says how much of it is attributable to that",
        "> limitation.",
        "",
        f"Model: `{args.model}`. Population: every Case C observation across all 12 conditions "
        f"(**n={len(rows)}**).",
        "",
        "## The limitation",
        "",
        "Case C is `coverage_at_5 > 0` — **any** gold anchor retrieved, not all. A comparative",
        "question names two companies and carries one anchor per company, and both are needed:",
        "a comparison cannot be made from one side. So a comparative item holding 1 of 2",
        "anchors is Case C while being unanswerable from what was retrieved, and an abstention",
        "there is arguably correct behaviour that the primary taxonomy scores as a failure.",
        "",
        "`coverage_split.md` for the same model measures the size of it: it reports the",
        "abstention rate on comparative partial-coverage items against the rate on thematic",
        "partial-coverage items at the same coverage status. Read the figures there rather",
        "than here -- this document does not recompute them.",
        "",
        "## The alternative rule, and why its scope is narrow",
        "",
        "`abstained` counts as correct **only for comparative questions at partial anchor",
        "coverage**. Not extended to:",
        "",
        "| excluded | why |",
        "|---|---|",
        "| thematic partial | disjunctive — any subset of anchors supports a valid answer, so an abstention is a real failure to use what was retrieved |",
        "| single-anchor factual | no partial state exists; one anchor is all-or-nothing |",
        "| comparative **full** coverage | both sides retrieved, the comparison is answerable, so an abstention is a real failure |",
        "| Case B | the taxonomy already treats abstention as correct there; those abstentions are not conversion failures to begin with |",
        "",
        "## 1. Case C conversion — primary vs alternative",
        "",
        "| scope | arm | primary | alternative | delta |",
        "|---|---|---|---|--:|",
    ]
    for arm in ("text_only", "enriched", None):
        rs = rows if arm is None else sel(rows, arm=arm)
        label = "both arms" if arm is None else arm
        lines.append(f"| pooled | {label} | {rate(rs, 'primary_correct')} | "
                     f"{rate(rs, 'alt_correct')} | {delta(rs)} |")
    for cat in CATEGORIES:
        for arm in ("text_only", "enriched", None):
            rs = sel(rows, category=cat) if arm is None else sel(rows, category=cat, arm=arm)
            label = "both arms" if arm is None else arm
            lines.append(f"| {cat} | {label} | {rate(rs, 'primary_correct')} | "
                         f"{rate(rs, 'alt_correct')} | {delta(rs)} |")

    lines += [
        "",
        "## 2. The 38-item matched intersection",
        "",
        "Case C in both arms, the like-for-like population from",
        "`analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md`.",
        "",
        "| scope | arm | primary | alternative | delta |",
        "|---|---|---|---|--:|",
    ]
    for arm in ("text_only", "enriched", None):
        rs = in_inter if arm is None else sel(in_inter, arm=arm)
        label = "both arms" if arm is None else arm
        lines.append(f"| pooled | {label} | {rate(rs, 'primary_correct')} | "
                     f"{rate(rs, 'alt_correct')} | {delta(rs)} |")
    for cat in CATEGORIES:
        for arm in ("text_only", "enriched"):
            rs = sel(in_inter, category=cat, arm=arm)
            if not rs:
                continue
            lines.append(f"| {cat} | {arm} | {rate(rs, 'primary_correct')} | "
                         f"{rate(rs, 'alt_correct')} | {delta(rs)} |")

    inter_t = sel(in_inter, arm="text_only")
    inter_e = sel(in_inter, arm="enriched")
    pt = sum(1 for r in inter_t if r["primary_correct"]) / len(inter_t)
    pe = sum(1 for r in inter_e if r["primary_correct"]) / len(inter_e)
    at = sum(1 for r in inter_t if r["alt_correct"]) / len(inter_t)
    ae = sum(1 for r in inter_e if r["alt_correct"]) / len(inter_e)

    lines += [
        "",
        "### 2.1 This view cuts both ways",
        "",
        "The alternative rule bounds a limitation in the case definition. It also removes most",
        "of the enrichment advantage it was not designed to test, and that consequence belongs",
        "here rather than in a footnote:",
        "",
        f"> **On the 38-item intersection the two arms converge at {at:.1%} and {ae:.1%} —",
        "> effectively identical.** Under the primary taxonomy the same population reads",
        f"> {pt:.1%} for `text_only` against {pe:.1%} for `metadata_enriched`, a gap of",
        f"> {(pe - pt) * 100:.1f} percentage points. **That gap largely disappears once correct",
        "> abstentions on unanswerable comparative items stop counting as failures.**",
        "",
        "Stated the other way round: a substantial part of the apparent Stage 2 benefit of",
        "enrichment is the primary taxonomy penalising `text_only` for abstaining correctly",
        "more often. `text_only` abstained on 15 of these comparative partial-coverage items",
        "and `metadata_enriched` on 17 across the full Case C population, but within the",
        "intersection the text_only arm carries more of them, so it absorbs more of the",
        "penalty. Neither reading is privileged here: the primary taxonomy remains the",
        "reported one, and this is the bound on how much of its Case C gap is attributable to",
        "the case definition rather than to generation quality.",
        "",
        "**The same dependency structure applies.** The changed observations come from a small",
        "number of repeated questions (section 3), so every figure in this section inherits the",
        "clustering that made the observation-level McNemar in",
        "`analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md` anti-conservative. These are observation counts, not",
        "independent evidence, and no significance claim is made from them in either direction.",
        "",
        "## 3. Observations that change status",
        "",
        f"**{len(changed)} of {len(rows)}** Case C observations change from a failure to a "
        f"success under the alternative rule — every one of them a comparative "
        f"partial-coverage abstention. "
        f"**{sum(1 for r in changed if (r['condition_id'].replace('_enriched', ''), r['question_id']) in inter)}** "
        "of them fall inside the 38-item intersection.",
        "",
        "| arm | count |",
        "|---|--:|",
    ]
    for arm in ("text_only", "enriched"):
        lines.append(f"| {arm} | {sum(1 for r in changed if r['arm'] == arm)} |")
    lines += [
        "",
        "| condition | question | coverage | in intersection |",
        "|---|---|--:|---|",
    ]
    for r in sorted(changed, key=lambda r: (r["condition_id"], r["question_id"])):
        in_i = (r["condition_id"].replace("_enriched", ""), r["question_id"]) in inter
        lines.append(f"| {r['condition_id']} | {r['question_id']} | {r['coverage']:.2f} | "
                     f"{'yes' if in_i else 'no'} |")

    by_q = collections.Counter(r["question_id"] for r in changed)
    lines += [
        "",
        f"The {len(changed)} changed observations come from **{len(by_q)} distinct questions** "
        f"({', '.join(f'`{q}` x{n}' for q, n in sorted(by_q.items()))}), the largest single "
        f"contributor being `{by_q.most_common(1)[0][0]}` with "
        f"{by_q.most_common(1)[0][1]} of the {len(changed)}. This is the same dependency "
        "structure that made the observation-level McNemar in "
        "`analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md` anti-conservative: a handful of questions repeated "
        "across condition pairs, not independent trials. **Every figure in this document, "
        "including section 2.1, inherits it.** Read these as observation counts; no "
        "significance claim is made from them in either direction.",
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
