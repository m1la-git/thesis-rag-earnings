"""Emit the thesis's numbers as LaTeX, so no figure is ever hand-copied.

Why this exists
---------------
A thesis quoting eighty pages of hand-typed figures has no way to tell which of
them went stale after a re-score. This repo has already produced that failure
twice at small scale -- a hardcoded "b = 0 everywhere" sentence contradicted by
its own table, and a 70% figure quoted from the wrong row -- and a thesis is the
same failure mode with no validator behind it.

So the numbers flow ONE WAY: results tables -> this script -> `\\input`-able
LaTeX. The prose cites a macro, never a literal. Regenerate, and `git diff`
shows exactly which numbers moved.

This is the opposite direction from `analysis/expectations/`, deliberately.
Expectations are PINNED and must never be auto-populated from a run's own
output, because they are what the run is checked against. Thesis prose is the
other way round: the text must follow the numbers.

Placement
---------
`scripts/`, not `analysis/`. The rule is that every `.py` directly under
`analysis/` produces one of the documents under `analysis/`; this one writes
into `thesis/`, so filing it there would break that invariant.

Arm safety -- the point of the naming scheme
--------------------------------------------
`qwen3.8-27b@q8_k_xl` is THE REPORTED GENERATOR. `q4_k_xl` is the validator
baseline and `Qwen3.8-Flash-Next` is a robustness check; neither is a thesis
result. A macro called `\\thesisCaseCConversion` is exactly how a robustness
figure ends up cited as a result, so **every Stage 2 macro carries its arm in
its own name** and the non-reported arms are additionally marked:

    \\thesisQeightCaseCConversion            <- reportable
    \\thesisQfourValidatorCaseCConversion    <- instrument, not a result
    \\thesisFlashRobustnessCaseCConversion   <- robustness check, not a result

Stage 1 macros carry NO arm, and that asymmetry is intentional rather than an
oversight: retrieval never calls a generator, so `results/retrieval/` and
`results/tables/retrieval_metrics.csv` serve all three arms unchanged.

Usage
-----
    python scripts/build_thesis_macros.py            # write
    python scripts/build_thesis_macros.py --check    # fail if stale, write nothing
"""

from __future__ import annotations

import argparse
import collections
import csv
import glob
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import analysis_path, generation_outcomes_path, model_slug  # noqa: E402

THESIS_DIR = REPO_ROOT / "thesis"
GENERATED_DIR = THESIS_DIR / "generated"
MACROS_TEX = GENERATED_DIR / "macros.tex"
RETRIEVAL_TABLE_TEX = GENERATED_DIR / "table_retrieval_metrics.tex"
# Only the REPORTED arm gets a rendered case x outcome table. The other two
# arms' figures stay available as macros for prose, but a floated table is the
# hardest thing in a thesis to read as anything other than a result, and
# ARM_INFIX exists precisely to stop that. See build_case_outcome_table().
CASE_OUTCOME_TABLE_TEX = GENERATED_DIR / "table_case_outcome.tex"

REPORTED_MODEL = "qwen3.8-27b@q8_k_xl"

# Arm -> macro infix. The two non-reported arms carry a word saying what they
# are, so a macro cannot be pasted into a results sentence without the reader
# seeing it. Enforced by assert_arm_naming() below, not left to discipline.
ARM_INFIX = {
    "qwen3.8-27b@q8_k_xl": "Qeight",
    "qwen3.8-27b@q4_k_xl": "QfourValidator",
    "qwen3.8-flash-next": "FlashRobustness",
}
NON_REPORTED_MUST_CONTAIN = {
    "qwen3.8-27b@q4_k_xl": "Validator",
    "qwen3.8-flash-next": "Robustness",
}

OUTCOMES = ["abstained", "answered_grounded_correct",
            "answered_grounded_offtarget", "answered_ungrounded"]
CORRECT = "answered_grounded_correct"
STRATEGIES = ["dense", "bm25", "hybrid"]
REPRESENTATIONS = ["text_only", "metadata_enriched"]


def assert_arm_naming() -> None:
    for model, marker in NON_REPORTED_MUST_CONTAIN.items():
        infix = ARM_INFIX[model]
        if marker not in infix:
            raise SystemExit(
                f"STOP: macro infix {infix!r} for non-reported arm {model!r} does not "
                f"contain {marker!r}. A non-reported arm must say so in every macro name.")


def tex_escape(s: str) -> str:
    return s.replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def read_outcomes(model: str) -> list[dict]:
    path = generation_outcomes_path(model)
    if not path.exists():
        raise SystemExit(f"missing outcomes table for {model!r}: {path}")
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def macro(name: str, value) -> str:
    return f"\\newcommand{{\\thesis{name}}}{{{value}}}"


def pct(n: int, d: int) -> str:
    return r"n/a" if d == 0 else f"{100.0 * n / d:.1f}\\%"


def build_design_macros() -> list[str]:
    """Grid shape, benchmark shape, corpus shape -- all DERIVED, never typed."""
    configs = sorted(p for p in glob.glob(str(REPO_ROOT / "configs" / "*.json"))
                     if Path(p).name != "base.json")
    n_conditions = len(configs)

    questions = [json.loads(line) for line
                 in (REPO_ROOT / "benchmark" / "questions.jsonl")
                 .read_text(encoding="utf-8").splitlines() if line.strip()]
    n_questions = len(questions)
    cats = collections.Counter(q["category"] for q in questions)
    n_anchors = sum(len(q["gold_anchors"]) for q in questions)

    manifest = json.loads((REPO_ROOT / "data" / "corpus_manifest.json")
                          .read_text(encoding="utf-8"))

    # Company and quarter counts, derived from the manifest's own selection
    # record rather than typed. Added 2026-09-12: both were hand-typed literals
    # in 03_Methods.tex prose and in 05_Discussion.tex's scope guard (:83-89,
    # :487), with no guard against drift, while the transcript total beside
    # them came from a macro. See the Pass 2 ledger entry in 03_Methods.tex.
    selection = manifest["selection"]
    n_companies = len(selection["tickers"])
    n_quarters = len(selection["years"]) * len(selection["quarters"])

    # Methods states the grid is complete -- "every company present
    # throughout". That claim IS this identity, so it is asserted here rather
    # than left for the three macros to drift apart silently. If this fires,
    # the prose is wrong, not the check.
    if n_companies * n_quarters != manifest["n_transcripts"]:
        raise SystemExit(
            f"STOP: {n_companies} companies x {n_quarters} quarters = "
            f"{n_companies * n_quarters}, but the manifest records "
            f"{manifest['n_transcripts']} transcripts. Either the corpus grid "
            "is not complete or the selection record is stale; Methods claims "
            "completeness, so fix the prose or the manifest before building.")

    base = json.loads((REPO_ROOT / "configs" / "base.json").read_text(encoding="utf-8"))
    top_k = base.get("top_k", base.get("retrieval", {}).get("top_k"))

    # The encoder's CONTENT budget: max_seq_length minus [CLS] and [SEP].
    # Added 2026-09-12 (Pass 4). Methods had this typed as "510", and worse,
    # labelled it "the encoder's budget" -- which is 512. 510 is what is LEFT
    # after the two delimiters, so the typed form was wrong by two under a
    # label that hid the derivation. Read from configs/base.json, which
    # run_experiment.validate_config_matches_code cross-checks against
    # index.MAX_CONTENT_TOKENS, so config and code cannot drift apart.
    # MAX_SEQ_LENGTH (512) is deliberately NOT macroed: it lives in exactly
    # one code site and is asserted at load time in index.get_embedding_model,
    # so it is better shown deriving in prose than emitted as a value.
    # The RRF offset, cross-checked against retrieve.RRF_K by
    # run_experiment.validate_config_matches_code (:164). Added 2026-09-12
    # (Pass 5): Methods had it typed as "60".
    rrf_k = base.get("rrf_k")
    if rrf_k is None:
        raise SystemExit("STOP: configs/base.json has no rrf_k.")

    max_content_tokens = base.get("max_content_tokens")
    if max_content_tokens is None:
        raise SystemExit(
            "STOP: configs/base.json has no max_content_tokens, so "
            "MaxContentTokens cannot be derived. Do not type the value into "
            "the prose instead -- restore the key or drop the macro."
        )

    # The RETRIEVAL-SCORED count, which is NOT n_questions. Unanswerable items
    # carry no gold anchors and are dropped from the coverage/MRR denominator
    # rather than scored zero, so every Stage 1 figure has this as its n. It is
    # the T10 trap in claims_map.md: 45 and 40 are both correct, in different
    # sections, and a figure quoted against the wrong one reads fine.
    n_scored = n_questions - cats.get("unanswerable", 0)

    # Cross-checked against what Stage 1 actually scored, rather than trusted as
    # arithmetic. Every retrieval run records its own n_questions; if the two
    # ever disagree, the benchmark and the persisted grid have diverged and a
    # macro is the last place that should be discovered.
    # All 12 retrieval files are tracked in git, so a fresh clone has them. The
    # counter below exists anyway: a glob that matches nothing would skip the
    # loop and silently retire the guard, which is a worse failure than a loud
    # one because the macro would still be published.
    checked = 0
    for path in sorted((REPO_ROOT / "results" / "retrieval").glob("*.jsonl")):
        with path.open(encoding="utf-8") as fh:
            meta = json.loads(fh.readline())
        if meta.get("_type") != "run_meta":
            continue
        checked += 1
        if meta.get("n_questions") != n_scored:
            raise SystemExit(
                f"STOP: benchmark implies {n_scored} retrieval-scored questions "
                f"({n_questions} minus {cats.get('unanswerable', 0)} unanswerable), but "
                f"{path.name} recorded n_questions={meta.get('n_questions')}. The "
                "benchmark and the persisted retrieval grid disagree; do not adjust "
                "this script.")
    if checked != n_conditions:
        raise SystemExit(
            f"STOP: cross-check read run_meta from {checked} retrieval files but the "
            f"grid has {n_conditions} conditions. results/retrieval/ is incomplete or "
            "has moved, so NumQuestionsScored cannot be verified against what Stage 1 "
            "actually scored. Restore the files rather than removing this check.")

    # Size of the manual review packet, read from the manifest the packet
    # generator wrote rather than typed. Used by the Methods description of the
    # review instrument.
    manifest_csv = analysis_path(REPORTED_MODEL, "manual_review_packet_manifest.csv")
    if not manifest_csv.exists():
        raise SystemExit(
            f"STOP: {manifest_csv} is missing, so NumReviewItems cannot be derived. "
            "The file is tracked in git; restore it rather than typing the count.")
    with manifest_csv.open(encoding="utf-8", newline="") as fh:
        n_review_items = sum(1 for _ in csv.DictReader(fh))

    # The assertion that earns this file its keep: if a 13th condition is added
    # and the grid is not re-run, the product stops matching the reported arm's
    # row count and this fails loudly instead of publishing a stale 540.
    expected = n_conditions * n_questions
    actual = len(read_outcomes(REPORTED_MODEL))
    if expected != actual:
        raise SystemExit(
            f"STOP: grid shape {n_conditions} conditions x {n_questions} questions = "
            f"{expected}, but the reported arm's table has {actual} rows. Either a "
            "condition was added without re-running the grid, or the benchmark changed. "
            "Fix the mismatch; do not adjust this script.")

    lines = [
        "% ---- Design (no generator involved) ----",
        macro("NumConditions", n_conditions),
        macro("NumChunkSizes", 2),
        macro("NumStrategies", len(STRATEGIES)),
        macro("NumRepresentations", len(REPRESENTATIONS)),
        macro("ChunkSizeSmall", 200),
        macro("ChunkSizeLarge", 500),
        macro("TopK", top_k if top_k is not None else 5),
        macro("MaxContentTokens", max_content_tokens),
        macro("RrfK", rrf_k),
        macro("NumQuestions", n_questions),
        macro("NumQuestionsScored", n_scored),
        macro("NumGenerations", expected),
        macro("NumGoldAnchors", n_anchors),
        macro("NumReviewItems", n_review_items),
        macro("NumTranscripts", manifest["n_transcripts"]),
        macro("NumCompanies", n_companies),
        macro("NumQuarters", n_quarters),
        macro("CorpusDataset", tex_escape(str(manifest["dataset"]))),
        macro("CorpusRevision", tex_escape(str(manifest["revision"])[:12])),
        "",
        "% questions by category",
    ]
    for cat in ["factual", "thematic", "comparative", "unanswerable"]:
        lines.append(macro(f"NumQuestions{cat.capitalize()}", cats.get(cat, 0)))
    return lines



def apa_p(p: float) -> str:
    """A p value as APA prints it: three decimals, no leading zero."""
    assert 0 <= p <= 1, p
    s = f"{p:.3f}"
    return s[1:] if s.startswith("0.") else s


def build_exact_sensitivity_macros() -> list[str]:
    """Stage 1 under an exact test: analysis/exact_sensitivity.py.

    Generator-independent, so these carry no arm. The thesis reports the scipy
    test; these numbers state whether any of its verdicts depends on the normal
    approximation it takes above 13 paired observations.
    """
    path = REPO_ROOT / "analysis" / "stage1" / "exact_sensitivity.csv"
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    sig_rep = [r for r in rows if r["sig_reported"] == "True"]
    survive = [r for r in sig_rep if r["sig_exact"] == "True"]
    gained = [r for r in rows if r["sig_exact"] == "True" and r["sig_reported"] != "True"]
    # The appendix says every reported-significant result survives; hold it to that.
    assert len(survive) == len(sig_rep), "a reported-significant result fails the exact test"
    # Every comparison that becomes significant only under the exact test must be
    # a pair differing in both chunk size and strategy -- the pairs Table 3 sets
    # aside because they isolate neither factor. If that ever stops holding, the
    # appendix sentence these macros feed is false, so stop here.
    for r in gained:
        sa, ma = r["a"].split("_")[:2]
        sb, mb = r["b"].split("_")[:2]
        assert sa != sb and ma != mb, f"exact test changes a one-factor verdict: {r}"
    bm = next(r for r in rows if r["family"] == "Family 1" and r["scope"] == "pooled"
              and r["metric"] == "mean_reciprocal_rank_at_5"
              and r["a"] == "chunk200_bm25_enriched" and r["b"] == "chunk200_bm25")
    return [
        "",
        "% ---- Stage 1 under an exact sign-flip test (no generator involved) ----",
        macro("ExactNumSigReported", len(sig_rep)),
        macro("ExactNumSigGained", len(gained)),
        macro("ExactBmSmallMrrHolmReported", apa_p(float(bm["p_holm_reported"]))),
        macro("ExactBmSmallMrrHolmExact", apa_p(float(bm["p_holm_exact"]))),
    ]


CASES = ["A", "B", "C"]


def outcome_camel(outcome: str) -> str:
    return "".join(w.capitalize() for w in outcome.split("_"))


def case_outcome_grid(model: str) -> tuple[collections.Counter, list[dict]]:
    """The 3x4 grid, and the rows it came from.

    ONE Counter is the single source for the cells, the column totals and the
    case sizes. They used to be three independent passes over `rows`, which is
    how a published table comes to disagree with the macros beside it: nothing
    made them reconcile, so nothing would have noticed if they stopped.

    Reconciliation is asserted here rather than trusted -- every row total
    against the case partition, every column total against a direct count, and
    the whole grid against the record count.
    """
    rows = read_outcomes(model)
    grid = collections.Counter((r["case"], r["outcome"]) for r in rows)

    stray_case = {c for c, _ in grid} - set(CASES)
    stray_outcome = {o for _, o in grid} - set(OUTCOMES)
    if stray_case or stray_outcome:
        raise SystemExit(f"{model}: unexpected case {sorted(stray_case)} / "
                         f"outcome {sorted(stray_outcome)} in the outcomes table")

    if sum(grid.values()) != len(rows):
        raise SystemExit(f"{model}: grid sums to {sum(grid.values())}, "
                         f"table has {len(rows)} rows")
    by_case = collections.Counter(r["case"] for r in rows)
    for c in CASES:
        row_total = sum(grid[(c, o)] for o in OUTCOMES)
        if row_total != by_case.get(c, 0):
            raise SystemExit(f"{model}: case {c} row sums to {row_total} but "
                             f"the partition says {by_case.get(c, 0)}")
    for o in OUTCOMES:
        col_total = sum(grid[(c, o)] for c in CASES)
        direct = sum(1 for r in rows if r["outcome"] == o)
        if col_total != direct:
            raise SystemExit(f"{model}: column {o} sums to {col_total} but a "
                             f"direct count gives {direct}")
    return grid, rows


def build_stage2_macros(model: str) -> list[str]:
    """Stage 2 headline figures for ONE arm, every macro naming that arm."""
    infix = ARM_INFIX[model]
    grid, rows = case_outcome_grid(model)
    by_case = collections.Counter(r["case"] for r in rows)
    case_c = [r for r in rows if r["case"] == "C"]
    conv = grid[("C", CORRECT)]
    case_a = [r for r in rows if r["case"] == "A"]
    a_abst = grid[("A", "abstained")]

    label = ("THE REPORTED ARM" if model == REPORTED_MODEL
             else "NOT a thesis result -- "
                  + ("validator baseline" if "Validator" in infix else "robustness check"))
    lines = [
        "",
        f"% ---- Stage 2: {model}  ({label}) ----",
        macro(f"{infix}Model", tex_escape(model)),
        macro(f"{infix}NumRecords", len(rows)),
        macro(f"{infix}CaseA", by_case.get("A", 0)),
        macro(f"{infix}CaseB", by_case.get("B", 0)),
        macro(f"{infix}CaseC", by_case.get("C", 0)),
        macro(f"{infix}CaseCConversion", f"{conv}/{len(case_c)}"),
        macro(f"{infix}CaseCConversionPct", pct(conv, len(case_c))),
        macro(f"{infix}CaseAAbstentions", f"{a_abst}/{len(case_a)}"),
    ]
    # Column totals, now summed FROM the grid rather than counted separately,
    # so a cell macro and its column can no longer drift apart.
    for outcome in OUTCOMES:
        lines.append(macro(f"{infix}{outcome_camel(outcome)}",
                           sum(grid[(c, outcome)] for c in CASES)))

    lines.append(f"% the 3x4 cells behind the four totals above, same source")
    for c in CASES:
        for outcome in OUTCOMES:
            lines.append(macro(f"{infix}Case{c}{outcome_camel(outcome)}",
                               grid[(c, outcome)]))
    return lines


def build_case_outcome_table() -> list[str]:
    """The 3x4 case x outcome table, REPORTED ARM ONLY.

    No file is emitted for the validator baseline or the robustness check. Their
    figures remain available as macros, whose infix names them; a floated table
    carries no such warning and is the easiest thing in a thesis to mistake for
    a result.
    """
    model = REPORTED_MODEL
    grid, rows = case_outcome_grid(model)
    by_case = collections.Counter(r["case"] for r in rows)
    headers = {"abstained": "abstained",
               "answered_grounded_correct": "grounded,\\\\on target",
               "answered_grounded_offtarget": "grounded,\\\\off target",
               "answered_ungrounded": "ungrounded"}

    L = [f"% GENERATED by scripts/build_thesis_macros.py from {model} -- do not edit.",
         "%",
         "% Rows only. The float, caption and label live in",
         "% chapters/98_TablesFigures.tex, per the guideline that tables sit",
         "% after the references, one per page.",
         "%",
         "% INTERPRET PER CASE. Different cases have different achievable",
         "% outcomes -- answered_grounded_correct is impossible in Case A by",
         "% construction, since unanswerable items carry no transcript_ids and",
         "% the on-target test cannot pass -- so a pooled RATE averages away the",
         "% exact distinction this table exists for.",
         "%",
         "% The Total row below is a RECONCILIATION, not a result: it shows the",
         "% four outcomes account for every generation. Do not compute a rate,",
         "% share or comparison on it. (This block used to read NEVER POOLED,",
         "% which the table contradicted by carrying its own Total row;",
         "% corrected 2026-09-09 to match the Methods wording.)",
         "%",
         "% `grounded, off target` is NOT an answer-quality column. It says no",
         "% supporting chunk belonged to the question's own transcript_ids,",
         "% which is a fact about retrieval targeting.",
         "\\begin{tabular}{@{}l" + "r" * (len(OUTCOMES) + 1) + "@{}}",
         "\\toprule",
         "Case & " + " & ".join(
             f"\\multicolumn{{1}}{{c}}{{\\shortstack[c]{{{headers[o]}}}}}"
             for o in OUTCOMES) + " & \\multicolumn{1}{c}{$n$} \\\\",
         "\\midrule"]
    for c in CASES:
        cells = " & ".join(str(grid[(c, o)]) for o in OUTCOMES)
        L.append(f"{c} & {cells} & {by_case.get(c, 0)} \\\\")
    L.append("\\midrule")
    totals = " & ".join(str(sum(grid[(c, o)] for c in CASES)) for o in OUTCOMES)
    L.append(f"Total & {totals} & {len(rows)} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    return L


def build_retrieval_table() -> list[str]:
    """Stage 1 overall coverage/MRR per condition. Generator-independent."""
    with (REPO_ROOT / "results" / "tables" / "retrieval_metrics.csv").open(encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh)
                if r["breakdown_type"] == "overall_not_cross_category_comparable"]
    per_cond: dict[str, dict] = {}
    for r in rows:
        per_cond.setdefault(r["condition_id"], dict(r))[r["metric"]] = float(r["value"])

    # APA: three decimals throughout, and no leading zero, because neither metric
    # can exceed 1. Two different values that print alike at three decimals are
    # left alike -- the float note discloses the pair and says which is larger --
    # since a four-decimal cell beside three-decimal ones is the mixed precision
    # APA rules out. Differences quoted in the prose are computed on the
    # unrounded values, as the note states.
    def fmt_column(metric: str) -> dict[str, str]:
        vals = {cid: d[metric] for cid, d in per_cond.items()}
        assert all(0 <= v < 1 for v in vals.values()), "a bounded metric left [0, 1)"
        return {cid: f"{v:.3f}"[1:] for cid, v in vals.items()}

    cov, mrr = fmt_column("anchor_coverage_at_5"), fmt_column("mean_reciprocal_rank_at_5")

    out = [
        "% GENERATED by scripts/build_thesis_macros.py -- do not edit.",
        "% Stage 1 is generator-independent: these numbers are identical under",
        "% every generator arm, because retrieval never calls one.",
        "%",
        "% NOTE the source column name: 'overall_not_cross_category_comparable'.",
        "% The overall figure pools categories with different achievable ceilings,",
        "% so it is NOT comparable across categories. Use the per-category",
        "% breakdown for any cross-category claim.",
        r"\begin{tabular}{llrr}",
        r"\toprule",
        # "Retrieval strategy", not "Retrieval": the column holds the strategy,
        # and the whole table is about retrieval, so the short form named the
        # wrong thing. Column heads and cell labels are sentence-case prose, not
        # the machine identifiers the results files use.
        r"Chunk size & Retrieval strategy & Anchor coverage@5 & MRR@5 \\",
        r"\midrule",
    ]
    rep_label = {"text_only": "Text-only", "metadata_enriched": "Metadata-enriched"}
    strat_label = {"dense": "Dense", "bm25": "BM25", "hybrid": "Hybrid"}
    for rep in REPRESENTATIONS:
        out.append(r"\multicolumn{4}{l}{\emph{" + rep_label[rep] + r"}} \\")
        for size in (200, 500):
            for strat in STRATEGIES:
                cid = f"chunk{size}_{strat}" + ("_enriched" if rep == "metadata_enriched" else "")
                d = per_cond.get(cid)
                if d is None:
                    continue
                out.append(f"{size} & {strat_label[strat]} & {cov[cid]} & {mrr[cid]} " + r"\\")
        out.append(r"\midrule")
    out[-1] = r"\bottomrule"
    out.append(r"\end{tabular}")
    return out


def render() -> dict[Path, str]:
    assert_arm_naming()
    header = [
        "% GENERATED by scripts/build_thesis_macros.py -- DO NOT EDIT BY HAND.",
        "% Regenerate after any re-score or re-run; `git diff` then shows exactly",
        "% which numbers moved. Cite these macros in the prose, never a literal.",
        "%",
        "% Stage 2 macros name their generator arm. Only the Qeight ones are",
        "% thesis results: QfourValidator is the instrument baseline and",
        "% FlashRobustness is a robustness check. Stage 1 macros carry no arm",
        "% because retrieval is generator-independent.",
        "",
    ]
    body = build_design_macros() + build_exact_sensitivity_macros()
    for model in [REPORTED_MODEL, "qwen3.8-27b@q4_k_xl", "qwen3.8-flash-next"]:
        if generation_outcomes_path(model).exists():
            body += build_stage2_macros(model)
    return {
        MACROS_TEX: "\n".join(header + body) + "\n",
        RETRIEVAL_TABLE_TEX: "\n".join(build_retrieval_table()) + "\n",
        CASE_OUTCOME_TABLE_TEX: "\n".join(build_case_outcome_table()) + "\n",
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if the generated files are stale; write nothing")
    args = ap.parse_args()

    rendered = render()
    if args.check:
        stale = [p for p, text in rendered.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        for p in stale:
            print(f"STALE  {p.relative_to(REPO_ROOT)}")
        if stale:
            print("\nRegenerate with: python scripts/build_thesis_macros.py")
            return 1
        print("thesis macros are up to date with the results tables")
        return 0

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    for p, text in rendered.items():
        p.write_text(text, encoding="utf-8")
        print(f"wrote {p.relative_to(REPO_ROOT)} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
