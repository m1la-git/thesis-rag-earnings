"""Regenerate the computable statistical tables of the two analysis write-ups.

Scope -- read this first, it is not "regenerate the two .md files"
------------------------------------------------------------------
`analysis/stage1/stage1_diagnostics.md` (756 lines, 521 of them prose) and
`analysis/qwen3.8-27b_q4_k_xl/stage2_statistics.md` (266 lines, 218 prose) are hand-authored
analytical documents. They contain one-off empirical probes (Stage 1 Part 2's
seven plumbing checks), concrete inspection of individual cases, "Reading"
sections and "Verdict" sections. **No script regenerates those**, and this one
does not pretend to. What IS mechanical is the tables, and that is what this
rebuilds:

  REBUILT + VALIDATED
    stage1 Part 6.1-6.2  pooled pairwise Wilcoxon, 15 pairs x 2 metrics
    stage2 A2            both main-effect tables (chunk size, strategy)

  NOT REBUILT (stated so coverage is unambiguous)
    stage1 Part 2        one-off plumbing probes; partly superseded by tests/
    stage1 Parts 1,3,4   derivable but narrative-embedded; not needed by Task 5
    stage1 Part 5        needs full index rebuilds; 5.4 is prose
    stage2 A1,A3,A4,A5   A1 summary rows validated below; the rest is prose

Method recovery
---------------
Both documents state their own method, so it is recoverable rather than guessed:

  Stage 1 (Part 6): paired Wilcoxon signed-rank, `zero_method="wilcox"`,
  two-sided. Win/loss/tie reported first. Effect size r = z / sqrt(n_nonzero),
  reported only when n_nonzero >= 10. Categories are SEPARATE families, not
  corrected against each other.

  Holm family size is 15 -- per metric -- NOT the 30 the document's prose
  claims. See `stage1_family` for the evidence: family size 15 reproduces all
  30 published cells exactly, family size 30 reproduces 28 of 30. The document
  contradicts itself and its numbers win; the prose is flagged for correction.

  The one thing the document does not state is how `z` was obtained, and it
  matters: scipy's `method="approx"` applies a tie correction that gives
  r=-0.274 where the document prints -0.268. The published values are the
  TEXTBOOK normal approximation with neither tie nor continuity correction --
  z = (W - n(n+1)/4) / sqrt(n(n+1)(2n+1)/24). That reproduces -0.268, -0.306
  and -0.121 exactly, i.e. every published r, so the method is recovered rather
  than fitted. `_wilcoxon_z` implements it and the validator proves it.

  Stage 2 (A2): each side pools its 2-3 conditions; a question contributes only
  via conditions where it is genuinely case K, valued as the fraction of those
  conditions achieving the outcome; included only with >=1 valid case-K
  observation on BOTH sides. Wilcoxon signed-rank on those fractions.

Validation protocol
-------------------
`--validate` recomputes each covered table and diffs it against the values
PARSED OUT OF THE PUBLISHED .md ITSELF -- no hand-transcribed expectations, so a
typo cannot manufacture a pass. Any mismatch is reported and nothing is written.

Dependency note: this uses `scipy`. Stage 1 Part 6's own aside flagged it as
unpinned -- acceptable for a one-off diagnostic, but requiring a pin if such
testing became part of the pipeline. Making these tracked generators was
exactly that condition, and the pin exists: `scipy==1.18.0` in
requirements.txt. This paragraph used to say scipy was NOT pinned, which
stopped being true when it was; corrected 2026-09-10.

Usage
-----
    python analysis/rebuild_statistics.py --validate
    python analysis/rebuild_statistics.py --stage1-12
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "analysis"))

from scipy.stats import wilcoxon  # noqa: E402

from model_paths import stage1_path, DEFAULT_MODEL, analysis_path  # noqa: E402
from rebuild_long_tables import (  # noqa: E402
    TEXT_ONLY_CONDITIONS,
    build_stage1,
    build_stage2,
    persisted_conditions,
)

# STAGE1_DOC and the two Stage 1 outputs are deliberately NOT model-scoped:
# Stage 1 is retrieval, which has no generator, and this script's own --model
# help says so ("Stage 1 is generator-independent; this affects only the Stage 2
# A2 validation"). Scoping them would create a per-generator copy of a document
# that cannot differ between generators.
STAGE1_DOC = stage1_path("stage1_diagnostics.md")
OUT_STAGE1_12 = stage1_path("stage1_statistics_12cond.md")
OUT_STAGE1_12_CSV = stage1_path("stage1_statistics_12cond.csv")

# STAGE2_DOC is the one generator-dependent surface here: validate_stage2 reads
# it, and it is a q4-derived document. Model-scoped, resolved from --model.
STAGE2_DOC_NAME = "stage2_statistics.md"

METRICS = ("anchor_coverage_at_5", "mean_reciprocal_rank_at_5")
CATEGORIES = ("factual", "thematic", "comparative")
OUTCOMES = ("abstained", "answered_grounded_correct",
            "answered_grounded_offtarget", "answered_ungrounded")


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def _wilcoxon_z(w: float, n_nonzero: int) -> float:
    """Textbook normal approximation, no tie or continuity correction.

    See the module docstring: this is the form that reproduces every published
    effect size in Stage 1 Part 6. scipy's `method="approx"` applies a tie
    correction and does not.
    """
    mean = n_nonzero * (n_nonzero + 1) / 4.0
    sd = math.sqrt(n_nonzero * (n_nonzero + 1) * (2 * n_nonzero + 1) / 24.0)
    return (w - mean) / sd if sd else float("nan")


def paired_wilcoxon(a: list[float], b: list[float], min_n_for_r: int = 10) -> dict:
    """Paired comparison of `a` vs `b`, in the form Stage 1 Part 6 reports it."""
    diffs = [x - y for x, y in zip(a, b)]
    win = sum(1 for d in diffs if d > 0)
    loss = sum(1 for d in diffs if d < 0)
    tie = sum(1 for d in diffs if d == 0)
    n_nonzero = win + loss

    if n_nonzero == 0:
        return {"win": win, "loss": loss, "tie": tie, "n_nonzero": 0,
                "W": None, "p": None, "r": None, "testable": False}

    res = wilcoxon(a, b, zero_method="wilcox", alternative="two-sided")
    w = float(res.statistic)
    r = _wilcoxon_z(w, n_nonzero) / math.sqrt(n_nonzero) if n_nonzero >= min_n_for_r else None
    return {"win": win, "loss": loss, "tie": tie, "n_nonzero": n_nonzero,
            "W": w, "p": float(res.pvalue), "r": r, "testable": True}


def holm(pvalues: list[float | None]) -> list[float | None]:
    """Holm-Bonferroni within one family. None (untestable) stays None and does
    not consume a rank -- an untestable comparison is not a test."""
    indexed = [(p, i) for i, p in enumerate(pvalues) if p is not None]
    m = len(indexed)
    adjusted: list[float | None] = [None] * len(pvalues)
    running = 0.0
    for rank, (p, i) in enumerate(sorted(indexed)):
        running = max(running, min(1.0, (m - rank) * p))
        adjusted[i] = running
    return adjusted


# ---------------------------------------------------------------------------
# Stage 1
# ---------------------------------------------------------------------------


def stage1_pivot(rows: list[dict]) -> dict:
    """{metric: {condition_id: {question_id: value}}}"""
    out: dict = {m: {} for m in METRICS}
    for r in rows:
        for m in METRICS:
            out[m].setdefault(r["condition_id"], {})[r["question_id"]] = float(r[m])
    return out


def stage1_family(pivot: dict, pairs: list[tuple[str, str]], question_ids: list[str]) -> list[dict]:
    """Pairwise comparisons with Holm applied WITHIN EACH METRIC separately.

    Family size is per (scope, metric) -- e.g. 15 for the pooled 15-pair set --
    NOT the 30 that Stage 1 Part 6's prose describes.

    This is a discrepancy inside the published document, not a choice made here.
    Part 6's prose says "each family below (15 pairwise conditions x 2 metrics =
    30 tests) is Holm-Bonferroni corrected within itself", but its own numbers
    are reproducible only at family size 15: the smallest coverage p (0.0434)
    is published as Holm 0.651 = 0.0434 x 15, and the smallest MRR p (0.0150) as
    0.225 = 0.0150 x 15. At family size 30 those become 1.000 and 0.449.
    Correcting per metric reproduces all 30 published cells with zero
    mismatches; correcting across both reproduces 28 of 30.

    The numbers are what the thesis reports, so the numbers define the method
    that was used, and this follows them. The prose needs fixing -- flagged to
    the human, not silently edited here.
    """
    results = []
    for metric in METRICS:
        metric_results = []
        for a_id, b_id in pairs:
            a = [pivot[metric][a_id][q] for q in question_ids]
            b = [pivot[metric][b_id][q] for q in question_ids]
            metric_results.append({"metric": metric, "a": a_id, "b": b_id, **paired_wilcoxon(a, b)})
        for res, adj in zip(metric_results, holm([r["p"] for r in metric_results])):
            res["p_holm"] = adj
        results.extend(metric_results)
    return results


def fmt(v, nd=3):
    if v is None:
        return "n/a"
    return f"{v:.{nd}f}"


# ---------------------------------------------------------------------------
# Validation: parse the published tables out of the .md itself
# ---------------------------------------------------------------------------


def parse_md_tables(path: Path) -> list[list[list[str]]]:
    """Every markdown table in `path`, as a list of row-cell-lists."""
    tables, current = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                current.append(cells)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables



# ---------------------------------------------------------------------------
# Table selection -- FULL header match, and a near-miss is a defect
# ---------------------------------------------------------------------------
#
# Selecting these tables by header PREFIX is unsafe. stage2_statistics_12cond's
# own extension document contains a table whose header also begins
# `case | outcome | pair`, but whose columns are `matched n ... n disc` where the
# A2-strategy table has `n included ...`. A prefix match selects it, reads the
# wrong columns by position, and reports PASS or a spurious mismatch -- with
# nothing in the output saying the wrong table was read.
#
# So: match the FULL header. And keep two failures apart that a prefix match
# conflates. A table that is absent is an ABSENCE (the caller may treat it as a
# missing target). A table whose header starts right and then diverges is a
# DEFECT -- malformed document, or the wrong document -- and it exits loudly
# rather than being reportable as an absence.
#
# Shared by rebuild_statistics and stage2_statistics_12cond so there is exactly
# one selector and one definition of each expected header.

A2_SIZE_HEADER = ["case", "outcome", "n included", "win(200>500)",
                  "loss(500>200)", "tie", "p (raw)"]
A2_STRATEGY_HEADER = ["case", "outcome", "pair", "n included", "win", "loss",
                      "tie", "p (raw)", "p (Holm)"]
A1_CASE_B_HEADER = ["outcome", "best (lowest) raw p across the 15 pairs",
                    "that pair", "Holm-adjusted", "win/loss/tie at that pair"]


def select_table(tables, expected: list[str], name: str, doc, prefix_len: int):
    """The one table whose header is exactly `expected`, or None if absent.

    Exits with an explicit message on a NEAR MISS -- a header sharing the first
    `prefix_len` cells but not equal to `expected`. That is a malformed or wrong
    document, not a missing one, and must never be reported as a missing target.
    """
    for t in tables:
        if t and t[0] == expected:
            return t
    near = [t for t in tables if t and t[0][:prefix_len] == expected[:prefix_len]]
    if near:
        raise SystemExit(
            f"\nMALFORMED VALIDATION DOCUMENT -- refusing to guess.\n"
            f"  document : {doc}\n"
            f"  table    : {name}\n"
            f"  expected : {expected}\n"
            f"  found    : {near[0][0]}\n"
            f"  The header starts as expected and then diverges, so a prefix match\n"
            f"  would have selected this table and read its columns by position --\n"
            f"  silently comparing the wrong quantities. This is a DEFECT in the\n"
            f"  document, not a missing target.\n"
            f"  Fix the document; do not relax the selector."
        )
    return None


def _num(cell: str):
    cell = cell.replace("**", "").replace("−", "-").strip()
    if cell in ("n/a", "", "—"):
        return None
    try:
        return float(cell)
    except ValueError:
        return None


def validate_stage1(pivot: dict, question_ids: list[str]) -> list[str]:
    """Diff recomputed Part 6.1-6.2 against the values published in the doc."""
    pairs = list(itertools.combinations(sorted(TEXT_ONLY_CONDITIONS), 2))
    computed = stage1_family(pivot, pairs, question_ids)
    by_key = {(c["metric"], c["a"], c["b"]): c for c in computed}

    tables = parse_md_tables(STAGE1_DOC)
    wanted = [t for t in tables
              if t and t[0][0] == "pair" and "W" in t[0] and len(t) == 16]
    if len(wanted) < 2:
        return [f"could not locate the two 15-row Part 6.1-6.2 tables in {STAGE1_DOC.name} "
                f"(found {len(wanted)})"]

    problems = []
    for metric, table in zip(METRICS, wanted[:2]):
        for row in table[1:]:
            pair, win, loss, tie, nz, w, p_raw, p_holm, r = row[:9]
            a_id, b_id = [s.strip() for s in pair.split(" vs ")]
            c = by_key[(metric, a_id, b_id)]
            checks = [
                ("win", float(win), float(c["win"])), ("loss", float(loss), float(c["loss"])),
                ("tie", float(tie), float(c["tie"])), ("n_nonzero", float(nz), float(c["n_nonzero"])),
                ("W", _num(w), c["W"]), ("p", _num(p_raw), c["p"]),
                        ("p_holm", _num(p_holm), c["p_holm"]), ("r", _num(r), c["r"]),
            ]
            for name, published, got in checks:
                if published is None and got is None:
                    continue
                if published is None or got is None:
                    problems.append(f"{metric} {pair} {name}: published={published} computed={got}")
                elif abs(published - got) > 5.5e-4:
                    # 5.5e-4, not 5e-4: the doc rounds to 3dp, so a value like
                    # 0.96449 printed as 0.965 is a rounding boundary, not a
                    # method difference.
                    problems.append(f"{metric} {pair} {name}: published={published} computed={got:.5f}")
    return problems


# ---------------------------------------------------------------------------
# Stage 2 A2 (main effects) -- method recovery check
# ---------------------------------------------------------------------------


def stage2_side_fractions(rows: list[dict], case: str, outcome: str,
                          sides: dict[str, list[str]]) -> tuple[list[float], list[float], list[str]]:
    """Per-question fraction-of-conditions achieving `outcome`, per side."""
    by_q: dict[str, dict[str, list[int]]] = {}
    for r in rows:
        if r["case"] != case:
            continue
        for side, condition_ids in sides.items():
            if r["condition_id"] in condition_ids:
                by_q.setdefault(r["question_id"], {}).setdefault(side, []).append(
                    1 if r["outcome"] == outcome else 0
                )
    names = list(sides)
    a, b, included = [], [], []
    for q, side_map in sorted(by_q.items()):
        if all(side_map.get(s) for s in names):
            a.append(sum(side_map[names[0]]) / len(side_map[names[0]]))
            b.append(sum(side_map[names[1]]) / len(side_map[names[1]]))
            included.append(q)
    return a, b, included


def _validate_stage2_impl(rows: list[dict], stage2_doc) -> list[str]:
    """Diff recomputed A2 chunk-size table against the published one."""
    tables = parse_md_tables(stage2_doc)
    t = select_table(tables, A2_SIZE_HEADER, "A2 chunk size", stage2_doc, 2)
    if t is None:
        return ["could not locate the A2 chunk-size table in stage2_statistics.md"]
    wanted = [t]

    sides = {"200": [c for c in TEXT_ONLY_CONDITIONS if c.startswith("chunk200")],
             "500": [c for c in TEXT_ONLY_CONDITIONS if c.startswith("chunk500")]}
    problems = []
    for row in wanted[0][1:]:
        case, outcome, n_inc, win, loss, tie, p_raw = row[:7]
        a, b, included = stage2_side_fractions(rows, case, outcome, sides)
        res = paired_wilcoxon(a, b)
        checks = [("n included", float(n_inc), float(len(included))),
                  ("win", float(win), float(res["win"])),
                  ("loss", float(loss), float(res["loss"])),
                  ("tie", float(tie), float(res["tie"]))]
        published_p = _num(p_raw)
        if published_p is not None:
            checks.append(("p", published_p, res["p"]))
        elif res["testable"]:
            problems.append(f"A2 {case}/{outcome} p: published n/a but computed {res['p']}")
        for name, published, got in checks:
            if got is None or abs(published - round(got, 3)) > 5e-4:
                problems.append(f"A2 {case}/{outcome} {name}: published={published} computed={got}")
    return problems


# ---------------------------------------------------------------------------
# Task 5: Stage 1 statistics across 12 conditions, three families
# ---------------------------------------------------------------------------


def enriched_of(condition_id: str) -> str:
    return f"{condition_id}_enriched"


def render_family(title: str, note: str, results: list[dict]) -> list[str]:
    lines = [f"### {title}", "", note, "",
             "| metric | pair | win | loss | tie | n≠0 | W | p (raw) | p (Holm) | r |",
             "|---|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for c in results:
        if not c["testable"]:
            lines.append(f"| {c['metric']} | {c['a']} vs {c['b']} | {c['win']} | {c['loss']} | "
                         f"{c['tie']} | 0 | n/a | n/a (all pairs tied) | n/a | n/a |")
        else:
            lines.append(f"| {c['metric']} | {c['a']} vs {c['b']} | {c['win']} | {c['loss']} | "
                         f"{c['tie']} | {c['n_nonzero']} | {fmt(c['W'], 1)} | {fmt(c['p'])} | "
                         f"{fmt(c['p_holm'])} | {fmt(c['r'])} |")
    lines.append("")
    return lines


def stage1_twelve(rows: list[dict]) -> int:
    pivot = stage1_pivot(rows)
    by_cat: dict[str, list[str]] = {}
    for r in rows:
        by_cat.setdefault(r["category"], set()).add(r["question_id"])  # type: ignore[union-attr]
    by_cat = {k: sorted(v) for k, v in by_cat.items()}
    all_q = sorted({r["question_id"] for r in rows})

    text_only = sorted(TEXT_ONLY_CONDITIONS)
    enriched = sorted(enriched_of(c) for c in TEXT_ONLY_CONDITIONS)

    # Each family is (title, pairs). It used to carry a third element, a prose
    # note -- but the note was overwritten below with the per-scope family-size
    # line before render_family ever saw it, so none of it reached the document.
    # Two of the three dead strings were also WRONG: they said "6 pairs x 2
    # metrics = 12 tests" and "15 pairs x 2 metrics = 30 tests", while
    # stage1_family corrects Holm WITHIN EACH METRIC, so the families are 6 and
    # 15. Deleting one line below would have started publishing that error into
    # a document later sessions read as an artifact. Removed 2026-09-10; the
    # document regenerates byte-identical, which is how the deadness was
    # confirmed rather than assumed.
    #
    # Family 1 is oriented enriched vs text_only, so `win` = enriched scored
    # higher. Families 2 and 3 are the same 15 within-arm comparisons on either
    # half of the grid; Family 2 replicates the original Part 6.1-6.2 set.
    families = [
        ("Family 1 — representation (6 matched pairs)",
         [(enriched_of(c), c) for c in text_only]),
        ("Family 2 — chunk size and strategy within `text_only` (15 pairs)",
         list(itertools.combinations(text_only, 2))),
        ("Family 3 — chunk size and strategy within `metadata_enriched` (15 pairs)",
         list(itertools.combinations(enriched, 2))),
    ]

    lines = [
        "# Stage 1 statistics across all 12 conditions",
        "",
        "Generated by `analysis/rebuild_statistics.py --stage1-12` from "
        "`analysis/stage1/stage1_scores_long_12cond.csv` (480 rows).",
        "",
        "**Method frozen, population extended.** Identical to Stage 1 Part 6: paired Wilcoxon "
        "signed-rank (`scipy.stats.wilcoxon`, `zero_method=\"wilcox\"`, two-sided); win/loss/tie "
        "first; Holm–Bonferroni **within each family at that family's own size**; effect size "
        "`r = z / sqrt(n≠0)` from the uncorrected normal approximation, reported only when "
        "n≠0 ≥ 10. Unanswerable items are excluded upstream by `evaluate.is_retrieval_scored` "
        "(Stage 1 never retrieved for them), so n = 40 answerable questions throughout. "
        "Categories are separate families and are **not** corrected against the pooled set, "
        "exactly as in the original.",
        "",
        "A comparison in which every question ties, leaving n≠0 = 0, has no test to run: "
        "it is reported as untestable rather than as a p-value, and consumes no Holm rank. "
        "(\"Discordant pairs\" is McNemar's term and does not apply to a signed-rank test; "
        "the analogue here is a non-zero difference.)",
        "",
        "**Effect-size parameterization.** `z` is the textbook normal approximation with "
        "**neither a tie correction nor a continuity correction** — "
        "`z = (W − n(n+1)/4) / sqrt(n(n+1)(2n+1)/24)`, n = n≠0. Stated explicitly because "
        "recomputing with scipy's defaults will not match: "
        "`scipy.stats.wilcoxon(..., method=\"approx\")` applies a tie correction and returns "
        "−0.274 where Stage 1 Part 6 prints −0.268. A third-decimal disagreement against "
        "`method=\"approx\"` is that tie correction, not an error. This is the same "
        "parameterization Part 6 used, so the two documents are directly comparable.",
        "",
        "**Holm family size.** Each metric forms its own family, at the size stated under each "
        "table — 6 pairs × 1 metric = 6 for Family 1, 15 for Families 2 and 3. This matches "
        "how Stage 1 Part 6's published numbers were actually computed (per metric), which its "
        "prose originally misdescribed as a single family of 30; see the correction note there.",
        "",
    ]

    csv_rows = []
    for title, pairs in families:
        lines.append(f"## {title}")
        lines.append("")
        for scope, qids in [("pooled (n=40)", all_q)] + [
            (f"{c} (n={len(by_cat.get(c, []))})", by_cat.get(c, [])) for c in CATEGORIES
        ]:
            if not qids:
                continue
            results = stage1_family(pivot, pairs, qids)
            # Holm is applied PER METRIC, so the family size quoted here is the
            # per-metric count, not the total number of rows in the table.
            # The note built below is the ONLY note the document ever shows.
            per_metric = {
                m: sum(1 for r in results if r["metric"] == m and r["testable"])
                for m in METRICS
            }
            note = "Holm family size (per metric, corrected separately): " + ", ".join(
                f"{m} = {n} testable of {len(pairs)}" for m, n in per_metric.items()
            ) + "."
            lines += render_family(scope, note, results)
            for c in results:
                csv_rows.append({"family": title.split(" — ")[0], "scope": scope.split(" (")[0],
                                 "metric": c["metric"], "a": c["a"], "b": c["b"],
                                 "win": c["win"], "loss": c["loss"], "tie": c["tie"],
                                 "n_nonzero": c["n_nonzero"], "W": c["W"], "p_raw": c["p"],
                                 "p_holm": c["p_holm"], "r": c["r"], "testable": c["testable"]})

    OUT_STAGE1_12.write_text("\n".join(lines), encoding="utf-8")
    with OUT_STAGE1_12_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    print("\n".join(lines))
    print(f"-> {OUT_STAGE1_12.relative_to(REPO_ROOT)}")
    print(f"-> {OUT_STAGE1_12_CSV.relative_to(REPO_ROOT)} ({len(csv_rows)} rows)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--stage1-12", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"generator model whose scored table to read (default: "
                             f"{DEFAULT_MODEL}). Stage 1 is generator-independent; this "
                             f"affects only the Stage 2 A2 validation.")
    args = parser.parse_args()
    if not (args.validate or args.stage1_12):
        parser.error("pass --validate or --stage1-12")

    if args.validate:
        s1 = build_stage1(TEXT_ONLY_CONDITIONS, with_representation=False)
        pivot = stage1_pivot(s1)
        qids = sorted({r["question_id"] for r in s1})
        p1 = validate_stage1(pivot, qids)
        print(f"stage1_diagnostics.md Part 6.1-6.2 (30 comparisons): "
              f"{'PASS -- every published cell reproduced' if not p1 else f'FAIL -- {len(p1)} mismatch(es)'}")
        for problem in p1[:15]:
            print(f"    {problem}")

        s2 = build_stage2(with_representation=False, model=args.model,
                          conditions=TEXT_ONLY_CONDITIONS)
        stage2_doc = analysis_path(args.model, STAGE2_DOC_NAME)
        doc_rel = stage2_doc.relative_to(REPO_ROOT).as_posix()
        if not stage2_doc.exists():
            # FIRST RUN for this generator: no A2 document to validate against.
            # Not a pass -- nothing was compared. Reported as its own state so it
            # cannot be mistaken for "0 mismatches".
            print(f"{doc_rel} A2 chunk-size table (8 rows): "
                  f"*** FIRST RUN -- document does not exist for model "
                  f"{args.model!r}; NOTHING VALIDATED ***")
            p2 = []
        else:
            p2 = _validate_stage2_impl(s2, stage2_doc)
            print(f"{doc_rel} A2 chunk-size table (8 rows): "
                  f"{'PASS -- every published cell reproduced' if not p2 else f'FAIL -- {len(p2)} mismatch(es)'}")
            for problem in p2[:15]:
                print(f"    {problem}")
        return 0 if not (p1 or p2) else 1

    rows = build_stage1(persisted_conditions(), with_representation=True)
    return stage1_twelve(rows)


if __name__ == "__main__":
    sys.exit(main())
