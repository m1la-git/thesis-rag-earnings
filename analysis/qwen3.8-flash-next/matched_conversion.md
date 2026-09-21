> **FIRST RUN -- nothing was validated against.** No expectation set existed for model `qwen3.8-flash-next` when this was written, so every figure below is COMPUTED AND UNCHECKED. Pin the model deliberately before citing any of it.

# Matched-subset Case C conversion

Model: `qwen3.8-flash-next`. Source: `results/tables/qwen3.8-flash-next/generation_outcomes.csv`.

Case C membership depends on whether the gold anchor reached the top-5, so the
enriched and text_only Case C sets are different populations. Every enriched
condition is compared against its matched text_only counterpart (same chunk size,
same strategy), per question.

**The generator never sees the enrichment.** `generate.format_context` renders
`chunk["text"]` only, `run_generation.build_items` puts only `{chunk_id, text}` into
`top5_chunks`, and `src/generate.py` is byte-identical to its committed version --
verified, not assumed. What enrichment changes is *which five chunks* occupy the
context window, not how any one of them is rendered.

## 1. Partition sizes

| set | n |
|---|--:|
| intersection (Case C in both arms) | **38** |
| newly entered (enriched only) | **63** |
| lost (text_only only) | **8** |

Reconciliation: intersection + lost = 38 + 8 = **46** (text_only Case C total 46); intersection + newly = 38 + 63 = **101** (enriched Case C total 101). Both check.

Per matched pair:

| matched pair | intersection | newly entered | lost | text_only C | enriched C |
|---|--:|--:|--:|--:|--:|
| chunk200_dense | 4 | 17 | 1 | 5 | 21 |
| chunk200_bm25 | 6 | 6 | 1 | 7 | 12 |
| chunk200_hybrid | 8 | 12 | 1 | 9 | 20 |
| chunk500_dense | 8 | 11 | 0 | 8 | 19 |
| chunk500_bm25 | 5 | 5 | 3 | 8 | 10 |
| chunk500_hybrid | 7 | 12 | 2 | 9 | 19 |

## 2. Conversion on the intersection — the like-for-like comparison

Same 38 (condition, question) items in both arms; only the representation differs.

| arm | n | correct | abstained | offtarget | ungrounded | **rate** |
|---|--:|--:|--:|--:|--:|--:|
| text_only | 38 | 23 | 15 | 0 | 0 | **60.5%** |
| enriched | 38 | 33 | 5 | 0 | 0 | **86.8%** |

## 3. Conversion on the newly-entered set

The 63 items that are Case C only under enrichment (no text_only counterpart,
so a single-arm figure by construction).

| set | n | correct | abstained | offtarget | ungrounded | rate |
|---|--:|--:|--:|--:|--:|--:|
| newly entered (enriched) | 63 | 50 | 12 | 1 | 0 | **79.4%** |
| lost (text_only) | 8 | 7 | 1 | 0 | 0 | 87.5% |

## 4. Category composition

| category | intersection | newly entered | lost |
|---|--:|--:|--:|
| factual | 14 (37%) | 41 (65%) | 1 (12% of 8) |
| thematic | 9 (24%) | 7 (11%) | 4 (50% of 8) |
| comparative | 15 (39%) | 15 (24%) | 3 (38% of 8) |

Per-category conversion rate, intersection (both arms) vs newly entered:

| category | intersection text_only | intersection enriched | newly entered |
|---|--:|--:|--:|
| factual | 100.0% (n=14) | 100.0% (n=14) | 100.0% (n=41) |
| thematic | 100.0% (n=9) | 88.9% (n=9) | 85.7% (n=7) |
| comparative | 0.0% (n=15) | 73.3% (n=15) | 20.0% (n=15) |

## 5. Is the conversion difference statistically supported?

> **Specified after the descriptive result was seen.** These tests were added once
> the section 2 conversion figures had been observed, to formalise an already-visible
> pattern. They are **not pre-registered comparisons**; read them as descriptive of
> this sample rather than confirmatory. Recorded so the artifact states the order of
> operations.

### 5.0 The independence problem, stated first

The 38 intersection observations come from only **13 distinct questions** -- the same question contributes one observation per condition pair where
it is Case C in both arms. Those observations are correlated: a question that converts
well under enrichment tends to do so in every condition.

| condition pairs contributed | questions |
|---|--:|
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |
| 4 | 2 |
| 5 | 2 |

| category | observations | distinct questions |
|---|--:|--:|
| factual | 14 | 6 |
| thematic | 9 | 3 |
| comparative | 15 | 4 |

**The 12 discordant observations come from only 4 distinct questions:**

| question | category | discordant in | of its intersection pairs | winner | condition pairs |
|---|---|--:|--:|---|---|
| `ref_comp_06` | comparative | 5 | 5 | enriched | chunk200_bm25, chunk200_hybrid, chunk500_dense, chunk500_bm25, chunk500_hybrid |
| `ref_comp_08` | comparative | 4 | 5 | enriched | chunk200_dense, chunk200_bm25, chunk200_hybrid, chunk500_hybrid |
| `ref_comp_11` | comparative | 2 | 2 | enriched | chunk200_hybrid, chunk500_dense |
| `ref_them_02` | thematic | 1 | 4 | text_only | chunk500_dense |

### 5.1 Observation-level test -- **ANTI-CONSERVATIVE, do not quote alone**

Each (question, chunk size, strategy) item is one trial. **The observations are not
independent** (see 5.0), so the exact binomial treats correlated observations as
independent trials and the p-values below are too small, possibly severely so.
Retained for transparency, not as the headline.

**Test: exact McNemar** -- `binomtest(max(b, c), b + c, 0.5)`, two-sided. Not the
chi-square approximation; discordant counts are single-digit.

| population | pairs | b (text_only only) | c (enriched only) | concordant | n disc | p (exact) |
|---|--:|--:|--:|--:|--:|--:|
| pooled | 38 | 1 | 11 | 26 | 12 | 0.0063 |
| factual | 14 | 0 | 0 | 14 | 0 | n/a (no discordant pairs) |
| thematic | 9 | 1 | 0 | 8 | 1 | 1.0000 |
| comparative | 15 | 0 | 11 | 4 | 11 | 0.0010 |

### 5.2 Question-level test -- **the conservative version, quote this one**

Each question contributes exactly one observation. **Tie-breaking rule:** a question is
an enriched win if it is correct-under-enriched-and-not-text_only in a strict majority
of the condition pairs where it appears in the intersection; a text_only win in the
reverse case; concordant otherwise -- which includes exact ties and questions discordant
in only a minority of their pairs. The denominator is all of the question's intersection
pairs, not only its discordant ones. Applied identically to every row.

| population | questions | b (text_only only) | c (enriched only) | concordant | n disc | p (exact) |
|---|--:|--:|--:|--:|--:|--:|
| pooled | 13 | 0 | 3 | 10 | 3 | 0.2500 |
| factual | 6 | 0 | 0 | 6 | 0 | n/a (no discordant questions) |
| thematic | 3 | 0 | 0 | 3 | 0 | n/a (no discordant questions) |
| comparative | 4 | 0 | 3 | 1 | 3 | 0.2500 |

**Sensitivity check** -- the same test with the majority taken over each question's
DISCORDANT pairs only, so a question discordant in 1 of 4 pairs counts as a win rather
than concordant. This is the more permissive rule; reported because it changes n.

| population | questions | b | c | concordant | n disc | p (exact) |
|---|--:|--:|--:|--:|--:|--:|
| pooled | 13 | 1 | 3 | 9 | 4 | 0.6250 |
| factual | 6 | 0 | 0 | 6 | 0 | n/a |
| thematic | 3 | 1 | 0 | 2 | 1 | 1.0000 |
| comparative | 4 | 0 | 3 | 1 | 3 | 0.2500 |

### 5.3 What the two tests jointly support

The observation-level test gives p=0.0063 pooled; the question-level test gives
p=0.2500. **The question-level test does not reach significance at any conventional
threshold, and it is the one to quote.** The observation-level result is an artifact of
counting correlated observations as independent trials. **There is no statistically
supported claim here that enrichment improves Case C conversion on comparable items** --
3 discordant questions cannot support one.

**What does stand, independent of any test, as a descriptive fact:**

> **b = 0 at the question level -- and ONLY there.** Across all 13 distinct questions, in every category, **not one was correct under `text_only` and incorrect under `metadata_enriched`.** At observation level that claim is FALSE and must not be stated: 1 of 38 matched observations, from 1 distinct question (ref_them_02), converted under `text_only` but not under `metadata_enriched` -- each a minority within its own question, which is why each falls to `concordant` under the `all_pairs` tie-breaking rule in 5.2. Quote this scoped to the question level; an unscoped "b = 0 everywhere" contradicts 5.1 above. The scoped claim is a property of the observed data, not an inference from a test, and it does not depend on the independence assumption that makes 5.1 unsafe.

No multiple-comparison correction is applied within either table: each is one pooled
test plus three category partitions of the same data, not independent families.
