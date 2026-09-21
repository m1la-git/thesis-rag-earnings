> **No validation surface.** No expectation set exists for this script under any model. Its one check is that it reproduces every stored p value from the frozen inputs before computing anything, and it stops if one does not.

# Smallest attainable p — Stage 1 (generator-independent)

Inputs: `analysis/stage1/stage1_scores_long_12cond.csv`, `analysis/stage1/stage1_statistics_12cond.csv`. Generator: `analysis/attainability.py`. For each comparison, the smallest two-sided p the paired Wilcoxon could have returned with every observed magnitude, tie and zero kept and only the signs set to agree — the same call and dispatch as `rebuild_statistics.paired_wilcoxon`. **Before correction.** Holm attainability is not computed: it depends on the rest of each family, so it is not a property of one comparison.

Every stored `p_raw` in the input was reproduced from the frozen scores before this was computed (tolerance 1e-12).

## By family and scope, both metrics together

| family | scope | comparisons | testable | could reach p < .05 | could not |
|---|---|--:|--:|--:|--:|
| Family 1 | pooled | 12 | 12 | 12 | 0 |
| Family 1 | factual | 12 | 12 | 12 | 0 |
| Family 1 | thematic | 12 | 10 | 0 | 10 |
| Family 1 | comparative | 12 | 12 | 3 | 9 |
| Family 2 | pooled | 30 | 30 | 29 | 1 |
| Family 2 | factual | 30 | 30 | 12 | 18 |
| Family 2 | thematic | 30 | 30 | 0 | 30 |
| Family 2 | comparative | 30 | 29 | 0 | 29 |
| Family 3 | pooled | 30 | 30 | 30 | 0 |
| Family 3 | factual | 30 | 29 | 23 | 6 |
| Family 3 | thematic | 30 | 28 | 1 | 27 |
| Family 3 | comparative | 30 | 30 | 7 | 23 |
| **all Stage 1** | | **288** | **282** | **129** | **153** |

## By family, scope and metric

| family | scope | metric | comparisons | testable | could reach p < .05 | could not |
|---|---|---|--:|--:|--:|--:|
| Family 1 | pooled | anchor_coverage_at_5 | 6 | 6 | 6 | 0 |
| Family 1 | pooled | mean_reciprocal_rank_at_5 | 6 | 6 | 6 | 0 |
| Family 1 | factual | anchor_coverage_at_5 | 6 | 6 | 6 | 0 |
| Family 1 | factual | mean_reciprocal_rank_at_5 | 6 | 6 | 6 | 0 |
| Family 1 | thematic | anchor_coverage_at_5 | 6 | 5 | 0 | 5 |
| Family 1 | thematic | mean_reciprocal_rank_at_5 | 6 | 5 | 0 | 5 |
| Family 1 | comparative | anchor_coverage_at_5 | 6 | 6 | 1 | 5 |
| Family 1 | comparative | mean_reciprocal_rank_at_5 | 6 | 6 | 2 | 4 |
| Family 2 | pooled | anchor_coverage_at_5 | 15 | 15 | 14 | 1 |
| Family 2 | pooled | mean_reciprocal_rank_at_5 | 15 | 15 | 15 | 0 |
| Family 2 | factual | anchor_coverage_at_5 | 15 | 15 | 8 | 7 |
| Family 2 | factual | mean_reciprocal_rank_at_5 | 15 | 15 | 4 | 11 |
| Family 2 | thematic | anchor_coverage_at_5 | 15 | 15 | 0 | 15 |
| Family 2 | thematic | mean_reciprocal_rank_at_5 | 15 | 15 | 0 | 15 |
| Family 2 | comparative | anchor_coverage_at_5 | 15 | 14 | 0 | 14 |
| Family 2 | comparative | mean_reciprocal_rank_at_5 | 15 | 15 | 0 | 15 |
| Family 3 | pooled | anchor_coverage_at_5 | 15 | 15 | 15 | 0 |
| Family 3 | pooled | mean_reciprocal_rank_at_5 | 15 | 15 | 15 | 0 |
| Family 3 | factual | anchor_coverage_at_5 | 15 | 14 | 9 | 5 |
| Family 3 | factual | mean_reciprocal_rank_at_5 | 15 | 15 | 14 | 1 |
| Family 3 | thematic | anchor_coverage_at_5 | 15 | 13 | 0 | 13 |
| Family 3 | thematic | mean_reciprocal_rank_at_5 | 15 | 15 | 1 | 14 |
| Family 3 | comparative | anchor_coverage_at_5 | 15 | 15 | 0 | 15 |
| Family 3 | comparative | mean_reciprocal_rank_at_5 | 15 | 15 | 7 | 8 |
| **all Stage 1** | | | **288** | **282** | **129** | **153** |

## Size-only pairs (chunk200_X vs chunk500_X) — H1's evidence

Families 2 and 3 only; Family 1 holds no size-only pair.

| family | scope | comparisons | testable | could reach p < .05 | could not |
|---|---|--:|--:|--:|--:|
| Family 2 | pooled | 6 | 6 | 6 | 0 |
| Family 2 | factual | 6 | 6 | 3 | 3 |
| Family 2 | thematic | 6 | 6 | 0 | 6 |
| Family 2 | comparative | 6 | 6 | 0 | 6 |
| Family 3 | pooled | 6 | 6 | 6 | 0 |
| Family 3 | factual | 6 | 6 | 4 | 2 |
| Family 3 | thematic | 6 | 5 | 1 | 4 |
| Family 3 | comparative | 6 | 6 | 2 | 4 |
| **size-only** | | **48** | **47** | **22** | **25** |

### Every size-only comparison

| family | scope | metric | pair | n≠0 | observed p | smallest attainable p | could reach .05 |
|---|---|---|---|--:|--:|--:|:-:|
| Family 2 | pooled | anchor_coverage_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 7 | 0.8623197383894363 | 0.0151862 | yes |
| Family 2 | pooled | anchor_coverage_at_5 | `chunk200_dense` vs `chunk500_dense` | 9 | 0.5055707258803321 | 0.00645895 | yes |
| Family 2 | pooled | anchor_coverage_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 6 | 0.5164122683960384 | 0.0231409 | yes |
| Family 2 | pooled | mean_reciprocal_rank_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 8 | 0.6236388261276493 | 0.011616 | yes |
| Family 2 | pooled | mean_reciprocal_rank_at_5 | `chunk200_dense` vs `chunk500_dense` | 11 | 0.13009440924007054 | 0.00329894 | yes |
| Family 2 | pooled | mean_reciprocal_rank_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 11 | 0.4224478419544786 | 0.00326803 | yes |
| Family 2 | factual | anchor_coverage_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 4 | 1.0 | 0.0455003 | yes |
| Family 2 | factual | anchor_coverage_at_5 | `chunk200_dense` vs `chunk500_dense` | 3 | 0.5637028616507731 | 0.0832645 | **no** |
| Family 2 | factual | anchor_coverage_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 4 | 0.31731050786291415 | 0.0455003 | yes |
| Family 2 | factual | mean_reciprocal_rank_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 4 | 0.8539232992870668 | 0.0655997 | **no** |
| Family 2 | factual | mean_reciprocal_rank_at_5 | `chunk200_dense` vs `chunk500_dense` | 3 | 0.5929800980174267 | 0.108809 | **no** |
| Family 2 | factual | mean_reciprocal_rank_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 5 | 0.6802795473344503 | 0.0393595 | yes |
| Family 2 | thematic | anchor_coverage_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 1 | 0.31731050786291415 | 0.317311 | **no** |
| Family 2 | thematic | anchor_coverage_at_5 | `chunk200_dense` vs `chunk500_dense` | 3 | 0.27630291733748347 | 0.10247 | **no** |
| Family 2 | thematic | anchor_coverage_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 1 | 0.31731050786291415 | 0.317311 | **no** |
| Family 2 | thematic | mean_reciprocal_rank_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 1 | 0.31731050786291415 | 0.317311 | **no** |
| Family 2 | thematic | mean_reciprocal_rank_at_5 | `chunk200_dense` vs `chunk500_dense` | 4 | 0.14412703481601533 | 0.0678892 | **no** |
| Family 2 | thematic | mean_reciprocal_rank_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 2 | 0.17971249487899976 | 0.179712 | **no** |
| Family 2 | comparative | anchor_coverage_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 2 | 0.5 | 0.5 | **no** |
| Family 2 | comparative | anchor_coverage_at_5 | `chunk200_dense` vs `chunk500_dense` | 3 | 0.25 | 0.25 | **no** |
| Family 2 | comparative | anchor_coverage_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 1 | 1.0 | 1 | **no** |
| Family 2 | comparative | mean_reciprocal_rank_at_5 | `chunk200_bm25` vs `chunk500_bm25` | 3 | 0.5 | 0.25 | **no** |
| Family 2 | comparative | mean_reciprocal_rank_at_5 | `chunk200_dense` vs `chunk500_dense` | 4 | 0.125 | 0.125 | **no** |
| Family 2 | comparative | mean_reciprocal_rank_at_5 | `chunk200_hybrid` vs `chunk500_hybrid` | 4 | 0.25 | 0.125 | **no** |
| Family 3 | pooled | anchor_coverage_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 8 | 0.5637028616507731 | 0.00937477 | yes |
| Family 3 | pooled | anchor_coverage_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 6 | 0.45035134358487394 | 0.0235441 | yes |
| Family 3 | pooled | anchor_coverage_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 9 | 0.41741292343058733 | 0.00500017 | yes |
| Family 3 | pooled | mean_reciprocal_rank_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 13 | 0.24828546343650038 | 0.00145412 | yes |
| Family 3 | pooled | mean_reciprocal_rank_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 18 | 0.2664285829701688 | 0.000194383 | yes |
| Family 3 | pooled | mean_reciprocal_rank_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 18 | 0.6625959372280352 | 0.000190996 | yes |
| Family 3 | factual | anchor_coverage_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 5 | 0.6547208460185769 | 0.0253473 | yes |
| Family 3 | factual | anchor_coverage_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 1 | 0.31731050786291415 | 0.317311 | **no** |
| Family 3 | factual | anchor_coverage_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 1 | 0.31731050786291415 | 0.317311 | **no** |
| Family 3 | factual | mean_reciprocal_rank_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 8 | 0.18181616460470695 | 0.011412 | yes |
| Family 3 | factual | mean_reciprocal_rank_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 7 | 0.12750833049058283 | 0.0177559 | yes |
| Family 3 | factual | mean_reciprocal_rank_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 7 | 0.23420128325876344 | 0.0173497 | yes |
| Family 3 | thematic | anchor_coverage_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 0 | — | — | untestable |
| Family 3 | thematic | anchor_coverage_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 3 | 0.27630291733748347 | 0.10247 | **no** |
| Family 3 | thematic | anchor_coverage_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 3 | 1.0 | 0.10247 | **no** |
| Family 3 | thematic | mean_reciprocal_rank_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 1 | 0.31731050786291415 | 0.317311 | **no** |
| Family 3 | thematic | mean_reciprocal_rank_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 4 | 0.7127018566581784 | 0.0655997 | **no** |
| Family 3 | thematic | mean_reciprocal_rank_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 5 | 0.22491588401596185 | 0.0431144 | yes |
| Family 3 | comparative | anchor_coverage_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 3 | 1.0 | 0.25 | **no** |
| Family 3 | comparative | anchor_coverage_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 2 | 0.5 | 0.5 | **no** |
| Family 3 | comparative | anchor_coverage_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 5 | 1.0 | 0.0625 | **no** |
| Family 3 | comparative | mean_reciprocal_rank_at_5 | `chunk200_bm25_enriched` vs `chunk500_bm25_enriched` | 4 | 1.0 | 0.125 | **no** |
| Family 3 | comparative | mean_reciprocal_rank_at_5 | `chunk200_dense_enriched` vs `chunk500_dense_enriched` | 7 | 0.78125 | 0.015625 | yes |
| Family 3 | comparative | mean_reciprocal_rank_at_5 | `chunk200_hybrid_enriched` vs `chunk500_hybrid_enriched` | 6 | 0.875 | 0.03125 | yes |

## Pooled comparisons that could not have reached p < .05

| family | metric | pair | n≠0 | smallest attainable p |
|---|---|---|--:|--:|
| Family 2 | anchor_coverage_at_5 | `chunk200_bm25` vs `chunk200_hybrid` | 4 | 0.0587817 |

Per-row detail: `analysis/stage1/attainability_stage1.csv`.
