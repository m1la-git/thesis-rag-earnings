"""Do the Stage 1 verdicts survive an exact test?

What this answers
-----------------
Stage 1 runs `scipy.stats.wilcoxon` with its default dispatch, which with a
zero among the paired differences takes the tie-corrected normal approximation
above 13 paired observations. Every result reported as significant sits on that
branch, some on as few as 10 untied pairs. This recomputes every Stage 1
comparison with an exact sign-flip permutation test of the same signed-rank
statistic -- midranks of |d|, zeros dropped, all 2^n sign assignments of the n
untied pairs enumerated -- Holm-adjusts it in exactly the blocks the reported
test uses (family x scope x metric), and records every comparison whose verdict
at .05 changes.

It is a sensitivity check on the reported test, not a replacement for it: the
thesis reports the scipy results, and this document states whether any of them
depends on the approximation.

Validation
----------
Every stored raw p value in `stage1_statistics_12cond.csv` is REPRODUCED from
the frozen per-question scores, through the same `paired_wilcoxon` call, and
every stored Holm value from those raw values, before anything is computed; the
run stops if one does not reproduce. There is no pinned expectation set.

Stage 1 is generator-independent, so both outputs go in analysis/stage1/.

Read-only over frozen inputs: calls no retriever or generator.

Usage
-----
    python analysis/exact_sensitivity.py
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "analysis"))

from model_paths import stage1_path  # noqa: E402
from rebuild_statistics import holm, paired_wilcoxon  # noqa: E402

SCORES = stage1_path("stage1_scores_long_12cond.csv")
STATS = stage1_path("stage1_statistics_12cond.csv")
OUT_CSV = stage1_path("exact_sensitivity.csv")
OUT_MD = stage1_path("exact_sensitivity.md")

ALPHA = 0.05
TOL = 1e-12
CHUNK = 1 << 16


def exact_signflip_p(d: np.ndarray) -> float:
    """Two-sided exact p of the signed-rank statistic, by full enumeration."""
    d = d[d != 0]
    n = len(d)
    ranks = rankdata(np.abs(d))
    t_obs = ranks[d > 0].sum()
    mean = ranks.sum() / 2
    dev = abs(t_obs - mean) - 1e-9   # at least as extreme, robust to float noise
    hits, total = 0, 1 << n
    for start in range(0, total, CHUNK):
        idx = np.arange(start, min(total, start + CHUNK), dtype=np.int64)
        signs = ((idx[:, None] >> np.arange(n)) & 1).astype(np.float64)
        hits += int((np.abs(signs @ ranks - mean) >= dev).sum())
    return hits / total


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    with SCORES.open(encoding="utf-8", newline="") as fh:
        scores = list(csv.DictReader(fh))
    by_cond: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for r in scores:
        by_cond[r["condition_id"]][r["question_id"]] = r

    with STATS.open(encoding="utf-8", newline="") as fh:
        stats = list(csv.DictReader(fh))

    out = []
    for s in stats:
        qa, qb = by_cond[s["a"]], by_cond[s["b"]]
        qids = sorted(q for q in qa
                      if s["scope"] == "pooled" or qa[q]["category"] == s["scope"])
        a = [float(qa[q][s["metric"]]) for q in qids]
        b = [float(qb[q][s["metric"]]) for q in qids]
        rep = paired_wilcoxon(a, b)
        stored = float(s["p_raw"]) if s["p_raw"] else None
        if (rep["p"] is None) != (stored is None) or (
                stored is not None and abs(rep["p"] - stored) > TOL):
            raise SystemExit(f"stored p does not reproduce: {s}")
        p_exact = exact_signflip_p(np.array(a) - np.array(b)) if rep["testable"] else None
        out.append({**{k: s[k] for k in ("family", "scope", "metric", "a", "b",
                                         "win", "loss", "n_nonzero")},
                    "p_raw_reported": stored, "p_holm_reported": None,
                    "p_raw_exact": p_exact, "p_holm_exact": None})

    blocks = collections.defaultdict(list)
    for i, r in enumerate(out):
        blocks[(r["family"], r["scope"], r["metric"])].append(i)
    for idx in blocks.values():
        for key in ("reported", "exact"):
            adj = holm([out[i][f"p_raw_{key}"] for i in idx])
            for i, p in zip(idx, adj):
                out[i][f"p_holm_{key}"] = p
    for r, s in zip(out, stats):
        stored = float(s["p_holm"]) if s["p_holm"] else None
        got = r["p_holm_reported"]
        if (got is None) != (stored is None) or (stored is not None and abs(got - stored) > TOL):
            raise SystemExit(f"stored Holm p does not reproduce: {s}")

    def sig(p):
        return p is not None and p < ALPHA

    for r in out:
        r["sig_reported"], r["sig_exact"] = sig(r["p_holm_reported"]), sig(r["p_holm_exact"])

    fields = list(out[0].keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    testable = [r for r in out if r["p_raw_exact"] is not None]
    sig_rep = [r for r in out if r["sig_reported"]]
    changed = [r for r in out if r["sig_reported"] != r["sig_exact"]]
    closest = max(sig_rep, key=lambda r: r["p_holm_reported"])

    def f(p):
        return "n/t" if p is None else f"{p:.3f}"

    lines = [
        "# Stage 1 verdicts under an exact test",
        "",
        "Generated by `analysis/exact_sensitivity.py`. Every stored raw and Holm p",
        "value in `stage1_statistics_12cond.csv` was reproduced before this was",
        "computed.",
        "",
        f"- Comparisons: {len(out)}, of which {len(testable)} testable.",
        f"- Significant at Holm p < .05 under the reported test: {len(sig_rep)}.",
        f"- **Verdicts that change under the exact test: {len(changed)}.**",
        f"- Closest reported-significant result: {closest['family']}, {closest['scope']},",
        f"  {closest['metric']}, {closest['a']} vs {closest['b']} "
        f"({closest['win']}-{closest['loss']}): Holm p {f(closest['p_holm_reported'])} "
        f"reported, {f(closest['p_holm_exact'])} exact.",
        "",
        "## Every comparison significant under either test",
        "",
        "| family | scope | metric | a | b | W-L | Holm p reported | Holm p exact |",
        "|---|---|---|---|---|--:|--:|--:|",
    ]
    for r in out:
        if r["sig_reported"] or r["sig_exact"]:
            lines.append(f"| {r['family']} | {r['scope']} | {r['metric']} | {r['a']} | "
                         f"{r['b']} | {r['win']}-{r['loss']} | {f(r['p_holm_reported'])} | "
                         f"{f(r['p_holm_exact'])} |")
    if changed:
        lines += ["", "## Verdicts that change", ""]
        lines += [f"- {r['family']}, {r['scope']}, {r['metric']}, {r['a']} vs {r['b']}"
                  for r in changed]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {OUT_CSV.relative_to(REPO_ROOT)} and {OUT_MD.relative_to(REPO_ROOT)}")
    print(f"{len(sig_rep)} significant reported; {len(changed)} verdicts change under the exact test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
