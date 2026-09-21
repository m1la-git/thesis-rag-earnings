> **No validation surface.** This script has no expectation set and validates nothing, under any model -- there is no pinned figure for it to reproduce and no reference document to diff against. Every figure below is computed and unchecked. This is a permanent property of this script, not a first-run state, and pinning a model does not change it.

# Case C conversion by anchor coverage: conjunctive vs disjunctive questions

Model: `qwen3.8-27b@q8_k_xl`. Population: every Case C observation across all 12 conditions (**n=147**).

## How Case C is determined — verified, not assumed

`evaluate.classify_case` returns Case C for coverage 0.5 and 1.0, Case B for 0.0 -- Case C is the **ANY-anchor** condition, asserted at run time.

`evaluate.anchor_coverage_at_5` returns `matched / len(gold_anchors)`, and
`evaluate.classify_case` is `CASE_B if coverage_at_5 == 0 else CASE_C`. So a
**comparative item holding 1 of 2 anchors is Case C** while being unanswerable from
what was actually retrieved: a comparison cannot be made from one side. An abstention
there is arguably correct behaviour scored as a conversion failure.

## Coverage groups

| group | definition |
|---|---|
| single | the question has exactly 1 gold anchor — full by definition, reported separately |
| full | >= 2 anchors, all matched within top-5 (coverage = 1.0) |
| partial | >= 2 anchors, some but not all matched (0 < coverage < 1.0) |

Cells with n < 5 are flagged ⚠.

## Anchor structure of the benchmark

| category | questions | anchors per question |
|---|--:|---|
| factual | 14 | 1 anchor: 14 q |
| thematic | 15 | 2 anchors: 7 q, 3 anchors: 8 q |
| comparative | 11 | 2 anchors: 11 q |

## Conversion rate by coverage group, per category, per arm

Cell = conversion rate (correct / n).

| category | arm | single (1 anchor) | full (>=2 anchors, all matched) | partial (some but not all) |
|---|---|---|---|---|
| factual | text_only | 100% (15/15) | — | — |
| factual | enriched | 98% (54/55) | — | — |
| thematic | text_only | — | — | 100% (13/13) |
| thematic | enriched | — | — | 88% (14/16) |
| comparative | text_only | — | — | 17% (3/18) |
| comparative | enriched | — | 100% (2/2) ⚠ | 29% (8/28) |

Both arms pooled (the coverage effect is not about representation):

| category | single (1 anchor) | full (>=2 anchors, all matched) | partial (some but not all) |
|---|---|---|---|
| factual | 99% (69/70) | — | — |
| thematic | — | — | 93% (27/29) |
| comparative | — | 100% (2/2) ⚠ | 24% (11/46) |

## The key contrast: coverage sensitivity, thematic vs comparative

Both have >= 2 anchors, so both have a meaningful full/partial split. Thematic is
disjunctive (any subset supports an answer); comparative is conjunctive (both sides
needed).

| category | full | partial | difference (full − partial) |
|---|---|---|---|
| thematic | — | 93% (27/29) | n/a |
| comparative | 100% (2/2) ⚠ | 24% (11/46) | +76% |

## Comparative partial-coverage items — outcome breakdown

These are the items the hypothesis says may be unanswerable-by-construction: a
comparison with only one side retrieved. Does the model abstain (arguably correct) or
answer off-target?

| arm | n | abstained | correct | offtarget | ungrounded |
|---|--:|--:|--:|--:|--:|
| text_only | 18 | 15 | 3 | 0 | 0 |
| enriched | 28 | 18 | 8 | 1 | 1 |
| both pooled | 46 | 33 | 11 | 1 | 1 |

For contrast, the same breakdown for **thematic** partial-coverage items:

| arm | n | abstained | correct | offtarget | ungrounded |
|---|--:|--:|--:|--:|--:|
| text_only | 13 | 0 | 13 | 0 | 0 |
| enriched | 16 | 1 | 14 | 1 | 0 |
| both pooled | 29 | 1 | 27 | 1 | 0 |

## Distractor displacement in comparative Case C top-5s

Mean number of the five retrieved chunks belonging to **neither named company**, over
every comparative Case C observation. If enrichment clears off-company chunks out of
the context window, this falls.

Two granularities, because they answer different questions. **Company-level** counts a
chunk as a distractor only if its ticker is neither of the two the question names — a
chunk from the right bank's wrong quarter is not a distractor. **Transcript-level**
counts anything outside the question's own `transcript_ids`, so the right bank's wrong
quarter does count; that is stricter and closer to what a quarter-specific comparison
actually needs.

| granularity | arm | n | mean of 5 | median |
|---|---|--:|--:|--:|
| company-level | text_only | 18 | 0.72 | 0 |
| company-level | enriched | 30 | 0.30 | 0 |
| transcript-level | text_only | 18 | 3.78 | 4 |
| transcript-level | enriched | 30 | 2.60 | 3 |

Difference (enriched − text_only): **-0.42** chunks company-level, **-1.18** chunks transcript-level.

**Read the company-level figure cautiously.** The median is 0 in both arms, so most
comparative Case C observations already had no off-company chunk under `text_only`;
the 0.42-chunk mean difference comes from a minority of observations and is
small in absolute terms. The transcript-level figure is the larger movement
(1.18 of 5 slots), and is the one that would carry a distractor-displacement
claim if one is made. Neither is a significance test.
