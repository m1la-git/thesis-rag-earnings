# Stage 2 diagnostics

Investigation only — no changes to `evaluate.py`, the runner, the taxonomy, retrieval,
the benchmark, or any results file. Everything below is derived from the persisted
`results/generation/*`, `results/retrieval/*.jsonl`, `results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv`,
and read-only calls into `evaluate.py`'s existing functions (`classify_outcome`,
`extract_numeric_claims`, `transcript_id_from_chunk_id`).

---

## Correction

My earlier summary said "chunk200_hybrid has zero Case B/C ungrounded." **Wrong — the
breakdown table itself shows chunk200_hybrid with 3 `answered_ungrounded` in Case B.**
Zero applies to **Case C only** (`chunk200_hybrid` Case C: 3 abstained, 6 correct, 0
offtarget, 0 ungrounded). Case B for that condition is 20 abstained, 1 correct, 7
offtarget, **3 ungrounded**. Correcting it here since it was about to go into the thesis;
if you'd copied the earlier summary anywhere else, it needs the same fix.

---

## Check 1 — the 12 Case B `answered_grounded_correct` items

All 12, with full retrieved-chunk text, generated answer, and a precise per-claim
grounding trace (which chunk supports which specific number, and whether that chunk's
transcript is one of the question's own gold `transcript_ids`). Method: for every numeric
claim in the answer (`evaluate.extract_numeric_claims`), checked which retrieved chunks
contain it verbatim and whether any of those chunks' `transcript_id`
(`evaluate.transcript_id_from_chunk_id`) is in the question's own `transcript_ids`.

**Headline, revised from a simple (a)/(b) split to what the evidence actually shows:**

| classification | n | meaning |
|---|--:|---|
| (a) Genuine redundant evidence | **8** | the answering fact is verbatim in a retrieved chunk from the gold transcript(s) — legitimate, not the annotated anchor sentence but a different, equally real occurrence |
| Classifier exposure — substantive fact off-target, "correct" via a trivial/coincidental digit | **3** | the number that actually answers the question comes only from a non-gold transcript; the on-target check passes only because an unrelated bare year or coincidental digit also appears in a gold-transcript chunk |
| Distinct pattern — soft abstention missed by exact-match, then scored on noise | **1** | the model actually declined (in its own words, ending with the exact ABSTENTION sentence), but a preamble before it means `answer == ABSTENTION` is False, so it fell into the outcome classifier and got tagged via incidental digits |
| (b) Parametric leakage (fact in neither gold nor retrieved chunk, from pretraining) | **0** | none found |

**Zero parametric leakage across all 12** — every substantive number traces to some real
retrieved chunk. `ref_fact_02` — your specific concern — is (a), cleanly, not (b): see below.

### `ref_fact_02` across all three conditions — the case you flagged

Question: *"What did American Express raise its full-year EPS guidance to in the third
quarter of 2024?"* Gold anchor: `"raising our full year EPS guidance to $13.75 to
$14.05,"` — gold transcript `AXP_2024_Q3`.

**All three conditions (`chunk500_bm25`, `chunk500_dense`, `chunk500_hybrid`) retrieve
the identical chunk `AXP_2024_Q3_prepared_remarks_500_000` at or near rank 1**, and all
three answers are effectively identical: *"American Express raised its full-year EPS
guidance to between $13.75 and $14.05."*

The reason coverage@5 reads 0 (Case B) despite this: **AXP_2024_Q3 states the figure
twice, in different words, at two different points in the call.** Confirmed directly
against the raw transcript content:

```
occurrence #1 (in the retrieved chunk, Stephen Squeri's opening remarks):
"...ong earnings we're generating, we are raising our full-year EPS guidance to
between $13.75 and $14.05, up from $13.30 to $13.80. And we continue to expect
full-year revenue growth..."

occurrence #2 (the annotated gold anchor, elsewhere in the transcript, not in
this condition's top-5):
"...he beginning of the year. We are also raising our full year EPS guidance to
$13.75 to $14.05, reflecting both the momentum and the earnings power of our
business. This represents 2..."
```

Note "We are **also** raising" in occurrence #2 — the transcript itself signals this is
a restatement. Hyphenation ("full-year" vs "full year") and phrasing ("between X and Y"
vs "X to Y") differ just enough that the exact-substring anchor test correctly reads 0
for occurrence #1, while occurrence #1 is nonetheless a complete, correct, verbatim
answer to the question, from the gold transcript, retrieved and used correctly by the
model in all three conditions. **This is classification (a), and it's the cleanest
possible example of it** — three independent conditions converging on the same figure is
exactly what you'd expect when the fact is stated twice in the source and the retriever
keeps finding the more prominent (rank-1, opening-remarks) occurrence, not evidence of
parametric leakage. Full chunk text (identical across all three conditions):

```
[AXP_2024_Q3_prepared_remarks_500_000]
...Stephen Squeri: Good morning, and thanks for joining us for our third quarter
earnings call. We had another strong quarter that reflects the steady earnings
power of our business model and our continued investments for growth. Earnings
per share in the third quarter were $3.49 and revenues were $16.6 billion, up 8%
over last year, marking our 10th consecutive quarter of record revenues. Based
on our performance to date and the strong earnings we're generating, we are
raising our full-year EPS guidance to between $13.75 and $14.05, up from $13.30
to $13.80. And we continue to expect full-year revenue growth that is within
the guidance range we provided at the beginning of the year at around 9%.
```

### The other 7 genuine (a) cases (verbatim-confirmed, substantive claim in a gold chunk)

| condition | question_id | fact confirmed verbatim in gold-transcript chunk |
|---|---|---|
| chunk200_bm25 | ref_fact_08 | `BLK_2023_Q2_prepared_remarks_200_012`: *"BlackRock generated $190 billion of total net inflows in the first half of 2023"* |
| chunk200_dense | ref_them_02 | `JPM_2023_Q3_prepared_remarks_200_007`: *"...does not mandate a 25% increase in capital requirements"* |
| chunk200_hybrid | ref_them_02 | `JPM_2023_Q3_prepared_remarks_200_006`: *"...we would see a 45% increase in our capital requirements relative to that 2017 starting point"* |
| chunk500_bm25 | ref_them_11 | `BAC_2024_Q2_prepared_remarks_500_009`: *"Net charge offs of $1.5 billion were little changed... net charge off ratio was 59 basis points"* (the BAC portion; MTB and USB — the question's other two target companies — go unaddressed, replaced by FITB and COF, which are not in `transcript_ids` at all) |
| chunk500_dense | ref_comp_07 | `PNC_2023_Q3_prepared_remarks_500_006`: *"This initiative will decrease the workforce by 4% and is expected to reduce 2024 expenses by approximately $325 million"* — and the model correctly declines the USB half rather than fabricating it (a clean partial-context case) |
| chunk500_dense | ref_fact_02 | see above |
| chunk500_hybrid | ref_fact_02 | see above |

### The 3 exposure cases — "correct" resting on a coincidental digit, not the real fact

These are documented in full in Check 3 below (they're the same mechanism). Short version:

- **`chunk200_bm25 / ref_them_12`** — the cited margin figures (12%, 17%, 25%) are all
  from `BK_2023_Q4` and `MS_2023_Q4`, neither a gold transcript (`BK_2023_Q3`,
  `MS_2023_Q3`). The on-target pass comes only from the bare token `"2023"` also
  appearing, coincidentally, in a gold `BK_2023_Q3` chunk about an unrelated topic (the
  Wove platform).
- **`chunk500_dense / ref_comp_10`** — the cited AOCI figures ($2.6B, $400M, $12.6B) all
  come from `PNC_2023_Q4`, `PNC_2023_Q2`, `FITB_2023_Q4` — none of them the gold
  `PNC_2023_Q1` / `FITB_2023_Q2`. On-target passes via bare `"2023"` plus a genuinely
  striking coincidence: the claim `"30"` (from *"tangible book value... grew nearly 30%"*)
  matches the gold `FITB_2023_Q2` chunk purely because that chunk separately says
  *"we have already delivered nearly $30 billion of our 10-year $100 billion
  commitment"* — a completely unrelated community-investment figure that happens to
  share the digits "30."
- **`chunk500_dense / ref_them_13`** — the ETF figures ($2.8T, 60%) are only in
  `BK_2024_Q4`, not any of the three gold quarters (`BK_2023_Q3`, `BK_2024_Q2`,
  `BK_2024_Q3`). On-target passes only via bare `"2023"` in a `BK_2023_Q3` chunk about an
  unrelated topic (culture/hiring).

### The 1 soft-abstention case

**`chunk500_bm25 / ref_comp_01`** — full answer: *"Based on the provided context, there
is no information regarding how Citi characterized Basel III endgame uncertainty. The
text for Citi's Q4 2023 earnings call focuses on strategic progress, services rankings,
and general priorities without mentioning Basel III. Therefore, a comparison between
Goldman Sachs and Citi cannot be made using only the provided context.\n\nThe provided
context does not contain enough information to answer this question."* The model
**did decline** — it ends with the exact canonical sentence — but the preamble before it
means `answer == ABSTENTION` is `False`, so `abstained_exact_match` reads `False` and the
record fell through to the outcome classifier. The only numeric claims in that whole
passage are `"4"` and `"2023"` (both trivial), which happen to co-occur in the gold
`GS_2023_Q4` chunk (*"Our effective tax rate for 2023 was 20.7%"*, *"$4.9 billion"*) for
reasons unrelated to anything about Citi or Basel III. This item is not really "answered"
at all in the sense the four-way taxonomy is meant to capture, and its `_correct` tag is
an artifact of that mismatch, not evidence about grounding quality one way or the other.

---

## Check 2 — grounding verdict stability (`ref_fact_09`, `ref_fact_05`)

**Verdict: classifier instability, not legitimate divergence.** In both cases the
generated answer is byte-identical across conditions (confirmed — same text, and the
core supporting evidence is present identically in both conditions' retrieved sets), and
the outcome flips solely because of an auxiliary, non-distinguishing digit picked up (or
not) by coincidence in each condition's other retrieved chunks.

### `ref_fact_09` — "M&T's average loans and leases, Q2 2023"

Gold anchor: `"average loans and leases were $133.5 billion during the second quarter,
up $1.5 billion compared"` (`MTB_2023_Q2`).

Answer (identical, both conditions): *"M&T's total average loans and leases were $133.5
billion during the second quarter of 2023, representing an increase of $1.5 billion
compared to the linked quarter."*

Both `chunk200_bm25` and `chunk200_dense` retrieve `MTB_2023_Q2_prepared_remarks_200_008`
— the chunk with the actual answering fact:

```
[MTB_2023_Q2_prepared_remarks_200_008]
...Turning to slide 13, we talk about the drivers on the loan growth. The total
average loans and leases were $133.5 billion during the second quarter, up $1.5
billion compared to the linked-quarter. Looking at the loans by category on an
average basis compared to the first quarter...
```

The $133.5B and $1.5B claims are supported identically in both conditions. **The
divergence is entirely the auxiliary claim `"2023,"`** (with a trailing comma) —
`extract_numeric_claims`'s regex `\d[\d,]*(?:\.\d+)?` treats a comma immediately after a
digit run as a possible thousands-separator and keeps consuming, so "...second quarter of
2023, representing..." extracts as the literal string `"2023,"`, comma included. Whether
that exact 5-character sequence — punctuation and all — happens to appear somewhere in a
condition's other 4 chunks is what decides the verdict:

- `chunk200_bm25`'s other chunks (`MTB_2023_Q1_qa_200_007`, `FITB_2024_Q1...`,
  `MTB_2023_Q1_prepared_remarks_200_007`, `FITB_2024_Q3...`) — none contains `"2023,"`
  verbatim → **unsupported → `answered_ungrounded`**.
- `chunk200_dense`'s other chunks include `PNC_2023_Q2_prepared_remarks_200_014`
  (*"...first half of **2023,** third quarter expectations..."*) and
  `MTB_2023_Q3_prepared_remarks_200_007` (*"...for the third quarter of **2023,** down
  1%..."*) — both happen to contain the literal substring `"2023,"`, in sentences about
  completely unrelated PNC and M&T-Q3 content → **supported → `answered_grounded_correct`**.

### `ref_fact_05` — "Capital One's Walmart-related build, Q2 2024"

Gold anchor: `"quarter, as you said, first, we had the effect of Walmart, the $826
million build"` (`COF_2024_Q2`).

Answer (identical, both conditions): *"The Walmart-related build that Capital One called
out as an adjusting item in the second quarter of 2024 was $826 million."*

Both `chunk200_bm25` and `chunk200_hybrid` retrieve `COF_2024_Q2_qa_200_000` — the chunk
with the actual fact:

```
[COF_2024_Q2_qa_200_000]
...Andrew Young: Sure, Sanjay. Well, let me start by covering this quarter's
allowance and then I'll talk about the future. So in the quarter, as you said,
first, we had the effect of Walmart, the $826 million build that we spelled out
as an adjusting item. We also reserved for the growth we saw in the quarter...
```

$826 million is supported identically in both. **The divergence is the auxiliary claim
`"2024"`** — echoed from the question's own framing ("...in the second quarter of
2024"), not asserting new information. Whether a bare `"2024"` happens to appear in a
condition's other chunks decides the verdict:

- `chunk200_bm25`'s other 4 chunks (`COF_2024_Q3_prepared_remarks_200_002`,
  `COF_2024_Q4_prepared_remarks_200_002`, `COF_2024_Q2_prepared_remarks_200_002`,
  `COF_2024_Q4_qa_200_027`) — none spells out the bare digits `"2024"` as literal text
  (dates are implicit from context, not stated) → **unsupported → `answered_ungrounded`**.
- `chunk200_hybrid`'s other chunks include `COF_2024_Q3_prepared_remarks_200_011`:
  *"We had guided to **2024** annual operating efficiency ratio, net of adjustments...we
  now expect the full year **2024** annual operating efficiency ratio..."* — an entirely
  unrelated efficiency-ratio guidance sentence that happens to spell out "2024" →
  **supported → `answered_grounded_correct`**.

### Root cause, stated precisely

Two compounding issues, both in `extract_numeric_claims`/`classify_outcome`, not in the
generator: (1) the regex's comma-handling turns an ordinary sentence-punctuation comma
into part of the "number," producing a claim string unlikely to recur verbatim by chance
in most chunks but liable to when it does; (2) the checker extracts and separately
verifies *every* digit sequence in the answer, including a bare year the model is simply
echoing from the question's own phrasing rather than asserting as a distinguishing fact.
Neither of these numbers is what actually answers the question — $133.5B/$1.5B and $826M
are — and those are supported identically in both conditions of each pair. **This is a
genuine reliability problem worth flagging as a headline caveat, not expected behaviour**
— the same claim against materially equivalent evidence is being scored differently, and
the mechanism is now fully traced.

---

## Check 3 — what `grounding_basis: numeric` actually verifies

> **LABEL SET: PRE-FIX.** This section was computed on the **pre-fix** labels,
> before the three scorer fixes of 2026-09-03. Its populations are the pre-fix
> ones: Case C `answered_grounded_correct` **n=26** and
> `answered_grounded_offtarget` **n=42**. Its headline figures — **7 of 26
> (27%)** and **39 of 42 (93%)** — are therefore statements about that label set
> and **must not be quoted against any post-fix table**.
>
> **Post-fix figures: 9 of 30 (30%) and 55 of 58 (95%)** — see
> `analysis/qwen3.8-27b_q4_k_xl/check3_attribution_postfix.md`, which re-runs this diagnostic
> unchanged in method (including its own 2022–2026 / 1–4 triviality rule, which
> is deliberately NOT `evaluate.is_trivial_claim`) over the post-fix labels, and
> breaks out the four records the fixes promoted into Case C correct — records
> this section never examined. That script reproduces the 7/26 and 39/42 below
> exactly when run against the pre-fix population, which is what licenses its
> post-fix numbers.
>
> This section is **left unmodified and unrecomputed** as the pre-fix record.

**Confirmed, precisely: the check verifies that every extracted number in the answer
appears *somewhere* in the retrieved top-5 text, verbatim. It does not verify *which*
chunk, company, quarter, or metric that number is attributed to in the answer's own
sentence.** `classify_outcome`'s on-target/off-target distinction is a separate,
coarser check layered on top: "correct" requires only that *at least one* of the chunks
supporting *any* of the answer's numbers belongs to a target transcript — it does not
require that the SPECIFIC number sitting next to a given company name in the answer text
is the one grounded in that company's own transcript.

**Direct answer to your question: yes, an answer can attach a correct figure to the
wrong company, wrong quarter, or wrong metric, and the current check will not catch it
if any other number anywhere else in the same answer happens to hit a target-transcript
chunk (or, per Check 1's `ref_comp_01`, even if that other number is a bare, irrelevant
year).**

### Quantified exposure

Method: for each item, checked whether at least one *non-trivial* numeric claim (i.e.
excluding bare years 2022–2026 and the digits 1–4, which recur too often to be
distinguishing) is supported **only** by chunks from a transcript **not** in the
question's own `transcript_ids` — a proxy for "a substantive figure is attached to an
unverifiable company/quarter."

| population | n | items with ≥1 substantive claim traceable only to an off-target transcript |
|---|--:|---|
| Case C `answered_grounded_correct` | 26 | **7 (27%)** |
| `answered_grounded_offtarget` (all cases) | 42 | **39 (93%)** |

The offtarget number is expected and not itself concerning — "offtarget" is supposed to
mean the substantive content is off-target, so 93% having exactly that property confirms
the check is doing its basic job for that category (the other 3/42 are presumably
on-target via a coincidental trivial digit while genuinely being off-target in substance
— the same failure mode as `ref_comp_01`, just landing on the offtarget label instead of
correct).

**The Case C number is the one that matters for the thesis: 7 of the 26 "correct,
grounded" answers (27%) have at least one substantive figure that cannot actually be
verified as belonging to the company/quarter/metric the answer attaches it to** — of
which, per Check 1's deeper read, 3 (`ref_them_12`, `ref_comp_10`'s Case-B twin at
`chunk500_bm25`, and the `ref_them_13`/`ref_fact_02` family) have this as their *entire*
basis for passing, not a minor secondary issue.

### Two more concrete examples (beyond `ref_fact_02`, `ref_them_12`, `ref_comp_10`,
`ref_them_13` already detailed above)

**`chunk200_bm25 / ref_them_06`** (Case C `answered_grounded_correct`) — claims `"65"`
(→ `GS_2023_Q4`, a non-target transcript) and `"57"` (→ `FITB_2024_Q2`, also non-target)
are the only support for those specific figures; the item nonetheless reads
`answered_grounded_correct` because some other claim in the same answer hits a genuine
target transcript.

**`chunk500_bm25 / ref_them_04`** (`answered_grounded_offtarget`) — claims `"180"` (→
`BK_2023_Q4`), `"190"` and `"200"` (→ `USB_2024_Q4`) are all attributed in the answer to
specific companies/quarters that don't match where the digits actually came from.

Full per-claim traces for every item in both populations are reproducible from
`results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv` plus `evaluate.extract_numeric_claims` /
`evaluate.transcript_id_from_chunk_id` — the script used for this check is not part of
the frozen pipeline (diagnostic only, per your instruction not to add code), but the
method is exactly `classify_outcome`'s own logic run per-claim instead of collapsed to a
single boolean.

### What this means for the limitations section

State it as: the automated grounding classification verifies factual presence, not
factual attribution. It reliably catches a number invented from nowhere (true
`answered_ungrounded` cases are numbers absent from all 5 retrieved chunks, which the
per-claim trace confirms is a clean, unambiguous check). It does **not** reliably catch a
real number lifted from the wrong place and re-attached to the wrong company, quarter, or
metric in the generated prose — that failure mode is currently indistinguishable, by this
mechanism alone, from genuine on-target grounding, and affects on the order of a quarter
of the items currently labeled `answered_grounded_correct`. The manual faithfulness check
on a human-read subset is exactly the layer that would catch this;
this mechanical check was never meant to replace it, and this diagnostic is the concrete
evidence for why that layer still matters.

---

# Follow-up on the re-scored results (three checks before write-up)

Reporting only — no changes to the scorer, the fixes, the taxonomy, retrieval, the
benchmark, or any results file in this pass.

## 1 — Case A, complete

Case A is unaffected by all three fixes: **identical outcome counts and identical
per-item labels, before and after, for all 30 Case A records.**

| outcome | old | new | delta |
|---|--:|--:|--:|
| abstained | 27 | 27 | +0 |
| answered_grounded_correct | 0 | 0 | +0 |
| answered_grounded_offtarget | 1 | 1 | +0 |
| answered_ungrounded | 2 | 2 | +0 |

**The 2 ungrounded were not year-echo artifacts — they, and the 1 offtarget, are all the
same single question (`ref_unans_01`, Northern Trust) in 3 conditions, and the mechanism
in every case is a genuine claim, not a scorer bug.**

Northern Trust is not in the frozen corpus (per the benchmark's own `absence_type:
out_of_corpus_company`), so this question has no correct grounded answer by
construction. All three non-abstained records instead answer with **The Bank of New
York Mellon's (BK)** real, correctly-quoted custody-bank figures — a substantive
company-identity conflation by the model (Northern Trust and BNY Mellon are both
large custody banks; nothing in the taxonomy fixes touches this):

**`chunk200_bm25 / ref_unans_01`** — outcome: `answered_ungrounded`
> "Based on the provided context, there are two different reporting periods for
> Northern Trust (BK):\n\n1.  In Q3 2023, ETFs Assets Under Custody/Administration
> were up over 20% year-over-year. The total assets under custody/administration and
> related investment services fees grew in the mid-single digit percentage
> range.\n2.  In Q1 2024, firm-wide assets under custody and administration were $48.8
> trillion, which was up 5% year-over-year.\n\n(Note: The context also mentions Q1 2023
> figures of $46.6 trillion, up 2% year-over-year, but the most recent specific figure
> provided is for Q1 2024.)"

Claim(s) driving the classification: `unsupported_claims = ['2023', '2023']` — both
occurrences of the bare year "2023" (from "Q3 2023" and "Q1 2023") do not appear as
literal text in the retrieved chunks' indexed content, even though the chunks are
genuinely from BK's 2023 transcripts — consistent with Stage 1's Part 5 finding that
company/period text is frequently absent from the indexed chunk string itself. Not
excluded by Fix 2, because the question never mentions any year at all ("What were
Northern Trust's assets under custody and administration, and how did they change
year-over-year?") — nothing to echo.

**`chunk200_dense / ref_unans_01`** — outcome: `answered_grounded_offtarget`
> "Northern Trust's firm-wide assets under custody and/or administration were $46.6
> trillion, which increased by 2% year-over-year."

`unsupported_claims = []` — every claim (46.6, 2) is verbatim in a retrieved BK chunk.
Offtarget rather than ungrounded because it's fully grounded, just in BK's transcripts,
not Northern Trust's (which don't exist). This is the mechanically-guaranteed case
the taxonomy already documents: Case A's `transcript_ids: []` makes
`answered_grounded_correct` impossible by construction, and this is what "impossible,
lands on offtarget instead" looks like in practice.

**`chunk500_bm25 / ref_unans_01`** — outcome: `answered_ungrounded`
> "In the first quarter of 2024, Northern Trust's firm-wide assets under custody
> and/or administration were $48.8 trillion, representing a 5% increase year-over-year.
> In the first quarter of 2023, these assets stood at $46.6 trillion, which was up 2%
> year-over-year."

Claim: `unsupported_claims = ['2023']` (one occurrence, from "first quarter of 2023") —
same mechanism as the bm25/200 case.

**Reading:** these 3 are a real, reportable finding about the generator (it substitutes
a topically-similar in-corpus company for one that's absent, rather than abstaining
cleanly, in 3 of 6 conditions for this specific question) — not a scorer defect. Worth a
line in the thesis's Case A discussion; not something these fixes could or should touch.

## 2 — The 15 Case B ungrounded flips, verified per-claim

> **SCOPE CORRECTION (added later, after a full counterfactual re-score).** This
> section is **Case B only**, and its result is correct as such — but do not
> quote it in an unqualified form. Neither "Fix 2 caused zero of the ungrounded
> flips" nor "all numeric flips traced purely to the comma regex" is true of the
> re-scoring as a whole.
>
> Across all 270 records: **19 records left the `answered_ungrounded` label and
> none entered it. 17 are attributable to Fix 1 (the comma regex), 1 to Fix 3
> (soft abstention detection), and exactly 1 — `chunk200_bm25/ref_fact_05` — to
> Fix 2, the question-echoed trivial claim exclusion. Within Case B
> specifically, Fix 2 caused zero of the 15 flips** (the statement below).
> `ref_fact_05` is Case C, and is the only record where the exclusion rule alone
> promotes an item into `answered_grounded_correct`.
>
> The mechanism there is the one Fix 2 was specified for: a bare year the
> question itself supplied, where the verdict otherwise depended on whether an
> unrelated chunk happened to spell out the same year. It is named rather than
> absorbed into an aggregate. Verified by `analysis/fix_attribution.py
> --decompose`; the script states the attribution rule
> and names the two rule-sensitive records (`ref_them_07`, `ref_them_14`).

**Result: Fix 2 caused none of the 15 Case B flips.** Every one of the 14 numeric-claim-based
flips is fully explained by Fix 1 alone — the specific claim that was "unsupported"
under the old scorer was, in every single case, a trailing-comma artifact (`"2024,"`,
`"2023,"`, `"8,"`, `"2,"`, `"2021,"`, `"2022,"`, `"2025,"`) that Fix 1's corrected regex
parses as the clean number (`"2024"`, `"2023"`, etc.), and that clean number is then
found verbatim in a retrieved chunk **without needing Fix 2 to exclude anything**. Fix
2 does remove additional trivial-and-echoed claims from these same answers (most of
them mention "2023"/"2024" many times), but in every one of the 15 cases, removing
those additional claims was never what flipped the outcome — the single previously-
unsupported claim was already resolved by Fix 1 before Fix 2 ever mattered. Traced by
replaying the OLD regex against the frozen cached answer text, and independently
re-deriving the NEW pre-filter and post-filter claim lists, for all 15 flips.

**Zero anomalies** — no flip rests on any mechanism other than Fix 1 or Fix 3 as
specified; nothing indicates Fix 2 reaching further than the bare-year/quarter-integer,
question-echoed rule it was written for.

**Mechanism split, as requested:** 1 moved to `abstained` (Fix 3), 14 moved to
`answered_grounded_offtarget` (Fix 1), 0 moved to `answered_grounded_correct`.

| condition | question_id | new outcome | old unsupported claim(s) | mechanism |
|---|---|---|---|---|
| chunk200_bm25 | ref_them_01 | offtarget | `2024,` ×4, `2,` | Fix 1 (comma artifact) |
| chunk200_bm25 | ref_them_03 | offtarget | `2023,`, `3,`, `4,` | Fix 1 |
| chunk200_bm25 | ref_them_14 | offtarget | `2023,` | Fix 1 |
| chunk200_dense | ref_them_03 | offtarget | `2023,` ×4 | Fix 1 |
| chunk200_dense | ref_them_08 | offtarget | `2022,`, `2024,` | Fix 1 |
| chunk200_dense | ref_them_11 | offtarget | `2023,` | Fix 1 |
| chunk200_hybrid | ref_them_03 | offtarget | `2023,` ×4 | Fix 1 |
| chunk200_hybrid | ref_them_15 | offtarget | `2023,` | Fix 1 |
| chunk500_bm25 | ref_them_06 | offtarget | `2024,` | Fix 1 |
| chunk500_bm25 | ref_them_07 | offtarget | `8,` | Fix 1 |
| chunk500_bm25 | ref_them_08 | offtarget | `2021,` | Fix 1 |
| chunk500_dense | ref_them_01 | offtarget | `2024,` ×3 | Fix 1 |
| chunk500_dense | ref_them_03 | offtarget | `2023,` ×3, `2024,` ×2 | Fix 1 |
| chunk500_dense | ref_them_10 | offtarget | `2024,` ×2, `2025,` | Fix 1 |
| chunk500_hybrid | ref_them_07 | **abstained** | *(none — short-circuits before any claim check)* | **Fix 3** |

The question text for each (shown because you asked to see it, even though no claim was
actually excluded via question-echo for any of these 15): `ref_them_01` "How did banks
report the impact of the FDIC special assessment on their expenses in late 2023 and the
first half of 2024?"; `ref_them_03` "What did banks say about their office and
commercial real estate credit exposure and the allowance against it during 2023?";
`ref_them_14` "What did banks report about investment banking revenue and fees across
2023 and 2024?"; `ref_them_08` "How did firms describe momentum in net inflows, AUM and
client investment assets during 2023?"; `ref_them_11` "How did banks characterise their
net charge-off levels and direction in 2023 and 2024?"; `ref_them_15` "How much did
banks say they were spending on technology over 2023 and 2024, and how did that spend
and related G&A expense change?"; `ref_them_06` "What efficiency ratio levels and
targets did banks discuss across 2023 and 2024?"; `ref_them_07` "How did banks describe
deposit growth in the second quarter of 2023?"; `ref_them_10` "What did banks say about
credit card growth and card credit performance over 2023 and 2024?" — every one of
these questions names a bare year in its own text (mostly "2023 and 2024"), which is
exactly why Fix 2's post-filter list also drops those years from these same answers —
but, again, that drop is not what resolved the old-unsupported claim in any of these 15
cases; Fix 1 alone already did.

One item, `chunk500_hybrid / ref_them_07`, resolves differently: its old-scorer
unsupported claim was never checked at all under the new scorer, because
`contains_abstention_sentence` catches this response as a soft abstention before
`classify_outcome` ever reaches the numeric-claim path. See Check 3 below for its full
text — this is the same item as `ref_them_07`'s bm25 sibling in the table above, but a
different condition (`chunk500_hybrid` vs `chunk500_bm25`), so it is a different
generation, not a duplicate row.

## 3 — `ref_them_07` / `chunk500_hybrid`, for your judgement

**Question:** "How did banks describe deposit growth in the second quarter of 2023?"

**Gold anchors:** `"during the quarter, increasing by $2.7 billion or 1.9%"`,
`"total period-end deposits increased 1% sequentially and increased 2% year-over-year
as compared to a 5%"` — gold transcripts `HBAN_2023_Q2`, `FITB_2023_Q2`. Neither
transcript is among this condition's retrieved top-5 (Case B, `coverage@5 == 0`).

**Full response, verbatim:**

> "Based on the provided context, there is no information describing how banks
> described deposit growth specifically for the **second quarter of 2023**. The
> available text contains data regarding:
>
> *   **Wells Fargo (Q3 2023):** Mentions average deposits declined 5% from a year ago
>     and stabilized in Corporate and Investment Banking, but does not provide specific
>     Q2 2023 growth figures or descriptions.
> *   **First Interstate BancSystem (FITB) (Q1 2023):** Provides an outlook for the
>     *second quarter of 2023*, stating they expected average deposits to be "stable to
>     up 1% on a sequential basis." However, this is a forward-looking expectation made
>     in Q1, not a description of actual results after the quarter ended.
> *   **M&T Bank (Q1 2023):** Discusses full-year expectations and Q1 results but does
>     not describe Q2 2023 deposit growth.
>
> Therefore, the context only contains an *expectation* for Q2 2023 from FITB, not a
> description of actual performance or general industry descriptions for that specific
> quarter.
>
> The provided context does not contain enough information to answer this question."

(Note in passing, not part of the judgement call: the response mislabels the second
bullet's company — the ticker FITB is Fifth Third Bancorp, not "First Interstate
BancSystem." The chunk itself, quoted below, never uses either full name.)

**All 5 retrieved chunks, verbatim, in rank order:**

```
[WFC_2023_Q3_prepared_remarks_500_006]
real estate office portfolio yet. However, we do expect higher losses over time, and
we continue to increase the coverage ratio in our commercial and -- in our CIB
commercial real estate office portfolio from 8.8% at the end of the second quarter to
10.8% at the end of the third quarter.  On Slide 7, we highlight loans and deposits.
Average loans were down modestly from both the second quarter and a year ago. While we
continue to have good growth in credit card loans from the second quarter, most other
portfolios declined. I'll highlight specific drivers when discussing our operating
segment results. Average loan yields increased 195 basis points from a year ago and 24
basis points from the second quarter due to the higher interest rate environment.
Average deposits declined 5% from a year ago predominantly driven by deposit outflows
in our consumer and wealth businesses, reflecting continued consumer spending and
customers reallocating cash into higher-yielding alternatives. Average deposits also
declined in Commercial Banking, while they stabilized in Corporate and Investment
Banking. As expected, our average deposit costs continued to increase, up 23 basis
points from the second quarter of 236 basis points with higher deposit costs across
all operating segments in response to rising interest rates. However, the pace of the
increase has slowed, and our percentage of average noninterest-bearing deposits
decreased modestly from the second quarter to 29% but remained above prepandemic
levels. Turning to net interest income on Slide 8. Third quarter net interest income
was $13.1 billion, up 8% from a year ago, as we continued to benefit from the impact
of higher rates. The $58 million decline from the second quarter was due to lower
average deposit balances, partially offset by 1 additional day in the quarter and the
impact of higher interest rates. Last quarter, we increased our expectations for full
year 2023 net interest income growth to approximately 14% compared with 2022, which
was up from our expectation of 10% growth at the beginning of the year. We now expect
full year 2023 net interest income growth to grow by approximately 16% compared with
2022 with the fourth quarter 2023 net interest income expected to be approximately
$12.7 billion. The expected decline in interest income in the fourth quarter was
primarily driven by our assumptions for additional deposit outflows and migration from
noninterest-bearing to interest-bearing deposits as well as continued deposit
repricing, including continued competitive pricing on commercial deposits. Turning to

[WFC_2024_Q3_prepared_remarks_500_004]
quarter. $128 million of this decline was due to the increased pricing on sweep
deposits and advisory brokerage accounts and wealth and investment management that we
highlighted on last quarter's call. This was the lowest linked-quarter decline in net
interest income since third quarter 2023, as customer migration to higher yielding
deposit products continued to slow and the pace of deposit pricing increases also
decelerated. Deposit costs were up 7 basis points in the third quarter with
approximately half of this increase driven by the pricing increase on sweep deposits in
advisory brokerage accounts. The third quarter increase in deposit costs was lower than
the 10 basis point increase in the second quarter and the 16 basis point rise in the
first quarter. In response to the Federal Reserve rate cut in September, we have
reduced rates on promotional deposit offers in our consumer businesses. Pricing on
sweep deposits and advisory brokerage accounts, which are aligned to money market
funds, will continue to move in-line with Fed rate cuts. Commercial deposit pricing is
responding quickly to Federal Reserve rate reductions, just as it did when rates were
rising. We are continuously monitoring competitive conditions and deposit trends and
will adjust pricing, tenor, and new balance requirements based on our observations. We
highlight loans and deposits on Slide 5. Average loans were down from both the second
quarter and a year ago with continued growth in credit card loan balances more than
offset by declines in most other categories. I'll highlight specific drivers when
discussing our operating segment results. Average deposits increased $1.4 billion from
a year ago and growth in our customer deposits enabled us to reduce higher cost
corporate treasury deposits. Average deposits were down $4.8 billion in the second
quarter. This decline was driven by an $18.5 billion reduction in higher-cost corporate
treasury deposits, while customer deposits grew $13.7 billion from the second quarter.
All else equal, a reduction in corporate treasury deposits is a positive for net
interest income in the current environment. Turning to non-interest income on Slide 6.
We had strong growth in non-interest income up 12% from a year ago. As Charlie
highlighted, this growth reflects the benefits of the investments we've been making in
our businesses as well as market conditions. We grew non-interest income across most
categories, including double-digit increases year-over-year in many of our largest
fee-generating activities, including investment advisory, net gains from trading
activities, deposit-related fees and investment banking. We also benefited from
improved results in our

[MTB_2023_Q1_prepared_remarks_500_007]
fund earning asset growth. We expect continued intense competition for deposits in the
face of industry-wide outflows. Full year average total deposit balances are expected
to be down low single digits compared to the $158.5 billion average during 2022.
During the first quarter, we issued $3.5 billion in senior debt and we'll utilize the
combination of FHLB funding and senior debt over the course of this year as needed to
ensure that we can continue to meet the loan demands of our customers. We continue to
expect the deposit mix to shift toward higher cost deposits with declines expected in
demand deposits and growth in time and on balance sheet suite. This is expected to
translate to a through-the-cycle interest-bearing deposit beta in the high 30% to low
40% range. Taking all of these factors into account, we anticipate the net interest
margin to be slightly below 4% for the full year of 2023 and to continue to migrate
towards the long-term range we have been discussing for the past couple of quarters.
Next, let's discuss the drivers of earning asset growth. We currently plan to grow the
securities portfolio by $2 billion compared to the $28 billion balance at the end of
March of this year with the addition of longer duration mortgage-backed securities
throughout the year. Looking at average loans. We expect average loan and lease
balances during 2023 to grow in the 10% to 12% range when compared to the 2022 full
year average of $119.3 billion. We anticipate growth to continue in the second
quarter. and then for average balances to be flat to slightly down over the second
half of the year. This implies total average loan and lease balances in the fourth
quarter of 2023 to be up 1% to 3% and from the $129.4 billion average during fourth
quarter of 2022. The mix of C&I, CRE and consumer loans, inclusive of consumer real
estate, is almost one-third each as of the end of March. We expect this trend to shift
slightly as C&I growth outpaces CRE. As we have seen over the past three quarters,
Higher levels of interest rates are expected to slow down the growth in our consumer
loan book in 2023. After these average loans grew 2% in the first quarter, we expect
the indirect portfolio to be relatively flat over the remainder of the year. Turning to
fees. Excluding the $136 million gain on

[FITB_2023_Q1_prepared_remarks_500_005]
current outlook, we expect full year average total loan growth between 2% and 3% which
reflects our cautious outlook on the economic environment. We expect total commercial
loans to increase in the low to mid-single digits area compared to 2022 which implies
modest incremental growth from the first quarter through year end given our outlook
for a tempered lending environment in the second half of the year. We expect line
utilization rates to remain stable. We expect total consumer loan growth to also be
modest as a strong increase from dividend finance will be mostly offset by a decline
in auto and mortgage. We continue to expect approximately $4.5 billion in dividend
loan production for the year given the secular tailwinds and our investments in the
business combined with market share gains. We expect deposits to be stable or grow
from the first quarter average level as we progress throughout 2023 consistent with
our strong customer acquisition trends. Within that, we expect continued migration
from DDA into interest bearing products throughout the remainder of 2023 with the mix
of demand deposits to total core deposits, declining from 32% today to 30% by year
end. For the second quarter of 2023, we expect average total loan balances to be
stable to up 1% sequentially with growth fairly balanced between commercial and
consumer portfolios. We expect average deposits to also be stable to up 1% on a
sequential basis. Shifting to the income statement, we expect full year NII will
increase 7% to 10%. As other banks have noted, industry wide deposit pricing pressures
intensified in the wake of the Silicon Valley and Signature Bank failures. Therefore,
as shown in our presentation materials, we are providing NII guidance under a range of
deposit betas given potential diverging levels of intensity with respect to deposit
competition going forward. The upper end of our NII guidance assumes an approximate
terminal beta of 43%, and the lower end assumes approximately a 49% terminal beta
compared to our January expectation of 42%. The midpoint of our NII outlook translates
to a 47% beta with total interest bearing deposit costs increasing 45 basis points or
so in the second quarter, and another 25 basis points in the second half of the year.
Our outlook also considers the lag effects from previous rate hikes and continued DDA
migration and assumes the Fed hikes 25 basis points in May, and then holds short term
rates of 525 basis points for the remainder of the year. Our guidance assumes that our
securities portfolio balances decline a couple billion dollars between now

[FITB_2024_Q2_prepared_remarks_500_006]
the second half of 2024. Given the year-to-date trends in customer activity, we now
expect full-year average total loans to be down 3% compared to 2023. Average total
loans in the fourth quarter of 2024 are expected to be stable to up 1% compared to the
fourth quarter of 2023, with similar performance in both the commercial and consumer
portfolios. Customer demand is the primary driver of this change, given the interest
rate environment and other economic uncertainties. If there's more economic optimism
in the second half of the year, we would expect to see loan growth in-line or better
than market growth. We are forecasting fourth quarter average core deposit growth of
2% to 3% when compared to the fourth quarter of 2023. Our forecast also assumes
commercial revolver utilization and our cash and other short-term investments remain
relatively stable throughout the remainder of 2024. We expect full-year adjusted
non-interest income to be stable to down 1% in 2024, reflecting the impact of weaker
than previously expected credit demand and customer hedging activities. We expect
strong growth in commercial payments and wealth and asset management revenue to
continue. In response to this expectation of lower customer activity in the second
half. We expect to manage full year adjusted non-interest expense stable to 2023
levels. Our expense outlook estimates efficiency ratio of around 57% for the full
year.
```

**My own reading, stated in one or two sentences, not resolved:** the response never
asserts the WFC/FITB/MTB figures *as the answer* — every one is immediately paired with
an explicit reason it doesn't count ("does not provide specific Q2 2023 growth
figures," "a forward-looking expectation... not a description of actual results," "does
not describe Q2 2023 deposit growth") — which reads to me as reasoning-through-the-
evidence-to-a-decline rather than a partial answer; but it is a longer and more
evidence-laden decline than `ref_comp_01`'s, and I can see the case for reading it the
other way. Yours to decide.

### Scope of the grey-area scan

The reverse check in the previous pass ("0/167 abstentions carrying extra content")
was run over `abstained_exact_match == True` **and separately, in full, over all 169
`abstained_soft_match == True` rows** — not only the exact-match ones — specifically
because the exact-match set can never contain extra content by construction (equality
requires it), so limiting the check to that set would have been circular. Confirmed:
**exactly 2** responses in all 270 contain the canonical sentence with non-whitespace
content beyond it — `ref_comp_01` and `ref_them_07`, both already covered above. No
other item in the grid sits in this grey area.
