# Benchmark Annotation Protocol

Rules under which `benchmark/questions.jsonl` was constructed. This document is
descriptive, not aspirational: every rule below was applied during authoring,
and where a rule was applied with a documented exception, the exception is
named here rather than omitted.

It is written *before* any experimental run, and deliberately so. The benchmark
is the measuring instrument; fixing its rules and publishing them ahead of
results is what keeps the instrument independent of the findings. Nothing here
describes or anticipates a result.

The questions, gold anchors and reference answers were selected by hand from a
larger calibration set, which also holds the per-item provenance, the reasoning
behind each decision, and a log of rejected candidates. That material is
working material and is not version-controlled; this document is the record of
the rules it was built under, and `benchmark/questions.jsonl` is the frozen
output.

**Status:** frozen at 45 items and 74 gold anchors.

| | factual | thematic | comparative | unanswerable | total |
|---|---|---|---|---|---|
| items | 14 | 15 | 11 | 5 | **45** |
| gold anchors | 14 | 38 | 22 | 0 | **74** |

---

## 1. Purpose and scope

The benchmark measures how two retrieval design choices affect answer quality in
a retrieval-augmented QA system over earnings call transcripts. It is an
instrument for a controlled experiment, not a general-purpose QA dataset.

The experiment varies two things and holds everything else constant:

- **chunk size** — 200 tokens and 500 tokens
- **retrieval strategy** — dense, BM25, and hybrid (reciprocal rank fusion)

giving a 2 × 3 grid of six conditions. Every question is run through all six.

> **Addendum, 2026-09-03 — the grid was extended to 12 conditions.** A third
> independent variable, **`indexing_representation`** (`text_only` vs
> `metadata_enriched`: raw chunk text, or chunk text prefixed with structured
> company/ticker/quarter/section metadata), was added after the six-condition
> grid returned a null on both retrieval and generation outcomes and the Stage 1
> diagnostic traced the mechanism to company and period signal being absent from
> the indexed string. The full design is 2 chunk sizes × 3 retrieval strategies
> × 2 indexing representations = **12 conditions**; the six described here are
> exactly the `text_only` half, unchanged and not re-run. **Every anchor and
> every rule in this document remains valid under the new variable by
> construction**, because a hit is defined against the raw chunk text, which the
> indexing variable does not touch — the enriched string is a separate,
> index-side-only field that the anchor matcher never reads. The extension was
> specified and recorded before any of the six new conditions was run. See
> README.md, "Variables".

The corpus (128 earnings call transcripts, 16 large-cap US banks, 2023 Q1 –
2024 Q4) is frozen and hash-verified before annotation began, because gold
anchors are verbatim strings and any upstream text change would silently
invalidate them.

### The four categories

| category | definition |
|---|---|
| **factual** | A single figure or statement from one transcript. One anchor each. |
| **thematic** | One topic recurring across two or three banks. Two or three anchors. |
| **comparative** | Two named companies set against each other. Two anchors, at least one per company. |
| **unanswerable** | No supporting passage exists in the corpus. No anchors. |

### Why unanswerables are excluded from the retrieval metrics

An unanswerable question has no passage to retrieve. Scoring it zero on
`anchor_coverage_at_5` or MRR would record a phantom retrieval failure that
drags down whichever condition happened to be measured, and would make the six
conditions differ on a quantity none of them can influence. Unanswerable items
are therefore **dropped from the denominator of both retrieval metrics
entirely**, not scored as misses, and are evaluated **only** on whether the
system abstained.

Each unanswerable rests on a *structural* absence, not a coincidental gap — a
company outside the 16 (`out_of_corpus_company`), a period outside 2023 Q1 –
2024 Q4 (`out_of_range_period`), or a topic never discussed (`absent_topic`) —
recorded per item in `absence_type`. Absence was verified by case-insensitive
substring search over the raw text of all 128 transcripts. A candidate resting
on an interior gap in a transcript that *does* discuss the topic was removed for
that reason.

---

## 2. Anchor construction rules

A **gold anchor** is a short verbatim string lifted character-for-character from
a transcript. A retrieved chunk counts as a **hit** when it contains that string
as a substring — exact and case-sensitive, with no normalisation.

Anchors rather than chunk IDs, because chunk IDs are not stable across
conditions: chunk 47 at 200 tokens is different text from chunk 47 at 500
tokens. Anchors are annotated once and scored unchanged across all six cells.

Every anchor satisfies all of the following:

1. **Verbatim.** An exact substring of its source sentence. Verified
   mechanically for all 74.
2. **Contained under both chunk sizes.** Present in a single chunk at 200 tokens
   *and* in a single chunk at 500 tokens. An anchor split by a boundary under one
   configuration but not the other would fail the substring test in one condition
   and pass in the other, manufacturing a difference between conditions that has
   nothing to do with retrieval quality.
3. **Edge-clear.** At least `MIN_EDGE_MARGIN_WORDS = 2` words clear of both ends
   of its source sentence, keeping headroom away from chunk edges.
4. **Within the word caps.** 5–15 words for prepared remarks, 5–20 for Q&A.
5. **No fragment edge.** An anchor may not begin or end on a dangling function
   word.
6. **Management-spoken.** All 74 anchors are utterances by company management;
   no analyst or operator speech is anchored.

These rules bind, and the rejections are logged. The construction record holds
19 entries covering anchors rejected for straddling a chunk boundary or
breaching the edge margin, whole candidates removed, two planned comparatives
abandoned, and the re-sourcing passes that followed a rule change. In one case
no valid span existed anywhere in either bank's eight transcripts, so the
planned item was abandoned rather than weakened to fit.

**Section distribution:** 64 of 74 anchors are from prepared remarks, 10 from
Q&A. See §6.3.

### How each property was verified

Every anchor was checked programmatically before inclusion:

| Property | Method |
|---|---|
| Verbatim | Exact substring match against the raw transcript text. No normalisation, no whitespace collapsing, no unicode substitution. |
| Contained under both configs | Exact containment check using the production chunking code, not a head/tail heuristic |
| Edge margin | ≥ 2 words left at both ends of the source sentence |
| Word cap | ≤ 15 words prepared remarks, ≤ 20 Q&A |
| Document frequency | Corpus-wide count; **all 74 anchors are df 1** |
| Speaker role | Derived from turn metadata; all 74 management-spoken |
| Figure support | Every number in a question or answer cross-checked against its anchor |

### Absence was proven, not assumed

For the unanswerable items, every search term was re-counted across the raw text
of all 128 transcripts; a single occurrence anywhere fails. Two findings show
the check doing real work rather than rubber-stamping:

- A planned unanswerable about **Truist** was rejected: the term appears 15
  times across five transcripts, because *Truist Securities* is an analyst firm.
  That affiliation leak would have made the question partially answerable.
- A planned out-of-range-period question had to be made **quarter-specific
  rather than year-specific**: the bare token "2021" appears 81 times as
  backward comparatives, and only "Q2 2021" and its variants return zero.

---

## 3. The support rule

> Every substantive claim in a reference answer must trace either to text inside
> a gold anchor, or to a term the question itself supplies.

Nothing may come from the source sentence *outside* the anchor. This is stricter
than faithfulness to the transcript: a claim can be perfectly true of the
earnings call and still violate the rule, because the evaluated system will only
ever see the retrieved chunk, and the anchor defines what the item guarantees is
retrievable.

Enforcement covers four failure classes specifically:

- **Period qualifiers past the anchor's end** — e.g. "compared to the end of
  June", "ago quarter", "in the prior year", "four quarters".
- **Metric names taken from outside the anchor** — naming a measure whose
  identifying word falls outside the span.
- **Scope qualifiers** — *adjusted*, *core*, *retail*, *gross*, *tangible*
  asserted without anchor or question support.
- **Comparison bases** stated without support.

### The question-licence mechanism

Where a metric name or qualifier sits outside its anchor and the anchor cannot
be extended to carry it — because doing so would breach the edge margin, exceed
the word cap, or break containment — **the question is worded to name the term
instead.** A term the question supplies is available to the answer, because the
system reading the question has that term in hand.

Eight items rely on this. In each, anchor extension was checked first and found
impossible under the rules in §2.

| item | term licensed by the question | why extension failed |
|---|---|---|
| `ref_them_03` | *allowance* | "allowance" occurs only at word index 1, inside the leading edge margin |
| `ref_them_08` | *AUM*, *client investment assets* | "AUM" is the final word, past the trailing margin; a span reaching "Client investment assets" would start at index 0 |
| `ref_them_09` | *adjusted* (reported and adjusted bases) | "adjusted" opens its sentence at index 1, inside the leading margin |
| `ref_them_15` | *G&A* | extending backward past a 200-token split would risk containment and the item's chunk-size sensitivity |
| `ref_comp_02` | *portfolio reduction* | anchor already ends at the last index the trailing margin permits |
| `ref_comp_06` | *revenue growth* | "revenue" is past the trailing margin in both source sentences |
| `ref_comp_10` | *tangible book value per share* | anchor carries "book value per share" only |
| `ref_comp_11` | *non-interest*, *the fall* | "Non-interest" opens its sentence at index 0 |

This mechanism has a measurable side effect on question wording; see
Limitations 3.

---

## 4. The quality rules

Fourteen rules govern the set. **Each was introduced in response to an observed
defect, not specified up front** — benchmark construction was itself an
iterative empirical process. The sequence matters, because several rules exist
only to repair damage an earlier rule caused; those cascades are marked below.

| # | Rule | Introduced because |
|---|---|---|
| 1 | **Speaker attribution.** If a question asks what a company said or reported, every anchor must be management-spoken. | Three thematic candidates anchored on *analysts* restating figures back to management. An analyst restating a number is evidence of what was discussed, not of what the company disclosed. *Cost: Q&A anchor share fell, since analyst speech concentrates there.* |
| 2 | **Answer support.** No reference answer may assert anything not contained in at least one anchor. Entity, metric and period may come from the question; no value or qualifier may be imported. See §3. | An answer completed a clause from text outside its anchor — the anchor ended on "not", the answer supplied "long-term clients". The most consequential rule in the set. |
| 3 | **No fragment edges.** Separate head and tail stoplists. The tail rule is broad; the head rule is narrow — starting on "the" or "our" is fine, on "of" is not. | An anchor ending on "increased by" left the value outside, degrading its answer to "$46.6 trillion, an increase." *→ caused Rule 8.* |
| 4 | **Thematic breadth.** A thematic item must span at least two companies unless explicitly labelled. | One candidate used three anchors from a single company across three quarters — testing period discrimination, not cross-company synthesis. Kept, labelled `subtype: temporal`, as the only item probing quarter-scoping; unlabelled single-company thematics are now rejected. |
| 5 | **Category independence.** Comparative items must not share anchors with thematic items. | Five of six early comparatives reused thematic anchors, making the categories non-independent and testing the same passages twice. *→ caused Rule 7.* |
| 6 | **Difficulty framing.** Difficulty is derived from question-versus-passage vocabulary divergence, not from anchor boundaries. | Early reasoning called items hard because "the anchor omits the query term" — mostly wrong, since retrieval matches *chunks*, not anchors, so anchor boundaries do not affect what is findable. The one genuine anchor-related signal is kept separately as `chunk_size_sensitive` (7 items). |
| 7 | **Period coverage.** Any quarter or year named in a question is parsed and checked against every anchor's fiscal period. | Introduced by Rule 5: re-sourcing anchors left questions naming periods their new evidence did not come from — one asked about Q3 2024 while two of three anchors were Q2 2023. *→ caused Rule 12.* |
| 8 | **Answer completeness.** Answers must be grammatically complete and must actually answer what was asked. | Introduced by Rule 3: clean anchors produced answers trailing off mid-clause — "resulting in an efficiency ratio" with no value. Where Rules 2, 3 and 8 cannot all hold for a sentence, the sentence is unusable and the item is reduced or dropped. Two items were resolved that way rather than by weakening a rule. |
| 9 | **Metadata currency.** Notes, difficulty labels, question text and provenance must describe the *current* anchors. | Notes described anchors that had been replaced — claiming Q&A anchors that no longer existed, or analyst anchors already swapped out. |
| 10 | **Answers name entity, metric and period.** | Several answers were bare figures ("$638 million."). Semantic similarity against a two-word reference is near-arbitrary, which would silently degrade one of three metrics on a sixth of the set. |
| 11 | **Answers read as prose.** Written and checked by reading, not assembled by applying rules to a previous version. | Answers that were grammatical but stitched from anchor spans. Explicitly a human judgement, stated as such rather than approximated by a regex. |
| 12 | **Questions name a period.** | Introduced by Rule 7: four questions were made period-neutral to resolve anchor mismatch, producing questions no analyst would ask — "What efficiency ratio levels did banks discuss?" with no time frame. |
| 13 | **The question licence.** Where a term cannot be brought inside any valid anchor, the question may name it, licensing its use in the answer. See §3. | Rule 2 forbids importing evidence, but the edge margin frequently places the metric name at word index 0 or 1, where no valid span reaches it. Applied to 8 items. |
| 14 | **The answer-verb convention.** Below. | Anchors frequently carry a figure without the verb governing it, so answers must supply one. Some verbs are harmless; others smuggle in information. |

### Scope-qualifier checks (review-only, not numbered rules)

Two checks covering a class Rule 2 misses. Rule 2 catches imported *values*; it
does not catch imported or dropped **qualifiers** — *gross, adjusted, tangible,
non-interest, core, average, period-end* — which change what a figure measures
without changing any number.

- **Forward check** — flags an answer describing a figure with a scope qualifier
  present in neither anchor nor question. Caught an answer stating a
  segment-level investment banking figure as firmwide: an error of roughly an
  order of magnitude, in an item built specifically to test that confusion.
- **Reverse check** — flags an answer using a noun without a qualifier its anchor
  carries. Caught two items where dropping "tangible" renamed the metric
  (tangible book value per share and book value per share are different lines).

Both are review-only, since whether a qualifier changes a figure's meaning is a
judgement. One special case: *reported* is flagged as a modifier ("on a reported
basis") but not as an attribution verb ("M&T reported"), since flagging both
would bury real hits in noise.

**A lesson worth carrying into the methodology chapter.** Rule 10's first
implementation enforced only a word-count minimum, so seven answers passed the
check while still failing the rule as written. An automated check confirms a
rule did not *obviously* fail — not that it passed.

### Rule 14 in full — the answer-verb convention

This convention was written down after the fact. It records judgements already
applied consistently across the 40 answerable items rather than introducing a
new standard, and it is stated here because an undocumented practice cannot be
checked by anyone else.

**Permitted.** A neutral attribution or attainment verb — *said, reported,
noted, booked, posted, achieved, generated, took in, repeated, decided* — may be
supplied where the anchor carries none. Such a verb asserts only that the
company made the statement or reached the figure already in the anchor, which
the item's framing establishes, and adds no information beyond the anchor.

**Not permitted.** A verb that carries information the anchor does not — in
particular the **direction** of a movement (*rose, fell, cut, reduced, grew, up,
down*) — unless the anchor carries that direction or the question supplies it.

A directional verb is licensed when the question names the movement:
`ref_comp_11` licenses *the fall*, `ref_comp_04` licenses *grew* via "deposit
growth", `ref_comp_02` licenses *reduced* via "portfolio reduction".

Cleared under the permitted clause: `ref_them_04` (*achieved*, *generated*),
`ref_fact_08` (*took in*), `ref_them_11` (*earlier that year*), `ref_them_12`
(*decided*), `ref_them_13` (*reached*, *stood at* — the anchors carry "up more
than 50%" and "up more than 70%").

**Documented exception — `ref_them_08`.** The answer says client investment
assets were *up* 21% year-on-year. The anchor begins at "21% year-on-year" and
carries no direction word, and "momentum" in the question does not supply one.
The direction is entailed by the anchor's own "driven by market performance and
strong net inflows" but is not stated in it. Retained as an accepted exception
rather than silently cleared: the claim is sound in substance and loose only in
wording. Fixing it would require re-sourcing the anchor, which was ruled out
after the file was frozen.

---

## 5. Metrics

### Answerable items (40)

Both retrieval metrics are **fractional over a question's own anchors**, and
both apply **uniformly** across factual, thematic and comparative items. There
are no per-category special cases; a uniform rule is what makes comparison
across categories defensible.

```
anchor_coverage_at_5 = (anchors matched within the top-5 chunks) / (total anchors)

mean_reciprocal_rank_at_5:
    per anchor: r = 1-indexed rank of the first top-5 chunk containing it
                contribution = 1/r if matched, else 0
    question score = mean of contributions across all its anchors
```

Both reduce to their standard single-anchor forms. Partial retrieval earns
partial credit but never full credit — a comparative item retrieving one of two
companies scores about 0.5.

This graded approach replaced a strict all-anchors-required rule, which would
have floored every multi-anchor item at zero across all six conditions and
destroyed their ability to discriminate between configurations.

The name **anchor coverage**, not Recall@5, is deliberate. This is not textbook
Recall@5 — binary per query over a set of relevant documents — but the fraction
of a question's own gold anchors found in the top 5. Calling it Recall@5 would
invite a reader to assume standard semantics and mis-read the numbers.

Answer quality is scored by semantic similarity to the reference answer, plus a
manual faithfulness check on a subset.

### Unanswerable items (5)

Excluded from `anchor_coverage_at_5`, from MRR, and from answer similarity.
Scored **only** on abstention: whether the system produced the exact canonical
abstention sentence.

**Abstention results are reported as counts out of 5, never as percentages.**
With n = 5 a single item moves the rate by 20 points, and a percentage would
imply a precision the sample size does not support.

---

## 6. Known limitations

### 6.1 Construction method

Candidates were **generated by a large language model** operating over the
frozen corpus under progressively formalised rule constraints (§4), with each
iteration reviewed by the researcher and the defects found in that review
driving the next rule. The researcher did not author each question
independently from a first reading of the transcripts.

This differs from the manual authoring originally proposed. What the researcher
authored is the rule set, the review at each iteration, and the accept or reject
decision on every item and every anchor.

### 6.2 Single annotator; no inter-annotator agreement

All review was performed by one person. No second annotator reviewed the set,
so no agreement statistic (Cohen's κ or equivalent) can be reported. Category
assignment, anchor selection and the support judgements in §3 are one informed
reader's decisions — documented, but not independently replicated.

### 6.3 Selection effects

The rule-based filtering systematically favours certain evidence. The benchmark
over-represents:

- **Cleanly chunk-contained evidence.** Anchors are drawn from the 81.39% of
  corpus sentences that sit whole under *both* chunk configurations. Evidence
  straddling a boundary — arguably the harder retrieval case — is excluded by
  construction.
- **Unique values.** All 74 anchors have corpus document frequency 1. That
  preference selects evidence with distinctive lexical signatures, which
  favours lexical matching.
- **Prepared remarks.** The Q&A share of anchors fell from 22% to 13% as rules
  accumulated, because conversational speech resists clean anchoring. 10 of 74
  anchors (13.5%) are Q&A. Q&A is where question and passage vocabulary diverge
  most, so this specifically weakens the benchmark's ability to separate dense
  from lexical retrieval. **No claim is made about section effects.**
- **Management speech.** Rule 1 excludes analyst-spoken evidence entirely.
- **Question–passage lexical overlap in licensed items.** Rule 13 wrote a metric
  term into the question in 8 of 40 answerable items (20%): `ref_them_03`,
  `ref_them_08`, `ref_them_09`, `ref_them_15`, `ref_comp_02`, `ref_comp_06`,
  `ref_comp_10`, `ref_comp_11`. Each licensed term appears in or adjacent to the
  anchor, so overlap rises in those items and may mildly favour BM25 and hybrid
  retrieval there. The effect is expected to be small — usually one noun phrase
  — but it is not zero and not randomly distributed: six of the eight are
  thematic or comparative. Per-strategy results should be checked for
  sensitivity to that subset rather than assumed unaffected.

**The consequence, stated plainly:** because the benchmark selects for evidence
that chunk-based retrieval handles well, **absolute retrieval scores are likely
optimistic** relative to a benchmark drawn without these constraints.
**Relative comparisons between the six configurations remain informative**,
since all six face the same questions. Absolute performance should not be read
as an estimate of real-world retrieval quality.

### 6.4 Scale

45 questions, of which 40 are retrieval-scored, across six conditions (twelve
since the 2026-09-03 extension — see the addendum in §1). Adequate
for detecting moderate effects in paired comparison; underpowered for small
effects. Where results are ambiguous this should be stated rather than
over-interpreted. The unanswerable subset (n = 5) is smaller still — abstention
is reported as counts, and no strong claim should rest on it.

### 6.5 Domain and period

US banks only, FY2023–2024, English only. Findings may not generalise to other
sectors, where terminology and disclosure conventions differ.

---

## 7. Accepted weakenings

Two items were knowingly left weaker than ideal rather than being forced to
comply by altering an anchor or an answer.

**`ref_comp_08` — the period-basis contrast could not be preserved.** The item
sets M&T's tangible book value per share against Fifth Third's. The two are
reported on incompatible bases: M&T sequentially and including AOCI, Fifth Third
year-over-year and *excluding* AOCI. The reference answer originally stated both
period qualifiers, but "compared to the end of June" sits outside the M&T anchor
and the Fifth Third anchor stops at "compared to the year", so both were removed
under §3. They cannot be restored: the M&T anchor is already at the 15-word
prepared-remarks cap, and extending the Fifth Third anchor to reach "year ago
quarter" would run to the sentence boundary and breach the edge margin. The
AOCI-basis half of the contrast survives, carried by "excluding AOCI" inside the
Fifth Third anchor. The item remains a valid retrieval target and a valid
faithfulness probe on the AOCI dimension, but it no longer tests whether an
answer notices the sequential-versus-year-over-year mismatch.

**`ref_them_08` — the "up" exception.** See §4. The direction of the JPMorgan
figure is entailed by the anchor but not stated in it, and is retained as a
documented exception.

---

## 8. What is version-controlled, and what is not

`benchmark/questions.jsonl` is the benchmark. It is frozen, and it is the only
benchmark artefact the experiment reads.

Each record carries exactly what a run needs: the question, its
`transcript_ids`, the gold anchors as verbatim strings, the reference answer,
`difficulty_level`, and `chunk_size_sensitive` for the subgroup analysis.
`retrieval_difficulty` and `faithfulness_difficulty` appear only on the one item
whose difficulty was graded separately on the two dimensions, `subtype` only
where set, and `absence_type` and `absence_reason` only on the five
unanswerables.

An unanswerable record carries **`reference_answer: null`**. It has no correct
answer — that is what makes it unanswerable — and the explanation of *why* no
answer exists is held separately in `absence_reason`, beside the
`absence_type` category. Keeping the two apart is deliberate. Were the prose
placed in `reference_answer`, an embedding similarity could be computed against
it and would return a plausible but meaningless number; with `null` such a call
fails loudly instead, and no consumer testing that field can mistake an
unanswerable item for an answerable one.

The calibration material it was selected from — per-item provenance recording
the source sentence and chunk ids behind every anchor, the reasoning behind each
decision, the log of 19 rejected candidates, and the corpus absence evidence for
the unanswerables — is working material and is **not** version-controlled. It
remains available on request for examination, but the repository carries the
finished instrument rather than the machinery that produced it. This document
exists so that the rules are auditable without it.

Before the benchmark was frozen, it was checked mechanically against those
rules: 45 items, the category counts above, 74 gold anchors, unique ids, the
required shape for answerable and unanswerable items, agreement between each
item's `transcript_ids` and the transcripts its anchors are drawn from, a
difficulty level on every item, and — the check that matters most — every one of
the 74 anchors verified as a verbatim substring of the transcript sentence it
was lifted from, and as contained within a single chunk under both the 200-token
and 500-token configurations.
