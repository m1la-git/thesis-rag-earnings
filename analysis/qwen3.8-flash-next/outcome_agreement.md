> **No validation surface.** This script has no expectation set, under any model, and is deliberately not part of `scripts/validate_all.py` -- there is no pinned figure for it to reproduce and no reference document to diff against. Every figure below is computed and unchecked. This is a property of the script, not a first-run state.

# Cross-arm outcome-label agreement

Baseline: `qwen3.8-27b@q8_k_xl`. Comparison: `qwen3.8-flash-next`.

Sources: `results/tables/qwen3.8-27b_q8_k_xl/generation_outcomes.csv`
and `results/tables/qwen3.8-flash-next/generation_outcomes.csv`.

This is a **diff of two published tables**. Outcome labels are read exactly as the scoring pass wrote them; nothing here re-scores, re-derives a case, or re-checks grounding. Holding the instrument fixed is what makes the comparison a statement about the two generators rather than about two runs of the scorer.

## 1. Overall agreement

| quantity | n |
|---|--:|
| shared (condition, question) keys | 540 |
| **agree** | **498 (92.2%)** |
| disagree | 42 (7.8%) |

Both arms cover the same grid exactly -- no key is present in one table and absent from the other, so nothing is excluded from the comparison.

The `case` column is identical on all 540 shared keys, as it must be: cases are computed from Stage 1 retrieval, which no generator touches. A mismatch would mean the two tables were built against different retrieval output, and this script stops rather than reporting one.

## 2. Transition matrix

Rows are `qwen3.8-27b@q8_k_xl` (baseline); columns are `qwen3.8-flash-next`. The diagonal is agreement.

| baseline \ comparison | abstained | correct | offtarget | ungrounded | total |
|---|--:|--:|--:|--:|--:|
| abstained | **270** | 9 | 5 | 1 | 285 |
| correct | 2 | **129** | 2 | 1 | 134 |
| offtarget | 9 | 1 | **98** | 4 | 112 |
| ungrounded | 5 | 0 | 3 | **1** | 9 |
| **total** | 286 | 139 | 108 | 7 | 540 |

Off-diagonal cells, largest first:

| baseline label | comparison label | n |
|---|---|--:|
| abstained | correct | 9 |
| offtarget | abstained | 9 |
| abstained | offtarget | 5 |
| ungrounded | abstained | 5 |
| offtarget | ungrounded | 4 |
| ungrounded | offtarget | 3 |
| correct | abstained | 2 |
| correct | offtarget | 2 |
| abstained | ungrounded | 1 |
| correct | ungrounded | 1 |
| offtarget | correct | 1 |

## 3. Disagreements by question category

| category | disagreements | shared keys | rate |
|---|--:|--:|--:|
| factual | 1 | 168 | 0.6% |
| thematic | 24 | 180 | 13.3% |
| comparative | 12 | 132 | 9.1% |
| unanswerable | 5 | 60 | 8.3% |
| **all** | **42** | **540** | **7.8%** |

## 4. Disagreements by case

| case | disagreements | shared keys | rate |
|---|--:|--:|--:|
| A | 5 | 60 | 8.3% |
| B | 27 | 333 | 8.1% |
| C | 10 | 147 | 6.8% |
| **all** | **42** | **540** | **7.8%** |

## 5. What the disagreement count may and may not be read as

**The 5 unanswerable disagreements are predetermined and carry no information.** `qwen3.8-flash-next` does not name companies. P1 (company misattribution) is structurally impossible for it, so these disagreements -- all attributable to a single question (`ref_unans_01`) -- follow from that difference rather than from anything about how the two arms handle unanswerable questions. They are not evidence about unanswerable handling, and a sentence reading them as such would be describing an artifact of the comparison's construction.

**Of the 42 disagreements, only the 37 outside that slice are informative** (7.7% of the shared answerable keys). Quote that figure, not the raw total, wherever the disagreement count is being read as a difference between the generators.

The corresponding agreement figure restricted to answerable items is 443/480.

This document reports agreement only. It makes no claim about which arm is more faithful: an outcome label is a mechanical verdict, and two arms differing on one says they were labelled differently, not that either was read.
