"""Smallest attainable p for every Stage 1 and Stage 2 comparison.

What this answers
-----------------
A test that does not reject says nothing about an effect if it could not have
rejected whatever the data. For each comparison this computes the smallest p
value the test COULD have returned, holding fixed everything the data fixed --
the number of untied pairs, and for Stage 1 the observed magnitudes and their
ties -- and letting only the direction of each difference vary. It is the
quantity the thesis's null sentence names: "the smallest attainable p value can
exceed any conventional threshold whatever the effect".

  Stage 1  paired Wilcoxon signed-rank, exactly as
           `rebuild_statistics.paired_wilcoxon` calls it:
           `wilcoxon(a, b, zero_method="wilcox", alternative="two-sided")`,
           scipy's default `method="auto"` dispatch. The attainable minimum is
           that same call on |d|, so every observed magnitude, tie and zero is
           kept and only the signs are set to agree. Same vector length, so the
           same dispatch branch.
  Stage 2  exact McNemar, exactly as `stage2_statistics_12cond.mcnemar` calls
           it: `binomtest(max(b, c), b + c, 0.5)`, two-sided. The attainable
           minimum is `binomtest(n, n, 0.5)` for n = b + c discordant pairs.

Every stored p value is REPRODUCED from the frozen inputs before anything is
computed, and the run stops if one does not. That check is the only validation
this script has: there is no pinned expectation set for it, under any model.

Corrected (Holm) attainability is deliberately NOT computed. Whether one
comparison could reach an adjusted threshold depends on the p values of every
other comparison in its family, so it is not a property of the comparison.

Where the outputs go, and why they are split
--------------------------------------------
Stage 1 is generator-independent, so its document goes in analysis/stage1/.
Stage 2's discordant counts are outcomes of a generator, so its document goes
in that generator's analysis/<slug>/ directory. Filing both under stage1/ would
assert that the Stage 2 half needs no generator, which is false.

Read-only over frozen inputs: it regenerates nothing, calls no retriever or
generator, reads no expectation file, and refuses to overwrite an existing
output whose content differs.

Usage
-----
    python analysis/attainability.py --model qwen3.8-27b@q8_k_xl
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import analysis_path, ensure_analysis_dir, stage1_path  # noqa: E402
from scipy.stats import binomtest, wilcoxon  # noqa: E402

ALPHA = 0.05
TOL = 1e-12
METRICS = ("anchor_coverage_at_5", "mean_reciprocal_rank_at_5")
SCOPES = ("pooled", "factual", "thematic", "comparative")
S1_SCORES = "stage1_scores_long_12cond.csv"
S1_STATS = "stage1_statistics_12cond.csv"
S2_STATS = "stage2_statistics_12cond.csv"
NO_SURFACE = ("> **No validation surface.** No expectation set exists for this script under any "
              "model. Its one check is that it reproduces every stored p value from the frozen "
              "inputs before computing anything, and it stops if one does not.")


def stop(msg: str) -> None:
    raise SystemExit(f"STOP: {msg}")


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        stop(f"missing input {path.relative_to(REPO_ROOT)}")
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_once(path: Path, text: str) -> str:
    """Write a new output; refuse to overwrite one whose content differs."""
    if path.exists():
        if path.read_text(encoding="utf-8") == text:
            return "unchanged"
        stop(f"{path.relative_to(REPO_ROOT)} exists with different content -- not overwriting")
    path.write_text(text, encoding="utf-8")
    return "written"


def write_csv_once(path: Path, rows: list[dict]) -> str:
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return write_once(path, buf.getvalue())


def size_only(a: str, b: str) -> bool:
    """chunk200_X vs chunk500_X, same strategy and representation."""
    ra, rb = a.split("_", 1), b.split("_", 1)
    return {ra[0], rb[0]} == {"chunk200", "chunk500"} and ra[1] == rb[1]


# ------------------------------------------------------------------- Stage 1 --
def stage1() -> tuple[list[dict], list[str]]:
    scores = collections.defaultdict(dict)
    category = {}
    for r in read_csv(stage1_path(S1_SCORES)):
        category[r["question_id"]] = r["category"]
        for met in METRICS:
            scores[(r["condition_id"], met)][r["question_id"]] = float(r[met])
    qids = {"pooled": sorted(category)}
    for c in SCOPES[1:]:
        qids[c] = sorted(q for q, cat in category.items() if cat == c)

    out, bad = [], []
    for r in read_csv(stage1_path(S1_STATS)):
        qs = qids[r["scope"]]
        a = [scores[(r["a"], r["metric"])][q] for q in qs]
        b = [scores[(r["b"], r["metric"])][q] for q in qs]
        d = [x - y for x, y in zip(a, b)]
        n_nz = sum(1 for v in d if v != 0)
        if n_nz != int(r["n_nonzero"]):
            bad.append(f"S1 n_nonzero {r['a']} vs {r['b']} {r['scope']} {r['metric']}: {n_nz} != {r['n_nonzero']}")
        row = {"family": r["family"], "scope": r["scope"], "metric": r["metric"], "a": r["a"], "b": r["b"],
               "n": len(qs), "n_nonzero": n_nz, "size_only": size_only(r["a"], r["b"]),
               "p_raw": r["p_raw"], "p_min_attainable": "", "attainable_below_05": ""}
        if r["testable"] == "True":
            p = float(wilcoxon(a, b, zero_method="wilcox", alternative="two-sided").pvalue)
            if abs(p - float(r["p_raw"])) > TOL:
                bad.append(f"S1 p {r['a']} vs {r['b']} {r['scope']} {r['metric']}: {p!r} != {r['p_raw']}")
            p_min = float(wilcoxon([abs(v) for v in d], [0.0] * len(d),
                                   zero_method="wilcox", alternative="two-sided").pvalue)
            row["p_min_attainable"] = f"{p_min:.6g}"
            row["attainable_below_05"] = p_min < ALPHA
        out.append(row)
    return out, bad


# ------------------------------------------------------------------- Stage 2 --
def stage2(model: str) -> tuple[list[dict], list[str]]:
    out, bad = [], []
    for r in read_csv(analysis_path(model, S2_STATS)):
        row = {"family": r["family"].split(" — ")[0], "scope": r["scope"].split(" (")[0],
               "a": r["a"], "b": r["b"], "case": r["case"], "outcome": r["outcome"],
               "n_disc": int(r["n_disc"]), "p": r["p"], "p_min_attainable": "", "attainable_below_05": ""}
        if r["testable"] == "True":
            n, k = int(r["n_disc"]), max(int(r["win"]), int(r["loss"]))
            p = float(binomtest(k, n, 0.5).pvalue)
            if abs(p - float(r["p"])) > TOL:
                bad.append(f"S2 p {r['a']} vs {r['b']} {r['scope']} {r['case']}/{r['outcome']}: {p!r} != {r['p']}")
            p_min = float(binomtest(n, n, 0.5).pvalue)
            row["p_min_attainable"] = f"{p_min:.6g}"
            row["attainable_below_05"] = p_min < ALPHA
        out.append(row)
    return out, bad


# ----------------------------------------------------------------- rendering --
def count_table(rows, keys, label):
    grp = collections.OrderedDict()
    for r in rows:
        k = tuple(r[x] for x in keys)
        g = grp.setdefault(k, [0, 0, 0])
        g[0] += 1
        if r["attainable_below_05"] == "":
            continue
        g[1] += 1
        g[2] += r["attainable_below_05"] is True
    lines = [f"| {' | '.join(keys)} | comparisons | testable | could reach p < .05 | could not |",
             "|" + "---|" * len(keys) + "--:|--:|--:|--:|"]
    tot = [0, 0, 0]
    for k, (n, t, ok) in grp.items():
        lines.append(f"| {' | '.join(k)} | {n} | {t} | {ok} | {t - ok} |")
        tot = [tot[0] + n, tot[1] + t, tot[2] + ok]
    lines.append(f"| **{label}** |" + " |" * (len(keys) - 1) + f" **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[1] - tot[2]}** |")
    return lines


def render_stage1(rows):
    L = [NO_SURFACE, "", "# Smallest attainable p — Stage 1 (generator-independent)", "",
         f"Inputs: `analysis/stage1/{S1_SCORES}`, `analysis/stage1/{S1_STATS}`. Generator: "
         "`analysis/attainability.py`. For each comparison, the smallest two-sided p the paired "
         "Wilcoxon could have returned with every observed magnitude, tie and zero kept and only "
         "the signs set to agree — the same call and dispatch as `rebuild_statistics.paired_wilcoxon`. "
         "**Before correction.** Holm attainability is not computed: it depends on the rest of each "
         "family, so it is not a property of one comparison.", "",
         "Every stored `p_raw` in the input was reproduced from the frozen scores before this was "
         "computed (tolerance 1e-12).", "", "## By family and scope, both metrics together", ""]
    L += count_table(rows, ["family", "scope"], "all Stage 1")
    L += ["", "## By family, scope and metric", ""]
    L += count_table(rows, ["family", "scope", "metric"], "all Stage 1")
    so = [r for r in rows if r["size_only"]]
    L += ["", "## Size-only pairs (chunk200_X vs chunk500_X) — H1's evidence", "",
          "Families 2 and 3 only; Family 1 holds no size-only pair.", ""]
    L += count_table(so, ["family", "scope"], "size-only")
    L += ["", "### Every size-only comparison", "",
          "| family | scope | metric | pair | n≠0 | observed p | smallest attainable p | could reach .05 |",
          "|---|---|---|---|--:|--:|--:|:-:|"]
    for r in so:
        att = "untestable" if r["attainable_below_05"] == "" else ("yes" if r["attainable_below_05"] else "**no**")
        L.append(f"| {r['family']} | {r['scope']} | {r['metric']} | `{r['a']}` vs `{r['b']}` | "
                 f"{r['n_nonzero']} | {r['p_raw'] or '—'} | {r['p_min_attainable'] or '—'} | {att} |")
    L += ["", "## Pooled comparisons that could not have reached p < .05", "",
          "| family | metric | pair | n≠0 | smallest attainable p |", "|---|---|---|--:|--:|"]
    for r in rows:
        if r["scope"] == "pooled" and r["attainable_below_05"] is False:
            L.append(f"| {r['family']} | {r['metric']} | `{r['a']}` vs `{r['b']}` | {r['n_nonzero']} | {r['p_min_attainable']} |")
    L += ["", f"Per-row detail: `analysis/stage1/attainability_stage1.csv`.", ""]
    return "\n".join(L)


def render_stage2(rows, model):
    t = [r for r in rows if r["attainable_below_05"] != ""]
    dist = collections.Counter(r["n_disc"] for r in t)
    L = [NO_SURFACE, "", f"# Smallest attainable p — Stage 2 (`{model}`)", "",
         f"Input: `{S2_STATS}` in this directory. Generator: `analysis/attainability.py`. For each "
         "testable comparison, the smallest two-sided p the exact McNemar test could have returned "
         "at its number of discordant pairs, n: `binomtest(n, n, 0.5)` = 2 × 0.5^n. The same call "
         "and dispatch as `stage2_statistics_12cond.mcnemar`. **Before correction**; Holm "
         "attainability is family-dependent and is not computed.", "",
         "Every stored `p` for a testable comparison was reproduced from its stored discordant "
         "counts before this was computed (tolerance 1e-12).", "",
         "## By family and scope", ""]
    L += count_table(rows, ["family", "scope"], "all Stage 2")
    L += ["", "## Testable comparisons by number of discordant pairs", "",
          "| discordant pairs | comparisons | smallest attainable p | could reach .05 |",
          "|--:|--:|--:|:-:|"]
    for n in sorted(dist):
        p_min = binomtest(n, n, 0.5).pvalue
        L.append(f"| {n} | {dist[n]} | {p_min:.4g} | {'yes' if p_min < ALPHA else 'no'} |")
    L += ["", f"Per-row detail: `attainability_stage2.csv` in this directory.", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True, help="generator whose Stage 2 table to read")
    args = ap.parse_args()

    s1, bad1 = stage1()
    s2, bad2 = stage2(args.model)
    if bad1 or bad2:
        stop("stored p values did not reproduce; nothing written.\n  " + "\n  ".join((bad1 + bad2)[:20]))
    print(f"reproduced: Stage 1 {sum(1 for r in s1 if r['p_min_attainable'])} testable p values, "
          f"Stage 2 {sum(1 for r in s2 if r['p_min_attainable'])} testable p values")

    ensure_analysis_dir(args.model)
    results = [
        (stage1_path("attainability_stage1.md"), write_once(stage1_path("attainability_stage1.md"), render_stage1(s1))),
        (stage1_path("attainability_stage1.csv"), write_csv_once(stage1_path("attainability_stage1.csv"), s1)),
        (analysis_path(args.model, "attainability_stage2.md"),
         write_once(analysis_path(args.model, "attainability_stage2.md"), render_stage2(s2, args.model))),
        (analysis_path(args.model, "attainability_stage2.csv"),
         write_csv_once(analysis_path(args.model, "attainability_stage2.csv"), s2)),
    ]
    for p, status in results:
        print(f"{status:9s} {p.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
