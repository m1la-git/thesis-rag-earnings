"""Run every validator in sequence and report one pass/fail table.

Purpose
-------
A regression check on the analysis logic, meant to be run immediately BEFORE and
immediately AFTER any work that could disturb it -- a generator swap, a scorer
change, a refactor. Before/after runs that both come back green are the evidence
that the work disturbed nothing.

It covers BOTH arms, for different reasons. q4 is the regression baseline: its
figures are frozen development history, so any drift in them is drift in the
code. q8 is the REPORTED arm: its figures are what the thesis cites, so they
have to be checked too. Neither substitutes for the other.

It exists because the alternative is a checklist, and a checklist eventually
gets skipped.

THE q4 JOBS STAY PINNED TO q4. DO NOT REPOINT THEM.
--------------------------------------------------
Every figure asserted by a `[q4]` job is a published q4 number, and it must keep
asserting those no matter which generator is being worked on. They are a
regression check on the analysis logic, not a report of the thesis's results.
Repointing them at q8 would delete the only baseline that can detect drift.

q8 jobs were ADDED alongside them (2026-09-06), not substituted for them. A job
runs under q8 only where a real validation target exists for that arm:

- ADDED under q8: rebuild_statistics, check3_enriched, stage2_statistics_12cond,
  matched_conversion, coverage_split.
- NOT added: rebuild_long_tables, because the q8 arm has no
  stage2_outcomes_long.csv reference table -- under q8 it prints FIRST RUN,
  which is not a pass and must never be reported as one. Give it a target and
  it can be added.
- CANNOT be added: check3_attribution_postfix and fix_attribution are q4-only by
  nature -- they compare against the frozen pre-fix table, which has no
  counterpart under any other generator, and they refuse a non-q4 --model. See
  README.md, "Generator runs".
- Model-independent, so run once: verify_invariant5 (retrieval/index only) and
  the unit tests.

"FIRST RUN" is in FAILURE_MARKERS for exactly this reason: if a job is ever
added for an arm that has no validation target, it fails loudly instead of
printing a green PASS for a check that did not happen.

One caveat on what a q8 PASS proves
-----------------------------------
`stage2_statistics_12cond [q8]` validates against a document that was written
FROM that script's own output, so its PASS is a REGRESSION PIN -- it catches
drift, it is not two independent sources agreeing. The q4 equivalent was
hand-authored before the script existed and its PASS is a real reproduction. The
q8 document says so in its own first line. Do not report the two as equivalent.

What it covers
--------------
  [q4] rebuild_long_tables            240 + 270 rows reproduce field for field
  [q4] rebuild_statistics             Part 6.1-6.2 and A2 reproduce cell by cell
  [q4] check3_attribution_postfix     pre (7/26, 39/42) AND post (9/30, 55/58)
  [q4] check3_enriched                text_only 9/30 AND all 11 enriched figures
  [q4] stage2_statistics_12cond       A2 size, A2 strategy, A1 Case B
  [q4] fix_attribution --decompose    19 departures, 17/1/1, Fix 2 = ref_fact_05
  [q4] coverage_split                 Case C is the ANY-anchor condition
  [q4] matched_conversion             partition reconciles; b=0; both McNemars
  [q8] rebuild_statistics             shared Stage 1 + the q8 A2 chunk-size table
  [q8] check3_enriched                q8 pinned text_only and enriched figures
  [q8] stage2_statistics_12cond       q8 A2 size, A2 strategy, A1 Case B (a pin)
  [q8] coverage_split                 Case C is the ANY-anchor condition
  [q8] matched_conversion             q8 partition, b/c membership, both McNemars
  verify_invariant5                   text_only retrieval byte-identical to git

`check3_attribution_postfix` and `check3_enriched` are run WITHOUT `--validate`
deliberately: `--validate` checks only the frozen pre-fix / text_only side, and
the side that can actually drift is asserted in the full run.

The unit tests are NOT included here, on purpose
------------------------------------------------
`python -m unittest` covers the frozen contracts of the pipeline -- metric
definitions, the case/outcome taxonomy, the indexing-representation isolation --
and is fast, hermetic, and has no dependency on any results file. This suite
covers published FIGURES and reads persisted artifacts. Keeping them separate
means a failure tells you immediately which kind of thing broke: a contract or a
number. `--with-tests` runs both when you want a single command.

`--fast` skips verify_invariant5 and nothing else
-------------------------------------------------
verify_invariant5 is roughly 90% of the suite's runtime and is the ONLY job that
touches the retrieval/index layer -- every other job reads persisted scored
tables. When the work being checked was confined to analysis/ (prose, label keys,
path scoping), it cannot have moved retrieval, and the full run is being paid for
nothing.

The rule: `--fast` for iteration, the FULL run for the before/after pair that is
the actual evidence. The full run stays the default; `--fast` is opt-in, prints a
loud warning naming what it skipped, and reports the job as SKIPPED rather than
PASS so a skipped check can never be read as a passing one.

Usage
-----
    python scripts/validate_all.py
    python scripts/validate_all.py --with-tests
    python scripts/validate_all.py --fast --with-tests
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The one job --fast skips. Named here rather than matched by string in main()
# so the flag can never silently start skipping a different or an extra job.
INVARIANT5_LABEL = "verify_invariant5 (byte-identity vs git)"

Q8 = "qwen3.8-27b@q8_k_xl"

# (label, argv). Anything non-zero, or an exception, is a failure.
# The q4 jobs pass no --model: they run under DEFAULT_MODEL and their assertions
# are the frozen baseline. The q8 jobs pass it explicitly.
VALIDATORS: list[tuple[str, list[str]]] = [
    # --- q4: the regression baseline -------------------------------------
    ("[q4] rebuild_long_tables --validate",
     ["analysis/rebuild_long_tables.py", "--validate"]),
    ("[q4] rebuild_statistics --validate",
     ["analysis/rebuild_statistics.py", "--validate"]),
    ("[q4] check3_attribution_postfix (pre + post)",
     ["analysis/check3_attribution_postfix.py"]),
    ("[q4] check3_enriched (text_only + enriched)",
     ["analysis/check3_enriched.py"]),
    ("[q4] stage2_statistics_12cond --validate",
     ["analysis/stage2_statistics_12cond.py", "--validate"]),
    ("[q4] fix_attribution --decompose",
     ["analysis/fix_attribution.py", "--decompose"]),
    ("[q4] coverage_split (Case C = ANY-anchor)",
     ["analysis/coverage_split.py"]),
    ("[q4] matched_conversion (partition, b/c, McNemar)",
     ["analysis/matched_conversion.py"]),
    # --- q8: the reported arm --------------------------------------------
    # rebuild_long_tables is absent on purpose: no q8 reference long table, so
    # it would print FIRST RUN. See the docstring.
    ("[q8] rebuild_statistics --validate",
     ["analysis/rebuild_statistics.py", "--validate", "--model", Q8]),
    ("[q8] check3_enriched (text_only + enriched)",
     ["analysis/check3_enriched.py", "--model", Q8]),
    ("[q8] stage2_statistics_12cond --validate (pin)",
     ["analysis/stage2_statistics_12cond.py", "--validate", "--model", Q8]),
    ("[q8] coverage_split (Case C = ANY-anchor)",
     ["analysis/coverage_split.py", "--model", Q8]),
    ("[q8] matched_conversion (partition, b/c, McNemar)",
     ["analysis/matched_conversion.py", "--model", Q8]),
    # --- generator-independent -------------------------------------------
    (INVARIANT5_LABEL,
     ["analysis/verify_invariant5.py"]),
]

TESTS = ["-m", "unittest", "tests.test_evaluate", "tests.test_run_experiment",
         "tests.test_index_representation"]

# Some scripts report a failure in prose and still exit 0, so the exit code
# alone is not sufficient. Any of these in the output is treated as a failure.
# "FIRST RUN" is here so a job added for an arm with no validation target fails
# loudly instead of printing PASS for a check that never happened. No job in the
# table above prints it today; if one starts to, that is the bug it catches.
FAILURE_MARKERS = ("MISMATCH", "REFUSING TO WRITE", "STOPPING", "Traceback",
                   "PARTITION DOES NOT RECONCILE", "FAIL:", "FIRST RUN")


def run(label: str, argv: list[str]) -> tuple[bool, float, str]:
    started = time.monotonic()
    proc = subprocess.run(
        [sys.executable, *argv],
        cwd=REPO_ROOT, capture_output=True, text=True,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    ok = proc.returncode == 0 and not any(m in out for m in FAILURE_MARKERS)
    return ok, time.monotonic() - started, out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-tests", action="store_true",
                        help="also run the unit-test suite (see the docstring for why "
                             "it is separate by default)")
    parser.add_argument("--fast", action="store_true",
                        help="skip verify_invariant5 (~90%% of the runtime) and nothing "
                             "else. Iteration only -- the full run is what counts as "
                             "evidence. See the docstring.")
    parser.add_argument("--verbose", action="store_true",
                        help="print each validator's full output")
    args = parser.parse_args()

    jobs = list(VALIDATORS)
    skipped: list[str] = []
    if args.fast:
        jobs = [j for j in jobs if j[0] != INVARIANT5_LABEL]
        skipped.append(INVARIANT5_LABEL)
    if args.with_tests:
        jobs.append(("unit tests (122)", TESTS))

    if skipped:
        print("=" * 78)
        print("  --fast: SKIPPING verify_invariant5. THIS IS NOT A FULL VALIDATION.")
        print("=" * 78)
        print("  verify_invariant5 is the ONLY end-to-end byte-identity check against git")
        print("  for the retrieval/index layer. Every other job in this suite reads a")
        print("  persisted scored table and cannot see that layer at all. With it skipped,")
        print("  a change to the chunker, the embedding model, or index.build_index_text")
        print("  WOULD PASS UNNOTICED.")
        print()
        if args.with_tests:
            print("  --with-tests still runs tests/test_index_representation.py, which catches")
            print("  a CONTRACT break (e.g. build_index_text(chunk, 'text_only') no longer")
            print("  returning chunk['text']) -- but NOT an end-to-end byte-identity break.")
        else:
            print("  Without --with-tests, nothing here checks the index layer in any form.")
            print("  tests/test_index_representation.py would at least catch a contract break.")
        print()
        print("  THE RULE: --fast for iteration. The FULL run is the before/after pair that")
        print("  is the actual evidence. Do not report a --fast run as a clean suite.")
        print("=" * 78)
        print()

    print(f"Validator suite -- {len(jobs)} job(s). Assertions are pinned to the "
          f"published q4 figures.\n")
    results = []
    for label, argv in jobs:
        print(f"  running {label} ...", flush=True)
        ok, secs, out = run(label, argv)
        results.append((label, ok, secs, out))
        if args.verbose or not ok:
            print("    " + "\n    ".join(out.strip().splitlines()[-25:]))

    width = max(len(label) for label, *_ in [*results, *((s, None, None, None) for s in skipped)])
    print("\n" + "=" * (width + 20))
    for label, ok, secs, _ in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<{width}}  {secs:6.1f}s")
    for label in skipped:
        # Deliberately NOT 'PASS': nothing ran, so nothing passed.
        print(f"  SKIP  {label:<{width}}       -   (--fast)")
    print("=" * (width + 20))

    failed = [label for label, ok, *_ in results if not ok]
    if failed:
        print(f"\n{len(failed)} of {len(results)} FAILED: {failed}")
        print("A failure here means a published q4 figure has moved, or the logic "
              "behind one has.\nTreat it as a finding: establish what changed before "
              "updating any expected value.")
        return 1
    tail = f" ({len(skipped)} SKIPPED)" if skipped else ""
    print(f"\nall {len(results)} passed{tail}")
    if skipped:
        print("NOT a full validation -- verify_invariant5 was skipped. See the warning above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
