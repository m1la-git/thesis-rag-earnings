# Claims map — every citable number, its source, and its population

**Every number below was read out of the artifact named beside it.** Where a
figure is not published as such but counted from an artifact's own table, it is
marked **derived**.

**How to use this.** Before writing a number, find it here, check the *arm*
column, and check the *twin* column. If a row has a twin, two different
populations share that number's name and quoting the wrong one is undetectable by
a reader.

**Arms.** `q8` = `qwen3.8-27b@q8_k_xl`, the reported generator — the only arm
whose Stage 2 numbers are thesis results. `flash` = `Qwen3.8-Flash-Next`,
robustness check. `q4` = `qwen3.8-27b@q4_k_xl`, validator baseline / development
history. `GI` = generator-independent (Stage 1 retrieval; identical under all
three arms because retrieval never calls a generator).

**Macros** are from `thesis/generated/macros.tex`. A blank means no macro exists.

---

## 0. Twins — read this section first

Places where one name covers two or more populations. These are the mistakes
that survive proofreading, because the sentence reads fine either way.

| # | name | population A | population B | why they differ |
|---|---|---|---|---|
| T1 | **Case C conversion** | **109/147 = 74.1%** — all 12 conditions pooled | **31/46 = 67%** — the six `text_only` conditions only | A is the full grid; B is what `stage2_statistics.md` §A3 publishes, computed before the enriched arm existed. `\thesisQeightCaseCConversion` is **A**. |
| T2 | **Case C conversion (again)** | **109/147** pooled | **24/38 → 29/38** matched intersection | The matched subset is only items in Case C under *both* arms. Different denominator, different question. |
| T3 | **Check 3 flagged rate** | full populations **10/31 = 32%** (text_only) vs **10/78 = 13%** (enriched) | Task 3 intersection **5/24 = 21%** vs **7/29 = 24%**; strictly matched **4/22 = 18%** vs **7/22 = 32%** | Three nested populations. The document says outright: **quote section 2, not section 1** — section 1 is a composition artifact. |
| T4 | **b (text_only-only wins)** | **observation level: b = 2** (q8), **b = 1** (flash) | **question level: b = 0** (both) | "No item converted under text_only but not enriched" is TRUE only at question level. |
| T5 | **agreement** | **498/540 = 92.2%** (q8 vs flash) | **525/540 = 97.2%** (q4 vs q8) | Different pairs of arms. Both live in files called `outcome_agreement.md`. |
| T6 | **comparative partial-coverage conversion** | pooled across arms **11/46 = 24%** (q8) | per-arm **3/18** text_only, **8/28** enriched | The pooled row mixes both arms. |
| T7 | **12** | **P1 pile n = 12** (company misattribution) | **I4 instrument finding n = 12** (faithful items carrying `offtarget`) | Coincidence of value: one is a generator behaviour, the other an instrument caution. 12 is also the number of **conditions**. Never write 12 without its noun. |
| T8 | **distractor displacement** | appears in `analysis/qwen3.8-27b_q8_k_xl/coverage_split.md` | **identical values** in `analysis/qwen3.8-flash-next/coverage_split.md` | It is a **retrieval** property, so it is generator-independent despite living in model-scoped files. Do not present it as an arm result. |
| T9 | **ungrounded, 9** | **9 = every `answered_ungrounded` record in the whole q8 grid** (a CENSUS) | **9 = the count in the 48-item review sample** | These are the same nine records — the packet captured all of them. So the manual finding is a census, not a sample estimate. Contrast `offtarget`: 17 sampled of 112, a genuine sample. |
| T10 | **"n"** | **45** questions — the benchmark and every Stage 2 count, since generation runs on all 45. **40** questions — the retrieval-scored set, because the 5 unanswerable items have no gold anchor and are dropped from the coverage@5 / MRR@5 denominator rather than scored as misses. | **480** observations — the descriptive-statistics table only: 40 × 12 conditions. | All three are correct in their own section. 45 → 40 is the unanswerable exclusion; 40 → 480 is crossing with the grid. Never "n = 45" beside a coverage figure, never "n = 40" beside a correlation. |
| T11 | **coverage@5 / MRR@5** | the **pooled** value — e.g. 0.408 at `chunk200_dense_enriched` — whose CSV column is named `overall_not_cross_category_comparable` | the **three per-category** values, e.g. that same condition is **0.786** factual, **0.089** thematic, **0.364** comparative | The pooled value is a weighted mix of ceilings that differ by a factor of nine. Do not quote a pooled figure beside a claim about a question type. Per-category numbers are in §2. |
| T12 | **abstentions** | **285** — records carrying the `abstained` outcome, which is what the classifier assigns and the case × outcome table shows | **284** — records matching the canonical sentence EXACTLY (`abstained_exact_match`) | The classifier uses the contains-rule, so 284 is a subset of 285; the difference is `chunk500_bm25/ref_comp_01`, which declines in its own words and then closes with the canonical sentence. **A third number: 286 responses contain the sentence once case is ignored**; the extra one, `chunk500_hybrid/ref_them_07`, states it after a connective in lowercase and is not labelled `abstained`. **286 present case-insensitively → 285 detected → 284 exact-match subset.** Never write "284 abstentions". |
| T13 | **inter-condition gap time** | **19.3 min = 27.1%** of wall clock — the sum of ALL 11 gaps, **Flash-Next** | **16.9 min = 23.8%** — the 3 largest gaps only, **Flash-Next** | 19.3 goes with 27.1%, 16.9 with 23.8%. Every arm's records carry `generated_at`, so timing exists for all arms, but the gap analysis in §10 was done for Flash-Next alone; name the arm with any gap figure. |
| T14 | **enrichment prefix cost** | **15–24 tokens, mean 19.3 at chunk\_size 200 and 19.4 at 500** — measured PER CHUNK (`truncation_tail.md`) | **mean 19.2** — PER DISTINCT PREFIX, over 128 strings | **The per-string 19.2 has NO artifact**; cite the per-chunk pair, labelled by chunk size. Never give a single unqualified "mean prefix cost". |
| T15 | **a bare question id** | **`chunk500_bm25/ref_comp_01`** — the one record caught by the contains-rule but not by exact equality (T12) | **`chunk200_dense_enriched/ref_comp_01`** — the one record labelled ungrounded through the empty-claims n-gram fallback; instrument finding **I3**, read as faithful | Same question id, different conditions, different mechanisms. Always name the condition with a question id. For `chunk500_hybrid/ref_them_07` name the arm too: it is missed by the case-sensitive test on q8 and caught on q4. That flip is a cross-arm comparison and does not belong in the thesis. |
| T16 | **coverage@5 × MRR@5 correlation** | **.85** — Pearson; the value the thesis quotes and `thesis/generated/table_descriptives.tex` prints (`analysis/stage1/descriptives.md`, main table) | **.98** — Spearman; the secondary table in the same file, labelled "reported for comparison only" | Two tables with identical layout and row labels in one file. With coverage@5 exactly zero on 69.4% of observations, the rank transform discards most of what separates the conditions. Of 45 coefficient cells, 16 differ and 3 change sign. **Quote the Pearson table only.** |
| T17 | **7, in Failure Modes and Answer Behaviour** | **the seven records Check 3 flagged** under metadata-enriched (7 of 29 converted; 7 of 22 converted under both) | **the seven observations converting under metadata-enriched alone** — the matched subset's c = 7 | Disjoint sets of the same size: the seven that converted under enriched alone are exactly the 29 − 22 the strict matching removes, and **none of them is flagged**. Reword neither sentence without the other. |
| T18 | **comparative conversion (again)** | **11/46 = 23.9%** at partial coverage, per arm 3/18 and 8/28 — `coverage_split.md` | **13/48 = 27.1%** over Case C entire, per arm 10/30 enriched — `abstention_rescore.md` | The second includes the two full-coverage observations. They agree on thematic (27/29) only because no thematic record reached full coverage. A third 13: 13 of 46 comparative partial-coverage observations were ANSWERED, against 13/48 CONVERTED. Name the artifact and the noun. |

---

## 1. Design and corpus — generator-independent

| number as written | artifact | macro | arm |
|---|---|---|---|
| 12 conditions | `configs/*.json` (13 minus `base.json`) | `\thesisNumConditions` | GI |
| 2 chunk sizes (200, 500) | `configs/` | `\thesisNumChunkSizes`, `\thesisChunkSizeSmall`, `\thesisChunkSizeLarge` | GI |
| 3 retrieval strategies | `configs/` | `\thesisNumStrategies` | GI |
| 2 indexing representations | `configs/` | `\thesisNumRepresentations` | GI |
| top-k = 5 | `configs/base.json` | `\thesisTopK` | GI |
| 45 questions | `benchmark/questions.jsonl` | `\thesisNumQuestions` | GI |
| 540 generations per arm | derived: 12 × 45, asserted against the outcomes table | `\thesisNumGenerations` | GI |
| 14 factual / 15 thematic / 11 comparative / 5 unanswerable | `benchmark/questions.jsonl` | `\thesisNumQuestions{Factual,Thematic,Comparative,Unanswerable}` | GI |
| 74 gold anchors | `benchmark/questions.jsonl` | `\thesisNumGoldAnchors` | GI |
| 128 transcripts | `data/corpus_manifest.json` | `\thesisNumTranscripts` | GI |
| `kurry/sp500_earnings_transcripts`, revision `f3ded372da8d` | `data/corpus_manifest.json` | `\thesisCorpusDataset`, `\thesisCorpusRevision` | GI |

---

## 2. Stage 1 — retrieval quality per condition (generator-independent)

Source: `results/tables/retrieval_metrics.csv`, rows where
`breakdown_type = overall_not_cross_category_comparable`. n = 40 scored for every
condition. Also rendered at `thesis/generated/table_retrieval_metrics.tex`.

> **The column name is a warning.** `overall_not_cross_category_comparable` pools
> categories with different achievable ceilings. Use the per-category breakdown
> (also in that CSV) for any cross-category claim.

| condition | anchor coverage@5 | MRR@5 |
|---|--:|--:|
| chunk200_bm25 | 0.125 | 0.064 |
| chunk200_dense | 0.083 | 0.043 |
| chunk200_hybrid | 0.163 | 0.090 |
| chunk500_bm25 | 0.138 | 0.074 |
| chunk500_dense | 0.113 | 0.073 |
| chunk500_hybrid | 0.138 | 0.109 |
| chunk200_bm25_enriched | 0.238 | 0.153 |
| chunk200_dense_enriched | **0.408** | 0.241 |
| chunk200_hybrid_enriched | 0.392 | **0.290** |
| chunk500_bm25_enriched | 0.200 | 0.077 |
| chunk500_dense_enriched | 0.375 | 0.290 |
| chunk500_hybrid_enriched | 0.363 | 0.260 |

### Descriptive statistics — `analysis/stage1/descriptives.md`

Source: `results/retrieval/*.jsonl` (per-question records). The generator
cross-checks its own condition means against all 24 CSV rows. Also rendered at
`thesis/generated/table_descriptives.tex`. Arm: GI.

**Unit: the question × condition pair. N = 480 = 40 × 12** (see **T10**).

| number as written | value | note |
|---|--:|---|
| Anchor coverage@5, M (SD) | **0.228 (0.371)** | pooled over all 480 observations |
| MRR@5, M (SD) | **0.147 (0.287)** | |
| Number of gold anchors, M (SD) | 1.850 (0.727) | range 1–3 |
| % of observations with coverage@5 = 0 | **69.4%** | identical for MRR@5 — MRR is zero exactly when no anchor matched |

Pearson correlations with the two outcomes (coverage@5, MRR@5):

| variable | r with coverage@5 | r with MRR@5 |
|---|--:|--:|
| Indexing: metadata-enriched | **.27** | **.25** |
| Chunk size (500 vs. 200) | **−.02** | **.00** |
| Retrieval strategy: BM25 | −.10 | −.14 |
| Retrieval strategy: hybrid | .07 | .10 |
| Question category: thematic | −.31 | −.28 |
| Question category: comparative | −.06 | −.06 |
| Number of gold anchors | **−.41** | −.36 |
| Chunk-size-sensitive anchor | .03 | −.02 |
| coverage@5 × MRR@5 | — | **.85** |

> **Three cautions travel with every number above.**
>
> 1. **No significance markers, deliberately.** The 480 observations are nested
>    (12 per question, 40 per condition), so the independence assumption behind a
>    correlation's significance test does not hold. These are **descriptive of
>    this sample rather than confirmatory**.
> 2. **A dummy contrasts its level with all others pooled**, not with the
>    reference level. "BM25 r = −.10" is BM25 against dense-and-hybrid together.
> 3. **The design factors' mutual correlations are exactly .00** — the grid is
>    balanced and fully crossed. The lone −.50 between BM25 and hybrid is
>    structural (two dummies from one three-level factor), not a finding.

**The anchor-count row is a property of the benchmark, not noise.** Factual asks
for one figure and carries one anchor, comparative carries one anchor per
company, thematic carries two or three. Hence r = .73 between anchor count and
the thematic dummy, and `n_transcript_ids` **equals** the anchor count on all 40
questions. Read −.41 as "questions that require more evidence are retrieved
against less completely".

### Stage 1 Holm families — `analysis/stage1/stage1_statistics_12cond.md`

Three families, each corrected separately, each per metric.

| claim | number | artifact | arm |
|---|---|---|---|
| Family 1 (representation), 6 matched pairs, pooled n=40 | 6 testable of 6, per metric | `stage1_statistics_12cond.md` §Family 1 | GI |
| `chunk200_dense_enriched vs chunk200_dense`, coverage | p raw 0.000, **p Holm 0.001**, r −0.862 | same | GI |
| `chunk500_dense_enriched vs chunk500_dense`, coverage | p Holm 0.006, r −0.883 | same | GI |
| `chunk200_hybrid_enriched vs chunk200_hybrid`, coverage | p Holm 0.009, r −0.824 | same | GI |
| `chunk500_hybrid_enriched vs chunk500_hybrid`, coverage | p Holm 0.010, r −0.763 | same | GI |
| the two BM25 pairs, coverage | p Holm 0.075 and 0.248 — **not significant** | same | GI |
| Family 2 (size × strategy within `text_only`), 15 pairs | 15 testable of 15; **every Holm p ≥ 0.651**, most 1.000 | `stage1_statistics_12cond.md` §Family 2 | GI |
| Family 3 (size × strategy within `metadata_enriched`), 15 pairs | see the MRR rows below — **this family is NOT a clean null** | `stage1_statistics_12cond.md` §Family 3 | GI |

**The table above is `anchor_coverage_at_5` only.** MRR@5 is corrected as its own
family and does not give the same answer:

| family | metric | pairs with Holm p < .05 | min Holm p |
|---|---|--:|--:|
| 1 — representation | coverage@5 | **4 of 6** | 0.001 |
| 1 — representation | MRR@5 | **5 of 6** | 0.003 |
| 2 — size × strategy, `text_only` | coverage@5 | 0 of 15 | 0.651 |
| 2 — size × strategy, `text_only` | MRR@5 | 0 of 15 | 0.225 |
| 3 — size × strategy, `metadata_enriched` | coverage@5 | 0 of 15 | **0.051** |
| 3 — size × strategy, `metadata_enriched` | MRR@5 | **3 of 15** | 0.004 |

Two points to state precisely:

1. **BM25 is metric-dependent.** On MRR@5, `chunk200_bm25_enriched vs
   chunk200_bm25` **is** significant (raw 0.024, **Holm 0.049**). BM25 at 200
   tokens is unmoved on coverage and moved on MRR — enrichment reordered its top
   5 without pulling in more anchors. Say which metric whenever the BM25 claim is
   made.
2. **Strategy is not null within `metadata_enriched`.** Family 3 has three
   significant MRR@5 pairs, and **all three involve `chunk500_bm25_enriched`**,
   the weakest enriched cell:

   | pair | raw | Holm | isolates |
   |---|--:|--:|---|
   | `chunk500_bm25_enriched` vs `chunk500_hybrid_enriched` | 0.000 | **0.004** | strategy (size held at 500) |
   | `chunk200_hybrid_enriched` vs `chunk500_bm25_enriched` | 0.000 | **0.006** | **nothing — differs on size AND strategy** |
   | `chunk500_bm25_enriched` vs `chunk500_dense_enriched` | 0.002 | **0.032** | strategy (size held at 500) |

   **Two clean strategy contrasts and one confounded pair.** All three are
   POOLED results and reproduce in no single category (min Holm p 0.071 factual,
   0.950 thematic, 1.000 comparative).

**Reading.** Enrichment moves coverage@5 for dense and hybrid at both chunk
sizes, and moves MRR@5 for those four plus BM25 at 200 tokens. **Chunk size moves
nothing anywhere** — no pair differing only in chunk size is significant in any
family, on either metric. **Strategy moves nothing within `text_only`, but within
`metadata_enriched` BM25 at 500 tokens is significantly worse than both dense and
hybrid on MRR@5.** Family 3's coverage min Holm p = 0.051 is a near miss and
should be reported as one rather than rounded either way.

### Per-category Stage 1

Source: `results/tables/retrieval_metrics.csv`, rows where `breakdown_type =
category`, and the per-category blocks of `stage1_statistics_12cond.md`. **n is
14 factual / 15 thematic / 11 comparative**, summing to the 40 retrieval-scored
questions (T10).

| condition | fact cov | fact MRR | them cov | them MRR | comp cov | comp MRR |
|---|--:|--:|--:|--:|--:|--:|
| chunk200_bm25 | 0.214 | 0.110 | 0.067 | 0.019 | 0.091 | 0.068 |
| chunk200_dense | 0.143 | 0.086 | 0.056 | 0.024 | 0.045 | 0.015 |
| chunk200_hybrid | 0.286 | 0.171 | 0.067 | 0.044 | 0.136 | 0.049 |
| chunk500_bm25 | 0.214 | 0.121 | 0.033 | 0.011 | 0.182 | 0.098 |
| chunk500_dense | 0.071 | 0.024 | 0.100 | 0.078 | 0.182 | 0.129 |
| chunk500_hybrid | 0.143 | 0.107 | 0.100 | 0.083 | 0.182 | 0.145 |
| chunk200_bm25_enriched | 0.500 | 0.342 | 0.033 | 0.008 | 0.182 | 0.111 |
| chunk200_dense_enriched | **0.786** | 0.476 | 0.089 | 0.056 | **0.364** | **0.193** |
| chunk200_hybrid_enriched | **0.786** | **0.655** | 0.111 | 0.036 | 0.273 | 0.172 |
| chunk500_bm25_enriched | 0.429 | 0.146 | 0.033 | 0.011 | 0.136 | 0.080 |
| chunk500_dense_enriched | 0.714 | 0.619 | **0.133** | 0.063 | 0.273 | 0.180 |
| chunk500_hybrid_enriched | 0.714 | 0.517 | **0.133** | **0.092** | 0.227 | 0.163 |

**The ranges, which is what the pooled column hides.** Factual coverage runs
0.071–0.286 under `text_only` and 0.429–0.786 under `metadata_enriched`.
Thematic runs 0.033–0.100 and 0.033–0.133 — **both arms sit near floor.**
Comparative runs 0.045–0.182 and 0.136–0.364.

#### The enrichment effect is concentrated in factual questions

Family 1 (representation, 6 matched pairs, corrected within each category block
and within each metric):

| category | metric | Holm p < .05 | testable | min Holm p |
|---|---|--:|--:|--:|
| factual (n=14) | coverage@5 | **4 of 6** | 6 | 0.016 |
| factual (n=14) | MRR@5 | **4 of 6** | 6 | 0.021 |
| thematic (n=15) | coverage@5 | 0 | 5 | 1.000 |
| thematic (n=15) | MRR@5 | 0 | 5 | 0.899 |
| comparative (n=11) | coverage@5 | 0 | 6 | 0.188 |
| comparative (n=11) | MRR@5 | 0 | 6 | 0.094 |

The four significant factual pairs are **the same four in both metrics** — dense
and hybrid at both chunk sizes — and the same four that carry the pooled
coverage result. Holm p 0.016–0.024 (coverage) and 0.021–0.048 (MRR). The two
BM25 pairs are not significant in factual either.

**Read the three categories differently:**

1. **Factual — present.** Significant on both metrics at n = 14, and the
   largest effect in the study: coverage roughly triples.
2. **Thematic — no detectable movement, and both arms sit near floor.** Raw p's
   are 0.317–1.000 (coverage) and 0.180–1.000 (MRR), and
   `chunk500_bm25_enriched vs chunk500_bm25` has **no discordant pairs at all**.
   This is a **floor effect, not evidence that identity metadata is irrelevant to
   thematic retrieval.** Do not write "metadata does not help thematic
   questions."
3. **Comparative — suggestive, not established.**
   `chunk200_dense_enriched vs chunk200_dense` is raw p 0.031 (coverage) and
   **0.016** (MRR); `chunk200_hybrid_enriched vs chunk200_hybrid` is raw 0.031
   (MRR). All are removed by Holm at family size 6 with n = 11. Report the raw
   p's *with* the correction that removes them, or not at all.

**Families 2 and 3 are null in every category.** Family 2: min Holm p = 1.000 in
all six category × metric blocks. Family 3: min Holm p 0.355 / 0.071 (factual
cov / MRR), 1.000 / 0.950 (thematic), 1.000 / 1.000 (comparative). So Family 3's
three pooled MRR@5 pairs are a **pooled** finding only; do not restate any of
them about a category.

**The mechanism is post hoc.** A factual question names one company and asks for
one figure, so company identity is exactly the discriminator the prefix
supplies; a thematic question names no company. That reading is **descriptive
of this sample rather than confirmatory**. The per-category blocks came out of
the same Stage 1 run as the pooled ones, but the category split was not
pre-specified as a test of H3, and nothing in this project was pre-registered.

#### `chunk_size_sensitive` breakdown

7 questions whose source sentence is whole in one chunk at 500 tokens but split
at 200; 33 others. Mechanically defined.

| condition | sens cov | sens MRR | rest cov | rest MRR |
|---|--:|--:|--:|--:|
| chunk200_bm25 | 0.214 | 0.046 | 0.106 | 0.068 |
| chunk200_dense | 0.262 | 0.194 | 0.045 | 0.011 |
| chunk200_hybrid | 0.357 | 0.243 | 0.121 | 0.058 |
| chunk500_bm25 | **0.000** | **0.000** | 0.167 | 0.089 |
| chunk500_dense | 0.071 | 0.071 | 0.121 | 0.073 |
| chunk500_hybrid | 0.214 | 0.143 | 0.121 | 0.102 |
| chunk200_bm25_enriched | 0.143 | 0.036 | 0.258 | 0.178 |
| chunk200_dense_enriched | 0.429 | 0.161 | 0.404 | 0.258 |
| chunk200_hybrid_enriched | 0.429 | 0.173 | 0.384 | 0.315 |
| chunk500_bm25_enriched | 0.214 | 0.046 | 0.197 | 0.084 |
| chunk500_dense_enriched | 0.357 | 0.226 | 0.379 | 0.303 |
| chunk500_hybrid_enriched | 0.286 | 0.238 | 0.379 | 0.265 |

**The 0.000 was verified per record.** Under `chunk500_bm25` all 7 sensitive
items score zero because their anchors are either unmatched or matched *below
rank 5* — ranks 6, 10, 18, 32 and 33 in the five items that match at all. Two
cross that boundary relative to `chunk200_bm25`: `ref_fact_01` rank 5 → 10,
`ref_them_04` rank 4 → 6. Enrichment recovers it (0.214 at
`chunk500_bm25_enriched`). **No significance test was run on this subgroup**;
n = 7 is a descriptive split.

---

### Exact-test sensitivity — `analysis/stage1/exact_sensitivity.md`

Appendix, Statistical Implementation. Every Stage 1 comparison recomputed with an
exact sign-flip permutation of the signed-rank statistic (midranks, zeros
dropped), Holm-adjusted in the same family × scope × metric blocks. The script
reproduces every stored raw and Holm p before computing anything.

| claim | value | macro |
|---|---|---|
| results significant under the reported test | **20** | `ExactNumSigReported` |
| of those, significant under the exact test | **20 — none lost** (asserted in the builder) | — |
| BM25, 200, MRR@5, Family 1 pooled: Holm p | **.049 reported → .043 exact** | `ExactBmSmallMrrHolmReported`, `…Exact` |
| comparisons significant only under the exact test | **3**, all two-factor pairs (size and strategy), which isolate neither factor | `ExactNumSigGained` |

**Twin warning.** One of the three gained comparisons is Family 3 factual MRR@5,
chunk200_hybrid_enriched vs chunk500_bm25_enriched: Table 3 Panel C prints its
reported Holm p, **.071**, as that block's minimum; exact it is **.029**. Results'
"Families 2 and 3 were null in every category block" is true of the REPORTED
test only. Never quote an exact-test value as a thesis result: the thesis
reports the scipy test, and this is a sensitivity check on it.

## 3. Stage 2 — case partition and case × outcome

The **case partition is byte-identical across all three arms** (A 60 / B 333 /
C 147), as it must be — cases come from Stage 1.
Source: `results/tables/<arm>/generation_outcomes.csv`.

| number | q8 (REPORTED) | flash (robustness) | q4 (dev) | macro (q8) |
|---|--:|--:|--:|---|
| Case A | 60 | 60 | 60 | `\thesisQeightCaseA` |
| Case B | 333 | 333 | 333 | `\thesisQeightCaseB` |
| Case C | 147 | 147 | 147 | `\thesisQeightCaseC` |

### Case × outcome, all 12 conditions pooled

**q8 — the reported arm.** Source: `results/tables/qwen3.8-27b_q8_k_xl/generation_outcomes.csv`

| case | abstained | grounded_correct | grounded_offtarget | ungrounded | n |
|---|--:|--:|--:|--:|--:|
| A | 55 | 0 | 1 | 4 | 60 |
| B | 195 | 25 | 109 | 4 | 333 |
| C | 35 | 109 | 2 | 1 | 147 |
| **total** | **285** | **134** | **112** | **9** | **540** |

**flash — robustness check, NOT a thesis result.**

| case | abstained | grounded_correct | grounded_offtarget | ungrounded | n |
|---|--:|--:|--:|--:|--:|
| A | 60 | 0 | 0 | 0 | 60 |
| B | 193 | 26 | 107 | 7 | 333 |
| C | 33 | 113 | 1 | 0 | 147 |
| **total** | **286** | **139** | **108** | **7** | **540** |

Column totals and per-case cells all have macros, e.g. `\thesisQeightAbstained`
(285), `\thesisQeightCaseBAnsweredGroundedOfftarget` (109), and the q4 and
`\thesisFlashRobustness…` equivalents.

| claim | number | artifact | arm | twin |
|---|---|---|---|---|
| Case A abstention | **55/60** | outcomes CSV | q8 | vs flash **60/60** |
| Case C conversion, 12-cond pooled | **109/147 = 74.1%** | outcomes CSV | q8 | **T1, T2** |
| Case C conversion, 12-cond pooled | 113/147 = 76.9% | outcomes CSV | flash | **T1, T2** |
| Case C conversion, six `text_only` conditions | **31/46 = 67%** | `qwen3.8-27b_q8_k_xl/stage2_statistics.md` §A3 | q8 | **T1** |
| Case B correct-abstention rate | **126/194 = 65%** (61–69% across conditions) | same §A3 | q8 | six-condition population |
| "35% of retrieval failures are answered rather than declined" | complement of the above | same §A3 | q8 | six-condition population |

### A1 / A5 — the null result and its power caveat

| claim | number | artifact | arm |
|---|---|---|---|
| A1: pairwise outcome tests | **120 tests, 65 testable, 0 significant after Holm** | `stage2_statistics.md` §A1 | q8 |
| 55 untestable because both conditions gave identical outcomes on every matched question | 55 of 120 | §A1, §A5 | q8 |
| A1's own minima | raw **0.2188**, every Holm-adjusted value **1.0000** | §A1 | q8 |
| A2 minima (chunk-size main effect; strategy family) | raw **0.084**, Holm **0.307** | §A2 | q8 |
| Case B matched n per pair | 26–31 | §A5 | q8 |
| Case C matched n per pair | **1–6** — nothing testable at that size | §A5 | q8 |
| 12-condition extension | **415 of 1152 comparisons testable, min raw p 0.125, min Holm p 0.750, 0 significant at either level** | `stage2_statistics_12cond.md` | q8 |

> **Keep the two documents' figures apart.** 0.084 and 0.307 are A2's, from
> `stage2_statistics.md`; they belong neither beside A1's count of 120 nor beside
> the 12-condition count of 415. That document's own summary line
> (`stage2_statistics.md:244–245`) pairs A1's count with A2's minima; quote the
> tables, not that line.
>
> §A5 states the rule for reporting this: **a null result with the power caveat
> attached, never evidence of equivalence.**

### Why there is no Stage 2 hypothesis

There is no H4. The thesis states three hypotheses, H1–H3, one per manipulated
factor, and treats Stage 2 as **Answer Behaviour** — described, not tested. From
`analysis/qwen3.8-27b_q8_k_xl/stage2_statistics_12cond.csv`, 1152
per-comparison rows:

| figure | value |
|---|---|
| comparisons testable | **415 of 1152** (737 have no discordant pair) |
| minimum raw p | **0.125** |
| minimum Holm-adjusted p | **0.750** |
| comparisons below .05 | **0 raw, 0 Holm** |

The exact test's granularity floor is a property of the design; how many
comparisons have no discordant pair is an observed property of these data. Keep
them apart. The measured basis:

- **Untestable in aggregate: 737 of 1152 (64%).** In every POOLED scope it is
  fewer than half: Family 1 17/48 (35%), Family 2 55/120 (46%), Family 3 42/120
  (35%). The aggregate majority comes from the per-category scopes (Family 3
  factual is 120/120). Any "most" must name the full grid.
- **Of the 415 testable comparisons, 402 have at most 5 discordant pairs**
  (1: 203, 2: 103, 3: 44, 4: 34, 5: 18; 6: 10, 7: 3; maximum 7). At n ≤ 5 the
  exact two-sided floor is ≥ 0.0625, so no *p* below .05 was attainable for 402
  of 415 whatever the split.

### Attainability

`analysis/stage1/attainability_stage1.md` and
`analysis/qwen3.8-27b_q8_k_xl/attainability_stage2.md` (both from
`analysis/attainability.py`) give, for each comparison, the smallest *p* the
test could have returned with only the direction of each difference free. It is
stated before correction, since Holm attainability depends on the rest of each
family.

- **Pooled Stage 1: 71 of 72** comparisons could have reached p < .05. The one
  that could not is Family 2 coverage@5 `chunk200_bm25` vs `chunk200_hybrid`
  (n≠0 = 4, smallest attainable 0.0588).
- **Stage 2: 13 of 415** testable comparisons could have reached p < .05.
- **Per-category Stage 1: 58 of 210** testable comparisons could have; in
  Family 2's thematic and comparative scopes, none of 59. **H1's per-category
  size-only comparisons: 10 of 35 testable** (Family 2 3 of 18, Family 3 7 of
  17; one untestable), while all 12 pooled ones could. A null in a scope where
  nothing could have rejected is not additional evidence.
- **Family 1 comparative: every comparison that could reject, did.** 3 of 12
  have a smallest attainable uncorrected *p* below .05 —
  `chunk200_dense_enriched` on coverage@5 (n≠0 = 6, floor 0.03125) and MRR@5
  (n≠0 = 7, floor 0.015625), and `chunk200_hybrid_enriched` on MRR@5 (n≠0 = 6,
  floor 0.03125) — and all three returned exactly their floor: 0.031, 0.016,
  0.031. Holm at family size six removes all three.

---

## 4. Matched subset and question-level McNemar

Source: `analysis/<arm>/matched_conversion.md`. Intersection = items in Case C
under *both* arms. **No macros.**

| number | q8 | flash | twin |
|---|--:|--:|---|
| intersection n | 38 | 38 | **T2** |
| conversion, text_only → enriched | 24/38 → 29/38 | 23/38 → 33/38 | **T2** |
| observation level: b / c / concordant / n disc | 2 / 7 / 29 / 9 | 1 / 11 / 26 / 12 | **T4** |
| observation-level p (exact) | 0.1797 | **0.0063** | anti-conservative — see below |
| question level: questions / b / c / concordant | 13 / 0 / 2 / 11 | 13 / 0 / 3 / 10 | **T4** |
| question-level p (exact) | **0.5000** | **0.2500** | |
| comparative, observation level | b 1, c 7, p 0.0703 | b 0, c 11, p 0.0010 | |
| comparative, question level | b 0, c 2, p 0.5000 | b 0, c 3, p 0.2500 | |
| newly-entered set (enriched only) | 63 items, 49 correct, **77.8%** | 63 items, 50 correct, **79.4%** | single-arm by construction |
| lost set (text_only only) | 8 items, 7 correct, 87.5% | 8, 7, 87.5% | |

> **Quote the question-level test, not the observation-level one.** 38
> observations come from 13 questions, so the observation-level binomial treats
> correlated observations as independent trials. **Neither arm is significant at
> question level.** Flash's observation-level p = 0.0063 is the clearest trap in
> this table.

**Known issue in the artifact.** `analysis/matched_conversion.py` writes, as
fixed prose into every arm's `matched_conversion.md`, the heading "Specified
after the descriptive result was seen" and the phrase "not pre-registered
comparisons". That is true of the development arm only: the script predates the
reported arm's grid. Left as generated; fix the heading ("not pre-specified")
the next time the script is edited.

---

## 5. Coverage split — conjunctive vs disjunctive

Source: `analysis/<arm>/coverage_split.md`. **No macros. No validation surface.**

| number | q8 | flash | twin |
|---|--:|--:|---|
| thematic, partial coverage — conversion | **27/29 = 93%** | 27/29 = 93% | identical rate, different composition |
| — text_only | 13 items: 0 abstained, 13 correct | 13: 0 abstained, 13 correct | |
| — enriched | 16: 1 abstained, 14 correct, 1 offtarget | 16: 2 abstained, 14 correct | |
| comparative, partial coverage — conversion | **11/46 = 24%** | 14/46 = 30% | **T6** |
| — text_only | 18: 15 abstained, 3 correct | 18: 16 abstained, 2 correct | **T6** |
| — enriched | 28: 18 abstained, 8 correct, 1 offtarget, 1 ungrounded | 28: 15 abstained, 12 correct, 1 offtarget | **T6** |
| comparative, full coverage — conversion | 2/2 = 100% ⚠ (n=2) | 2/2 ⚠ | n=2, do not lean on it |
| full − partial difference, comparative | **+76%** | +70% | |
| distractor displacement, company-level | text_only 0.72 → enriched 0.30 (−0.42) | **identical** | **T8** — retrieval property |
| distractor displacement, transcript-level | text_only 3.78 → enriched 2.60 (−1.18) | **identical** | **T8** |

**Distractor displacement, scope.** Population: the 48 comparative Case C
observations, 18 `text_only` and 30 `metadata_enriched` — not the grid, not all
Case C. The section is byte-identical in the q4, q8 and Flash-Next
`coverage_split.md` files. The company-level **median is 0 in both arms**, so the
0.42 mean difference moves on a minority of observations; the transcript-level
figure (1.18 of 5 slots) is the larger movement and the one that would carry a
displacement claim. Neither was tested. The thesis does not report it.

---

## 6. Check 3 — attribution exposure

Source: `analysis/qwen3.8-27b_q8_k_xl/check3_enriched.md`. **No macros.**
All three populations are **lower bounds** — see §7.

| population | text_only | metadata_enriched | twin |
|---|---|---|---|
| §1 full populations | 10/31 = **32%** | 10/78 = **13%** | **T3** — a composition artifact, **NOT a finding** |
| §2 Task 3 intersection (Case C in both) | 5/24 = **21%** | 7/29 = **24%** | **T3** — *"quote section 2, not this table"* |
| §2b strictly matched (`correct` in both) | 4/22 = **18%** | 7/22 = **32%** | **T3** — the only fully paired comparison; **no evidence either way** at n=22 |

---

## 7. Failure taxonomy P1–P4 (manual review, q8 only)

Source: `analysis/qwen3.8-27b_q8_k_xl/manual_review_second_pass.md` §2, §3b.
48 items, 25 distinct questions, 12 conditions. **23 items carry a pile; 25 carry
none.** **No macros.**

| pile | behaviour | n | twin |
|---|---|--:|---|
| P1 | gives one company's material under another's name | **12** | **T7** |
| P2 | declines the whole when it holds one side | 8 | |
| P3 | dates material to a period it doesn't come from | 3 | |
| P4 | answers outside the asked window, but says so | 2 | |

Items 13 and 28 sit in two piles each, so the piles sum to 25 assignments over 23 items.

**Cross-tabs** (observations, not questions — these do not support a
significance claim):

| pile | text_only | enriched | | factual | thematic | comparative | unanswerable | | A | B | C |
|---|--:|--:|---|--:|--:|--:|--:|---|--:|--:|--:|
| P1 | 8 | 4 | | 0 | 6 | 1 | 5 | | 5 | 5 | 2 |
| P2 | 3 | 5 | | 0 | 0 | 8 | 0 | | 0 | 0 | 8 |
| P3 | 1 | 2 | | 0 | 3 | 0 | 0 | | 0 | 1 | 2 |
| P4 | 0 | 2 | | 0 | 1 | 1 | 0 | | 0 | 1 | 1 |

> **P1 spans all three cases; Check 3 sees only 2 of its 12.** Check 3's
> population is Case C `answered_grounded_correct` only, so P1's Case A (5) and
> Case B (5) instances are invisible to it by construction. **Report every Check 3
> figure as a floor, never as a measurement.**

---

## 8. Instrument findings I1–I6 (a separate axis from the piles)

Same source, §2b. Claims about the **scorer or benchmark**, not the generator.

| id | finding | n | twin |
|---|---|--:|---|
| I1 | a correctly-read date is checked as a figure | 2 | |
| I2 | transparently-marked arithmetic counts as ungrounded | 1 | |
| I3 | n-gram fallback can't see a paraphrase that doesn't copy | 1 | |
| I4 | `offtarget` reflects transcript targeting, not the answer | **12** | **T7** |
| I5 | gold anchor doesn't answer its own question (`ref_fact_14`) | 1 | |
| I6 | identical failure gets two different labels | 1 | |

> **I4 is a sample statement:** 12 of the 48 reviewed items read as faithful yet
> carry `offtarget`. The grid holds **112** offtarget records and only **17**
> were reviewed, so this is 12/17 of the sampled offtarget items — **do not
> extrapolate it to a rate over the 112.**

### The ungrounded census — a CENSUS, not a sample

**Derived** by counting `manual_review_second_pass.md` §3 against
`results/tables/qwen3.8-27b_q8_k_xl/generation_outcomes.csv`. The reported arm
contains **9** `answered_ungrounded` records in total, and the review packet
contains **all 9** — an exact set match.

| claim | number | twin |
|---|---|---|
| `answered_ungrounded` records in the whole q8 grid | **9** | **T9** |
| of those, read as **faithful** on manual inspection | **4 of 9 (44%)** | **T9** |
| — items 10, 17 (`ref_them_15`, `ref_them_12`) | I1 — a date verified as a figure | |
| — item 29 (`ref_them_09`) | I2 — the model's own flagged arithmetic | |
| — item 40 (`ref_comp_01`) | I3 — faithful paraphrase, no shared 6-gram | |
| read as "should have abstained" | 4 of 9 (all `ref_unans_01`, pile P1) | |
| read as unfaithful | 1 of 9 (item 28) | |

Nearly half of the reported arm's entire `answered_ungrounded` population is
faithful text mislabelled by documented instrument limitations of two kinds:
I1, a traced defect in the classifier, and I2 and I3, the conservative proxy
behaving as specified.

---

## 9. Manual review packet — sampling strata

Source: `analysis/qwen3.8-27b_q8_k_xl/manual_review_packet_manifest.csv`
(48 rows). Seeded mechanical rule, seed `20260906`. **No macros.**

| stratum | n | | facet | breakdown |
|---|--:|---|---|---|
| S1 | 10 | | arm | enriched 29, text_only 19 |
| S2 | 16 | | category | thematic 25, comparative 13, factual 5, unanswerable 5 |
| S3 | 10 | | case | C 23, B 20, A 5 |
| S4 | 8 | | outcome | offtarget 17, correct 12, abstained 10, ungrounded 9 |
| S5 | 4 | | check3_flagged | True 8, False 4, n/a 36 |

> The packet is **stratified, not random**. Any rate computed on it is a rate
> within a stratified sample, except `answered_ungrounded`, which is a census
> (§8). Its strata are defined on the reported arm's own outcome labels
> (`manual_review_packet.build_frames`): S1 every `answered_ungrounded` record
> plus the Case A offtarget one, S2 `offtarget`, S3 Case C `abstained`, S4/S5
> Case C `correct` split on the Check 3 flag. A stratum defined on an observed
> label cannot precede the observation, so the sampling design is definitional.

---

## 10. Cross-arm outcome agreement

Source: `analysis/<comparison arm>/outcome_agreement.md`. **No macros.
No validation surface.**

| comparison | agree | disagree | artifact | twin |
|---|---|---|---|---|
| **q8 vs Flash-Next** | **498/540 = 92.2%** | 42 (7.8%) | `qwen3.8-flash-next/outcome_agreement.md` | **T5** |
| q4 vs q8 | 525/540 = 97.2% | 15 (2.8%) | `qwen3.8-27b_q8_k_xl/outcome_agreement.md` | **T5** |

**q8 vs Flash-Next, disagreements** — by category: factual 1/168 (0.6%),
thematic 24/180 (13.3%), comparative 12/132 (9.1%), unanswerable 5/60 (8.3%).
By case: A 5/60, B 27/333, C 10/147.

> **Only 37 of the 42 are informative.** All 5 unanswerable disagreements come
> from `ref_unans_01` and are predetermined by Flash-Next naming no companies,
> which makes P1 structurally impossible for it.

**q4 vs q8, disagreements** — by category: factual 0/168, thematic 11/180 (6.1%),
comparative 4/132 (3.0%), unanswerable 0/60. By case: A 0, B 9/333, C 6/147.

The q4 comparison is not reported in the thesis, which makes no cross-arm
comparison of the two 27B builds.

### Run timing — Flash-Next only

Derived from the 540 `generated_at` stamps in
`results/generation/qwen3.8-flash-next/`; no published timing artifact and no
macro. **Never attach these to the reported q8 arm or to Stage 1.** See **T13**.

| quantity | value | share of wall clock |
|---|--:|--:|
| wall clock, first to last record | 4263 s = **71.0 min** | — |
| sum of within-condition spans | 3107 s = 51.8 min | 72.9% |
| sum of 11 inter-condition gaps | 1156 s = **19.3 min** | **27.1%** |
| the 3 largest gaps only | 1016 s = **16.9 min** | **23.8%** |

**The three large gaps are index rebuilds.** Every gap that changes only the
retrieval strategy is 10–26 s (8 of 11); every gap that changes the indexing
representation is 304–361 s (3 of 11), because dense and BM25 indexes must be
rebuilt when the indexed string changes but not when the ranker changes:

| gap | what changed | seconds |
|---|---|--:|
| `chunk200_hybrid_enriched` → `chunk200_bm25` | repr + strategy | 304 |
| `chunk200_hybrid` → `chunk500_bm25_enriched` | size + repr + strategy | 361 |
| `chunk500_hybrid_enriched` → `chunk500_bm25` | repr + strategy | 351 |
| the other 8 | strategy only | 10–26 |

A cost observation about the robustness run, not a measurement of the pipeline:
no timer was run and the gaps include process startup.

---

## 11. Unsourced — do not cite until an artifact exists

| wanted | status |
|---|---|
| a published "ungrounded census" | **does not exist** as an artifact. §8 is derived by counting two artifacts against each other. |
| P1–P4 counts or any manual review for Flash-Next | **do not exist by design** — the pile taxonomy is derived from q8 answer text and does not transfer. |
| Flash-Next Check 3 / attribution figures | **not computed.** |
| answer-similarity figures | computed (`stage2_statistics.md` §A4, Case C answered rows, 112 of 540 records) but supports no test and no comparison; the thesis does not mention it. |
| any analysis keyed on `difficulty_level` | **the coding rule is not operationally documented** (`benchmark_process.md` Rule 6 gives the principle but no metric or cut-points). The field is usable as an annotation, not as a measure, and its distribution is disputed (`benchmark_process.md` §10.6). **Cite no difficulty distribution.** |
| truncation exposure, ticker collision, lost questions | in `analysis/stage1/truncation_tail.md`, `ticker_collision.md`, `lost_questions.md`; not extracted here. |

---

## 12. Standing cautions that travel with these numbers

1. **`answered_grounded_offtarget` is not an answer-quality label** (I4). It says
   no supporting chunk belonged to the question's own `transcript_ids`. Report it
   as a retrieval-targeting count.
2. **Grounding is a verbatim-substring proxy**, deliberately conservative. **I2
   and I3 are two measured instances of it behaving as specified; I1 is a traced
   defect in the classifier**, reported and not fixed. Together they account for
   4 of the arm's 9 ungrounded labels (§8).
3. **`evaluate.is_bertscore_scored` is named for a metric that is not the one
   computed.** The answer-similarity measure is a **cosine over
   `bge-small-en-v1.5`** (`configs/base.json`: `similarity_metric:
   cosine_bge_small`); the output column is `bertscore_cosine` for the same
   reason. BERTScore was never used; do not cite it. The name is left unchanged
   because the function sits on a frozen scoring path.
4. **`manual_review_packet.allocate`'s docstring disagrees with its code.** It
   says a floor seat is paid for "out of the largest cell"; the code deducts from
   the cell holding the most currently-allocated seats, ties broken toward the
   more populous cell. **The code is authoritative**; any description of the
   allocation must describe the code.
5. **The abstention detector is case-sensitive, and one record in 540 falls
   through it** (README, "Scorer fixes and known defects"). Numbers: **T12**.
   Ambiguous id: **T15**.
6. **`{infix}CaseAAbstentions` and `{infix}CaseAAbstained` are one letter apart
   and emit different nouns.** `CaseAAbstentions` emits a **fraction** (`55/60`
   on both 27B arms, `60/60` on Flash-Next); `CaseAAbstained` emits a **count**
   (`55`, `55`, `60`). If you cite either, put the noun in the sentence.
7. **Q&A is under-represented among gold anchors, so no claim about section
   effects is made.** `benchmark/benchmark_process.md` §10.2 records the Q&A
   share falling from 22% to 13% as the anchoring rules accumulated, because
   conversational speech resists clean anchoring.
8. **Every Check 3 figure is a lower bound**, because its population is Case C
   `answered_grounded_correct` only.
9. **Nothing from `q4` or `Flash-Next` is a thesis result.** q4 is the validator
   baseline; Flash-Next is a robustness check whose confounds (architecture,
   parameter count, attention design, n-gram table, KV cache precision) are
   deliberate and unresolvable — attribute no difference to any single one.
10. **Stage 1 is generator-independent.** Never present a retrieval number as
    belonging to an arm, including the distractor-displacement table (**T8**).
11. **Unanswerable items are excluded** from both retrieval metrics and answer
    similarity, and scored only on abstention. Retrieval n is 40, not 45.

---

## 13. Pre-specification — what was fixed before any result

**Fixed before any condition ran:** the research questions; chunk size and
retrieval strategy as manipulated factors; coverage@5 and MRR@5 in their
fractional form (the scoring functions are unchanged since the first Stage 1
run); answer similarity and a manual faithfulness check on a subset as measures;
the corpus; the benchmark.

**Not fixed before any condition ran:** any hypothesis (the hypothesis text was
written after every result); any statistical test; the third factor, indexing
representation, which was added after the six text-only conditions had run and
was motivated by them; the case × outcome answer classification, which replaced
an earlier four-tag scheme after the development runs. Nothing in this project
was pre-registered.

**The enrichment format** was settled about three hours before the first
enriched run. The repository cannot show that order, because the format and the
first enriched run landed in one commit; the evidence is a working log kept
outside the repository.

**Every hypothesis family was set up after its own descriptive result.** Family
2's test (H1/H2 within `text_only`) was specified in a follow-up diagnostic after
the six-condition descriptives. For Families 1 and 3, the test *procedure*
(paired Wilcoxon, Holm within each family) was inherited unchanged from that
diagnostic, but the *family structure* for the new factor was set after the
enriched descriptive result had been seen. The confirmatory standing of H1–H3
therefore rests on what was fixed before their conditions ran — for H1 and H2
the research questions and the two factors; for H3, only the design record of
the added factor.
