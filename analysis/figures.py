"""Thesis figures, rendered to vector PDF for LaTeX.

Two figures, each chosen for the job its data has to do rather than for variety.

  Figure 1 -- retrieval coverage, DUMBBELL.
      The finding is the MOVEMENT from text_only to metadata_enriched within
      each of the six chunk-size x strategy cells, so the chart encodes movement
      as length. A grouped bar chart would show the same twelve numbers while
      making the reader compute the six differences that are the point.

  Figure 2 -- answer outcomes by case, HORIZONTAL STACKED BAR.
      Part-to-whole within each ground-truth case. Table 3 already carries the
      exact counts; what it does not show at a glance is that the three cases
      have three different SHAPES, which is the whole argument for interpreting
      outcomes per case rather than pooled. Table 3's own column totals are a
      reconciliation that the four outcomes account for every generation, not a
      result: no rate, share or comparison is computed on them. (This said
      "never pooled" until 2026-09-10, which the table contradicted by carrying
      those totals.)

Design constraints, and why they are not negotiable here
--------------------------------------------------------
GREYSCALE, NOT COLOUR. A bachelor thesis is printed and photocopied, and the
chair's template is a black-and-white document. A hue-coded figure degrades to
mud in the one medium it is guaranteed to be read in. Everything below is a
lightness ramp plus hatching, which survives print, photocopying and every form
of colour vision deficiency at once.

IDENTITY IS NEVER CARRIED BY FILL ALONE. Every stacked segment is hatched AND
directly labelled, and the dumbbell's two ends are labelled on the first row and
distinguished by marker shape as well as fill. Fill is the third cue, not the
only one.

SERIF TO MATCH THE DOCUMENT. Times New Roman, so a figure's axis labels do not
announce themselves as foreign to the body text. Falls back through STIX to
DejaVu Serif so this runs on a machine without the Microsoft fonts.

RECESSIVE CHROME. Hairline axes, no top or right spine, no gridline heavier than
the data, no dashes. The marks are the only dark thing on the page.

Sources
-------
Figure 1 reads `results/tables/retrieval_metrics.csv` -- Stage 1, which never
calls a generator, so the figure belongs to no arm.
Figure 2 reads the REPORTED arm's outcomes table only. No figure is produced for
the validator baseline or the robustness check, for the same reason no table is:
a figure carries no arm label and is the easiest thing in a thesis to mistake
for a result.

Read-only. Writes thesis/generated/figure_*.pdf (and .png with --png, for
looking at while iterating -- LaTeX uses the PDF).

Usage
-----
    python analysis/figures.py
    python analysis/figures.py --png
"""

from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import generation_outcomes_path  # noqa: E402

METRICS_CSV = REPO_ROOT / "results" / "tables" / "retrieval_metrics.csv"
OUT_DIR = REPO_ROOT / "thesis" / "generated"
REPORTED_MODEL = "qwen3.8-27b@q8_k_xl"

OVERALL = "overall_not_cross_category_comparable"
COVERAGE = "anchor_coverage_at_5"

# Ordered so the reader walks strategy-major, size-minor: the pairs that share a
# strategy sit together, which is the comparison H3 is about.
CELLS = [(200, "dense"), (500, "dense"),
         (200, "hybrid"), (500, "hybrid"),
         (200, "bm25"), (500, "bm25")]
STRATEGY_LABEL = {"dense": "Dense", "bm25": "BM25", "hybrid": "Hybrid"}

CASES = ["A", "B", "C"]
OUTCOMES = ["abstained", "answered_grounded_correct",
            "answered_grounded_offtarget", "answered_ungrounded"]
OUTCOME_LABEL = {"abstained": "Abstained",
                 "answered_grounded_correct": "Grounded, on target",
                 "answered_grounded_offtarget": "Grounded, off target",
                 "answered_ungrounded": "Ungrounded"}
CASE_BLURB = {"A": "A  no anchor exists",
              "B": "B  anchor not retrieved",
              "C": "C  anchor retrieved"}

# A lightness ramp, not a hue ramp. Steps are spaced far enough apart to survive
# a photocopier; hatching carries identity when they do not.
INK = "#1a1a1a"
MUTED = "#767676"
FILLS = ["#e8e8e8", "#bdbdbd", "#8a8a8a", "#4a4a4a"]
HATCHES = ["", "///", "...", "xx"]


def style() -> None:
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 9,
        "axes.edgecolor": MUTED,
        "axes.linewidth": 0.6,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK,
        "ytick.labelcolor": INK,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "figure.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,   # embed real glyphs, not Type 3 outlines
    })


def read_coverage() -> dict[tuple[int, str, str], float]:
    out = {}
    with METRICS_CSV.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["breakdown_type"] != OVERALL or r["metric"] != COVERAGE:
                continue
            out[(int(r["chunk_size"]), r["retrieval_strategy"],
                 r["indexing_representation"])] = float(r["value"])
    missing = [c for c in CELLS
               if (c[0], c[1], "text_only") not in out
               or (c[0], c[1], "metadata_enriched") not in out]
    if missing:
        raise SystemExit(f"missing coverage rows for {missing}")
    return out


def figure_coverage(path_stem: Path, also_png: bool) -> None:
    cov = read_coverage()
    fig, ax = plt.subplots(figsize=(5.4, 3.1))

    ys = list(range(len(CELLS)))[::-1]
    for y, (size, strat) in zip(ys, CELLS):
        a = cov[(size, strat, "text_only")]
        b = cov[(size, strat, "metadata_enriched")]
        # The connector is the finding: its length IS the effect.
        ax.plot([a, b], [y, y], color=MUTED, linewidth=1.4,
                solid_capstyle="round", zorder=1)
        ax.scatter([a], [y], s=46, facecolor="white", edgecolor=INK,
                   linewidth=1.1, marker="o", zorder=3)
        ax.scatter([b], [y], s=52, facecolor=INK, edgecolor=INK,
                   linewidth=1.1, marker="D", zorder=3)
        # APA: a quantity that cannot exceed 1 carries no leading zero.
        ax.annotate(f"{b - a:+.3f}".replace("0.", ".", 1), xy=(max(a, b), y), xytext=(7, 0),
                    textcoords="offset points", va="center", fontsize=8,
                    color=INK)

    ax.set_yticks(ys)
    ax.set_yticklabels([f"{STRATEGY_LABEL[s]}, {n}" for n, s in CELLS])
    ax.set_xlabel("Anchor coverage@5")
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: "0" if v == 0 else f"{v:.1f}".replace("0.", ".", 1)))
    ax.set_xlim(0, 0.52)
    ax.set_ylim(-0.6, len(CELLS) - 0.4)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color="#e0e0e0", linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)

    ax.legend(handles=[
        Line2D([], [], marker="o", linestyle="none", markersize=7,
               markerfacecolor="white", markeredgecolor=INK, label="Text-only"),
        Line2D([], [], marker="D", linestyle="none", markersize=7,
               markerfacecolor=INK, markeredgecolor=INK,
               label="Metadata-enriched")],
        loc="lower right", frameon=False, fontsize=8, handletextpad=0.4)

    save(fig, path_stem, also_png)


# The research model. Unlike the other two figures this one plots no data: it is
# the design the chair's guidelines ask to see as a graphic (a research-model
# diagram), so its content is the factors, the hypotheses and the two measured
# stages, all of which are fixed by the design rather than read from results/.
FACTORS = [("Chunk size", "200, 500 tokens", "H1"),
           ("Retrieval strategy", "dense, BM25, hybrid", "H2"),
           ("Indexing representation", "text-only, metadata-enriched", "H3")]


def _box(ax, x, y, w, h, title, sub, fill="white"):
    ax.add_patch(Rectangle((x, y - h / 2), w, h, facecolor=fill,
                           edgecolor=INK, linewidth=0.6, zorder=2))
    ax.text(x + w / 2, y + 0.052, title, ha="center", va="center",
            fontsize=9, color=INK, zorder=3)
    ax.text(x + w / 2, y - 0.055, sub, ha="center", va="center",
            fontsize=7.5, color=MUTED, zorder=3)


def figure_research_model(path_stem: Path, also_png: bool) -> None:
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Full-bleed axes: the layout below is in figure fractions, so a box
    # width means what it says and the labels inside it have the room.
    ax.set_position([0, 0, 1, 1])

    lx, lw = 0.00, 0.32
    mx, mw = 0.40, 0.30
    rx, rw = 0.78, 0.22
    h, ys = 0.20, [0.84, 0.50, 0.16]

    for (title, sub, tag), y in zip(FACTORS, ys):
        _box(ax, lx, y, lw, h, title, sub, fill=FILLS[0])
        ax.annotate("", xy=(mx, 0.50 + (y - 0.50) * 0.14),
                    xytext=(lx + lw, y),
                    arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=0.9,
                                    shrinkA=2, shrinkB=2))
        # The tag rides its own arrow's midpoint, on the open side of the
        # line: below a descending arrow, above an ascending one.
        mid = (y + 0.50 + (y - 0.50) * 0.14) / 2
        below = y > 0.50
        ax.text((lx + lw + mx) / 2 - 0.018, mid + (-0.022 if below else 0.030),
                tag, ha="center", va="top" if below else "bottom",
                fontsize=8, color=INK)

    _box(ax, mx, 0.50, mw, h, "Retrieval quality", "anchor coverage@5, MRR@5")
    ax.text(mx + mw / 2, 0.50 - h / 2 - 0.040, "Stage 1", ha="center",
            va="top", fontsize=8, color=MUTED)

    _box(ax, rx, 0.50, rw, h, "Answer behavior", "case × outcome")
    ax.text(rx + rw / 2, 0.50 - h / 2 - 0.040, "Stage 2", ha="center",
            va="top", fontsize=8, color=MUTED)

    # Dashed, because the answer stage was examined without a hypothesis being
    # scored on it: the exact test could not reach significance at these counts.
    ax.annotate("", xy=(rx, 0.50), xytext=(mx + mw, 0.50),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=0.9,
                                linestyle=(0, (4, 2)), shrinkA=2, shrinkB=2))
    ax.text((mx + mw + rx) / 2, 0.685, "examined,", ha="center", va="bottom",
            fontsize=8, color=MUTED)
    ax.text((mx + mw + rx) / 2, 0.635, "not hypothesized", ha="center",
            va="bottom", fontsize=8, color=MUTED)

    save(fig, path_stem, also_png)


def read_grid(model: str) -> tuple[collections.Counter, int]:
    path = generation_outcomes_path(model)
    if not path.exists():
        raise SystemExit(f"missing outcomes table for {model!r}: {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    grid = collections.Counter((r["case"], r["outcome"]) for r in rows)
    if sum(grid.values()) != len(rows):
        raise SystemExit("grid does not reconcile with the table")
    return grid, len(rows)


def figure_case_outcome(path_stem: Path, also_png: bool) -> None:
    grid, total = read_grid(REPORTED_MODEL)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))

    ys = [2, 1, 0]
    for y, case in zip(ys, CASES):
        n = sum(grid[(case, o)] for o in OUTCOMES)
        left = 0.0
        for i, outcome in enumerate(OUTCOMES):
            v = grid[(case, outcome)]
            if v == 0:
                continue
            share = 100.0 * v / n
            # A 2px surface gap between segments, as the mark spec asks: the
            # boundary reads as a boundary rather than as a shade change.
            ax.barh(y, share, left=left, height=0.58, color=FILLS[i],
                    edgecolor="white", linewidth=1.2, hatch=HATCHES[i],
                    zorder=2)
            if share >= 7:
                ax.text(left + share / 2, y, str(v), ha="center", va="center",
                        fontsize=8,
                        color="white" if i == len(OUTCOMES) - 1 else INK,
                        zorder=3)
            left += share
        ax.text(101, y, f"$n$ = {n}", va="center", fontsize=8, color=MUTED)

    ax.set_yticks(ys)
    ax.set_yticklabels([CASE_BLURB[c] for c in CASES])
    # matplotlib is not LaTeX -- a backslash-escaped percent renders literally.
    ax.set_xlabel("Share of generations within case (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 2.6)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_axisbelow(True)

    ax.legend(handles=[Patch(facecolor=FILLS[i], edgecolor="white",
                             hatch=HATCHES[i], label=OUTCOME_LABEL[o])
                       for i, o in enumerate(OUTCOMES)],
              loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2,
              frameon=False, fontsize=8, handlelength=1.8, handletextpad=0.5)

    save(fig, path_stem, also_png)


def save(fig, stem: Path, also_png: bool) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"))
    print(f"wrote {stem.with_suffix('.pdf').relative_to(REPO_ROOT)}")
    if also_png:
        fig.savefig(stem.with_suffix(".png"), dpi=200)
        print(f"wrote {stem.with_suffix('.png').relative_to(REPO_ROOT)}")
    plt.close(fig)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--png", action="store_true",
                    help="also write PNGs, for looking at while iterating")
    args = ap.parse_args()

    style()
    figure_research_model(OUT_DIR / "figure_research_model", args.png)
    figure_coverage(OUT_DIR / "figure_coverage", args.png)
    figure_case_outcome(OUT_DIR / "figure_case_outcome", args.png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
