> **No validation surface.** This script has no expectation set and validates nothing, under any model -- there is no pinned figure for it to reproduce and no reference document to diff against. Every figure below is computed and unchecked. This is a permanent property of this script, not a first-run state, and pinning a model does not change it.

# Abstention-rescoring for conjunctive questions — SECONDARY VIEW

> ## The primary taxonomy is unchanged.
>
> `src/evaluate.py`, the four-way outcome taxonomy, every threshold and every table
> under `results/` are **untouched**. This document reports an ALTERNATIVE VIEW
> alongside the primary figures, never in place of them.
>
> It exists to **bound the effect of a known case-definition limitation**, not to
> improve any number. The primary conversion rate remains the reported one; this is
> the sensitivity analysis that says how much of it is attributable to that
> limitation.

Model: `qwen3.8-27b@q4_k_xl`. Population: every Case C observation across all 12 conditions (**n=147**).

## The limitation

Case C is `coverage_at_5 > 0` — **any** gold anchor retrieved, not all. A comparative
question names two companies and carries one anchor per company, and both are needed:
a comparison cannot be made from one side. So a comparative item holding 1 of 2
anchors is Case C while being unanswerable from what was retrieved, and an abstention
there is arguably correct behaviour that the primary taxonomy scores as a failure.

`coverage_split.md` for the same model measures the size of it: it reports the
abstention rate on comparative partial-coverage items against the rate on thematic
partial-coverage items at the same coverage status. Read the figures there rather
than here -- this document does not recompute them.

## The alternative rule, and why its scope is narrow

`abstained` counts as correct **only for comparative questions at partial anchor
coverage**. Not extended to:

| excluded | why |
|---|---|
| thematic partial | disjunctive — any subset of anchors supports a valid answer, so an abstention is a real failure to use what was retrieved |
| single-anchor factual | no partial state exists; one anchor is all-or-nothing |
| comparative **full** coverage | both sides retrieved, the comparison is answerable, so an abstention is a real failure |
| Case B | the taxonomy already treats abstention as correct there; those abstentions are not conversion failures to begin with |

## 1. Case C conversion — primary vs alternative

| scope | arm | primary | alternative | delta |
|---|---|---|---|--:|
| pooled | text_only | 65.2% (30/46) | 97.8% (45/46) | +32.6pp |
| pooled | enriched | 78.2% (79/101) | 95.0% (96/101) | +16.8pp |
| pooled | both arms | 74.1% (109/147) | 95.9% (141/147) | +21.8pp |
| factual | text_only | 100.0% (15/15) | 100.0% (15/15) | — |
| factual | enriched | 98.2% (54/55) | 98.2% (54/55) | — |
| factual | both arms | 98.6% (69/70) | 98.6% (69/70) | — |
| thematic | text_only | 92.3% (12/13) | 92.3% (12/13) | — |
| thematic | enriched | 93.8% (15/16) | 93.8% (15/16) | — |
| thematic | both arms | 93.1% (27/29) | 93.1% (27/29) | — |
| comparative | text_only | 16.7% (3/18) | 100.0% (18/18) | +83.3pp |
| comparative | enriched | 33.3% (10/30) | 90.0% (27/30) | +56.7pp |
| comparative | both arms | 27.1% (13/48) | 93.8% (45/48) | +66.7pp |

## 2. The 38-item matched intersection

Case C in both arms, the like-for-like population from
`analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md`.

| scope | arm | primary | alternative | delta |
|---|---|---|---|--:|
| pooled | text_only | 60.5% (23/38) | 97.4% (37/38) | +36.8pp |
| pooled | enriched | 78.9% (30/38) | 97.4% (37/38) | +18.4pp |
| pooled | both arms | 69.7% (53/76) | 97.4% (74/76) | +27.6pp |
| factual | text_only | 100.0% (14/14) | 100.0% (14/14) | — |
| factual | enriched | 100.0% (14/14) | 100.0% (14/14) | — |
| thematic | text_only | 88.9% (8/9) | 88.9% (8/9) | — |
| thematic | enriched | 100.0% (9/9) | 100.0% (9/9) | — |
| comparative | text_only | 6.7% (1/15) | 100.0% (15/15) | +93.3pp |
| comparative | enriched | 46.7% (7/15) | 93.3% (14/15) | +46.7pp |

### 2.1 This view cuts both ways

The alternative rule bounds a limitation in the case definition. It also removes most
of the enrichment advantage it was not designed to test, and that consequence belongs
here rather than in a footnote:

> **On the 38-item intersection the two arms converge at 97.4% and 97.4% —
> effectively identical.** Under the primary taxonomy the same population reads
> 60.5% for `text_only` against 78.9% for `metadata_enriched`, a gap of
> 18.4 percentage points. **That gap largely disappears once correct
> abstentions on unanswerable comparative items stop counting as failures.**

Stated the other way round: a substantial part of the apparent Stage 2 benefit of
enrichment is the primary taxonomy penalising `text_only` for abstaining correctly
more often. `text_only` abstained on 15 of these comparative partial-coverage items
and `metadata_enriched` on 17 across the full Case C population, but within the
intersection the text_only arm carries more of them, so it absorbs more of the
penalty. Neither reading is privileged here: the primary taxonomy remains the
reported one, and this is the bound on how much of its Case C gap is attributable to
the case definition rather than to generation quality.

**The same dependency structure applies.** The changed observations come from a small
number of repeated questions (section 3), so every figure in this section inherits the
clustering that made the observation-level McNemar in
`analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md` anti-conservative. These are observation counts, not
independent evidence, and no significance claim is made from them in either direction.

## 3. Observations that change status

**32 of 147** Case C observations change from a failure to a success under the alternative rule — every one of them a comparative partial-coverage abstention. **21** of them fall inside the 38-item intersection.

| arm | count |
|---|--:|
| text_only | 15 |
| enriched | 17 |

| condition | question | coverage | in intersection |
|---|---|--:|---|
| chunk200_bm25 | ref_comp_06 | 0.50 | yes |
| chunk200_bm25 | ref_comp_08 | 0.50 | yes |
| chunk200_bm25_enriched | ref_comp_02 | 0.50 | no |
| chunk200_bm25_enriched | ref_comp_08 | 0.50 | yes |
| chunk200_bm25_enriched | ref_comp_11 | 0.50 | no |
| chunk200_dense | ref_comp_08 | 0.50 | yes |
| chunk200_dense_enriched | ref_comp_02 | 0.50 | no |
| chunk200_dense_enriched | ref_comp_07 | 0.50 | no |
| chunk200_dense_enriched | ref_comp_08 | 0.50 | yes |
| chunk200_dense_enriched | ref_comp_12 | 0.50 | no |
| chunk200_hybrid | ref_comp_06 | 0.50 | yes |
| chunk200_hybrid | ref_comp_08 | 0.50 | yes |
| chunk200_hybrid | ref_comp_11 | 0.50 | yes |
| chunk200_hybrid_enriched | ref_comp_02 | 0.50 | no |
| chunk200_hybrid_enriched | ref_comp_04 | 0.50 | no |
| chunk200_hybrid_enriched | ref_comp_08 | 0.50 | yes |
| chunk500_bm25 | ref_comp_02 | 0.50 | yes |
| chunk500_bm25 | ref_comp_06 | 0.50 | yes |
| chunk500_bm25_enriched | ref_comp_01 | 0.50 | no |
| chunk500_bm25_enriched | ref_comp_02 | 0.50 | yes |
| chunk500_dense | ref_comp_02 | 0.50 | yes |
| chunk500_dense | ref_comp_06 | 0.50 | yes |
| chunk500_dense | ref_comp_08 | 0.50 | yes |
| chunk500_dense | ref_comp_11 | 0.50 | yes |
| chunk500_dense_enriched | ref_comp_02 | 0.50 | yes |
| chunk500_dense_enriched | ref_comp_08 | 0.50 | yes |
| chunk500_dense_enriched | ref_comp_12 | 0.50 | no |
| chunk500_hybrid | ref_comp_02 | 0.50 | yes |
| chunk500_hybrid | ref_comp_08 | 0.50 | yes |
| chunk500_hybrid | ref_comp_11 | 0.50 | no |
| chunk500_hybrid_enriched | ref_comp_08 | 0.50 | yes |
| chunk500_hybrid_enriched | ref_comp_09 | 0.50 | no |

The 32 changed observations come from **9 distinct questions** (`ref_comp_01` x1, `ref_comp_02` x8, `ref_comp_04` x1, `ref_comp_06` x4, `ref_comp_07` x1, `ref_comp_08` x10, `ref_comp_09` x1, `ref_comp_11` x4, `ref_comp_12` x2), the largest single contributor being `ref_comp_08` with 10 of the 32. This is the same dependency structure that made the observation-level McNemar in `analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md` anti-conservative: a handful of questions repeated across condition pairs, not independent trials. **Every figure in this document, including section 2.1, inherits it.** Read these as observation counts; no significance claim is made from them in either direction.
