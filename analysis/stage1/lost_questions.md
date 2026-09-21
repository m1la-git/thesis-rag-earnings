# The four questions `metadata_enriched` lost

`ref_comp_10`, `ref_fact_08`, `ref_them_06`, `ref_them_15` score non-zero in at
least one `text_only` condition and **zero in all six `metadata_enriched`**
conditions.

**Why the 200/500 split is diagnostic.** chunk200 truncates *nothing* under the
frozen P2 format (0 of 7918 chunks); chunk500 truncates 2985 of 3239, dropping a
mean of 9.4 tokens. So a loss that appears at chunk200 cannot be caused by missing
content — there is none missing — and implicates the ~19-token metadata prefix
changing what the retrievers rank. A loss confined to chunk500 is consistent with
truncation.

Tail membership below is computed with `analysis/truncation_tail.py`'s own logic.

## `ref_comp_10`

Scored non-zero in 1 of 6 `text_only` conditions. Loss locus: chunk500 only — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement**.

| text_only condition | coverage@5 |
|---|--:|
| chunk500_bm25 | 0.5 |

Per-anchor rank, matched condition vs its enriched counterpart (rank is within the 50-deep logged ranking; `>50` = not found at all):

| condition | anchor | text_only rank | enriched rank | in a truncated tail? |
|---|---|--:|--:|---|
| chunk500_bm25 | `Category 3 institution, we don't include AOCI in…` | 42 | 40 | no — fully inside the kept prefix |
| chunk500_bm25 | `book value per share, excluding AOCI, increased …` | 3 | 7 | no — fully inside the kept prefix |

## `ref_fact_08`

Scored non-zero in 1 of 6 `text_only` conditions. Loss locus: chunk500 only — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement**.

| text_only condition | coverage@5 |
|---|--:|
| chunk500_bm25 | 1.0 |

Per-anchor rank, matched condition vs its enriched counterpart (rank is within the 50-deep logged ranking; `>50` = not found at all):

| condition | anchor | text_only rank | enriched rank | in a truncated tail? |
|---|---|--:|--:|---|
| chunk500_bm25 | `BlackRock with an industry-leading $190 billion …` | 5 | 7 | no — fully inside the kept prefix |

## `ref_them_06`

Scored non-zero in 2 of 6 `text_only` conditions. Loss locus: both sizes — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement**.

| text_only condition | coverage@5 |
|---|--:|
| chunk200_hybrid | 0.5 |
| chunk500_hybrid | 0.5 |

Per-anchor rank, matched condition vs its enriched counterpart (rank is within the 50-deep logged ranking; `>50` = not found at all):

| condition | anchor | text_only rank | enriched rank | in a truncated tail? |
|---|---|--:|--:|---|
| chunk200_hybrid | `an adjusted efficiency ratio of 59% and a season…` | >50 | >50 | n/a (chunk200 truncates nothing) |
| chunk200_hybrid | `annual operating efficiency ratio, net of adjust…` | 3 | 11 | n/a (chunk200 truncates nothing) |
| chunk500_hybrid | `an adjusted efficiency ratio of 59% and a season…` | >50 | >50 | no matching chunk |
| chunk500_hybrid | `annual operating efficiency ratio, net of adjust…` | 2 | 14 | no — fully inside the kept prefix |

## `ref_them_15`

Scored non-zero in 1 of 6 `text_only` conditions. Loss locus: chunk200 only — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement**.

| text_only condition | coverage@5 |
|---|--:|
| chunk200_dense | 0.3333333333333333 |

Per-anchor rank, matched condition vs its enriched counterpart (rank is within the 50-deep logged ranking; `>50` = not found at all):

| condition | anchor | text_only rank | enriched rank | in a truncated tail? |
|---|---|--:|--:|---|
| chunk200_dense | `themes, technology spend was $3 billion in the q…` | 3 | 12 | n/a (chunk200 truncates nothing) |
| chunk200_dense | `increased our technology initiatives and expect …` | >50 | >50 | n/a (chunk200 truncates nothing) |
| chunk200_dense | `up 7% year-over-year, primarily due to the timin…` | >50 | >50 | n/a (chunk200 truncates nothing) |

## Summary

| question | non-zero text_only conditions | loss locus |
|---|--:|---|
| ref_comp_10 | 1/6 | chunk500 only — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement** |
| ref_fact_08 | 1/6 | chunk500 only — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement** |
| ref_them_06 | 2/6 | both sizes — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement** |
| ref_them_15 | 1/6 | chunk200 only — no anchor is in a discarded tail, so **not truncation**; the anchor's chunk fell out of the top-5 by rank: **prefix displacement** |

**None of the four is a truncation loss.** Every anchor involved sits fully inside
the kept prefix, including the chunk500 cases. In each question the anchor's chunk
was still found — it simply fell below rank 5 in the enriched index (3→7, 5→7,
3→11, 2→14, 3→12). These are rank-displacement losses: the metadata prefix changed
what outranked what, not what was available to match.
