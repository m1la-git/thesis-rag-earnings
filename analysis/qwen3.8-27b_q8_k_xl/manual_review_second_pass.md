# Second-pass worksheet — manual faithfulness review

Generator: `qwen3.8-27b@q8_k_xl`. 48 items, carried across verbatim from
`analysis/qwen3.8-27b_q8_k_xl/manual_review_packet.md`.

**Piles are deliberately unassigned.** The first pass read each item alone, in a
shuffled order, which is what keeps 48 readings independent. This pass is the
opposite move: put them side by side, decide what actually groups, and name it.
Nothing here proposes a grouping — a pile that arrives pre-named is an artifact
of the tooling rather than a finding about the generator.

## How to use this

1. Read section 3 straight through once without writing anything. It is the
   whole first pass in one view, which the packet deliberately never gives you.
2. Name the piles in section 2 as they suggest themselves. Give each a short
   id (`P1`, `P2`, …) and a definition sharp enough to exclude something.
3. Pile ids go in each row's `pile` cell in section 3; `—` means no mode applies. More than one is fine
   and often right — an answer that names the wrong company AND the wrong
   quarter is both, and picking one loses a real observation. An item that
   resists every pile is telling you the piles are wrong.
4. Put an instrument id in `instr` where the item says something about the
   SCORER or the BENCHMARK rather than the generator. Independent of the pile:
   an item can be a clean answer and still expose a defective rule.
5. Revise the first-pass verdict or failure mode wherever sorting shows it was
   wrong. That is the point of the pass, not a side effect — the `verdict` and
   `failure mode` columns are drafts, and the scorer's `outcome` column is not
   ground truth either.
6. Section 5 is for what neither axis covers. A pile with one member is
   usually a single observation, not a mode — say so there rather than
   promoting it.

## 1. What is being sorted

| | |
|---|--:|
| items | 48 |
| distinct questions | 25 |
| distinct conditions | 12 |
| piles named | 4 |
| instrument findings named | 6 |
| items assigned to a pile | 23 (25 no defect) |

## 2. Piles

Four modes. Each is named by what the generator did, and each definition is
sharp enough to exclude something — an "out" clause that keeps P3 and P4 apart,
and item 34 out of P2.

| id | name (a behaviour, not a category) | definition (what is in, and what is deliberately out) | n |
|---|---|---|--:|
| P1 | gives one company's material under another's name | In: real text from the context presented under the wrong company's name. Out: an answer that names the right company and gets a figure wrong. | 12 |
| P2 | declines the whole when it holds one side | In: a two-part question where one part IS answerable from the context and the answer declines entirely. Out: item 34, where BOTH parts were answerable — see section 5. | 8 |
| P3 | dates material to a period it doesn't come from | In: material assigned to a quarter or year it does not come from. Out: P4, where out-of-window material is used but dated correctly. | 3 |
| P4 | answers outside the asked window, but says so | In: material from outside the asked window, correctly dated, so the reader can see the drift. Out: P3, where the date is moved to fit the question. | 2 |

**13 and 28 sit in two piles each.** Naming the wrong company and dating material
to the wrong period are separate behaviours; an item can do both, and forcing a
single label would drop one of them.

25 of the 48 carry no pile — they are marked `—` in section 3. That is the
no-defect majority, not an unfinished sort.

### 2b. Instrument and benchmark findings — a SEPARATE axis

Not piles. These are claims about the scorer or the benchmark, not about the
generator, and an item can carry one at the same time as a pile. Keeping them
here is what stops an instrument defect from either hiding inside a clean pile
or inflating the failure taxonomy with something that is not a model failure.

| id | finding | what it means for any count computed from the outcome labels | n |
|---|---|---|--:|
| I1 | a correctly-read date is checked as a figure | `extract_numeric_claims` treats a date as a numeric claim and Fix 2 exempts a trivial year only when the QUESTION supplies it. A year read correctly from the context is verified like a quantity, and one is enough to sink a record. | 2 |
| I2 | transparently-marked arithmetic counts as ungrounded | Correct under the stated rule — the figure is absent in any form. What the rule cannot separate is a derivation the answer itself flags from a fabrication. | 1 |
| I3 | n-gram fallback can't see a paraphrase that doesn't copy | With no numeric claims, grounding falls to a shared 6-word run. An accurate answer that paraphrases around short quotations shares none. | 1 |
| I4 | offtarget reflects transcript targeting, not the answer | `answered_grounded_offtarget` says no supporting chunk belonged to the question's own transcript_ids. It is not a judgement on the answer: 12 of the 48 items read as faithful carry it. | 12 |
| I5 | gold anchor doesn't answer its own question | `ref_fact_14`'s anchor is a three-year cumulative and the reference answer drops that scope, so the item cannot score a correct answer as correct. | 1 |
| I6 | identical failure gets two different labels | Item 39 scores `answered_grounded_offtarget` where 11, 26, 27 and 38 — the same substitution — score `answered_ungrounded`. The split turns on whether a bare year happened to go unmatched, nothing about the answers. | 1 |

I4 is the one with reach. The other five are narrow defects; I4 says a whole
outcome label does not mean what its name suggests.

## 3. Items

`#` is the packet's reading number — the item's full text, answer and five
chunks are under that heading in the packet. `outcome` is the scorer's label;
`verdict` and `failure mode` are the first pass's.

| # | pile | instr | question_id | condition | cat | case | outcome (scorer) | verdict (1st pass) | failure mode (1st pass) |
|--:|---|---|---|---|---|:-:|---|---|---|
| 1 | — |  | `ref_them_02` | `chunk200_bm25_enriched` | thematic | C | answered_grounded_correct | faithful | none — one undated inference ("by mid-2024"); Check-3 flag looks like a thematic-question artifact |
| 2 | — | I4 | `ref_them_10` | `chunk200_bm25_enriched` | thematic | B | answered_grounded_offtarget | faithful | none — the offtarget label reflects which transcripts were retrieved, not the answer |
| 3 | P3 |  | `ref_them_04` | `chunk500_dense_enriched` | thematic | C | answered_grounded_correct | unfaithful | period misattribution — USB and MTB material from Q3 2024 dated "early 2024", pulling it inside the asked win… |
| 4 | — |  | `ref_fact_05` | `chunk200_bm25_enriched` | factual | C | answered_grounded_correct | faithful | none |
| 5 | P1 |  | `ref_them_08` | `chunk200_bm25` | thematic | B | answered_grounded_offtarget | unfaithful | company misattribution — BNY Mellon (BK_2024_Q4) reported as Bank of America |
| 6 | P1 |  | `ref_them_08` | `chunk500_dense` | thematic | B | answered_grounded_offtarget | unfaithful | company misattribution — BNY Mellon (BK_2023_Q4) reported as Bank of America, ticker printed beside the wrong… |
| 7 | P4 |  | `ref_them_04` | `chunk500_hybrid_enriched` | thematic | C | answered_grounded_correct | faithful | scope drift — three of four items outside the asked window, but correctly dated |
| 8 | — | I4 | `ref_them_01` | `chunk200_bm25` | thematic | B | answered_grounded_offtarget | faithful | none |
| 9 | — | I4 | `ref_them_15` | `chunk500_bm25_enriched` | thematic | B | answered_grounded_offtarget | faithful | none |
| 10 | — | I1 | `ref_them_15` | `chunk500_dense_enriched` | thematic | B | answered_ungrounded | faithful | date verified as though it were a figure — the answer normalises the context's "'22" to "2022" |
| 11 | P1 |  | `ref_unans_01` | `chunk500_bm25_enriched` | unanswerable | A | answered_ungrounded | should have abstained | company substitution on an unanswerable question — BNY Mellon's AUCA reported as Northern Trust's |
| 12 | P2 |  | `ref_comp_08` | `chunk200_bm25` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 13 | P1 P3 |  | `ref_them_04` | `chunk200_bm25` | thematic | C | answered_grounded_correct | unfaithful | company misattribution — "Barings" attached to BK (BNY Mellon) content; plus STT dated "early 2024" from a Q3… |
| 14 | P1 |  | `ref_them_12` | `chunk200_dense` | thematic | B | answered_grounded_offtarget | unfaithful | company misattribution x2 — Citi's line given to BNY, BNY's line given to Bank of America |
| 15 | P4 | I4 | `ref_comp_01` | `chunk500_dense_enriched` | comparative | B | answered_grounded_offtarget | faithful | out-of-window sourcing — Q2/Q3 2024 characterisations presented for a late-2023/early-2024 question |
| 16 | — |  | `ref_fact_09` | `chunk500_dense_enriched` | factual | C | answered_grounded_correct | faithful | none |
| 17 | — | I1 | `ref_them_12` | `chunk200_hybrid` | thematic | B | answered_ungrounded | faithful | date verified as though it were a figure — the answer normalises the context's "'22" to "2022" |
| 18 | P2 |  | `ref_comp_07` | `chunk200_dense_enriched` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 19 | P2 |  | `ref_comp_12` | `chunk200_dense_enriched` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 20 | — | I4 | `ref_comp_01` | `chunk200_hybrid` | comparative | B | answered_grounded_offtarget | faithful | none — scored offtarget on transcript targeting, not on grounding |
| 21 | — | I4 | `ref_them_06` | `chunk500_dense` | thematic | B | answered_grounded_offtarget | faithful | none — WFC omitted, but it gives no ratio either |
| 22 | — | I4 | `ref_them_10` | `chunk500_hybrid_enriched` | thematic | B | answered_grounded_offtarget | faithful | none |
| 23 | — | I4 | `ref_them_09` | `chunk500_bm25_enriched` | thematic | B | answered_grounded_offtarget | faithful | none |
| 24 | — |  | `ref_fact_01` | `chunk200_hybrid_enriched` | factual | C | answered_grounded_correct | faithful | none |
| 25 | — | I5 | `ref_fact_14` | `chunk200_bm25_enriched` | factual | C | abstained | correct abstention | benchmark defect — the gold anchor is a three-year cumulative, and the reference answer drops that scope |
| 26 | P1 |  | `ref_unans_01` | `chunk200_bm25_enriched` | unanswerable | A | answered_ungrounded | should have abstained | company substitution, plus a unit error ($48.8 billion vs. trillion) leaving the answer self-inconsistent |
| 27 | P1 |  | `ref_unans_01` | `chunk500_bm25` | unanswerable | A | answered_ungrounded | should have abstained | company substitution — BNY Mellon's AUCA reported as Northern Trust's |
| 28 | P1 P3 |  | `ref_them_09` | `chunk200_hybrid_enriched` | thematic | B | answered_ungrounded | unfaithful | wrong company name (FITB as First Interstate) and wrong year (Q4 2023 guidance given as Q4 2024), which inver… |
| 29 | — | I2 | `ref_them_09` | `chunk500_hybrid_enriched` | thematic | B | answered_ungrounded | faithful | none — the flagged claim is the model's own arithmetic, correctly flagged by the stated rule |
| 30 | P1 |  | `ref_comp_10` | `chunk500_bm25` | comparative | C | answered_grounded_correct | unfaithful | company misattribution — Huntington's Q1 2023 capital metrics reported as Fifth Third's, on a comparative que… |
| 31 | — |  | `ref_them_04` | `chunk200_hybrid` | thematic | C | answered_grounded_correct | faithful | selective omission — 968bps reported quoted, 288bps excluding notable items dropped from the same sentence |
| 32 | — |  | `ref_them_07` | `chunk200_dense_enriched` | thematic | C | answered_grounded_correct | faithful | none |
| 33 | P2 |  | `ref_comp_06` | `chunk500_hybrid` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 34 | — |  | `ref_comp_08` | `chunk200_bm25_enriched` | comparative | C | abstained | over-conservative abstention | declines although BOTH sides are present in the asked quarter — the one case here where the conjunction was s… |
| 35 | — | I4 | `ref_them_08` | `chunk200_dense` | thematic | B | answered_grounded_offtarget | faithful | none |
| 36 | P2 |  | `ref_comp_08` | `chunk500_hybrid_enriched` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 37 | — |  | `ref_them_02` | `chunk500_dense` | thematic | C | answered_grounded_correct | faithful | none — GS and JPM language merged into one "banks characterized" opening, acceptable for a thematic question |
| 38 | P1 |  | `ref_unans_01` | `chunk200_bm25` | unanswerable | A | answered_ungrounded | should have abstained | company substitution, mechanism stated outright: "Northern Trust (BK)" |
| 39 | P1 | I6 | `ref_unans_01` | `chunk200_dense` | unanswerable | A | answered_grounded_offtarget | should have abstained | company substitution — BNY Mellon's AUCA reported as Northern Trust's; scored offtarget where the identical f… |
| 40 | — | I3 | `ref_comp_01` | `chunk200_dense_enriched` | comparative | C | answered_ungrounded | faithful | none — no numeric claims, and the n-gram fallback cannot see a faithful paraphrase |
| 41 | — | I4 | `ref_them_08` | `chunk500_dense_enriched` | thematic | B | answered_grounded_offtarget | faithful | none |
| 42 | P2 |  | `ref_comp_12` | `chunk500_dense_enriched` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 43 | — |  | `ref_fact_03` | `chunk500_hybrid_enriched` | factual | C | answered_grounded_correct | faithful | none — right figure chosen against two plausible distractors |
| 44 | P1 |  | `ref_them_04` | `chunk200_bm25_enriched` | thematic | B | answered_grounded_offtarget | unfaithful | company misattribution x3 plus a misattributed executive — every "Bank of America" here is BNY Mellon |
| 45 | — | I4 | `ref_them_11` | `chunk500_hybrid` | thematic | B | answered_grounded_offtarget | faithful | none |
| 46 | — | I4 | `ref_them_05` | `chunk200_hybrid_enriched` | thematic | B | answered_grounded_offtarget | faithful | none |
| 47 | P2 |  | `ref_comp_02` | `chunk500_bm25_enriched` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |
| 48 | P2 |  | `ref_comp_06` | `chunk500_dense` | comparative | C | abstained | correct abstention | all-or-nothing on conjunctive questions (holds one side, declines the whole) |


### 3b. Cross-tabs

Each pile against the three factors the grid varies or the taxonomy splits on.
Counts are observations, not questions — the same question recurs across
conditions, so these do not support a significance claim.

**by arm**

| pile | text_only | enriched | total |
|---|---|---|--:|
| P1 | 8 | 4 | 12 |
| P2 | 3 | 5 | 8 |
| P3 | 1 | 2 | 3 |
| P4 | 0 | 2 | 2 |

**by category**

| pile | factual | thematic | comparative | unanswerable | total |
|---|---|---|---|---|--:|
| P1 | 0 | 6 | 1 | 5 | 12 |
| P2 | 0 | 0 | 8 | 0 | 8 |
| P3 | 0 | 3 | 0 | 0 | 3 |
| P4 | 0 | 1 | 1 | 0 | 2 |

**by case**

| pile | A | B | C | total |
|---|---|---|---|--:|
| P1 | 5 | 5 | 2 | 12 |
| P2 | 0 | 0 | 8 | 8 |
| P3 | 0 | 1 | 2 | 3 |
| P4 | 0 | 1 | 1 | 2 |

**P1 spans all three cases; Check 3 only sees one of them.**

P1's 12 items split A 5 / B 5 / C 2. The attribution-exposure
diagnostic (`check3_enriched`) is computed over Case C `answered_grounded_correct`
only, so of these it can see just 2 — items 13, 30. The Case A and
Case B instances are invisible to it by construction, which means the published
Check 3 figure is a lower bound on this behaviour and not a measurement of it.

## 4. Notes carried forward

The first-pass note for each item, in reading order, so the worksheet stands on
its own. Edit freely — these are drafts.

**1. `ref_them_02` / `chunk200_bm25_enriched`**  
All claims trace (GS 90bps ch1; JPM 45%/2017, modest buybacks, European approach ch2/4/5; MS ch3), and both halves of the question are answered. One unsupported inference: "by mid-2024" — no date appears in the GS chunk. The Check-3 flag looks like an artifact of a question that asks about "banks" generally while the anchors sit on JPM. Label agrees.

second-pass note:

**2. `ref_them_10` / `chunk200_bm25_enriched`**  
Every figure traces and every company is right (AXP ch1/ch3, JPM ch5, WFC ch2, COF ch4); it genuinely answers the question. The quarter labels ("In Q3 2024, JPM...") are asserted rather than stated in the chunks — inferred, and here correct. "offtarget" is about which transcripts were retrieved, not about this answer.

second-pass note:

**3. `ref_them_04` / `chunk500_dense_enriched`**  
Figures all trace (FITB ch1, BAC ch2, USB ch5, MTB ch3), but two period errors: USB is labelled "early 2024 (Q3 2024 context)" and MTB "in early 2024" — both are Q3 2024. Both items also fall outside the asked "late 2023 and early 2024" window, and the mislabelling makes them look in-window. Grounded but not responsive; the label cannot see this. Compare item 7, same question, periods stated correctly.

second-pass note:

**4. `ref_fact_05` / `chunk200_bm25_enriched`**  
Exact, minimal, correct: $826m, ch1 rank 1, no padding. Answers precisely what was asked. Label agrees. Useful as the clean baseline for the rest.

second-pass note:

**5. `ref_them_08` / `chunk200_bm25`**  
JPM (ch1) and BLK (ch3) figures all correct. But the third bullet attributes ch2 — BK_2024_Q4, BNY Mellon — to Bank of America; those are BNY's AUCA and AUM. The State Street bullet is honest that its context is Q1 2024. The label says nothing about the substitution. Compare items 6, 35, 41.

second-pass note:

**6. `ref_them_08` / `chunk500_dense`**  
BLK (ch1) and MS (ch2/ch3/ch4) figures all correct. Again "Bank of America (BK)" for ch5 = BK_2023_Q4, BNY Mellon — the same substitution as item 5 in a different condition. The answer prints the BK ticker beside the wrong name, so the mechanism is visible: it is mapping the ticker to a name.

second-pass note:

**7. `ref_them_04` / `chunk500_hybrid_enriched`**  
Same question as item 3. All four banks correct and periods stated correctly (BAC ch1, FITB ch3+ch4, USB ch2, MTB ch5). Three of four items are 2024/2025, outside the asked window — but here the answer says so rather than relabelling them to fit. Same label as item 3; not the same quality.

second-pass note:

**8. `ref_them_01` / `chunk200_bm25`**  
All four companies and both quarters correct (MTB ch1, JPM ch2, Citi ch3/ch4, WFC ch5). The M&T sentence inverts the chunk's framing but still assigns $29m to Q1 and $5m to Q2 correctly. Directly responsive; "offtarget" here reflects retrieval targeting, not the answer.

second-pass note:

**9. `ref_them_15` / `chunk500_bm25_enriched`**  
Opens by stating that no total tech-spend figure exists — correct. $88bn is correctly framed as a consensus number JPM was still budgeting against (ch4), and $17bn is attributed to the questioner rather than to management (ch5). BLK (ch1/ch3) and FITB (ch2) figures right. Careful about who said what.

second-pass note:

**10. `ref_them_15` / `chunk500_dense_enriched`**  
Every figure traces (Citi ch3, BAC ch1/ch5, MTB ch2, WFC ch4), companies and periods right, and the BAC decade figure correctly tagged "Q2 2023 context". The single flagged claim is "2022", from "$94 million higher than Q4 2022" — a correct reading of ch1's "$94 million higher than the fourth quarter of '22". Mechanism, checked in the scorer: extract_numeric_claims treats a date as a numeric claim, and Fix 2 exempts a trivial year ONLY when the question itself supplies it. This year came from the context, not the question, so it is verified like a quantity — and "2022" appears nowhere in the five chunks in that form. One correctly-read date decides the record.

second-pass note:

**11. `ref_unans_01` / `chunk500_bm25_enriched`**  
Should have abstained. $48.8tn/+5% and $46.6tn/+2% are BNY Mellon's (ch4, ch2), presented as Northern Trust's — a company not in the corpus — with no hedging. The scorer's unsupported claim is "2023", a bare year; the actual failure, the company substitution, is invisible to it. Compare item 24, where the same figure is asked about BNY and answered correctly.

second-pass note:

**12. `ref_comp_08` / `chunk200_bm25`**  
M&T's half is in ch2 verbatim ("tangible book value per share increased 3% compared to the end of June", MTB_2023_Q3). Fifth Third appears only at Q4 2023 — outside the asked quarter — so the comparison the question asks for cannot be made from this context. Answering the M&T half alone would not have answered the question.

second-pass note:

**13. `ref_them_04` / `chunk200_bm25`**  
BAC (ch4) and USB (ch2) correct. Ch1 is BK_2023_Q3 — Robin Vince, BNY Mellon — rendered as "Barings (BK)". Checked: "Barings" appears in none of the five chunks, in no Stage 1 retrieval output, and zero times in the raw corpus, so it is not lifted from the STT chunk or any other; the model supplied it from outside the context. Same class as items 5, 6, 14, 30 and 44 all the same — a real company name attached to another company's content. STT content is right (ch5) but dated "early 2024" when the chunk is Q3 2024. Labelled answered_grounded_correct: a wrong company name is not something a numeric check can see.

second-pass note:

**14. `ref_them_12` / `chunk200_dense`**  
Two of three bullets misattribute. "Bank of New York Mellon (BNY)" is given Citigroup's line from ch1 (C_2023_Q4, "2024 will be a turning point... five businesses"), and "Bank of America" is given BNY's "green shoots" from ch4 (BK_2023_Q4). GS (ch3) is right. The text is real; the speakers are swapped.

second-pass note:

**15. `ref_comp_01` / `chunk500_dense_enriched`**  
Both companies correct and figures trace (GS ch1; Citi ch2/ch4). But the headline characterisations come from GS Q2 2024 and Citi Q3 2024, outside the asked window; only the $14bn is tagged "late 2023". A reasonable answer carrying a label about retrieval targeting.

second-pass note:

**16. `ref_fact_09` / `chunk500_dense_enriched`**  
Exact and complete: $133.5bn, up $1.5bn versus Q1 (ch1 rank 1, verbatim), answering both parts of the question. Label agrees.

second-pass note:

**17. `ref_them_12` / `chunk200_hybrid`**  
All four bullets correct, including BK correctly named "Bank of New York Mellon" (ch4) — the same chunk item 14 gave to Bank of America. The single flagged claim is "2022", from "the 2020–2022 period", a correct reading of ch2's "in 2020 to '22, the COVID years". Same mechanism as item 10: a context-derived date, exempt from Fix 2 because the question did not supply it, checked as if it were a figure. Set beside item 13 — the scorer sinks this answer over a date and passes that one with a company that does not exist in the corpus.

second-pass note:

**18. `ref_comp_07` / `chunk200_dense_enriched`**  
All five chunks are PNC; U.S. Bancorp does not appear at all. PNC's Q3 2023 expense plan is complete in context ($450m CIP goal, $325m staff reductions, >$725m total), but a two-company comparison cannot be built from one company.

second-pass note:

**19. `ref_comp_12` / `chunk200_dense_enriched`**  
All five chunks are PNC_2024_Q1; Capital One does not appear. PNC's NIM (2.57%, down 9bps) is in ch3, but there is no second margin to compare it against.

second-pass note:

**20. `ref_comp_01` / `chunk200_hybrid`**  
Both companies right, both in window (GS Q1 2024 ch4; Citi Q4 2023 ch5), quotes accurate. Notable: it reports that Citi's remarks did not characterise Basel III rather than inventing a characterisation. Correcting my own first note: this record is answered_grounded_offtarget with 0 unsupported claims, NOT ungrounded — the n-gram fallback decided which chunks counted as supporting, and none belonged to the question's own transcript_ids. So there is no scorer false positive here, unlike item 40 where the same fallback produced an ungrounded verdict.

second-pass note:

**21. `ref_them_06` / `chunk500_dense`**  
COF's 43.54% and the flat-to-modestly-down 2024 guide both correct (ch2, ch4). The PNC and Citi bullets correctly state that no ratio was given. WFC (ch1) is ignored, though it gives no ratio either. Reports absence rather than filling it.

second-pass note:

**22. `ref_them_10` / `chunk500_hybrid_enriched`**  
Every figure traces and every company and quarter is right (COF ch1/ch3/ch5, AXP ch2, JPM ch4), covering both growth and credit performance as asked. One of the strongest answers in the set.

second-pass note:

**23. `ref_them_09` / `chunk500_bm25_enriched`**  
M&T (ch1), Huntington (ch2) and BAC (ch4) all correct. It keeps NII and NIM apart for BAC instead of inventing a margin, and states plainly that no adjusted-NIM figures exist for USB or AXP.

second-pass note:

**24. `ref_fact_01` / `chunk200_hybrid_enriched`**  
Exact: $48.8tn, up 5% year-over-year (ch2). This is the same figure the model gave as Northern Trust's in items 11, 26, 27 and 38 — asked about the right company it answers correctly, so that failure is about not abstaining, not about misreading.

second-pass note:

**25. `ref_fact_14` / `chunk200_bm25_enriched`**  
The gold anchor is "over $30 billion in active equity net inflows, while our average AUM has grown", from ch1. Its source sentence is preceded in the same chunk by "over the last three years" — the $30bn is a three-year cumulative, not a Q3 2023 flow. The reference answer ("BlackRock reported over $30 billion in active equity net inflows on its third-quarter 2023 call") drops that qualifier, so a correct answer to the question as read would state a three-year figure as if it answered a question about a quarter. The annotator note flags a basis concern ("a narrower slice than the headline") but not the period. Declining is defensible; the item needs the anchor or the question rescoped before it can score anything.

second-pass note:

**26. `ref_unans_01` / `chunk200_bm25_enriched`**  
Same substitution as item 11, plus a unit error: "$48.8 billion" against ch5's "$48.8 trillion", which leaves the answer inconsistent with its own "$46.6 trillion". The scorer flags neither — "48.8" matches as a string regardless of unit.

second-pass note:

**27. `ref_unans_01` / `chunk500_bm25`**  
Same as items 11 and 26, with units correct here. Three conditions, one fabrication.

second-pass note:

**28. `ref_them_09` / `chunk200_hybrid_enriched`**  
Two real errors, neither caught. "First Interstate BancSystem (FITB)" — FITB is Fifth Third, and the content from ch4 is Fifth Third's. And ch2's "approximately 3% by Q4" is Huntington guiding to Q4 2023, given here as Q4 2024, which makes the closing "Summary of Direction" (305-310 falling to 300) wrong. The flagged claim is instead "300", the model's own basis-point gloss on 3%.

second-pass note:

**29. `ref_them_09` / `chunk500_hybrid_enriched`**  
Accurate throughout (HBAN ch4, BAC ch2, JPM ch3, USB ch5), and honest that the context never separates reported from adjusted NIM. The flagged claim is "3.2", from "up to 10 basis points above that range (i.e., approximately 3.1% to 3.2%)". Checked: 3.2 appears in no chunk in any form — it is the model's own addition, explicitly marked "i.e.". So the outcome label is CORRECT under the documented rule (every numeric claim must appear verbatim); what it does not capture is that a transparent derivation is not a fabrication. A limitation of the rule, not a defect in its implementation.

second-pass note:

**30. `ref_comp_10` / `chunk500_bm25`**  
PNC correct (ch4). Fifth Third's Q2, Q3 and Q4 bullets correct (ch3, ch1, ch2). The Q1 bullet — adjusted CET1 7.6%, TCE 7.27%, TBVPS $9.23 — is Huntington's, from ch5 (HBAN_2023_Q1), presented as Fifth Third's. A full paragraph of one bank's capital metrics under another's name, on a comparative question, labelled answered_grounded_correct.

second-pass note:

**31. `ref_them_04` / `chunk200_hybrid`**  
All correct, including BNY named correctly (ch2) and USB's three figures (ch3, ch4). One selective omission: ch2 gives 968bps reported and 288bps excluding notable items, and only the larger figure is quoted. Same drift beyond the asked window as items 3 and 7.

second-pass note:

**32. `ref_them_07` / `chunk200_dense_enriched`**  
Both companies right, both in Q2 2023, every figure traces (FITB ch1/ch2, BAC ch3). Directly on-question with no scope drift. Label agrees.

second-pass note:

**33. `ref_comp_06` / `chunk500_hybrid`**  
Ch1, at rank 1, is FITB_2023_Q1 and contains exactly the Fifth Third half — "nine points of year-over-year positive operating leverage driven by an 18% increase in revenue". Bank of America appears only at Q4 2023 and Q2 2023, never Q1 2023, so the comparison is unmakeable from this context.

second-pass note:

**34. `ref_comp_08` / `chunk200_bm25_enriched`**  
Unlike items 12 and 36, this condition retrieved both halves for Q3 2023: ch1 (MTB_2023_Q3) has M&T's "tangible book value per share increased 3% compared to the end of June", and ch3 (FITB_2023_Q3_qa) has Fifth Third discussing TBVPS accretion and the AOCI burn-down. The comparison was makeable and was declined anyway. The strongest abstention case in the packet.

second-pass note:

**35. `ref_them_08` / `chunk200_dense`**  
All correct — MS (ch1, ch4), BLK (ch5) — and honest that the STT material is Q1 2024 rather than 2023. No misattribution here, unlike items 5 and 6 on the same question; note that no BNY chunk was retrieved in this one.

second-pass note:

**36. `ref_comp_08` / `chunk500_hybrid_enriched`**  
Ch1 (MTB_2023_Q3) holds the M&T half verbatim; Fifth Third appears only at Q1 2023. Same shape as item 12 under a different condition — one side in period, one side not.

second-pass note:

**37. `ref_them_02` / `chunk500_dense`**  
All correct and well attributed (JPM ch3, GS ch2/ch4, USB ch5), covering both characterisation and capital actions. The opening paragraph merges GS's and JPM's language into a single "banks characterized..." — acceptable for a thematic question, though "way too far" is Solomon's alone.

second-pass note:

**38. `ref_unans_01` / `chunk200_bm25`**  
Same fabrication as items 11, 26 and 27, and here the mechanism is stated outright: "there are two different reporting periods for Northern Trust (BK)". It is mapping the BK ticker onto the name in the question. Everything after that is BNY's real data.

second-pass note:

**39. `ref_unans_01` / `chunk200_dense`**  
Same substitution as items 11, 26, 27 and 38: BNY's $46.6tn/+2% (ch3) presented as Northern Trust's. The label differs only because no bare year went unmatched here — nothing about the answer differs in kind. Four instances of one failure carry two different outcome labels for a reason unrelated to the failure, which is the clearest evidence in the packet that the outcome label is not tracking company identity at all.

second-pass note:

**40. `ref_comp_01` / `chunk200_dense_enriched`**  
Both companies right, both quotes accurate and in window (GS ch1 "fluid" / "meaningfully impact end users"; Citi ch4 "not finalized. It's not in place yet" / CCAR). Checked: the answer contains zero numeric claims, so grounding falls to _shared_ngram_chunk_ids, which returns an EMPTY set — the answer paraphrases around short quotations and shares no 6-word verbatim run with any chunk. The label is what the rule specifies; the rule requires copying, and this answer reads rather than copies.

second-pass note:

**41. `ref_them_08` / `chunk500_dense_enriched`**  
Every figure across both companies traces, with periods and quarters correct (MS ch1/ch2/ch4, BLK ch3). The most complete synthesis in the packet. Again no BNY chunk retrieved and no misattribution — the same pattern as item 35, against items 5 and 6.

second-pass note:

**42. `ref_comp_12` / `chunk500_dense_enriched`**  
All five chunks are PNC and PNC's NIM is in ch5; Capital One is absent. Second condition of this question with the same one-sided retrieval.

second-pass note:

**43. `ref_fact_03` / `chunk500_hybrid_enriched`**  
Exact: $638m (ch1). Three plausible distractors were in context — $449m (Q3 2023) and $461m (Q1 2024) — and it took the right one. Label agrees.

second-pass note:

**44. `ref_them_04` / `chunk200_bm25_enriched`**  
Every "Bank of America" here is BNY Mellon: Robin Vince is BNY's CEO (ch1), the Q1 2024 2%/3% figures are BK_2024_Q1 (ch4), and the "North Star" line is Dermot McDonogh (ch5). Three misattributions plus a named executive. Note the contrast inside the answer — it writes "another bank" and "a bank executive" where it was unsure, and names the wrong bank where it guessed.

second-pass note:

**45. `ref_them_11` / `chunk500_hybrid`**  
All four banks correct with accurate quotes (COF ch1, BAC ch2, USB ch3, FITB ch4), answering both level and direction as asked.

second-pass note:

**46. `ref_them_05` / `chunk200_hybrid_enriched`**  
Correctly restricts to the two banks that report Q3 2024 (STT ch4, FITB ch3), gives the scale comparison the question asks for, and explains why BLK and BNY do not qualify — naming BNY correctly. The dividend residual is flagged as inferred rather than stated.

second-pass note:

**47. `ref_comp_02` / `chunk500_bm25_enriched`**  
Ch2 is BAC_2024_Q1 with the full Bank of America side — 16 office loans charged off, roughly one-third of office exposure reservable criticized, NCO ratio 58bps. Huntington never appears; PNC and WFC arrive instead.

second-pass note:

**48. `ref_comp_06` / `chunk500_dense`**  
Ch2 is the same FITB_2023_Q1 chunk as item 33, with the nine-points/18% sentence intact. Bank of America's Q1 2023 is again absent. Same question, different condition, same correct decline.

second-pass note:

## 5. What neither axis covers


Two single observations. Named here rather than promoted: a pile with one member
is a note about an item, not a mode of the generator.

- **Item 34 — declined with both sides present.** The other eight P2 items decline a
  two-part question whose second part is absent from the asked period, which is
  correct. 34 had M&T's Q3 2023 TBVPS in ch1 AND Fifth Third's in ch3 and declined
  anyway. Keeping it out of P2 is what preserves the distinction; folding it in would
  make P2 look like over-caution when eight ninths of it is not.
- **Item 31 — selective omission.** ch2 gives BNY's 968bps reported and 288bps
  excluding notable items in one sentence; the answer quotes only the larger figure.
  Everything stated is true. One instance, so a note, not a mode — but the direction
  is worth remembering if a second turns up.

## 6. What this changes upstream

The instrument axis is the part of this review that does not belong to the
generator. Each finding has somewhere it has to be recorded, or it is lost when
the piles become prose.

**Nothing here is a licence to change the scorer.** The project's rule on the
abstention match applies to the whole classifier: a divergence found after
results exist is reported and signed off, not fixed, because changing a rule
mid-experiment changes what every already-scored record means. I1-I6 are
disclosures and, at most, candidates for a documented instrument fix on a future
arm — not edits to make now.

| id | lands in | as what |
|---|---|---|
| I1 | README.md, scorer fixes and known defects | a fourth traced defect, alongside Fixes 1-3 — reported, not fixed |
| I2 | README.md, measures (grounding proxy) | a worked instance of the documented conservative bias |
| I3 | README.md, measures (grounding proxy) | the n-gram fallback's failure direction, currently undocumented |
| I4 | README.md measures + thesis RQ2 reporting | a caution on reading the offtarget count as an answer-quality count |
| I5 | thesis §10 | a disclosure — the benchmark is frozen, so it cannot be repaired |
| I6 | README.md, beside I1 | the visible consequence of I1, and the evidence for it |

**I1 — a correctly-read date is checked as a figure.** The existing section
documents three fixes and states Fix 2 is "deliberately narrow": it exempts a
trivial year only when the question supplies it. This review shows what that
narrowness costs — a year read correctly from the *context* is verified like a
quantity, and one is enough to sink a record. It belongs beside Fixes 1-3 with
the same treatment: named, traced to a mechanism, and left in place.

**I2 and I3 — the grounding proxy behaving as specified.** Neither is a defect.
Grounding is by design a mechanical, verbatim-substring proxy, not
a semantic judgment, with a deliberate conservative bias. I2 is that bias
meeting a derivation the answer itself flags; I3 is the numberless-answer
fallback meeting a faithful paraphrase. The fallback's failure direction is not
currently written down anywhere — it should be, in the same paragraph.

**I4 — the one with reach.** `answered_grounded_offtarget` means no supporting
chunk belonged to the question's own `transcript_ids`. It says nothing about
whether the answer is good, and in this sample **12 of 48 items that read as
faithful carry it**. Any sentence that treats the offtarget count as a measure
of answer quality is wrong, and the count is large enough that this is not a
footnote. The taxonomy section defines the label correctly; what is missing is
the caution about reading it.

**I5 — `ref_fact_14` cannot score its own question.** The anchor is a three-year
cumulative and the reference answer drops that scope, so an answer that reports
the figure correctly *as a three-year figure* does not match, and one that
reports it as a quarterly figure is wrong. The corpus and the benchmark are
frozen and the anchors were annotated once, so this is not repairable without
breaking the freeze. Disclose it in §10, with the item named.

**I6 — two labels for one failure.** Items 11, 26, 27 and 38 score
`answered_ungrounded`; item 39, the same substitution, scores
`answered_grounded_offtarget`. The split turns on whether a bare year happened
to go unmatched — I1's mechanism — and nothing about the answers differs in
kind. Report it as evidence that the outcome label does not track company
identity, which is the behaviour P1 is about.

**What P1 implies for Check 3, restated here because it is an upstream claim.**
`check3_enriched` measures attribution exposure over Case C
`answered_grounded_correct` only. P1 spans Case A (5), Case B (5) and Case C
(2), so the diagnostic can see 2 of 12. The published Check 3 figure is a lower
bound on this behaviour, not a measurement of it, and should be reported that
way.
