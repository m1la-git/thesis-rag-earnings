"""Descriptive statistics -- means, SDs and correlations over Stage 1 retrieval.

Why this exists
---------------
The chair's binding guidelines require one specific table of every quantitative
empirical thesis:

    "One table that needs be included in every quantitative empirical thesis, is
     the table including the descriptive statistics (i.e., means, standard
     deviations and correlations) which should be formatted in line with the
     guidelines of the APA."
        -- Guidelines_ScientificManuscripts.pdf p. 6

No artifact in this repo held a correlation matrix, so no such table could be
cited without inventing numbers. This generator produces it.

The source is NOT results/tables/retrieval_metrics.csv
------------------------------------------------------
That file is already aggregated -- one row per condition x breakdown x metric,
means only. An SD and a correlation need the underlying observations, which live
in `results/retrieval/*.jsonl` as `_type: question_result` records.

The CSV is still used, as a CHECK rather than a source: `assert_matches_csv()`
recomputes each condition's overall mean from the 480 observations and requires
it to reproduce the CSV's `overall_not_cross_category_comparable` rows. This
generator has no expectation set (see the stamp below), so that cross-artifact
agreement is the only thing standing between it and silent drift.

Unit of observation: the question x condition pair, n = 480
-----------------------------------------------------------
40 questions x 12 conditions. Two other units were available and rejected:

  - per condition (n = 12): the SD would be the dispersion of *means*, a much
    smaller and different quantity, and 12 points cannot carry a correlation.
  - per question (n = 40): the three manipulated factors do not vary at all
    within a question, so every design correlation would be exactly zero.

Only the question x condition pair is a unit at which chunk size, retrieval
strategy and indexing representation vary, which is what makes the correlation
column answer the thesis's hypotheses rather than describe the benchmark.

n = 40, not 45: the five unanswerable items carry no gold anchors, so anchor
coverage@5 and MRR@5 exclude them entirely -- they are dropped from the metric
denominator, never scored as a retrieval failure. Stage 1's own `run_meta`
records `n_questions: 40` for every condition, and that is asserted here.

Why no significance stars
-------------------------
The 480 observations are nested: 12 share each question, 40 share each
condition. The independence assumption behind a correlation's significance test
therefore does not hold, and starring these coefficients would assert a
structure the design does not have. The estimates are reported bare, and the
table note says what they are -- the same standing that
`analysis/matched_conversion.py` gives its post-hoc tests: descriptive of this
sample rather than confirmatory.

Collinearity is a property of the benchmark, not a nuisance
-----------------------------------------------------------
Anchor count is nearly determined by question category, and that is by design
rather than by accident: the question type IS the evidence requirement. A
factual question asks for one figure from one transcript and carries one anchor.
A comparative question cannot be answered from one side, so it carries two, one
per company. A thematic question asks what several banks said and carries two or
three. `n_transcript_ids` is therefore not merely correlated with the anchor
count -- it is EQUAL to it on all 40 questions (asserted below), which is why
only one of the two appears as a variable.

Read the anchor-count row as a statement about what the benchmark asks for, and
read its correlation with the category dummies as the design showing through,
not as a defect to be corrected away.

Read-only. Writes analysis/stage1/descriptives.md and, unless --skip-latex,
thesis/generated/table_descriptives.tex.

Usage
-----
    python analysis/descriptives.py
    python analysis/descriptives.py --skip-latex      # markdown only
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import stage1_path  # noqa: E402

RETRIEVAL_DIR = REPO_ROOT / "results" / "retrieval"
METRICS_CSV = REPO_ROOT / "results" / "tables" / "retrieval_metrics.csv"
LATEX_OUT = REPO_ROOT / "thesis" / "generated" / "table_descriptives.tex"
OUT_MD_NAME = "descriptives.md"

N_QUESTIONS = 40
N_CONDITIONS = 12
N_OBSERVATIONS = N_QUESTIONS * N_CONDITIONS

# Reference levels are omitted, as in any dummy coding: `dense` for strategy and
# `factual` for category. A dummy's correlation with an outcome is that level
# against ALL OTHERS POOLED, not against the reference alone -- stated in the
# document, because it is the easiest row in the table to misread.
#
# Labels are carried twice on purpose. LaTeX needs `vs.\ ` so the period does
# not take end-of-sentence spacing, and `@` is fine in both, but a LaTeX escape
# leaking into the markdown document is a defect the first run of this script
# actually produced.
VARIABLES = [
    ("chunk_size_500", "Chunk size (500 vs. 200)", "Chunk size (500 vs.\\ 200)"),
    ("strategy_bm25", "Retrieval strategy: BM25", "Retrieval strategy: BM25"),
    ("strategy_hybrid", "Retrieval strategy: hybrid", "Retrieval strategy: hybrid"),
    ("repr_enriched", "Indexing: metadata-enriched", "Indexing: metadata-enriched"),
    ("category_thematic", "Question category: thematic", "Question category: thematic"),
    ("category_comparative", "Question category: comparative", "Question category: comparative"),
    ("n_gold_anchors", "Number of gold anchors", "Number of gold anchors"),
    ("chunk_size_sensitive", "Chunk-size-sensitive anchor", "Chunk-size-sensitive anchor"),
    ("anchor_coverage_at_5", "Anchor coverage@5", "Anchor coverage@5"),
    ("mrr_at_5", "MRR@5", "MRR@5"),
]

# The stamp used by every generator with no expectation set, verbatim from
# coverage_split.py / outcome_agreement.py. This script is deliberately not
# added to scripts/validate_all.py and has no analysis/expectations/ entry.
NO_VALIDATION_SURFACE = (
    "> **No validation surface.** This script has no expectation set and "
    "validates nothing, under any model -- there is no pinned figure for it to "
    "reproduce and no reference document to diff against. Every figure below is "
    "computed and unchecked. This is a permanent property of this script, not a "
    "first-run state, and pinning a model does not change it."
)


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_observations() -> list[dict]:
    """One row per question x condition, read from Stage 1's persisted output.

    `indexing_representation` is read with a `text_only` default: the six
    text_only conditions were written before that field existed, so requiring it
    would fail on exactly the files invariant 5 froze. Their absence IS the
    evidence that they are the text_only arm.
    """
    rows = []
    files = sorted(RETRIEVAL_DIR.glob("*.jsonl"))
    if len(files) != N_CONDITIONS:
        raise SystemExit(f"expected {N_CONDITIONS} condition files in "
                         f"{RETRIEVAL_DIR}, found {len(files)}")

    for path in files:
        with path.open(encoding="utf-8") as fh:
            records = [json.loads(line) for line in fh if line.strip()]
        meta = records[0]
        if meta.get("_type") != "run_meta":
            raise SystemExit(f"{path.name}: first line is not run_meta")
        representation = meta.get("indexing_representation", "text_only")

        if meta.get("n_questions") != N_QUESTIONS:
            raise SystemExit(
                f"{path.name}: run_meta says n_questions="
                f"{meta.get('n_questions')!r}, expected {N_QUESTIONS}. The "
                "unanswerable exclusion is what makes this 40 rather than 45; "
                "a different value means that exclusion changed.")

        results = [r for r in records if r.get("_type") == "question_result"]
        if len(results) != N_QUESTIONS:
            raise SystemExit(f"{path.name}: {len(results)} question_result "
                             f"lines, expected {N_QUESTIONS}")

        for r in results:
            n_anchors = len(r["anchor_detail"])
            # Not a redundancy to tidy away later: the two are equal by
            # construction, so carrying both as variables would be exact
            # collinearity. Asserted so a future benchmark edit that breaks the
            # identity is caught here rather than silently changing the table.
            if n_anchors != len(r["transcript_ids"]):
                raise SystemExit(
                    f"{path.name}/{r['question_id']}: {n_anchors} anchors but "
                    f"{len(r['transcript_ids'])} transcript_ids. These were "
                    "equal on all 40 questions when this table was designed, "
                    "which is why only the anchor count is a variable.")

            m = r["retrieval_metrics"]
            rows.append({
                "condition_id": r["condition_id"],
                "question_id": r["question_id"],
                "category": r["category"],
                "chunk_size_500": 1 if r["chunk_size"] == 500 else 0,
                "strategy_bm25": 1 if r["retrieval_strategy"] == "bm25" else 0,
                "strategy_hybrid": 1 if r["retrieval_strategy"] == "hybrid" else 0,
                "repr_enriched": 1 if representation == "metadata_enriched" else 0,
                "category_thematic": 1 if r["category"] == "thematic" else 0,
                "category_comparative": 1 if r["category"] == "comparative" else 0,
                "n_gold_anchors": n_anchors,
                "chunk_size_sensitive": 1 if r["chunk_size_sensitive"] else 0,
                "anchor_coverage_at_5": float(m["anchor_coverage_at_5"]),
                "mrr_at_5": float(m["mean_reciprocal_rank_at_5"]),
            })

    if len(rows) != N_OBSERVATIONS:
        raise SystemExit(f"{len(rows)} observations, expected {N_OBSERVATIONS}")
    if len({r["question_id"] for r in rows}) != N_QUESTIONS:
        raise SystemExit("question ids are not the same 40 across conditions")
    return rows


def assert_matches_csv(rows: list[dict]) -> int:
    """Condition means must reproduce the published aggregate table.

    This generator has no expectation set, so this is the one check that would
    catch it drifting away from the artifact the thesis already cites.
    """
    wanted = {"anchor_coverage_at_5": "anchor_coverage_at_5",
              "mean_reciprocal_rank_at_5": "mrr_at_5"}
    checked = 0
    with METRICS_CSV.open(encoding="utf-8", newline="") as fh:
        for rec in csv.DictReader(fh):
            if rec["breakdown_type"] != "overall_not_cross_category_comparable":
                continue
            col = wanted.get(rec["metric"])
            if col is None:
                continue
            mine = [r[col] for r in rows if r["condition_id"] == rec["condition_id"]]
            if len(mine) != N_QUESTIONS:
                raise SystemExit(f"{rec['condition_id']}: {len(mine)} rows")
            if int(rec["n_scored"]) != N_QUESTIONS:
                raise SystemExit(f"{rec['condition_id']}: CSV n_scored="
                                 f"{rec['n_scored']}, expected {N_QUESTIONS}")
            if abs(float(np.mean(mine)) - float(rec["value"])) > 1e-12:
                raise SystemExit(
                    f"{rec['condition_id']}/{rec['metric']}: recomputed "
                    f"{np.mean(mine)!r} but retrieval_metrics.csv says "
                    f"{rec['value']!r}. The persisted aggregate and the "
                    "per-question records disagree -- do not publish either "
                    "until that is explained.")
            checked += 1
    if checked != N_CONDITIONS * 2:
        raise SystemExit(f"cross-checked {checked} condition means, expected "
                         f"{N_CONDITIONS * 2}")
    return checked


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------

def matrix(rows: list[dict]) -> np.ndarray:
    return np.array([[float(r[k]) for k, _, _t in VARIABLES] for r in rows])


def describe(data: np.ndarray) -> list[dict]:
    out = []
    for i, (key, label, _tex) in enumerate(VARIABLES):
        col = data[:, i]
        out.append({
            "key": key,
            "label": label,
            "label_tex": _tex,
            "mean": float(col.mean()),
            "sd": float(col.std(ddof=1)),
            "min": float(col.min()),
            "max": float(col.max()),
            "pct_zero": 100.0 * float((col == 0).sum()) / col.size,
            "skew": float(stats.skew(col)),
            "kurtosis": float(stats.kurtosis(col)),  # excess: normal == 0
        })
    return out


def correlations(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pearson = np.corrcoef(data, rowvar=False)
    spearman = stats.spearmanr(data).statistic
    return pearson, spearman


def fmt_r(x: float) -> str:
    """APA: no leading zero on a coefficient that cannot exceed 1.

    A value that rounds to zero prints as `.00`, never `-.00`. The design
    factors are exactly orthogonal by construction, so their intercorrelations
    come back as tiny signed floats; printing a minus sign on one would suggest
    a direction where there is no association at all.
    """
    s = f"{x:.2f}"
    if s in ("-0.00", "0.00", "-0.0", "0.0"):
        return ".00"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

NOTE_SENTENCES = [
    f"N = {N_OBSERVATIONS} observations, comprising {N_QUESTIONS} benchmark "
    f"questions crossed with {N_CONDITIONS} retrieval conditions.",

    "The five unanswerable benchmark items are excluded from both retrieval "
    "metrics -- they have no gold anchor to retrieve -- so the question count "
    f"here is {N_QUESTIONS}, not the 45 items in the benchmark.",

    "Dichotomous variables are coded 0/1. Retrieval strategy enters as "
    "indicators for BM25 and hybrid, and question category as indicators for "
    "thematic and comparative; dense and factual are carried implicitly and "
    "are not reference levels. Each indicator's correlation therefore "
    "contrasts the level it names against all the others pooled.",

    "Correlations are Pearson coefficients; for a dichotomous variable this is "
    "the point-biserial correlation, and for two dichotomous variables the phi "
    "coefficient.",

    "The observations are nested -- twelve share each question and forty share "
    "each condition -- so the independence assumption behind a significance "
    "test does not hold. No p-values or significance markers are reported: read "
    "these coefficients as descriptive of this sample rather than confirmatory.",

    "Anchor count is largely determined by question category because the "
    "question type is the evidence requirement: a factual question asks for one "
    "figure and carries one anchor, a comparative question cannot be answered "
    "from one side and carries one anchor per company, and a thematic question "
    "carries two or three. The number of transcripts a question spans is equal "
    "to its anchor count on all forty questions and is therefore not listed "
    "separately.",
]


def build_markdown(desc, pearson, spearman, checked) -> list[str]:
    L = [f"# Descriptive statistics -- Stage 1 retrieval, N = {N_OBSERVATIONS}",
         "",
         NO_VALIDATION_SURFACE,
         "",
         "Generated by `analysis/descriptives.py`. Generator-independent: "
         "retrieval never calls a generator, so this document serves all three "
         "arms and is filed in `analysis/stage1/` rather than under a model "
         "slug.",
         "",
         "## What is being described",
         "",
         f"One observation is one **question x condition** pair: {N_QUESTIONS} "
         f"benchmark questions x {N_CONDITIONS} conditions = "
         f"**{N_OBSERVATIONS} observations**, read from "
         "`results/retrieval/*.jsonl`.",
         "",
         f"**{N_QUESTIONS}, not 45.** The five unanswerable items carry no gold "
         "anchors, so anchor coverage@5 and MRR@5 exclude them from the "
         "denominator entirely rather than scoring them as retrieval failures. "
         "Every condition's `run_meta` records `n_questions: 40`, asserted at "
         "load time.",
         "",
         f"**Cross-checked against the published aggregate.** All "
         f"{checked} condition-level means recomputed here reproduce "
         "`results/tables/retrieval_metrics.csv` exactly (`breakdown_type = "
         "overall_not_cross_category_comparable`). That check exists because "
         "this script has no expectation set.",
         "",
         "## Table: means, standard deviations and correlations",
         ""]

    head = "| Variable | M | SD | " + " | ".join(str(i + 1) for i in range(len(VARIABLES) - 1)) + " |"
    L += [head, "|" + "---|" * (3 + len(VARIABLES) - 1)]
    for i, d in enumerate(desc):
        cells = [fmt_r(pearson[i, j]) if j < i else "" for j in range(len(VARIABLES) - 1)]
        L.append(f"| {i + 1}. {d['label']} | "
                 f"{d['mean']:.3f} | {d['sd']:.3f} | " + " | ".join(cells) + " |")
    L += ["", "*Note.* " + " ".join(NOTE_SENTENCES), ""]

    L += ["## Distributional diagnostics",
          "",
          "Reported so the assumption statement below rests on measured values "
          "rather than assertion. Kurtosis is excess kurtosis (0 = normal).",
          "",
          "| Variable | M | SD | Min | Max | % zero | Skew | Kurtosis |",
          "|---|---|---|---|---|---|---|---|"]
    for d in desc:
        L.append(f"| {d['label']} | {d['mean']:.3f} | "
                 f"{d['sd']:.3f} | {d['min']:.3f} | {d['max']:.3f} | "
                 f"{d['pct_zero']:.1f}% | {d['skew']:.2f} | {d['kurtosis']:.2f} |")
    L.append("")

    cov = desc[VARIABLE_INDEX["anchor_coverage_at_5"]]
    mrr = desc[VARIABLE_INDEX["mrr_at_5"]]
    L += ["### What that means for Pearson",
          "",
          f"Both outcomes are bounded in [0, 1] and zero-inflated: anchor "
          f"coverage@5 is exactly zero on **{cov['pct_zero']:.1f}%** of the "
          f"{N_OBSERVATIONS} observations and MRR@5 on "
          f"**{mrr['pct_zero']:.1f}%**, with skew "
          f"{cov['skew']:.2f} and {mrr['skew']:.2f} respectively. Neither is "
          "normally distributed, and MRR@5 is additionally discrete -- a "
          "per-anchor reciprocal rank can only be one of "
          "{1, 1/2, 1/3, 1/4, 1/5, 0} before averaging across a question's "
          "anchors.",
          "",
          "Pearson's *estimate* remains a valid measure of linear association "
          "under non-normality; what non-normality invalidates is the "
          "significance test and confidence interval built on it. That is a "
          "second reason, independent of the nesting, why no p-values are "
          "reported.",
          "",
          "## Spearman rank correlations (secondary)",
          "",
          "Reported for comparison only, and **not** as the robust answer: with "
          f"anchor coverage@5 exactly zero on {cov['pct_zero']:.1f}% of "
          "observations, the tie mass at the bottom of the ranking is large "
          "enough that the rank transform discards much of what distinguishes "
          "the conditions. Where Spearman and Pearson disagree here, read it as "
          "a statement about the tie structure rather than about robustness.",
          ""]
    L += [head, "|" + "---|" * (3 + len(VARIABLES) - 1)]
    for i, d in enumerate(desc):
        cells = [fmt_r(spearman[i, j]) if j < i else "" for j in range(len(VARIABLES) - 1)]
        L.append(f"| {i + 1}. {d['label']} | "
                 f"{d['mean']:.3f} | {d['sd']:.3f} | " + " | ".join(cells) + " |")
    L.append("")
    return L


def fmt_r_tex(x: float) -> str:
    """As fmt_r, but with a real minus sign.

    A bare `-` in LaTeX text mode sets a hyphen, which is visibly shorter than
    the minus APA expects and reads as a dash in a column of numbers.
    """
    s = fmt_r(x)
    return "$-$" + s[1:] if s.startswith("-") else s


def build_latex(desc, pearson) -> list[str]:
    ncol = len(VARIABLES) - 1
    L = ["% GENERATED by analysis/descriptives.py -- do not edit.",
         "%",
         "% Rows only. The float, caption and label live in",
         "% chapters/98_TablesFigures.tex, per the guideline that tables sit",
         "% after the references, one per page.",
         "%",
         "% Correlations carry no significance markers ON PURPOSE. The 480",
         "% observations are nested (12 per question, 40 per condition), so the",
         "% independence assumption behind a significance test does not hold.",
         "% Do not add stars.",
         "\\setlength{\\tabcolsep}{3pt}",
         "\\footnotesize",
         "\\begin{tabular}{@{}l" + "r" * (2 + ncol) + "@{}}",
         "\\toprule",
         "Variable & \\multicolumn{1}{c}{$M$} & \\multicolumn{1}{c}{$SD$} & "
         + " & ".join(f"\\multicolumn{{1}}{{c}}{{{i + 1}}}" for i in range(ncol))
         + " \\\\",
         "\\midrule"]
    for i, d in enumerate(desc):
        cells = [fmt_r_tex(pearson[i, j]) if j < i else "" for j in range(ncol)]
        L.append(f"{i + 1}. {d['label_tex']} & {d['mean']:.3f} & {d['sd']:.3f} & "
                 + " & ".join(cells) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\normalsize"]
    return L


VARIABLE_INDEX = {k: i for i, (k, _, _t) in enumerate(VARIABLES)}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-latex", action="store_true",
                    help="write the markdown only; leave thesis/generated/ alone")
    args = ap.parse_args()

    rows = load_observations()
    checked = assert_matches_csv(rows)
    data = matrix(rows)
    desc = describe(data)
    pearson, spearman = correlations(data)

    print(f"observations: {len(rows)} = {N_QUESTIONS} questions x "
          f"{N_CONDITIONS} conditions")
    print(f"cross-checked {checked} condition means against "
          f"{METRICS_CSV.relative_to(REPO_ROOT)} -- all exact")
    print("*** No validation surface: no expectation set exists for this "
          "script, under any model. Figures are computed and unchecked.")

    out_md = stage1_path(OUT_MD_NAME)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(build_markdown(desc, pearson, spearman, checked)),
                      encoding="utf-8")
    print(f"wrote {out_md.relative_to(REPO_ROOT)}")

    if args.skip_latex:
        print(f"--skip-latex: {LATEX_OUT.relative_to(REPO_ROOT)} NOT written")
    else:
        LATEX_OUT.parent.mkdir(parents=True, exist_ok=True)
        LATEX_OUT.write_text("\n".join(build_latex(desc, pearson)) + "\n",
                             encoding="utf-8")
        print(f"wrote {LATEX_OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
