> **No validation surface.** This script has no expectation set, under any model, and is deliberately not part of `scripts/validate_all.py` -- there is no pinned figure for it to reproduce and no reference document to diff against. Every figure below is computed and unchecked. This is a property of the script, not a first-run state.

# Cross-arm outcome-label agreement

Baseline: `qwen3.8-27b@q4_k_xl`. Comparison: `qwen3.8-27b@q8_k_xl`.

Sources: `results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv`
and `results/tables/qwen3.8-27b_q8_k_xl/generation_outcomes.csv`.

This is a **diff of two published tables**. Outcome labels are read exactly as the scoring pass wrote them; nothing here re-scores, re-derives a case, or re-checks grounding. Holding the instrument fixed is what makes the comparison a statement about the two generators rather than about two runs of the scorer.

## 1. Overall agreement

| quantity | n |
|---|--:|
| shared (condition, question) keys | 540 |
| **agree** | **525 (97.2%)** |
| disagree | 15 (2.8%) |

Both arms cover the same grid exactly -- no key is present in one table and absent from the other, so nothing is excluded from the comparison.

The `case` column is identical on all 540 shared keys, as it must be: cases are computed from Stage 1 retrieval, which no generator touches. A mismatch would mean the two tables were built against different retrieval output, and this script stops rather than reporting one.

## 2. Transition matrix

Rows are `qwen3.8-27b@q4_k_xl` (baseline); columns are `qwen3.8-27b@q8_k_xl`. The diagonal is agreement.

| baseline \ comparison | abstained | correct | offtarget | ungrounded | total |
|---|--:|--:|--:|--:|--:|
| abstained | **283** | 1 | 1 | 0 | 285 |
| correct | 1 | **128** | 1 | 0 | 130 |
| offtarget | 0 | 3 | **108** | 3 | 114 |
| ungrounded | 1 | 2 | 2 | **6** | 11 |
| **total** | 285 | 134 | 112 | 9 | 540 |

Off-diagonal cells, largest first:

| baseline label | comparison label | n |
|---|---|--:|
| offtarget | correct | 3 |
| offtarget | ungrounded | 3 |
| ungrounded | correct | 2 |
| ungrounded | offtarget | 2 |
| abstained | correct | 1 |
| abstained | offtarget | 1 |
| correct | abstained | 1 |
| correct | offtarget | 1 |
| ungrounded | abstained | 1 |

## 3. Disagreements by question category

| category | disagreements | shared keys | rate |
|---|--:|--:|--:|
| factual | 0 | 168 | 0.0% |
| thematic | 11 | 180 | 6.1% |
| comparative | 4 | 132 | 3.0% |
| unanswerable | 0 | 60 | 0.0% |
| **all** | **15** | **540** | **2.8%** |

## 4. Disagreements by case

| case | disagreements | shared keys | rate |
|---|--:|--:|--:|
| A | 0 | 60 | 0.0% |
| B | 9 | 333 | 2.7% |
| C | 6 | 147 | 4.1% |
| **all** | **15** | **540** | **2.8%** |

## 5. What the disagreement count may and may not be read as

No unanswerable item disagrees between the two arms, so there is no slice to discount and the full disagreement count is informative.

This document reports agreement only. It makes no claim about which arm is more faithful: an outcome label is a mechanical verdict, and two arms differing on one says they were labelled differently, not that either was read.
