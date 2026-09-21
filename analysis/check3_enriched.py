"""Check 3 (attribution exposure) on the metadata_enriched arm.

Check 3 asks: how many items have at least one **substantive** numeric claim
supported ONLY by chunks from a transcript outside the question's own
`transcript_ids` -- a figure the answer attaches to a company/quarter that
cannot be verified as belonging there. `classify_outcome` verifies that a number
is present *somewhere* in the retrieved top-5, not that it belongs where the
answer puts it.

`analysis/qwen3.8-27b_q4_k_xl/check3_attribution_postfix.md` publishes the post-fix figure for the
text_only Case C `answered_grounded_correct` population. This extends the same
measurement to the enriched arm.

Method: unchanged, and NOT reimplemented
----------------------------------------
`trace`, `is_substantive` and `retrieved_chunks` are imported from
`analysis/check3_attribution_postfix.py` -- the module whose `--validate` mode
reproduces its own published figures. Re-deriving the rule here would be a
second implementation that could silently diverge.

That module's own triviality rule is preserved: substantive = not a bare year
2022-2026 and not a bare digit 1-4. That is deliberately NOT
`evaluate.is_trivial_claim`.

Validate before extending
-------------------------
`--validate` restricts to the six text_only conditions and asserts the result
reproduces this model's pinned text_only figure exactly. Only after that does
anything enriched get computed. The same protocol licensed the post-fix figures
twice already.

Populations reported
--------------------
1. enriched Case C `answered_grounded_correct`, against the text_only figure;
2. the same, restricted to the Task 3 **intersection** -- Case C in BOTH arms --
   so the comparison is like-for-like rather than confounded by the population
   change that enrichment causes;
3. broken down by retrieval strategy.

Assertions
----------
`--validate` checks the pinned text_only figure. The full run additionally
asserts every
ENRICHED figure this document publishes, because those are the ones that can
drift -- the text_only side is frozen by construction. All expectations are
loaded per `--model` from `analysis/expectations/{model_slug}.json`. The q4 set
holds exactly the numbers that were previously hardcoded here. A model with no
expectation set is announced as FIRST RUN and its figures are reported as
unpinned -- never as passing. The script refuses to write the document if a
pinned figure moves.

Read-only. Writes a NEW file; does not touch check3_attribution_postfix.md.

Usage
-----
    python analysis/check3_enriched.py --validate
    python analysis/check3_enriched.py
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
    analysis_path, ensure_analysis_dir, expectations_path, generation_outcomes_path,
    load_expectations,
)
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import check3_attribution_postfix as c3  # noqa: E402

# Model-scoped: results/tables/{model_slug}/generation_outcomes.csv
# Resolved per --model so a q8 table is never read under a q4 label.
# Output paths are model-scoped via analysis_path(): under q4 they resolve to the
# existing analysis/check3_enriched.{md,csv}; every other generator writes into
# its own analysis/{slug}/ subdirectory, so a q8 run cannot overwrite a q4
# document. Resolved in main() from --model, not at import time.
OUT_MD_NAME = "check3_enriched.md"
OUT_CSV_NAME = "check3_enriched.csv"

DEFAULT_MODEL = "qwen3.8-27b@q4_k_xl"
BASE_CONDITIONS = ["chunk200_dense", "chunk200_bm25", "chunk200_hybrid",
                   "chunk500_dense", "chunk500_bm25", "chunk500_hybrid"]
CORRECT = "answered_grounded_correct"
STRATEGIES = ["dense", "bm25", "hybrid"]


def load_rows(model: str) -> list[dict]:
    with generation_outcomes_path(model).open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["model"] == model]
    if not rows:
        raise SystemExit(f"no rows for model {model!r}")
    return rows


def is_enriched(condition_id: str) -> bool:
    return condition_id.endswith("_enriched")


def strategy_of(condition_id: str) -> str:
    return condition_id.replace("_enriched", "").split("_")[1]


def intersection_keys(rows: list[dict]) -> set[tuple[str, str]]:
    """(base_condition, question) that are Case C in BOTH arms -- Task 3's set."""
    by = {(r["condition_id"], r["question_id"]): r for r in rows}
    out = set()
    for base in BASE_CONDITIONS:
        for (cid, q) in list(by):
            if cid != base:
                continue
            e = by.get((f"{base}_enriched", q))
            if e is not None and by[(base, q)]["case"] == "C" and e["case"] == "C":
                out.add((base, q))
    return out


def flag(rows: list[dict], questions: dict) -> list[dict]:
    return [c3.trace(r, questions, c3.POST_FIX1_RE) for r in rows]


def summarise(traced: list[dict]) -> tuple[int, int]:
    return sum(1 for t in traced if t["flagged"]), len(traced)


def pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.0f}%" if d else "n/a"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"generator model to analyse (default: {DEFAULT_MODEL})")
    parser.add_argument("--validate", action="store_true",
                        help="reproduce the published text_only 9/30 and exit")
    args = parser.parse_args()

    c3.MODEL = args.model  # the imported module's trace() reads this for cache paths
    questions = c3.load_questions()
    rows = load_rows(args.model)

    text_only_c = [r for r in rows if not is_enriched(r["condition_id"])
                   and r["case"] == "C" and r["outcome"] == CORRECT]
    n_flag_t, n_t = summarise(flag(text_only_c, questions))

    exp = load_expectations(args.model)
    first_run = exp is None
    out_md = analysis_path(args.model, OUT_MD_NAME)
    out_csv = analysis_path(args.model, OUT_CSV_NAME)

    print(f"Validation -- text_only Case C {CORRECT} population:")
    if first_run:
        # A missing expectation set is FIRST RUN, never a pass. Note what this
        # costs while it lasts: the text_only gate below is the guard that stops
        # the enriched figures being computed on a population that has already
        # moved, and until this model is pinned there is NO gate at all. That is
        # a real loosening, so it is announced rather than left silent.
        print(f"  {n_flag_t}/{n_t} ({pct(n_flag_t, n_t)})   expected: NOTHING PINNED")
        print(f"  *** FIRST RUN -- no expectation set for model {args.model!r}")
        print(f"  *** nothing was validated against; the text_only gate did NOT run")
        print(f"  *** pin deliberately by creating "
              f"{expectations_path(args.model).relative_to(REPO_ROOT).as_posix()}")
        if args.validate:
            return 0
    else:
        exp_t = tuple(exp["check3_enriched"]["text_only_gate"])
        print(f"  {n_flag_t}/{n_t} ({pct(n_flag_t, n_t)})   "
              f"expected {exp_t[0]}/{exp_t[1]} ({pct(exp_t[0], exp_t[1])})")
        ok = (n_flag_t, n_t) == exp_t
        print("  " + ("PASS -- reproduces the published post-fix figure exactly"
                      if ok else "MISMATCH -- do NOT trust the enriched figures below"))
        if not ok:
            return 1
        if args.validate:
            return 0

    enriched_c = [r for r in rows if is_enriched(r["condition_id"])
                  and r["case"] == "C" and r["outcome"] == CORRECT]
    traced_e = flag(enriched_c, questions)
    n_flag_e, n_e = summarise(traced_e)

    inter = intersection_keys(rows)
    inter_t = [r for r in text_only_c if (r["condition_id"], r["question_id"]) in inter]
    inter_e = [r for r in enriched_c
               if (r["condition_id"].replace("_enriched", ""), r["question_id"]) in inter]
    ft, nt_ = summarise(flag(inter_t, questions))
    fe, ne_ = summarise(flag(inter_e, questions))

    # Strictly matched: correct in BOTH arms. The intersection above still has
    # unequal n per arm, because an item only enters Check 3's population if it
    # was classified `correct` in that arm -- so it controls for Case C
    # membership but not for the correct/not-correct split. This does both, and
    # is the only fully paired comparison available.
    both_correct = {
        (r["condition_id"], r["question_id"]) for r in inter_t
    } & {
        (r["condition_id"].replace("_enriched", ""), r["question_id"]) for r in inter_e
    }
    bc_t = [r for r in inter_t if (r["condition_id"], r["question_id"]) in both_correct]
    bc_e = [r for r in inter_e
            if (r["condition_id"].replace("_enriched", ""), r["question_id"]) in both_correct]
    fbt, nbt = summarise(flag(bc_t, questions))
    fbe, nbe = summarise(flag(bc_e, questions))

    traced_t = flag(text_only_c, questions)
    by_strategy = {}
    for s in STRATEGIES:
        t = [x for x in traced_t if strategy_of(x["condition_id"]) == s]
        e = [x for x in traced_e if strategy_of(x["condition_id"]) == s]
        by_strategy[s] = (summarise(t), summarise(e))

    # --- Assert the ENRICHED figures, which are the ones that can drift -----
    #
    # The text_only 9/30 checked above is the frozen side: it is a statement
    # about six conditions whose records and labels are fixed, so it cannot move
    # and asserting it alone proves almost nothing. Every figure below is on the
    # enriched arm or a matched population involving it -- the side that moves if
    # a generation is re-scored, a condition is re-run, or a population filter
    # changes. That asymmetry is exactly what let check3_attribution_postfix
    # silently broaden from 9/30 to 20/109 while its own --validate kept passing.
    #
    # Expectations are per-model DATA, loaded from
    # analysis/expectations/{model_slug}.json, NOT literals here. The q4 set
    # holds exactly the values that used to be hardcoded at this spot. A model
    # with no set is FIRST RUN: figures are computed and reported as UNPINNED,
    # never as passing, so a second generator can neither inherit q4's pins nor
    # quietly skip the check.
    computed = [
        ("enriched Case C answered_grounded_correct", n_flag_e, n_e),
        ("intersection text_only", ft, nt_),
        ("intersection enriched", fe, ne_),
        ("strictly matched text_only", fbt, nbt),
        ("strictly matched enriched", fbe, nbe),
    ]
    for strategy in ("dense", "bm25", "hybrid"):
        (tf, tn), (ef, en) = by_strategy[strategy]
        computed.append((f"strategy {strategy} text_only", tf, tn))
        computed.append((f"strategy {strategy} enriched", ef, en))

    failures = []
    if first_run:
        print(f"\n*** FIRST RUN -- no expectation set for model {args.model!r}.")
        print("*** The figures below were COMPUTED AND NOT CHECKED against anything.")
        for label, got_f, got_n in computed:
            print(f"  ----  {label:<42} {got_f}/{got_n} ({pct(got_f, got_n)})   unpinned")
    else:
        expected = exp["check3_enriched"]["figures"]
        print("\nPublished enriched-arm figures:")
        for label, got_f, got_n in computed:
            exp_f, exp_n = expected[label]
            ok_row = (got_f, got_n) == (exp_f, exp_n)
            print(f"  {'PASS' if ok_row else 'FAIL'}  {label:<42} "
                  f"{got_f}/{got_n} ({pct(got_f, got_n)})   expected {exp_f}/{exp_n}")
            if not ok_row:
                failures.append(f"{label}: computed {got_f}/{got_n}, expected {exp_f}/{exp_n}")
    if failures:
        print("\n  REFUSING TO WRITE -- a published figure has moved:")
        for f_ in failures:
            print(f"    {f_}")
        print("  This is a finding, not something to accommodate. Either the scored\n"
              "  table changed, or a population filter did. Do not update the\n"
              "  expected values without establishing which.")
        return 1
    print("  all reproduce exactly" if not first_run
          else "  NOTHING CHECKED -- FIRST RUN, figures above are unpinned")

    ensure_analysis_dir(args.model)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list((traced_t + traced_e)[0].keys()))
        w.writeheader()
        w.writerows(traced_t + traced_e)

    lines = [
        "# Check 3 (attribution exposure) — the `metadata_enriched` arm",
        "",
        f"Model: `{args.model}`. Population: Case C `{CORRECT}`.",
        "",
        "Method imported unchanged from `analysis/check3_attribution_postfix.py`, whose",
        "This script re-asserts the pinned post-fix `text_only` figure for the model in",
        "scope before computing anything enriched, and exits if it does not reproduce.",
        "Expectations are per-model; a model with no pinned set runs unchecked and says so.",
        "",
        "An item is flagged when at least one **substantive** numeric claim is supported ONLY",
        "by chunks outside the question's own `transcript_ids`. `substantive` = not a bare",
        "year 2022–2026 and not a bare digit 1–4 (the diagnostic's own rule, deliberately not",
        "`evaluate.is_trivial_claim`).",
        "",
        "## 1. Full populations",
        "",
        "> **This pooled comparison is a composition artifact and is NOT a finding.** The two",
        "> populations are not the same items: Case C membership depends on whether the gold",
        "> anchor was retrieved, so enrichment changes who is in the population at the same",
        "> time as it changes the outcome. The two percentages below are therefore not",
        "> comparable, and their difference does not measure an effect of enrichment. The",
        "> strictly-matched population in section 2 is the like-for-like one.",
        "> **Quote section 2, not this table.**",
        "",
        "> **Every figure in this document is a LOWER BOUND on wrong-company"
        " attribution.**",
        "> Check 3's population is Case C `answered_grounded_correct` — by"
        " construction it",
        "> can only see items that were retrieved well AND scored correct. An answer"
        " that",
        "> attributes one company's material to another in Case A or Case B is outside"
        " the",
        "> population entirely and is never counted here.",
        ">",
        "> This is measured, not hypothetical. The manual faithfulness review of the"
        " q8 arm",
        "> (`analysis/qwen3.8-27b_q8_k_xl/manual_review_second_pass.md`, pile P1)"
        " found 12 such",
        "> items in a 48-item sample, split Case A 5 / Case B 5 / Case C 2 — so the"
        " diagnostic",
        "> could see 2 of the 12. The behaviour is not arm-specific and the population"
        " limit is",
        "> structural, so treat the figures below as a floor in EVERY arm, never as a"
        " measurement.",
        "",
        "| arm | n | flagged | % |",
        "|---|--:|--:|--:|",
        f"| text_only (published post-fix) | {n_t} | {n_flag_t} | {pct(n_flag_t, n_t)} |",
        f"| **metadata_enriched** | **{n_e}** | **{n_flag_e}** | **{pct(n_flag_e, n_e)}** |",
        "",
        "## 2. Restricted to the Task 3 intersection (Case C in BOTH arms)",
        "",
        "Like-for-like: the same items in both arms, so this is not confounded by the",
        "population change enrichment causes.",
        "",
        "| arm | n | flagged | % |",
        "|---|--:|--:|--:|",
        f"| text_only | {nt_} | {ft} | {pct(ft, nt_)} |",
        f"| **metadata_enriched** | **{ne_}** | **{fe}** | **{pct(fe, ne_)}** |",
        "",
        "Note these n are unequal by construction: an item enters Check 3's population only",
        "if it was classified `correct` in that arm, so this controls for Case C membership",
        "but not for the correct/not-correct split.",
        "",
        "### Strictly matched — `answered_grounded_correct` in BOTH arms",
        "",
        "The only fully paired comparison available: identical items, identical n.",
        "",
        "**Read as: no evidence either way** at this sample size.",
        "This is the like-for-like population, but it is small: read the two rows below as a",
        "point estimate on a sample too small to distinguish any difference from chance, in",
        "either direction. Whatever the pooled section 1 comparison appears to show, it is a",
        "composition artifact and does not carry over to this matched population.",
        "",
        "| arm | n | flagged | % |",
        "|---|--:|--:|--:|",
        f"| text_only | {nbt} | {fbt} | {pct(fbt, nbt)} |",
        f"| **metadata_enriched** | **{nbe}** | **{fbe}** | **{pct(fbe, nbe)}** |",
        "",
        "## 3. By retrieval strategy",
        "",
        "> **Unmatched populations — cannot establish a strategy effect in either direction.**",
        "> These are the section 1 populations split by strategy, so every row inherits the",
        "> same composition confound: the enriched n is larger because enrichment moved items",
        "> into Case C, not because the same items behaved differently. The apparent ordering",
        "> of the rows below is not evidence of a strategy effect,",
        "> and no matched per-strategy comparison is computed here because the per-strategy",
        "> matched n would be in single digits.",
        "",
        "| strategy | text_only flagged/n | % | enriched flagged/n | % |",
        "|---|--:|--:|--:|--:|",
    ]
    for s in STRATEGIES:
        (tf, tn), (ef, en) = by_strategy[s]
        lines.append(f"| {s} | {tf}/{tn} | {pct(tf, tn)} | {ef}/{en} | {pct(ef, en)} |")
    lines += ["", f"Per-record detail: `{out_csv.name}`.", ""]

    if first_run:
        lines.insert(0, "> **FIRST RUN -- nothing was validated against.** No expectation "
                        f"set existed for model `{args.model}` when this was written, so "
                        "every figure below is COMPUTED AND UNCHECKED. Pin the model "
                        "deliberately before citing any of it.")
        lines.insert(1, "")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[lines.index("## 1. Full populations"):]))
    print(f"-> {out_md.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
