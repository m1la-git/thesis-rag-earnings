"""Regenerate the two long-format analysis CSVs from the persisted records.

Why this exists
---------------
`analysis/stage1/stage1_scores_long.csv` and `analysis/qwen3.8-27b_q4_k_xl/stage2_outcomes_long.csv` were
produced by ad-hoc scripts that were never kept. They are cited by
`analysis/stage1/stage1_diagnostics.md` (Part 6) and `analysis/qwen3.8-27b_q4_k_xl/stage2_statistics.md`
("everything below is reproducible by pivoting that file") as the reproducible
basis for every statistic in those documents -- but with no generator on disk,
neither could actually be reproduced, and both described 6 conditions after the
grid grew to 12.

This is that generator, tracked.

Validation protocol
-------------------
`--validate` rebuilds each file restricted to the six `text_only` conditions and
diffs it against the committed artifact, field by field. It must reproduce them
EXACTLY before any extended version is written. A mismatch is reported, not
worked around: it would mean either the original used a method that is no longer
recoverable, or this rebuild is wrong, and those need different responses.

`--write` emits the extended versions to NEW paths. The originals are never
overwritten -- they are the historical 6-condition record.

Coverage note (important, and not symmetric between the two files)
------------------------------------------------------------------
Stage 1 retrieval exists for all 12 conditions, so the Stage 1 long table
extends to 480 rows. **Stage 2 generation exists only for the six `text_only`
conditions** (on `qwen3.8-27b@q4_k_xl`), so the Stage 2 long table cannot be
extended to 12 -- there is nothing to extend it with, and running generation is
out of scope. Its rebuilt version therefore still covers 6 conditions; it gains
the `indexing_representation` column (constant `text_only`) so that when the
enriched arm is eventually generated the schema is already correct. The output
filename states its coverage rather than implying 12.

Usage
-----
    python analysis/rebuild_long_tables.py --validate
    python analysis/rebuild_long_tables.py --write
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import (  # noqa: E402
    DEFAULT_MODEL, analysis_path, ensure_analysis_dir, generation_outcomes_path,
    stage1_path,
)

RETRIEVAL_DIR = REPO_ROOT / "results" / "retrieval"
# Model-scoped, resolved per --model.

# Validation targets AND rebuilt outputs are model-scoped via analysis_path().
# The two Stage 2 tables are model-scoped; the two Stage 1 tables are not
# (see stage1_path). Under q4 the Stage 2 pair resolves into the q4
# regression check reads and reproduces exactly the files it always did. Under
# any other generator they resolve into analysis/{slug}/ -- which is normally
# empty, and that absence is the FIRST RUN signal (see main()): a q8 rebuild
# must never be diffed against a q4 reference, and must never silently pass for
# lack of one.
STAGE1_ORIGINAL_NAME = "stage1_scores_long.csv"
STAGE2_ORIGINAL_NAME = "stage2_outcomes_long.csv"
STAGE1_REBUILT_NAME = "stage1_scores_long_12cond.csv"
STAGE2_REBUILT_NAME = "stage2_outcomes_long_6cond.csv"

TEXT_ONLY_CONDITIONS = [
    "chunk200_bm25", "chunk200_dense", "chunk200_hybrid",
    "chunk500_bm25", "chunk500_dense", "chunk500_hybrid",
]

# Persisted run_meta from the original six carries no indexing_representation --
# they predate the field and are the text_only arm by construction (README.md
# invariant 5), so they are READ with this default rather than re-run.
DEFAULT_REPRESENTATION = "text_only"

STAGE1_FIELDS_ORIGINAL = [
    "condition_id", "chunk_size", "strategy", "question_id", "category",
    "chunk_size_sensitive", "anchor_coverage_at_5", "mean_reciprocal_rank_at_5",
]
STAGE2_FIELDS_ORIGINAL = [
    "question_id", "condition_id", "chunk_size", "retrieval_strategy", "category",
    "case", "outcome", "coverage_at_5", "chunk_size_sensitive", "bertscore_cosine",
]


def persisted_conditions() -> list[str]:
    """Every condition with a persisted Stage 1 file, in sorted order."""
    return sorted(p.stem for p in RETRIEVAL_DIR.glob("*.jsonl"))


def read_stage1(condition_id: str) -> tuple[dict, list[dict]]:
    meta, records = None, []
    for line in (RETRIEVAL_DIR / f"{condition_id}.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row["_type"] == "run_meta":
            meta = row
        elif row["_type"] == "question_result":
            records.append(row)
    return meta, records


def build_stage1(condition_ids: list[str], with_representation: bool) -> list[dict]:
    """One row per (condition, question) with both retrieval metrics.

    Column order and row order follow the committed artifact exactly: conditions
    in sorted order, questions in the order Stage 1 persisted them.
    """
    rows = []
    for condition_id in sorted(condition_ids):
        meta, records = read_stage1(condition_id)
        representation = meta.get("indexing_representation", DEFAULT_REPRESENTATION)
        for record in records:
            row = {
                "condition_id": condition_id,
                "chunk_size": meta["chunk_size"],
                "strategy": meta["retrieval_strategy"],
                "question_id": record["question_id"],
                "category": record["category"],
                "chunk_size_sensitive": record["chunk_size_sensitive"],
                "anchor_coverage_at_5": record["retrieval_metrics"]["anchor_coverage_at_5"],
                "mean_reciprocal_rank_at_5": record["retrieval_metrics"]["mean_reciprocal_rank_at_5"],
            }
            if with_representation:
                # Inserted after `strategy` so the three independent variables sit together.
                row = {
                    **{k: row[k] for k in ("condition_id", "chunk_size", "strategy")},
                    "indexing_representation": representation,
                    **{k: row[k] for k in STAGE1_FIELDS_ORIGINAL if k not in ("condition_id", "chunk_size", "strategy")},
                }
            rows.append(row)
    return rows


def build_stage2(with_representation: bool, model: str = DEFAULT_MODEL,
                 conditions: list[str] | None = None) -> list[dict]:
    """One row per (condition, question) of scored generation output.

    A projection of `results/tables/{model_slug}/generation_outcomes.csv` -- same rows, same
    order, a subset of columns reordered. That table is the scorer's own output,
    so deriving from it (rather than re-deriving case/outcome here) keeps this
    file a view of the scored results rather than a second implementation of the
    scorer.
    """
    path = generation_outcomes_path(model)
    with path.open(newline="", encoding="utf-8") as f:
        source = [r for r in csv.DictReader(f) if r.get("model") == model]
    if conditions is not None:
        source = [r for r in source if r["condition_id"] in set(conditions)]
    if not source:
        raise SystemExit(f"no rows in {path} for model {model!r}")

    rows = []
    for r in source:
        row = {k: r[k] for k in STAGE2_FIELDS_ORIGINAL}
        if with_representation:
            row = {
                "model": r.get("model", model),
                "question_id": row["question_id"],
                "condition_id": row["condition_id"],
                "chunk_size": row["chunk_size"],
                "retrieval_strategy": row["retrieval_strategy"],
                "indexing_representation": r.get("indexing_representation") or DEFAULT_REPRESENTATION,
                **{k: row[k] for k in STAGE2_FIELDS_ORIGINAL
                   if k not in ("question_id", "condition_id", "chunk_size", "retrieval_strategy")},
            }
        rows.append(row)
    return rows


def diff_against(rows: list[dict], original_path: Path, float_fields: set[str]) -> list[str]:
    """Field-by-field diff of rebuilt rows against a committed CSV."""
    with original_path.open(newline="", encoding="utf-8") as f:
        original = list(csv.DictReader(f))

    problems = []
    if len(rows) != len(original):
        problems.append(f"row count: rebuilt {len(rows)}, original {len(original)}")
        return problems
    if original and list(original[0].keys()) != list(rows[0].keys()):
        problems.append(
            f"column order: rebuilt {list(rows[0].keys())}, original {list(original[0].keys())}"
        )
        return problems

    for i, (a, b) in enumerate(zip(rows, original)):
        for key in b:
            av, bv = str(a[key]), b[key]
            if key in float_fields:
                if (av == "") != (bv == ""):
                    problems.append(f"row {i} {key}: rebuilt {av!r}, original {bv!r}")
                elif av and abs(float(av) - float(bv)) > 1e-12:
                    problems.append(f"row {i} {key}: rebuilt {av}, original {bv}")
            elif av != bv:
                problems.append(f"row {i} ({a.get('condition_id')}/{a.get('question_id')}) "
                                f"{key}: rebuilt {av!r}, original {bv!r}")
    return problems


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true",
                        help="reproduce the committed 6-condition artifacts and diff; write nothing")
    parser.add_argument("--write", action="store_true",
                        help="write the extended versions to new paths (validates first)")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"generator model whose scored table to read (default: {DEFAULT_MODEL})")
    args = parser.parse_args()
    if not (args.validate or args.write):
        parser.error("pass --validate or --write")

    # Stage 1 is generator-independent; Stage 2 is not. Before the split both
    # went through analysis_path(), which would now file the Stage 1 tables
    # under a model slug they do not belong to.
    stage1_original = stage1_path(STAGE1_ORIGINAL_NAME)
    stage2_original = analysis_path(args.model, STAGE2_ORIGINAL_NAME)
    stage1_rebuilt = stage1_path(STAGE1_REBUILT_NAME)
    stage2_rebuilt = analysis_path(args.model, STAGE2_REBUILT_NAME)

    print(f"VALIDATION -- rebuild restricted to the six text_only conditions, "
          f"model {args.model!r}\n")

    s1 = build_stage1(TEXT_ONLY_CONDITIONS, with_representation=False)
    # Restricted to the six text_only conditions, matching what the committed
    # artifact covers -- the live table now holds all 12.
    s2 = build_stage2(with_representation=False, model=args.model,
                      conditions=TEXT_ONLY_CONDITIONS)

    missing = [q.relative_to(REPO_ROOT).as_posix()
               for q in (stage1_original, stage2_original) if not q.exists()]
    if missing:
        # No validation target for this generator. That is FIRST RUN, and it is
        # NOT a pass: nothing was compared, so nothing is known to reproduce.
        # Announce it, because a silent skip here would defeat the entire point
        # of validating before extending.
        print(f"  *** FIRST RUN -- no validation target for model {args.model!r}")
        for m in missing:
            print(f"  *** missing: {m}")
        print(f"  *** stage1 {len(s1)} rows and stage2 {len(s2)} rows were rebuilt "
              f"but NOT VALIDATED AGAINST ANYTHING.")
        print(f"  *** Nothing here reproduces a reference, because there is no "
              f"reference for this model.")
    else:
        p1 = diff_against(s1, stage1_original,
                          {"anchor_coverage_at_5", "mean_reciprocal_rank_at_5"})
        print(f"  {STAGE1_ORIGINAL_NAME}  : {len(s1)} rows rebuilt, "
              f"{'PASS -- exact reproduction' if not p1 else f'FAIL -- {len(p1)} difference(s)'}")
        for problem in p1[:10]:
            print(f"      {problem}")

        p2 = diff_against(s2, stage2_original, {"coverage_at_5", "bertscore_cosine"})
        print(f"  {STAGE2_ORIGINAL_NAME}: {len(s2)} rows rebuilt, "
              f"{'PASS -- exact reproduction' if not p2 else f'FAIL -- {len(p2)} difference(s)'}")
        for problem in p2[:10]:
            print(f"      {problem}")

        if p1 or p2:
            print("\nSTOPPING: a rebuilt table does not reproduce its committed original. "
                  "Not writing anything, and not adjusting the generator to force a match.")
            return 1

    if not args.write:
        print("\nBoth reproduce exactly. Re-run with --write to emit the extended versions."
              if not missing else
              "\nFIRST RUN -- nothing validated. Re-run with --write to emit the versions.")
        return 0

    all_conditions = persisted_conditions()
    print(f"\nEXTENDED OUTPUT -- {len(all_conditions)} persisted Stage 1 condition(s)\n")

    ensure_analysis_dir(args.model)
    s1_all = build_stage1(all_conditions, with_representation=True)
    write_csv(s1_all, stage1_rebuilt)
    print(f"  {stage1_rebuilt.relative_to(REPO_ROOT)}")
    print(f"      {len(s1_all)} rows (was {len(s1)}), columns: {list(s1_all[0].keys())}")

    s2_all = build_stage2(with_representation=True, model=args.model,
                          conditions=TEXT_ONLY_CONDITIONS)
    write_csv(s2_all, stage2_rebuilt)
    covered = sorted({r["condition_id"] for r in s2_all})
    print(f"  {stage2_rebuilt.relative_to(REPO_ROOT)}")
    print(f"      {len(s2_all)} rows (was {len(s2)}), columns: {list(s2_all[0].keys())}")
    print(f"      covers {len(covered)} condition(s) -- generation exists for the text_only "
          f"arm only, so this CANNOT extend to 12 until the enriched arm is generated.")

    print("\nOriginals left untouched as the historical 6-condition record:")
    print(f"  {stage1_original.relative_to(REPO_ROOT)}")
    print(f"  {stage2_original.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
