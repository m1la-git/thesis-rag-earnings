> **No validation surface.** No expectation set exists for this script under any model. Its one check is that it reproduces every stored p value from the frozen inputs before computing anything, and it stops if one does not.

# Smallest attainable p — Stage 2 (`qwen3.8-27b@q8_k_xl`)

Input: `stage2_statistics_12cond.csv` in this directory. Generator: `analysis/attainability.py`. For each testable comparison, the smallest two-sided p the exact McNemar test could have returned at its number of discordant pairs, n: `binomtest(n, n, 0.5)` = 2 × 0.5^n. The same call and dispatch as `stage2_statistics_12cond.mcnemar`. **Before correction**; Holm attainability is family-dependent and is not computed.

Every stored `p` for a testable comparison was reproduced from its stored discordant counts before this was computed (tolerance 1e-12).

## By family and scope

| family | scope | comparisons | testable | could reach p < .05 | could not |
|---|---|--:|--:|--:|--:|
| Family 1 | pooled | 48 | 31 | 2 | 29 |
| Family 1 | factual | 48 | 4 | 0 | 4 |
| Family 1 | thematic | 48 | 22 | 1 | 21 |
| Family 1 | comparative | 48 | 15 | 0 | 15 |
| Family 2 | pooled | 120 | 65 | 4 | 61 |
| Family 2 | factual | 120 | 22 | 0 | 22 |
| Family 2 | thematic | 120 | 39 | 3 | 36 |
| Family 2 | comparative | 120 | 41 | 0 | 41 |
| Family 3 | pooled | 120 | 78 | 3 | 75 |
| Family 3 | factual | 120 | 0 | 0 | 0 |
| Family 3 | thematic | 120 | 65 | 0 | 65 |
| Family 3 | comparative | 120 | 33 | 0 | 33 |
| **all Stage 2** | | **1152** | **415** | **13** | **402** |

## Testable comparisons by number of discordant pairs

| discordant pairs | comparisons | smallest attainable p | could reach .05 |
|--:|--:|--:|:-:|
| 1 | 203 | 1 | no |
| 2 | 103 | 0.5 | no |
| 3 | 44 | 0.25 | no |
| 4 | 34 | 0.125 | no |
| 5 | 18 | 0.0625 | no |
| 6 | 10 | 0.03125 | yes |
| 7 | 3 | 0.01562 | yes |

Per-row detail: `attainability_stage2.csv` in this directory.
