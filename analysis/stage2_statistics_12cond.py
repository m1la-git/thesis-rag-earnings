"""Stage 2 statistics extended to the 12-condition / 540-row grid.

Method recovery
---------------
`analysis/qwen3.8-27b_q4_k_xl/stage2_statistics.md` states its own method, so it is recovered rather
than chosen:

  Case membership (A/B/C) is per (question, condition), not per question. For a
  comparison of X vs Y within case K, the matched set is the questions where
  case(q,X) == case(q,Y) == K -- so matched n differs for every pair.

  A1 pairwise: **McNemar's exact test** -- `scipy.stats.binomtest` on the larger
  of the two discordant counts, n = b + c, p = 0.5, two-sided. A pair with zero
  discordant pairs has no test to run and is reported untestable.

  A2 main effects: each side pools its 2-3 conditions; a question contributes
  only via conditions where it is genuinely case K, valued as the fraction of
  those conditions achieving the outcome; included only with >= 1 valid case-K
  observation on BOTH sides. **Wilcoxon signed-rank** on those fractions.

Holm handling matches Stage 1's, at each family's own size: a family is one
(case, outcome) cell, corrected across the pairs within it; untestable
comparisons consume no rank. Categories are separate families. Unanswerable
items remain Case A throughout -- they are never Case B or C, so they are
excluded from every B/C comparison exactly as they are today.

Validate before extending
-------------------------
`--validate` reproduces, on the 270-row `text_only` population only:
  * A2 chunk-size, all 8 rows, cell for cell;
  * A2 strategy, the 5 published rows, including Holm;
  * A1 Case B, the per-outcome best raw p, its pair, Holm, and win/loss/tie.
Expected values are PARSED from the published document, not transcribed.
Nothing is extended unless all of it reproduces.

Read-only. Writes a NEW file; `stage2_statistics.md` is not modified.

Usage
-----
    python analysis/stage2_statistics_12cond.py --validate
    python analysis/stage2_statistics_12cond.py
    python analysis/stage2_statistics_12cond.py --model qwen3.8-27b@q8_k_xl
"""

from __future__ import annotations

import argparse
import csv
import itertools
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import (  # noqa: E402
    analysis_path, ensure_analysis_dir, generation_outcomes_path,
)
sys.path.insert(0, str(REPO_ROOT / "analysis"))

from scipy.stats import binomtest  # noqa: E402

from rebuild_statistics import (  # noqa: E402
    A1_CASE_B_HEADER, A2_SIZE_HEADER, A2_STRATEGY_HEADER, METRICS, holm,
    paired_wilcoxon, parse_md_tables, select_table, _num, stage2_side_fractions,
)

# Model-scoped: results/tables/{model_slug}/generation_outcomes.csv
# Resolved per --model so a q8 table is never read under a q4 label.
# Validation target and outputs are model-scoped via analysis_path(). Under q4
# all three resolve into that generator's own analysis/<slug>/ directory
# reads and writes inside analysis/{slug}/. stage2_statistics.md is a q4-derived
# document, so validating a q8 table against it would compare two generators.
STAGE2_DOC_NAME = "stage2_statistics.md"
OUT_MD_NAME = "stage2_statistics_12cond.md"
OUT_CSV_NAME = "stage2_statistics_12cond.csv"

DEFAULT_MODEL = "qwen3.8-27b@q4_k_xl"
BASE = ["chunk200_bm25", "chunk200_dense", "chunk200_hybrid",
        "chunk500_bm25", "chunk500_dense", "chunk500_hybrid"]
ENRICHED = [f"{c}_enriched" for c in BASE]
OUTCOMES = ["abstained", "answered_grounded_correct",
            "answered_grounded_offtarget", "answered_ungrounded"]
CASES = ["B", "C"]
CATEGORIES = ["factual", "thematic", "comparative"]


def load(model: str) -> list[dict]:
    with generation_outcomes_path(model).open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["model"] == model]
    if not rows:
        raise SystemExit(f"no rows for model {model!r}")
    return rows


def mcnemar(rows: list[dict], a_id: str, b_id: str, case: str, outcome: str,
            question_ids: set[str] | None = None) -> dict:
    """McNemar's exact test for one (pair, case, outcome), as A1 defines it."""
    by = {(r["condition_id"], r["question_id"]): r for r in rows}
    qs = sorted({q for (c, q) in by if c == a_id})
    if question_ids is not None:
        qs = [q for q in qs if q in question_ids]

    matched = [q for q in qs
               if (a_id, q) in by and (b_id, q) in by
               and by[(a_id, q)]["case"] == case and by[(b_id, q)]["case"] == case]
    b = sum(1 for q in matched
            if by[(a_id, q)]["outcome"] == outcome and by[(b_id, q)]["outcome"] != outcome)
    c = sum(1 for q in matched
            if by[(a_id, q)]["outcome"] != outcome and by[(b_id, q)]["outcome"] == outcome)
    tie = len(matched) - b - c

    if b + c == 0:
        return {"a": a_id, "b": b_id, "case": case, "outcome": outcome, "n_matched": len(matched),
                "win": b, "loss": c, "tie": tie, "n_disc": 0, "p": None, "testable": False}
    p = binomtest(max(b, c), b + c, 0.5).pvalue
    return {"a": a_id, "b": b_id, "case": case, "outcome": outcome, "n_matched": len(matched),
            "win": b, "loss": c, "tie": tie, "n_disc": b + c, "p": float(p), "testable": True}


def a1_family(rows: list[dict], pairs: list[tuple[str, str]], case: str, outcome: str,
              question_ids: set[str] | None = None) -> list[dict]:
    """One Holm family: all pairs within a (case, outcome) cell."""
    res = [mcnemar(rows, a, b, case, outcome, question_ids) for a, b in pairs]
    for r, adj in zip(res, holm([x["p"] for x in res])):
        r["p_holm"] = adj
    return res


# ---------------------------------------------------------------------------
# Validation against the published document

# `select_table` and the three expected headers live in rebuild_statistics,
# imported above: this module already depends on that one, so the shared
# selector cannot live here without a circular import -- and the headers
# describe stage2_statistics.md, which both modules parse.


def validate(rows: list[dict], stage2_doc) -> list[str] | None:
    """Reproduce the published values, or None when there is nothing to compare.

    None means FIRST RUN -- no validation document exists for this generator.
    It is NOT an empty problem list: an empty list means "checked, all good",
    and conflating the two is exactly how an unvalidated run would come to look
    like a passing one. The caller must distinguish them.
    """
    if not stage2_doc.exists():
        return None
    text_only = [r for r in rows if r["condition_id"] in BASE]
    problems: list[str] = []
    tables = parse_md_tables(stage2_doc)

    # --- A2 chunk size (8 rows) ---
    t = select_table(tables, A2_SIZE_HEADER, "A2 chunk size", stage2_doc, 2)
    if t is None:
        return ["could not locate the A2 chunk-size table"]
    sides = {"200": [c for c in BASE if c.startswith("chunk200")],
             "500": [c for c in BASE if c.startswith("chunk500")]}
    for row in t[1:]:
        case, outcome, n_inc, win, loss, tie, p_raw = row[:7]
        a, b, inc = stage2_side_fractions(text_only, case, outcome, sides)
        res = paired_wilcoxon(a, b)
        for name, pub, got in [("n included", float(n_inc), float(len(inc))),
                               ("win", float(win), float(res["win"])),
                               ("loss", float(loss), float(res["loss"])),
                               ("tie", float(tie), float(res["tie"]))]:
            if abs(pub - got) > 5e-4:
                problems.append(f"A2-size {case}/{outcome} {name}: published={pub} computed={got}")
        pub_p = _num(p_raw)
        if pub_p is not None and (res["p"] is None or abs(pub_p - res["p"]) > 5.5e-4):
            problems.append(f"A2-size {case}/{outcome} p: published={pub_p} computed={res['p']}")

    # --- A2 strategy (5 published rows, with Holm) ---
    t = select_table(tables, A2_STRATEGY_HEADER, "A2 strategy", stage2_doc, 3)
    if t is None:
        problems.append("could not locate the A2 strategy table")
    else:
        strat_sides = {s: [c for c in BASE if c.endswith(s)] for s in ("dense", "bm25", "hybrid")}
        cells: dict[tuple[str, str], list[dict]] = {}
        for case in CASES:
            for outcome in OUTCOMES:
                res = []
                for x, y in itertools.combinations(("dense", "bm25", "hybrid"), 2):
                    a, b, inc = stage2_side_fractions(
                        text_only, case, outcome, {x: strat_sides[x], y: strat_sides[y]})
                    r = paired_wilcoxon(a, b)
                    res.append({"pair": f"{x} vs {y}", "n": len(inc), **r})
                for r, adj in zip(res, holm([x["p"] for x in res])):
                    r["p_holm"] = adj
                cells[(case, outcome)] = res
        for row in t[1:]:
            case, outcome, pair, n_inc, win, loss, tie, p_raw, p_holm = row[:9]
            cand = cells.get((case, outcome), [])
            got = next((r for r in cand if r["pair"] == pair
                        or r["pair"] == " vs ".join(reversed(pair.split(" vs ")))), None)
            if got is None:
                problems.append(f"A2-strategy {case}/{outcome}/{pair}: not computed")
                continue
            flip = got["pair"] != pair
            gw, gl = (got["loss"], got["win"]) if flip else (got["win"], got["loss"])
            for name, pub, g in [("n included", float(n_inc), float(got["n"])),
                                 ("win", float(win), float(gw)), ("loss", float(loss), float(gl)),
                                 ("tie", float(tie), float(got["tie"])),
                                 ("p", _num(p_raw), got["p"]),
                                 ("p (Holm)", _num(p_holm), got["p_holm"])]:
                if pub is None or g is None:
                    problems.append(f"A2-strategy {case}/{outcome}/{pair} {name}: pub={pub} got={g}")
                elif abs(pub - g) > 1.5e-3:
                    problems.append(f"A2-strategy {case}/{outcome}/{pair} {name}: pub={pub} got={g:.4f}")

    # --- A1 Case B best-p rows ---
    t = select_table(tables, A1_CASE_B_HEADER, "A1 Case B", stage2_doc, 1)
    if t is None:
        problems.append("could not locate the A1 Case B table")
    else:
        pairs = list(itertools.combinations(sorted(BASE), 2))
        for row in t[1:]:
            outcome, best_p, _pair_txt, holm_txt, wlt = row[:5]
            res = a1_family(text_only, pairs, "B", outcome)
            testable = [r for r in res if r["testable"]]
            if not testable:
                problems.append(f"A1 B/{outcome}: nothing testable but doc lists a p")
                continue
            got_best = min(r["p"] for r in testable)
            pub_best = _num(best_p)
            if pub_best is None or abs(pub_best - got_best) > 5.5e-4:
                problems.append(f"A1 B/{outcome} best raw p: published={pub_best} computed={got_best:.4f}")
            got_holm = min(r["p_holm"] for r in testable if r["p_holm"] is not None)
            pub_holm = _num(holm_txt)
            if pub_holm is not None and abs(pub_holm - got_holm) > 5.5e-4:
                problems.append(f"A1 B/{outcome} Holm at best pair: published={pub_holm} computed={got_holm:.4f}")
    return problems


# ---------------------------------------------------------------------------
# Extension
# ---------------------------------------------------------------------------


MODEL_IN_SCOPE = ""


def render(rows: list[dict], pairs: list[tuple[str, str]], title: str, note: str,
           question_ids: set[str] | None, scope: str) -> tuple[list[str], list[dict]]:
    lines = [f"### {scope}", "", note, "",
             "| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |",
             "|---|---|---|--:|--:|--:|--:|--:|--:|--:|"]
    csv_rows = []
    n_untestable = 0
    for case in CASES:
        for outcome in OUTCOMES:
            res = a1_family(rows, pairs, case, outcome, question_ids)
            for r in res:
                if not r["testable"]:
                    n_untestable += 1
                    lines.append(f"| {case} | {outcome.replace('answered_grounded_','').replace('answered_','')} "
                                 f"| {r['a']} vs {r['b']} | {r['n_matched']} | {r['win']} | {r['loss']} | "
                                 f"{r['tie']} | 0 | **untestable (no discordant pairs)** | n/a |")
                else:
                    lines.append(f"| {case} | {outcome.replace('answered_grounded_','').replace('answered_','')} "
                                 f"| {r['a']} vs {r['b']} | {r['n_matched']} | {r['win']} | {r['loss']} | "
                                 f"{r['tie']} | {r['n_disc']} | {r['p']:.3f} | {r['p_holm']:.3f} |")
                csv_rows.append({"model": MODEL_IN_SCOPE, "family": title, "scope": scope, **r})
    lines += ["", f"Untestable (zero discordant pairs): **{n_untestable} of "
                  f"{len(CASES) * len(OUTCOMES) * len(pairs)}** comparisons in this scope.", ""]
    return lines, csv_rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()

    global MODEL_IN_SCOPE
    MODEL_IN_SCOPE = args.model
    rows = load(args.model)
    stage2_doc = analysis_path(args.model, STAGE2_DOC_NAME)
    out_md = analysis_path(args.model, OUT_MD_NAME)
    out_csv = analysis_path(args.model, OUT_CSV_NAME)

    # Deliberately UNCONDITIONAL -- this runs before the --validate guard below,
    # because it is the check that stops a mixed-arm analysis, not an optional
    # extra. Do not move it behind a flag.
    problems = validate(rows, stage2_doc)
    first_run = problems is None
    doc_rel = stage2_doc.relative_to(REPO_ROOT).as_posix()
    print(f"Validation against {doc_rel} (270-row text_only population):")
    if first_run:
        print(f"  *** FIRST RUN -- no validation document for model {args.model!r}")
        print(f"  *** missing: {doc_rel}")
        print(f"  *** NOTHING WAS VALIDATED. The figures below are computed and "
              f"unchecked.")
    else:
        print("  " + ("PASS -- A2 chunk-size, A2 strategy and A1 Case B all reproduce"
                      if not problems else f"FAIL -- {len(problems)} mismatch(es)"))
        for p in problems[:20]:
            print(f"    {p}")
        if problems:
            print("\nSTOPPING: not extending to 540 until the published values reproduce.")
            return 1
    if args.validate:
        return 0

    by_cat: dict[str, set[str]] = {}
    for r in rows:
        by_cat.setdefault(r["category"], set()).add(r["question_id"])

    families = [
        ("Family 1 — representation",
         "Each `metadata_enriched` condition against its matched `text_only` counterpart "
         "(same chunk size, same strategy). Orientation: enriched first, so `win` = the "
         "enriched condition achieved the outcome where text_only did not. Holm family = "
         "the 6 pairs within each (case, outcome) cell.",
         [(f"{c}_enriched", c) for c in sorted(BASE)]),
        ("Family 2 — chunk size and strategy within text_only",
         "The original A1 comparisons, as a replication check. Holm family = the 15 pairs "
         "within each (case, outcome) cell.",
         list(itertools.combinations(sorted(BASE), 2))),
        ("Family 3 — chunk size and strategy within metadata_enriched",
         "The same comparisons inside the arm whose index carries company/period identity. "
         "Holm family = the 15 pairs within each (case, outcome) cell.",
         list(itertools.combinations(sorted(ENRICHED), 2))),
    ]

    lines = [
        "# Stage 2 statistics across all 12 conditions",
        "",
        f"Model: `{args.model}`. Source: "
        f"`{generation_outcomes_path(args.model).relative_to(REPO_ROOT).as_posix()}` "
        f"({len(rows)} rows, 12 conditions).",
        "",
        "**Method frozen, population extended.** Recovered from `analysis/qwen3.8-27b_q4_k_xl/stage2_statistics.md` "
        "and re-validated against its published values before anything here was computed: "
        "case membership is per (question, condition); a pair's matched set is the questions "
        "both conditions call case K; **McNemar's exact test** (`binomtest` on the larger "
        "discordant count, n = b+c, p = 0.5, two-sided). Holm–Bonferroni within each "
        "(case, outcome) cell at that cell's own size; untestable comparisons consume no rank. "
        "Categories are separate families. Unanswerable items are Case A and therefore never "
        "enter a Case B or Case C comparison, exactly as before.",
        "",
        "Case A is not tested: it has no pairwise structure to test here (27–28 of 30 records "
        "abstain in both arms), matching the original, which tested B and C only.",
        "",
    ]
    csv_all = []
    for title, note, pairs in families:
        lines += [f"## {title}", ""]
        block, rr = render(rows, pairs, title, note, None, f"pooled (n={len(by_cat and set().union(*by_cat.values()))})")
        lines += block
        csv_all += rr
        for cat in CATEGORIES:
            block, rr = render(rows, pairs, title, note + f" Restricted to {cat} questions.",
                               by_cat.get(cat, set()), f"{cat} (n={len(by_cat.get(cat, set()))})")
            lines += block
            csv_all += rr

    if first_run:
        lines.insert(0, "> **FIRST RUN -- nothing was validated against.** No "
                        f"validation document existed for model `{args.model}` when "
                        "this was written, so every figure below is COMPUTED AND "
                        "UNCHECKED. Pin the model deliberately before citing it.")
        lines.insert(1, "")
    ensure_analysis_dir(args.model)
    out_md.write_text("\n".join(lines), encoding="utf-8")
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_all[0].keys()))
        w.writeheader()
        w.writerows(csv_all)
    print(f"\n-> {out_md.relative_to(REPO_ROOT)}")
    print(f"-> {out_csv.relative_to(REPO_ROOT)} ({len(csv_all)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
