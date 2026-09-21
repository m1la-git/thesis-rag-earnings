> **REGRESSION PIN, NOT AN INDEPENDENT REPRODUCTION.** This document was written FROM `analysis/stage2_statistics_12cond.py`'s output, so that script validating against it proves only that the script still computes today what it computed yesterday. It catches drift; it is not two sources agreeing. The q4 document was hand-authored BEFORE the script existed, so its PASS is a real check. **A PASS on this file and a PASS on that one do not mean the same thing.** See Provenance below.

# Stage 2 statistical analysis of generation outcomes — `qwen3.8-27b@q8_k_xl`

Population: the **270 `text_only` records** (6 conditions × 45 questions) of the
reported arm. The `metadata_enriched` half and the 12-condition extension are in
`stage2_statistics_12cond.md`; this document is the 6-condition counterpart of
`analysis/qwen3.8-27b_q4_k_xl/stage2_statistics.md`.

Case partition of the 270: **A 30, B 194, C 46.** Cases come from Stage 1 and are
identical across generators.

## Provenance — read this before quoting the validation

This document was written **from** `analysis/stage2_statistics_12cond.py`'s own
computation. The q4 document it mirrors was hand-authored *before* that script
existed, so the script reproducing it is a genuine independent check. Nothing of
the sort is true here.

**So `stage2_statistics_12cond.py --validate` against this file is a REGRESSION
PIN, not a reproduction.** It guards against the analysis code drifting away from
the figures published today — the same job `analysis/expectations/*.json` does —
and it is worth having for exactly that. It is not evidence that two independent
derivations agree, and must not be reported as if it were.

## Direction convention, stated because it is easy to invert

In every paired table below, `win` counts questions where the **first-named**
side scores higher on that outcome, `loss` where the second does. So in
`dense vs hybrid`, `win = 2` means **dense** beat hybrid on two questions.

For `abstained` and `answered_grounded_correct`, higher is better. For
`answered_grounded_offtarget` and `answered_ungrounded`, higher is **worse** — a
side that "wins" those rows is performing worse, not better.

> The corresponding paragraphs in the q4 document read these columns the other
> way round and conclude that hybrid leads. The q4 tables are correct; the prose
> around them inverts the sign. That document is development history and not a
> source of any thesis claim, so it is left as it stands — but do not carry its
> directional wording across to this arm.

## Method note

Unchanged from the q4 document and from Stage 1 Part 6, so the two arms are
comparable:

- Case membership is per (question, condition). A pair's matched set is the
  questions **both** conditions place in that case.
- A1 uses **McNemar's exact test** (`binomtest` on the larger discordant count,
  n = b+c, two-sided). A2 uses the **paired Wilcoxon** over per-question
  fractions-of-conditions.
- **Holm–Bonferroni within each (case, outcome) family**, at that family's own
  size. An untestable comparison consumes no rank, because it is not a test.
- Unanswerable items are Case A and never enter a Case B or Case C comparison.
- Case C is the **any-anchor** condition (coverage@5 > 0), asserted at run time.

---

## A1 — Do outcomes differ across conditions? (15 pairwise, Case B and Case C separately)

### Headline: no. Of **120 tests** (15 pairs × 4 outcomes × 2 cases), **65 are testable and 0 are significant after Holm.**

The 55 untestable comparisons are not failures — they are cells where both
conditions produced the identical outcome for every matched question, so there is
no discordance to test.

### Case B (matched n per pair 26–31 — the majority class, so this is the real test)

| outcome | best (lowest) raw p across the 15 pairs | that pair | Holm-adjusted | win/loss/tie at that pair |
|---|--:|---|--:|---|
| abstained | 0.6250 | chunk200_bm25 vs chunk500_hybrid | 1.0000 | 3/1/25 |
| answered_grounded_correct | 0.2500 | chunk200_bm25 vs chunk500_bm25 | 1.0000 | 0/3/26 |
| answered_grounded_offtarget | 0.2188 | chunk500_bm25 vs chunk500_hybrid | 1.0000 | 1/5/22 |
| answered_ungrounded | 1.0000 | chunk200_bm25 vs chunk200_hybrid | 1.0000 | 0/1/29 |

Testable comparisons per family: 15, 14, 15 and **5** respectively. The
`answered_ungrounded` family is nearly empty because that outcome is rare in this
arm — 1 record across all 194 Case B rows.

Even the best raw p in the family (0.2188) is an order of magnitude from
significance before adjustment, and every Holm-adjusted value is 1.0000.

### Case C (matched n per pair **1–6** — this is the number to sit with)

`abstained` and `answered_grounded_correct` have 8 of 15 pairs testable, best raw
p **1.0000** in both. `answered_grounded_offtarget` and `answered_ungrounded` have
**0 of 15** testable: Case C in this arm contains only `abstained` (15) and
`answered_grounded_correct` (31), so the other two outcomes never vary.

With 1–6 matched questions per pair, Case C cannot distinguish anything from
chance and no reading should be attempted from it.

---

## A2 — The two main effects

### Chunk size (200 vs 500), collapsed across strategy

| case | outcome | n included | win(200>500) | loss(500>200) | tie | p (raw) |
|---|---|--:|--:|--:|--:|--:|
| B | abstained | 34 | 5 | 4 | 25 | 0.475 |
| B | answered_grounded_correct | 34 | 1 | 5 | 28 | 0.084 |
| B | answered_grounded_offtarget | 34 | 5 | 3 | 26 | 0.324 |
| B | answered_ungrounded | 34 | 1 | 0 | 33 | 0.317 |
| C | abstained | 8 | 1 | 0 | 7 | 1.000 |
| C | answered_grounded_correct | 8 | 0 | 1 | 7 | 1.000 |
| C | answered_grounded_offtarget | 8 | 0 | 0 | 8 | n/a (zero variance) |
| C | answered_ungrounded | 8 | 0 | 0 | 8 | n/a (zero variance) |

**Nothing significant.** The strongest lean in the whole arm is Case B
`answered_grounded_correct` at **p = 0.084**: 1 win for 200 tokens against 5 for
500, i.e. **500 produces the correct answer more often** on the discordant
questions. That is the same direction Stage 1 found for MRR, and it survives from
the q4 arm, but n included is 34 — already most of Case B — so this is not a
power shortfall that more conditions would fix. It would need a larger benchmark.

Case C's `n included` is 8 questions. Nothing there is interpretable.

### Strategy (dense vs bm25 vs hybrid), collapsed across chunk size

All rows with raw p < 0.35; the remaining 9 testable combinations are at
p ≥ 0.35 or untestable, and the full set is in the companion CSV.

| case | outcome | pair | n included | win | loss | tie | p (raw) | p (Holm) |
|---|---|---|--:|--:|--:|--:|--:|--:|
| B | answered_grounded_correct | bm25 vs hybrid | 32 | 3 | 0 | 29 | 0.102 | 0.307 |
| B | answered_grounded_correct | dense vs hybrid | 34 | 2 | 0 | 32 | 0.157 | 0.315 |
| B | answered_grounded_offtarget | bm25 vs hybrid | 32 | 2 | 5 | 25 | 0.206 | 0.618 |
| B | answered_grounded_offtarget | dense vs hybrid | 34 | 1 | 3 | 30 | 0.317 | 0.635 |
| B | answered_ungrounded | dense vs hybrid | 34 | 0 | 1 | 33 | 0.317 | 0.635 |
| B | answered_ungrounded | bm25 vs hybrid | 32 | 0 | 1 | 31 | 0.317 | 0.635 |

**The consistent lean is against hybrid, and it does not clear significance.**
Reading the columns by the convention above: hybrid never wins a discordant
question on `answered_grounded_correct` (0 losses in both comparisons means
hybrid was never the better side), it takes more `answered_grounded_offtarget`
than either alternative, and it holds the arm's single `answered_ungrounded`
record. Raw counts across the 194 Case B rows agree:

| | dense | bm25 | hybrid |
|---|--:|--:|--:|
| answered_grounded_correct | 4 | 4 | **2** |
| answered_grounded_offtarget | 19 | 18 | **20** |
| answered_ungrounded | 0 | 0 | **1** |

Minimum Holm-adjusted p across the whole strategy family is **0.307**. "A
consistent lean that does not clear significance at n = 45" is the correct and
complete description; this is not evidence that hybrid is worse.

---

## A3 — Retrieval-to-answer conversion

### Case C: does retrieval success convert to a correct answer?

| condition | Case C n | correct | rate |
|---|--:|--:|--:|
| chunk200_bm25 | 7 | 5 | 71% |
| chunk200_dense | 5 | 4 | 80% |
| chunk200_hybrid | 9 | 6 | 67% |
| chunk500_bm25 | 8 | 6 | 75% |
| chunk500_dense | 8 | 4 | 50% |
| chunk500_hybrid | 9 | 6 | 67% |
| **pooled** | **46** | **31** | **67%** |

Every per-condition n is between 5 and 9. The spread from 50% to 80% is four
questions wide at its extremes and should be read as noise.

### Case B, inverse: of retrieval failures, how often does the system correctly abstain?

| condition | Case B n | abstained | rate |
|---|--:|--:|--:|
| chunk200_bm25 | 33 | 22 | 67% |
| chunk200_dense | 35 | 24 | 69% |
| chunk200_hybrid | 31 | 20 | 65% |
| chunk500_bm25 | 32 | 21 | 66% |
| chunk500_dense | 32 | 20 | 62% |
| chunk500_hybrid | 31 | 19 | 61% |
| **pooled** | **194** | **126** | **65%** |

Tight: 61%–69% across all six conditions. **The complement is the number that
matters — 35% of retrieval failures are answered rather than declined**, and by
the Case B definition those answers cannot be grounded in the passage the
question was written from. That is a property of the generator's abstention
behaviour, not of any retrieval choice, which is why it barely moves across
conditions.

---

## A4 — BERTScore (cosine), Case C answered rows

Scope by design: Case C, answered only. Case A and Case B are excluded by
construction, not for missing data — comparing an answer grounded in the wrong
transcript against a reference written for the right one measures retrieval's
failure, not generation's.

n = **31** (every answered Case C record in this arm is
`answered_grounded_correct`; Case C has no offtarget or ungrounded records here).

| | value |
|---|--:|
| mean | 0.8728 |
| median | 0.8886 |
| min | 0.6837 |
| max | 1.0000 |

| condition | n | mean |
|---|--:|--:|
| chunk200_bm25 | 5 | 0.9066 |
| chunk200_dense | 4 | 0.9008 |
| chunk200_hybrid | 6 | 0.9002 |
| chunk500_bm25 | 6 | 0.9117 |
| chunk500_dense | 4 | 0.7781 |
| chunk500_hybrid | 6 | 0.8230 |

**Descriptive only, and n per condition is 4–6.** No test is run and none should
be: this is reported as a number for the thesis, not leaned on for any claim.
The two low means are each four to six questions.

---

## A5 — Power

- **Case B**: matched n per pair **26–31**. This is the arm's usable population
  and it is where the tests above actually live.
- **Case C**: matched n per pair **1–6**. Nothing is testable at that size, and 7
  of 15 pairs are untestable outright in the two outcomes that vary at all.
- **A1 overall**: 120 tests, 65 testable, 0 significant after Holm.
- 55 of 120 comparisons are untestable because both conditions produced the
  identical outcome on every matched question — which is itself the finding:
  the conditions largely do not differ.

At n = 45 questions, with Case C reduced to 46 of 270 records, this design can
detect only large effects. The absence of significance is consistent with there
being no effect and equally consistent with an effect this design cannot see.
Report it as a null result with the power caveat attached, never as evidence of
equivalence.

---

## Report summary

1. **No condition differs significantly from another on any generation outcome.**
   0 of 65 testable pairwise tests survive Holm; the minimum raw p anywhere in
   the arm is 0.084 and the minimum Holm-adjusted p is 0.307.
2. **The only lean worth naming on chunk size** is Case B
   `answered_grounded_correct` favouring 500 tokens (1 win vs 5, p = 0.084),
   matching the direction Stage 1 found for MRR.
3. **The only lean worth naming on strategy is against hybrid**, consistently
   across three outcomes and confirmed by raw counts, at minimum Holm p = 0.307.
   Note this is the opposite direction to the q4 document's prose, which inverts
   the win/loss columns.
4. **Conversion is stable across conditions**: 67% of Case C converts to a
   correct answer, 65% of Case B correctly abstains, both moving less than 10
   points across all six conditions.
5. **35% of retrieval failures are answered rather than declined.** This is the
   largest single quantity in the arm and it is a generator property, not a
   retrieval one.
6. **Case C is too small to analyse** — 46 of 270 records, 1–6 matched per pair.
   Every Case C figure here is descriptive.
