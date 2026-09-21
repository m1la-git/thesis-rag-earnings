"""Assemble a manual faithfulness-review packet from one generator's records.

What this is
------------
The manual faithfulness check (README.md, "Measures"), done by the
researcher, needs a bounded, auditable sample of generations to read. This script
selects that sample by a **mechanical, seeded rule** and formats it. It makes no
judgement: no verdict, no failure-mode label, no proposed taxonomy, no
commentary. The taxonomy is built by reading the packet, so anything this script
suggested would contaminate it.

It reads already-persisted artifacts ONLY. No generator is called, and nothing
under `results/` is written.

Why a script exists at all
--------------------------
The earlier packet (`analysis/qwen3.8-27b_q4_k_xl/manual_review_packet.md`, the q4 arm) was
hand-assembled against a coverage objective -- "chosen to cover 12 of the 14
distinct thematic question_ids", and so on. That is curation, not a procedure:
it has no seed, no ordering rule, and its stratum sizes are themselves q4
findings. It cannot be restated in a methods chapter and it cannot be re-applied
to another generator without someone re-doing the curation by hand, which makes
the selector a participant in what gets read. This script replaces the curation
with a rule that fits in one sentence per stratum.

Strata (mutually exclusive by construction, asserted at run time)
----------------------------------------------------------------
S1  CENSUS -- every `answered_ungrounded` record, plus the single Case A
    `answered_grounded_offtarget`. Taken whole; nothing is sampled, so the RNG
    is not touched. Subsumes the `ref_unans_01` non-abstention set.
S2  `answered_grounded_offtarget` excluding the Case A record already in S1.
    Allocated across arm x category proportionally to cell size with
    largest-remainder rounding, floored at one per non-empty cell.
S3  Case C `abstained`. The one factual item is force-included -- it is a
    singleton and a uniform sample would drop it with probability 5/7 -- and
    the rest are sampled from the remainder.
S4  Case C `answered_grounded_correct` FLAGGED by Check 3 (attribution
    exposure), balanced across arms rather than proportionally, because the
    arm contrast is the thing this stratum exists to expose.
S5  Case C `answered_grounded_correct` NOT flagged -- the control, what a
    clean pass looks like.

Frame sizes are VERIFICATION TARGETS, not things to reproduce by adjustment. A
frame that comes out a different size stops the run before anything is selected;
a take is never silently resized to compensate for a frame that moved.

Guards
------
Both the input and the output path resolve through `src/model_paths.py` from a
REQUIRED `--model`. `--model` has no default on purpose: a defaulted run would
resolve to DEFAULT_MODEL's directory and overwrite the hand-curated q4 packet,
which no script produced and none can reproduce.
`refuse_handcurated_slot()` is the second, independent guard on the same
hazard.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import index  # noqa: E402
from model_paths import (  # noqa: E402
    DEFAULT_MODEL, analysis_path, ensure_analysis_dir, generation_outcomes_path,
)
from run_generation import generation_cache_path  # noqa: E402

# `retrieved_chunks` handles the Case A split (unanswerable items are excluded
# from Stage 1 retrieval scoring, so their top-5 lives in
# results/generation/case_a_retrieval/). Imported, not re-derived: a second
# implementation of "which five chunks entered the context" could diverge from
# the one every other diagnostic uses.
from check3_attribution_postfix import retrieved_chunks  # noqa: E402
from coverage_split import anchor_counts, group_of  # noqa: E402

BENCHMARK = REPO_ROOT / "benchmark" / "questions.jsonl"
CHECK3_CSV_NAME = "check3_enriched.csv"
OUT_MD_NAME = "manual_review_packet.md"
OUT_CSV_NAME = "manual_review_packet_manifest.csv"

# Deliberately NOT the generation seed (20260831). Reusing it would tie the
# reading order to the generation run for no reason and make the two look
# related when they are not.
SEED = 20260906

CORRECT = "answered_grounded_correct"
OFFTARGET = "answered_grounded_offtarget"
UNGROUNDED = "answered_ungrounded"
ABSTAINED = "abstained"

# From the caller's own frame verification. A mismatch is a STOP.
EXPECTED_FRAMES = {"S1": 10, "S2": 111, "S3": 35, "S4": 20, "S5": 89}
EXPECTED_S4_PER_ARM = 10
TAKES = {"S1": 10, "S2": 16, "S3": 10, "S4": 8, "S5": 4}
S4_PER_ARM = 4
TOTAL = 48

# The enriched prefix is index-side only (README.md invariant 4): the generator
# was shown `chunk["text"]`. This matches the FROZEN P2 prefix shape so the
# packet can assert it never prints one.
_ENRICHMENT_LINE_RE = re.compile(
    r"^.+ \([A-Z.]{1,6}\) (?:%s) \d{4} Q[1-4] \d{4} (?:%s)%s"
    % (
        "|".join(re.escape(v) for v in index.QUARTER_PROSE.values()),
        "|".join(re.escape(v) for v in index.SECTION_LABELS.values()),
        re.escape(index.ENRICHMENT_JOINER),
    )
)


def arm_of(condition_id: str) -> str:
    return "enriched" if condition_id.endswith("_enriched") else "text_only"


def stop(msg: str) -> None:
    raise SystemExit(f"STOP: {msg}")


def refuse_handcurated_slot(model: str, out_md: Path) -> None:
    """Refuse to write into the hand-curated q4 packet's slot.

    `--model qwen3.8-27b@q4_k_xl` resolves onto
    `analysis/qwen3.8-27b_q4_k_xl/manual_review_packet.md` -- a hand-assembled
    document that no script produced and none can reproduce, so writing there
    would be a destructive overwrite rather than a regeneration.
    """
    if model == DEFAULT_MODEL or out_md == analysis_path(DEFAULT_MODEL, OUT_MD_NAME):
        stop(
            f"refusing to write {out_md}.\n"
            f"  That is the q4 arm's packet, which was assembled BY HAND against a\n"
            "  coverage objective -- it has no seed, no ordering rule, and its stratum\n"
            "  sizes are q4 findings rather than parameters. This script cannot\n"
            "  reproduce it, so an overwrite would not be recoverable by re-running.\n"
            "  Pass a different --model."
        )


def load_rows(model: str) -> list[dict]:
    path = generation_outcomes_path(model)
    if not path.exists():
        stop(f"no generation outcomes table for {model!r} at {path}")
    rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
    wrong = {r.get("model") for r in rows} - {model}
    if wrong:
        stop(f"{path} contains rows for another generator: {sorted(wrong)}")
    return rows


def load_check3_flags(model: str) -> dict[tuple[str, str], bool]:
    """Check-3 attribution flags, per (condition_id, question_id)."""
    path = analysis_path(model, CHECK3_CSV_NAME)
    if not path.exists():
        stop(
            f"no Check 3 flag source for {model!r} at {path}.\n"
            "  S4/S5 are defined by that flag; run analysis/check3_enriched.py first."
        )
    flags = {}
    for r in csv.DictReader(path.read_text(encoding="utf-8").splitlines()):
        if r["model"] != model:
            stop(f"{path} contains a row for another generator: {r['model']!r}")
        flags[(r["condition_id"], r["question_id"])] = r["flagged"] == "True"
    return flags


def load_questions() -> dict:
    return {
        json.loads(line)["id"]: json.loads(line)
        for line in BENCHMARK.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def key(row: dict) -> tuple[str, str]:
    return (row["condition_id"], row["question_id"])


def build_frames(rows: list[dict], flags: dict) -> dict[str, list[dict]]:
    """The five frames. Sorted by (condition_id, question_id) so frame order is
    deterministic regardless of the order the table happened to be read in."""
    ung = [r for r in rows if r["outcome"] == UNGROUNDED]
    a_off = [r for r in rows if r["case"] == "A" and r["outcome"] == OFFTARGET]
    c_corr = [r for r in rows if r["case"] == "C" and r["outcome"] == CORRECT]
    missing = [key(r) for r in c_corr if key(r) not in flags]
    if missing:
        stop(f"{len(missing)} Case C correct records have no Check 3 flag, e.g. {missing[:3]}")
    frames = {
        "S1": ung + a_off,
        "S2": [r for r in rows if r["outcome"] == OFFTARGET and r["case"] != "A"],
        "S3": [r for r in rows if r["case"] == "C" and r["outcome"] == ABSTAINED],
        "S4": [r for r in c_corr if flags[key(r)]],
        "S5": [r for r in c_corr if not flags[key(r)]],
    }
    return {k: sorted(v, key=key) for k, v in frames.items()}


def verify_frames(frames: dict[str, list[dict]]) -> None:
    bad = [
        f"{name}: expected {EXPECTED_FRAMES[name]}, found {len(f)}"
        for name, f in frames.items()
        if len(f) != EXPECTED_FRAMES[name]
    ]
    per_arm = Counter(arm_of(r["condition_id"]) for r in frames["S4"])
    if set(per_arm.values()) != {EXPECTED_S4_PER_ARM}:
        bad.append(f"S4 per-arm: expected {EXPECTED_S4_PER_ARM} each, found {dict(per_arm)}")
    if bad:
        stop(
            "frame size mismatch -- nothing has been selected.\n  "
            + "\n  ".join(bad)
            + "\n  Reporting rather than resizing a take to compensate."
        )


def allocate(cells: Counter, take: int) -> dict:
    """Seats per cell: proportional, largest-remainder, floored at 1.

    The three operations run in the order stated: allocate proportionally to
    cell size, round by largest remainder, then apply the floor -- each cell
    lifted to 1 pays for the seat out of the largest cell. The floor is a
    correction to the proportional result, not a reservation taken before it.
    """
    n = sum(cells.values())
    quota = {k: take * v / n for k, v in cells.items()}
    alloc = {k: int(q) for k, q in quota.items()}
    order = sorted(cells, key=lambda k: (-(quota[k] - alloc[k]), k))
    for k in order[: take - sum(alloc.values())]:
        alloc[k] += 1
    for k in sorted(cells):
        if alloc[k] == 0:
            donor = max(alloc, key=lambda c: (alloc[c], cells[c]))
            alloc[donor] -= 1
            alloc[k] = 1
    over = [k for k in alloc if alloc[k] > cells[k]]
    if over or sum(alloc.values()) != take:
        stop(f"allocation invalid: total={sum(alloc.values())} take={take} over-drawn={over}")
    return alloc


def select(frames: dict[str, list[dict]], rng: random.Random) -> tuple[dict, dict]:
    """Draw each stratum. S1 is a census and draws nothing from the RNG."""
    chosen: dict[str, list[dict]] = {"S1": list(frames["S1"])}

    cells = Counter((arm_of(r["condition_id"]), r["category"]) for r in frames["S2"])
    alloc = allocate(cells, TAKES["S2"])
    s2 = []
    for cell in sorted(cells):
        pool = [r for r in frames["S2"] if (arm_of(r["condition_id"]), r["category"]) == cell]
        s2 += rng.sample(pool, alloc[cell])
    chosen["S2"] = s2

    factual = [r for r in frames["S3"] if r["category"] == "factual"]
    if len(factual) != 1:
        stop(
            f"expected exactly one factual Case C abstention, found {len(factual)}: "
            f"{[key(r) for r in factual]}.\n"
            "  The force-include is defined on that item being a singleton."
        )
    rest = [r for r in frames["S3"] if r is not factual[0]]
    chosen["S3"] = factual + rng.sample(rest, TAKES["S3"] - 1)

    s4 = []
    for a in ("enriched", "text_only"):
        s4 += rng.sample([r for r in frames["S4"] if arm_of(r["condition_id"]) == a], S4_PER_ARM)
    chosen["S4"] = s4

    chosen["S5"] = rng.sample(frames["S5"], TAKES["S5"])
    return chosen, alloc


def assert_selection(chosen: dict, rows: list[dict]) -> None:
    seen: dict[tuple[str, str], str] = {}
    for name, items in chosen.items():
        if len(items) != TAKES[name]:
            stop(f"{name} took {len(items)}, expected {TAKES[name]}")
        for r in items:
            if key(r) in seen:
                stop(f"{key(r)} appears in both {seen[key(r)]} and {name}")
            seen[key(r)] = name
    if len(seen) != TOTAL:
        stop(f"selected {len(seen)} items, expected {TOTAL}")
    universe = {key(r) for r in rows}
    absent = [k for k in seen if k not in universe]
    if absent:
        stop(f"selected items absent from the record set: {absent}")


def item_payload(row: dict, model: str, questions: dict, n_anchors: dict) -> dict:
    """Everything one item needs, with the two integrity checks that matter."""
    cid, qid = key(row)
    rec = json.loads(generation_cache_path(model, cid, qid).read_text(encoding="utf-8"))
    if rec["model"] != model:
        stop(f"{cid}/{qid}: generation record belongs to {rec['model']!r}")
    chunks = retrieved_chunks(cid, qid)

    # The text printed must be the text the generator saw. Chunk ids resolved
    # from the retrieval artifacts must equal the record's own, in order.
    ids = [c["chunk_id"] for c in chunks]
    if ids != rec["retrieved_chunk_ids"]:
        stop(
            f"{cid}/{qid}: retrieved chunk ids disagree with the generation record.\n"
            f"  retrieval: {ids}\n  record:    {rec['retrieved_chunk_ids']}"
        )
    # Invariant 1 / 4: the enriched string is index-side only and must never
    # reach this packet, or the text being read is not the text generated from.
    for c in chunks:
        if _ENRICHMENT_LINE_RE.match(c["text"]):
            stop(
                f"{cid}/{qid}: chunk {c['chunk_id']} carries a metadata-enrichment "
                "prefix. The packet must print raw chunk text, never index_text."
            )

    cov = float(row["coverage_at_5"]) if row["coverage_at_5"] not in ("", None) else None
    return {
        "condition_id": cid,
        "question_id": qid,
        "arm": arm_of(cid),
        "category": row["category"],
        "case": row["case"],
        "outcome": row["outcome"],
        "coverage": cov,
        # The single/full/partial split is defined on which of a question's
        # anchors were matched, so it is meaningful only where some were: Case A
        # has no anchors and no coverage value, Case B has coverage 0 and would
        # report "single" or "partial" for a question nothing was matched on.
        "group": group_of(n_anchors[qid], cov) if row["case"] == "C" else None,
        "question": questions[qid]["question"],
        "answer": rec["raw_response"],
        "chunks": chunks,
    }


def render(items: list[dict], model: str, flags: dict) -> str:
    out = [
        "# Manual review packet",
        "",
        f"Generator: `{model}`. {len(items)} items, drawn from the 12-condition grid by a",
        f"seeded mechanical rule (seed `{SEED}`) and shuffled into a single reading order.",
        "",
        "Assembled material only: no verdict, no failure-mode label, no proposed",
        "categories, no commentary. Stratum membership is deliberately NOT shown here --",
        f"it is in `{OUT_CSV_NAME}` beside this file, so the sampling rationale is",
        "auditable without being visible while reading.",
        "",
        "Chunk text is the raw chunk text the generator was given, never the",
        "metadata-enriched index string; chunk ids are asserted against each",
        "generation record's own `retrieved_chunk_ids`.",
        "",
        "---",
        "",
    ]
    for n, it in enumerate(items, 1):
        flag = flags.get((it["condition_id"], it["question_id"]))
        out += [
            f"## {n}. `{it['question_id']}` / `{it['condition_id']}`",
            "",
            f"- **condition:** {it['condition_id']}",
            f"- **arm:** {it['arm']}",
            f"- **question_id:** {it['question_id']}",
            f"- **category:** {it['category']}",
            f"- **case:** {it['case']}",
            f"- **outcome label:** {it['outcome']}",
        ]
        if it["group"] is not None:
            out.append(f"- **coverage group:** {it['group']} (coverage@5 = {it['coverage']:g})")
        elif it["coverage"] is not None:
            out.append(f"- **coverage@5:** {it['coverage']:g}")
        else:
            out.append("- **coverage@5:** n/a (unanswerable; excluded from retrieval metrics)")
        if flag is not None:
            out.append(f"- **Check 3 flag:** {'flagged' if flag else 'not flagged'}")
        out += [
            "",
            "**Question:**",
            "",
            "> " + it["question"].replace("\n", "\n> "),
            "",
            "**Generated answer, verbatim:**",
            "",
            "```",
            it["answer"],
            "```",
            "",
            "**Retrieved chunks (top 5), verbatim:**",
            "",
        ]
        for rank, c in enumerate(it["chunks"], 1):
            out += [f"*Rank {rank} — `{c['chunk_id']}`*", "", "```", c["text"], "```", ""]
        # Three empty slots per item, filled in by the reader. Empty on purpose:
        # a pre-filled verdict or failure-mode label would anchor the taxonomy
        # this packet exists to build.
        out += ["verdict:", "", "failure mode:", "", "notes:", "", "---", ""]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # No default: see refuse_handcurated_slot(). A defaulted run would resolve
    # onto the hand-curated q4 packet.
    ap.add_argument("--model", required=True, help="generator whose records to sample (required)")
    args = ap.parse_args()
    model = args.model

    out_md = analysis_path(model, OUT_MD_NAME)
    out_csv = analysis_path(model, OUT_CSV_NAME)
    refuse_handcurated_slot(model, out_md)

    rows = load_rows(model)
    flags = load_check3_flags(model)
    frames = build_frames(rows, flags)

    print(f"model: {model}   seed: {SEED}   records: {len(rows)}")
    print("\nframe sizes (expected -> found):")
    for name in sorted(frames):
        f = frames[name]
        mark = "ok" if len(f) == EXPECTED_FRAMES[name] else "MISMATCH"
        print(f"  {name}  {EXPECTED_FRAMES[name]:4d} -> {len(f):4d}  {mark}")
    verify_frames(frames)

    rng = random.Random(SEED)
    chosen, alloc = select(frames, rng)
    assert_selection(chosen, rows)

    print("\nS2 allocation (arm x category), proportional / largest-remainder / floor 1:")
    cells = Counter((arm_of(r["condition_id"]), r["category"]) for r in frames["S2"])
    for cell in sorted(cells):
        print(f"  {cell[0]:10s} {cell[1]:12s} n={cells[cell]:4d}  seats={alloc[cell]}")

    stratum_of = {key(r): name for name, items in chosen.items() for r in items}
    flat = [r for items in chosen.values() for r in items]
    rng.shuffle(flat)

    questions = load_questions()
    n_anchors = anchor_counts()
    items = [item_payload(r, model, questions, n_anchors) for r in flat]

    ensure_analysis_dir(model)
    out_md.write_text(render(items, model, flags), encoding="utf-8")
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([
            "reading_number", "stratum", "model", "condition_id", "arm", "question_id",
            "category", "case", "outcome", "coverage_at_5", "coverage_group", "check3_flagged",
        ])
        for n, it in enumerate(items, 1):
            k = (it["condition_id"], it["question_id"])
            w.writerow([
                n, stratum_of[k], model, it["condition_id"], it["arm"], it["question_id"],
                it["category"], it["case"], it["outcome"],
                "" if it["coverage"] is None else f"{it['coverage']:g}",
                it["group"] or "", "" if flags.get(k) is None else flags[k],
            ])

    print(f"\ntakes: " + "  ".join(f"{k}={len(v)}" for k, v in sorted(chosen.items())))
    print(f"wrote {out_md}")
    print(f"wrote {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
