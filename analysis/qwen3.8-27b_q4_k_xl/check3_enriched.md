# Check 3 (attribution exposure) — the `metadata_enriched` arm

Model: `qwen3.8-27b@q4_k_xl`. Population: Case C `answered_grounded_correct`.

Method imported unchanged from `analysis/check3_attribution_postfix.py`, whose
This script re-asserts the pinned post-fix `text_only` figure for the model in
scope before computing anything enriched, and exits if it does not reproduce.
Expectations are per-model; a model with no pinned set runs unchecked and says so.

An item is flagged when at least one **substantive** numeric claim is supported ONLY
by chunks outside the question's own `transcript_ids`. `substantive` = not a bare
year 2022–2026 and not a bare digit 1–4 (the diagnostic's own rule, deliberately not
`evaluate.is_trivial_claim`).

## 1. Full populations

> **This pooled comparison is a composition artifact and is NOT a finding.** The two
> populations are not the same items: Case C membership depends on whether the gold
> anchor was retrieved, so enrichment changes who is in the population at the same
> time as it changes the outcome. The two percentages below are therefore not
> comparable, and their difference does not measure an effect of enrichment. The
> strictly-matched population in section 2 is the like-for-like one.
> **Quote section 2, not this table.**

> **Every figure in this document is a LOWER BOUND on wrong-company attribution.**
> Check 3's population is Case C `answered_grounded_correct` — by construction it
> can only see items that were retrieved well AND scored correct. An answer that
> attributes one company's material to another in Case A or Case B is outside the
> population entirely and is never counted here.
>
> This is measured, not hypothetical. The manual faithfulness review of the q8 arm
> (`analysis/qwen3.8-27b_q8_k_xl/manual_review_second_pass.md`, pile P1) found 12 such
> items in a 48-item sample, split Case A 5 / Case B 5 / Case C 2 — so the diagnostic
> could see 2 of the 12. The behaviour is not arm-specific and the population limit is
> structural, so treat the figures below as a floor in EVERY arm, never as a measurement.

| arm | n | flagged | % |
|---|--:|--:|--:|
| text_only (published post-fix) | 30 | 9 | 30% |
| **metadata_enriched** | **79** | **11** | **14%** |

## 2. Restricted to the Task 3 intersection (Case C in BOTH arms)

Like-for-like: the same items in both arms, so this is not confounded by the
population change enrichment causes.

| arm | n | flagged | % |
|---|--:|--:|--:|
| text_only | 23 | 4 | 17% |
| **metadata_enriched** | **30** | **7** | **23%** |

Note these n are unequal by construction: an item enters Check 3's population only
if it was classified `correct` in that arm, so this controls for Case C membership
but not for the correct/not-correct split.

### Strictly matched — `answered_grounded_correct` in BOTH arms

The only fully paired comparison available: identical items, identical n.

**Read as: no evidence either way** at this sample size.
This is the like-for-like population, but it is small: read the two rows below as a
point estimate on a sample too small to distinguish any difference from chance, in
either direction. Whatever the pooled section 1 comparison appears to show, it is a
composition artifact and does not carry over to this matched population.

| arm | n | flagged | % |
|---|--:|--:|--:|
| text_only | 23 | 4 | 17% |
| **metadata_enriched** | **23** | **6** | **26%** |

## 3. By retrieval strategy

> **Unmatched populations — cannot establish a strategy effect in either direction.**
> These are the section 1 populations split by strategy, so every row inherits the
> same composition confound: the enriched n is larger because enrichment moved items
> into Case C, not because the same items behaved differently. The apparent ordering
> of the rows below is not evidence of a strategy effect,
> and no matched per-strategy comparison is computed here because the per-strategy
> matched n would be in single digits.

| strategy | text_only flagged/n | % | enriched flagged/n | % |
|---|--:|--:|--:|--:|
| dense | 2/8 | 25% | 6/32 | 19% |
| bm25 | 3/10 | 30% | 2/16 | 12% |
| hybrid | 4/12 | 33% | 3/31 | 10% |

Per-record detail: `check3_enriched.csv`.
