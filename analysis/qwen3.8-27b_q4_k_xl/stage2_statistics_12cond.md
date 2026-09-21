# Stage 2 statistics across all 12 conditions

Model: `qwen3.8-27b@q4_k_xl`. Source: `results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv` (540 rows, 12 conditions).

**Method frozen, population extended.** Recovered from `analysis/qwen3.8-27b_q4_k_xl/stage2_statistics.md` and re-validated against its published values before anything here was computed: case membership is per (question, condition); a pair's matched set is the questions both conditions call case K; **McNemar's exact test** (`binomtest` on the larger discordant count, n = b+c, p = 0.5, two-sided). Holm–Bonferroni within each (case, outcome) cell at that cell's own size; untestable comparisons consume no rank. Categories are separate families. Unanswerable items are Case A and therefore never enter a Case B or Case C comparison, exactly as before.

Case A is not tested: it has no pairwise structure to test here (27–28 of 30 records abstain in both arms), matching the original, which tested B and C only.

## Family 1 — representation

### pooled (n=45)

Each `metadata_enriched` condition against its matched `text_only` counterpart (same chunk size, same strategy). Orientation: enriched first, so `win` = the enriched condition achieved the outcome where text_only did not. Holm family = the 6 pairs within each (case, outcome) cell.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 27 | 1 | 1 | 25 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk200_dense | 18 | 0 | 0 | 18 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 19 | 1 | 3 | 15 | 4 | 0.625 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 27 | 1 | 2 | 24 | 3 | 1.000 | 1.000 |
| B | abstained | chunk500_dense_enriched vs chunk500_dense | 21 | 1 | 5 | 15 | 6 | 0.219 | 1.000 |
| B | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 19 | 2 | 1 | 16 | 3 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_bm25 | 27 | 3 | 1 | 23 | 4 | 0.625 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk200_dense | 18 | 1 | 1 | 16 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 19 | 3 | 0 | 16 | 3 | 0.250 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_bm25 | 27 | 0 | 0 | 27 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense_enriched vs chunk500_dense | 21 | 2 | 1 | 18 | 3 | 1.000 | 1.000 |
| B | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 19 | 1 | 0 | 18 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 27 | 1 | 3 | 23 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk200_dense | 18 | 1 | 1 | 16 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 19 | 2 | 4 | 13 | 6 | 0.688 | 1.000 |
| B | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 27 | 2 | 1 | 24 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk500_dense_enriched vs chunk500_dense | 21 | 2 | 1 | 18 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 19 | 2 | 3 | 14 | 5 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 27 | 0 | 0 | 27 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_dense | 18 | 0 | 0 | 18 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 19 | 1 | 0 | 18 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 27 | 0 | 0 | 27 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_dense | 21 | 2 | 0 | 19 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 19 | 0 | 1 | 18 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 6 | 0 | 1 | 5 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 8 | 0 | 2 | 6 | 2 | 0.500 | 1.000 |
| C | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 5 | 0 | 1 | 4 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_dense_enriched vs chunk500_dense | 8 | 0 | 2 | 6 | 2 | 0.500 | 1.000 |
| C | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 7 | 0 | 1 | 6 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_bm25 | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 8 | 2 | 0 | 6 | 2 | 0.500 | 1.000 |
| C | correct | chunk500_bm25_enriched vs chunk500_bm25 | 5 | 2 | 0 | 3 | 2 | 0.500 | 1.000 |
| C | correct | chunk500_dense_enriched vs chunk500_dense | 8 | 2 | 0 | 6 | 2 | 0.500 | 1.000 |
| C | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 5 | 0 | 1 | 4 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_dense_enriched vs chunk500_dense | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense_enriched vs chunk500_dense | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 7 | 1 | 0 | 6 | 1 | 1.000 | 1.000 |

Untestable (zero discordant pairs): **18 of 48** comparisons in this scope.

### factual (n=14)

Each `metadata_enriched` condition against its matched `text_only` counterpart (same chunk size, same strategy). Orientation: enriched first, so `win` = the enriched condition achieved the outcome where text_only did not. Holm family = the 6 pairs within each (case, outcome) cell. Restricted to factual questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 1 | 0 | 6 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_dense_enriched vs chunk500_dense | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 1 | 6 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25_enriched vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense_enriched vs chunk500_dense | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_dense_enriched vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk200_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_dense_enriched vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk200_bm25 | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk200_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_dense_enriched vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_dense_enriched vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk200_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense_enriched vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **44 of 48** comparisons in this scope.

### thematic (n=15)

Each `metadata_enriched` condition against its matched `text_only` counterpart (same chunk size, same strategy). Orientation: enriched first, so `win` = the enriched condition achieved the outcome where text_only did not. Holm family = the 6 pairs within each (case, outcome) cell. Restricted to thematic questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 13 | 0 | 1 | 12 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk200_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 11 | 1 | 3 | 7 | 4 | 0.625 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 14 | 1 | 2 | 11 | 3 | 1.000 | 1.000 |
| B | abstained | chunk500_dense_enriched vs chunk500_dense | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 10 | 1 | 1 | 8 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_bm25 | 13 | 3 | 0 | 10 | 3 | 0.250 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk200_dense | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 11 | 3 | 0 | 8 | 3 | 0.250 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_bm25 | 14 | 0 | 0 | 14 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense_enriched vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 13 | 1 | 3 | 9 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk200_dense | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 11 | 2 | 4 | 5 | 6 | 0.688 | 1.000 |
| B | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 14 | 2 | 1 | 11 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk500_dense_enriched vs chunk500_dense | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 10 | 2 | 2 | 6 | 4 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 13 | 0 | 0 | 13 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 14 | 0 | 0 | 14 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_dense | 11 | 2 | 0 | 9 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_dense_enriched vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk200_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_bm25 | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_dense_enriched vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 1 | 0 | 1 | 0 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_dense_enriched vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense_enriched vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **28 of 48** comparisons in this scope.

### comparative (n=11)

Each `metadata_enriched` condition against its matched `text_only` counterpart (same chunk size, same strategy). Orientation: enriched first, so `win` = the enriched condition achieved the outcome where text_only did not. Holm family = the 6 pairs within each (case, outcome) cell. Restricted to comparative questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_dense_enriched vs chunk500_dense | 6 | 1 | 2 | 3 | 3 | 1.000 | 1.000 |
| B | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 5 | 1 | 0 | 4 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25_enriched vs chunk500_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense_enriched vs chunk500_dense | 6 | 1 | 1 | 4 | 2 | 1.000 | 1.000 |
| B | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_dense_enriched vs chunk500_dense | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 5 | 0 | 1 | 4 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_dense | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk200_bm25 | 2 | 0 | 1 | 1 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 2 | 1 | 2 | 0.500 | 1.000 |
| C | abstained | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 1 | 1 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_dense_enriched vs chunk500_dense | 4 | 0 | 2 | 2 | 2 | 0.500 | 1.000 |
| C | abstained | chunk500_hybrid_enriched vs chunk500_hybrid | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_bm25 | 2 | 1 | 0 | 1 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 2 | 0 | 1 | 2 | 0.500 | 1.000 |
| C | correct | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 1 | 0 | 1 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_dense_enriched vs chunk500_dense | 4 | 2 | 0 | 2 | 2 | 0.500 | 1.000 |
| C | correct | chunk500_hybrid_enriched vs chunk500_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_dense_enriched vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_hybrid_enriched vs chunk500_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense_enriched vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_hybrid_enriched vs chunk500_hybrid | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |

Untestable (zero discordant pairs): **33 of 48** comparisons in this scope.

## Family 2 — chunk size and strategy within text_only

### pooled (n=45)

The original A1 comparisons, as a replication check. Holm family = the 15 pairs within each (case, outcome) cell.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25 vs chunk200_dense | 31 | 1 | 2 | 28 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk200_hybrid | 30 | 2 | 2 | 26 | 4 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_bm25 | 29 | 3 | 2 | 24 | 5 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_dense | 29 | 3 | 2 | 24 | 5 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_hybrid | 29 | 2 | 1 | 26 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk200_hybrid | 30 | 1 | 1 | 28 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_bm25 | 28 | 2 | 2 | 24 | 4 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_dense | 29 | 3 | 2 | 24 | 5 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_hybrid | 28 | 2 | 1 | 25 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_bm25 | 26 | 3 | 4 | 19 | 7 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_dense | 27 | 3 | 2 | 22 | 5 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_hybrid | 28 | 2 | 1 | 25 | 3 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25 vs chunk500_dense | 28 | 3 | 1 | 24 | 4 | 0.625 | 1.000 |
| B | abstained | chunk500_bm25 vs chunk500_hybrid | 28 | 3 | 2 | 23 | 5 | 1.000 | 1.000 |
| B | abstained | chunk500_dense vs chunk500_hybrid | 29 | 1 | 1 | 27 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk200_dense | 31 | 1 | 0 | 30 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk200_hybrid | 30 | 1 | 0 | 29 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_bm25 | 29 | 0 | 2 | 27 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_dense | 29 | 1 | 3 | 25 | 4 | 0.625 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_hybrid | 29 | 1 | 1 | 27 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_dense vs chunk200_hybrid | 30 | 0 | 0 | 30 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk500_bm25 | 28 | 0 | 2 | 26 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_dense vs chunk500_dense | 29 | 0 | 3 | 26 | 3 | 0.250 | 1.000 |
| B | correct | chunk200_dense vs chunk500_hybrid | 28 | 0 | 1 | 27 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_bm25 | 26 | 0 | 2 | 24 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_dense | 27 | 0 | 3 | 24 | 3 | 0.250 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_hybrid | 28 | 0 | 1 | 27 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_bm25 vs chunk500_dense | 28 | 1 | 1 | 26 | 2 | 1.000 | 1.000 |
| B | correct | chunk500_bm25 vs chunk500_hybrid | 28 | 1 | 0 | 27 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_dense vs chunk500_hybrid | 29 | 2 | 0 | 27 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk200_dense | 31 | 1 | 1 | 29 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk200_hybrid | 30 | 2 | 2 | 26 | 4 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_bm25 | 29 | 3 | 2 | 24 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_dense | 29 | 2 | 1 | 26 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_hybrid | 29 | 0 | 0 | 29 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk200_hybrid | 30 | 2 | 1 | 27 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_bm25 | 28 | 3 | 1 | 24 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_dense | 29 | 2 | 0 | 27 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_hybrid | 28 | 1 | 1 | 26 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_bm25 | 26 | 4 | 2 | 20 | 6 | 0.688 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_dense | 27 | 1 | 0 | 26 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_hybrid | 28 | 2 | 2 | 24 | 4 | 1.000 | 1.000 |
| B | offtarget | chunk500_bm25 vs chunk500_dense | 28 | 1 | 3 | 24 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk500_bm25 vs chunk500_hybrid | 28 | 2 | 3 | 23 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk500_dense vs chunk500_hybrid | 29 | 1 | 2 | 26 | 3 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25 vs chunk200_dense | 31 | 0 | 0 | 31 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk200_hybrid | 30 | 0 | 1 | 29 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25 vs chunk500_bm25 | 29 | 0 | 0 | 29 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_dense | 29 | 0 | 0 | 29 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_hybrid | 29 | 0 | 1 | 28 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_dense vs chunk200_hybrid | 30 | 0 | 1 | 29 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_dense vs chunk500_bm25 | 28 | 0 | 0 | 28 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_dense | 29 | 0 | 0 | 29 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_hybrid | 28 | 0 | 0 | 28 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_bm25 | 26 | 1 | 0 | 25 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_hybrid vs chunk500_dense | 27 | 1 | 0 | 26 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_hybrid vs chunk500_hybrid | 28 | 1 | 1 | 26 | 2 | 1.000 | 1.000 |
| B | ungrounded | chunk500_bm25 vs chunk500_dense | 28 | 0 | 0 | 28 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25 vs chunk500_hybrid | 28 | 0 | 1 | 27 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk500_dense vs chunk500_hybrid | 29 | 0 | 1 | 28 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25 vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk200_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_bm25 | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25 vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_hybrid | 5 | 1 | 0 | 4 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_bm25 | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_bm25 | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_hybrid vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_hybrid | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_bm25 vs chunk500_dense | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_bm25 vs chunk500_hybrid | 5 | 1 | 1 | 3 | 2 | 1.000 | 1.000 |
| C | abstained | chunk500_dense vs chunk500_hybrid | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25 vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk200_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_bm25 | 4 | 1 | 1 | 2 | 2 | 1.000 | 1.000 |
| C | correct | chunk200_bm25 vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_hybrid | 5 | 0 | 1 | 4 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_bm25 | 1 | 0 | 1 | 0 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_bm25 | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_hybrid vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_hybrid | 6 | 0 | 1 | 5 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_bm25 vs chunk500_dense | 4 | 1 | 1 | 2 | 2 | 1.000 | 1.000 |
| C | correct | chunk500_bm25 vs chunk500_hybrid | 5 | 1 | 2 | 2 | 3 | 1.000 | 1.000 |
| C | correct | chunk500_dense vs chunk500_hybrid | 6 | 0 | 1 | 5 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_bm25 vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk200_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_bm25 | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_bm25 vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_bm25 | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25 vs chunk500_dense | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_bm25 vs chunk500_hybrid | 5 | 1 | 0 | 4 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_dense vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_bm25 | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk200_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_bm25 | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_dense | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_hybrid | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **50 of 120** comparisons in this scope.

### factual (n=14)

The original A1 comparisons, as a replication check. Holm family = the 15 pairs within each (case, outcome) cell. Restricted to factual questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25 vs chunk200_dense | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk200_hybrid | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_bm25 | 9 | 1 | 0 | 8 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_dense | 10 | 1 | 1 | 8 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_hybrid | 10 | 1 | 1 | 8 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk200_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense vs chunk500_bm25 | 9 | 1 | 0 | 8 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_dense | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_hybrid | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_bm25 | 8 | 1 | 0 | 7 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_dense | 9 | 1 | 0 | 8 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_hybrid | 9 | 1 | 0 | 8 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25 vs chunk500_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25 vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk200_dense | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk200_hybrid | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_bm25 | 9 | 0 | 1 | 8 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_dense | 10 | 1 | 1 | 8 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_hybrid | 10 | 1 | 1 | 8 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_dense vs chunk200_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk500_bm25 | 9 | 0 | 1 | 8 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_dense vs chunk500_dense | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_dense vs chunk500_hybrid | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_bm25 | 8 | 0 | 1 | 7 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_dense | 9 | 0 | 1 | 8 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_hybrid | 9 | 0 | 1 | 8 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_bm25 vs chunk500_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25 vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk200_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk200_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk500_bm25 | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk500_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk200_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk500_bm25 | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid vs chunk500_bm25 | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid vs chunk500_dense | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid vs chunk500_hybrid | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25 vs chunk500_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25 vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk200_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk200_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_bm25 | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk200_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_bm25 | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_bm25 | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_dense | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_hybrid | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25 vs chunk500_dense | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25 vs chunk500_hybrid | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_dense | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense vs chunk500_hybrid | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **98 of 120** comparisons in this scope.

### thematic (n=15)

The original A1 comparisons, as a replication check. Holm family = the 15 pairs within each (case, outcome) cell. Restricted to thematic questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25 vs chunk200_dense | 12 | 1 | 0 | 11 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk200_hybrid | 12 | 1 | 0 | 11 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_bm25 | 13 | 2 | 2 | 9 | 4 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_dense | 12 | 1 | 1 | 10 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_hybrid | 12 | 1 | 0 | 11 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk200_hybrid | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_bm25 | 12 | 1 | 2 | 9 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_dense | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_hybrid | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_bm25 | 12 | 2 | 3 | 7 | 5 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_dense | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_hybrid | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25 vs chunk500_dense | 12 | 2 | 1 | 9 | 3 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25 vs chunk500_hybrid | 12 | 3 | 2 | 7 | 5 | 1.000 | 1.000 |
| B | abstained | chunk500_dense vs chunk500_hybrid | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk200_dense | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk200_hybrid | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk500_bm25 | 13 | 0 | 1 | 12 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_dense | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk500_hybrid | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk200_hybrid | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk500_bm25 | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_dense vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid vs chunk500_bm25 | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid vs chunk500_hybrid | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25 vs chunk500_dense | 12 | 1 | 0 | 11 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_bm25 vs chunk500_hybrid | 12 | 1 | 0 | 11 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk200_dense | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk200_hybrid | 12 | 1 | 1 | 10 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_bm25 | 13 | 3 | 2 | 8 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_dense | 12 | 1 | 1 | 10 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_hybrid | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk200_hybrid | 12 | 2 | 0 | 10 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_bm25 | 12 | 3 | 1 | 8 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_dense | 11 | 2 | 0 | 9 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_hybrid | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_bm25 | 12 | 3 | 2 | 7 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid vs chunk500_hybrid | 12 | 1 | 1 | 10 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk500_bm25 vs chunk500_dense | 12 | 1 | 3 | 8 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk500_bm25 vs chunk500_hybrid | 12 | 2 | 3 | 7 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk500_dense vs chunk500_hybrid | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25 vs chunk200_dense | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk200_hybrid | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25 vs chunk500_bm25 | 13 | 0 | 0 | 13 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_dense | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_hybrid | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_dense vs chunk200_hybrid | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_dense vs chunk500_bm25 | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_dense | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_hybrid | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_bm25 | 12 | 1 | 0 | 11 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_hybrid vs chunk500_dense | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_hybrid vs chunk500_hybrid | 12 | 1 | 1 | 10 | 2 | 1.000 | 1.000 |
| B | ungrounded | chunk500_bm25 vs chunk500_dense | 12 | 0 | 0 | 12 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25 vs chunk500_hybrid | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk500_dense vs chunk500_hybrid | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25 vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_bm25 | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25 vs chunk500_dense | 1 | 0 | 1 | 0 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 1 | 0 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 1 | 0 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25 vs chunk500_dense | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_bm25 vs chunk500_hybrid | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_bm25 | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **74 of 120** comparisons in this scope.

### comparative (n=11)

The original A1 comparisons, as a replication check. Holm family = the 15 pairs within each (case, outcome) cell. Restricted to comparative questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25 vs chunk200_dense | 9 | 0 | 1 | 8 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk200_hybrid | 8 | 1 | 1 | 6 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_bm25 vs chunk500_dense | 7 | 1 | 0 | 6 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25 vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense vs chunk200_hybrid | 8 | 1 | 0 | 7 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense vs chunk500_dense | 7 | 2 | 0 | 5 | 2 | 0.500 | 1.000 |
| B | abstained | chunk200_dense vs chunk500_hybrid | 7 | 1 | 0 | 6 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_bm25 | 6 | 0 | 1 | 5 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_dense | 7 | 2 | 1 | 4 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid vs chunk500_hybrid | 7 | 1 | 1 | 5 | 2 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25 vs chunk500_dense | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25 vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_dense vs chunk500_hybrid | 7 | 0 | 1 | 6 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25 vs chunk200_dense | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk200_hybrid | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25 vs chunk500_dense | 7 | 0 | 2 | 5 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_bm25 vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk200_hybrid | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense vs chunk500_dense | 7 | 0 | 2 | 5 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_dense vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid vs chunk500_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid vs chunk500_dense | 7 | 0 | 2 | 5 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_hybrid vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25 vs chunk500_dense | 6 | 0 | 1 | 5 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_bm25 vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense vs chunk500_hybrid | 7 | 2 | 0 | 5 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk200_dense | 9 | 1 | 0 | 8 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk200_hybrid | 8 | 1 | 1 | 6 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25 vs chunk500_dense | 7 | 1 | 0 | 6 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25 vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk200_hybrid | 8 | 0 | 1 | 7 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk500_dense | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense vs chunk500_hybrid | 7 | 0 | 1 | 6 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_bm25 | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_dense | 7 | 1 | 0 | 6 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid vs chunk500_hybrid | 7 | 1 | 1 | 5 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk500_bm25 vs chunk500_dense | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25 vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_dense vs chunk500_hybrid | 7 | 0 | 1 | 6 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25 vs chunk200_dense | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk200_hybrid | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_dense | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25 vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk200_hybrid | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_bm25 | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_dense | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_bm25 | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_dense | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25 vs chunk500_dense | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25 vs chunk500_hybrid | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense vs chunk500_hybrid | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_bm25 | 2 | 1 | 0 | 1 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25 vs chunk500_hybrid | 2 | 1 | 0 | 1 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_bm25 | 1 | 1 | 0 | 0 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_bm25 | 2 | 1 | 0 | 1 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_hybrid vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid vs chunk500_hybrid | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_bm25 vs chunk500_dense | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_bm25 vs chunk500_hybrid | 3 | 1 | 1 | 1 | 2 | 1.000 | 1.000 |
| C | abstained | chunk500_dense vs chunk500_hybrid | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_bm25 | 2 | 0 | 1 | 1 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 1 | 1 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_bm25 | 1 | 0 | 1 | 0 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_bm25 | 2 | 0 | 1 | 1 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_hybrid vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid vs chunk500_hybrid | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_bm25 vs chunk500_dense | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | correct | chunk500_bm25 vs chunk500_hybrid | 3 | 1 | 1 | 1 | 2 | 1.000 | 1.000 |
| C | correct | chunk500_dense vs chunk500_hybrid | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid vs chunk500_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25 vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25 vs chunk500_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_dense vs chunk500_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk200_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_dense | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25 vs chunk500_hybrid | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk200_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_bm25 | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_dense | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense vs chunk500_hybrid | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_bm25 | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid vs chunk500_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_dense | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25 vs chunk500_hybrid | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense vs chunk500_hybrid | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **79 of 120** comparisons in this scope.

## Family 3 — chunk size and strategy within metadata_enriched

### pooled (n=45)

The same comparisons inside the arm whose index carries company/period identity. Holm family = the 15 pairs within each (case, outcome) cell.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 17 | 1 | 1 | 15 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 19 | 3 | 1 | 15 | 4 | 0.625 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 25 | 2 | 3 | 20 | 5 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 19 | 5 | 1 | 13 | 6 | 0.219 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 19 | 2 | 2 | 15 | 4 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 17 | 1 | 0 | 16 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 18 | 1 | 1 | 16 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 2 | 0 | 15 | 2 | 0.500 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 1 | 0 | 15 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 19 | 1 | 2 | 16 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 17 | 2 | 0 | 15 | 2 | 0.500 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 16 | 1 | 0 | 15 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 19 | 4 | 0 | 15 | 4 | 0.125 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 21 | 1 | 0 | 20 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 18 | 0 | 2 | 16 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 17 | 1 | 0 | 16 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 19 | 0 | 1 | 18 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 25 | 2 | 0 | 23 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 19 | 3 | 2 | 14 | 5 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 19 | 2 | 0 | 17 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 17 | 0 | 2 | 15 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 18 | 1 | 1 | 16 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 1 | 1 | 15 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 19 | 2 | 0 | 17 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 17 | 3 | 1 | 13 | 4 | 0.625 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 16 | 2 | 0 | 14 | 2 | 0.500 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 19 | 1 | 2 | 16 | 3 | 1.000 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 21 | 1 | 1 | 19 | 2 | 1.000 | 1.000 |
| B | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 18 | 1 | 1 | 16 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 17 | 1 | 2 | 14 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 19 | 3 | 2 | 14 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 25 | 1 | 2 | 22 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 19 | 2 | 5 | 12 | 7 | 0.453 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 19 | 1 | 3 | 15 | 4 | 0.625 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 17 | 3 | 0 | 14 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 18 | 1 | 1 | 16 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 1 | 1 | 15 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 1 | 15 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 19 | 0 | 3 | 16 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 17 | 0 | 3 | 14 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 16 | 0 | 4 | 12 | 4 | 0.125 | 1.000 |
| B | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 19 | 2 | 3 | 14 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 21 | 0 | 1 | 20 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 18 | 2 | 2 | 14 | 4 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 17 | 0 | 0 | 17 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 19 | 0 | 2 | 17 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 25 | 0 | 0 | 25 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 19 | 0 | 2 | 17 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 19 | 0 | 0 | 19 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 17 | 0 | 2 | 15 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 18 | 0 | 0 | 18 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 0 | 2 | 15 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 19 | 2 | 0 | 17 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 17 | 0 | 1 | 16 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 16 | 1 | 0 | 15 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 19 | 0 | 2 | 17 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 21 | 0 | 0 | 21 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 18 | 2 | 0 | 16 | 2 | 0.500 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 18 | 1 | 0 | 17 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 9 | 0 | 1 | 8 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 0 | 0 | 17 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 1 | 0 | 15 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 15 | 1 | 0 | 14 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 10 | 2 | 0 | 8 | 2 | 0.500 | 1.000 |
| C | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 16 | 1 | 1 | 14 | 2 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 18 | 0 | 1 | 17 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 0 | 0 | 17 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 15 | 0 | 0 | 15 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 16 | 1 | 0 | 15 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 18 | 0 | 0 | 18 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 9 | 1 | 0 | 8 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 0 | 0 | 17 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 15 | 0 | 0 | 15 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 7 | 0 | 0 | 7 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 18 | 0 | 0 | 18 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 17 | 0 | 0 | 17 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 1 | 15 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 16 | 0 | 0 | 16 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 15 | 0 | 1 | 14 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 8 | 0 | 0 | 8 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 16 | 0 | 1 | 15 | 1 | 1.000 | 1.000 |

Untestable (zero discordant pairs): **45 of 120** comparisons in this scope.

### factual (n=14)

The same comparisons inside the arm whose index carries company/period identity. Holm family = the 15 pairs within each (case, outcome) cell. Restricted to factual questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 9 | 0 | 0 | 9 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **120 of 120** comparisons in this scope.

### thematic (n=15)

The same comparisons inside the arm whose index carries company/period identity. Holm family = the 15 pairs within each (case, outcome) cell. Restricted to thematic questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 12 | 2 | 0 | 10 | 2 | 0.500 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 14 | 2 | 2 | 10 | 4 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 11 | 2 | 0 | 9 | 2 | 0.500 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 11 | 2 | 1 | 8 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 12 | 1 | 2 | 9 | 3 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 11 | 2 | 0 | 9 | 2 | 0.500 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 12 | 0 | 1 | 11 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 14 | 2 | 0 | 12 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 11 | 3 | 0 | 8 | 3 | 0.250 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 11 | 2 | 0 | 9 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 12 | 2 | 0 | 10 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 3 | 0 | 7 | 3 | 0.250 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 2 | 0 | 8 | 2 | 0.500 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 11 | 1 | 0 | 10 | 1 | 1.000 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 12 | 2 | 1 | 9 | 3 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 14 | 0 | 2 | 12 | 2 | 0.500 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 11 | 1 | 4 | 6 | 5 | 0.375 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 11 | 0 | 3 | 8 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 3 | 0 | 8 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 11 | 1 | 1 | 9 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 1 | 1 | 8 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 12 | 0 | 3 | 9 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 0 | 3 | 7 | 3 | 0.250 | 1.000 |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 0 | 4 | 6 | 4 | 0.125 | 1.000 |
| B | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 11 | 2 | 3 | 6 | 5 | 1.000 | 1.000 |
| B | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 11 | 0 | 1 | 10 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 11 | 2 | 2 | 7 | 4 | 1.000 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 12 | 0 | 2 | 10 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 14 | 0 | 0 | 14 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 10 | 0 | 2 | 8 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 10 | 0 | 0 | 10 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 12 | 2 | 0 | 10 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 10 | 0 | 1 | 9 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 10 | 1 | 0 | 9 | 1 | 1.000 | 1.000 |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 11 | 0 | 2 | 9 | 2 | 0.500 | 1.000 |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 11 | 0 | 0 | 11 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 11 | 2 | 0 | 9 | 2 | 0.500 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 0 | 0 | 0 | 0 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 1 | 0 | 0 | 1 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |

Untestable (zero discordant pairs): **65 of 120** comparisons in this scope.

### comparative (n=11)

The same comparisons inside the arm whose index carries company/period identity. Holm family = the 15 pairs within each (case, outcome) cell. Restricted to comparative questions.

| case | outcome | pair | matched n | win | loss | tie | n disc | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| B | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 5 | 1 | 1 | 3 | 2 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 6 | 0 | 1 | 5 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 6 | 3 | 1 | 2 | 4 | 0.625 | 1.000 |
| B | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 5 | 0 | 1 | 4 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| B | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 2 | 0 | 3 | 2 | 0.500 | 1.000 |
| B | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 6 | 0 | 2 | 4 | 2 | 0.500 | 1.000 |
| B | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| B | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 2 | 3 | 2 | 0.500 | 1.000 |
| B | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 5 | 1 | 1 | 3 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 6 | 1 | 0 | 5 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 6 | 1 | 1 | 4 | 2 | 1.000 | 1.000 |
| B | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 5 | 1 | 0 | 4 | 1 | 1.000 | 1.000 |
| B | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 6 | 0 | 0 | 6 | 0 | **untestable (no discordant pairs)** | n/a |
| B | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_bm25_enriched vs chunk500_dense_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk200_hybrid_enriched | 5 | 1 | 0 | 4 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_dense_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_dense_enriched vs chunk500_hybrid_enriched | 4 | 1 | 0 | 3 | 1 | 1.000 | 1.000 |
| C | abstained | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | abstained | chunk500_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | abstained | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 3 | 2 | 0 | 1 | 2 | 0.500 | 1.000 |
| C | abstained | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_bm25_enriched vs chunk500_dense_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk200_hybrid_enriched | 5 | 0 | 1 | 4 | 1 | 1.000 | 1.000 |
| C | correct | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | correct | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk200_hybrid_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 1 | 0 | 2 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk200_dense_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | offtarget | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | offtarget | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk200_hybrid_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk200_dense_enriched vs chunk200_hybrid_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_bm25_enriched | 3 | 0 | 0 | 3 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_dense_enriched | 5 | 0 | 0 | 5 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_dense_enriched vs chunk500_hybrid_enriched | 4 | 0 | 1 | 3 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_bm25_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_dense_enriched | 4 | 0 | 0 | 4 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk200_hybrid_enriched vs chunk500_hybrid_enriched | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_dense_enriched | 2 | 0 | 0 | 2 | 0 | **untestable (no discordant pairs)** | n/a |
| C | ungrounded | chunk500_bm25_enriched vs chunk500_hybrid_enriched | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |
| C | ungrounded | chunk500_dense_enriched vs chunk500_hybrid_enriched | 3 | 0 | 1 | 2 | 1 | 1.000 | 1.000 |

Untestable (zero discordant pairs): **80 of 120** comparisons in this scope.
