# Benchmark Construction: Full Process Record

**Thesis:** How retrieval design affects answer quality in RAG-based question answering over earnings call transcripts
**Author:** Kamila Bekkozhina
**Supervisor:** Joe Yu, Chair for Strategy and Organization, TUM
**Status:** Benchmark frozen — 45 questions, 74 gold anchors
**Document purpose:** Complete record of benchmark design decisions, for reference when writing the Methodology chapter

> **Supersedes the earlier process document.** The principal correction is the anchor count: the earlier version stated 75 throughout. The verified figure is **74**, confirmed independently three ways (sum of `gold_anchors`, sum of `provenance` entries, and per-category subtotals). Sections 6 and 8 below also record a construction phase that postdates the earlier document.

---

## 1. Purpose and Scope

This document records how the evaluation benchmark was constructed: what constraints the experimental design imposed, what defects were discovered during construction, what rules were introduced in response, and what limitations remain.

The benchmark exists to measure one thing: whether differences in retrieval configuration (chunk size × retrieval strategy) produce measurable differences in retrieval quality and answer faithfulness. Every design decision below traces back to that requirement.

---

## 2. Constraints Imposed by the Experimental Design

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


### 2.1 Gold passages must be text anchors, not chunk identifiers

The experiment varies chunk size across two conditions (200 and 500 tokens). A chunk identifier is therefore not a stable reference: chunk #47 under the 200-token configuration contains different text than chunk #47 under the 500-token configuration.

An early version of the design specified `gold_passage_ids` referencing specific chunks, with the note that "the corpus must not change afterward." This was corrected before annotation began. Had it not been, every gold label would have required re-annotation when switching chunk conditions.

**The adopted scheme:** each question stores one or more `gold_anchors` — verbatim strings lifted character-for-character from the source transcript. A retrieved chunk counts as a hit if it contains the anchor as a substring. This rule is identical across both chunk configurations, so anchors are annotated once and reused.

### 2.2 Anchors must survive chunking

A consequence of non-overlapping chunks: an anchor straddling a chunk boundary appears in neither chunk, producing a false retrieval miss attributable to chunking rather than to retrieval quality.

Measured across the corpus, 84.67% of sentences are contained within a single chunk at 200 tokens, 93.83% at 500 tokens, and 81.39% under both. All benchmark anchors are drawn from the 81.39% that survive both configurations, verified programmatically rather than by heuristic. (An earlier head/tail probe reported 92%/99.9%; those figures were wrong and were corrected when the exact containment method was implemented.)

Anchors are additionally drawn from the interior of their source sentence, leaving a margin of at least two words at both ends (`MIN_EDGE_MARGIN_WORDS = 2`), so that trimming inward provides headroom beyond sentence-level containment.

### 2.3 Metric definitions follow from multi-anchor questions

Two questions had to be settled before annotation:

**Scoring rule.** Requiring all anchors to match would floor multi-anchor questions near zero across all six conditions — a three-anchor thematic question would need three specific chunks from three specific transcripts inside a top-5 window over a 128-transcript corpus. Questions that score zero everywhere cannot discriminate between configurations, which defeats their purpose.

The adopted metric is fractional:

```
anchor_coverage@5 = (anchors matched in top-5) / (total anchors)
```

Named `anchor_coverage_at_5` rather than `recall_at_5` specifically to signal that it is not standard Recall@5.

**Reciprocal rank.** The initial definition — smallest *k* at which the top-*k* jointly covers all anchors — became inconsistent once coverage went fractional, since a question could score 0.67 coverage and 0.0 MRR. The adopted definition computes reciprocal rank per anchor and averages, with unmatched anchors contributing zero. Both metrics reduce to their standard single-anchor forms.

**Consequence, stated explicitly:** a comparative question retrieving one of two companies scores approximately 0.5 — partial credit, never full credit.

**Cross-category comparability.** Because factual questions carry one anchor and thematic questions carry two or three, the achievable score granularity differs by category: factual items score 0 or 1, three-anchor items score across four levels. Comparisons *between configurations within a category* are valid; comparisons of mean scores *across categories* are not. This must be stated in the Results chapter.

### 2.4 Unanswerable questions are excluded, not zeroed

Questions with no valid answer in the corpus have no anchors. They are excluded from both retrieval metrics entirely and scored only on abstention. Scoring them as zero would penalise correct system behaviour and drag down aggregate metrics.

This is enforced in code (`is_retrieval_scored` returns False) and stated identically in three cross-referencing locations — the metric definitions, the benchmark schema, and the failure-mode taxonomy — so the definitions cannot drift apart. Unit tests confirm that one perfect question plus one unanswerable question aggregates to coverage 1.0 with n_scored = 1, not 0.5.

**Abstention reporting.** With n = 5, abstention accuracy moves in 20-point steps. It is therefore reported as counts ("4 of 5"), not percentages, and the small n is noted as a limitation. The category was kept at 5 deliberately: unanswerable items contribute nothing to the primary research question, and 11% of the set matches the proportion in the approved proposal.

---

## 3. Corpus Foundation

### 3.1 Selection and freeze

The corpus is 128 earnings call transcripts: 16 US bank tickers × 8 quarters (FY2023–FY2024), all with complete quarterly coverage. Source is the `kurry/sp500_earnings_transcripts` dataset (MIT licensed, publicly available).

Because gold anchors are verbatim substrings, corpus stability is a precondition for benchmark validity — an upstream text revision would silently invalidate anchors while leaving transcript identifiers intact. The freeze therefore records:

- a pinned dataset revision (`f3ded372da8d18dc6ad98955c4558e34b5fe6d45`)
- SHA-256 hashes of both `content` and `structured_content` per transcript, with `structured_content` canonicalised to fixed-key-order JSON (the numpy representation is not version-stable)
- a `--verify` mode that re-ingests at the pin, diffs every hash, and fails loudly on any drift

The full remote round-trip was verified to reproduce byte-identical text for all 128 transcripts.

### 3.2 Section segmentation

Each transcript is split into prepared remarks and analyst Q&A. The boundary is the Operator turn opening the question session; all 128 transcripts follow this pattern. Chunking operates within sections, so no chunk spans the boundary.

A real defect was found and fixed here during development: a falsy-index-0 truthiness bug in the section-split heuristic mislabelled JPMorgan transcripts. It was caught through independent verification of a pasted code review, fixed, and re-validated against all 128 transcripts with zero anomalies.

This segmentation matters for the benchmark because speaker role differs systematically between sections — see Rule 1.

### 3.3 Corpus navigation tooling

A deterministic index was built over the corpus to support systematic navigation rather than exhaustive reading. It extracts per transcript: topic labels (keyword/phrase frequency with a finance stopword list), notable figures with their verbatim containing sentences, Q&A themes, and section statistics. Aggregate views include topic frequency, topic co-occurrence by company, and rare-figure identification.

The index uses no LLM calls. It is deterministic (two full runs produce byte-identical output), reproducible, and explainable — properties that matter if the construction process is questioned.

A derived filter (`anchor_candidates`) narrows the 16,875 extracted figure-sentences to the 13,735 contained within a single chunk under both configurations, preserving salience ranking. This is the pool from which factual anchors were drawn.

---

## 4. Question Categories

Four categories, chosen to exercise different retrieval behaviours.

| Category | Count | Anchors each | Anchors total | What it tests |
|---|---|---|---|---|
| Factual | 14 | 1 | 14 | Single-passage retrieval; binary scoring |
| Thematic | 15 | 2–3 | 38 | Distributed evidence across transcripts; graded scoring |
| Comparative | 11 | 2 | 22 | Paired evidence from two companies; partial credit |
| Unanswerable | 5 | 0 | 0 | Abstention under tempting distractors |
| **Total** | **45** | | **74** | |

**Factual** questions target a specific value stated in one transcript. Drawn preferentially from figure-sentences whose value is unique corpus-wide (document frequency = 1), so the answer is unambiguous.

**Thematic** questions ask how a topic was discussed across companies or periods. Multi-anchor by construction, which makes them the most discriminating category: a three-anchor question scores across four distinct levels (0, 0.33, 0.67, 1.0) where a factual question scores 0 or 1.

**Comparative** questions name two companies on the same topic. Exactly two anchors, one per company. These directly exercise the partial-credit property of the fractional metric.

**Unanswerable** questions have no valid answer in the corpus. Three structural sources of absence were used: a company outside the 16 tickers, a period outside FY2023–2024, and a topic never discussed.

---

## 5. Verification Methods

Every anchor is verified programmatically before inclusion:

| Property | Method |
|---|---|
| Verbatim | Exact substring match against the raw `content` field. No normalisation, no whitespace collapsing, no unicode substitution. |
| Contained under both configs | Exact containment check using the production chunking method, not a head/tail heuristic |
| Edge margin | Anchor must leave ≥ 2 words at both ends of its source sentence |
| Word cap | ≤ 15 words for prepared remarks, ≤ 20 for Q&A |
| Document frequency | Corpus-wide count; all 74 anchors are df 1 |
| Speaker role | Derived from turn metadata; all 74 are management-spoken |
| Figure support | Every number in a question or answer cross-checked against its anchor |

Absence for unanswerable questions is *proven*, not assumed: `verify_absence()` re-counts every search term across all 128 raw `content` fields at build time, and a single occurrence anywhere fails the build.

Two verification findings worth recording, because they demonstrate the checks doing real work:

- A planned unanswerable question about Truist was rejected — the term appears 15 times across five transcripts, because Truist Securities is an analyst firm. The competitor/affiliation leak would have made the question partially answerable.
- A planned out-of-range-period question had to be made quarter-specific rather than year-specific. The bare token "2021" appears 81 times as backward comparatives; only "Q2 2021" and its variants return zero.

---

## 6. Quality Rules

Fourteen rules were introduced during construction, each in response to an observed defect. All are enforced at build time except where noted as review-only; the build fails on regression.

The narrative below records what motivated each rule, because the sequence is itself informative: several rules were introduced to fix defects that *earlier* rules had created.

### Rule 1 — Speaker attribution must match the question

**Defect:** three thematic candidates used anchors spoken by analysts (restating figures back to management), while the question asked what banks reported. An analyst restating a number is evidence of what was discussed, not of what the company disclosed.

**Rule:** every provenance entry carries `speaker_role`. If a question asks what a company said, reported, or described, every anchor must be management-spoken.

**Cost:** Q&A anchor share fell, since analyst speech is concentrated there.

### Rule 2 — Reference answers must be supported by anchors alone

**Defect:** one answer completed a clause from text outside its anchor (the anchor ended on "not"; the answer supplied "long-term clients").

**Rule:** no reference answer may assert anything not contained in at least one anchor. Entity, metric, and period may be taken from the question, since the question names them — but no value or qualifier may be imported.

This is the single most consequential rule in the set. Sections 6.13 and 8 record the sweeps required to enforce it fully.

### Rule 3 — Anchors must not end or begin on a syntactic fragment

**Defect:** an anchor ending on "increased by" left the value outside, degrading its answer to "$46.6 trillion, an increase."

**Rule:** separate tail and head stoplists (prepositions, conjunctions, auxiliaries, determiners). The tail rule is broad; the head rule is narrow, since starting on "the" or "our" is fine while starting on "of" is not.

**Cost:** this rule pushed fragmentation downstream into the answers, requiring Rule 8.

### Rule 4 — Thematic questions must span at least two companies

**Defect:** one candidate used three anchors from a single company across three quarters, testing period discrimination rather than cross-company synthesis.

**Resolution:** labelled as subtype `temporal` rather than replaced, since it is the only candidate probing quarter-scoping — the exact failure mode the corpus's quarter-scoping rule exists to prevent. The build now rejects any *unlabelled* single-company thematic.

### Rule 5 — Comparative candidates must not share anchors with thematic candidates

**Defect:** five of six early comparatives reused anchors from thematic candidates, making the two categories non-independent and testing the same passages twice.

**Rule:** asserted in code; the build fails on regression.

### Rule 6 — Difficulty must be framed as question-versus-passage vocabulary

**Defect:** early difficulty reasoning claimed questions were hard because "the anchor omits the query term." This is mostly wrong — retrieval matches chunks, not anchors, so anchor boundaries do not affect what is findable.

**Rule:** difficulty is derived from vocabulary divergence between question and passage. The one genuine anchor-related signal is retained separately: candidates whose source sentence sits whole in one chunk at 500 tokens but splits at 200 are flagged `chunk_size_sensitive`. Seven candidates carry this flag; they are the items that most directly exercise the independent variable.

### Rule 7 — The question's stated period must cover every anchor

**Defect:** introduced by Rule 5. Re-sourcing anchors left questions naming periods their new evidence did not come from — one question asked about Q3 2024 while two of three anchors were from Q2 2023.

**Rule:** any quarter or year named in a question is parsed and checked against every anchor's fiscal period.

### Rule 8 — Reference answers must be complete and must answer the question

**Defect:** introduced by Rule 3. Clean anchors produced answers trailing off mid-clause — "resulting in an efficiency ratio" with no value.

**Rule:** answers must be grammatically complete and must actually answer what was asked. Where Rules 2, 3 and 8 cannot all hold for a sentence, the sentence is unusable and the candidate is reduced or dropped. Two candidates were resolved this way rather than by weakening a rule.

### Rule 9 — Metadata must match current anchors

**Defect:** notes and difficulty labels described anchors that had been replaced — claiming Q&A anchors that no longer existed, or analyst anchors that had been swapped out.

**Rule:** consistency checks between notes, difficulty labels, question text, and current provenance.

### Rule 10 — Answers must name entity, metric, and period

**Defect:** several reference answers were bare figures ("$638 million."). Semantic similarity scoring against a two-word reference is near-arbitrary, which would silently degrade one of three metrics on a sixth of the set.

**Rule:** every answerable reference answer must name the company, the metric, and the period.

**Note:** the first implementation enforced only a word-count minimum, so seven answers passed while still failing the rule as written. This is worth recording as a general lesson — an automated check confirms a rule did not *obviously* fail, not that it passed.

### Rule 11 — Answers must read as prose, not stitched fragments

**Defect:** answers that were grammatical but assembled from anchor spans ("...driven by lower net interest revenue and changes", where "in product mix" sat outside the anchor).

**Rule:** answers are written as prose and checked by reading, not assembled by applying rules to a previous version. This is explicitly a human judgement, stated as such in the code rather than approximated by a regex.

### Rule 12 — Questions must name a time period

**Defect:** introduced by Rule 7. Four questions were made period-neutral to resolve anchor mismatch, producing questions no analyst would ask ("What efficiency ratio levels did banks discuss?" with no time frame).

**Rule:** every question names a period consistent with its anchors — a quarter, a year, or an explicit span.

### Rule 13 — The question licence

**Context:** Rule 2 forbids an answer from asserting anything outside its anchors, but the edge margin frequently places an essential term — usually the metric name — at word index 0 or 1 of its source sentence, where no valid span can reach it.

**Rule:** where a term cannot be brought inside any valid anchor, the *question* may name it, which licenses its use in the answer. The question is part of the item; a term the question supplies is not imported evidence.

**Applied to eight items**, each recorded in the item's notes with the licensed term and the reason extension failed:

| Item | Licensed term | Why extension failed |
|---|---|---|
| ref_them_03 | allowance | "allowance" only at index 1, inside leading margin |
| ref_them_08 | AUM, client investment assets | "AUM" past trailing margin; "Client investment" inside leading margin |
| ref_them_09 | adjusted basis | "adjusted" at index 1 |
| ref_them_15 | G&A | "G&A" opens sentence; extending would destroy chunk-size sensitivity |
| ref_comp_02 | portfolio reduction | "reduced" at index 1 |
| ref_comp_06 | revenue growth | "revenue" past trailing margin in both sentences |
| ref_comp_10 | tangible book value per share | "tangible" inside leading margin |
| ref_comp_11 | non-interest | "Non-interest" at index 0 |

The alternative — waiving the edge margin where containment happens to be verified empirically — was considered and **rejected**, because the margin exists precisely to guarantee containment, and waiving it once would retroactively unblock cases already recorded as unusable. Consistency was preferred over convenience.

**Cost:** see limitation §9.2. This rule raises question–passage lexical overlap in the eight affected items.

### Rule 14 — The answer-verb convention

**Context:** anchors frequently carry a figure without the verb that governs it, so answers necessarily supply one. Some verbs are harmless; others smuggle in information.

**Rule:**

- **Permitted:** a neutral attribution or attainment verb (*said, reported, noted, booked, posted, achieved, generated, took in, repeated, decided*) may be supplied where the anchor carries none. Such a verb asserts only that the company made the statement or reached the figure already in the anchor.
- **Not permitted:** a verb carrying information the anchor does not — in particular the **direction** of a movement (*rose, fell, cut, reduced, grew, up, down*) — unless the anchor carries that direction or the question supplies it.

Directional verbs are licensed through the question under Rule 13 (ref_comp_02 "portfolio reduction", ref_comp_04 "deposit growth", ref_comp_11 "the fall").

**One documented accepted exception:** ref_them_08's "up", where the direction is entailed by the anchor's "driven by market performance and strong net inflows" but not stated in it. Re-sourcing the anchor would have modified a frozen anchor; the exception was recorded instead.

This convention was written down **after the fact**. It records judgements already applied consistently across the file rather than introducing a new standard — but leaving it undocumented would have made a defensible practice look arbitrary.

### Scope-qualifier checks (bidirectional, review-only)

Not numbered rules, but two checks addressing a class Rule 2 does not cover. Rule 2 catches imported *values*; it does not catch imported or dropped *qualifiers* — words like gross, adjusted, tangible, non-interest, core, average, period-end. These change what a figure measures without changing any number.

**Forward check:** flags an answer describing a figure with a scope qualifier present in neither anchor nor question. Caught one candidate whose answer stated a segment-level investment banking figure as firmwide — an error of roughly an order of magnitude, in a candidate specifically built to test that confusion.

**Reverse check:** flags an answer using a noun without a qualifier that its anchor carries. Caught two candidates where removing "tangible" renamed the metric (tangible book value per share and book value per share are different lines).

Both are review-only, since whether a qualifier changes a figure's meaning is a judgement. The word list covers fifteen terms. One special case: "reported" is flagged as a modifier ("on a reported basis") but not as an attribution verb ("M&T reported"), since flagging both would bury real hits in noise.

---

## 7. Construction Process

Construction proceeded in batches with audit passes between them.

**Batch 1 (20 candidates).** Established the schema and provenance format. Concentrated on a subset of the corpus — five tickers unused, prepared remarks dominant, comparatives largely recycled from thematic anchors.

**Batch 2 (20 candidates).** Constrained to complement batch 1: the five unused tickers required, underrepresented quarters targeted, comparative independence enforced, fresh topics only.

**Audit passes (Rules 1–6, then 7–9, then 10–12, then qualifier checks).** Each pass applied newly-formalised rules retroactively to the full set. Several passes introduced defects that the next pass corrected — Rule 3 pushed fragments into answers, Rule 7's fix produced unnatural questions, Rule 10's fix produced period misattribution.

The mechanism causing this was identified and corrected: answers were being *patched* to satisfy each new rule rather than rewritten. The final answer pass rewrote each answer from question and anchors directly, then checked rules against the result. This eliminated the pattern.

**Batch 3 (unanswerable candidates).** Deferred until absence could be verified mechanically against the frozen corpus rather than asserted.

**Rebalancing.** One unanswerable candidate was removed (its absence rested on an interior gap — 2029 happened to be zero while 2028 and 2030 appear — rather than a structural property) and replaced with a thematic candidate, chosen to be chunk-size sensitive with three anchors on an untouched topic.

**Support sweeps (three rounds).** Detailed in §8. These enforced Rule 2 exhaustively rather than by sampling, and produced Rules 13 and 14.

**Externalisation.** The verified candidate set was projected into a lean runtime benchmark file; see §8.4.

18 candidates were rejected during construction and recorded with reasons in `dropped_in_verification`.

---

## 8. The Support Sweeps

This phase postdates the earlier process document and is recorded here in full, because it is where the most subtle defects were found — and because the pattern of what was missed is itself worth reporting.

### 8.1 What the sweeps looked for

A systematic check that every substantive claim in every reference answer traces either to anchor text or to a term the question supplies. Rule 2 had been enforced by sampling; the sweeps enforced it item by item.

Four recurring failure classes emerged:

1. **Period qualifiers past the anchor end** — "four quarters", "ago quarter", "compared to the end of June", "we posted in 2023", "in the prior year"
2. **Metric names taken from outside the anchor** — the G&A, net-interest-income, and allowance cases
3. **Scope qualifiers** asserted without anchor or question support
4. **Comparison bases** stated without support

### 8.2 What the sweeps found

Round one found and fixed unnamed measures in ref_them_08 and a metric-name failure in ref_them_15. Round two found the ref_comp_02 period qualifier. Round three — after two rounds had reported clean — found two further instances of the *same* failure class already fixed twice: ref_fact_13 ("in the prior year") and ref_comp_06 (two clauses naming revenue).

**This is the finding most worth recording.** A defect class can be identified, named, fixed in the items where it was noticed, and still persist elsewhere in the same file. The sweeps only converged once the check was run item-by-item against a named list of failure classes, rather than by re-reading for problems in general.

### 8.3 What was accepted rather than fixed

Two weakenings are recorded as permanent, with reasons:

- **ref_comp_08** — the sequential-versus-year-over-year contrast could not be restored. The M&T anchor is already at the 15-word cap and extending the Fifth Third anchor would breach the edge margin. The AOCI-basis half of the contrast survives. The item is weaker as a faithfulness probe than intended.
- **ref_them_08** — the directional "up", accepted under Rule 14 as an entailed-but-unstated direction.

Both are stated in the annotation protocol rather than buried in item notes.

### 8.4 Externalisation and the two-file architecture

The verified set was split into two artifacts:

| File | Role |
|---|---|
| `analysis/benchmark_authoring/reference_candidates.json` | Calibration and audit trail. Working material, not version-controlled. Carries provenance, notes, the full SUPPORT FIX history, difficulty prose, concerns, and `dropped_in_verification`. Hand-authored; unregenerable. |
| `benchmark/questions.jsonl` | Runtime artifact. Thirteen fields consumed by `evaluate.py` and `run_experiment.py`, five of them optional and omitted where they do not apply. Generated, never hand-edited. |

`analysis/benchmark_authoring/build_benchmark.py`, kept with the calibration file outside version control, projects the second from the first and asserts eleven invariants before writing: item count, category counts, anchor total, id uniqueness, unanswerable shape, answerable shape, transcript/provenance consistency, difficulty values, verbatim anchor-in-source-sentence, anchor/provenance agreement, and a substantive absence explanation on every unanswerable. A `--check` flag verifies sync without writing, and was tested in both directions.

This split makes the "reference material, NOT the benchmark" claim structurally true rather than a note at the top of a file.

### 8.5 The anchor count correction

The working figure was 75 throughout construction. An independent recount during the final review returned 74. The discrepancy was resolved programmatically: `sum(len(gold_anchors))` = 74, `len(provenance)` = 74, and per-category subtotals (14 + 38 + 22 + 0) = 74 all agree.

**74 is the correct figure** and is the one to use in the thesis. Any earlier note, draft, or summary stating 75 is superseded.

### 8.6 Splitting the absence explanation from `reference_answer`

Found after the first runtime artifact was committed, by the test suite rather than by review.

**Defect:** the five unanswerable records carried an `ABSTAIN — …` string in `reference_answer`. `tests/test_evaluate.py` asserts that field is null for the category, per CLAUDE.md, so the committed benchmark failed its own suite.

**Why null rather than prose.** The text was an explanation of why no answer exists, not an answer, and `reference_answer` means "the correct answer to this question". The distinction is not cosmetic: with a string in that field, `is_similarity_scored` is the *only* thing preventing an embedding cosine being computed against it, which would return a plausible and entirely meaningless number rather than failing. With null, such a call raises loudly if the guard is ever bypassed, and no consumer testing `if record["reference_answer"]` can read an unanswerable item as answerable. Defence in depth, not spec compliance.

**Why the prose was kept.** Deleting it was the first proposal and was wrong. The calibration file is not version-controlled, so the tracked benchmark would have retained only the `absence_type` label — a tag, where the prose is the argument for why the item is genuinely unanswerable. That argument is what an examiner would ask for.

**Resolution:** `reference_answer: null`, with the text moved to a new `absence_reason` field beside `absence_type`. The projection strips the `ABSTAIN — ` prefix, which had been doing the work the field name now does. `analysis/benchmark_authoring/build_benchmark.py` gained an eleventh assertion requiring every unanswerable to carry a substantive explanation, since an empty one is lost evidence rather than a cosmetic gap.

The calibration file was **not** modified — the prose already sat in its `reference_answer`, so the split happens during projection. One source of truth, still frozen, same SHA-256.

**Worth recording as a general point:** this defect survived the freeze, the support sweeps, and a manual review pass. It was caught by an automated test asserting a schema property, not by reading. §6 Rule 10 records the converse lesson — that an automated check confirms only what it checks. Both are true, and the pairing is the useful observation: the sweeps caught what reading catches, the suite caught what reading does not.

---

## 9. Final Composition

**45 questions, 74 anchors.**

| Category | Count | Anchors |
|---|---|---|
| Factual | 14 | 14 |
| Thematic | 15 | 38 |
| Comparative | 11 | 22 |
| Unanswerable | 5 | 0 |
| **Total** | **45** | **74** |

| Anchors per question | Questions |
|---|---|
| 0 (unanswerable) | 5 |
| 1 | 14 |
| 2 | 18 |
| 3 | 8 |

**Coverage:** all 16 tickers, all 8 quarters represented. Q&A-sourced anchors: approximately 13%.

**Chunk-size sensitive:** 7 items.

**Difficulty distribution:** every item carries a categorical `difficulty_level` (easy / medium / hard) alongside the original prose reasoning. One item (ref_them_09) additionally carries split `retrieval_difficulty` and `faithfulness_difficulty`, being easy to retrieve and hard to answer faithfully.

**Verification status:** 74/74 anchors verbatim, contained under both configurations, edge-clear, within word caps, document frequency 1, management-spoken. Zero unsupported claims in reference answers. Absence proven for all 5 unanswerable questions. Fourteen rules and both qualifier checks green.

---

## 10. Limitations

These belong in the thesis and should be stated plainly rather than minimised.

### 10.1 Construction method

Candidates were generated by a large language model operating over the frozen corpus under progressively formalised rule constraints, with each iteration reviewed by the researcher and defects identified through that review driving the next rule. The researcher did not author each question independently from a first reading of the transcripts.

This differs from the manual authoring originally proposed. What the researcher authored is the rule set, the review at each iteration, and the accept or reject decision on every item and every anchor.

### 10.2 Selection effects

The rule-based filtering systematically favours certain evidence. The benchmark over-represents:

- **Cleanly chunk-contained evidence.** Anchors are drawn from the 81.39% of sentences whole under both configurations. Evidence that straddles boundaries — arguably the harder retrieval case — is excluded by construction.
- **Unique values.** The df-1 preference selects evidence with distinctive lexical signatures, which favours lexical matching.
- **Prepared remarks.** Q&A share fell from 22% to 13% as rules accumulated, because conversational speech resists clean anchoring. Q&A is where question and passage vocabulary diverge most, so this weakens the benchmark's ability to separate dense from lexical retrieval. **No claims should be made about section effects.**
- **Management speech.** Rule 1 excludes analyst-spoken evidence entirely.
- **Question–passage lexical overlap in licensed items.** Rule 13 added a metric term to the question in 8 of 40 answerable items (20%), each time a term appearing in or adjacent to the anchor. This raises lexical overlap in those items and may mildly favour BM25 and hybrid retrieval there. The affected items are named in §6 Rule 13, and six of the eight are thematic or comparative — so per-strategy results should be checked for sensitivity to that subset rather than assumed unaffected.

The consequence: because the benchmark selects for evidence that chunk-based retrieval handles well, absolute retrieval scores are likely optimistic relative to a benchmark drawn without these constraints. **Relative comparisons between the six configurations remain informative**, since all configurations face the same questions — but absolute performance should not be read as an estimate of real-world retrieval quality.

### 10.3 Single annotator

All review was performed by one person. No inter-annotator agreement was measured. Standard for a bachelor thesis; would require validation in a published study.

### 10.4 Scale

45 questions, of which 40 are retrieval-scored, across six conditions — twelve since the 2026-09-03 extension of the grid (see the addendum in §2). Adequate for detecting moderate effects in paired comparison; underpowered for small effects. Where results are ambiguous, this should be stated rather than over-interpreted.

The unanswerable subset (n = 5) is smaller still. Abstention accuracy is reported as counts, and no strong claim should rest on it.

### 10.5 Domain and period

US banks only, FY2023–2024, English only. Findings may not generalise to other sectors, where terminology and disclosure conventions differ.

### 10.6 Two authoring gaps in a frozen artifact

Both were found after the benchmark was frozen, so neither is repairable: the corpus and the anchors were annotated once, and editing either now would invalidate every scored record. They are grouped because they share that status and that cause — a benchmark-authoring decision that only became visible downstream — and separated because they fail in different ways and license different sentences.

**`ref_fact_14` — the gold anchor does not answer its own question.** Found in the q8 manual faithfulness review as instrument finding I5 (`analysis/qwen3.8-27b_q8_k_xl/manual_review_second_pass.md` §4, routed to the thesis limitations by that document's §6 table). The anchor is a three-year cumulative figure while the reference answer drops that scope, so an answer reporting the figure correctly *as a three-year figure* does not match the reference, and one reporting it as a quarterly figure is wrong. The item cannot score a correct answer as correct. **Affects one item of 40, and it is named** — this is a defect in a specific record, bounded and countable, and any result that turns on `ref_fact_14` should say so.

**`difficulty_level` — the field cannot be reproduced as a measure.** §6 Rule 6 states the principle ("difficulty is derived from vocabulary divergence between question and passage") and records the defective reasoning it replaced, but neither this document nor `annotation_protocol.md` operationalises it: there is no metric for "vocabulary divergence" and no easy/medium/hard cut-point. The only mechanical check is `analysis/benchmark_authoring/build_benchmark.py` invariant 8, which asserts membership in `{easy, medium, hard}` and nothing more. The per-item reasoning exists — free text such as *"easy — question vocabulary matches the passage almost word for word"* — but it lives in `reference_candidates.json`, which §8 of the annotation protocol places deliberately outside version control. **Affects the whole field, on all 45 items**, and is not a defect in any one of them.

> **DISPUTED FIGURE — marked 2026-09-09, deliberately not reconciled.** This sentence previously gave the distribution as *7 easy / 26 medium / 7 hard*. Those three numbers sum to **40**, not to the 45 items the same sentence describes. Read directly from the frozen `benchmark/questions.jsonl`, the distribution is **a different set of three numbers that does sum to 45**. Which is correct has not been established, and reconciling them would mean choosing one without evidence, so neither is recorded here. **Do not cite any difficulty distribution — in this document, in the claims map, or in the thesis — until the discrepancy is resolved against the frozen artifact.** Nothing depends on it: no analysis is keyed on `difficulty_level`, and the disclosure of this limitation does not require the counts. The same disputed figure was propagated to `analysis/claims_map.md` §11 and is marked there too.

**Where they differ, and what each licenses.** `ref_fact_14` is a wrong value in one place; `difficulty_level` is a right-looking value everywhere whose derivation cannot be audited. So the first is disclosed and worked around — report it, name it, exclude it where it would distort. The second is not disclosed-and-used but disclosed-and-not-used: the field remains a legitimate *annotation*, and an unreproducible annotation is a poor basis for a reported result, so no analysis is keyed on it. That is why it is absent from the descriptive-statistics table (`analysis/stage1/descriptives.md`) while `chunk_size_sensitive` — same kind of field, but with a mechanical definition, a source sentence whole in one chunk at 500 tokens and split at 200 — is present.

The contrast is the point worth making in the thesis: a hand annotation is only as citable as its written-down rule, and the two fields differ in exactly that respect rather than in care taken.

---

## 11. Notes for the Methodology Chapter

Suggested structure for the benchmark subsection:

1. **Design constraints** (§2) — why anchors rather than chunk IDs; why fractional scoring; why cross-category comparison is invalid. These follow from the experimental design and are worth stating early, since they explain otherwise unusual choices.
2. **Corpus and freeze** (§3) — brief; the reproducibility apparatus is a strength and takes two sentences.
3. **Categories** (§4) — the table plus a paragraph on why thematic and comparative carry the discriminating power.
4. **Verification** (§5) — the Truist and 2021 examples are worth including as concrete evidence that absence was proven rather than assumed.
5. **Quality rules** (§6) — do not list all fourteen. Summarise the classes (speaker attribution, anchor integrity, answer support, metadata consistency) and note that rules were introduced in response to observed defects, with the full set documented in the repository. Rules 13 and 14 are worth naming individually, since they are the ones with a measurable effect on the data.
6. **Limitations** (§10) — in full, particularly §10.1 and §10.2.

The most defensible framing is that benchmark construction was itself an iterative empirical process, with each rule motivated by a specific observed failure. That is true, it is unusual to document at this level of detail, and it is more interesting than a claim of clean single-pass design.

The §8.2 finding — that a named defect class survived two rounds of fixing before an item-by-item sweep caught the remainder — is worth a sentence in the Discussion as well. It is a small, concrete result about verification practice, and it costs nothing to report.

**Three things to avoid:**

- describing the questions as manually authored
- presenting absolute retrieval scores without the §10.2 caveat
- quoting 75 anchors anywhere; the figure is 74
