# Stage 2 statistical analysis of generation outcomes

> **SUPERSEDED — population, not method.** Every number in this file describes the
> **6-condition, 270-row `text_only` population** as it stood before the
> `metadata_enriched` arm was generated. The grid is now **12 conditions / 540 rows**,
> so the pooled figures here (Case B n=194, Case C n=46, "the six conditions are not
> distinguishable") are statements about the `text_only` half only and must not be
> quoted as describing the experiment as a whole.
>
> **Replaced by `analysis/qwen3.8-27b_q4_k_xl/stage2_statistics_12cond.md`**, which recovers this file's
> method unchanged, reproduces every value below on the 270-row population first, and
> then extends to 540 under the same three-family structure Stage 1 uses.
>
> This file is **left unmodified below this note** as the historical `text_only` record.


Read-only over the post-fix results. No changes to the scorer, taxonomy, retrieval,
benchmark, corpus, or any results file. **All numbers below use the post-fix tables**
(`results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv`, 270 rows). The pre-fix tables remain
preserved, unmodified, at `results/tables/prefix/` for comparison — not used here.

Companion file: `analysis/qwen3.8-27b_q4_k_xl/stage2_outcomes_long.csv` — one row per (question_id,
condition_id), with case, outcome, chunk_size, retrieval_strategy, category, coverage,
chunk_size_sensitive, and bertscore_cosine where applicable. Everything below is
reproducible by pivoting that file.

---

## Method note, stated up front because it drives every number below

**Case membership (A/B/C) is assigned per (question, condition) pair, not per
question.** A question's gold anchor can surface in one condition's top-5 and not
another's, so the same question can be Case B under `chunk200_bm25` and Case C under
`chunk200_hybrid`. This matters for every "within Case B" / "within Case C" test below:

- **A1 (raw pairwise, 15 pairs):** for a comparison of condition X vs Y within case K,
  the matched set is questions where case(q, X) == case(q, Y) == K. This is the only
  way to keep the comparison genuinely paired (both conditions facing a case-K
  situation for that specific question) — but it means **the matched n is different for
  every pair**, not a fixed 194 (Case B total) or 46 (Case C total). Reported per pair.
- **A2 (main effects, chunk size / strategy):** for each question, a "side" (e.g.
  chunk_size=200) pools its 2–3 conditions; the question contributes to that side only
  via the conditions where it is genuinely case K, and its value on that side is the
  fraction of those conditions achieving the outcome. A question is included in the
  paired test only if it has at least one valid case-K observation on **both** sides.
  Denominator distributions (how many of the 2–3 conditions per side actually
  contributed) are reported for transparency, since they're not fixed either.

Test choice, as asked: **McNemar's exact test** (`scipy.stats.binomtest` on the larger
of the two discordant counts, n = trials, p = 0.5 — the standard exact-McNemar
formulation) for A1, because the per-pair outcome is a genuine binary indicator
(achieved outcome O or not) on matched pairs — McNemar is the standard test for paired
binary/nominal data, not Wilcoxon, which assumes an ordinal or continuous paired
difference. For A2, after collapsing 2–3 conditions per side into a fraction
(0, 1/3, 1/2, 2/3, or 1), the value is no longer purely binary, so **Wilcoxon
signed-rank** is used there instead, matching the convention already used for the
retrieval-metric main effects in `stage1_diagnostics.md`.

---

## A1 — Do outcomes differ across conditions? (15 pairwise, Case B and Case C separately)

### Headline: no. Every single one of the 240 pairwise tests (15 pairs × 4 outcomes × 2
cases) is non-significant, and the vast majority are non-significant even *before* Holm
correction. This is the same conclusion Stage 1 reached for retrieval metrics, now
extended to generation outcomes: **the six conditions are not distinguishable on
generation outcomes either, at this sample size.**

### Case B (matched n per pair ranges 26–31 — Case B is the majority class, so this is
reasonably close to full-sample)

| outcome | best (lowest) raw p across the 15 pairs | that pair | Holm-adjusted | win/loss/tie at that pair |
|---|--:|---|--:|---|
| abstained | 0.625 | chunk500_bm25 vs chunk500_dense | 1.000 | 3/1/24 |
| answered_grounded_correct | 0.250 | chunk200_dense vs chunk500_dense (and chunk200_hybrid vs chunk500_dense) | 1.000 | 0/3/26 |
| answered_grounded_offtarget | 0.500 | chunk200_dense vs chunk500_dense | 1.000 | 0/2/27 |
| answered_ungrounded | 1.000 | (all ties or single discordant pairs) | 1.000 | -- |

Every discordant-pair count (the "win_x / win_y" in the raw output) is small — 1 to 7
out of ~28 matched questions per pair — and roughly balanced between the two directions
in almost every case. There is no pair, for any outcome, where one condition
systematically outscores another; the pattern is noise-sized swings in both directions.

### Case C (matched n per pair ranges **1–6** — this is the number to sit with)

Case C is only 5–9 questions per condition to begin with (see A3), so the *intersection*
of "both conditions call this question Case C" collapses further — several pairs have
only 1–3 matched questions. At that n, McNemar's exact test has essentially no power to
detect anything, and most pairs show 0 discordant pairs (`n_disc=None` in the raw
output — literally nothing to test). The few p-values that do compute are all 1.0000
before correction. **Case C pairwise comparisons are uninformative at this sample size,
not merely non-significant** — there usually isn't enough matched data to run the test
at all. This is itself a finding, expanded in A5.

Full 15-pair × 4-outcome tables for both cases (win/loss/tie, McNemar p raw and
Holm-adjusted, Cohen's g) are reproducible from `stage2_outcomes_long.csv`; omitted here
in full since every cell tells the same story (no pair survives correction, several
pairs in Case C have no test to run).

---

## A2 — The two main effects

### Chunk size (200 vs 500), collapsed across strategy

| case | outcome | n included | win(200>500) | loss(500>200) | tie | p (raw) |
|---|---|--:|--:|--:|--:|--:|
| B | abstained | 34 | 5 | 4 | 25 | 0.552 |
| B | answered_grounded_correct | 34 | 1 | 4 | 29 | 0.131 |
| B | answered_grounded_offtarget | 34 | 5 | 2 | 27 | 0.350 |
| B | answered_ungrounded | 34 | 1 | 1 | 32 | 1.000 |
| C | abstained | 8 | 2 | 0 | 6 | 0.500 |
| C | answered_grounded_correct | 8 | 1 | 2 | 5 | 1.000 |
| C | answered_grounded_offtarget | 8 | 0 | 1 | 7 | 1.000 |
| C | answered_ungrounded | 8 | 0 | 0 | 8 | n/a (zero variance) |

Nothing significant, same as retrieval metrics. The closest thing to a lean —
Case B `answered_grounded_correct` favoring 500 tokens (loss=4 vs win=1, i.e. 500 wins
more often), p=0.131 — is the same direction Stage 1 found for MRR, but still nowhere
near significance and n=34 is already most of Case B, so this isn't a power artifact
being fixed by more data within this design; it would need a larger benchmark. Case C's
n included is only 8 questions (denominators — how many of the 2–3 same-side conditions
actually counted as Case C — are mostly 1–3, shown in the raw output), too thin to lean
on at all.

### Strategy (dense vs bm25 vs hybrid), collapsed across chunk size

| case | outcome | pair | n included | win | loss | tie | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|
| B | answered_grounded_correct | dense vs hybrid | 34 | 2 | 0 | 32 | 0.157 | 0.472 |
| B | answered_grounded_correct | bm25 vs hybrid | 32 | 2 | 0 | 30 | 0.180 | 0.472 |
| B | answered_grounded_correct | dense vs bm25 | 35 | 2 | 2 | 31 | 0.706 | 0.706 |
| B | answered_ungrounded | dense vs hybrid | 34 | 0 | 2 | 32 | 0.157 | 0.315 |
| B | answered_ungrounded | bm25 vs hybrid | 32 | 0 | 2 | 30 | 0.157 | 0.315 |

(All other case/outcome/pair combinations have p_raw ≥ 0.35 or are untestable; full
table in the companion CSV.) The pattern worth naming even though it doesn't clear
significance: **hybrid never loses to dense or bm25 on `answered_grounded_correct` in
Case B** (2 wins, 0 losses, both comparisons) and **never loses to them on
`answered_ungrounded`** either (0 wins for dense/bm25, i.e. hybrid has fewer or equal
ungrounded answers in every discordant pair). That's directionally consistent with
Stage 1's finding that hybrid trended ahead on MRR — but "consistent lean, doesn't
clear significance" is the correct and complete description; it is not evidence hybrid
is better at n=45.

---

## A3 — Retrieval-to-answer conversion

### Case C: does retrieval success convert to a correct answer?

| condition | Case C n | correct | abstained | other | conversion rate |
|---|--:|--:|--:|--:|--:|
| chunk200_bm25 | 7 | 5 | 2 | 0 | 0.714 |
| chunk200_dense | 5 | 4 | 1 | 0 | 0.800 |
| chunk200_hybrid | 9 | 6 | 3 | 0 | 0.667 |
| chunk500_bm25 | 8 | 5 | 2 | 1 | 0.625 |
| chunk500_dense | 8 | 4 | 4 | 0 | 0.500 |
| chunk500_hybrid | 9 | 6 | 3 | 0 | 0.667 |

Pooled: 30/46 = 0.652, matching the 65% figure already known. Per-condition it ranges
0.50–0.80, with `chunk500_dense` visibly lower (half its Case C items are abstained
rather than answered) and `chunk200_dense` visibly higher — but both are n=5 and n=8.

**Whether this differs across conditions: tested, but the test isn't trustworthy at
this n and I'm saying so rather than reporting a number that looks more solid than it
is.** A 6×2 contingency (correct vs. other, by condition) gives χ²=1.460, df=5,
p=0.918 — but the minimum expected cell count is 1.74, well under the conventional
rule-of-5 for chi-square validity, so this p-value is descriptive at best, not a result
to cite. **Correct statement: n does not permit a reliable test of whether conversion
rate differs by condition. Report the six rates descriptively (table above); do not
report the χ² p-value as evidence of "no difference."**

### Case B, inverse: of retrieval failures, how often does the system correctly abstain?

| condition | Case B n | abstained | abstain rate |
|---|--:|--:|--:|
| chunk200_bm25 | 33 | 22 | 0.667 |
| chunk200_dense | 35 | 24 | 0.686 |
| chunk200_hybrid | 31 | 20 | 0.645 |
| chunk500_bm25 | 32 | 21 | 0.656 |
| chunk500_dense | 32 | 20 | 0.625 |
| chunk500_hybrid | 31 | 20 | 0.645 |

Tight band, 0.625–0.686 — the model's abstain-on-failure behavior is remarkably
consistent across all six conditions, which is itself worth stating: whatever drives
abstention looks like a property of the generator's response to a given context, not
something the retrieval condition is influencing.

---

## A4 — BERTScore (cosine), Case C answered rows

| | n | mean | median | min | max |
|---|--:|--:|--:|--:|--:|
| pooled | 31 | 0.881 | 0.888 | 0.684 | 1.000 |
| chunk200_bm25 | 5 | 0.910 | 0.960 | 0.792 | 1.000 |
| chunk200_dense | 4 | 0.903 | 0.931 | 0.772 | 0.979 |
| chunk200_hybrid | 6 | 0.902 | 0.963 | 0.739 | 1.000 |
| chunk500_bm25 | 6 | 0.917 | 0.907 | 0.830 | 1.000 |
| chunk500_dense | 4 | 0.805 | 0.782 | 0.684 | 0.971 |
| chunk500_hybrid | 6 | 0.833 | 0.839 | 0.715 | 0.944 |

By outcome label: 30 rows are `answered_grounded_correct` (mean 0.882, full range
0.684–1.000), and exactly **1 row is `answered_grounded_offtarget`** — the only
non-correct Case C row that was ever eligible (`is_bertscore_scored` requires Case C +
answered, not specifically "correct"). That row scores **0.830**.

**Does it separate the outcome labels? No — checked directly, not asserted.** The one
offtarget row's score (0.830) sits inside the interquartile range of the 30 "correct"
scores, which span from 0.684 to 1.000 with a median of 0.888 — it is not an outlier on
the low end, it's comfortably mid-pack. A single counterexample is enough to answer the
question: a correctly-labeled offtarget answer can score higher than a meaningful
fraction of correctly-labeled correct answers, so a BERTScore threshold could not have
recovered the outcome label here. With only 1 non-correct row this can't be
generalized into a distributional claim, but it directly supports treating BERTScore as
descriptive supplementary information, not a metric that adds discriminative power
beyond the outcome taxonomy — which is the conclusion you expected, now backed by the
actual number rather than assumed.

---

## A5 — Power

**Effective n is small almost everywhere, and Case C is the extreme case of a pattern
that already showed up in Stage 1.**

- **A1 (McNemar, Case B):** discordant-pair counts (the effective n McNemar actually
  runs on) range roughly 1–7 out of ~28–31 matched questions per pair — most of the
  matched sample is tied (same outcome under both conditions), which is expected when
  both raw outcome rates and the true effect are small, but it means the test is
  working with a handful of informative pairs even though the matched sample looks
  respectable.
- **A1 (McNemar, Case C):** matched n itself collapses to 1–6 before any discordant-pair
  count is even computed — several pairs have zero discordant pairs and no test runs at
  all. This is a harder power problem than Case B: it's not that the effect is small
  within an adequate sample, there frequently isn't an adequate matched sample to begin
  with.
- **A2 (Wilcoxon, main effects):** n_nonzero (informative, non-tied questions) is 2–9
  out of 34 (chunk size, Case B) or 34 (strategy, Case B) — and only 0–3 out of 8
  (Case C, either main effect).

**Same concentration pattern as Stage 1, quantified directly:** 22 of the 45 questions
(49%) get the **identical outcome label in all 6 conditions** — condition has no effect
on these at all, by definition, for this measure. 29 of 45 (64%) get the **identical
case (A/B/C) in all 6 conditions** — meaning for most questions, retrieval either always
finds the anchor or never does, regardless of chunk size or strategy. This mirrors
Stage 1's "23 of 40 questions scored zero in every condition" finding almost exactly,
and it's the direct mechanical reason effective n is small everywhere above: a large
share of the benchmark contributes zero information to any condition-vs-condition
comparison, on either the retrieval or the generation side.

**Bottom line for power:** this isn't a statistical technicality to note in passing —
it's the reason A1–A3 come back non-significant. With roughly half the benchmark
providing no discordant information at all, no realistic effect size at n=45 would
survive correction. A larger, more heterogeneous benchmark (more questions where
condition actually could plausibly flip the outcome) is the only lever that would
change this — not a different test.

---

## Report summary

**Are the six conditions distinguishable on generation outcomes? No — stated plainly,
matching Stage 1's retrieval-side conclusion.** Every one of the pairwise and main-effect
tests across both cases and all four outcomes is non-significant, and the raw
discordant-pair counts (led with, as requested) show no consistent direction, only
noise-sized swings in both directions — with one partial exception: hybrid never loses
to dense or bm25 on Case B `answered_grounded_correct` or `answered_ungrounded` across
both pairwise comparisons, a directionally consistent lean that still doesn't clear
significance at this n. Case C analyses in particular are frequently underpowered to the
point of having no test to run, not merely a non-significant one, because Case C is only
5–9 questions per condition and the paired-matching requirement shrinks that further.
The retrieval-to-answer conversion rate (A3) ranges 50–80% by condition but the test for
whether that's real is explicitly flagged as unreliable at this n rather than reported
as a clean null. BERTScore (A4) is confirmed, not assumed, to add nothing beyond the
outcome taxonomy — the one non-correct scored row lands mid-pack in the correct
distribution. The root cause of all of this (A5) is the same one Stage 1 already
identified: roughly half the benchmark returns the identical result in every condition,
which caps how much any test at n=45 can detect regardless of which test is used.
