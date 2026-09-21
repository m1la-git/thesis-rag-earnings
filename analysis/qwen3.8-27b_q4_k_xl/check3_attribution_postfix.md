# Check 3 (attribution exposure) — POST-fix label set

**Label set: POST-fix** (`results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv`), i.e. after
the three scorer fixes of 2026-09-03. Populations: Case C
`answered_grounded_correct` **n=30**, `answered_grounded_offtarget`
(all cases) **n=58**.

This **supersedes for post-fix purposes** the Check 3 table in
`analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md`, which was computed on the **PRE-fix** label
set (n=26 and n=42) and remains valid only as a statement about those labels.
The earlier file is unmodified and stays part of the audit trail.

## Method (unchanged from the original)

An item is flagged when at least one **substantive** numeric claim in its answer
is supported ONLY by chunks from a transcript outside the question's own
`transcript_ids` — i.e. a figure the answer attaches to a company/quarter that
cannot be verified as belonging there.

`substantive` = not a bare year 2022–2026 and not a bare digit 1–4. **This is the
diagnostic's own rule, deliberately preserved, and is NOT
`evaluate.is_trivial_claim`** (2000–2030, plus Fix 2's echoed-by-question
conjunct). Keeping the original rule is what makes the pre/post difference a
population change rather than a population change confounded with a method change.

Claim extraction uses the corrected (Fix 1) regex, since the point is to
characterise the current instrument. `--validate` re-runs this same code over the
pre-fix population with the pre-fix regex and reproduces the published 7/26 and
39/42 exactly, so the implementation is faithful and the post-fix figures below
are a real change rather than a reimplementation artifact.

## Results

| population | label set | n | flagged | % |
|---|---|--:|--:|--:|
| Case C `answered_grounded_correct` | pre-fix (published) | 26 | 7 | 27% |
| Case C `answered_grounded_correct` | **post-fix** | **30** | **9** | **30%** |
| `answered_grounded_offtarget` (all cases) | pre-fix (published) | 42 | 39 | 93% |
| `answered_grounded_offtarget` (all cases) | **post-fix** | **58** | **55** | **95%** |

## The four newly-promoted Case C records

Promoted into `answered_grounded_correct` by the fixes, so never examined by the
original Check 3. **2 of 4 flagged.**

| condition | question | substantive claims | off-target-only claims | flagged |
|---|---|--:|---|---|
| chunk200_bm25 | ref_fact_05 | 1 | — | no |
| chunk200_bm25 | ref_fact_09 | 2 | — | no |
| chunk200_dense | ref_them_15 | 5 | 1.1 -> BAC_2023_Q4,WFC_2023_Q4; 52.6 -> WFC_2023_Q4; 6 -> BAC_2023_Q4,BLK_2024_Q1,WFC_2023_Q4; 12 -> BAC_2023_Q4,BLK_2024_Q1 | **YES** |
| chunk500_hybrid | ref_them_04 | 3 | 190 -> USB_2024_Q4; 200 -> USB_2024_Q4 | **YES** |

## Flagged Case C `answered_grounded_correct` items (post-fix)

| condition | question | off-target-only claims |
|---|---|---|
| chunk200_bm25 | ref_them_02 | 90 -> GS_2024_Q2 |
| chunk200_bm25 | ref_them_04 | 900 -> USB_2023_Q3 |
| chunk200_dense *(newly promoted)* | ref_them_15 | 1.1 -> BAC_2023_Q4,WFC_2023_Q4; 52.6 -> WFC_2023_Q4; 6 -> BAC_2023_Q4,BLK_2024_Q1,WFC_2023_Q4; 12 -> BAC_2023_Q4,BLK_2024_Q1 |
| chunk200_hybrid | ref_them_04 | 10 -> BK_2024_Q4; 968 -> BK_2024_Q4; 30 -> USB_2024_Q3; 200 -> USB_2024_Q3,USB_2024_Q4 |
| chunk200_hybrid | ref_them_06 | 57 -> FITB_2024_Q2; 43.54 -> COF_2023_Q4; 99 -> COF_2023_Q4; 65 -> GS_2023_Q4 |
| chunk500_bm25 | ref_comp_10 | 77.80 -> PNC_2023_Q2; 30 -> FITB_2023_Q4,PNC_2023_Q2 |
| chunk500_dense | ref_them_02 | 90 -> GS_2024_Q2; 2027 -> USB_2024_Q3 |
| chunk500_hybrid *(newly promoted)* | ref_them_04 | 190 -> USB_2024_Q4; 200 -> USB_2024_Q4 |
| chunk500_hybrid | ref_them_06 | 57 -> FITB_2024_Q2; 100 -> STT_2023_Q4 |

Per-record detail for both populations: `check3_attribution_postfix.csv`.
