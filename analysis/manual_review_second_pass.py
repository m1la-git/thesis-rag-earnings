"""Build the second-pass worksheet from an annotated manual review packet.

What the second pass is for
---------------------------
The packet is a first pass: 48 items read one at a time, in a shuffled order, each
with a verdict, a failure mode and a note. That produces 48 independent readings
and no taxonomy. The second pass is where the taxonomy comes from -- sorting the
48 into **piles** and naming what each pile has in common.

Two axes, not one
-----------------
An item can fail as a MODEL behaviour and, independently, expose something about
the INSTRUMENT -- a scorer rule firing on the wrong thing, a benchmark item that
cannot score. Those are different claims about different objects, and forcing
them into one set of piles corrupts both counts: an instrument finding buried in
a "no defect found" pile makes the generator look cleaner than it is, and one
promoted to a pile of its own inflates the failure taxonomy with something that
is not a failure of the generator at all.

So the worksheet carries `pile` (model behaviour) and `instr` (instrument or
benchmark) as separate columns. Every item gets exactly one pile; `instr` is
blank for most of them. Piles are multi-valued on purpose -- an answer that
names the wrong company AND the wrong quarter is both, and picking one loses a
real observation.

This script does NOT assign either. It carries the first-pass annotations across
verbatim, lays them out so items can be compared side by side instead of one at a
time, and leaves every `pile` and `instr` cell empty. Proposing them here would
make the taxonomy an output of the tooling rather than of the reading, which is
the whole thing the shuffled packet exists to prevent.

Read-only with respect to the packet: it parses, it never edits.

This always produces an EMPTY worksheet. The filled one is in git -- if a rerun
empties it, that is a large deletion in `git diff`; restore with `git checkout`.

Why the first-pass fields are shown at all
------------------------------------------
They are the thing being revised. A worksheet that hid them would force a third
reading of the packet to find out what was already concluded about an item, and
the point of a second pass is to overrule the first where it was wrong -- which
requires seeing it. The scorer's own outcome label is shown beside them for the
same reason, and neither is authority: the packet's own header says the label is
the scorer's judgement, not ground truth.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import analysis_path, ensure_analysis_dir  # noqa: E402

PACKET_NAME = "manual_review_packet.md"
OUT_MD_NAME = "manual_review_second_pass.md"

# One heading per item: "## 7. `ref_them_04` / `chunk500_hybrid_enriched`"
_HEAD_RE = re.compile(r"^## (\d+)\. `([^`]+)` / `([^`]+)`$")
_FIELD_RE = re.compile(r"^- \*\*([^:*]+):\*\* (.*)$")

# Left blank on purpose. The count is a reminder that a pile with one member is
# usually a note, not a pile -- but that judgement belongs to the reader.
BLANK_PILE_ROWS = 8
BLANK_INSTRUMENT_ROWS = 5


def stop(msg: str) -> None:
    raise SystemExit(f"STOP: {msg}")


def parse_packet(path: Path) -> list[dict]:
    """Every item, with its metadata and its three first-pass annotations."""
    if not path.exists():
        stop(f"no packet at {path}. Run analysis/manual_review_packet.py first.")
    lines = path.read_text(encoding="utf-8").split("\n")
    heads = [i for i, l in enumerate(lines) if _HEAD_RE.match(l)]
    if not heads:
        stop(f"{path} has no item headings -- is it the packet?")

    items = []
    for pos, i in enumerate(heads):
        end = heads[pos + 1] if pos + 1 < len(heads) else len(lines)
        n, qid, cond = _HEAD_RE.match(lines[i]).groups()
        it = {"n": int(n), "question_id": qid, "condition": cond}
        for line in lines[i:end]:
            m = _FIELD_RE.match(line)
            if m:
                it[m.group(1).strip().lower()] = m.group(2).strip()
            for key in ("verdict", "failure mode", "notes"):
                if line.startswith(f"{key}: "):
                    it[key] = line[len(key) + 2:].strip()
        missing = [k for k in ("verdict", "failure mode", "notes") if not it.get(k)]
        if missing:
            stop(
                f"item {n} ({qid} / {cond}) has no {', '.join(missing)}.\n"
                "  The second pass revises the first; there is nothing to revise until\n"
                "  every item is annotated. Fill the packet in before building this."
            )
        items.append(it)
    return items


def cell(s: str, width: int | None = None) -> str:
    s = (s or "—").replace("|", "\\|").replace("\n", " ")
    return s if width is None or len(s) <= width else s[: width - 1] + "…"


def render(items: list[dict], model: str, packet_rel: str) -> str:
    out = [
        "# Second-pass worksheet — manual faithfulness review",
        "",
        f"Generator: `{model}`. {len(items)} items, carried across verbatim from",
        f"`{packet_rel}`.",
        "",
        "**Piles are deliberately unassigned.** The first pass read each item alone, in a",
        "shuffled order, which is what keeps 48 readings independent. This pass is the",
        "opposite move: put them side by side, decide what actually groups, and name it.",
        "Nothing here proposes a grouping — a pile that arrives pre-named is an artifact",
        "of the tooling rather than a finding about the generator.",
        "",
        "## How to use this",
        "",
        "1. Read section 3 straight through once without writing anything. It is the",
        "   whole first pass in one view, which the packet deliberately never gives you.",
        "2. Name the piles in section 2 as they suggest themselves. Give each a short",
        "   id (`P1`, `P2`, …) and a definition sharp enough to exclude something.",
        "3. Put pile ids in each row's `pile` cell in section 3. More than one is fine",
        "   and often right — an answer that names the wrong company AND the wrong",
        "   quarter is both, and picking one loses a real observation. An item that",
        "   resists every pile is telling you the piles are wrong.",
        "4. Put an instrument id in `instr` where the item says something about the",
        "   SCORER or the BENCHMARK rather than the generator. Independent of the pile:",
        "   an item can be a clean answer and still expose a defective rule.",
        "5. Revise the first-pass verdict or failure mode wherever sorting shows it was",
        "   wrong. That is the point of the pass, not a side effect — the `verdict` and",
        "   `failure mode` columns are drafts, and the scorer's `outcome` column is not",
        "   ground truth either.",
        "6. Section 5 is for what neither axis covers. A pile with one member is",
        "   usually a single observation, not a mode — say so there rather than",
        "   promoting it.",
        "",
        "## 1. What is being sorted",
        "",
        "| | |",
        "|---|--:|",
        f"| items | {len(items)} |",
        f"| distinct questions | {len({i['question_id'] for i in items})} |",
        f"| distinct conditions | {len({i['condition'] for i in items})} |",
        "| piles named | _(0)_ |",
        "| instrument findings named | _(0)_ |",
        "| items assigned to a pile | _(0)_ |",
        "",
        "## 2. Piles",
        "",
        "Name them here. A pile needs a definition that could exclude an item, not a",
        "label that could absorb any of them.",
        "",
        "| id | name (a behaviour, not a category) | definition (what is in, and what is deliberately out) | n |",
        "|---|---|---|--:|",
    ]
    for k in range(1, BLANK_PILE_ROWS + 1):
        out.append(f"| P{k} |  |  |  |")
    out += [
        "",
        "Name a pile by what the generator DID, not by the bucket it belongs to.",
        "\"attributes one company's material to another\" can be checked against an item;",
        "\"company identity\" cannot.",
        "",
        "### 2b. Instrument and benchmark findings — a SEPARATE axis",
        "",
        "Not piles. These are claims about the scorer or the benchmark, not about the",
        "generator, and an item can carry one at the same time as a pile. Keeping them",
        "here is what stops an instrument defect from either hiding inside a clean pile",
        "or inflating the failure taxonomy with something that is not a model failure.",
        "",
        "| id | finding | what it means for any count computed from the outcome labels | n |",
        "|---|---|---|--:|",
    ]
    for k in range(1, BLANK_INSTRUMENT_ROWS + 1):
        out.append(f"| I{k} |  |  |  |")
    out += [
        "",
        "## 3. Items",
        "",
        "`#` is the packet's reading number — the item's full text, answer and five",
        "chunks are under that heading in the packet. `outcome` is the scorer's label;",
        "`verdict` and `failure mode` are the first pass's.",
        "",
        "| # | pile | instr | question_id | condition | cat | case | outcome (scorer) | verdict (1st pass) | failure mode (1st pass) |",
        "|--:|---|---|---|---|---|:-:|---|---|---|",
    ]
    for it in items:
        out.append(
            f"| {it['n']} |  |  | `{it['question_id']}` | `{it['condition']}` | "
            f"{cell(it.get('category'), 12)} | {cell(it.get('case'), 4)} | "
            f"{cell(it.get('outcome label'), 28)} | {cell(it['verdict'], 32)} | "
            f"{cell(it['failure mode'], 110)} |"
        )
    out += [
        "",
        "## 4. Notes carried forward",
        "",
        "The first-pass note for each item, in reading order, so the worksheet stands on",
        "its own. Edit freely — these are drafts.",
        "",
    ]
    for it in items:
        out.append(f"**{it['n']}. `{it['question_id']}` / `{it['condition']}`**  ")
        out.append(f"{it['notes']}")
        out.append("")
        out.append("second-pass note:")
        out.append("")
    out += [
        "## 5. What the piles do not cover",
        "",
        "Anything that survived the sort without fitting: single items that are their own",
        "category, tensions between piles, and anything the packet cannot settle because",
        "the evidence is not in it.",
        "",
        "-",
        "",
        "## 6. What this changes upstream",
        "",
        "Findings here that are about the instrument rather than the generator — a",
        "scorer rule that fires on the wrong thing, a benchmark item that cannot score —",
        "belong in the project documentation or a diagnostic, not only in this worksheet. List them so",
        "they are not lost when the piles become prose.",
        "",
        "-",
        "",
    ]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--model", required=True,
                    help="generator whose annotated packet to build from (required)")
    args = ap.parse_args()

    packet = analysis_path(args.model, PACKET_NAME)
    out_md = analysis_path(args.model, OUT_MD_NAME)
    if out_md.exists():
        stop(
            f"{out_md} already exists.\n"
            "  Regenerating would discard whatever piles have been assigned in it --\n"
            "  this script only ever builds an EMPTY worksheet. Move or delete the\n"
            "  existing one first if you really want to start the sort over."
        )

    items = parse_packet(packet)
    ensure_analysis_dir(args.model)
    out_md.write_text(
        render(items, args.model, str(packet.relative_to(REPO_ROOT)).replace("\\", "/")),
        encoding="utf-8",
    )
    print(f"model:  {args.model}")
    print(f"packet: {packet.relative_to(REPO_ROOT)}  ({len(items)} items)")
    print(f"wrote   {out_md.relative_to(REPO_ROOT)}  -- piles empty, by design")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
