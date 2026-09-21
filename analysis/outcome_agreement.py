"""Cross-arm outcome-label agreement: a table diff over two generators.

What this is
------------
A DIFF OF TWO PUBLISHED TABLES, nothing more. It reads the `outcome` column of
two `results/tables/<slug>/generation_outcomes.csv` files and reports how often
they agree on the same (condition, question).

What this is NOT
----------------
**It is not a scoring instrument.** It never calls `src/evaluate.py`, never
re-derives a case, never re-checks grounding, never opens a generation record.
Labels are read exactly as the scoring pass wrote them. That matters because the
whole point of the comparison is to hold the instrument fixed and vary only the
generator: re-scoring here would put a second, differently-versioned scorer in
the loop and the disagreement count would stop meaning what it says.

The case partition is a consequence, not an input. Cases come from Stage 1
retrieval, which no generator touches, so the two files MUST agree on `case` for
every shared key. That is asserted rather than assumed -- a mismatch would mean
one of the tables was built against different retrieval output, and every number
below would be comparing across grids.

Placement
---------
Flat in `analysis/`, per the layout rule: it is generator-independent in FORM
(it hardcodes no slug and takes both arms as arguments), so it is a generator
like the others, not a per-model document. Its OUTPUT is model-scoped -- the
document lands under the comparison arm's directory, since that is the arm the
comparison is about.

Validation
----------
No expectation set, under any model, and deliberately not in
`scripts/validate_all.py`. Its figures are computed and unchecked; the stamp at
the top of the document says so rather than leaving a reader to assume a silent
pass.

Usage
-----
    python analysis/outcome_agreement.py <baseline> <comparison>
    python analysis/outcome_agreement.py qwen3.8-27b@q8_k_xl qwen3.8-flash-next

Either argument may be a model identifier (`qwen3.8-27b@q8_k_xl`) or its
filesystem slug (`qwen3.8-27b_q8_k_xl`); both resolve to the same table.
"""

from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import (  # noqa: E402
    analysis_path, ensure_analysis_dir, generation_outcomes_path, model_slug,
)

OUT_MD_NAME = "outcome_agreement.md"

# Column order for the transition matrix. Fixed rather than derived from the
# data so the matrix keeps the same shape when a label happens to be absent
# from one arm -- an empty row is informative, a missing row is confusing.
OUTCOMES = [
    "abstained",
    "answered_grounded_correct",
    "answered_grounded_offtarget",
    "answered_ungrounded",
]
SHORT = {
    "abstained": "abstained",
    "answered_grounded_correct": "correct",
    "answered_grounded_offtarget": "offtarget",
    "answered_ungrounded": "ungrounded",
}
CATEGORIES = ["factual", "thematic", "comparative", "unanswerable"]
CASES = ["A", "B", "C"]

UNANSWERABLE = "unanswerable"

# Arms for which "produces no company misattribution" is an ESTABLISHED
# EMPIRICAL PROPERTY, not an assumption. The P1 paragraph below asserts it, so
# it may only be asserted where it was actually observed.
#
# This is deliberately a whitelist rather than a default. Asserted about an
# arbitrary arm the claim is simply false -- q8 names companies, and its
# ref_unans_01 substitution (Northern Trust answered with BNY Mellon's figures)
# is a company misattribution, the exact failure the paragraph calls impossible.
# An earlier draft emitted the claim for whichever arm was passed second and
# published that falsehood into a q8 document.
NO_COMPANY_NAMING = {"qwen3.8-flash-next"}


def load(model: str) -> tuple[dict, str]:
    """Rows of one arm's outcomes table, keyed by (condition_id, question_id).

    Returns the rows and the single model identifier the file records. The
    table is read WHOLE and its `model` column checked for homogeneity, rather
    than filtered by the argument: the identifier in the column (`...@q8_k_xl`)
    differs from the directory slug (`..._q8_k_xl`), and filtering on the wrong
    one silently yields zero rows instead of an error.
    """
    path = generation_outcomes_path(model)
    if not path.exists():
        sys.exit(f"no outcomes table for {model!r}: {path}")
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit(f"empty outcomes table: {path}")

    models = sorted({r["model"] for r in rows})
    if len(models) != 1:
        sys.exit(f"STOP: {path} mixes {len(models)} generators ({models}). "
                 "An agreement figure over a mixed table is meaningless.")

    keyed = {(r["condition_id"], r["question_id"]): r for r in rows}
    if len(keyed) != len(rows):
        sys.exit(f"STOP: {path} has duplicate (condition_id, question_id) keys.")
    return keyed, models[0]


def pct(n: int, d: int) -> str:
    return "n/a" if d == 0 else f"{100.0 * n / d:.1f}%"


def main() -> int:
    # See coverage_split.py: the document text is UTF-8 and echoing it to a
    # default Windows console raises UnicodeEncodeError after the file is
    # already written. Fixed on the print path, never in the text.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", help="model identifier or slug of the reference arm")
    parser.add_argument("comparison", help="model identifier or slug of the arm being checked")
    args = parser.parse_args()

    if model_slug(args.baseline) == model_slug(args.comparison):
        sys.exit("STOP: both arguments resolve to the same generator; "
                 "an arm cannot be compared against itself.")

    base, base_id = load(args.baseline)
    comp, comp_id = load(args.comparison)

    keys = sorted(set(base) & set(comp))
    only_base = sorted(set(base) - set(comp))
    only_comp = sorted(set(comp) - set(base))
    if not keys:
        sys.exit("STOP: the two tables share no (condition_id, question_id) key.")

    # Cases come from Stage 1, which no generator touches. A mismatch means the
    # two tables were built against different retrieval output.
    case_mismatch = [k for k in keys if base[k]["case"] != comp[k]["case"]]
    if case_mismatch:
        sys.exit(f"STOP: {len(case_mismatch)} shared key(s) disagree on `case`, "
                 "which is generator-independent. The two tables were not built "
                 f"against the same Stage 1 output. First: {case_mismatch[0]}")

    agree = [k for k in keys if base[k]["outcome"] == comp[k]["outcome"]]
    disagree = [k for k in keys if base[k]["outcome"] != comp[k]["outcome"]]

    by_cat = collections.Counter(comp[k]["category"] for k in disagree)
    by_case = collections.Counter(comp[k]["case"] for k in disagree)
    matrix = collections.Counter((base[k]["outcome"], comp[k]["outcome"]) for k in keys)

    # The predetermined slice: unanswerable disagreements. Counted, never
    # assumed -- the constraint paragraph below interpolates these.
    unans_dis = [k for k in disagree if comp[k]["category"] == UNANSWERABLE]
    unans_qs = sorted({q for _, q in unans_dis})
    informative = len(disagree) - len(unans_dis)

    lines = [
        "> **No validation surface.** This script has no expectation set, under any model, and "
        "is deliberately not part of `scripts/validate_all.py` -- there is no pinned figure for "
        "it to reproduce and no reference document to diff against. Every figure below is "
        "computed and unchecked. This is a property of the script, not a first-run state.",
        "",
        "# Cross-arm outcome-label agreement",
        "",
        f"Baseline: `{base_id}`. Comparison: `{comp_id}`.",
        "",
        f"Sources: `{generation_outcomes_path(args.baseline).relative_to(REPO_ROOT).as_posix()}`",
        f"and `{generation_outcomes_path(args.comparison).relative_to(REPO_ROOT).as_posix()}`.",
        "",
        "This is a **diff of two published tables**. Outcome labels are read exactly as the "
        "scoring pass wrote them; nothing here re-scores, re-derives a case, or re-checks "
        "grounding. Holding the instrument fixed is what makes the comparison a statement about "
        "the two generators rather than about two runs of the scorer.",
        "",
        "## 1. Overall agreement",
        "",
        "| quantity | n |",
        "|---|--:|",
        f"| shared (condition, question) keys | {len(keys)} |",
        f"| **agree** | **{len(agree)} ({pct(len(agree), len(keys))})** |",
        f"| disagree | {len(disagree)} ({pct(len(disagree), len(keys))}) |",
    ]
    if only_base or only_comp:
        lines += [
            f"| keys only in baseline | {len(only_base)} |",
            f"| keys only in comparison | {len(only_comp)} |",
        ]
    lines += [
        "",
    ]
    if only_base or only_comp:
        lines += [
            "**The two grids are not identical.** Every figure above and below is computed over "
            "the shared keys only; the unshared keys are excluded rather than counted as "
            "disagreements, since a missing record is not a differing label.",
            "",
        ]
    else:
        lines += [
            "Both arms cover the same grid exactly -- no key is present in one table and absent "
            "from the other, so nothing is excluded from the comparison.",
            "",
        ]

    lines += [
        "The `case` column is identical on all "
        f"{len(keys)} shared keys, as it must be: cases are computed from Stage 1 retrieval, "
        "which no generator touches. A mismatch would mean the two tables were built against "
        "different retrieval output, and this script stops rather than reporting one.",
        "",
        "## 2. Transition matrix",
        "",
        f"Rows are `{base_id}` (baseline); columns are `{comp_id}`. The diagonal is agreement.",
        "",
        "| baseline \\ comparison | " + " | ".join(SHORT[o] for o in OUTCOMES) + " | total |",
        "|---|" + "--:|" * (len(OUTCOMES) + 1),
    ]
    for row_o in OUTCOMES:
        cells = [matrix[(row_o, col_o)] for col_o in OUTCOMES]
        marked = [f"**{v}**" if row_o == col_o and v else str(v)
                  for v, col_o in zip(cells, OUTCOMES)]
        lines.append(f"| {SHORT[row_o]} | " + " | ".join(marked) + f" | {sum(cells)} |")
    col_totals = [sum(matrix[(r, c)] for r in OUTCOMES) for c in OUTCOMES]
    lines.append("| **total** | " + " | ".join(str(v) for v in col_totals)
                 + f" | {sum(col_totals)} |")

    off_diag = sorted(
        ((r, c, matrix[(r, c)]) for r in OUTCOMES for c in OUTCOMES
         if r != c and matrix[(r, c)]),
        key=lambda t: -t[2])
    lines += [
        "",
        "Off-diagonal cells, largest first:",
        "",
        "| baseline label | comparison label | n |",
        "|---|---|--:|",
    ]
    for r, c, n in off_diag:
        lines.append(f"| {SHORT[r]} | {SHORT[c]} | {n} |")

    lines += [
        "",
        "## 3. Disagreements by question category",
        "",
        "| category | disagreements | shared keys | rate |",
        "|---|--:|--:|--:|",
    ]
    for cat in CATEGORIES:
        n_cat = sum(1 for k in keys if comp[k]["category"] == cat)
        lines.append(f"| {cat} | {by_cat.get(cat, 0)} | {n_cat} | "
                     f"{pct(by_cat.get(cat, 0), n_cat)} |")
    lines.append(f"| **all** | **{len(disagree)}** | **{len(keys)}** | "
                 f"**{pct(len(disagree), len(keys))}** |")

    lines += [
        "",
        "## 4. Disagreements by case",
        "",
        "| case | disagreements | shared keys | rate |",
        "|---|--:|--:|--:|",
    ]
    for case in CASES:
        n_case = sum(1 for k in keys if comp[k]["case"] == case)
        lines.append(f"| {case} | {by_case.get(case, 0)} | {n_case} | "
                     f"{pct(by_case.get(case, 0), n_case)} |")
    lines.append(f"| **all** | **{len(disagree)}** | **{len(keys)}** | "
                 f"**{pct(len(disagree), len(keys))}** |")

    # --- The constraint on how the unanswerable slice may be read ------------
    #
    # Emitted as PROSE IN THE DOCUMENT, not as a comment here: a reader of the
    # agreement figure has to see it, and a comment in the generator reaches
    # nobody. Counts and question ids are interpolated, so the paragraph stays
    # true if the slice ever changes rather than freezing today's numbers.
    lines += [
        "",
        "## 5. What the disagreement count may and may not be read as",
        "",
    ]
    comp_no_companies = model_slug(args.comparison) in NO_COMPANY_NAMING
    if unans_dis and comp_no_companies:
        q_txt = (f"a single question (`{unans_qs[0]}`)" if len(unans_qs) == 1
                 else f"{len(unans_qs)} questions (" + ", ".join(f"`{q}`" for q in unans_qs) + ")")
        lines += [
            f"**The {len(unans_dis)} unanswerable "
            f"{'disagreement is' if len(unans_dis) == 1 else 'disagreements are'} predetermined and carry no "
            f"information.** `{comp_id}` does not name companies. P1 (company misattribution) is "
            f"structurally impossible for it, so these disagreements -- all attributable to "
            f"{q_txt} -- follow from that difference rather than from anything about how the two "
            "arms handle unanswerable questions. They are not evidence about unanswerable "
            "handling, and a sentence reading them as such would be describing an artifact of "
            "the comparison's construction.",
            "",
            f"**Of the {len(disagree)} disagreements, only the {informative} outside that slice "
            f"are informative** ({pct(informative, len(keys) - sum(1 for k in keys if comp[k]['category'] == UNANSWERABLE))} "
            "of the shared answerable keys). Quote that figure, not the raw total, wherever the "
            "disagreement count is being read as a difference between the generators.",
            "",
            f"The corresponding agreement figure restricted to answerable items is "
            f"{len(agree) - (sum(1 for k in keys if comp[k]['category'] == UNANSWERABLE) - len(unans_dis))}"
            f"/{len(keys) - sum(1 for k in keys if comp[k]['category'] == UNANSWERABLE)}.",
        ]
    elif unans_dis:
        lines += [
            f"**The {len(unans_dis)} unanswerable "
            f"{'disagreement is' if len(unans_dis) == 1 else 'disagreements are'} not "
            "interpreted here.** The predetermined-slice argument applies only to a comparison "
            "arm that names no companies, making P1 (company misattribution) structurally "
            f"impossible for it; that is not an established property of `{comp_id}`, so this "
            "script does not assert it. Check what drives these "
            f"{'disagreement' if len(unans_dis) == 1 else 'disagreements'} before reading them "
            "as evidence about unanswerable handling.",
        ]
    else:
        lines += [
            "No unanswerable item disagrees between the two arms, so there is no slice to "
            "discount and the full disagreement count is informative.",
        ]

    lines += [
        "",
        "This document reports agreement only. It makes no claim about which arm is more "
        "faithful: an outcome label is a mechanical verdict, and two arms differing on one says "
        "they were labelled differently, not that either was read.",
        "",
    ]

    ensure_analysis_dir(args.comparison)
    out_md = analysis_path(args.comparison, OUT_MD_NAME)
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"-> {out_md.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
