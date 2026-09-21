# Manual review packet -- Stage 2 faithfulness check
Assembled material only. No classification, no proposed failure-mode categories, no commentary beyond the factual metadata below. Verdict and failure-mode-note fields are left empty for you to fill in by reading.

Post-fix tables used throughout (`results/tables/qwen3.8-27b_q4_k_xl/generation_outcomes.csv`). Pre-fix tables are preserved separately at `results/tables/prefix/` and not used here.

## Sampling frame (B1)

| stratum | n |
|---|--:|
| Stratum 1 -- Case C answered_grounded_correct flagged in Check 3 (off-target-only substantive claim, the 27% exposure set) | 7 |
| Stratum 2 -- ref_unans_01 non-abstentions (Northern Trust substituted with BNY Mellon) | 3 |
| Stratum 3 -- answered_grounded_offtarget, spread across conditions and categories (dominant failure mode) | 15 |
| Stratum 4 -- answered_grounded_ungrounded, Case B (the 2 remaining ungrounded items) | 2 |
| Stratum 5 -- Case C answered_grounded_correct, NOT flagged in Check 3 (control -- what a clean pass looks like) | 5 |
| Stratum 6 -- Case C abstentions, sample of 8 of 15 (over-conservative refusal candidates) | 8 |
| **total** | **40** |

Notes on fit: stratum 6 (Case C abstentions) is a sample of 8 of the 15 total, chosen to cover all 6 conditions and all 4 distinct comparative question_ids that appear in this stratum (the remaining 7 are not included, to keep the packet at 40). Stratum 3 (offtarget) draws 15 of 58 total offtarget items -- all 3 comparative-category offtarget items, plus 12 thematic items chosen to cover 12 of the 14 distinct thematic question_ids with offtarget occurrences (2 per condition, no repeats where avoidable), rather than repeating the same 1-2 questions across all 6 conditions. No item appears in more than one stratum.

---

## Stratum 1 -- Case C answered_grounded_correct flagged in Check 3 (off-target-only substantive claim, the 27% exposure set)

### Item 1: `ref_them_02` / `chunk200_bm25`

- **question_id:** ref_them_02
- **condition:** chunk200_bm25
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did banks characterise the uncertainty around the Basel III endgame proposal over 2023 and 2024, and how did it affect their capital actions?

**Gold anchor(s):**
> capital, while uncertainty about the Basel III Endgame prevails, our capital position remains very robust
> pace of buybacks will likely remain modest in light of the Basel III

**Generated answer, verbatim:**

```
Based on the provided context, banks characterized the uncertainty surrounding the Basel III endgame proposal as significant, complex, and "overcalibrated," with specific concerns regarding the quantum and timing of its resolution. Goldman Sachs noted that while there was favorable momentum in press reports and regulator comments, uncertainty remained, leading them to operate at the wider end of their capital range (running 90 bps of cushion above normal) to signal flexibility. JPMorgan Chase described the proposal as "overcalibrated" and criticized its construct for exacerbating procyclicality and discouraging scale and diversification; they noted that if finalized in its current form, it would result in a 45% increase in capital requirements relative to 2017 levels. Wells Fargo characterized the rules as a "complicated set" that included higher capital requirements than expected, estimating a potential 20% increase in Risk-Weighted Assets (RWA) if no changes were made or actions taken.

Regarding capital actions, JPMorgan Chase stated that the pace of share buybacks would likely remain modest due to the proposal and that they would continue to reassess their buyback trajectory as circumstances evolved. Goldman Sachs indicated that running with higher capital cushions was a deliberate strategy to address the remaining uncertainty associated with both the Stress Capital Buffer (SCB) and the Basel III endgame.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `GS_2024_Q2_qa_200_020` -- transcript `GS_2024_Q2` -- NOT one of the question's own transcript_ids*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution
```

*Rank 2 -- `JPM_2023_Q3_prepared_remarks_200_006` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
ing out from the details of this most recent proposal, this page reminds us of what's happened since 2017. Since then, SA-CCR and the stress capital buffer have been adopted and our GSIB surcharge will increase to 4.5%. So assuming the Basel III endgame and GSIB proposals are finalized in their current form, we would see a 45% increase in our capital requirements relative to that 2017 starting point. This illustrates again how overcalibrated these proposals are and it's not done yet. We still expect the Fed to incorporate CECL into CCAR, which will likely increase the SCB. And, of course, given the absence of a fix to the GSIB clause, it continues to present a headwind into the indefinite future. And aside from those dynamics, there remains the long-standing issue of procyclicality in the overall capital [Technical Difficulty]. We think it's also important to point out that the agencies did
```

*Rank 3 -- `JPM_2023_Q3_prepared_remarks_200_003` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
. We ended the quarter with a CET1 ratio of 14.3%, up about 50 basis points versus the prior quarter as the benefit of net income less capital distributions was partially offset by AOCI. We had $2 billion of net share repurchases this quarter and the pace of buybacks will likely remain modest in light of the Basel III endgame proposal. In line with our capital hierarchy, we will continue to reassess the buyback trajectory as circumstances evolve or opportunities emerge. And on the topic of the Basel III endgame, you'll see that we added a couple of pages on it. So, let's cover that now, starting on Page 4. Given the significance of this proposal for us, the broader industry as well as households and businesses as end-users, we thought it was important to spend time discussing it. And while we know there is interest in having us quantify the expected impact of this proposal in a lot of granular detail,
```

*Rank 4 -- `JPM_2023_Q3_prepared_remarks_200_007` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
actually have a choice here. While it may technically be true that the proposal is Basel compliant, Basel compliant does not mandate a 25% increase in capital requirements. Implementing the Basel III endgame consistently with how the Europeans have by retaining credit risk modeling and also addressing the compounding effects of GSIB and SCB would have achieved Basel compliance without creating this unnecessary increase in capital requirements. As you would expect, we will continue to engage and forcefully advocate during the comment period and beyond in a great deal of technical detail. For the purposes of this call, we wanted to make the equally important broader plans about both the level of capital increase and the flaws in the construct of the framework itself since coherent design is critical to the framework's durability over time. The current proposal exacerbates existing features that discourage beneficial scale and diversification. If it goes through as written, there will likely be significant impacts on pricing and availability of credit for businesses and consumers. In addition, the ongoing and persistent
```

*Rank 5 -- `WFC_2023_Q3_prepared_remarks_200_009` -- transcript `WFC_2023_Q3` -- NOT one of the question's own transcript_ids*

```
serving the Navajo community. The centers help engage and empower communities to achieve their financial goals through financial education workshops and free one-on-one coaching.  Looking ahead, the U.S. economy has continued to be resilient with key support from the labor and strength -- from the labor market and strength in consumer spending. Delinquencies have continued to deteriorate at a relatively slow consistent rate without signs of acceleration across our portfolios. Our base case remains a continued slowing of the economy, but we remain prepared for a wide range of scenarios given there is still significant uncertainty ahead.  Regarding capital, the Basel III Endgame proposal included higher capital requirements as we expected. It's a complicated set of rules. But at this point, if nothing changed and we didn't take actions, we estimate that our RWA would increase by approximately 20%. There are some items that increased our capital requirements that we are hopeful will be adjusted, and we will be participating and sharing
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 90 | `GS_2024_Q2_qa_200_020` | GS_2024_Q2 | no |
| 45 | `JPM_2023_Q3_prepared_remarks_200_006` | JPM_2023_Q3 | yes |
| 2017 | `JPM_2023_Q3_prepared_remarks_200_006` | JPM_2023_Q3 | yes |
| 20 | `JPM_2023_Q3_prepared_remarks_200_006`, `WFC_2023_Q3_prepared_remarks_200_009` | JPM_2023_Q3, WFC_2023_Q3 | yes |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 2: `ref_them_04` / `chunk200_bm25`

- **question_id:** ref_them_04
- **condition:** chunk200_bm25
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Gold anchor(s):**
> 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven
> operating leverage this quarter as expenses decreased 4%, driven by actions taken to right size

**Generated answer, verbatim:**

```
In late 2023, Bank of America reported achieving 170 basis points of operating leverage for the full year, attributing this to good expense discipline and a reduction in headcount and expenses every quarter. U.S. Bancorp indicated that by the end of the fourth quarter of 2023, it would be on a run rate recognizing $900 million in savings, which would support flat expenses between 2023 and 2024 and contribute to positive operating leverage in 2024. Barclays stated its commitment to delivering aggregate positive operating leverage in the following year (2024), expressing confidence based on ongoing investments and platform efficiencies.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BK_2023_Q3_qa_200_019` -- transcript `BK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
approach across the company. We've got KYC as an example as well. We used to do KYC in each of our businesses. We're bringing that together to have a KYC platform. So there are a lot of proof points that we've got in various stages of development here in addition to the actual pilots that we did, specifically for a platform's operating model.

Mike Mayo: So when you add it all together you said next year you expect to have positive operating leverage, is that in aggregate or positive fee operating leverage and how can you have such confidence at this stage?

Robin Vince: So look we're committed to positive operating leverage over time. And I don't want my second year as CEO to be one where we have negative operating leverage. So we are focused on positive operating leverage next year. That's aggregate operating leverage to answer your question. And one of the reasons why we have confidence in that is because we've been investing on
```

*Rank 2 -- `USB_2023_Q3_qa_200_009` -- transcript `USB_2023_Q3` -- NOT one of the question's own transcript_ids*

```
next coming year. But that's embedded into our full year guidance of flat expenses between 2023 and 2024.

Andy Cecere: So Mike, the way I think about it, this is Andy, by the end of the fourth quarter, we will be on a run rate recognizing $900 million of savings, which will be fully reflected in 2024 in our expense base. And that is consistent with how we think about a relatively flat 23% to 24% expense base, including those savings plus investments we'll continue to make in the business.

Mike Mayo: And then the big question then is, so if you have flat 2024 expenses, do you think you can get to positive operating leverage? Or is it too early or too many moving parts? Because this is the sweet spot of the merger savings coming up, right, by the next quarter.

Andy Cecere: It is a sweet spot, Mike, you're absolutely right. And the savings are great.
```

*Rank 3 -- `BK_2023_Q1_prepared_remarks_200_006` -- transcript `BK_2023_Q1` -- NOT one of the question's own transcript_ids*

```
-over-year, and we generated a healthy return on tangible common equity of 20%. And given how in focused capital and liquidity are at the moment, I'll note that our Tier 1 leverage ratio as well as our liquidity coverage ratio remains strong and unchanged compared to the prior quarter, well above regulatory requirements and our own management buffers. Stepping back for a moment, I'm encouraged by the early progress that we are seeing around the Company to deliver on the commitment that we made to you back in January. First, we are bending the cost curve. Our first quarter expense growth came in marginally better than our initial internal plan and we remain firmly committed to cutting our core expense growth by roughly half this year compared to 2022 on a constant currency basis. Second, in line with our outlook for the year, we continued to derive healthy growth in net interest revenue. Third, we delivered positive operating leverage on a year-over-year basis. And fourth, we returned
```

*Rank 4 -- `BAC_2023_Q4_prepared_remarks_200_005` -- transcript `BAC_2023_Q4` -- ONE OF the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as
```

*Rank 5 -- `STT_2024_Q3_prepared_remarks_200_002` -- transcript `STT_2024_Q3` -- NOT one of the question's own transcript_ids*

```
afternoon, everyone. Our third quarter results, which we released earlier this morning, demonstrate the accelerating financial performance and strong business momentum we are achieving this year, which in turn positions State Street well for future growth. We achieved robust fee and total revenue growth and generated positive fee and total operating leverage in 3Q, which, when combined with increased capital return quarter-on-quarter, drove strong earnings growth for our shareholders on both the year-over-year and sequential basis, with quarterly EPS reaching the highest on record. In addition to strong 3Q results, our year-to-date results also highlight the strength of our franchise and financial performance in three quarters of the way through the year, with solid fee and total revenue growth and good expense discipline driving better than expected positive fee and positive total operating leverage, as well as strong earnings growth relative to the same period in 2023 and excluding notable items. The operating environment in the third quarter was dynamic. While global equity and fixed income markets moved notably
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 170 | `BAC_2023_Q4_prepared_remarks_200_005` | BAC_2023_Q4 | yes |
| 900 | `USB_2023_Q3_qa_200_009` | USB_2023_Q3 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 3: `ref_them_04` / `chunk200_hybrid`

- **question_id:** ref_them_04
- **condition:** chunk200_hybrid
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Gold anchor(s):**
> 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven
> operating leverage this quarter as expenses decreased 4%, driven by actions taken to right size

**Generated answer, verbatim:**

```
Based on the provided context, Bank of America achieved 170 basis points of operating leverage in 2023, driven by expense discipline that reduced headcount and expenses every quarter. In early 2024, Bank of New York Mellon (BNY) set an ambitious goal to at least break even from an operating leverage perspective, anticipating a roughly 10% NII headwind that would offset fee revenue growth; they ultimately delivered 968 basis points of positive operating leverage on a reported basis for the full year. U.S. Bank reported approximately 30 basis points of positive operating leverage in Q3 2024 and guided for greater than 200 basis points of positive operating leverage (excluding security gains or losses) for full-year 2025, noting that 2024 was a pivotal year where they effectively managed through macroeconomic uncertainty.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BAC_2023_Q4_prepared_remarks_200_005` -- transcript `BAC_2023_Q4` -- ONE OF the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as
```

*Rank 2 -- `BK_2024_Q4_prepared_remarks_200_006` -- transcript `BK_2024_Q4` -- NOT one of the question's own transcript_ids*

```
. We've worked hard to say what we do and to do what we say. And so, turning to Page 4, I'm pleased that in 2024, we once again met or exceeded our financial goals for the year. We are confident that BNY can deliver positive operating leverage across a wide range of scenarios and so we started 2024 determined to at least breakeven from an operating leverage perspective. That was an ambitious goal at the time, considering that our revenue outlook at the beginning of the year foresaw an approximately 10% NII headwind to largely offset growth in fee revenue. Therefore, we had to set up to keep expenses, excluding notable items roughly flat, while at the same time self-funding incremental investments in the business. Dermot will discuss the financials in more detail, but in summary, in 2024, we delivered 968 basis points of positive operating leverage on a reported basis and 288 basis points, excluding notable items. We grew
```

*Rank 3 -- `USB_2024_Q3_qa_200_005` -- transcript `USB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
have anything contemplated at this particular point in time.

John Pancari: Okay. All right. Thank you. And then separately, on the expense side, you put up some pretty good positive operating leverage this quarter, and you implied that fourth quarter you'll see that as well. And I believe at the Investor Day, you expressed confidence in continued positive operating leverage. As you look at 2025, can you maybe help us get a sense of the magnitude of that operating leverage that you think is reasonable as you enter 2025 and longer-term, I believe The Street is looking at about 150 basis points to 200 basis points operating leverage next year. Wanted to get your thoughts on that as we look at your return profile in the coming years?

Andy Cecere: Yeah. Thanks, John. This is Andy. So as you saw, we reported positive operating leverage of approximately 30 basis points in Q3 here. The guidance that John provided would indicate that our expectation for positive operating leverage
```

*Rank 4 -- `USB_2024_Q4_prepared_remarks_200_008` -- transcript `USB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
more on a year-over-year basis. I'll now provide full-year 2025 guidance. Total revenue growth on an adjusted basis is estimated to be in the range of 3% to 5% compared to the full year 2024. We expect to achieve positive operating leverage excluding the impact of security gains or losses of greater than 200 basis points for the full year. I'll now hand it back over to Andy for closing remarks.

Andy Cecere: Thanks, John. 2024 was a pivotal year for the company in many ways and it marked a very important inflection point in our story. Going into the year, there was much uncertainty with respect to the broader macroeconomic environment, persistent inflation, significant rate volatility, political and regulatory headwinds to name a few, but we effectively managed through the changes and most importantly executed on our strategic objectives. Fourth quarter results showcase our commitment to execution which was highlighted by our delivery of 190 basis points of positive operating
```

*Rank 5 -- `BK_2024_Q2_prepared_remarks_200_020` -- transcript `BK_2024_Q2` -- NOT one of the question's own transcript_ids*

```
macroeconomic and interest rate environment, as well as the size of our balance sheet. To wrap up, we enter the second half of the year on the back of solid fee growth, a better than expected NII performance to date, and continued expense discipline, which gives us incremental confidence in our ability to drive positive operating leverage in 2024. With that, Operator, can you please open the line for Q&A?
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 170 | `BAC_2023_Q4_prepared_remarks_200_005` | BAC_2023_Q4 | yes |
| 10 | `BK_2024_Q4_prepared_remarks_200_006` | BK_2024_Q4 | no |
| 968 | `BK_2024_Q4_prepared_remarks_200_006` | BK_2024_Q4 | no |
| 30 | `USB_2024_Q3_qa_200_005` | USB_2024_Q3 | no |
| 3 | `BAC_2023_Q4_prepared_remarks_200_005`, `USB_2024_Q3_qa_200_005`, `USB_2024_Q4_prepared_remarks_200_008` | BAC_2023_Q4, USB_2024_Q3, USB_2024_Q4 | yes |
| 200 | `USB_2024_Q3_qa_200_005`, `USB_2024_Q4_prepared_remarks_200_008` | USB_2024_Q3, USB_2024_Q4 | no |
| 2025 | `USB_2024_Q3_qa_200_005`, `USB_2024_Q4_prepared_remarks_200_008` | USB_2024_Q3, USB_2024_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 4: `ref_them_06` / `chunk200_hybrid`

- **question_id:** ref_them_06
- **condition:** chunk200_hybrid
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> What efficiency ratio levels and targets did banks discuss across 2023 and 2024?

**Gold anchor(s):**
> an adjusted efficiency ratio of 59% and a seasonally challenged quarter, which is a six
> annual operating efficiency ratio, net of adjustments to be modestly down compared to the 43.5%

**Generated answer, verbatim:**

```
Based on the provided context, the following efficiency ratio levels and targets were discussed by the banks:

*   **Fifth Third Bancorp (FITB):** For full-year 2024, the bank projects an efficiency ratio of around 57%. They expect to manage full-year adjusted non-interest expense stable to 2023 levels.
*   **Capital One Financial Corporation (COF):**
    *   In Q4 2023, the annual operating efficiency ratio, net of adjustments, was reported at 43.54% for the full year 2023. This represented a 99 basis point improvement over the previous year.
    *   For full-year 2024, Capital One initially guided that the annual operating efficiency ratio (net of adjustments) would be flat to modestly down compared to 2023. By Q3 2024, they updated this expectation to a range in the low 42s for the full year 2024.
    *   The year-to-date operating efficiency ratio through September 2024 was 41.7%.
*   **Goldman Sachs (GS):** In Q4 2023, it was noted that if selected items were excluded, the efficiency ratio for 2023 would have been approximately 65%, which is significantly better than the fully reported number.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2024_Q2_prepared_remarks_200_016` -- transcript `FITB_2024_Q2` -- NOT one of the question's own transcript_ids*

```
2024, reflecting the impact of weaker than previously expected credit demand and customer hedging activities. We expect strong growth in commercial payments and wealth and asset management revenue to continue. In response to this expectation of lower customer activity in the second half. We expect to manage full year adjusted non-interest expense stable to 2023 levels. Our expense outlook assumes continued investments in technology with tech expense growth in the mid-single digits and sales additions in middle market, commercial payments, and wealth. We will open 30 to 35 new branches in our higher growth markets and have already closed a similar number of branches in 2024. Our outlook still projects an efficiency ratio of around 57% for the full year. For full year 2024, the net charge-off outlook remains in the 35 to 45 basis points range. While we expect to resume provision builds in connection with loan growth and mix in the second half of 2024, we expect the second half build to be less than the first half of 2024
```

*Rank 2 -- `COF_2023_Q4_prepared_remarks_200_015` -- transcript `COF_2023_Q4` -- NOT one of the question's own transcript_ids*

```
-year 2024, we expect annual operating efficiency ratio, net of adjustments, will be flat to modestly down compared to 2023. Our expectation includes the partial year impact of the proposed CFPB late fee rule, assuming that rule takes effect in October 2024. Pulling way up, our modern technology capabilities are generating an expanding set of opportunities across our businesses. We continue to drive improvements in underwriting, modeling, and marketing, as we increasingly leverage machine learning at scale. And our tech engine drives growth, efficiency improvement, and enduring value creation over the long term. We remain well-positioned to deliver compelling long-term shareholder value and to thrive in a broad range of possible economic scenarios. And now we'll be happy to answer your questions. Jeff?

Jeff Norris: Thank you, Rich. We’ll now start the Q&A session. As a courtesy to other investors and analysts who may wish to ask a question, please limit yourself to one question plus a single follow
```

*Rank 3 -- `COF_2024_Q3_prepared_remarks_200_011` -- transcript `COF_2024_Q3` -- ONE OF the question's own transcript_ids*

```
the third quarter. We delivered another quarter of top-line growth in domestic card loans, purchase volume and revenue. In the auto business, we saw year-over-year growth in originations for the third consecutive quarter and consumer credit trends remained stable. Our year-to-date operating efficiency ratio, net of adjustments through September was 41.7%. We had guided to 2024 annual operating efficiency ratio, net of adjustments to be modestly down compared to the 43.5% we posted in 2023. Our view included the positive impact from the end of the revenue sharing related to the Walmart partnership and assumed the CFPB late fee rule would take effect in October. Looking forward, we now expect the full year 2024 annual operating efficiency ratio net of adjustments to be in the low 42s. We expect a sequential quarter increase in operating expense in the fourth quarter, that will be roughly in line with historical patterns as we continue to invest in our technology transformation. And we are
```

*Rank 4 -- `COF_2023_Q4_prepared_remarks_200_014` -- transcript `COF_2023_Q4` -- NOT one of the question's own transcript_ids*

```
, we continued to deliver solid results in the fourth quarter. We posted another strong quarter of top line growth in domestic card revenue, purchase volume, and loans. Domestic card and auto delinquency trends were in line with normal seasonal patterns, a continuing indicator of stabilizing consumer credit results. We grew consumer deposits and total deposits. And we added liquidity and maintained capital to further strengthen our already strong and resilient balance sheet. Our annual operating efficiency ratio, net of adjustments for the full year 2023, was 43.54%. In 2023, we saw incremental opportunities and made choices to grow revenue and tightly manage costs to achieve a 99 basis point improvement in our annual operating efficiency ratio. The actual improvement was better than the “modest improvement” growth we had been expecting. Over the last decade, we've driven significant operating efficiency improvement even as we've invested to transform our technology. And we continue to drive for efficiency improvement over time. For the full
```

*Rank 5 -- `GS_2023_Q4_qa_200_024` -- transcript `GS_2023_Q4` -- NOT one of the question's own transcript_ids*

```
the impact of selected items. If you take the impact over the course of 2023, the efficiency ratio would have been more like 65%. That's, obviously, not where we want it to be, but significantly better than the fully reported number. We have a number of initiatives across the firm to get after our non-compensation expense. We had a very structured process we implemented once we put out some of the efficiency targets at the end of last year, rigorously marking to market our business plan and our execution against it over the course of the year. There is a -- we have a ton of different categories. We're in the process of reviewing each and every category of our non-compensation expense, benchmarking it, reviewing KPIs, thinking about our processes, incentive structures, governance, things that we can do to continue to drive that expense as efficiently as possible. We do see an impact of inflation across these activities, and it's for that reason,
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 57 | `FITB_2024_Q2_prepared_remarks_200_016` | FITB_2024_Q2 | no |
| 4 | `FITB_2024_Q2_prepared_remarks_200_016`, `COF_2023_Q4_prepared_remarks_200_015`, `COF_2024_Q3_prepared_remarks_200_011`, `COF_2023_Q4_prepared_remarks_200_014` | COF_2023_Q4, COF_2024_Q3, FITB_2024_Q2 | yes |
| 43.54 | `COF_2023_Q4_prepared_remarks_200_014` | COF_2023_Q4 | no |
| 99 | `COF_2023_Q4_prepared_remarks_200_014` | COF_2023_Q4 | no |
| 3 | `FITB_2024_Q2_prepared_remarks_200_016`, `COF_2023_Q4_prepared_remarks_200_015`, `COF_2024_Q3_prepared_remarks_200_011`, `COF_2023_Q4_prepared_remarks_200_014`, `GS_2023_Q4_qa_200_024` | COF_2023_Q4, COF_2024_Q3, FITB_2024_Q2, GS_2023_Q4 | yes |
| 42 | `COF_2024_Q3_prepared_remarks_200_011` | COF_2024_Q3 | yes |
| 41.7 | `COF_2024_Q3_prepared_remarks_200_011` | COF_2024_Q3 | yes |
| 4 | `FITB_2024_Q2_prepared_remarks_200_016`, `COF_2023_Q4_prepared_remarks_200_015`, `COF_2024_Q3_prepared_remarks_200_011`, `COF_2023_Q4_prepared_remarks_200_014` | COF_2023_Q4, COF_2024_Q3, FITB_2024_Q2 | yes |
| 65 | `GS_2023_Q4_qa_200_024` | GS_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 5: `ref_comp_10` / `chunk500_bm25`

- **question_id:** ref_comp_10
- **condition:** chunk500_bm25
- **category:** comparative
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did PNC and Fifth Third each treat AOCI when describing their capital and tangible book value per share during 2023?

**Gold anchor(s):**
> Category 3 institution, we don't include AOCI in our CET1 ratio, but I understand why
> book value per share, excluding AOCI, increased 11% compared to the year

**Generated answer, verbatim:**

```
Based on the provided context, PNC reported a negative AOCI of $9.5 billion at quarter-end in Q2 2023, which resulted in a tangible book value of $77.80 per common share (an increase of 5% year-over-year). Fifth Third described its capital and tangible book value metrics by explicitly excluding or adjusting for AOCI to show the underlying strength; specifically, they noted that their tangible book value per share excluding AOCI increased 11% compared to the prior year quarter in Q2 2023. Additionally, Fifth Third highlighted that moving securities to held-to-maturity would de-risk potential AOCI volatility to capital by about 30%.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2023_Q3_qa_500_002` -- transcript `FITB_2023_Q3` -- NOT one of the question's own transcript_ids*

```
we know our portfolio is going to pay down.  And we know that this is going to be very manageable from a regulatory capital perspective. When we model the capital impact at a fully phased-in level on AOCI, the impact on CET1 is about 125 basis points when you reach the third quarter of 2028 and that's why we continue to accrete CET1 is to be able to have sufficient regulatory capital for that world. And in fact, should rates get north of 8%. We would still be maintaining a CET1 well above regulatory minimums would be over 8% CET1 in that environment.  So we feel good about how we're positioned, how we will roll down the curve and ultimately, the regulatory capital. It's just one of the challenges in this environment with everything in AFS is that you have that mark on the tangible book value per share, that erosion. But at the same time, should rates fall. I think all of you would be very pleased with how much tangible book value accretion, we would report in that environment.

TimothySpence: And Scott, if I just put a point on the last thing, Jamie you said. I mean, we believe investors want us to do what is best for managing the business and for recognizing the fact that options have value but if you believe that the AOCI mark is weighing on the stock, then the other way to look at it is the burn down is 25% accretion in tangible book value per share in the next two years, just given the current outlook on rates, which is a pretty unique buying opportunity, be the other way to look at it.

ScottSiefers: Yes, I agree. All right. That's perfect. So Tim and Jamie, thank you both.

Operator: And your next question comes from the line of Erika Najarian from UBS.

ErikaNajarian: Jamie, this first one is for you. Not to belabor the earlier point, but all the PPNR metrics and balance sheet metrics look great and also did the forward look? And I guess, if you could just explain what happened in the quarter, I think given that your portfolio -- your securities portfolio is 61% CMBS. I think investors that know you well, expected not as much negative convexity -- was there something unique that happened in this quarter in the portfolio that -- where the AOCI was that
```

*Rank 2 -- `FITB_2023_Q4_prepared_remarks_500_001` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
AOCI of 15.9% and an adjusted efficiency ratio of 55.9%. All among the best of our peers. We also continue to take market share organically by growing our customer base and deepening relationships. We grew consumer households by 3% overall punctuated by 6% growth in the Southeast. In commercial, we added a record number of new quality middle market relationships up 11% over the prior year. As a result, we grew or maintained our deposit market share position in all 40 of our largest MSAs. As we turn the page to 2024, we remain focused on differentiating Fifth Third based on the strength and consistency of our financial performance by prioritizing stability, profitability, and growth in that order. Bryan will take you through the detail on the fourth quarter and our outlook for the year shortly. But before that, I would like to touch on a few points. The first of these is the strength of our balance sheet. Our defensive positioning and decision to move quickly to adapt to proposed regulatory changes have put us in a position to play offense in 2024. Having achieved full Category 1 LCR compliance on August 31st and maintained it since, our liquidity position is very strong. We completed our RWA diet in the fourth quarter and accreted nearly 50 basis points of CET1, putting us on pace to reach a 10.5% CET1 ratio by mid-year 2024. Given our strong earnings profile and the significant rally in interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

*Rank 3 -- `FITB_2023_Q2_prepared_remarks_500_005` -- transcript `FITB_2023_Q2` -- ONE OF the question's own transcript_ids*

```
closely and believe the overall impact on Fifth Third will be limited. We had deemphasized office even before the pandemic, and we are not currently pursuing new office CRE originations. From an overall credit management perspective, we have continually improved the granularity and diversification of our loan portfolios through a focus on generating and maintaining high-quality relationships. As many of you know, we have been and remain cautious in our economic outlook. We tightened underwriting standards during COVID, including stressing credits to an up 200-basis-point scenario off the forward curve, which limited our growth but improved the stability of our balance sheet. Since we began tightening underwriting standards, roughly 90% of our commercial portfolio has been re-underwritten. Our criticized assets have been stable over the past several quarters. Across all loan categories, we continue to closely monitor exposures where inflation and higher rates may cause stress. Moving to the ACL. Our reserves increased $87 million, reflecting the impacts of dividend finance and Moody's macroeconomic forecast, which eroded slightly. The ACL ratio increased nine basis points sequentially. As you know, we incorporate Moody's macroeconomic scenarios when evaluating our allowance. The base economic scenario from Moody's assumes the unemployment rate reaches 4.3%, while the downside scenario incorporates a peak unemployment rate of 7.8%. We maintained our scenario weightings of 80% to the base and 10% to each of the upside and downside scenarios. Moving to capital. Our CET1 ratio increased 25 basis points sequentially, ending the quarter at over 9.5%. Our capital position reflects our ability to build capital quickly through our strong earnings generation. Our tangible book value per share, excluding AOCI, increased 11% compared to the year ago quarter. We continue to expect a meaningful improvement in our unrealized loss position, assuming the forward curve plays out, resulting in approximately 36% of our current loss position accreting back into equity by the end of 2024 and approximately 50% by the end of 2025. Looking forward, we expect to build capital at an accelerated pace given our RWA optimization initiatives and by extending our share buyback pause. As Tim mentioned, we will postpone repurchases until we have more clarity on the regulatory environment in order to determine the new level of required capital dollars. Assuming we do not buy back shares through year-end, we would antici
```

*Rank 4 -- `PNC_2023_Q2_prepared_remarks_500_001` -- transcript `PNC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
are taking a hard look at opportunities for even further expense improvements across the franchise.  Third, credit quality for the quarter remained strong reflecting our diversified lending franchise and our focus on developing valuable, sustainable businesses based on long term customer relationships.  And finally, I'd like to thank our employees for their efforts and contributions during the quarter.  And with that, I'll turn it over to Rob.

Robert Reilly: Thanks, Bill, and good morning, everyone. Our balance sheet is on Slide 3 and we're presenting on an average basis and comparing to the first quarter. Loans were stable at $325 billion. Investment securities declined $2 billion or 2%. Cash balances at the Federal Reserve were $31 billion and decreased $3 billion, deposits of $426 billion declined $10 billion or 2%. Borrowed funds increased $3 billion. As an aside, since 2021, we've been deliberate in issuing TLAC compliant debt. So we're confident we'll meet the upcoming TLAC requirements through our normal course of funding.  At quarter end, AOCI was a negative $9.5 billion, and tangible book value was $77.80 per common share, an increase of 5% compared to the same period a year ago. We remain well capitalized with an estimated CET1 ratio of 9.5% as of June 30, 2023, which increased 30 basis points linked quarter. We returned approximately $700 million of capital to shareholders in the quarter, which included $600 million of common dividends and approximately a $100 million of share repurchases or 1.1 million shares.  And as Bill just mentioned, our Board recently approved a $0.05 increase to our quarterly cash dividend on common stock, raising the dividend to a $1.55 per share. Our recent CCAR results underscore the strength of our balance sheet. And as previously announced, our current stress capital buffer of 2.9% will improve to the regulatory minimum of 2.5% for the four quarter period beginning in October 2023. Due to the expected issuance by the Federal banking agencies of proposed rules to adjust the Basel III capital framework, share repurchase activity in the third quarter is expected to remain modest. We will continue to monitor this and may adjust share repurchase activity as appropriate.  Slide 4 shows our loans in more detail. Second quarter loans averaged $325 billion and increased $20 billion or 6% compared
```

*Rank 5 -- `HBAN_2023_Q1_prepared_remarks_500_006` -- transcript `HBAN_2023_Q1` -- NOT one of the question's own transcript_ids*

```
to Slide 18. GAAP noninterest expense increased by $9 million. Adjusted for notable items, core expenses decreased by $18 million, driven by lower personnel expense, primarily as a result of reduced incentives and revenue driven compensation. We're proactively managing expenses and have taken actions over the last several quarters to orient to a low level of expense growth in order to deliver positive operating leverage and self-fund strategic investments. Slide 19 recaps our capital position. Common equity Tier 1 increased to 9.55% and has increased sequentially for three quarters. OCI impacts to common equity Tier 1 resulted in an adjusted CET1 ratio of 7.6%. As a reminder, the reported regulatory capital framework does not include OCI impacts in the capital calculation. Our tangible common equity ratio, or TCE, increased 22 basis points to 5.7%. Note that we were holding higher cash balances at the end of Q1, which reduced the TCE ratio by 13 basis points. Adjusting for AOCI, our TCE ratio was 7.27%. Tangible book value per share increased by 7% from the prior quarter to $7.32. Adjusting for AOCI, tangible book value increased to $9.23, and has increased for the past four quarters. Our capital management strategy for the balance of 2023 will result in expanding capital over the course of the year, while maintaining our top priority to fund high-return loan growth. We intend to grow CET1 to the top end of our 9% to 10% operating range by the end of the year. We believe this is a prudent approach given the dynamic environment.  Based on our expectation for continued loan growth, we do not expect to utilize the share repurchase program during 2023. Turning to Slide 20. Our capital plus reserves is top quartile in the peer group and gives us substantial total loss absorption capacity. On Slide 21, credit quality continues to perform very well. As mentioned, net charge-offs were 19 basis points for the quarter. This was higher than last quarter by 2 basis points and up 12 basis points from the prior year as charge-offs continue to normalize.  Non-performing assets declined from the previous quarter and have reduced for seven consecutive quarters. Allowance for credit losses was flat at 1.9% of total loans. Turning to Slide 22. We have provided incremental disclosures on our commercial real estate balances. This
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 9.5 | `FITB_2023_Q2_prepared_remarks_500_005`, `PNC_2023_Q2_prepared_remarks_500_001`, `HBAN_2023_Q1_prepared_remarks_500_006` | FITB_2023_Q2, HBAN_2023_Q1, PNC_2023_Q2 | yes |
| 2 | `FITB_2023_Q3_qa_500_002`, `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2023_Q2_prepared_remarks_500_005`, `PNC_2023_Q2_prepared_remarks_500_001`, `HBAN_2023_Q1_prepared_remarks_500_006` | FITB_2023_Q2, FITB_2023_Q3, FITB_2023_Q4, HBAN_2023_Q1, PNC_2023_Q2 | yes |
| 77.80 | `PNC_2023_Q2_prepared_remarks_500_001` | PNC_2023_Q2 | no |
| 5 | `FITB_2023_Q3_qa_500_002`, `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2023_Q2_prepared_remarks_500_005`, `PNC_2023_Q2_prepared_remarks_500_001`, `HBAN_2023_Q1_prepared_remarks_500_006` | FITB_2023_Q2, FITB_2023_Q3, FITB_2023_Q4, HBAN_2023_Q1, PNC_2023_Q2 | yes |
| 11 | `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2023_Q2_prepared_remarks_500_005` | FITB_2023_Q2, FITB_2023_Q4 | yes |
| 2 | `FITB_2023_Q3_qa_500_002`, `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2023_Q2_prepared_remarks_500_005`, `PNC_2023_Q2_prepared_remarks_500_001`, `HBAN_2023_Q1_prepared_remarks_500_006` | FITB_2023_Q2, FITB_2023_Q3, FITB_2023_Q4, HBAN_2023_Q1, PNC_2023_Q2 | yes |
| 30 | `FITB_2023_Q4_prepared_remarks_500_001`, `PNC_2023_Q2_prepared_remarks_500_001` | FITB_2023_Q4, PNC_2023_Q2 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 6: `ref_them_02` / `chunk500_dense`

- **question_id:** ref_them_02
- **condition:** chunk500_dense
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did banks characterise the uncertainty around the Basel III endgame proposal over 2023 and 2024, and how did it affect their capital actions?

**Gold anchor(s):**
> capital, while uncertainty about the Basel III Endgame prevails, our capital position remains very robust
> pace of buybacks will likely remain modest in light of the Basel III

**Generated answer, verbatim:**

```
Based on the provided transcripts, banks characterized the uncertainty surrounding the Basel III endgame proposal as significant, disconcerting, and lacking in detailed analysis to support the magnitude of proposed capital increases. They described the rules as going "way too far," potentially increasing systemic risk by pushing activity into shadow banking, raising credit costs, and reducing U.S. competitiveness. Specific concerns included a lack of clarity on the timing (with some suggesting it might not take effect until 2025) and the quantum of the final resolution.

This uncertainty directly affected capital actions in the following ways:
*   **JPMorgan Chase** kept its share repurchase pace "modest" due to the proposal, noting that while they expected RWA to increase by around $500 billion (requiring roughly $22.5 billion in additional capital at their current GSIB ratio), they were reassessing buyback trajectories as circumstances evolved.
*   **Goldman Sachs** maintained a wider-than-normal CET1 cushion (running with 90 bps of extra buffer) to signal flexibility and address the lingering uncertainty regarding both the timing and final requirements of the rules, while still aiming to return capital to shareholders.
*   **U.S. Bank** indicated that clarity on Basel III was a key factor in their timeline for building upon modest buybacks, though they remained confident in their ability to meet capital targets even under stricter scenarios (CAT II) expected around 2027.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `JPM_2023_Q2_prepared_remarks_500_006` -- transcript `JPM_2023_Q2` -- NOT one of the question's own transcript_ids*

```
on capital from the pending finalization of the Basel III rules. Nonetheless, despite the likely headwinds ahead, we remain optimistic about the Company's ability to continue delivering excellent performance through a range of scenarios. With that, operator, please open the line for Q&A.
```

*Rank 2 -- `GS_2023_Q3_prepared_remarks_500_002` -- transcript `GS_2023_Q3` -- NOT one of the question's own transcript_ids*

```
data has come in above estimates, driving market expectations of higher for longer interest rates. And there still are a number of sectors in the economy that have yet to absorb the impact of higher rates, especially in light of the further tightening in financial conditions we've seen over the last quarter. At the same time, there has been an escalation of geopolitical stresses around the globe, the [indiscernible] war in Ukraine, tensions with China and now the conflict in the Middle East. Overall levels of risk are more elevated than we've seen in quite some time. While we don't know where this will all lead, it could impact economic growth and stability in the U.S. and around the world, and we remain cautiously positioned. Before I turn it over to Denis, I'd like to spend a moment on Basel III Endgame proposal and reiterate my views on it. We, of course, support sensible regulation and the desire to ensure we have a safe and sound financial system. There are some who have recently said we need to address the lessons from the 2008 financial crisis, which is driving the needs of much higher regulations. But frankly speaking, the rules, as proposed, go way too far and do not account for the vast array of improvements made by the largest banks as a result of Dodd-Frank and other reforms. Not only have banks doubled capital over the last 15 years, have improved the quality of capital, increased liquidity, simplified businesses that have been subjected to ongoing annual stress tests. Requiring too much capital will have negative consequences. I believe if these rules are implemented, three things will happen. First, the cost of credit will go up for businesses of all sizes from large corporations to small businesses. Second, more activity will move to the unregulated shadow banking sector. Policies that incentivize a transfer of risk outside the regulated banking system could, in fact, increase systemic risk. And third, US competitiveness will go down. Our capital markets are the deepest and the most liquid in the world. They're the engine of our economy as access to capital allows for innovation and growth across the country. Our competitive standing as the leading global economy would be negatively impacted by this proposal. The net result of these proposed rules would be slower economic growth in the US, material improvement in the -- soundness of the banking system. We, alongside clients and others in the industry, have been engaging heavily
```

*Rank 3 -- `JPM_2023_Q3_prepared_remarks_500_001` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
Expenses of $20.9 billion were up $1.7 billion or 9% year-on-year, primarily driven by ongoing growth and front office and technology staffing, as well as wage inflation and higher legal expense. And credit costs were $1.4 billion, predominantly driven by net charge-offs in Card, and included a $102 million net reserve release, driven by changes in the central scenario, primarily offset by card loan growth. On to balance sheet and capital on Page 3. We ended the quarter with a CET1 ratio of 14.3%, up about 50 basis points versus the prior quarter as the benefit of net income less capital distributions was partially offset by AOCI. We had $2 billion of net share repurchases this quarter and the pace of buybacks will likely remain modest in light of the Basel III endgame proposal. In line with our capital hierarchy, we will continue to reassess the buyback trajectory as circumstances evolve or opportunities emerge. And on the topic of the Basel III endgame, you'll see that we added a couple of pages on it. So, let's cover that now, starting on Page 4. Given the significance of this proposal for us, the broader industry as well as households and businesses as end-users, we thought it was important to spend time discussing it. And while we know there is interest in having us quantify the expected impact of this proposal in a lot of granular detail, it's important to start by asking why the proposed increase is so large given the repeated statement over time by policymakers that banks are well-capitalized and well-positioned to deal with stress. Given that context, the absence of detailed analysis supporting a capital increase of this magnitude is disconcerting and there's a lot that does not make sense to us. Starting with RWA, we've already said we expect the firm's RWA to increase by around 30% or $500 billion, which results in capital requirements increasing by about 25% or $50 billion. One immediate thing to point out is that at 4.5% GSIB, a $500 billion increase in RWA requires $22.5 billion of additional capital with no change in our systemic risk footprint. We've been on the record for a long time that GSIB was conceptually flawed and miscalibrated originally. Since implementation, the failure to address economic growth despite the Fed themselves acknowledging this
```

*Rank 4 -- `GS_2024_Q2_qa_500_008` -- transcript `GS_2024_Q2` -- NOT one of the question's own transcript_ids*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution. It sounds from some of Powell's latest comments that, that may not be something that comes into effect until perhaps into 2025, but we are sort of maintaining a level of cushion that think is appropriate in light of what we know and we don't know about the future opportunity set for Goldman Sachs, but that buffer is designed to support clients return capital shareholders, while maintaining a prudent buffer with some of the lingering uncertainty with respect to future regulatory input.

Steven Chubak: Helpful color. Thanks for taking my questions.

Dennis Coleman: Thank you.

Operator: We'll go next to Devin Ryan with Citizens JMP.

Devin Ryan: All right, great. Good morning, David and Dennis. A couple questions on AWM progress. So the first one is on the alts business specifically, and you're tracking obviously well ahead of the fundraising targets relative to when you set the $1 billion medium term target for annual incentive fees? And now with over $500 billion in alts AUM and obviously growing, that would seem pretty conservative. So I appreciate there's a lot of work to do to generate the returns ahead here, but how should we think about the underlying assumptions for incentive fees in a more normal harvesting environment, just given the mixed shift and the growth that you're seeing in AUM there?

Dennis Coleman: So Devin, I think it's a good question, and I think we share your expectation that, that's going
```

*Rank 5 -- `USB_2024_Q3_qa_500_006` -- transcript `USB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
-- as we talked about and as John articulated in his comments, we would expect to go to some level of modest buybacks here shortly. And then, we would expect to build upon that once we have more clarity on Basel III and some of the capital rules and then loan growth as you talked about is a key factor as well. But given all that, we would still expect to be up at our capital targets even under the CAT II when we cross that threshold, which again as a reminder, we talked about is not expected till 2027.

Erika Najarian: I guess just to follow-up on that, the Basel III shouldn't impact you that much, right, other than -- and everybody had already put in the impact of AOCI actually more immediately than whatever phase-in Basel III end game has. I guess I'm wondering, as a regional bank, are you -- do you think it's just a -- you're just a prudent constituent in terms of not wanting to be aggressive ahead of a new set of revisions? Or are there -- are you also considering that the ratings agency is just sort of wondering what the -- and I completely understand that you're about to buyback in the first quarter, but I think that it's probably an important component of long-only investors starting to increase their position in U.S. Bank.

Andy Cecere: Yeah. All those constituencies you talked about are factors in our thinking. Loan growth, the final capital rules, the rating agencies, those are all factors. But we're very confident in our accretion ability as you saw this quarter, 20 basis points, we've articulated 20 to 25. We're very comfortable with our capital position and we're very comfortable with the ability to start to buy-back and distribute as well as accrete, the level of which we'll continue to determine and judge over-time, given all those factors you talked about.

Erika Najarian: Thank you, Andy.

Andy Cecere: You bet, Erika. See you.

Operator: Your next question comes from Mike Mayo from Wells Fargo Securities. Your line is now open.

Andy Cecere: Good morning, Mike.

Mike Mayo: Hi. First -- hey, good morning. First, a cleanup question. So, are you interested in buying a bank in the Southeast because that's got a lot
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 2025 | `GS_2024_Q2_qa_500_008` | GS_2024_Q2 | no |
| 500 | `JPM_2023_Q3_prepared_remarks_500_001`, `GS_2024_Q2_qa_500_008` | GS_2024_Q2, JPM_2023_Q3 | yes |
| 22.5 | `JPM_2023_Q3_prepared_remarks_500_001` | JPM_2023_Q3 | yes |
| 1 | `GS_2023_Q3_prepared_remarks_500_002`, `JPM_2023_Q3_prepared_remarks_500_001`, `GS_2024_Q2_qa_500_008` | GS_2023_Q3, GS_2024_Q2, JPM_2023_Q3 | yes |
| 90 | `GS_2024_Q2_qa_500_008` | GS_2024_Q2 | no |
| 2027 | `USB_2024_Q3_qa_500_006` | USB_2024_Q3 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 7: `ref_them_06` / `chunk500_hybrid`

- **question_id:** ref_them_06
- **condition:** chunk500_hybrid
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> What efficiency ratio levels and targets did banks discuss across 2023 and 2024?

**Gold anchor(s):**
> an adjusted efficiency ratio of 59% and a seasonally challenged quarter, which is a six
> annual operating efficiency ratio, net of adjustments to be modestly down compared to the 43.5%

**Generated answer, verbatim:**

```
Based on the provided context, the following efficiency ratio levels and targets were discussed by Capital One (COF) and Fifth Third Bancorp (FITB):

**Capital One (COF)**
*   **2023 Actual:** The company posted an annual operating efficiency ratio, net of adjustments, of 43.5% in 2023.
*   **2024 Guidance/Target:**
    *   Initially guided to be flat to modestly down compared to 2023, assuming the CFPB late fee rule took effect in October 2024 and including the positive impact from the end of the Walmart partnership revenue sharing.
    *   By Q3 2024, the company updated its expectation for the full-year 2024 annual operating efficiency ratio (net of adjustments) to be in the **low 42s**. This update reflected the removal of the assumption that the CFPB late fee rule would take effect in 2024 due to litigation uncertainty.
    *   Year-to-date through September 2024, the operating efficiency ratio (net of adjustments) was 41.7%.

**Fifth Third Bancorp (FITB)**
*   **2024 Target:** The company projected a full-year 2024 efficiency ratio of around **57%**. This outlook assumed stable to slightly lower adjusted non-interest income and managed expenses, including continued technology investments and branch network changes.

**State Street Corporation (STT)**
*   While STT discussed returning approximately 100% of earnings in 2024 and implementing productivity initiatives to drive operating model efficiency, the provided text does not specify a numerical target or level for their efficiency ratio.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `COF_2023_Q4_prepared_remarks_500_006` -- transcript `COF_2023_Q4` -- NOT one of the question's own transcript_ids*

```
-year 2024, we expect annual operating efficiency ratio, net of adjustments, will be flat to modestly down compared to 2023. Our expectation includes the partial year impact of the proposed CFPB late fee rule, assuming that rule takes effect in October 2024. Pulling way up, our modern technology capabilities are generating an expanding set of opportunities across our businesses. We continue to drive improvements in underwriting, modeling, and marketing, as we increasingly leverage machine learning at scale. And our tech engine drives growth, efficiency improvement, and enduring value creation over the long term. We remain well-positioned to deliver compelling long-term shareholder value and to thrive in a broad range of possible economic scenarios. And now we'll be happy to answer your questions. Jeff?

Jeff Norris: Thank you, Rich. We’ll now start the Q&A session. As a courtesy to other investors and analysts who may wish to ask a question, please limit yourself to one question plus a single follow-up. So if you have any questions after the Q&A session, the Investor Relations team will be available after the call. Amy, please start the Q&A.
```

*Rank 2 -- `COF_2024_Q3_prepared_remarks_500_004` -- transcript `COF_2024_Q3` -- ONE OF the question's own transcript_ids*

```
2022, auto charge-offs have been strong and stable. Slide 13 shows third quarter results for our Commercial Banking business. Compared to the linked quarter, ending loan balances decreased about 2%. Average loans were down about 1%. The modest declines are largely the result of choices we made in 2023 to tighten credit. Ending deposits were up about 5% from the linked quarter. Average deposits were down about 1%. We continue to manage down selected less attractive commercial deposit balances. Third quarter revenue was up 1% from the linked quarter and non-interest expense was up by about 2%. The Commercial Banking annualized net charge-off rate for the third quarter increased 7 basis points from the sequential quarter to 0.22%. The Commercial Banking criticized performing loan rate was 7.66%, down 96 basis points compared to the linked quarter. The criticized non-performing loan rate increased 9 basis points to 1.55%. In closing, we continued to post strong results in the third quarter. We delivered another quarter of top-line growth in domestic card loans, purchase volume and revenue. In the auto business, we saw year-over-year growth in originations for the third consecutive quarter and consumer credit trends remained stable. Our year-to-date operating efficiency ratio, net of adjustments through September was 41.7%. We had guided to 2024 annual operating efficiency ratio, net of adjustments to be modestly down compared to the 43.5% we posted in 2023. Our view included the positive impact from the end of the revenue sharing related to the Walmart partnership and assumed the CFPB late fee rule would take effect in October. Looking forward, we now expect the full year 2024 annual operating efficiency ratio net of adjustments to be in the low 42s. We expect a sequential quarter increase in operating expense in the fourth quarter, that will be roughly in line with historical patterns as we continue to invest in our technology transformation. And we are no longer assuming that the CFPB late fee rule will be implemented in 2024, given ongoing uncertainty around industry litigation. Our view of 2024 marketing has not changed. We continue to lean into marketing to grow and to further strengthen our franchise. In the Domestic Card business, we continue to get traction in originations across our products and channels. In Consumer Banking, we're leaning into marketing to grow our digital first national banking franchise. We continue to expect total company marketing in the second half
```

*Rank 3 -- `FITB_2024_Q2_prepared_remarks_500_006` -- transcript `FITB_2024_Q2` -- NOT one of the question's own transcript_ids*

```
the second half of 2024. Given the year-to-date trends in customer activity, we now expect full-year average total loans to be down 3% compared to 2023. Average total loans in the fourth quarter of 2024 are expected to be stable to up 1% compared to the fourth quarter of 2023, with similar performance in both the commercial and consumer portfolios. Customer demand is the primary driver of this change, given the interest rate environment and other economic uncertainties. If there's more economic optimism in the second half of the year, we would expect to see loan growth in-line or better than market growth. We are forecasting fourth quarter average core deposit growth of 2% to 3% when compared to the fourth quarter of 2023. Our forecast also assumes commercial revolver utilization and our cash and other short-term investments remain relatively stable throughout the remainder of 2024. We expect full-year adjusted non-interest income to be stable to down 1% in 2024, reflecting the impact of weaker than previously expected credit demand and customer hedging activities. We expect strong growth in commercial payments and wealth and asset management revenue to continue. In response to this expectation of lower customer activity in the second half. We expect to manage full year adjusted non-interest expense stable to 2023 levels. Our expense outlook assumes continued investments in technology with tech expense growth in the mid-single digits and sales additions in middle market, commercial payments, and wealth. We will open 30 to 35 new branches in our higher growth markets and have already closed a similar number of branches in 2024. Our outlook still projects an efficiency ratio of around 57% for the full year. For full year 2024, the net charge-off outlook remains in the 35 to 45 basis points range. While we expect to resume provision builds in connection with loan growth and mix in the second half of 2024, we expect the second half build to be less than the first half of 2024 release. Therefore, we expect full-year provision to be a 0 to $10 million release, assuming no change to credit quality of the portfolio or projected economic conditions. Moving to our quarterly outlook, we expect NII and NIM growth to continue in both the third and fourth quarter. We expect NII in the third quarter to be up 2% sequentially, reflecting the impact of slowing deposit cost pressures and the continued benefit of our fixed rate asset repricing. Our current outlook assumes interest
```

*Rank 4 -- `STT_2023_Q4_prepared_remarks_500_004` -- transcript `STT_2023_Q4` -- NOT one of the question's own transcript_ids*

```
to return substantial amount of excess capital in recent quarters. For example, over the last five quarters to the end of December, we have returned $6.4 billion of capital to our shareholders. As we pivot to a more normalized level of capital return, in 2024, it is currently our intention to return approximately 100% of earnings in the form of common share dividends and share repurchases, subject to market conditions. Accordingly, as we announced this morning, our Board of Directors has authorized a new common share purchase program of up to $5 billion with no set expiration date. To conclude, while 2023 was an eventful year, we finished strongly in 4Q, which creates an encouraging starting point for our businesses into 2024. This year, we remain highly focused on both the execution of our strategy and the accountability for results. Our goals are clear. We must continue the improvement in our sales performance that we demonstrated in the second half of 2023, continue to implement a set of productivity initiatives and product enhancements that will drive longer term improvements in our operating model efficiency and effectiveness and deliver positive fee operating leverage in 2024, all while returning capital to our shareholders. We are laser focused on these goals. Now, let me hand the call over to Eric who will take you through the quarter in more detail.

Eric Aboaf: Thank you, Ron, and good morning, everyone. Before I begin my review of our fourth quarter and full year 2023 results, let me briefly discuss the notable items we recognized in the quarter on Slide 5, which collectively totaled $620 million pretax or $1.49 of EPS. First, we recognized an FDIC special assessment of $387 million, which is reflected in other expenses. Second, we recognized $203 million of net repositioning charges to enable the next phase of our productivity program. As we had indicated in December, the bulk of this action primarily relates to severance of around 1,500 employees. Our initiative to streamline and delayer our operations, technology and staff functions and improve efficiency will allow us to sustainably reduce expenses. We expect these actions collectively to have a payback of roughly six quarters and begin this quarter with roughly two-thirds of the benefit occurring in 2024. These actions and the related savings will contribute to our fee operating leverage goal for 2024 and in subsequent years. Turning to Slide 6. I will begin my review of both our fourth quarter
```

*Rank 5 -- `COF_2024_Q2_prepared_remarks_500_004` -- transcript `COF_2024_Q2` -- NOT one of the question's own transcript_ids*

```
auto charge-off rate for the quarter was 1.81%, up 41 basis points year-over-year. The 30 plus delinquency rate was 5.67%, up 29 basis points year-over-year, largely as a result of our choice to tighten credit and pull back in 2022, auto charge-offs have been strong and stable. Slide 13 shows second quarter results for our commercial banking business compared to the linked quarter, ending loan balances decreased about 1%. Average loans were also down about 1%. The modest declines are largely the result of choices we made in 2023 to tighten credit. Ending deposits were down about 6% from the linked quarter. Average deposits were down about 3%. The declines are largely driven by our continued choices to manage down selected less attractive commercial deposit balances. Second quarter revenue was essentially flat from the linked quarter and non-interest expense was lower by about 6%. The Commercial Banking annualized net charge-off rate for the second quarter increased 2 basis points from the sequential quarter to 0.15%. The commercial banking criticized performing loan rate was 8.62%, up 23 basis points compared to the linked quarter. The criticized non-performing loan rate increased 18 basis points to 1.46%. In closing, we continued to deliver strong results in the second quarter. We delivered another quarter of top line growth in domestic card loans, purchase volume, and revenue and a second consecutive quarter of year-over-year growth in auto originations. Consumer credit trends continued to show stability and our operating efficiency ratio improved. We had guided to 2024 annual operating efficiency ratio, net of adjustment to be flat to modestly down compared to 2023, assuming the CFPB late fee rule takes effect in October. And we're on a very consistent path with what we expected when we gave that guidance. If the implementation of the rule is delayed, that would be a tailwind to 2024 annual operating efficiency ratio. One thing that has changed is the Walmart relationship. Our partnership ended in the second quarter, which will increase charge-off rates, but have a positive impact on operating efficiency ratio. Including the Walmart impact, we expect full year 2024 operating efficiency ratio, net of adjustments to be modestly down compared to 2023. We continue to lean into marketing to grow and to further strengthen our franchise. In the domestic card business, we continue to get traction in originations across our products
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 43.5 | `COF_2024_Q3_prepared_remarks_500_004` | COF_2024_Q3 | yes |
| 3 | `COF_2023_Q4_prepared_remarks_500_006`, `COF_2024_Q3_prepared_remarks_500_004`, `FITB_2024_Q2_prepared_remarks_500_006`, `STT_2023_Q4_prepared_remarks_500_004`, `COF_2024_Q2_prepared_remarks_500_004` | COF_2023_Q4, COF_2024_Q2, COF_2024_Q3, FITB_2024_Q2, STT_2023_Q4 | yes |
| 42 | `COF_2024_Q3_prepared_remarks_500_004` | COF_2024_Q3 | yes |
| 41.7 | `COF_2024_Q3_prepared_remarks_500_004` | COF_2024_Q3 | yes |
| 57 | `FITB_2024_Q2_prepared_remarks_500_006` | FITB_2024_Q2 | no |
| 100 | `STT_2023_Q4_prepared_remarks_500_004` | STT_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

## Stratum 2 -- ref_unans_01 non-abstentions (Northern Trust substituted with BNY Mellon)

### Item 8: `ref_unans_01` / `chunk200_bm25`

- **question_id:** ref_unans_01
- **condition:** chunk200_bm25
- **category:** unanswerable
- **case:** A
- **current outcome label:** answered_ungrounded

**Question:**
> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Gold anchor(s):** none (unanswerable question)

**Generated answer, verbatim:**

```
Based on the provided context, there are two different reporting periods for Northern Trust (BK):

1.  In Q3 2023, ETFs Assets Under Custody/Administration were up over 20% year-over-year. The total assets under custody/administration and related investment services fees grew in the mid-single digit percentage range.
2.  In Q1 2024, firm-wide assets under custody and administration were $48.8 trillion, which was up 5% year-over-year.

(Note: The context also mentions Q1 2023 figures of $46.6 trillion, up 2% year-over-year, but the most recent specific figure provided is for Q1 2024.)
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BK_2023_Q3_prepared_remarks_200_018` -- transcript `BK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and
```

*Rank 2 -- `STT_2023_Q1_qa_200_047` -- transcript `STT_2023_Q1` -- NOT one of the question's own transcript_ids*

```
they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it won't be quite at that level because the revenues come through over time as you get the different, I'll call it, layers of services that are provided associated with those -- that assets under custody, administration. But what we'll do is we'll -- I think it's -- that may be some kind of broad perspective. What we'll try to do each quarter is give you more and more visibility as we get to those implementation points because, remember,
```

*Rank 3 -- `BK_2023_Q1_prepared_remarks_200_012` -- transcript `BK_2023_Q1` -- NOT one of the question's own transcript_ids*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 -- `STT_2023_Q1_qa_200_046` -- transcript `STT_2023_Q1` -- NOT one of the question's own transcript_ids*

```
said you should see a pickup in 2Q. Ron and Eric, what's your expectation for how much of that do you expect would get installed over the course of this year, 2Q, 3Q, 4Q? And by the time we exit this year, how much should be done? And therefore, what benefit should there be to [indiscernible] from that?

Eric Aboaf: Yeah. I think, Vivek, there are a couple of ways to think about that because what happens here is that it gets onboarded on -- in tranches. So we might onboard the assets under custody, administration, but there are multiple services that we're often providing for those assets. So we had a couple of wins over the last year or two years with $1 trillion. Those $1 trillion wins would have had some custody, some accounting, they might have had some performance analytics. They would have had some middle office services in many cases because
```

*Rank 5 -- `BK_2024_Q1_prepared_remarks_200_010` -- transcript `BK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 1 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |
| 3 | `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2024_Q1, STT_2023_Q1 | no |
| 2023 | *(not found in any retrieved chunk)* | -- | -- |
| 20 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q3, BK_2024_Q1 | no |
| 2 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |
| 1 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |
| 2024 | `BK_2024_Q1_prepared_remarks_200_010` | BK_2024_Q1 | no |
| 48.8 | `BK_2024_Q1_prepared_remarks_200_010` | BK_2024_Q1 | no |
| 5 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1 | no |
| 1 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |
| 2023 | *(not found in any retrieved chunk)* | -- | -- |
| 46.6 | `BK_2023_Q1_prepared_remarks_200_012` | BK_2023_Q1 | no |
| 2 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |
| 1 | `BK_2023_Q3_prepared_remarks_200_018`, `BK_2023_Q1_prepared_remarks_200_012`, `STT_2023_Q1_qa_200_046`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |
| 2024 | `BK_2024_Q1_prepared_remarks_200_010` | BK_2024_Q1 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 9: `ref_unans_01` / `chunk200_dense`

- **question_id:** ref_unans_01
- **condition:** chunk200_dense
- **category:** unanswerable
- **case:** A
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Gold anchor(s):** none (unanswerable question)

**Generated answer, verbatim:**

```
Northern Trust’s firm-wide assets under custody and/or administration were $46.6 trillion, which increased by 2% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BK_2023_Q3_qa_200_044` -- transcript `BK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
underneath the hood that is nuanced, that is different by different segments. Like if you think about asset servicing, our issuer services as a segment made up of three businesses, asset servicing, depository receipts, and corporate trust. Corporate trust as a business tends to attract a higher level of NIBs due to the nature of that business. Q3 would have been a seasonally quieter period for that business. Debt issuance activity was more muted. So that would explain a little bit of that. And asset servicing, let's just say how clients are behaving with us at the moment in the ecosystem, but I wouldn't really call anything out that is kind of noticeably different. And we kind of think about our deposits as one platform, kind of centrally managed under one roof, and that's how we kind of manage it.

Brian Bedell: Okay, great. And then just maybe just to follow up on the, actually in the other investment and other revenue
```

*Rank 2 -- `MS_2023_Q3_qa_200_008` -- transcript `MS_2023_Q3` -- NOT one of the question's own transcript_ids*

```
. You're right, you know, from a -- if you think about the self-directed client versus a advisory-based client that we've had in the historical wealth management franchise, one has proven to be somewhat of a stickier deposit base than you would see on the wealth management side. And I think that, you know, on the -- what I would say is the traditional wealth management side that we had historically had. So that does provide you with a sense of what's going on in terms of which client base is seeing that. On the potential growth of NII going forward, again, that's part of the same asset gathering strategy. Some proportion of these assets as they come over, be that into the self-directed or the advice-based relationship, will be held in some sort of transactional cash. So that will be supportive over time of NII to some degree from a deposit perspective. But that also provides us with lending capabilities and opportunities
```

*Rank 3 -- `BK_2023_Q1_prepared_remarks_200_012` -- transcript `BK_2023_Q1` -- NOT one of the question's own transcript_ids*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 -- `BK_2023_Q3_prepared_remarks_200_018` -- transcript `BK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and
```

*Rank 5 -- `MS_2024_Q4_prepared_remarks_200_019` -- transcript `MS_2024_Q4` -- NOT one of the question's own transcript_ids*

```
the quarterly margin by approximately 140 basis points. Asset management revenues in the quarter set a new record of $4.4 billion, showcasing the progress we have made to durable fee-based revenues. With each quarter this year, asset management revenues saw sequential improvement, powered by constructive markets and consistently strong fee-based flows. Fourth quarter fee-based flows were $35 billion. Importantly, over the last two years, we have seen an increase in the number and the pace of assets migrating from advisor-led brokerage accounts to fee-based accounts. We remain an industry leader in organic growth. Net new assets for the quarter were $57 billion. Full year NNA of $252 billion represents approximately 5% annual growth of beginning period assets. This year, our advisor-led channel drove the results, benefiting from both existing clients and new clients coming to the firm. Transactional revenues for the quarter were $1 billion. Excluding the impact of DCP, transactional revenues represent the highest level
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 46.6 | `BK_2023_Q1_prepared_remarks_200_012` | BK_2023_Q1 | no |
| 2 | `BK_2023_Q1_prepared_remarks_200_012`, `BK_2023_Q3_prepared_remarks_200_018`, `MS_2024_Q4_prepared_remarks_200_019` | BK_2023_Q1, BK_2023_Q3, MS_2024_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 10: `ref_unans_01` / `chunk500_bm25`

- **question_id:** ref_unans_01
- **condition:** chunk500_bm25
- **category:** unanswerable
- **case:** A
- **current outcome label:** answered_ungrounded

**Question:**
> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Gold anchor(s):** none (unanswerable question)

**Generated answer, verbatim:**

```
In the first quarter of 2024, Northern Trust’s firm-wide assets under custody and/or administration were $48.8 trillion, representing a 5% increase year-over-year. In the first quarter of 2023, these assets stood at $46.6 trillion, which was up 2% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BK_2023_Q1_prepared_remarks_500_004` -- transcript `BK_2023_Q1` -- NOT one of the question's own transcript_ids*

```
performance remains solid, AUM flows were mixed with strength in fixed income and LDI strategies partly offset by outflows in other long-term strategies. During the quarter, our U.K. investment manager Newton launched five future legacy funds, its first range of risk-rated sustainable multi-asset funds to support growth in the U.K. retirement market. And back in the U.S., the Dreyfus Bold share class, which we introduced last year, has now raised over $4 billion in AUM. In summary, over the past few months, I've spoken about our combination of client trust at scale platforms, client-focused culture and resilience as a powerful foundation on which we can build. I'm also proud that our culture has been front and center in recent weeks as our people have risen to the occasion, responding commercially and working tirelessly to enable successful outcomes for our clients in these uncertain times. I view this client-first culture as the key to make more out of our diversified portfolio of adjacent businesses. While we are the world's largest custodian and a trust bank, the contributions from Clearance and Collateral Management, Pershing, Treasury Services and Issuer Services are differentiating in our client value proposition. With that, let me officially welcome Dermot to his first earnings call. Dermot, over to you.

Dermot McDonogh: Thank you, Robin, for the introduction, and good morning, everyone. It's a privilege to be here, and I look forward to working with you all. I'll start on Page 3 of the presentation with some additional details on our consolidated financial results in the first quarter. Total revenue was $4.4 billion, up 11% year-over-year. This reflects fee revenue being flat as headwinds from lower market value, a stronger dollar and the sale of Alcentra, which closed in November last year, were offset by significant improvement in fee waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.
```

*Rank 2 -- `STT_2023_Q1_qa_500_018` -- transcript `STT_2023_Q1` -- NOT one of the question's own transcript_ids*

```
that that there is a range of revenue growth in our different fee categories. We've described back office as growing towards the -- traditional back office growing closer to the lower single-digit revenue growth. We've described middle and front office, which would include CRD at high single-digit growth. There will be years when it could be double-digit revenue growth. So that's what we said about that category -- this category. I think what we see in particular in software is the on-premise revenues over time will -- may not be as heavy, but we do see real momentum in the combination of the software enabled and SaaS. But all in, that should grow in the higher-single digit revenues typically though there'll be some range around that in a given year.

Vivek Juneja: Okay. And then going back to this question that's come up on the large amount of new business that remains to be installed in servicing, and you said you should see a pickup in 2Q. Ron and Eric, what's your expectation for how much of that do you expect would get installed over the course of this year, 2Q, 3Q, 4Q? And by the time we exit this year, how much should be done? And therefore, what benefit should there be to [indiscernible] from that?

Eric Aboaf: Yeah. I think, Vivek, there are a couple of ways to think about that because what happens here is that it gets onboarded on -- in tranches. So we might onboard the assets under custody, administration, but there are multiple services that we're often providing for those assets. So we had a couple of wins over the last year or two years with $1 trillion. Those $1 trillion wins would have had some custody, some accounting, they might have had some performance analytics. They would have had some middle office services in many cases because they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it
```

*Rank 3 -- `BK_2023_Q3_prepared_remarks_500_007` -- transcript `BK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
.1 billion, up 1% year-over-year. Fee revenue was flat. 2% growth in investment services fees was offset by a 19% decline in foreign exchange revenue on the back of lower volatility and volumes. Net interest revenue was up 12%. In asset servicing, investment services fees were up 3%, driven by higher market values, healthy net new business, and a weaker dollar, partially offset by lower client transaction activity. The strength of our balance sheet, as well as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and net interest revenue increased by 6%. In Pershing, investment services fees were up 2%, reflecting higher fees on sweep balances, partially upset by the impact of lost business and lower transaction volumes consistent with the decline in US equity exchange volumes. Despite the continued headwind from the ongoing deconversion of the regional bank client highlighted in the second quarter, Pershing saw $23 billion of net new assets on the platform this quarter, reflecting positive momentum in the underlying business. As Robin mentioned earlier, the momentum around Wove is building with both new and existing clients. While at the same time, ongoing investments in the core Pershing platform to enhance advisor experience and lead with innovative solutions have positioned us well to capitalize on the heightened pace of change in the RIA community. In Treasury services, investment services fees decreased by 1% as growth from higher client activity was offset by higher earnings credits for non-interest bearing deposit balances. In clearance and collateral management, investment services fees were up
```

*Rank 4 -- `BK_2024_Q1_prepared_remarks_500_004` -- transcript `BK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year, both largely reflecting higher market values. Investment and other revenue was $182 million in the quarter. Effective January 1, we adopted new accounting guidance for our investments in renewable energy projects resulting in an approximately $50 million increase to investment and other revenue. We have restated prior periods in our earnings materials to provide you with like-for-like, year-over-year and sequential comparisons. The adoption of this new accounting guidance is largely neutral to net income and earnings per share, as the increase in provision for income taxes roughly equals the increase in investment and other revenue. Net interest income decreased by 8% year-over-year, primarily reflecting changes in the composition of deposits, partially offset by the impact of higher interest rates. Expenses were up 2% year-over-year on a reported basis and up 1% excluding notable items, primarily severance expense. Growth was from incremental investments and employee merit increases offset by efficiency savings. Provision for credit losses was $27 million in the quarter, primarily driven by reserve increases related to commercial real estate exposure. As Robin mentioned earlier, we reported earnings per share of a $1.25 up 11% year-over-year, a pre-tax margin of 29% and a return on tangible common equity of 20.7%. Excluding notable items, earnings per share were $1.29, up 14% year-over-year. Pre-tax margin was 30%, and our return on tangible common equity was 21.
```

*Rank 5 -- `BK_2024_Q1_prepared_remarks_500_006` -- transcript `BK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
supplement that we filed on March 26th for detailed reconciliations to previous disclosures. Now, starting with Security Services on Page 6. Security services reported total revenue of $2.1 billion, up 1% year-over-year. Investment services fees were up 8% year-over-year. In asset servicing, investment services fees were up 8%, driven by higher market values, net new business and higher client activity. We've remained focused on deal margins, and as a result the year-over-year impact of repricing on fee growth was de-minimis. Consistent with past quarters, we continue to see particular success with our ETF offering. ETF assets under custody and/or administration surpassed $2 trillion this quarter up over 40% year-over-year on the back of higher market values, net new business and client flows, and the number of funds serviced was up 16% year-over-year. While the pace of alternative fund launches was slower than in the prior year quarter, investment services fees for alternatives were up over 10% on a year-over-year basis. Throughout the quarter, we saw broad-based strength across client segments, products and regions. In issuer services, investment services fees were up 11% reflecting net new business across both depository receipts and corporate trust, as well as higher cancellation fees in depository receipts. Foreign exchange revenue was down 11% year-over-year and net interest income was down 12%. Expenses of $1.5 billion were flat year-over-year, reflecting incremental investments, as well as the impact of employee merit increases offset by efficiency savings. Pre-tax income was $591 million, a 4% increase year-over-year, and pre-tax margin expanded to 28%. Next, Market and Wealth Services on Page 7. Market and Wealth Services reported total revenue of $1.5 billion, up 3% year-over-year. Total investment services fees were up 7% year-over-year. In Pershing, investment services fees were up 3%, reflecting higher market values and client activity, partially offset by the impact of business lost in the prior year. Net new assets were negative $2 billion for the quarter, reflecting the ongoing deconversion of the before-mentioned lost business. Client demand for our Wealth Advisor platform, Wove, continues to be strong. In the first quarter, we signed nine additional client agreements,
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 2024 | `BK_2024_Q1_prepared_remarks_500_004` | BK_2024_Q1 | no |
| 48.8 | `BK_2024_Q1_prepared_remarks_500_004` | BK_2024_Q1 | no |
| 5 | `BK_2023_Q1_prepared_remarks_500_004`, `BK_2023_Q3_prepared_remarks_500_007`, `BK_2024_Q1_prepared_remarks_500_004`, `BK_2024_Q1_prepared_remarks_500_006` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1 | no |
| 2023 | *(not found in any retrieved chunk)* | -- | -- |
| 46.6 | `BK_2023_Q1_prepared_remarks_500_004` | BK_2023_Q1 | no |
| 2 | `BK_2023_Q1_prepared_remarks_500_004`, `STT_2023_Q1_qa_500_018`, `BK_2023_Q3_prepared_remarks_500_007`, `BK_2024_Q1_prepared_remarks_500_004`, `BK_2024_Q1_prepared_remarks_500_006` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, STT_2023_Q1 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

## Stratum 3 -- answered_grounded_offtarget, spread across conditions and categories (dominant failure mode)

### Item 11: `ref_comp_10` / `chunk200_bm25`

- **question_id:** ref_comp_10
- **condition:** chunk200_bm25
- **category:** comparative
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did PNC and Fifth Third each treat AOCI when describing their capital and tangible book value per share during 2023?

**Gold anchor(s):**
> Category 3 institution, we don't include AOCI in our CET1 ratio, but I understand why
> book value per share, excluding AOCI, increased 11% compared to the year

**Generated answer, verbatim:**

```
Based on the provided context, **PNC** noted that its tangible book value increased by 1% to $77.80 in Q2 2023 "notwithstanding this AOCI impact." The company stated it expects a meaningful improvement to tangible book value from AOCI accretion as lower-rate securities and swaps roll off.

The provided context does not contain information regarding how **Fifth Third** treated AOCI when describing its capital or tangible book value per share during 2023; the available excerpt for Fifth Third is from Q4 2023 (likely referring to early 2024 actions) and discusses moving securities to held-to-maturity to de-risk potential AOCI volatility, but does not describe how AOCI was treated in their capital or TBVPS metrics during 2023.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `HBAN_2023_Q1_prepared_remarks_200_016` -- transcript `HBAN_2023_Q1` -- NOT one of the question's own transcript_ids*

```
by 13 basis points. Adjusting for AOCI, our TCE ratio was 7.27%. Tangible book value per share increased by 7% from the prior quarter to $7.32. Adjusting for AOCI, tangible book value increased to $9.23, and has increased for the past four quarters. Our capital management strategy for the balance of 2023 will result in expanding capital over the course of the year, while maintaining our top priority to fund high-return loan growth. We intend to grow CET1 to the top end of our 9% to 10% operating range by the end of the year. We believe this is a prudent approach given the dynamic environment.  Based on our expectation for continued loan growth, we do not expect to utilize the share repurchase program during 2023. Turning to Slide 20. Our capital plus reserves is top quartile in the peer group and gives us substantial total loss absorption capacity. On Slide 21, credit quality continues to perform
```

*Rank 2 -- `FITB_2023_Q4_prepared_remarks_200_004` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

*Rank 3 -- `PNC_2023_Q2_prepared_remarks_200_008` -- transcript `PNC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
rates throughout the quarter.  Notwithstanding this AOCI impact, our tangible book value increased 1% to $77.80 compared to March 31.  Importantly, as lower rate securities and swaps roll off, we expect our securities yields to continue to increase, resulting in a meaningful improvement to tangible book value from AOCI accretion.  Turning to the income statement on Slide 7. For the first half of 2023, revenue grew 11% compared to the same period a year ago, reflecting higher interest rates and overall business growth. Non-interest expense grew 4% and was well controlled despite a higher FDIC assessment rate and inflationary pressures. As a result, PPNR grew 24%.  For the second quarter, net income was $1.5 billion or $3.36 per share. Total revenue of $5.3 billion decreased $310 million or 6% compared to the first quarter of 2023. Net interest income declined 75 million or 2%, and our net interest margin was 2
```

*Rank 4 -- `BAC_2023_Q2_prepared_remarks_200_016` -- transcript `BAC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
, up modestly from the first quarter of '23, and still remains nearly $300 billion above our pre-pandemic fourth quarter '19 level. Shareholders' equity increased $3 billion from the first quarter as earnings were only partially offset by capital distributed to shareholders. AOCI decreased by $2 billion, driven by derivatives valuation and AFS securities values were little changed. So, there is little change in the AOCI component that impacts regulatory capital. Tangible book-value is up 10% per share year-over-year. During the quarter, we also paid out $1.8 billion in common dividends, and we bought back $550 million in shares to offset our employee awards. And last week, we announced the intent to increase our dividend by 9%, beginning in the third quarter. Turning to regulatory capital, our CET1 level improved to $190 billion from March 31st, and the ratio of CET1 improved more than 20 basis points to 11.6
```

*Rank 5 -- `PNC_2024_Q2_prepared_remarks_200_005` -- transcript `PNC_2024_Q2` -- NOT one of the question's own transcript_ids*

```
and improved $600 million compared with March 31st. Our tangible book value increased $89.12 per common share, a 4% increased linked quarter, and a 15% increase compared to the same period a year ago. We remain well capitalized and our estimated CET1 ratio increased to 10.2% as of June 30th. Regarding the Basel III end-game, we expect the inclusion of AOCI in the final rule and our CET1 ratio with the impact of AOCI would be 8.7%. And while we recognize the likelihood of changes to certain other aspects of the Basel III end-game NPR, under the currently proposed capital rules, our estimated fully phased-in expanded risk-based CET1 ratio would be approximately 8.4%. We continue to be well positioned with capital flexibility. We returned roughly $700 million of capital to shareholders during the quarter, which included $600 million in common dividends and $100 million of share repurchases. And
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 1 | `HBAN_2023_Q1_prepared_remarks_200_016`, `FITB_2023_Q4_prepared_remarks_200_004`, `PNC_2023_Q2_prepared_remarks_200_008`, `BAC_2023_Q2_prepared_remarks_200_016`, `PNC_2024_Q2_prepared_remarks_200_005` | BAC_2023_Q2, FITB_2023_Q4, HBAN_2023_Q1, PNC_2023_Q2, PNC_2024_Q2 | no |
| 77.80 | `PNC_2023_Q2_prepared_remarks_200_008` | PNC_2023_Q2 | no |
| 2 | `HBAN_2023_Q1_prepared_remarks_200_016`, `FITB_2023_Q4_prepared_remarks_200_004`, `PNC_2023_Q2_prepared_remarks_200_008`, `BAC_2023_Q2_prepared_remarks_200_016`, `PNC_2024_Q2_prepared_remarks_200_005` | BAC_2023_Q2, FITB_2023_Q4, HBAN_2023_Q1, PNC_2023_Q2, PNC_2024_Q2 | no |
| 4 | `FITB_2023_Q4_prepared_remarks_200_004`, `PNC_2023_Q2_prepared_remarks_200_008`, `PNC_2024_Q2_prepared_remarks_200_005` | FITB_2023_Q4, PNC_2023_Q2, PNC_2024_Q2 | no |
| 2024 | `FITB_2023_Q4_prepared_remarks_200_004` | FITB_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 12: `ref_comp_01` / `chunk200_hybrid`

- **question_id:** ref_comp_01
- **condition:** chunk200_hybrid
- **category:** comparative
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did Goldman Sachs and Citi differ in how they characterised Basel III endgame uncertainty in late 2023 and early 2024?

**Gold anchor(s):**
> taking a more conservative posture around that, just given some of the uncertainty around Basel
> how the Basel III endgame proposal could evolve, but that hasn't

**Generated answer, verbatim:**

```
Based on the provided context, Goldman Sachs characterized the Basel III endgame uncertainty as a factor that would be resolved through "significant modifications" to the proposed rule, which they expected would provide them with "materially more flexibility on capital deployment." In contrast, Citi’s prepared remarks in late 2023 did not explicitly characterize the Basel III endgame; instead, Jane Fraser focused on the company's progress in simplifying operations and executing its strategy, noting that Q4 results were disappointing. The context does not contain specific statements from Citi regarding their characterization of Basel III uncertainty during this period.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `GS_2024_Q2_qa_200_020` -- transcript `GS_2024_Q2` -- NOT one of the question's own transcript_ids*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution
```

*Rank 2 -- `USB_2023_Q4_qa_200_016` -- transcript `USB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
. And now you're sitting here with 9.9% CET1. No longer have to be a Category II bank early, and all the color that we're getting from Washington is that Basel III endgame will be at least delayed, if not soften significantly. As you think about maybe just one more hurdle ahead over the near term in terms of the DFAST, how are you thinking about where U.S.-based proper CET1 ratio is in terms of the minimum looking forward to a future where maybe capital is a little bit tighter, but you're also growing? And do you feel like you're now on offense and all the sort of the balance sheet management that was designed to optimize capital is fully behind you?

Andy Cecere: Yeah, Erika, as John mentioned, I think our balance sheet optimization efforts are behind us. Our focus on capital accretion will be from earnings as we go into 2024 and forward. As
```

*Rank 3 -- `JPM_2023_Q3_prepared_remarks_200_017` -- transcript `JPM_2023_Q3` -- NOT one of the question's own transcript_ids*

```
political situation, economic outlook, rate environment, deposit reprice and the impact of the Basel III endgame proposal are as prominent now as they have been in the recent past. But as always, we continue to prepare for a range of scenarios and are focused on being there for our clients and customers when they need us most. And with that, let's open the line for Q&A.
```

*Rank 4 -- `GS_2024_Q1_prepared_remarks_200_014` -- transcript `GS_2024_Q1` -- NOT one of the question's own transcript_ids*

```
. Given expectations for significant modifications to the Basel III proposed rule, we should have materially more flexibility on capital deployment. We also remain committed to paying our shareholders a sustainable and growing dividend. In conclusion, our first quarter results reflect the strength of our leading global banking and markets franchise and our growing Asset & Wealth Management business. Simply put, we are delivering on the things we said we would do. We are focused on our strategic objectives and the execution focus areas for 2024 that we laid out in January, which will help our businesses produce mid-teens returns through the cycle. We are confident in our ability to deliver for shareholders while continuing to support our clients and remain optimistic about the future opportunity set for Goldman Sachs. With that, we'll now open up the line for questions.
```

*Rank 5 -- `C_2023_Q4_prepared_remarks_200_001` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
subject to uncertainty and changes in circumstances. Actual results may differ materially from these statements due to a variety of factors, including those described in our earnings materials, as well as in our SEC filings. And with that, I'll turn it over to Jane.

Jane Fraser: Thank you, Jenn, and a very Happy New Year to everyone, and I hope you all had a good break. At Citi, we're back at it. And given the notable items and our new financial reporting structure, we've got a lot to cover today, so I'm going to get right to it. 2023 was a foundational year in which we made substantial progress, simplifying Citi and executing the strategy we laid out at Investor Day. With that said, the fourth quarter was clearly very disappointing. Today, I'm going to provide a high-level view on our progress in 2023, discuss our Q4 results and finish with our priorities for '
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 4 | `USB_2023_Q4_qa_200_016`, `GS_2024_Q1_prepared_remarks_200_014`, `C_2023_Q4_prepared_remarks_200_001` | C_2023_Q4, GS_2024_Q1, USB_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 13: `ref_comp_10` / `chunk500_hybrid`

- **question_id:** ref_comp_10
- **condition:** chunk500_hybrid
- **category:** comparative
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did PNC and Fifth Third each treat AOCI when describing their capital and tangible book value per share during 2023?

**Gold anchor(s):**
> Category 3 institution, we don't include AOCI in our CET1 ratio, but I understand why
> book value per share, excluding AOCI, increased 11% compared to the year

**Generated answer, verbatim:**

```
Based on the provided context, both banks highlighted improvements in Accumulated Other Comprehensive Income (AOCI) that positively impacted their tangible book value per share during 2023:

*   **PNC:** In Q4 2023, PNC reported that AOCI improved by $2.6 billion due to lower interest rates. This improvement contributed to a 9% linked-quarter increase in tangible book value per common share to $85.08. The bank noted that as lower-rate securities and swaps roll off, they expect continued meaningful improvements to tangible book value from AOCI accretion.
*   **Fifth Third:** In Q4 2023, Fifth Third stated that its tangible book value per share grew nearly 30% during the quarter, driven in part by a significant rally in interest rates (which typically increases AOCI for banks with fixed-rate assets or specific portfolio structures, though the text explicitly links the growth to earnings and rate movements). Additionally, the bank moved $12.6 billion of securities to held-to-maturity at the beginning of January 2024 to de-risk potential AOCI volatility to capital by about 30% in case rates rise again.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2023_Q4_prepared_remarks_500_001` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
AOCI of 15.9% and an adjusted efficiency ratio of 55.9%. All among the best of our peers. We also continue to take market share organically by growing our customer base and deepening relationships. We grew consumer households by 3% overall punctuated by 6% growth in the Southeast. In commercial, we added a record number of new quality middle market relationships up 11% over the prior year. As a result, we grew or maintained our deposit market share position in all 40 of our largest MSAs. As we turn the page to 2024, we remain focused on differentiating Fifth Third based on the strength and consistency of our financial performance by prioritizing stability, profitability, and growth in that order. Bryan will take you through the detail on the fourth quarter and our outlook for the year shortly. But before that, I would like to touch on a few points. The first of these is the strength of our balance sheet. Our defensive positioning and decision to move quickly to adapt to proposed regulatory changes have put us in a position to play offense in 2024. Having achieved full Category 1 LCR compliance on August 31st and maintained it since, our liquidity position is very strong. We completed our RWA diet in the fourth quarter and accreted nearly 50 basis points of CET1, putting us on pace to reach a 10.5% CET1 ratio by mid-year 2024. Given our strong earnings profile and the significant rally in interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

*Rank 2 -- `FITB_2024_Q3_prepared_remarks_500_006` -- transcript `FITB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
exceeding our buffered minimum of 7.7%, reflecting strong capital levels. Our pro-forma CET1 ratio, including the AOCI impact of the securities portfolio is 8.7%. We expect continued improvement in the unrealized losses in our securities portfolio, given that 59% of the AFS portfolio is in bullet or locked out securities, which provides a high degree of certainty to our principal cash flow expectations. Assuming the forward curve is realized, approximately 24% of the AOCI related to securities losses will accrete back into equity by the end of 2025, increasing tangible book value per share by 6% before considering any future earnings. 61% of the securities related AOCI should accrete back to equity by the end of 2028. During the quarter, we completed $200 million in share repurchases, which reduced our share count by 4.9 million shares. As we assess our capital priorities, we continue to believe that 10.5% is an appropriate near-term operating level. Moving to our current outlook, we anticipate continued growth in NII and NIM during the Q4, with NII up 1% sequentially, reflecting the impact of lower deposit rates and the continued benefit of fixed rate asset repricing, partially offset by the decrease in yield from our floating rate loan portfolio. This outlook assumes a 25 basis point cut in November and a 50 basis point cut in December. We would not expect any change to this outlook if fewer rate cuts were to occur. We expect average total loan balances to be stable to up 1% from the third quarter, with middle market and auto production offsetting mix demand in other asset classes. Fourth quarter adjusted noninterest income is anticipated to rise 3% to 4% compared to the strong Q3, largely due to a continued rebound in capital markets revenue and continued growth in commercial payments. Additionally, we expect fourth quarter TRA revenue to be $10 million down from $22 million in the fourth quarter of 2023. Fourth quarter total adjusted noninterest expenses are expected to be stable compared to the third quarter as the increases in revenue-based compensation and the investments in branches and technology are largely offset by efficiencies achieved in other areas. Fourth quarter net charge-offs are projected to be similar or slightly down from the third quarter. Given the expected increase in loans during the fourth quarter, we anticipate an ACL build of $20
```

*Rank 3 -- `PNC_2023_Q2_prepared_remarks_500_003` -- transcript `PNC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
received fixed swaps pointed to the commercial loan book totaled $40 billion at the end of the second quarter. The weighted average received fixed rate of our swap portfolio increased 25 basis points linked quarter to 1.73%, and the portfolio duration was 2.3 years as of June 30.  During the second quarter, our accumulated other comprehensive loss increased by $400 million. Paydowns and maturities were in line with our expectations, but were more than offset by the negative impact from higher than expected rates throughout the quarter.  Notwithstanding this AOCI impact, our tangible book value increased 1% to $77.80 compared to March 31.  Importantly, as lower rate securities and swaps roll off, we expect our securities yields to continue to increase, resulting in a meaningful improvement to tangible book value from AOCI accretion.  Turning to the income statement on Slide 7. For the first half of 2023, revenue grew 11% compared to the same period a year ago, reflecting higher interest rates and overall business growth. Non-interest expense grew 4% and was well controlled despite a higher FDIC assessment rate and inflationary pressures. As a result, PPNR grew 24%.  For the second quarter, net income was $1.5 billion or $3.36 per share. Total revenue of $5.3 billion decreased $310 million or 6% compared to the first quarter of 2023. Net interest income declined 75 million or 2%, and our net interest margin was 2.79%, a decline of 5 basis points.  Non-interest income declined $235 million or 12%, driven by both lower fee income and other non-interest income, which included Visa fair value adjustments of a negative $83 million that I will discuss in a moment. Second quarter expenses increased $51 million or 2% linked quarter.  Provision was $146 million in the second quarter, reflecting portfolio activity and changes in macroeconomic variables, and our effective tax rate was 15.5%, which included the favorable impact of certain tax matters in the second quarter.  Turning to Slide 8, we highlight our revenue trends. Second quarter revenue was down $310 million or 6% compared with the first quarter. Net interest income of $3.5 billion decreased $75 million or 2%, with higher yields on interest earning assets were more than offset by increased funding costs and lower loan and security balances. Fee income was $1.7 billion and decreased $106 million or 6% linked quarter
```

*Rank 4 -- `PNC_2023_Q4_prepared_remarks_500_003` -- transcript `PNC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
swaps pointing to the commercial loan book totaled $33 billion on December 31st. The weighted-average received fixed rate of our swap portfolio increased three basis points to 2.1% and the duration of the portfolio was 2.3 years. AOCI improved by $2.6 billion in the fourth quarter, reflecting lower interest rates. Importantly, as lower rate securities and swaps roll-off, we expect a continued meaningful improvement to tangible book value from AOCI accretion. Turning to the income statement on Slide 7. Fourth quarter net income was $883 million or $1.85 per share, which included pre-tax non-core expenses of $665 million or $525 million after tax related to the FDIC special assessment and the workforce reduction charges incurred in the fourth quarter. Excluding non-core expenses, adjusted EPS was $3.16. Total revenue of $5.4 billion increased $128 million or 2% compared to the third quarter of 2023. Net interest income declined modestly by $15 million. And our net interest margin was 2.66%, a decline of five basis points.  Non-interest income increased to $143 million, or 8%. Non-interest expense of $4.1 billion increased $829 million or 26% and included $665 million of non-core expenses. Core non-interest expense was $3.4 billion and increased $164 million or 5%. Provision was $232 million in the fourth quarter and our effective tax rate was 16.3%. Full year 2023 revenue grew 2% compared to 2022. Core non-interest expense was well controlled and grew 1%. Importantly, our disciplined expense management and CIP savings allowed us to deliver modest positive operating leverage and PPNR growth of 2% on an adjusted basis. Turning to Slide 8, we highlight our revenue trends. Fourth quarter revenue was up $128 million, or 2% compared with the third quarter, driven by strong fee income as net interest income of $3.4 billion was down modestly. Fee income was $1.8 billion and increased $99 million or 6% linked quarter. Looking at the detail, capital markets and advisory fees rebounded as expected and increased $141 million, or 84%, driven by higher M&A advisory fees. Asset Management and Brokerage revenue grew $12 million or 3%, reflecting favorable market conditions. And residential and commercial mortgage revenue declined $52 million or 26
```

*Rank 5 -- `PNC_2023_Q4_prepared_remarks_500_001` -- transcript `PNC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
. Expense discipline remains a top priority for us and accordingly we are targeting stable expenses for 2024 even as we continue to invest in key growth initiatives. Fourth, our credit quality remained strong during the quarter, reflecting our thoughtful approach us to growing our balance sheet. While we continue to expect credit charge offs to increase over time, particularly in the CRE office segment, we’re adequately reserved. Finally, during the fourth quarter, we increased our capital position, saw solid improvement in our AOCI intangible book value and repurchased a modest amount of shares. In summary, we run our company with a focus on delivering through the cycle performance and feel very good about our strategy, our capabilities and the strength of our balance sheet as we enter 2024. And we believe we are well positioned to drive growth and deliver shareholder value in the coming year and beyond. As always, I want to thank our employees for everything they do to meet the needs of our customers and make our success possible.  And with that, I'll turn it over to Rob.

Rob Reilly: Thanks, Bill, and good morning, everyone. Our balance sheet is on Slide 3 and is presented on an average basis and compared to the third quarter. Loans were up 2% and averaged $325 billion, which includes the acquired Signature capital commitment loans. Investment securities declined $2 billion or 2%. Cash balances at the Federal Reserve increased $4 billion to $42 billion and deposits increased $1.4 billion and averaged $424 billion. Borrowed funds increased $5 billion to $73 billion, driven by higher FHLB borrowings and parent company senior debt issuances. At year end, P&C was fully compliant with the proposed holding company long term debt requirements. And we expect to reach compliance with the bank level metrics through our normal course of funding well in advance of the phase in period. AOCI improved $2.6 billion to negative $7.7 billion at quarter end, primarily reflecting the impact of favorable interest rate movements during the quarter. Accordingly, tangible book value increased to $85.08 per common share, up 9% linked quarter and 18% compared to the same period a year ago. We remain well capitalized with an estimated CET1 ratio of 9.9% as of December 31st, which increased 10 basis points linked quarter. Our estimated fully phased in expanded risk based CET1 ratio based on the new proposed capital rules would be approximately 8
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 4 | `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2024_Q3_prepared_remarks_500_006`, `PNC_2023_Q2_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q4, FITB_2024_Q3, PNC_2023_Q2, PNC_2023_Q4 | no |
| 2.6 | `FITB_2023_Q4_prepared_remarks_500_001`, `PNC_2023_Q4_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q4, PNC_2023_Q4 | no |
| 9 | `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2024_Q3_prepared_remarks_500_006`, `PNC_2023_Q2_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q4, FITB_2024_Q3, PNC_2023_Q2, PNC_2023_Q4 | no |
| 85.08 | `PNC_2023_Q4_prepared_remarks_500_001` | PNC_2023_Q4 | no |
| 4 | `FITB_2023_Q4_prepared_remarks_500_001`, `FITB_2024_Q3_prepared_remarks_500_006`, `PNC_2023_Q2_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_003`, `PNC_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q4, FITB_2024_Q3, PNC_2023_Q2, PNC_2023_Q4 | no |
| 30 | `FITB_2023_Q4_prepared_remarks_500_001`, `PNC_2023_Q2_prepared_remarks_500_003` | FITB_2023_Q4, PNC_2023_Q2 | no |
| 12.6 | `FITB_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q4 | no |
| 2024 | `FITB_2023_Q4_prepared_remarks_500_001`, `PNC_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q4, PNC_2023_Q4 | no |
| 30 | `FITB_2023_Q4_prepared_remarks_500_001`, `PNC_2023_Q2_prepared_remarks_500_003` | FITB_2023_Q4, PNC_2023_Q2 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 14: `ref_them_02` / `chunk500_bm25`

- **question_id:** ref_them_02
- **condition:** chunk500_bm25
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did banks characterise the uncertainty around the Basel III endgame proposal over 2023 and 2024, and how did it affect their capital actions?

**Gold anchor(s):**
> capital, while uncertainty about the Basel III Endgame prevails, our capital position remains very robust
> pace of buybacks will likely remain modest in light of the Basel III

**Generated answer, verbatim:**

```
Based on the provided context, banks characterized the uncertainty surrounding the Basel III endgame proposal in several ways:

*   **JPMorgan Chase** described the proposed increases as "overcalibrated" and noted that the absence of detailed analysis supporting such a large capital increase was "disconcerting." They viewed the proposals as flawed due to issues with GSIB surcharges and operational risk overlaps.
*   **Morgan Stanley** acknowledged significant speculation regarding the rules but emphasized that they had not yet seen the actual proposed rules, noting there would be an extensive comment period. Management expressed encouragement from regulators who wanted to hear industry comments and ensure the right economic outcomes. They also noted uncertainty regarding whether the rules were being fully implemented in Europe compared to the U.S.
*   **Goldman Sachs** highlighted lingering uncertainty regarding both the "quantum and timing" of the proposal's resolution, noting that it might not take effect until 2025.

This uncertainty affected their capital actions as follows:

*   **JPMorgan Chase** indicated that the pace of share buybacks would likely remain modest in light of the proposal.
*   **Morgan Stanley** stated they needed to see the proposed rule first before determining specific mitigating actions, though they noted flexibility around Risk-Weighted Assets (RWA) and maintained a cautious stance due to recent banking sector stress.
*   **Goldman Sachs** chose to operate at the wider end of their capital range, maintaining a higher-than-normal cushion (90 bps above normal) to signal flexibility and support client returns while managing the regulatory uncertainty.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `JPM_2023_Q3_prepared_remarks_500_002` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
problem at the outset has made matters worse. And now all of those problems are being applied to an additional $500 billion of RWA. Our view is that the combined proposals could have adjusted the surcharge levels to keep dollars of capital associated GSIB buffer constant rather than simply multiplying the RWA increase by the existing surcharges. Another lens on the proposed increases is the introduction of RWA for operational risk and its clear overlap with op risk losses already capitalized through the stress capital Buffer. Although there is limited disclosure from the Fed on this point, we have estimated that we have about $15 billion of operational risk capital embedded in the SCB based on the information the Fed does disclose. Once we capitalize for this new op risk RWA, our required capital will go up by around $30 billion without any change to our portfolio. Now let's turn to Page 5, which shows the impact of the actual and proposed capital rules over the last few years. Zooming out from the details of this most recent proposal, this page reminds us of what's happened since 2017. Since then, SA-CCR and the stress capital buffer have been adopted and our GSIB surcharge will increase to 4.5%. So assuming the Basel III endgame and GSIB proposals are finalized in their current form, we would see a 45% increase in our capital requirements relative to that 2017 starting point. This illustrates again how overcalibrated these proposals are and it's not done yet. We still expect the Fed to incorporate CECL into CCAR, which will likely increase the SCB. And, of course, given the absence of a fix to the GSIB clause, it continues to present a headwind into the indefinite future. And aside from those dynamics, there remains the long-standing issue of procyclicality in the overall capital [Technical Difficulty]. We think it's also important to point out that the agencies did actually have a choice here. While it may technically be true that the proposal is Basel compliant, Basel compliant does not mandate a 25% increase in capital requirements. Implementing the Basel III endgame consistently with how the Europeans have by retaining credit risk modeling and also addressing the compounding effects of GSIB and SCB would have achieved Basel compliance without creating this unnecessary increase in capital requirements. As you would expect, we will continue to engage and forcefully advocate during the comment period and beyond in a great deal of
```

*Rank 2 -- `MS_2023_Q2_qa_500_000` -- transcript `MS_2023_Q2` -- NOT one of the question's own transcript_ids*

```
Operator: [Operator Instructions] We'll take our first question from Ebrahim Poonawala with Bank of America. Your line is now open. Please go ahead.

Ebrahim Poonawala: Thank you, and good morning.

James Gorman: Good morning.

Ebrahim Poonawala: I guess maybe first question, James, for you. Thanks for the update on the succession. As we think about what you built in terms of the franchise, and I think you talked about the unfolding Basel Endgame rules that are expected over the next week or two, from a shareholder perspective, do you see these rules as game-changing where investors will have to reevaluate the value proposition of Morgan Stanley as a franchise? And you, as a management team, would have to review strategic targets that you've laid out? Give us a sense. And I know plenty of unknowns. But I think the question we get from shareholders is the comfort around the ability of the firm to manage through what could be pretty radical changes.

James Gorman: Well, it's an important question. And you're right, I have made comments on it. Let's sort of set the table of where we are right now. We've had a lot of speculation based off of what the Basel III Endgame looks like. By the way, I'm not sure it's actually being implemented fully in Europe, just to say. I think the U.S. banks actually have more capital, but putting that knit aside, we did get the speech from the Vice Chair. I think it's important to look at the title of that speech, which was holistic capital review. So, it's taking into account all of the CCAR, stress tests, SCB buffers and the like as this stuff is implemented. Secondly, we haven't seen the actual rules. I mean, I guess there will be a proposal coming out, as you said, in a couple of weeks. There will be an extensive comment period. There is clearly very different views as to the need for the U.S. banking system to accrete more capital. In fact, if you look at the test of the last few years, what happened with the regional banks, what -- Silicon Valley First Republic Signature, what happened during COVID, what's happened during this period of high inflation, what's happened with the biggest rate increase
```

*Rank 3 -- `JPM_2023_Q3_prepared_remarks_500_001` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
Expenses of $20.9 billion were up $1.7 billion or 9% year-on-year, primarily driven by ongoing growth and front office and technology staffing, as well as wage inflation and higher legal expense. And credit costs were $1.4 billion, predominantly driven by net charge-offs in Card, and included a $102 million net reserve release, driven by changes in the central scenario, primarily offset by card loan growth. On to balance sheet and capital on Page 3. We ended the quarter with a CET1 ratio of 14.3%, up about 50 basis points versus the prior quarter as the benefit of net income less capital distributions was partially offset by AOCI. We had $2 billion of net share repurchases this quarter and the pace of buybacks will likely remain modest in light of the Basel III endgame proposal. In line with our capital hierarchy, we will continue to reassess the buyback trajectory as circumstances evolve or opportunities emerge. And on the topic of the Basel III endgame, you'll see that we added a couple of pages on it. So, let's cover that now, starting on Page 4. Given the significance of this proposal for us, the broader industry as well as households and businesses as end-users, we thought it was important to spend time discussing it. And while we know there is interest in having us quantify the expected impact of this proposal in a lot of granular detail, it's important to start by asking why the proposed increase is so large given the repeated statement over time by policymakers that banks are well-capitalized and well-positioned to deal with stress. Given that context, the absence of detailed analysis supporting a capital increase of this magnitude is disconcerting and there's a lot that does not make sense to us. Starting with RWA, we've already said we expect the firm's RWA to increase by around 30% or $500 billion, which results in capital requirements increasing by about 25% or $50 billion. One immediate thing to point out is that at 4.5% GSIB, a $500 billion increase in RWA requires $22.5 billion of additional capital with no change in our systemic risk footprint. We've been on the record for a long time that GSIB was conceptually flawed and miscalibrated originally. Since implementation, the failure to address economic growth despite the Fed themselves acknowledging this
```

*Rank 4 -- `GS_2024_Q2_qa_500_008` -- transcript `GS_2024_Q2` -- NOT one of the question's own transcript_ids*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution. It sounds from some of Powell's latest comments that, that may not be something that comes into effect until perhaps into 2025, but we are sort of maintaining a level of cushion that think is appropriate in light of what we know and we don't know about the future opportunity set for Goldman Sachs, but that buffer is designed to support clients return capital shareholders, while maintaining a prudent buffer with some of the lingering uncertainty with respect to future regulatory input.

Steven Chubak: Helpful color. Thanks for taking my questions.

Dennis Coleman: Thank you.

Operator: We'll go next to Devin Ryan with Citizens JMP.

Devin Ryan: All right, great. Good morning, David and Dennis. A couple questions on AWM progress. So the first one is on the alts business specifically, and you're tracking obviously well ahead of the fundraising targets relative to when you set the $1 billion medium term target for annual incentive fees? And now with over $500 billion in alts AUM and obviously growing, that would seem pretty conservative. So I appreciate there's a lot of work to do to generate the returns ahead here, but how should we think about the underlying assumptions for incentive fees in a more normal harvesting environment, just given the mixed shift and the growth that you're seeing in AUM there?

Dennis Coleman: So Devin, I think it's a good question, and I think we share your expectation that, that's going
```

*Rank 5 -- `MS_2023_Q2_qa_500_006` -- transcript `MS_2023_Q2` -- NOT one of the question's own transcript_ids*

```
savings or seeing savings products, we still have over 80% of our actual deposit base is coming from our own client base. What's interesting in terms of the movement of sweeps, which might be your question, I'm not sure I'm totally answering it, Glenn, is that we began to see some of those sweeps not just -- remember, we used to see them move into money markets or other cash alternatives. In June, we began to see some of those dollars actually move into markets, so various assets. We hadn't seen that trend since January. So that just shows that some of the clients are actually also deploying excess cash or cash equivalents actually into the marketplace as well.

Operator: For our next question, we'll move to Steven Chubak with Wolfe Research. Please go ahead.

Steven Chubak: Hey, good morning. So James, I appreciate your comments on Basel III Endgame. It might be helpful if you could just speak to how the lengthy transition period informs your near-term buyback appetite if at all? And given the RWA inflation could be quite meaningful, what are some of the mitigating actions you can pursue to alleviate some of the pressure on your businesses?

James Gorman: Well, again, I think, Steve, we've got to see the rule proposed first. I mean, without talking out of school, I clearly had conversations with all the appropriate regulatory bodies. And I'm encouraged by their response, which is they sincerely want to hear comments from the industry. They do understand capital changes across the whole industry have to result in the right economic outcome for the country. And by definition, the bank's stability, as evidenced by the recent many years of CCARs, shows that the G-SIB banks, the top eight banks for sure, are well capitalized. So, I don't want to get ahead and talk about what we'd mitigate. Clearly, we have flexibility around our RWAs. You saw that this quarter, we ended up with 15.5% CET1. We did that not really from a Basel III perspective. I mean, we had that in the back of my mind, but more from this environment, it was a little squarely. I mean, let's just say it that you had three bank fails at the beginning of the quarter. That wasn't a good look. So, we wanted to be cautious
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 2025 | `GS_2024_Q2_qa_500_008` | GS_2024_Q2 | no |
| 90 | `GS_2024_Q2_qa_500_008` | GS_2024_Q2 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 15: `ref_them_04` / `chunk500_bm25`

- **question_id:** ref_them_04
- **condition:** chunk500_bm25
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Gold anchor(s):**
> 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven
> operating leverage this quarter as expenses decreased 4%, driven by actions taken to right size

**Generated answer, verbatim:**

```
Based on the provided context, banks described their progress on positive operating leverage as follows:

*   **Bank of New York Mellon (BNY Mellon):** In Q1 2023, they reported delivering positive operating leverage year-over-year. For full-year 2023, they stated that excluding notable items, they generated approximately 180 basis points of positive operating leverage, which contributed to improved pre-tax margins and return on tangible common equity.
*   **State Street (STT):** In Q1 2024, the bank reported delivering both positive fee and total operating leverage relative to the year-ago period. They noted that underlying expenses were well-controlled, with first-quarter expenses increasing just 1% year-over-year excluding notable items, despite increased investments in the business.
*   **U.S. Bancorp (USB):** In Q4 2024, they highlighted their delivery of 190 basis points of positive operating leverage as a showcase of their commitment to execution and financial discipline. For Q1 2025 guidance, they expected to deliver at least 200 basis points of positive operating leverage year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2023_Q1_prepared_remarks_500_000` -- transcript `FITB_2023_Q1` -- NOT one of the question's own transcript_ids*

```
Chris Doll: Good morning everyone. Welcome to Fifth Third’s First Quarter 2023 Earnings Call. This morning our President and CEO, Tim Spence and CFO, Jamie Leonard will provide an overview of our first quarter results and outlook. Our Treasurer, Bryan Preston has also joined for the Q&A portion of the call. Please review the cautionary statements and our materials which can be found on our earnings release and presentation. These materials contain information regarding to the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third’s performance. These statements speak only as of April 20th 2023 and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris. And good morning, everyone. Thank you for joining us today. The past six weeks have seen a great deal of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide impact of quantitative tightening and normal seasonal pressures. Our key credit metrics remain near historical lows with net charge-offs of 26 basis points coming in at the low end of our guidance range. NPAs NPLs and early stage delinquency ratios remained below normalized levels, and criticized assets decrease modestly during the quarter. Moreover, we accomplished all this while also being recognized by Ethisphere as one of only two U.S. banks on their world's most ethical companies
```

*Rank 2 -- `BK_2023_Q4_prepared_remarks_500_001` -- transcript `BK_2023_Q4` -- NOT one of the question's own transcript_ids*

```
not only highlight BNY Mellon's characteristic resilience, but they demonstrate the strength of our execution when we are appropriately organized and focused. On a reported basis, 2023, earnings per share increased by 38% year-over-year. On a core basis, excluding notable items, EPS of $5.05 increased by 10% year-over-year. Both pre-tax margin and return on tangible common equity improved on the back of significant operating leverage. Excluding notable items, we generated approximately 180 basis points of positive operating leverage. ROTCE improved 0.5 percentage point to 21.6%, and pre-tax margin improved roughly 80 basis points to 30%. Moving on to Page 3. At the beginning of last year, we communicated three financial goals for 2023. First, we expected to generate approximately 20% net interest revenue growth year-over-year. We delivered 24%. Second, we set out to half our constant-currency expense growth rate in 2022 to approximately 4% year-over-year expense growth, excluding notable items in 2023. We delivered 2.7%. And third, we sought to return north of 100% of 2023 earnings to common shareholders through dividends and buybacks. We delivered 123%. Over the course of 2023, we returned $3.9 billion of capital to common shareholders, all while having further strengthened our regulatory capital ratios to be well-positioned for a wide range of macroeconomic and regulatory outcomes. So we are still at the beginning of our transformation journey. Our ability this past year, not just to deliver on our commitments but to exceed them gives us confidence that we can effect meaningful change and consistently improve our financial performance over time. While mindful, there is a lot more work ahead of us. I'm proud of the effort that our people put in over the last 12 months as we embraced a focus on commerciality, accountability and efficiency, which drove these results. We are committed to improving the firm's financial performance in the near, medium and long term, and we have framed this work for our people with three strategic pillars, which we describe on Page 4. Last year we introduced these three pillars to get at the heart of how we operate and who we are day-to-day for our clients, managing their money, moving it and keeping it safe. Pillar number one, be more for our clients; number two, run our company better; and number three
```

*Rank 3 -- `STT_2024_Q1_prepared_remarks_500_001` -- transcript `STT_2024_Q1` -- NOT one of the question's own transcript_ids*

```
while continuing to invest meaningfully in our business and controlling underlying expenses. Excluding notable items, we delivered both positive fee and total operating leverage, as well as solid EPS growth in Q1 relative to the year ago period. The first quarter was an important milestone. We have detailed our strategic priorities for 2024, including the growth initiatives we are undertaking across each of our business areas, as we continue to both invest in our capabilities and also target further productivity gains. Guided by our purpose to help create better outcomes for the world's investors and the people they serve, our four strategic priorities are aimed at continuing to extend our competitive advantage, while delivering positive fee operating leverage excluding notable items in 2024. These 2024 priorities are: growing fee revenue; extending our leadership in our markets and financing and global advisors franchises; enhancing and optimizing our operating model; and continuing to differentiate our business through innovative client solutions and technology-led capabilities to support business growth. We remain intensely focused on executing against these strategic priorities, particularly in a dynamic operating environment in which financial market expectations continue to change significantly. For example, as inflation remains elevated and economic data continued to be robust, investors pushed back their expectation for the timing of Central Bank rate cuts and treasury yields increased during the first quarter. Despite this, global equity markets performed strongly and volatility remained muted, with many indices setting records as fears of a hard economic landing receded and optimism surrounding the potential economic benefit from artificial intelligence continued in Q1. Turning to slide three of our investor presentation, I will review our first quarter highlights before Eric takes you through the quarter in more detail. Beginning with our financial performance, 2024 started strongly. Year-over-year, we produced both positive fee and total operating leverage, as well as good EPS growth, excluding notable items. First quarter EPS was $1.37 or $1.69, excluding a notable item related to the increase to the FDIC special assessments. Underlying year-over-year EPS growth was supported by total fee revenue growth and continued common share repurchases, which more than offset the impact of lower NII on total revenue. Underlying expenses continued to be well controlled, supported by our ongoing productivity efforts, with first quarter expenses increasing just 1% year-over-year, excluding notable items, even as we have increased the level of investments in our business. Turning to our business momentum, which you can see on the middle of the slide, we continue to make progress
```

*Rank 4 -- `USB_2024_Q4_prepared_remarks_500_003` -- transcript `USB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
5 forward-looking guidance on Slide 15. Starting with the first quarter 2025 guidance, net interest income is expected to be relatively stable to the fourth quarter of 2024, excluding the impact of fewer days. As a reminder, the first quarter has two fewer days than the fourth quarter. Total non-interest expense is expected to be relatively stable to the fourth quarter level of approximately $4.2 billion as adjusted. We expect to deliver positive operating leverage in the first quarter of 200 basis points or more on a year-over-year basis. I'll now provide full-year 2025 guidance. Total revenue growth on an adjusted basis is estimated to be in the range of 3% to 5% compared to the full year 2024. We expect to achieve positive operating leverage excluding the impact of security gains or losses of greater than 200 basis points for the full year. I'll now hand it back over to Andy for closing remarks.

Andy Cecere: Thanks, John. 2024 was a pivotal year for the company in many ways and it marked a very important inflection point in our story. Going into the year, there was much uncertainty with respect to the broader macroeconomic environment, persistent inflation, significant rate volatility, political and regulatory headwinds to name a few, but we effectively managed through the changes and most importantly executed on our strategic objectives. Fourth quarter results showcase our commitment to execution which was highlighted by our delivery of 190 basis points of positive operating leverage. As credit quality continued to stabilize and we prudently manage our capital position, it was effective balance sheet management, our financial discipline, and expanding interconnectedness across the franchise that enabled us to fully deliver the strong results we did this quarter and fully expect that momentum to continue into 2025. Finally, I'd like to extend our thoughts to those impacted by the devastating and ongoing wildfires in Los Angeles. We are closely monitoring the situation and have teams across the Bank involved in our collective response efforts to help best support our employees, customers, and their communities. Let me close by thanking our employees for their continued dedication to our clients, communities, and shareholders in what was a meaningful year for the company. We will now open up the call for Q&A.
```

*Rank 5 -- `BK_2023_Q1_prepared_remarks_500_002` -- transcript `BK_2023_Q1` -- NOT one of the question's own transcript_ids*

```
operational and sticky in nature and derived from a diverse set of business lines. And as I mentioned earlier, we manage over $1 trillion of cash on behalf of our clients across deposits, money market funds, repos and securities lending, which allows us to retain a connection to the money when it moves around various short-term investment alternatives. And we're also the largest provider of collateral services globally, our average tri-party balances increased to $5.6 trillion this quarter, which is another example of just how comprehensive our role is in the broader liquidity ecosystem. Now turning to our financial performance in the quarter. As you can see on Page 2 of our financial highlights presentation, we delivered solid results. We reported earnings per share of $1.12, up 30% year-over-year or up 20% excluding notable items, primarily in the first quarter of last year. Revenue was up 11% year-over-year. We closely managed expenses, up 3% year-over-year, and we generated a healthy return on tangible common equity of 20%. And given how in focused capital and liquidity are at the moment, I'll note that our Tier 1 leverage ratio as well as our liquidity coverage ratio remains strong and unchanged compared to the prior quarter, well above regulatory requirements and our own management buffers. Stepping back for a moment, I'm encouraged by the early progress that we are seeing around the Company to deliver on the commitment that we made to you back in January. First, we are bending the cost curve. Our first quarter expense growth came in marginally better than our initial internal plan and we remain firmly committed to cutting our core expense growth by roughly half this year compared to 2022 on a constant currency basis. Second, in line with our outlook for the year, we continued to derive healthy growth in net interest revenue. Third, we delivered positive operating leverage on a year-over-year basis. And fourth, we returned a meaningful amount of capital to our shareholders, including $1.3 billion of common share repurchases. We've made good initial progress on our plan to return more than 100% of earnings to shareholders in 2023, and we currently expect to continue buying back stock, albeit at a slower pace given the uncertain environment. At the same time, I've made a promise to you to call it as it is when we fall short of our expectations. And so to be candid
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 1 | `FITB_2023_Q1_prepared_remarks_500_000`, `BK_2023_Q4_prepared_remarks_500_001`, `STT_2024_Q1_prepared_remarks_500_001`, `USB_2024_Q4_prepared_remarks_500_003`, `BK_2023_Q1_prepared_remarks_500_002` | BK_2023_Q1, BK_2023_Q4, FITB_2023_Q1, STT_2024_Q1, USB_2024_Q4 | no |
| 180 | `BK_2023_Q4_prepared_remarks_500_001` | BK_2023_Q4 | no |
| 1 | `FITB_2023_Q1_prepared_remarks_500_000`, `BK_2023_Q4_prepared_remarks_500_001`, `STT_2024_Q1_prepared_remarks_500_001`, `USB_2024_Q4_prepared_remarks_500_003`, `BK_2023_Q1_prepared_remarks_500_002` | BK_2023_Q1, BK_2023_Q4, FITB_2023_Q1, STT_2024_Q1, USB_2024_Q4 | no |
| 1 | `FITB_2023_Q1_prepared_remarks_500_000`, `BK_2023_Q4_prepared_remarks_500_001`, `STT_2024_Q1_prepared_remarks_500_001`, `USB_2024_Q4_prepared_remarks_500_003`, `BK_2023_Q1_prepared_remarks_500_002` | BK_2023_Q1, BK_2023_Q4, FITB_2023_Q1, STT_2024_Q1, USB_2024_Q4 | no |
| 4 | `BK_2023_Q4_prepared_remarks_500_001`, `STT_2024_Q1_prepared_remarks_500_001`, `USB_2024_Q4_prepared_remarks_500_003` | BK_2023_Q4, STT_2024_Q1, USB_2024_Q4 | no |
| 190 | `USB_2024_Q4_prepared_remarks_500_003` | USB_2024_Q4 | no |
| 1 | `FITB_2023_Q1_prepared_remarks_500_000`, `BK_2023_Q4_prepared_remarks_500_001`, `STT_2024_Q1_prepared_remarks_500_001`, `USB_2024_Q4_prepared_remarks_500_003`, `BK_2023_Q1_prepared_remarks_500_002` | BK_2023_Q1, BK_2023_Q4, FITB_2023_Q1, STT_2024_Q1, USB_2024_Q4 | no |
| 2025 | `USB_2024_Q4_prepared_remarks_500_003` | USB_2024_Q4 | no |
| 200 | `USB_2024_Q4_prepared_remarks_500_003` | USB_2024_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 16: `ref_them_09` / `chunk200_dense`

- **question_id:** ref_them_09
- **condition:** chunk200_dense
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What net interest margin levels did banks report in 2023 and 2024, on reported and adjusted bases, and which way were they moving?

**Gold anchor(s):**
> interest margin of 2.84%, declined 8 basis points reflecting the increased funding costs, I
> quarter net interest margin was 6.69%, 21 basis points higher than last quarter and 11
> net interest margin improved 3 basis points compared

**Generated answer, verbatim:**

```
Based on the provided context, here are the net interest margin (NIM) levels and trends for the specified periods:

**Huntington Bancshares (HBAN)**
*   **Q3 2023:** The bank anticipated Q4 2023 NIM to be between **305 basis points and 310 basis points**, which was an increase of 5 to 10 basis points from previous guidance. This was driven by loan growth, funding mix performance, and a "higher for longer" interest rate scenario.
*   **Q2 2023 Outlook:** The bank anticipated NIM of approximately **3%** (plus or minus a few basis points) by Q4 2023.
*   **2024 Trend:** Modeling indicated that 2024 NIM would trend **flat to higher** from the Q4 2023 endpoint.
*   **Q3 2024:** Reported NIM was **2.98%**, representing a decrease of 1 basis point from Q2 2024. This decline was attributed to lower spread net of free funds and higher cash balances, partially offset by improved hedging program drag.

**U.S. Bancorp (USB)**
*   **Q4 2023:** The context does not provide a specific NIM percentage for Q4 2023 but notes that the margin reflected market dynamics including deposit pricing pressure and unfavorable shifts in deposit mix, partially offset by better earning asset spreads. It projects full-year 2024 net interest income to be consistent with or slightly up from the annualized Q4 2023 level of approximately $4.14 billion.
*   **Q1 2024 Outlook:** Net interest income on a fully-taxable equivalent basis was expected to be in the range of **$4.0 billion to $4.1 billion**.

**Bank of America (BAC)**
*   **Full Year 2023:** The context does not provide a specific NIM percentage but characterizes Net Interest Income (NII) as "strong but slowing" during the course of the year, with adjusted full-year revenue growth driven by a **9% NII improvement**.

**Summary of Direction:**
*   **HBAN:** NIM was expected to rise into late 2023 and trend flat to higher in early 2024, but actually decreased slightly (by 1 bps) in Q3 2024 compared to Q2 2024.
*   **USB:** Margins faced pressure from deposit pricing and mix shifts in late 2023, with income expected to remain stable or increase slightly in early 2024.
*   **BAC:** NII was strong but slowing throughout 2023.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `USB_2023_Q4_prepared_remarks_200_006` -- transcript `USB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
interest margin reflected market dynamics including deposit pricing pressure and unfavorable shifts in the deposit mix, partially offset by better earning asset spreads and improved total funding mix. In the first quarter of 2024, we expect net interest income on a fully-taxable equivalent basis to be in the range of $4.0 billion to $4.1 billion. For the full year 2024, we expect net interest income on a fully-taxable equivalent basis to be consistent with our annualized fourth quarter 2023 net interest income level of approximately $4.14 billion to up slightly. Slide 10 highlights trends in noninterest income. Noninterest income, as adjusted, increased 12.1% on a year-over-year basis, driven by new account growth and deepening relationships across the business. Year-over-year payment service revenue benefited by continued strength in consumer and business spending activities, while increases in trust and investment management fees and commercial product revenue were driven by underlying
```

*Rank 2 -- `HBAN_2023_Q3_prepared_remarks_200_010` -- transcript `HBAN_2023_Q3` -- NOT one of the question's own transcript_ids*

```
loan growth and funding mix continue to perform very well. These factors resulted in the margin coming in better than we had expected when we shared our outlook in July. We continue to analyze multiple potential interest rate scenarios. The basis of our planning and guidance continues to be a central set of those scenarios that is bounded on the low end by the forward yield curve and at the high end by a scenario that projects rates stay higher for longer. The higher for longer scenario today assumes one additional rate increase in 2023, flat Fed funds through October of 2024, and ends 2024 approximately 75 basis points higher than the forward curve. With the move and rates higher, we now anticipate net interest margin for the fourth quarter to be around 305 basis points to 310 basis points. This is 5 basis points to 10 basis points higher than the level we shared previously. Looking further out, our modeling continues to indicate 2024 NIM trending flat to higher from the Q4 2023 endpoint. Turning to
```

*Rank 3 -- `HBAN_2023_Q2_prepared_remarks_200_010` -- transcript `HBAN_2023_Q2` -- NOT one of the question's own transcript_ids*

```
3 and into 2024. The 2 primary scenarios we incorporate include: one which is represented by the forward yield curve and another which assumes rates stay higher for longer and end 2024, approximately 75 basis points higher than the forward. We think this is the most likely range for short-term rates over the next 6 quarters. Based on this range, we anticipate net interest margin of approximately 3% by Q4, plus or minus a few basis points. This would equate to core net interest income on a dollar basis for the fourth quarter to be down approximately 1% to 2% from Q2 levels. As we look out further into 2024, clearly, the trends will depend on both those interest rate scenarios and what is happening with the broader economy and industry factors, including loan demand and deposit growth. That said, our modeling indicates NIM outlooks are stable to rising during 2024 which, coupled with earning asset growth, is expected to drive net interest income dollar expansion as
```

*Rank 4 -- `BAC_2023_Q4_prepared_remarks_200_005` -- transcript `BAC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as
```

*Rank 5 -- `HBAN_2024_Q3_prepared_remarks_200_012` -- transcript `HBAN_2024_Q3` -- NOT one of the question's own transcript_ids*

```
. Net interest margin was 2.98% for the third quarter. Reconciling the change in NIM from Q2, we saw a decrease of 1 basis point. This was due to spread net of free funds lower by 2 basis points, higher cash balances driving margin lower by 2 basis points, partially offset by lower drag from the hedging program, which improved by 3 basis points. We continue to project full year net interest income to be within our prior guidance range. The fourth quarter level is expected to be flat to up 1% on a year-over-year basis and then resume growth over the first half of 2025 and accelerate in the second half. This is expected to result in record net interest income for 2025 based on current rate curve expectations. We continue to benefit from fixed rate loan repricing with loan yields expanding by 4 basis points from the prior quarter. This occurred even as SOFR moved lower during the quarter. As a reminder, we continue
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 3 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 305 | `HBAN_2023_Q3_prepared_remarks_200_010` | HBAN_2023_Q3 | no |
| 310 | `HBAN_2023_Q3_prepared_remarks_200_010` | HBAN_2023_Q3 | no |
| 5 | `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3 | no |
| 10 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010` | HBAN_2023_Q3, USB_2023_Q4 | no |
| 2 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 3 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 3 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 2.98 | `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2024_Q3 | no |
| 1 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 2 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `HBAN_2024_Q3_prepared_remarks_200_012` | HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4.14 | `USB_2023_Q4_prepared_remarks_200_006` | USB_2023_Q4 | no |
| 1 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 4.0 | `USB_2023_Q4_prepared_remarks_200_006` | USB_2023_Q4 | no |
| 4.1 | `USB_2023_Q4_prepared_remarks_200_006` | USB_2023_Q4 | no |
| 9 | `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2024_Q3 | no |
| 1 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 3 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |
| 2 | `USB_2023_Q4_prepared_remarks_200_006`, `HBAN_2023_Q3_prepared_remarks_200_010`, `HBAN_2023_Q2_prepared_remarks_200_010`, `BAC_2023_Q4_prepared_remarks_200_005`, `HBAN_2024_Q3_prepared_remarks_200_012` | BAC_2023_Q4, HBAN_2023_Q2, HBAN_2023_Q3, HBAN_2024_Q3, USB_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 17: `ref_them_11` / `chunk200_dense`

- **question_id:** ref_them_11
- **condition:** chunk200_dense
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did banks characterise their net charge-off levels and direction in 2023 and 2024?

**Gold anchor(s):**
> $127 million in the second quarter compared to $70 million in this year's
> expectation that net charge-offs in the second-half of 2024 will be lower than the first-half
> anticipate approaching 60 basis points here in the back half of the year is kind of how we're thinking

**Generated answer, verbatim:**

```
Based on the provided context, banks characterized their net charge-off levels and direction as follows:

*   **Capital One (COF):** In Q4 2023, net charge-offs were approximately 15% above 2018 levels. Looking ahead into 2024, the bank concluded that net charge-offs are stabilizing at about 15% above 2019 levels, with typical month-to-month volatility and seasonality.
*   **Fifth Third Bancorp (FITB):** For full year 2024, the net charge-off outlook remained in the range of 35 to 45 basis points. The bank expected to resume provision builds in connection with loan growth and mix in the second half of 2024, though this build was expected to be less than in the first half of the year.
*   **American Express (AXP):** While specific charge-off levels for 2023 were not detailed in the provided text, management indicated that credit performance is driven by product quality and disciplined risk execution. They noted they would provide more details on 2024 credit performance during their guidance call at the beginning of the next year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `COF_2023_Q4_qa_200_021` -- transcript `COF_2023_Q4` -- NOT one of the question's own transcript_ids*

```
, for comparing our charge-offs in this fourth quarter that just happened to a past stable year. In the fourth quarter, our net charge-offs were about 15% above 2018 levels. And of course, 2018 rolled into 2019, so that's an appropriate benchmark to look at as we head into 2024 and compared to 2019. Now when we look ahead, extrapolating from our current delinquency inventories and recent flow rates, we conclude that our net charge-offs are stabilizing at about 15% above 2019, with of course some typical month-to-month volatility and normal seasonality. Now, of course, the seeds of this stabilization have been planted for quite a long time now and partly driven by the choices that we made back in 2020 and 2021. Coming out the pandemic, we were concerned about two trends. FinTechs were flooding the market, especially the subprime market with credit offers, creating the potential for credit
```

*Rank 2 -- `FITB_2024_Q2_prepared_remarks_200_016` -- transcript `FITB_2024_Q2` -- NOT one of the question's own transcript_ids*

```
2024, reflecting the impact of weaker than previously expected credit demand and customer hedging activities. We expect strong growth in commercial payments and wealth and asset management revenue to continue. In response to this expectation of lower customer activity in the second half. We expect to manage full year adjusted non-interest expense stable to 2023 levels. Our expense outlook assumes continued investments in technology with tech expense growth in the mid-single digits and sales additions in middle market, commercial payments, and wealth. We will open 30 to 35 new branches in our higher growth markets and have already closed a similar number of branches in 2024. Our outlook still projects an efficiency ratio of around 57% for the full year. For full year 2024, the net charge-off outlook remains in the 35 to 45 basis points range. While we expect to resume provision builds in connection with loan growth and mix in the second half of 2024, we expect the second half build to be less than the first half of 2024
```

*Rank 3 -- `C_2023_Q4_prepared_remarks_200_010` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
investors through both of these channels. As I reflect on the year, I also want to note that we were a source of strength for the system and for clients during a volatile period for the banking sector and geopolitically and I'm very proud of how our people around the world performed during challenging times. 2024 looks to be similar to 2023 in terms of the macro environment with moderating rates and inflation. We expect to see growth slowing globally with the US well positioned to withstand a run-of-the-mill recession should one materialize. With a strong balance sheet, ample liquidity and diligent risk management we are well positioned to support our clients through whatever environment comes to path. Moreover, we think environments like these play to our strengths, given how far we are down the path of our simplification and divestitures. 2024 will be a turning point as we will be able to completely focus on the performance of our five businesses and our transformation. I
```

*Rank 4 -- `COF_2024_Q3_prepared_remarks_200_010` -- transcript `COF_2024_Q3` -- NOT one of the question's own transcript_ids*

```
2022, auto charge-offs have been strong and stable. Slide 13 shows third quarter results for our Commercial Banking business. Compared to the linked quarter, ending loan balances decreased about 2%. Average loans were down about 1%. The modest declines are largely the result of choices we made in 2023 to tighten credit. Ending deposits were up about 5% from the linked quarter. Average deposits were down about 1%. We continue to manage down selected less attractive commercial deposit balances. Third quarter revenue was up 1% from the linked quarter and non-interest expense was up by about 2%. The Commercial Banking annualized net charge-off rate for the third quarter increased 7 basis points from the sequential quarter to 0.22%. The Commercial Banking criticized performing loan rate was 7.66%, down 96 basis points compared to the linked quarter. The criticized non-performing loan rate increased 9 basis points to 1.55%. In closing, we continued to post strong results in
```

*Rank 5 -- `AXP_2023_Q3_qa_200_019` -- transcript `AXP_2023_Q3` -- NOT one of the question's own transcript_ids*

```
and below pre-pandemic levels. What are your thoughts on net charge-offs heading into 2024? And maybe you could touch a little bit on how the season-end curves are happening for your recent vintages.

Christophe Le Caillec: Yeah, yeah. So we're not going to give you a lot of details about 2024 on this call. We plan to do that at the beginning of next year when we speak about 2024 guidance. But what I can tell you is that the starting point for us of our credit performance and all our credit decisions is the quality of the products and the fact that it attracts premium Card Members. That's the starting point, right? We have a very talented risk organization. We have a very disciplined execution of our risk decision, but it starts with the quality of the product and that's the key differentiator vis-a-vis our peers and that's what we are focused on. And as you know
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 4 | `COF_2023_Q4_qa_200_021`, `FITB_2024_Q2_prepared_remarks_200_016`, `C_2023_Q4_prepared_remarks_200_010`, `AXP_2023_Q3_qa_200_019` | AXP_2023_Q3, COF_2023_Q4, C_2023_Q4, FITB_2024_Q2 | no |
| 15 | `COF_2023_Q4_qa_200_021` | COF_2023_Q4 | no |
| 2018 | `COF_2023_Q4_qa_200_021` | COF_2023_Q4 | no |
| 15 | `COF_2023_Q4_qa_200_021` | COF_2023_Q4 | no |
| 2019 | `COF_2023_Q4_qa_200_021` | COF_2023_Q4 | no |
| 35 | `FITB_2024_Q2_prepared_remarks_200_016` | FITB_2024_Q2 | no |
| 45 | `FITB_2024_Q2_prepared_remarks_200_016` | FITB_2024_Q2 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 18: `ref_them_15` / `chunk200_hybrid`

- **question_id:** ref_them_15
- **condition:** chunk200_hybrid
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How much did banks say they were spending on technology over 2023 and 2024, and how did that spend and related G&A expense change?

**Gold anchor(s):**
> themes, technology spend was $3 billion in the quarter, up 13%, primarily driven by change
> increased our technology initiatives and expect to spend nearly $4 billion on technology initiatives
> up 7% year-over-year, primarily due to the timing of technology spend in the prior year

**Generated answer, verbatim:**

```
Based on the provided context, here is the information regarding technology spending and General & Administrative (G&A) expenses for the specified periods:

**Bank of America (BAC)**
*   **Technology Spend:** The text notes increased investments in technology but does not provide a specific dollar amount for 2023 or 2024. It mentions that incentives were up 15% year-over-year in Q4 2024, partly related to market revenues, and that the firm added bankers/advisers and increased brand/technology investments in 2024.
*   **G&A/Expense Change:** Total expense was $16.8 billion in Q4 2024. Excluding the FDIC special assessment charge from Q4 2023, expenses increased year-over-year. This increase was driven by higher incentives (up 15% YoY), added personnel, and brand/technology investments, partially offset by a $300 million release of prior period accruals for the FDIC assessment.

**Citigroup (C)**
*   **Technology Spend:** Over the past three years (2021–2023), roughly 30% of transformation investments were in technology. The text does not provide a specific dollar figure for total technology spend in 2023 or 2024, but notes that expense growth relative to the prior year was driven by transformation and business-led investments, including technology.
*   **G&A/Expense Change:** Expense growth continued to be driven by transformation/business-led investments, volume-related expenses, and risk/controls/technology investments, partially offset by productivity savings and reductions in legacy franchises.

**Wells Fargo (WFC)**
*   **Technology Spend:** The company expects approximately $1.1 billion of incremental technology and equipment expense for 2024. This reflects higher costs related to the amortization of prior year investments and new planned investments.
*   **G&A/Expense Change:** Total non-insurance expense is expected to be approximately $52.6 billion in 2024. This outlook includes ongoing business-related operating losses of approximately $1.3 billion (similar to 2023) and merit increases of approximately $700 million.

**BlackRock (BLK)**
*   **Technology Spend:** While not a bank, the context notes that technology is expected to be one of the primary areas of investment within G&A. In Q1 2024, G&A expense increased 6% year-over-year due to the timing of technology investment spend in the prior year. Sequentially, G&A decreased 12% in Q1 2024 reflecting the timing of this spend and seasonally higher marketing expenses in Q4 2023.
*   **G&A/Expense Change:** For 2024 (excluding GIP transaction impacts), BlackRock expects a low to mid-single-digit percentage increase in core G&A expense, with most growth coming from continued technology investment. In Q1 2024, total expenses increased 8% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BLK_2024_Q1_prepared_remarks_200_007` -- transcript `BLK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
of aligning investment spend with our highest conviction growth areas, variabilizing more of our expense base and generating fixed cost scale. Total expense increased 8% year-over-year, reflecting higher compensation, G&A and sales asset and account expense. Employee compensation and benefit expense was up 11%, primarily reflecting higher incentive compensation as a result of higher operating income and performance fees. G&A expense increased 6% due to the timing of technology investment spend in the prior year. Sequentially, G&A expense decreased 12%, reflecting timing of technology investment spend and seasonally higher marketing and promotional expense in the fourth quarter. While one quarter's results can be impacted by timing of spend, we expect technology to be one of our primary areas of investment within G&A. Sales asset and account expense increased 5% compared to a year ago, primarily driven by higher direct fund expense. Direct fund expense was up 7% year-over-year, mainly due to higher average index
```

*Rank 2 -- `BLK_2023_Q4_prepared_remarks_200_012` -- transcript `BLK_2023_Q4` -- NOT one of the question's own transcript_ids*

```
and career growth. Looking forward, we're prioritizing investments to propel our differentiated organic growth and operating leverage. We'll aim to align investment spend with our highest conviction structural growth areas, find additional ways to variabilize expenses and generate fixed cost scale through technology, automation and optimization of our footprint through our innovation hubs. Excluding the impact of the GIP transaction at present, we'd expect our headcount to be broadly flat in 2024. Also excluding the impact of GIP and related transaction costs, we'd expect a low to mid-single-digit percentage increase in 2024 core G&A expense. Most core G&A growth should come from continued investment in technology as we look to operate more efficiently and better serve our clients. One of our biggest long-term advantages has been scale. Our ability to add significant assets managed with excellence without growing expenses linearly. Our platform strategy has delivered scale and operating leverage over time and we're
```

*Rank 3 -- `WFC_2023_Q4_prepared_remarks_200_025` -- transcript `WFC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
initiatives, we’re also continuing to invest and we expect approximately $1.1 billion of incremental technology and equipment expense, reflecting higher costs related to the amortization of investment in prior years, as well as new investments planned for 2024. We also expect merit increases of approximately $700 million, which are primarily awarded to employees with lower salaries. We highlight some of the other areas where we plan to invest on the next slide. Our 2024 expense outlook includes ongoing business related operating losses of approximately $1.3 billion, similar to the level we had in 2023. As previously disclosed, we have outstanding litigation, regulatory and customer remediation matters that could impact operating losses. So putting this all together, we expect 2024 non-insurance expense to be approximately $52.6 billion. It’s important to note that while we’ve made substantial progress executing on our efficiency initiatives, as Charlie highlighted, we still have a significant opportunity to get more efficient across the
```

*Rank 4 -- `C_2023_Q4_prepared_remarks_200_018` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
of restructuring costs associated with our organizational simplification and additional severance costs of approximately $730 million, which included actions to address stranded costs and start to right-size the businesses. Relative to the prior year, expense growth continued to be driven by transformation and business-led investments, volume-related expenses and other investments in risk and controls and technology, partially offset by productivity savings and a reduction in expenses and legacy franchises within all other. Over the past few years, we've been investing across these themes, which has not only impacted the performance of the firm, but also the businesses. On slide 10, we show the components of our transformation and technology spend from 2021 to 2023. Over the past three years, we have invested significantly in our infrastructure, platforms, applications, processes and data. As you can see in the bar chart at the top of the slide, roughly 30% of our transformation investments over the last three years were in technology, with the remainder related to non-tech
```

*Rank 5 -- `BAC_2024_Q4_prepared_remarks_200_018` -- transcript `BAC_2024_Q4` -- NOT one of the question's own transcript_ids*

```
the discussion. We reported $16.8 billion in expense this quarter. And the fourth quarter of '23 included the large FDIC special assessment charge and excluding that, expense increased. The increased expense from prior periods was driven by a number of factors and was partially offset by a roughly $300 million release of prior period accruals for the FDIC special assessment. Let's talk about the drivers of the expense. First, in regard to revenue, our markets-related businesses of investment banking, investment in Brokerage and Sales & Trading, those were up 20% year-over-year. Incentives for the firm were up 15% versus the fourth quarter of '23 and were in large part related to these market-related revenue streams. On investments that we made, we added bankers and advisers across most of our businesses in 2024, and we also increased investments in our brand with significant sponsorships like the Masters in FIFA to name a few. And we increased our investments around technology as
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 15 | `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4 | no |
| 4 | `BLK_2023_Q4_prepared_remarks_200_012`, `WFC_2023_Q4_prepared_remarks_200_025`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2023_Q4, WFC_2023_Q4 | no |
| 16.8 | `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4 | no |
| 4 | `BLK_2023_Q4_prepared_remarks_200_012`, `WFC_2023_Q4_prepared_remarks_200_025`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2023_Q4, WFC_2023_Q4 | no |
| 4 | `BLK_2023_Q4_prepared_remarks_200_012`, `WFC_2023_Q4_prepared_remarks_200_025`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2023_Q4, WFC_2023_Q4 | no |
| 15 | `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4 | no |
| 300 | `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4 | no |
| 2021 | `C_2023_Q4_prepared_remarks_200_018` | C_2023_Q4 | no |
| 30 | `C_2023_Q4_prepared_remarks_200_018`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, C_2023_Q4 | no |
| 1.1 | `WFC_2023_Q4_prepared_remarks_200_025` | WFC_2023_Q4 | no |
| 52.6 | `WFC_2023_Q4_prepared_remarks_200_025` | WFC_2023_Q4 | no |
| 1.3 | `WFC_2023_Q4_prepared_remarks_200_025` | WFC_2023_Q4 | no |
| 700 | `WFC_2023_Q4_prepared_remarks_200_025` | WFC_2023_Q4 | no |
| 1 | `BLK_2024_Q1_prepared_remarks_200_007`, `WFC_2023_Q4_prepared_remarks_200_025`, `C_2023_Q4_prepared_remarks_200_018`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2024_Q1, C_2023_Q4, WFC_2023_Q4 | no |
| 6 | `BLK_2024_Q1_prepared_remarks_200_007`, `WFC_2023_Q4_prepared_remarks_200_025`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2024_Q1, WFC_2023_Q4 | no |
| 12 | `BLK_2024_Q1_prepared_remarks_200_007` | BLK_2024_Q1 | no |
| 1 | `BLK_2024_Q1_prepared_remarks_200_007`, `WFC_2023_Q4_prepared_remarks_200_025`, `C_2023_Q4_prepared_remarks_200_018`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2024_Q1, C_2023_Q4, WFC_2023_Q4 | no |
| 4 | `BLK_2023_Q4_prepared_remarks_200_012`, `WFC_2023_Q4_prepared_remarks_200_025`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2023_Q4, WFC_2023_Q4 | no |
| 1 | `BLK_2024_Q1_prepared_remarks_200_007`, `WFC_2023_Q4_prepared_remarks_200_025`, `C_2023_Q4_prepared_remarks_200_018`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2024_Q1, C_2023_Q4, WFC_2023_Q4 | no |
| 8 | `BLK_2024_Q1_prepared_remarks_200_007`, `BAC_2024_Q4_prepared_remarks_200_018` | BAC_2024_Q4, BLK_2024_Q1 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 19: `ref_them_10` / `chunk200_hybrid`

- **question_id:** ref_them_10
- **condition:** chunk200_hybrid
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What did banks say about credit card growth and card credit performance over 2023 and 2024?

**Gold anchor(s):**
> card net charge-off rate rose 12 basis points to 2.72% in Q3, and it remains
> think it's -- you saw the card growth rate was about 1% or so versus
> product offerings continue to drive strong credit card spend, up approximately $5 billion or 14%

**Generated answer, verbatim:**

```
Based on the provided context, American Express reported that loan and card member receivable growth moderated from 13% year-over-year in Q4 2023 to 11% in Q2 2024. While this growth is expected to continue moderating through 2024, it remains elevated compared to pre-pandemic levels and is growing modestly faster than billings. American Express attributed its strong, best-in-class credit performance to a high-quality customer base, robust risk management, and disciplined growth strategies, noting that write-off and delinquency rates ticked up in Q4 2023 but are expected to remain generally stable for the remainder of 2024.

Bank of America stated that there continues to be nice growth in the credit card space, particularly among prime and super-prime customers. They noted that while they make marginal adjustments to underwriting due to economic uncertainties and consumer pressure, they expect the overall credit performance of their credit card business to remain very strong through the cycle.

Huntington Bancshares indicated that it outperformed on loans throughout 2023 while effectively managing deposit beta. The bank stated that credit trends are normalizing as expected and that they continue to believe they will outperform the industry on credit through the cycle, consistent with their moderate to low risk appetite.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `AXP_2023_Q4_prepared_remarks_200_012` -- transcript `AXP_2023_Q4` -- NOT one of the question's own transcript_ids*

```
, we are pleased with the continued strong engagement and loyalty of our card members across the globe. As we think about 2024, we are assuming a spend environment similar to what we've seen in the past few quarters. Now moving on to loans and card member receivables on slide seven. We saw a year-over-year growth of 13%. We expect this growth, which has been elevated versus pre-pandemic levels to continue to moderate as we progress through the 2024, but to still grow modestly faster than billings. Turning next to credit and provision on slide eight through 10. First and most importantly, we continue to see strong and best-in-class credit metrics. We attribute this performance to the high credit quality of our customer base, our robust risk management practices, and our disciplined growth strategy. As we had expected, our write-off and delinquency rates did continue to tick up this quarter, as you see on slide right.
```

*Rank 2 -- `AXP_2024_Q2_prepared_remarks_200_010` -- transcript `AXP_2024_Q2` -- NOT one of the question's own transcript_ids*

```
volumes are tracking in-line with our expectations and support our revenue expectations for the year. Moving on to loans and card member receivables, on Slide 7, we saw year-over-year growth of 11%, demonstrating strong growth, but continuing to moderate as expected. As we progress through 2024, we expect loan growth in particular to continue to moderate by a few percentage points, but it still grew in double-digits as we exit the year. Turning next to credit and provision on Slide 8, through 10, our credit performance remains very strong and is a direct result of our disciplined growth strategy which has been focused on growing our high credit quality premium customer base, including through the younger customers we attract to the franchise. This strategy, coupled with our robust risk management practices are an important aspect of our business models. Going forward, we expect our write-off rates to remain generally stable for the remainder of 2024. Turning now to the accounting of this credit performance on Slide 9
```

*Rank 3 -- `AXP_2023_Q1_prepared_remarks_200_011` -- transcript `AXP_2023_Q1` -- NOT one of the question's own transcript_ids*

```
with this growth and with the overall lending economics we are generating. That said, looking forward, you may see the growth rate of our loan balances moderate a bit as we progress through 2023, but we would expect it to remain elevated versus pre-pandemic levels. If you then turn to credit and provision on Slides 9 through 11, the high credit quality of our customer base continues to show through in our best-in-class credit performance. Our card member loans and receivables write-off and delinquency rates remain below pre-pandemic levels, though they did continue to move up this quarter as we expected, which you can see on Slide 9. We view these consolidated write-off and delinquency rates as more comparable to pre-pandemic rates than the individual loans and receivable rates because, as we talked about last quarter, our charge products in many instances now have embedded lending functionality. Going forward, we continue to expect
```

*Rank 4 -- `HBAN_2023_Q4_prepared_remarks_200_002` -- transcript `HBAN_2023_Q4` -- NOT one of the question's own transcript_ids*

```
Second, we outperformed on both deposits and loans throughout the year. Our colleagues are acquiring new customers and deepening our existing customer relationships. Importantly, we delivered this growth, while effectively managing our deposit beta. Third, we expect to modestly expand net interest income as we manage the challenges of the interest rate cycle and are driving increased fee revenues. Fourth, we are rigorously managing credit across our portfolios, consistent with our aggregate moderate to low risk appetite. Credit trends are normalizing as expected, and we continue to believe we will outperform the industry on credit through the cycle. Finally, we remain intently focused on our core strategies. Huntington remained resilient through the events of 2023, emerging as one of the strongest regional banks. We maintained our disciplined execution and we expect to grow earnings over the course of 2024 and continuing into 2025 and beyond. I will move us on to Slide 5 to recap our performance in 2023. Huntington delivered solid results over the
```

*Rank 5 -- `USB_2023_Q4_qa_200_026` -- transcript `USB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
up credit card and say we should slow growth at this point in the cycle, or do you think there's still quite a bit of runway of, call it, good growth or healthy growth?

Terry Dolan: Yeah. Well, I mean, it is an area, Matt, that we think that there continues to be a nice growth in that particular space. It is an area, though, that certainly as we have looked at the economic uncertainties and all sorts of things, the pressure on consumers, especially given the inflationary sort of pressure. We -- on the margin around the edges, we do make adjustments to underwriting and tighten that up where we need to. But when you end up kind of thinking about the overall credit performance of credit card business, we still think it's a very nice business. We focus on prime, super prime sort of customers. And even through this cycle, I think it's going to perform very well.

Matt O'Connor:
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 13 | `AXP_2023_Q4_prepared_remarks_200_012` | AXP_2023_Q4 | no |
| 4 | `AXP_2023_Q4_prepared_remarks_200_012`, `AXP_2024_Q2_prepared_remarks_200_010`, `HBAN_2023_Q4_prepared_remarks_200_002` | AXP_2023_Q4, AXP_2024_Q2, HBAN_2023_Q4 | no |
| 11 | `AXP_2024_Q2_prepared_remarks_200_010`, `AXP_2023_Q1_prepared_remarks_200_011` | AXP_2023_Q1, AXP_2024_Q2 | no |
| 2 | `AXP_2023_Q4_prepared_remarks_200_012`, `AXP_2024_Q2_prepared_remarks_200_010`, `AXP_2023_Q1_prepared_remarks_200_011`, `HBAN_2023_Q4_prepared_remarks_200_002` | AXP_2023_Q1, AXP_2023_Q4, AXP_2024_Q2, HBAN_2023_Q4 | no |
| 4 | `AXP_2023_Q4_prepared_remarks_200_012`, `AXP_2024_Q2_prepared_remarks_200_010`, `HBAN_2023_Q4_prepared_remarks_200_002` | AXP_2023_Q4, AXP_2024_Q2, HBAN_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 20: `ref_them_13` / `chunk500_dense`

- **question_id:** ref_them_13
- **condition:** chunk500_dense
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did BNY Mellon describe growth in its ETF servicing business through 2023 and 2024?

**Gold anchor(s):**
> ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced
> strong momentum in ETF servicing with AUC/A of over $2 trillion, up more than 50%
> $2.7 trillion was up more than 70% year-on-year, and the number of funds serviced

**Generated answer, verbatim:**

```
Based on the provided context, BNY Mellon described growth in its ETF servicing business as follows:

*   **2024:** The company reported that ETF Assets Under Custody and Administration (AUCA) reached $2.8 trillion, representing an increase of over 60% year-over-year. Inflows into ETFs on the platform outpaced the market again during this period.
*   **2023:** The provided text does not contain specific quantitative data or descriptions regarding ETF servicing growth for 2023. It only mentions that in 2024, the company continued to see "particular strength in ETF and alternative servicing," which validated multi-year investments made into these platforms.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BK_2023_Q3_prepared_remarks_500_004` -- transcript `BK_2023_Q3` -- ONE OF the question's own transcript_ids*

```
year. We also signed the first external client, a leading GSIB-owned European Asset Manager, for our recently launched buy-side trading solutions. Without a doubt, we expect our more prominent solutions, like Wove and buy-side trading, to move the needle on growth over time. But we are leaning into innovation to solve evolving client challenges across all of our businesses. For example, in Treasury Services, we were one of the first banks to go live on FedNow, the Federal Reserve's new instant payment rail. This allows us to expand our capabilities for corporations, non-bank financial institutions, and fintechs, and as a service provider, we are helping our financial institutions clients access instant payments, remain competitive, and provide best-in-class service for their customers. As another example, this quarter the business announced the launch of [Bankify] (ph), an open banking payment solution that as an alternative to credit or debit cards and third-party payment platforms helps organizations receive consumer payments from bank accounts with a seamless user experience and guaranteed settlement. Let me conclude by saying that we are optimistic about the opportunity in front of us and our strategic objectives for the short, medium, and long term are clear. We are innovating and pushing forward on our multi-year growth investments, all the while remaining disciplined to deliver positive operating leverage and pre-tax margin expansion. As I've said all along, the path to transforming BNY Mellon into a consistently high-performing company will take some time, but for 2023, we are on track to deliver what we said we deliver at the beginning of the year, while making steady progress toward our strategic priorities. I'm proud and appreciative of our people's dedication to be more for our clients, run our company better, and power our culture, collectively to unlock BNY Mellon's potential. With that, over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning, everyone. I will start on Page 3 of the presentation with our consolidated financial results for the third quarter. Total revenue of $4.4 billion was up 2% year-over-year. Net interest revenue was up 10% year-over-year, primarily driven by higher interest rates, partially offset by changes in balance sheet size and mix. Fee revenue was flat. Growth on the back of higher market values, net new business, and
```

*Rank 2 -- `BK_2023_Q4_prepared_remarks_500_003` -- transcript `BK_2023_Q4` -- NOT one of the question's own transcript_ids*

```
fund over $0.5 billion of incremental investments, and we laid the foundation needed to transition to a platform's operating model, including successful pilots in two areas of the organization, which were important proof points as we start to unlock the power of our platforms in several phases over the next couple of years. While we focus on being more for our clients and running our company better, we know none of it can happen without our people, which is why we are powering our culture to make BNY Mellon a place where people are proud to work and excited to grow their careers. We elevated recruitment and retention programs, including welcoming the largest class of campus analysts in BNY Mellon's history, a class double the size of the previous year and we're going to double it again this year. We launched our BK shares program to grant shares to the 45,000 employees who didn't previously receive stock as part of their compensation to cascade a sense of ownership and accountability across our company. And we rolled out enhanced employee benefits recognizing value in fostering both a human and high-performing work environment. I'll wrap up where I began. We remain confident in the strength of our culture, our strategy and our ability to execute to help us unlock value for our clients, our shareholders, and our people. 2023 was an important year in which we assembled more of the team that can deliver on what is needed and we got ourselves pointed in the right direction for what we need to achieve, but it was also a year where being humble and resilient mattered. While we have a lot of work ahead of us, what started as a theory and a belief now has early proof points, and we can see the possibility of what we can achieve. We have an ambitious agenda as we move forward, but I continue to be optimistic about the opportunity ahead. With that, I'll turn it over to Dermot.

Dermot McDonogh: Thank you, Robin, and good afternoon, everyone. I'm picking up on Page 6 of the presentation with our consolidated financials for the fourth quarter, and as Robin noted, I'm also going to speak to our 2024 outlook and medium-term targets, including how we are going to execute on our goals. For the fourth quarter, our reported results reflect several notable items. Approximately $750 million of non-interest expense is related to the FDIC special assessment severance and litigation reserves. And we
```

*Rank 3 -- `BK_2023_Q4_prepared_remarks_500_008` -- transcript `BK_2023_Q4` -- NOT one of the question's own transcript_ids*

```
of teams that transcend our lines of business and segments. Robin mentioned several updates when he talks about our progress in 2023, so I'll highlight just a few with them. The first is our enhanced commercial model. We're driving a new culture of commerciality to deliver all of BNY Mellon in a unified front to facilitate deeper client relationships with solutions from across the firm. With our clients at the center, our module is led by client coverage teams with clear accountability to retain business, expand revenue into new areas and drive client satisfaction. Our new sales operations and enablement organization, the client coverage practice, will make it easier for our clients to do more business with BNY Mellon and create consistent commercial roles, tools and support internally for an enhanced and more efficient sales experience. And what we call integrated solutions represents a new more focused approach to assembling components from multiple client platforms into a piece will go-to-market capabilities that span across our lines of business, driving better value for our clients and higher profitable growth. The second one I'd like to highlight is our transition to a platform's operating model. By grouping similar activities together into logical platforms and uniting related capabilities, we are enabling the streamlining of internal processes to drive higher efficiency and further enhance resiliency and risk management. Our model is based on two types of platforms. Client platforms will own the delivery of a commercial solution to our external clients, while enterprise platforms will own the delivery of internal services. Over the past few months, we've developed a detailed implementation approach and our transition into this new model will be gradual and deliberate, starting with the first implementation wave this spring. And the third is our culture. People come to BNY Mellon to make an impact on global financial markets. While we focus on driving growth and running our company better, none of it can happen without our people. That's why we're making meaningful investments, including in enhanced learning, development and feedback to foster exciting careers. Moving to our segments, starting with Securities Services on Page 16. Here, we are reiterating our existing 30% pre-tax margin target. Over the past 24 months, we've improved the margin from 21% in 2021 to 25% in 2023. We are pleased with the performance of the business over the past two years, but we appreciate that the path from 25% to 30% will be the harder yards. First of all, we are firmly focused on driving
```

*Rank 4 -- `BK_2024_Q4_prepared_remarks_500_008` -- transcript `BK_2024_Q4` -- NOT one of the question's own transcript_ids*

```
are increasingly looking to leverage the scale of BNY's platforms and utilize the differentiated breadth of our capabilities and at the same time, we continue to see particular strength in ETF and alternative servicing, validating the multiyear investments we've made into these platforms. ETF AUCA of $2.8 trillion were up over 60% year-over-year with inflows into ETFs on our platform once again outpacing the market and alternatives AUCA were up 20% year-over-year. In issuer services, investment services fees were up 4%. Healthy net-new business and higher client activity in corporate trust was partially offset by lower depository receipt fees, reflecting a higher level of corporate actions and cross-border activity in the prior year quarter. Over the course of 2024, we've maintained our market-leading share in straight stat servicing and by increasing our market share in CLO servicing, further strengthened our number 2 position. In this segment, foreign exchange revenue was up 25% year-over-year, reflecting growth from higher client activity. Net interest income for the segment was up 7% year-over-year. Segment expenses of $1.7 billion were up 1% year-over-year, reflecting higher litigation reserves, employee marriage increases and higher investments, partially offset by efficiency savings. Pre-tax income was $643 million, a 39% increase year-over-year, and pre-tax margin was 28%. Next, Market and Wealth Services on Page 15. Market and Wealth Services reported total revenue of $1.7 billion, up 11% year-over-year. Total investment services fees were up 12% year-over-year. In Pershing, investment services fees were up 9%, reflecting higher market values and client activity. Net-new assets were $41 billion, including a large client onboarding in the quarter. In Clearance and Collateral Management, investment services fees increased by 13%, primarily reflecting higher collateral management fees and clearance volumes. We continue to see strong US securities clearance volumes on the back of US treasury issues as well as trading activity across the platform. And we remain focused on increasing market connectivity by expanding our global collateral platform to new markets. In Treasury Services, investment services fees were up 15%, primarily reflecting net-new business. In November, the US Department of the Treasury's Bureau of the Fiscal Service selected BNY as the new financial agent for the Direct
```

*Rank 5 -- `BK_2024_Q4_prepared_remarks_500_003` -- transcript `BK_2024_Q4` -- NOT one of the question's own transcript_ids*

```
operating leverage resulted in pre-tax margin expansion and improved profitability and we delivered attractive capital returns to our shareholders, all of which underscored the execution of a reinvigorated BNY. But now, let's look forward on Page 5. We are entering 2025 with strong momentum and determination to deliver further value for our clients and shareholders. BNY plays a central role in global capital markets with $52 trillion of AUCA, $14 trillion of debt serviced, $3 trillion of wealth assets, and $5.6 trillion of assets on our collateral management platform. We manage $2 trillion of AUM and on an average day, we settle over $15 trillion worth of securities and roughly $2.5 trillion worth of payments for clients around the world. This exceptional client franchise and leadership across our diversified financial services platforms positions us well to capture market beta and capitalize on evolving market trends, several of which we describe on the left hand side of the page. Some of our fastest-growing businesses in 2024, treasury services, clearance and collateral management and corporate trust demonstrate our gearing toward economic growth and higher capital markets activity, both public and private. And through Pershing and Wealth, we are a leader in serving one of the fastest-growing segments in financial services, the US wealth market. Within that market, our wealth business is focused on the faster-growing ultra-high net worth space. Our Pershing business, on the other hand, leverages the size and scale of our platforms to power advisors' businesses, helping them navigate an increasingly complex operating environment using the power of our technology. Relevant for both retail and institutional investors, the trend toward private markets represents an opportunity for BNY to support our clients end-to-end from servicing to distribution, cash investment, FX hedging and lending across traditional and alternative asset classes. Last year also saw the mass adoption of digital assets exchange-traded products in the US, which grew to more than $100 billion in assets under management. BNY has been an early mover in the digital asset space. Today, we provide fund services for the vast majority of digital asset exchange-traded products in both the US and Canada and over the long term, we believe digital assets and the technology underpinnings have the transformative potential to help solve client and market needs. And finally, on this list of important market trends, as global markets evolve and become ever more complex, both buy-side and
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 2.8 | `BK_2024_Q4_prepared_remarks_500_008` | BK_2024_Q4 | no |
| 60 | `BK_2024_Q4_prepared_remarks_500_008` | BK_2024_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 21: `ref_them_06` / `chunk500_dense`

- **question_id:** ref_them_06
- **condition:** chunk500_dense
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What efficiency ratio levels and targets did banks discuss across 2023 and 2024?

**Gold anchor(s):**
> an adjusted efficiency ratio of 59% and a seasonally challenged quarter, which is a six
> annual operating efficiency ratio, net of adjustments to be modestly down compared to the 43.5%

**Generated answer, verbatim:**

```
Based on the provided context, the following efficiency ratios and targets were discussed:

*   **Citigroup (COF):** Reported an annual operating efficiency ratio of **43.54%** for full-year 2023 (net of adjustments). This represented a **99 basis point improvement** over the prior year. For 2024, Citigroup expects its annual operating efficiency ratio to be **flat to modestly down** compared to 2023.
*   **PNC Financial Services (PNC):** While specific percentage ratios were not cited, PNC stated that its Cost Improvement Program (CIP) has historically allowed the bank to deliver **low single-digit annual expense growth**. For 2024, PNC set an objective to keep **core expenses stable** (excluding one-time charges related to workforce reductions).
*   **Wells Fargo (WFC):** Did not provide a specific efficiency ratio percentage but noted that it successfully delivered approximately **$10 billion in gross expense saves** through efficiency initiatives over the past three years. For 2024, Wells Fargo expects approximately **$2.7 billion in gross expense reductions** due to these initiatives.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `WFC_2023_Q4_prepared_remarks_500_009` -- transcript `WFC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
in consumer banking and lending deposits, as well as continued mix shift from lower yielding products to higher yielding, deposits in our other deposit gathering businesses are expected to be relatively stable and market funding will replace the decline in consumer deposits as needed. We currently expect that net interest income will trough towards the end of this year. As we’ve done in prior years, we are also assuming the asset cap will remain in place throughout the year. Ultimately, the amount of net interest income we earn in 2024 will depend on a variety of factors, which many of which are uncertain, including the absolute level of rates, the shape of the yield curve, deposit balances, mix and pricing and loan demand. Turning to our 2024 expense expectations on Slide 19. We started our focus on efficiency initiatives three years ago and we’ve successfully delivered on our commitment of approximately $10 billion of gross expense saves. Through our efficiency initiatives we have reduced headcount every quarter since third quarter of 2020 and headcount is down 16% since the end of 2020. Looking at our expectations for this year and following the waterfall on the slide from left to right. We reported $55.6 billion of non-interest expense in 2023, which included the $1.9 billion FDIC special assessment. Excluding this item, expenses would have been $53.6 billion, which we believe is a good starting point for discussion of 2024 expenses. Looking at the next bar, we expect severance expense to be approximately $1.3 billion lower, driven by the $969 million expense we took in the fourth quarter for planned actions, we expect expenses to increase by at least $300 million due to higher revenue related expense, driven by wealth and investment management, revenue related expenses will ultimately be a function of activity and market levels, and therefore could be higher or lower than this estimate. At this point, we expect all other expenses to be flat, though there are significant efficiencies and increased investments included in this expectation. We expect approximately $2.7 billion of gross expense reductions in 2024 due to the efficiency initiatives. We highlight in the slide some of the areas where we anticipate additional savings and continue to believe we have more opportunities beyond 2024. Similar to prior years, the resources needed to address our risk and control work are separate from our efficiency initiatives and we will continue to make significant investments in our risk and control infrastructure. While we remain focused on executing on our efficiency
```

*Rank 2 -- `COF_2023_Q4_prepared_remarks_500_005` -- transcript `COF_2023_Q4` -- NOT one of the question's own transcript_ids*

```
. On a monthly basis auto delinquency rate and charge-off rate had been tracking normal seasonal patterns since the first half of 2023 and continued to do so through December. Slide 13 shows fourth-quarter results for our Commercial Banking business. Compared to the linked-quarter, ending loan balances decreased about 1%. Average loans were also down about 1%. The modest declines are largely the result of choices we made earlier in the year to tighten credit. Ending deposits were down about 9% from the linked quarter. Average deposits were down about 7%. The declines are largely driven by our continuing choices to manage down selected less attractive commercial deposit balances. Reducing these less attractive deposits also drove the 14 basis point linked-quarter improvement in our average rate paid on commercial deposits. Fourth-quarter revenue was down 5% from the linked quarter. Non-interest expense was also down about 5%. The Commercial Banking annualized charge-off rate for the fourth quarter increased 28 basis points from the third quarter to 0.53%. The Commercial Banking criticized performing loan rate was 8.81%, up 73 basis points compared to the linked quarter. The criticized non-performing loan rate was down 6 basis points to 0.84%. Commercial Banking credit trends were largely driven by continuing pressure in our commercial office portfolio. Slide 17 of the fourth-quarter 2023 results presentation shows additional information about the remaining commercial office portfolio, which is less than 1% of our total loans. In closing, we continued to deliver solid results in the fourth quarter. We posted another strong quarter of top line growth in domestic card revenue, purchase volume, and loans. Domestic card and auto delinquency trends were in line with normal seasonal patterns, a continuing indicator of stabilizing consumer credit results. We grew consumer deposits and total deposits. And we added liquidity and maintained capital to further strengthen our already strong and resilient balance sheet. Our annual operating efficiency ratio, net of adjustments for the full year 2023, was 43.54%. In 2023, we saw incremental opportunities and made choices to grow revenue and tightly manage costs to achieve a 99 basis point improvement in our annual operating efficiency ratio. The actual improvement was better than the “modest improvement” growth we had been expecting. Over the last decade, we've driven significant operating efficiency improvement even as we've invested to transform our technology. And we continue to drive for efficiency improvement over time. For the full
```

*Rank 3 -- `PNC_2023_Q3_prepared_remarks_500_006` -- transcript `PNC_2023_Q3` -- NOT one of the question's own transcript_ids*

```
do expect a 2024 annual CIP goal of similar magnitude to the 2023 program. Our CIP efforts over the years have allowed us to substantially invest in our company while still delivering low single digit annual expense growth. However, the current environment poses meaningful pressures necessitating expense control measures beyond our annual CIP program. As a result, we took a hard look at our organizational structure and identified opportunities to operate more efficiently through staff reductions, which we began implementing earlier this month. This initiative will decrease the workforce by 4% and is expected to reduce 2024 expenses by approximately $325 million. One-time costs associated with this plan are expected to be approximately $150 million and will be incurred during the fourth quarter of 2023. We believe these actions will position PNC for stronger efficiency going forward. As a result, even though our budgeting cycle isn't complete, we have an objective to keep core expenses stable in 2024, which by definition would exclude the fourth quarter one-time charges. In summary, PNC reported a solid third quarter 2023. In regard to our view of the overall economy, we're expecting a mild recession starting in the first half of 2024, with a contraction in real GDP of less than 1%. We expect the federal funds rate to remain unchanged in the near term between 5.25% and 5.5% through mid-2024 when we expect the Fed to begin cutting rates. Looking ahead, our outlook for the fourth quarter of 2023 compared to the third quarter of 2023 is as follows. We expect average loans to be up approximately 3%, including the acquisition of the Signature Bank capital commitment facilities. Net interest income to be down 1% to 2%. Fee income to be up approximately 1% as increased capital markets activity is expected to more than offset the impact of the elevated MSR hedge gains during the third quarter. Other noninterest income to be in the range of $150 million and $200 million, excluding net securities and Visa activity. We expect total core non-interest expense to be up 3% to 4%, which excludes charges related to the workforce reduction. Additionally, this guidance does not contemplate the pending FDIC special assessment, which could occur during the fourth quarter. And we expect fourth quarter net charge-offs to be between $200 million and $250 million. And with that, Bill and I are ready to take your questions.
```

*Rank 4 -- `COF_2023_Q4_prepared_remarks_500_006` -- transcript `COF_2023_Q4` -- NOT one of the question's own transcript_ids*

```
-year 2024, we expect annual operating efficiency ratio, net of adjustments, will be flat to modestly down compared to 2023. Our expectation includes the partial year impact of the proposed CFPB late fee rule, assuming that rule takes effect in October 2024. Pulling way up, our modern technology capabilities are generating an expanding set of opportunities across our businesses. We continue to drive improvements in underwriting, modeling, and marketing, as we increasingly leverage machine learning at scale. And our tech engine drives growth, efficiency improvement, and enduring value creation over the long term. We remain well-positioned to deliver compelling long-term shareholder value and to thrive in a broad range of possible economic scenarios. And now we'll be happy to answer your questions. Jeff?

Jeff Norris: Thank you, Rich. We’ll now start the Q&A session. As a courtesy to other investors and analysts who may wish to ask a question, please limit yourself to one question plus a single follow-up. So if you have any questions after the Q&A session, the Investor Relations team will be available after the call. Amy, please start the Q&A.
```

*Rank 5 -- `C_2023_Q4_prepared_remarks_500_004` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
investors through both of these channels. As I reflect on the year, I also want to note that we were a source of strength for the system and for clients during a volatile period for the banking sector and geopolitically and I'm very proud of how our people around the world performed during challenging times. 2024 looks to be similar to 2023 in terms of the macro environment with moderating rates and inflation. We expect to see growth slowing globally with the US well positioned to withstand a run-of-the-mill recession should one materialize. With a strong balance sheet, ample liquidity and diligent risk management we are well positioned to support our clients through whatever environment comes to path. Moreover, we think environments like these play to our strengths, given how far we are down the path of our simplification and divestitures. 2024 will be a turning point as we will be able to completely focus on the performance of our five businesses and our transformation. I recognize the importance of this year and I am highly confident that we will see the benefits of the actions we've taken through the momentum of our businesses. Backed by investments in key products we believe we can continue to grow revenues ex-divestitures by 4% to 5% over the medium term. Overall, we remain confident in our ability to adapt to the evolving capital and macro environment to reach our medium-term return targets and return capital to our shareholders whilst continuing the investments needed in our information. With that, I'd like to turn it over to Mark, and then we will be delighted, as always, to take your questions.

Mark Mason: Thanks, Jane, and good morning, everyone. We have a lot to cover on today's call. I'm going to start with the fourth quarter and full year firm-wide financial results, focusing on year-over-year comparisons, unless I indicate otherwise. I'll also focus on our guidance for 2024 and end with the path to our medium-term return target. The presentation of our results reflects the changes we've made in conjunction with our organizational simplification, including reporting legacy franchises and corporate other in all other. However, before I go into the results, let me walk you through some of the notable items that impacted the quarter that were included in the 8-K we recently filed. At the top right of slide seven, we show these items on a pre-tax basis. The F
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 43.54 | `COF_2023_Q4_prepared_remarks_500_005` | COF_2023_Q4 | no |
| 99 | `COF_2023_Q4_prepared_remarks_500_005` | COF_2023_Q4 | no |
| 10 | `WFC_2023_Q4_prepared_remarks_500_009` | WFC_2023_Q4 | no |
| 2.7 | `WFC_2023_Q4_prepared_remarks_500_009` | WFC_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 22: `ref_them_12` / `chunk500_hybrid`

- **question_id:** ref_them_12
- **condition:** chunk500_hybrid
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What did firms say during 2023 about their wealth management businesses and the investment behind them?

**Gold anchor(s):**
> wealth management business, revenue decreased by 5%, driven by lower net interest revenue and changes
> keep investing through the cycle on the funnel and wealth,

**Generated answer, verbatim:**

```
Based on the provided context, here is what the firms said regarding their wealth management businesses and investments in 2023:

*   **BNY Mellon:** The firm stated that it launched new solutions to deepen relationships with existing clients and attract new ones, including Pershing’s wealth advisory platform (Wove) and buy-side trading solutions. BNY Mellon also noted that all its businesses were bringing new client solutions to market, such as Bankify and real-time payments on FedNow. Additionally, the company hired its first Chief Commercial Officer in 2023 to operationalize its "one BNY Mellon" initiative and created an integrated team to facilitate multi-line of business solutions at scale.
*   **Morgan Stanley:** Management highlighted that the Wealth business is a key differentiator for the firm, noting that it has been built into something "truly special" through the integration of Smith Barney. The company emphasized having a "full funnel" approach that combines self-directed, traditional advisory, and workplace channels working as one. While specific 2023 investment figures were not detailed in this excerpt, the leadership discussed the strategic importance of integrating these channels to deliver differentiated value to clients.
*   **State Street:** The firm noted that its asset manager segment faced pricing headwinds of about 2% per year, partly due to a shift from mutual funds to ETFs. However, it observed that well-managed firms were responding by launching new product types (such as ETF lines and collective trust offerings) and focusing on their cost base and technology stacks. State Street stated it was supporting these clients in participating in the wealth business and leveraging its position as the largest middle office provider.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BK_2023_Q4_prepared_remarks_500_002` -- transcript `BK_2023_Q4` -- NOT one of the question's own transcript_ids*

```
, power our culture. They are deliberately simple and our people are rallying around them. As I've said before, strategy is important, but ultimately just a set of words. Actually doing it and how we do it matters a lot. I'm encouraged by the progress we made in 2023, some of which we highlight on Slide 5. Our global clients across government's pension funds, mutual funds, unions, endowments, corporations, financial services firms, and individuals, both trust and want to do more business with us. And our analysis clearly shows that is more for them to do with us as we continue to partner alongside them to help achieve their ambitions. As the global financial system grows and becomes ever more complex, demand for a trusted resilient partner with the scale to service clients across the entire financial life-cycle, such as BNY Mellon, grows as well. In 2023, we launched several new solutions that allow us to deepen our relationships with existing clients and to open the door to new ones. Of course, that includes the launch of Wove, Pershing's wealth advisory platform, as well as the rollout of our buy-side trading solutions offering, but it goes far beyond these more visible product launches. All of our businesses are bringing new client solutions to the market, Bankify, real-time payments on FedNow, white labeling Liquidity Direct, bond-wise intraday repo settlement, BNY Mellon Advisors are all examples. And in 2023, we filed more patent applications than ever before. At the same time, we have an opportunity to bring more of BNY Mellon to clients who currently use us for just a single service. Last year, we hired our first Chief Commercial Officer as we began to operationalize our one BNY Mellon initiative across the organization. As part of enhancing the organizational setup and focus of our client coverage organization, we created an integrated team to facilitate multi-line of business solutions at scale, and we also formed a coverage practice group to implement consistency and approach and tooling. Next, while 2023 was a foundational year and what will be a multi-year journey to transform to a more streamlined and effective operating model, we took important steps toward running our company better to improve efficiency, reduce bureaucracy, and be more intentional with how we spend so our investments in the business go further. We generated nearly double the amount of efficiency savings versus the prior year, which allowed us to self-
```

*Rank 2 -- `STT_2024_Q2_qa_500_012` -- transcript `STT_2024_Q2` -- NOT one of the question's own transcript_ids*

```
quarter and this year, and for the rest of the year, we expect pricing headwinds to be in line with the previous years and guidance. We've said pricing headwinds of about 2% per year. We're not seeing any more or any less of that. It tends to be a little more geared towards the asset manager segment, because those are the -- that is the group of clients that has mutual funds and some mutual fund versus ETF shifting. But it's not -- we're not seeing anything out of the ordinary or anything that is unexpected at this point.

Mike Mayo: And then one last one to follow-up on that. I mean, I guess maybe as goes your clients, as goes any company or as goes [indiscernible] and with the record high stock markets and historically such a strong position with the mutual fund, which you just mentioned, are you seeing that uptick? Or is it still a slog for your big long only asset managers that are your legacy strength?

Ron O'Hanley: Mike, it's Ron. Let me take that. I mean, I think that the -- as you would know as well as anybody, the business continues to change. And we've seen the continued move from the mutual fund to the ETF to the FMA. But you're also seeing these firms, particularly the well managed ones respond, and they're responding in a couple of ways. I mean, one new product types are -- I mean, even the most traditional mutual fund companies now have pretty interesting ETF lines. Most of -- they're involved in the DC 401(k) business, they've got a mutual fund offering, but they've got a collective trust offering too. So they're responding to that market pressure. Most of them are figuring out ways to participate in the wealth business, and we continue to respond and support them in that. So the nature of the business is changing. In some cases, some things were more lucrative than others. And so what you're also finding in those businesses, they're very focused on their cost base. Their technology stack, their operating stack, and again, that presses in our favor as we think about the Alpha front to back solution, we are the largest middle office provider by far in the industry and we've gotten quite good at that. So the -- we
```

*Rank 3 -- `MS_2023_Q4_qa_500_014` -- transcript `MS_2023_Q4` -- NOT one of the question's own transcript_ids*

```
ll take our last question from Mike Mayo with Wells Fargo Securities. Please go ahead. Your line is now open.

Mike Mayo: Okay. Well, it looks like you have a heavy lift after following James [indiscernible]. What is your message to the wealth managers and investment managers at half of the company that you haven't run in the past. So you've proven yourself in half the company, that's clearly capital markets and Wall Street banking. But what's your message to the other half of the company at a time when they've had a step down in their -- the growth rates, new asset flows on wealth and outflows in investment management.

Ted Pick: Well, thanks for the question, Mike. The Wealth business is actually in my blood. My dad and my father-in-law were both brokers once upon a time, and I grew up studying that business as a kid. And I think it is absolutely that, which is differentiated on Morgan Stanley during this 15-year period. The ability to integrate Smith Barney and build out something that's truly special is -- has been existentially, as you know better than most, but also thematically exactly what the firm as needed. In no way has it actually worked to the disbenefit of the investment bank. As you know, the history of our -- of our merger '97 was largely about social issues, but the industrial idea wasn't necessarily off at all. to build a world-class wealth manager would be something that would have enormous barriers to entry and have run well and run their first-class way to deliver value to clients in a differentiated manner. And what we have done, thanks to the leadership of Andy Saperstein with Jed Fin and then the investment management business with Dan Simkowitz now moving over to the Investment Bank and [Ben Huneke] and [Jacques Chappuis] running investor management today is we've got effectively the full funnel. We've got the soup to nuts self-directed the traditional advisory channel and this new channel workplace are working as one. I've spent time working some of the chairman’s and hitting a branch here in Midtown and spending some time with folks that are actually making the engine work. And I think it's fair to say that We, at one point, we're calling the wealth and investment management business, the ballast, which was
```

*Rank 4 -- `GS_2024_Q4_prepared_remarks_500_003` -- transcript `GS_2024_Q4` -- NOT one of the question's own transcript_ids*

```
both public and private markets. We are taking the current capabilities of our financing group, adding coverage of financial sponsors and alternative asset management firms to better innovate and accelerate the delivery of services to clients. We are also creating an alternative origination group focused on sourcing to provide seamless coverage to our private credit and private equity clients. We are excited about providing our clients with access to differentiated sourcing and investment capabilities, which will in turn help us accelerate growth across the franchise. Now let me turn to Asset & Wealth Management on Page 6. Our assets under supervision reached another record, reflecting our 28th consecutive quarter of long-term fee based net inflows. In Wealth Management, our total client assets rose to $1.6 trillion. We also bolstered our more durable revenue streams. Management and other fees and private banking and lending revenues together have grown at a CAGR of 12% since 2019, and we continue to expect to drive high-single digit annual growth in the coming years. Turning to Page 7. We meaningfully improved our AWM pretax margin in 2024, achieving our medium-term target. In our journey to further improve the return profile of the firm, we are committed to driving this business towards mid-teens returns. We see significant growth opportunities across wealth management, alternatives and solutions. In Wealth Management, we are growing this business by increasing the number of advisers in the field and surrounding them with content specialists. We are expanding our loan product offerings, and we're elevating our overall client experience with further investment in our digital capabilities. In alternatives, we are scaling our flagship fund program and developing new strategies. We remain focused on penetrating the institutional client base and expanding our wealth channel. Additionally, we are investing in tailored solutions for institutional and third-party wealth clients, who continue to see customization across SMAs, direct indexing and ETFs in a structured form. On Page 8, we demonstrate the durability of the revenues across the firm. This is not the first time we've laid out this information, but it serves as a good reminder. Baseline revenues are shown in gray, which represent the sum of the trailing 10-year lows for each of the businesses that are considered to be more cyclical advisory, underwriting and intermediation. As I said last year, we believe this is a very conservative measurement because it's unlikely that every one of these businesses would ever hit a low point all
```

*Rank 5 -- `JPM_2023_Q4_prepared_remarks_500_005` -- transcript `JPM_2023_Q4` -- NOT one of the question's own transcript_ids*

```
the page, we've highlighted some firmwide drivers. Thematically, the biggest driver is what I might call business growth writ large. Within that, narrowly defined volume and revenue-related growth represents about $1 billion of the increase across the company as a result of an improved NIR outlook, compared to about $400 million in 2023. But in addition, the ongoing growth of the company, which continues to produce share gains and additional profitability, is coming with increased expense across a range of categories. The quantum of investment increase is comparable to last year's increase and is driven by all the same themes, bankers, branches, advisors, technology as well as marketing. Net-net, First Republic produces a modest increase in expenses, but with a significantly lower 2024 exit run rate as the result of business integration efforts. Finally, despite significantly lower inflation outlook in the economy as a whole, we still see some residual effects of inflation flowing through most of our expense categories. It's worth noting that both the general business growth and investment growth include decisions that have been executed both in response to market conditions during 2023 and to support the future growth and profitability of the company. We've included the fourth quarter 2023 exit rate on the page to illustrate that a significant portion of the year-on-year increase in expense is already in the run rate. Now, let's turn to Page 12 and cover credit and wrap up. On credit, we continue to expect the 2024 card net charge-off rate to be below 3.5%, consistent with Investor Day guidance. So in closing, we shouldn't leave 2023 without noting what an outstanding year it was, producing record revenue and net income despite some notable significant items. We're very proud of what we accomplished this year and want to thank everyone who made it possible. At the same time, we emphasized throughout 2023 the extent to which we were over-earning, as indicated by an ROTCE that is 4% above our through-the-cycle target. As we turn to 2024, it shouldn't be surprising that our outlook has us beginning to march down the path towards normalization of our returns. But despite the expected dissipation of the 2023 tailwinds and the presence of significant economic and geopolitical uncertainties, we remain optimistic about this franchise's ability to produce superior returns through a broad range of environments. And this management team remains laser
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 2 | `BK_2023_Q4_prepared_remarks_500_002`, `STT_2024_Q2_qa_500_012`, `GS_2024_Q4_prepared_remarks_500_003`, `JPM_2023_Q4_prepared_remarks_500_005` | BK_2023_Q4, GS_2024_Q4, JPM_2023_Q4, STT_2024_Q2 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 23: `ref_them_14` / `chunk500_hybrid`

- **question_id:** ref_them_14
- **condition:** chunk500_hybrid
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What did banks report about investment banking revenue and fees across 2023 and 2024?

**Gold anchor(s):**
> fourth quarter, investment banking fees of $1.7 billion fell 12% year-over-year, driven by a decline
> muted IPO market, investment banking fees are up 44%, that's driven by investment-grade debt issuance
> grew investment banking fees 18% year-over-year sales and trading revenue increased 12% year-over-year and aggregate,

**Generated answer, verbatim:**

```
Based on the provided context, only JPMorgan Chase reported specific details regarding investment banking revenue and fees for 2024. The other transcripts (State Street, Bank of America, and Huntington Bancshares) do not contain information specifically about "investment banking" revenue or fees; State Street discusses general fee revenue and trading businesses, while Bank of America mentions sales and trading results but does not break out investment banking fees.

According to the JPMorgan Chase 2024 Q4 prepared remarks:
*   **Investment Banking Fees:** Investment banking (IB) fees were up 49% year-on-year in 2024.
    *   Advisory fees increased by 41%.
    *   Underwriting fees rose significantly, with debt underwriting up 56% and equity underwriting up 54%.
*   **Revenue:** The context does not provide a specific total revenue figure for the Investment Banking division alone, but it notes that CIB (Corporate & Investment Banking) reported net income of $6.6 billion on revenue of $17.6 billion in Q4 2024.

The provided context does not contain information about investment banking revenue or fees specifically for State Street, Bank of America, or Huntington Bancshares for either 2023 or 2024.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `STT_2023_Q4_prepared_remarks_500_001` -- transcript `STT_2023_Q4` -- NOT one of the question's own transcript_ids*

```
we carefully navigated State Street through various headwinds, while continuing to execute against our strategic agenda. We focused and delivered on that agenda in three key areas; achieve strong sales wins across our businesses, drive strategic change in our investment services business and remain disciplined on productivity and broader cost management. Further on that last point, during 2023, we implemented key productivity actions and announced additional efficiency measures that will enable us to enhance the productivity of our operating model in 2024 and the years ahead. We took these many actions all while investing in our business and returning substantial capital to our shareholders, which helped to drive full year earnings growth excluding notable items. The world's investors, State Street and our industry, faced a host of significant market events and macroeconomic forces in 2023. In the first quarter, turmoil in the banking sector ultimately led to the resolution from several banks, which was a catalyst for some of the largest fixed income market moves seen in decades. In the second quarter, anticipation grew about the potential economic benefit from artificial intelligence, helping to drive equity markets higher. However, as we progress into the third quarter and as the Federal Reserve raised interest rates to the highest level in 2022 years in July, the prospect of higher for longer rates led to a substantial sell off in bond markets with the US 10-year treasury yield exceeding 5% in October, for the first time since the global financial crisis. Rate uncertainty and an increasing number of geopolitical concerns caused equities to struggle. Then during the fourth quarter, the equity market rallied vigorously as inflation receded and investors grew increasingly optimistic about a soft landing with positive sentiment gaining further momentum in the last month as the Federal Reserve signaled a pivot to lower interest rates this year. In sum, while our full year overall financial results benefited from higher interest rates globally last year and despite the strong market appreciation in the fourth quarter, daily average global equity markets only increased by low single digits in 2023, providing just a modest tailwind to our fee revenue, while client activity was muted as investors stayed on the sidelines for much of the year. And even in such an eventful year, equity and FX market volatility continued to contract creating revenue headwinds for our trading businesses. Slide 3 of our investor presentation provides some of our highlights for the year. Beginning with our financial performance, full year earnings per share was 5.58 or 7.66 excluding notable items. Year-over-year, excluding notable items
```

*Rank 2 -- `STT_2023_Q4_prepared_remarks_500_011` -- transcript `STT_2023_Q4` -- NOT one of the question's own transcript_ids*

```
-over-year basis with servicing fees expected to be up 1%, management fees up 7% to 8% and front office software and data expected to be up over 20%, largely due to increased SaaS new business and conversions and on-premise renewals. We expect full year 2024 NII to be down about 10% on a year-over-year basis compared to a record 2023. This is dependent on the outcome of global rate cuts and deposit mix and levels, which are obviously difficult to predict. Regarding the first quarter of 2024, after a significant step up in 4Q '23, we expect 1Q '24 NII to be flat to down 3% on a sequential quarter basis given current deposit mix expectations. Turning to expenses. As you can see on the walk on Page 16, we expect full year expenses ex-notables will be up about 2.5% on a nominal basis in 2023, driven largely by our continued investment in the business, which we expect to largely offset through greater productivity savings worth $0.5 billion, which is approximately 1.7 times last year's gross savings level. Regarding the first quarter of 2024, we expect expenses ex-notable items to be up 1% to 1.5% on a year-over-year basis, keeping in mind that seasonal expenses usually occur in the first quarter. As a reminder, we expect to achieve positive fee operating leverage, excluding notable items for full year 2024, given the projected growth in fee revenue and well controlled expenses. Finally, we expect taxes should be in the 21% to 22% range for 2024. And with that, let me hand the call back to Ron.

Ron O'Hanley: Thank you, Eric. Operator, we can now open the call for questions.
```

*Rank 3 -- `JPM_2024_Q4_prepared_remarks_500_002` -- transcript `JPM_2024_Q4` -- NOT one of the question's own transcript_ids*

```
. CIB reported net income of $6.6 billion on revenue of $17.6 billion. IV fees were up 49% year-on-year and we ranked number one with wallet share of 9.3% for 2024. Advisory fees were up 41%, benefiting from large deals and share growth in a number of key sectors. Underwriting fees were up meaningfully with debt up 56% and equity up 54%, primarily driven by favorable market conditions. In terms of the outlook for the overall investment banking wallet, in light of the positive momentum, we remain optimistic about our pipeline. Payments revenue was $4.7 billion, up 3% year-on-year, excluding equity investments, driven by higher deposit balances and fee growth, largely offset by deposit margin compression. Lending revenue was $1.9 billion, up 9% year-on-year, predominantly driven by lower losses on hedges. Moving to markets, total revenue was $7 billion, up 21% year-on-year. Fixed income was up 20% with better performance in credit as well as continued outperformance in currencies and emerging markets. Equities was up 22% on elevated client activity and derivatives amid increased volatility and higher trading volumes and cash. Security Services revenue was $1.3 billion, up 10% year-on-year, driven by fee growth on higher client activity and market levels as well as higher deposit balances. Expenses of $8.7 billion were up 7% year-on-year, predominantly driven by higher brokerage, technology, and legal expense. Average banking and payments loans were down 2% year-on-year and down 1% sequentially. Global Corporate & Investment Banking loans were down 2% quarter-on-quarter, driven by paydowns in lower short-term financing, primarily offset by new originations. In commercial banking, middle market loans were also down 2%, driven by paydowns, predominantly offset by new originations, and commercial real estate loans were flat as new originations were offset by paydowns. Average client deposits were up 9% year-on-year and 5% sequentially, driven by underlying client growth. Finally, credit costs were $61 million, driven by net downgrade activity and the net impact of charge-offs, offset -- largely offset by a reserve release due to an update to certain loss assumptions. Then to complete our lines of business
```

*Rank 4 -- `BAC_2023_Q4_prepared_remarks_500_002` -- transcript `BAC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 5 -- `HBAN_2023_Q3_qa_500_008` -- transcript `HBAN_2023_Q3` -- NOT one of the question's own transcript_ids*

```
to expand on that. If I think about the equation that we were managing in 2023, we've been seeing around a 2%, 2.5% underlying expense growth. And that's with the benefit of significant efficiencies that we're generating this year. I estimate that’s around 1% benefit in expenses in 2023 for these cumulative initiatives we are running for the last six, 18 months and self-funding underlying investments. We've talked about this model before, driving efficiencies is the core, keeping the underlying core at a low level with the funnel and outsized level of investment and expense growth into key investment earnings like tech, marketing, new additions of personnel to support new strategies, those underlying investments are up almost 20% in 2023, which is what we will hold the competitive capabilities that we’ve got. As we go into -- that model is what drove the overall roughly 2.5% growth that we saw in 2023. I think what we're seeing as we go into 2024 is roughly similar sort of underlying expense management program, really modeling down somewhat the underlying adjustments in light of the environment, clearly, but also bearing some modest incremental impacts of just the cumulative inflationary environment and the efficiencies will rise as well. And so, the net kind of underlying run rate that I would have expected into next year is around 2.5%. And then on top of that, we are accelerating, again, these investments in regulatory response, risk management capabilities that represents the additional 1.5% expense growth as we go into next year. That's the 4% trajectory. If I think about where we're investing just to touch on this briefly, continued focus on core strategy investments, delivering the TCF revenue synergies, growing our commercial bank through vertical specialized – specialties, expertise, digital and product development in our Consumer Banking and Business Banking division, continue to drive the fee revenue strategies and capital markets, payments and wealth. And then on top of that, clearly dealing with these additional areas around Basel III, CCAR, liquidity, interest rate risk management, resolution planning and data and alteration.

Steve Steinour: Scott, this is Steve. Just to add on. You'll also see several new initiatives that are also included in that number of 4% and we'll be announcing Q4 and Q1.

Scott Siefers: Okay. Perfect
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 4 | `STT_2023_Q4_prepared_remarks_500_001`, `STT_2023_Q4_prepared_remarks_500_011`, `JPM_2024_Q4_prepared_remarks_500_002`, `BAC_2023_Q4_prepared_remarks_500_002`, `HBAN_2023_Q3_qa_500_008` | BAC_2023_Q4, HBAN_2023_Q3, JPM_2024_Q4, STT_2023_Q4 | no |
| 49 | `JPM_2024_Q4_prepared_remarks_500_002` | JPM_2024_Q4 | no |
| 41 | `JPM_2024_Q4_prepared_remarks_500_002` | JPM_2024_Q4 | no |
| 56 | `JPM_2024_Q4_prepared_remarks_500_002` | JPM_2024_Q4 | no |
| 54 | `JPM_2024_Q4_prepared_remarks_500_002` | JPM_2024_Q4 | no |
| 6.6 | `JPM_2024_Q4_prepared_remarks_500_002` | JPM_2024_Q4 | no |
| 17.6 | `JPM_2024_Q4_prepared_remarks_500_002` | JPM_2024_Q4 | no |
| 4 | `STT_2023_Q4_prepared_remarks_500_001`, `STT_2023_Q4_prepared_remarks_500_011`, `JPM_2024_Q4_prepared_remarks_500_002`, `BAC_2023_Q4_prepared_remarks_500_002`, `HBAN_2023_Q3_qa_500_008` | BAC_2023_Q4, HBAN_2023_Q3, JPM_2024_Q4, STT_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 24: `ref_them_01` / `chunk200_bm25`

- **question_id:** ref_them_01
- **condition:** chunk200_bm25
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> How did banks report the impact of the FDIC special assessment on their expenses in late 2023 and the first half of 2024?

**Gold anchor(s):**
> a $289 million accrual for our current estimate of the FDIC
> Q1, which included $700 million for the FDIC
> up 20% year-over-year on a reported basis, primarily reflecting the FDIC

**Generated answer, verbatim:**

```
Based on the provided context, banks reported the impact of the FDIC special assessment as a significant driver of expense increases or noted its absence when comparing periods:

*   **M&T Bank (MTB):** In Q1 2024, expenses included $29 million related to the FDIC special assessment. This was compared to only $5 million in Q2 2024. When calculating the adjusted efficiency ratio for Q2, MTB excluded this impact.
*   **JPMorgan Chase (JPM):** In Q4 2024, expenses were down year-on-year predominantly because of the absence of the $2.9 billion FDIC Special Assessment that had been incurred in the prior year (late 2023).
*   **Citigroup (Citi):** In Q4 2024, expenses were down 18% largely due to the absence of the FDIC special assessment from the prior year. Excluding this impact and divestiture-related impacts, expenses were still down 7%. For full-year 2023, Citi reported that expenses excluding the FDIC special assessment and divestiture-related impacts were $54.3 billion.
*   **Wells Fargo (WFC):** In Q1 2024, non-interest expense increased 5% year-over-year, driven in part by the FDIC special assessment. Excluding this specific expense, WFC stated its full-year 2024 non-interest expense guidance remained unchanged at approximately $52.6 billion.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `MTB_2024_Q2_prepared_remarks_200_011` -- transcript `MTB_2024_Q2` -- NOT one of the question's own transcript_ids*

```
million to $764 million, reflecting seasonally elevated expenses in the first quarter, offset by the full quarter impact of annual merit increases. The second quarter included $5 million related to the FDIC special assessment compared to $29 million in the prior quarter. Other cost of operations decreased $18 million to $116 million from lower supplemental executive retirement costs and lower losses on lease terminations. The adjusted efficiency ratio, excluding the impact of the FDIC special assessment, was 55.1% compared to 59.6% in the first quarter. Next, let's turn to Slide 16 for credit. Net charge-offs for the quarter totaled $137 million or 41 basis points, down from 42 basis points in the linked quarter. The three largest charge-offs were $40 million combined and represent C&I loans that span industries including services, manufacturing and retail. The CRE charge-offs, including charge offs within the office portfolio, remain at manageable levels through the first half of the
```

*Rank 2 -- `JPM_2024_Q4_prepared_remarks_200_009` -- transcript `JPM_2024_Q4` -- NOT one of the question's own transcript_ids*

```
-on-year, driven by the impact of lower rates, largely offset by balance sheet actions, primarily securities reinvestment activity. NII was a net loss of $30 million compared to the net loss of $668 million in the prior year, driven by lower net investment securities losses this quarter. And expenses of $550 million were down $3 billion year-on-year, predominantly driven by the absence of the FDIC Special Assessment of $2.9 billion in the prior year. With that, let's pivot to the outlook, starting with NII on Page 9. We expect 2025 NII ex-markets to be approximately $90 billion. Going through the drivers, as usual, the outlook assumes that rates follow the forward curve. It's worth noting that the NII decrease is driven by both the cut expected in 2025 and the impact of the 100 basis points of cuts in the back half of 2024. You can see on the page that
```

*Rank 3 -- `C_2024_Q4_prepared_remarks_200_010` -- transcript `C_2024_Q4` -- NOT one of the question's own transcript_ids*

```
and RoTCE of 6.1% or $19.6 billion of revenues generating positive operating leverage for the firm and in each of our businesses. Total revenues were up 12% driven by growth in each of our businesses and a smaller impact of Argentina currency devaluation. Net interest income excluding markets was roughly flat with growth in USPB and wealth offset by declines in corporate other and banking. Non-interest revenues excluding markets was up 40% driven by continued strong fee momentum across services, banking and wealth along with lower partner payments in USPB as well as a smaller impact of Argentina currency devaluation. And total markets revenues were up 36%. Expenses were $13.2 billion, down 18%, largely driven by the absence of the FDIC special assessment and restructuring charge in the prior year. Excluding the impact of the FDIC special assessment and divestiture related impacts, expenses were down 7% driven by the absence of the restructuring charge in the prior year and savings associated
```

*Rank 4 -- `C_2023_Q4_prepared_remarks_200_017` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
of our investments in digital acquisition and customer engagement. Total revenues, excluding divestitures, came in at $77.1 billion, below our guidance of $78 billion to $79 billion for the year, largely due to the impact of the Argentina devaluation, softer markets performance, particularly in December and losses on loan hedges. However, NIIX ex-markets came in at $47.6 billion in line with our guidance. Despite the challenging environment and the impact of the Argentina devaluation, we grew firm-wide revenues by approximately 4% ex-divestitures in line with our Investor Day target, demonstrating the benefit of our diversified business model and the investments we've been making. On slide nine, we show full year expense trends from 2021 to 2023, excluding the FDIC special assessment and divestiture-related impacts, full year expenses were $54.3 billion for 2023 in line with our guidance. As I mentioned, this includes roughly $780 million
```

*Rank 5 -- `WFC_2024_Q1_prepared_remarks_200_012` -- transcript `WFC_2024_Q1` -- NOT one of the question's own transcript_ids*

```
Slide 7, first quarter non-interest expense increased 5% from a year ago, driven by higher operating losses, the FDIC special assessment, an increase in revenue related compensation, predominantly due to higher investment advisory fees in our wealth and investment management business and higher technology and equipment expense. These increases were partially offset by the impact of efficiency initiatives, including lower professional and outside services expense, which declined 10% from a year ago. The higher operating losses were driven by customer remediation accruals for a small number of historical matters that we are working hard to get behind us. The increase in personnel expense from the fourth quarter was driven by approximately $650 million of seasonally higher expenses in the first quarter, including payroll taxes, restricted stock expense for retirement eligible employees and 401(k) matching contributions. Not including expense for the FDIC special assessment in the first quarter, our full year 2024 non-interest expense guidance is unchanged and is still expected to be approximately $52.6 billion
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 1 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 29 | `MTB_2024_Q2_prepared_remarks_200_011` | MTB_2024_Q2 | no |
| 5 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 2 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 2 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 4 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 2.9 | `JPM_2024_Q4_prepared_remarks_200_009` | JPM_2024_Q4 | no |
| 4 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 18 | `MTB_2024_Q2_prepared_remarks_200_011`, `C_2024_Q4_prepared_remarks_200_010` | C_2024_Q4, MTB_2024_Q2 | no |
| 7 | `MTB_2024_Q2_prepared_remarks_200_011`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 54.3 | `C_2023_Q4_prepared_remarks_200_017` | C_2023_Q4 | no |
| 1 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2024_Q4_prepared_remarks_200_010`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, C_2024_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 5 | `MTB_2024_Q2_prepared_remarks_200_011`, `JPM_2024_Q4_prepared_remarks_200_009`, `C_2023_Q4_prepared_remarks_200_017`, `WFC_2024_Q1_prepared_remarks_200_012` | C_2023_Q4, JPM_2024_Q4, MTB_2024_Q2, WFC_2024_Q1 | no |
| 52.6 | `WFC_2024_Q1_prepared_remarks_200_012` | WFC_2024_Q1 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 25: `ref_them_03` / `chunk200_bm25`

- **question_id:** ref_them_03
- **condition:** chunk200_bm25
- **category:** thematic
- **case:** B
- **current outcome label:** answered_grounded_offtarget

**Question:**
> What did banks say about their office and commercial real estate credit exposure and the allowance against it during 2023?

**Gold anchor(s):**
> decreased by $37 million, primarily driven by the charge-offs of office real-estate loans
> CRE comprises less than 2% of total loans, and the majority are suburban

**Generated answer, verbatim:**

```
During 2023, Wells Fargo reported that its allowance for credit losses increased primarily due to commercial real estate office loans. In Q3, the allowance rose by $333 million driven by these office loans and higher credit card balances, while in Q4, it increased slightly due to credit card and commercial real estate loans. The bank noted that nonaccrual loans in commercial real estate grew significantly, with a $1.3 billion increase in office nonaccrual loans in Q3 and a further $567 million increase in Q4.

Regarding credit exposure and losses, Wells Fargo stated that as expected, losses began to materialize in the commercial real estate office portfolio due to weak market fundamentals, borrower performance issues, and lower appraisals resulting from properties or loans being sold at a loss. These losses were spread across various markets and loans. The bank emphasized that it had substantially built reserves for this portfolio throughout 2023 as criticized and nonperforming assets increased. Additionally, the company noted that while additional losses were expected in coming quarters due to market fundamentals and liquidity challenges, these amounts would likely be uneven and episodic. The commercial real estate team continued to derisk and reduce exposure through a rigorous monitoring process.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `WFC_2023_Q3_prepared_remarks_200_014` -- transcript `WFC_2023_Q3` -- NOT one of the question's own transcript_ids*

```
The decline in commercial industrial nonaccrual loans was primarily due to payoffs and paydowns, which is a good reminder that the resolution of nonperforming assets doesn't always result in charge-offs. The increase in commercial real estate nonaccrual loans was driven by a $1.3 billion increase in the office nonaccrual loan.  Moving to Slide 6. Our allowance for credit losses increased $333 million in the third quarter primarily for commercial real estate office loans as well as for higher credit card loan balances, which was partially offset by a lower allowance for auto loans. Since the composition of our office portfolio is relatively consistent with what we shared with you in the past few quarters, we did not include a separate commercial real estate slide this quarter. However, we did update the table showing the allowance for credit losses coverage ratio for commercial real estate, including the breakdown of the office portfolio.  We've not seen significant increases in charge-offs in our commercial
```

*Rank 2 -- `WFC_2024_Q1_prepared_remarks_200_015` -- transcript `WFC_2024_Q1` -- NOT one of the question's own transcript_ids*

```
, partially offset by higher allowance for credit card loans. The table on the page shows the allowance for credit losses coverage ratio for commercial real estate, including the breakdown of the office portfolio. We didn't increase our allowance for this portfolio in the first quarter and the coverage ratio in our CIB commercial real estate office portfolio of 11% was stable compared with the fourth quarter. Turning to capital and liquidity on Slide 10. Our capital position remains strong and our CET-1 ratio of 11.2% continue to be well above our 8.9% regulatory minimum plus buffers. We repurchased $6.1 billion of common stock in the first quarter. While the amount of stock we repurchased each quarter will vary, we continue to expect to repurchase more common stock this year than we did in 2023. Turning to our operating segment, starting with Consumer Banking and Lending on Slide 11. Consumer, small and business banking revenue declined 4% from a year
```

*Rank 3 -- `WFC_2023_Q4_prepared_remarks_200_011` -- transcript `WFC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
the third quarter to 53 basis points of average loans, driven by commercial real estate office and credit card loans. The increase in commercial net loan charge-offs reflected the higher losses in commercial real estate office, while losses in the rest of our commercial portfolio were stable from the third quarter. As expected, losses started to materialize in our commercial real estate office portfolio as market fundamentals remained weak. The losses were across a number of loans spread across various markets and were driven by borrower performance, lower appraisals were the result of properties or loans being sold at a loss. We substantially built reserves for this portfolio throughout 2023 as criticized and nonperforming assets increased. And while we expect additional losses in the coming quarters given the market fundamentals, and capital markets and liquidity challenges in this sector, the amounts will likely going to be uneven and episodic. Our commercial real estate team has a rigorous monitoring process and continues to derisk and reduce exposure, and we're
```

*Rank 4 -- `BK_2024_Q1_qa_200_055` -- transcript `BK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
Correct, yeah.

Ken Usdin: All right, great, thanks a lot.

Operator: And our final question comes from the line of Mike Mayo with Wells Fargo Securities. Please go ahead.

Mike Mayo: Hi. When you mentioned your comments about commercial real estate, I was just wondering, I don't think you have much exposure, but you highlighted that commercial real estate, I guess, to the industry or are you talking office? You said it's really a 2025 refinancing story and ASCO the 10-year, ASCO commercial real estate. It's just – if you could provide any color. Why did you highlight that and why do you have that sort of conclusion?

Robin Vince: Well, the question, Mike, was more general in nature. It wasn't really applying to us. Dermot talked a little bit about us in particular on commercial real estate, but I think the question that was being asked was just using our vantage point,
```

*Rank 5 -- `WFC_2023_Q4_prepared_remarks_200_012` -- transcript `WFC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
using this information to evaluate our allowance, which I will discuss later. Consumer net loan charge-offs continued to increase and were up $118 million from the third quarter to 79 basis points of average loans. The increase was driven by the credit card portfolio, which performed as expected with increased losses driven by recent vintages maturing. Nonperforming assets increased 3% from the third quarter as growth in commercial nonaccrual loans more than offset declines in consumer. The increase in commercial real estate non-accrual loans was driven by a $567 million increase in office non-accrual loans. Moving to Slide 8. Our allowance for credit losses increased slightly in the fourth quarter, driven by an increase for credit card and commercial real estate loans, partially offset by a lower allowance for auto loans. The table on the page shows the allowance for credit losses coverage ratio for commercial real estate, including the breakdown of the office portfolio. While the charge offs we took in the fourth quarter
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 3 | `WFC_2023_Q3_prepared_remarks_200_014`, `WFC_2024_Q1_prepared_remarks_200_015`, `WFC_2023_Q4_prepared_remarks_200_011`, `WFC_2023_Q4_prepared_remarks_200_012` | WFC_2023_Q3, WFC_2023_Q4, WFC_2024_Q1 | no |
| 333 | `WFC_2023_Q3_prepared_remarks_200_014` | WFC_2023_Q3 | no |
| 4 | `WFC_2024_Q1_prepared_remarks_200_015` | WFC_2024_Q1 | no |
| 1.3 | `WFC_2023_Q3_prepared_remarks_200_014` | WFC_2023_Q3 | no |
| 3 | `WFC_2023_Q3_prepared_remarks_200_014`, `WFC_2024_Q1_prepared_remarks_200_015`, `WFC_2023_Q4_prepared_remarks_200_011`, `WFC_2023_Q4_prepared_remarks_200_012` | WFC_2023_Q3, WFC_2023_Q4, WFC_2024_Q1 | no |
| 567 | `WFC_2023_Q4_prepared_remarks_200_012` | WFC_2023_Q4 | no |
| 4 | `WFC_2024_Q1_prepared_remarks_200_015` | WFC_2024_Q1 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

## Stratum 4 -- answered_grounded_ungrounded, Case B (the 2 remaining ungrounded items)

### Item 26: `ref_them_12` / `chunk200_hybrid`

- **question_id:** ref_them_12
- **condition:** chunk200_hybrid
- **category:** thematic
- **case:** B
- **current outcome label:** answered_ungrounded

**Question:**
> What did firms say during 2023 about their wealth management businesses and the investment behind them?

**Gold anchor(s):**
> wealth management business, revenue decreased by 5%, driven by lower net interest revenue and changes
> keep investing through the cycle on the funnel and wealth,

**Generated answer, verbatim:**

```
Based on the provided context, several firms discussed their wealth management businesses and related investments for 2023:

*   **Wells Fargo (WFC):** The firm stated that revenue growth from investments in Wealth and Investment Management would help fund additional investments. They noted that these drivers would help close gaps and improve returns.
*   **Morgan Stanley (MS):** The company highlighted that its wealth and investment management business line generated operating leverage and high returns during the 2020–2022 period following acquisitions of E*TRADE and Eaton Vance. In 2023, despite challenges, the firm’s business model generated consistent results with $54 billion in revenues and a 13% return on tangible common equity.
*   **Goldman Sachs (GS):** The firm reported driving solid investment performance and consistent growth in its Asset & Wealth Management segment. This included growth in management fees, other fees, and private banking and lending revenues. They also noted surpassing their five-year alternatives fundraising target one year early.
*   **Bank of America (BK):** Executives described 2023 as a foundational year involving significant investments across all segments, including wealth management. They mentioned beginning to see "green shoots" in the wealth management business and making investments to modernize platforms and drive efficiency and growth.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `WFC_2023_Q4_prepared_remarks_200_029` -- transcript `WFC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
, and help drive growth. We expect the revenue growth that these investments should generate in businesses like Corporate Investment Banking and Wealth And Investment Management will help fund additional investments. So, we have many drivers to close the gap and improve returns. In summary, our results in 2023 demonstrated our commitment to improving our financial performance. We grew revenue, reduced expenses, increased capital returns to shareholders and maintained our strong capital position. We will now take your questions.
```

*Rank 2 -- `MS_2023_Q4_prepared_remarks_200_002` -- transcript `MS_2023_Q4` -- NOT one of the question's own transcript_ids*

```
equities. During this period, we also acquired Solium, which was a step toward leadership in the corporate stock plan space. Then in 2020 to '22, the COVID years, we achieved incremental scale in both wealth and investment management with the acquisitions of E*TRADE and Eaton Vance, giving us a leading self-directed platform and pushing forward in investment solutions. During this period, each of the two major business lines -- wealth and investment management and institutional securities generated operating leverage and high returns. Transformed Morgan Stanley today has tripled client assets in its durable businesses with significant opportunities for further growth. Notwithstanding 2023's geopolitical, macroeconomic and industry challenges, the firm's business model generated consistent results. In 2023, firm revenues were $54 billion with $12 billion of PBT, double the averages of 2009 to '14. Our return on tangible common equity was a solid 13%, inclusive of notable items that reduced returns by over 100 basis points
```

*Rank 3 -- `GS_2023_Q4_prepared_remarks_200_003` -- transcript `GS_2023_Q4` -- NOT one of the question's own transcript_ids*

```
scaled business with over $2.8 trillion in assets under supervision and where we see significant opportunity for further growth. Across these two businesses, our extraordinary talent and unmatched execution are bolstered by our One Goldman Sachs operating ethos. On page three, we lay out our progress across a number of key priorities that we discussed at our most recent Investor Day in February 2023. Global Banking & Markets, we've maintained and strengthened our leadership positions across investment banking. In FICC and equities, we have improved our standing with the top 150 clients. We generated record total financing revenues across these businesses in 2023 and have demonstrated impressive growth over the last four years. In Asset & Wealth Management, we've driven solid investment performance and consistent growth in a more durable revenue base of management, other fees, and private banking and lending revenues. This past year, we reduced our historical principal investments by $13 billion, and also surpassed our five-year alternatives fundraising target one year
```

*Rank 4 -- `BK_2023_Q4_qa_200_001` -- transcript `BK_2023_Q4` -- NOT one of the question's own transcript_ids*

```
it, if you take the comments stock both Rob and I have prepared and we've just laid out over the last 30 to 35 minutes, you can see truly that 2023 was a foundational year. We did a lot of kind of exploratory work, detailed planning. We've made a bunch of investments, both which will drive efficiency and which will drive growth. We've talked over the last few quarters about Wove, which we launched last June, and in my prepared remarks, I talked about $30 million to $40 million of revenue this year. So I would say we are making investments in all of our segments, and you can also see is in investments in wealth management, where we are beginning to see green shoots, and you can see, we're making a lot of investments in our security and services business, modernizing our platforms. So I would say you're going to see us quarter-by-quarter and I think over time as
```

*Rank 5 -- `STT_2023_Q4_prepared_remarks_200_002` -- transcript `STT_2023_Q4` -- NOT one of the question's own transcript_ids*

```
as of today, and we disclaim any obligation to update them, even if our views change.  Now, let me turn it over to Ron.

Ron O'Hanley: Thank you, Ilene, and good morning, everyone. Earlier today, we released our fourth quarter and full year 2023 financial results. As I reflect on 2023, the operating environment was dynamic with a complex set of challenges for the world's investors and for our industry, and I am proud of how we carefully navigated State Street through various headwinds, while continuing to execute against our strategic agenda. We focused and delivered on that agenda in three key areas; achieve strong sales wins across our businesses, drive strategic change in our investment services business and remain disciplined on productivity and broader cost management. Further on that last point, during 2023, we implemented key productivity actions and announced additional efficiency measures that will enable us to enhance the productivity of our operating model in 2024 and the years ahead. We
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 2020 | `MS_2023_Q4_prepared_remarks_200_002` | MS_2023_Q4 | no |
| 2022 | *(not found in any retrieved chunk)* | -- | -- |
| 54 | `MS_2023_Q4_prepared_remarks_200_002` | MS_2023_Q4 | no |
| 13 | `MS_2023_Q4_prepared_remarks_200_002`, `GS_2023_Q4_prepared_remarks_200_003` | GS_2023_Q4, MS_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 27: `ref_them_15` / `chunk500_hybrid`

- **question_id:** ref_them_15
- **condition:** chunk500_hybrid
- **category:** thematic
- **case:** B
- **current outcome label:** answered_ungrounded

**Question:**
> How much did banks say they were spending on technology over 2023 and 2024, and how did that spend and related G&A expense change?

**Gold anchor(s):**
> themes, technology spend was $3 billion in the quarter, up 13%, primarily driven by change
> increased our technology initiatives and expect to spend nearly $4 billion on technology initiatives
> up 7% year-over-year, primarily due to the timing of technology spend in the prior year

**Generated answer, verbatim:**

```
Based on the provided context, here is the information regarding technology spending and General & Administrative (G&A) expenses:

**Bank of America (BAC)**
*   **Technology Spend:** The text does not specify a total dollar amount for Bank of America’s technology spend in 2023 or 2024. It notes that expense growth was driven by investments in risk, controls, and technology, but specific figures are not provided.
*   **G&A/Expense Changes:** In 2023, the bank achieved 170 basis points of operating leverage as quarterly expense levels were driven lower throughout the year despite continued growth investments. The text does not provide specific G&A percentage changes for 2024.

**BlackRock (BLK)**
*   **Technology Spend:** BlackRock stated that technology is one of its primary areas of investment within G&A. In Q1 2024, G&A expense increased 6% year-over-year due to the timing of technology investment spend in the prior year. The company expects a low-to-mid-single-digit percentage increase in core G&A expense for full-year 2024.
*   **G&A Expense Changes:**
    *   **Q1 2024:** G&A expense increased 6% compared to the same period last year, primarily due to the timing of technology investment spend. Sequentially (compared to Q4 2023), G&A decreased by 12%, reflecting the timing of that technology spend and seasonally higher marketing expenses in Q4.
    *   **Q3 2023:** Total expense was 4% higher year-over-year, with G&A lower than the prior year (partially offsetting higher compensation). The company expected full-year 2023 core G&A to fall on the low end of its guidance for a mid-to-high-single-digit percentage increase.

**Note on Other Institutions:**
*   **JPMorgan Chase (implied by C_2023_Q4 context):** While the chunk labeled `C_2023_Q4_prepared_remarks_500_007` discusses a firm that invested over $12 billion in technology in 2023 and had full-year expenses of $54.3 billion, it does not explicitly name the bank as "Bank of America" or another specific entity in the text provided (though the context ID suggests a major bank). It states that roughly 30% of transformation investments over the last three years were in technology. For 2023, there was a shift from consulting expenses to technology and compensation. No specific G&A percentage change is given for this firm, only total expense figures.

**Summary of Specific Figures:**
*   **BlackRock Q1 2024 G&A:** Up 6% year-over-year; down 12% sequentially.
*   **BlackRock 2024 Outlook:** Low-to-mid-single-digit increase in core G&A.
*   **Unnamed Firm (C_2023_Q4):** Invested over $12 billion in technology in 2023.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `C_2023_Q4_prepared_remarks_500_007` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
uation, we grew firm-wide revenues by approximately 4% ex-divestitures in line with our Investor Day target, demonstrating the benefit of our diversified business model and the investments we've been making. On slide nine, we show full year expense trends from 2021 to 2023, excluding the FDIC special assessment and divestiture-related impacts, full year expenses were $54.3 billion for 2023 in line with our guidance. As I mentioned, this includes roughly $780 million of restructuring costs associated with our organizational simplification and additional severance costs of approximately $730 million, which included actions to address stranded costs and start to right-size the businesses. Relative to the prior year, expense growth continued to be driven by transformation and business-led investments, volume-related expenses and other investments in risk and controls and technology, partially offset by productivity savings and a reduction in expenses and legacy franchises within all other. Over the past few years, we've been investing across these themes, which has not only impacted the performance of the firm, but also the businesses. On slide 10, we show the components of our transformation and technology spend from 2021 to 2023. Over the past three years, we have invested significantly in our infrastructure, platforms, applications, processes and data. As you can see in the bar chart at the top of the slide, roughly 30% of our transformation investments over the last three years were in technology, with the remainder related to non-tech employees and consultants. In 2023, we've seen a shift from consulting expenses to technology and compensation as we've gotten deeper into the execution of our transformation. And you should expect to see this trend continue. In total, we invested over $12 billion in technology in 2023. Beyond transformation, our technology investments are also focused on digital innovation, new product development, client experience enhancements and areas that support our infrastructure like cloud and cyber. On slide 11, we show key consumer and corporate credit metrics. Across branded cards and retail services, approximately 80% of our card loans are to consumers with FICO scores of 680 or higher. And across both portfolios, NCL rates have reached pre-COVID levels, but we continue to be well reserved with a reserve to funded loan ratio of 7.7%. In our corporate portfolio, the majority of our exposure is investment grade, which is reflected in our low level of nonaccrual loans at 63 basis points of
```

*Rank 2 -- `BLK_2024_Q1_prepared_remarks_500_003` -- transcript `BLK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
, G&A expense decreased 12%, reflecting timing of technology investment spend and seasonally higher marketing and promotional expense in the fourth quarter. While one quarter's results can be impacted by timing of spend, we expect technology to be one of our primary areas of investment within G&A. Sales asset and account expense increased 5% compared to a year ago, primarily driven by higher direct fund expense. Direct fund expense was up 7% year-over-year, mainly due to higher average index AUM. Sequentially, direct fund expense increased due to higher average index AUM in the current quarter and higher rebates that seasonally occurred in the fourth quarter. Our first quarter as adjusted operating margin of 42.2% was up 180 basis points from a year ago. As markets improve, we remain committed to driving operating leverage and profitable growth. BlackRock's industry leading organic growth is a direct result of the disciplined investments we've made consistently through market cycles. Looking forward, we'll continue to prioritize investments with differentiated organic growth potential or that will expand operating leverage through enhanced scale. In line with our guidance in January and excluding the impact of global infrastructure partners and related transaction costs, at present, we would expect our headcount to be broadly flat in 2024 and we would also expect a low to mid-single-digits percentage increase in 2024 core G&A expense. Our capital management strategy remains consistent. We invest first, either to scale strategic growth initiatives or drive operational efficiency and then return excess cash to our shareholders through a combination of dividends and share repurchases. At times, we may make inorganic investments, where we see an opportunity to accelerate organic growth and support our strategic initiatives. Last month, we announced our agreement to acquire the remaining equity interest in SpiderRock Advisors, a leading provider of customized option overlay strategies in the U.S. wealth market. This transaction expands on BlackRock's minority investment in SpiderRock Advisors made in 2021 and builds on BlackRock's strong growth in personalized separately managed accounts via Aperio and ETF model portfolios. At present, we expect the transaction to close in the second quarter of this year, subject to customary closing conditions. In March, we issued $3 billion of debt to fund a portion of the cash consideration for our planned acquisition of GIP. Our offering consisted of three tranches of senior unsecured notes across 5, 10 and 30 year maturities
```

*Rank 3 -- `BLK_2023_Q3_prepared_remarks_500_003` -- transcript `BLK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
-US equity markets, and changing client risk preferences favoring risk off lower fee exposures. As a result of continued global equity and bond market depreciation toward the end of the third quarter, including the impact of FX-related dollar appreciation, we entered the fourth quarter with an estimated base fee run rate, approximately 3% lower than our total base fees for the third quarter. Performance fees of $70 million decreased from a year ago, primarily reflecting lower revenue from liquid alternatives. Quarterly technology services revenue was up 20% compared to a year ago, driven by sustained demand for our technology offerings. Current quarter technology services revenue also benefited from the impact of several large client renewals of their eFront on-premises licenses, for which accounting treatment recognizes a majority of the revenue at time of renewal. Approximately half of the year-over-year technology services revenue increase resulted from these eFront contract renewals. Annual contract value, or ACV, increased 10% year-over-year. We remain committed to low- to mid-teens ACV growth over the long-term, driven by demand for Aladdin's broadening technology capabilities and the growing value proposition it presents for clients. Total expense was 4% higher year-over-year. Higher compensation and direct fund expenses were partially offset by lower distribution and servicing costs and G&A. At present, we expect full year 2023 core G&A to fall on the low end of our previously communicated guidance of a mid- to high-single-digit percentage increase. In line with this outlook, we would also expect fourth quarter core G&A to reflect seasonal increases in marketing spend and execution of planned technology investment spend. Our third quarter as-adjusted operating margin of 42.3% was up 30 basis points from a year ago, benefiting in part from the favorable impact of market movements on quarterly revenue over the last year. Our platform strategy has delivered scale and operating leverage through time, and we aim to be disciplined in driving profitable growth. We're prioritizing investments to propel our differentiated organic growth and drive operating leverage. We'll look to find more opportunities to variabilize expenses, generate fixed cost scale through technology and automation, and align investment spend with organic revenue growth potential. Our capital management strategy remains consistent. We invest first, either to scale strategic growth initiatives or drive operational efficiency, and then return excess cash to our shareholders through a combination of dividends and share repurchases
```

*Rank 4 -- `BAC_2023_Q4_prepared_remarks_500_002` -- transcript `BAC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 5 -- `BLK_2024_Q1_prepared_remarks_500_002` -- transcript `BLK_2024_Q1` -- NOT one of the question's own transcript_ids*

```
awards that vest in the first quarter of each year. We continue to estimate that 25% is a reasonable projected tax run rate for the remainder of 2024, though the actual effective tax rate may differ because of non-recurring or discrete items or potential changes in tax legislation. First quarter base fee in securities lending revenue of $3.8 billion was up 8% year-over-year and up 5% sequentially driven by the positive impact of market beta on average AUM and positive organic base fee growth. On an equivalent day count basis, our annualized effective fee rate was 3/10 of a basis point lower compared to the fourth quarter. This was mainly due to the relative outperformance of lower fee U.S. equity markets, client preferences for lower fee U.S. exposures and lower securities lending revenue. Performance fees of $204 million increased from a year ago, primarily reflecting higher revenue from alternatives. Quarterly technology services revenue was up 11% compared to a year ago, reflecting sustained demand for our Aladdin technology offerings. Annual contract value or ACV increased 9% year-over-year. Beginning in the first quarter of 2024, earnings recognized from minority investments accounted for under equity method will be presented as part of our non-operating results. Advisory and other revenue increased from a year ago, primarily reflecting this change. In addition, as many of you know, we updated the presentation of expense line items by including a new sales asset and account income statement caption. This category includes distribution and servicing costs, direct fund expense and sub-advisory and other sales asset and account-based expense. Sub-advisory and other expense, which are variable non-compensation expenses associated with asset and revenue growth was previously reported within general and administration expense. We believe this change provides investors a clearer view of both BlackRock's variable non-compensation expense and G&A, which represents more fixed costs. It represents how we'll execute on our financial rubric of aligning investment spend with our highest conviction growth areas, variabilizing more of our expense base and generating fixed cost scale. Total expense increased 8% year-over-year, reflecting higher compensation, G&A and sales asset and account expense. Employee compensation and benefit expense was up 11%, primarily reflecting higher incentive compensation as a result of higher operating income and performance fees. G&A expense increased 6% due to the timing of technology investment spend in the prior year. Sequentially
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 170 | `BAC_2023_Q4_prepared_remarks_500_002` | BAC_2023_Q4 | no |
| 1 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 6 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_002` | BLK_2024_Q1, C_2023_Q4 | no |
| 1 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 6 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_002` | BLK_2024_Q1, C_2023_Q4 | no |
| 4 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 12 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003` | BLK_2024_Q1, C_2023_Q4 | no |
| 4 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 3 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 4 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 4 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 4 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 500 | *(not found in any retrieved chunk)* | -- | -- |
| 007 | *(not found in any retrieved chunk)* | -- | -- |
| 12 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003` | BLK_2024_Q1, C_2023_Q4 | no |
| 54.3 | `C_2023_Q4_prepared_remarks_500_007` | C_2023_Q4 | no |
| 30 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003` | BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 1 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 6 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_002` | BLK_2024_Q1, C_2023_Q4 | no |
| 12 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003` | BLK_2024_Q1, C_2023_Q4 | no |
| 4 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003`, `BLK_2023_Q3_prepared_remarks_500_003`, `BAC_2023_Q4_prepared_remarks_500_002`, `BLK_2024_Q1_prepared_remarks_500_002` | BAC_2023_Q4, BLK_2023_Q3, BLK_2024_Q1, C_2023_Q4 | no |
| 12 | `C_2023_Q4_prepared_remarks_500_007`, `BLK_2024_Q1_prepared_remarks_500_003` | BLK_2024_Q1, C_2023_Q4 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

## Stratum 5 -- Case C answered_grounded_correct, NOT flagged in Check 3 (control -- what a clean pass looks like)

### Item 28: `ref_fact_01` / `chunk200_bm25`

- **question_id:** ref_fact_01
- **condition:** chunk200_bm25
- **category:** factual
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> What were BNY Mellon's assets under custody and administration in the first quarter of 2024, and how did they change?

**Gold anchor(s):**
> custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management

**Generated answer, verbatim:**

```
In the first quarter of 2024, BNY Mellon’s firm-wide assets under custody and/or administration were $48.8 trillion, representing a 5% increase year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `STT_2023_Q1_qa_200_047` -- transcript `STT_2023_Q1` -- NOT one of the question's own transcript_ids*

```
they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it won't be quite at that level because the revenues come through over time as you get the different, I'll call it, layers of services that are provided associated with those -- that assets under custody, administration. But what we'll do is we'll -- I think it's -- that may be some kind of broad perspective. What we'll try to do each quarter is give you more and more visibility as we get to those implementation points because, remember,
```

*Rank 2 -- `BK_2024_Q3_prepared_remarks_200_004` -- transcript `BK_2024_Q3` -- NOT one of the question's own transcript_ids*

```
ciencies from running our company in new and better ways. Pre-tax margin and return on tangible common equity improved year-over-year to 33% and 23%, respectively. For the first time in our history, we reported over $50 trillion of assets under custody and/or administration at the end of the quarter. Now, custody is not something we are, but it is something important that we do. This number one market position improves our unique vantage point as a global financial services company, and it provides opportunity to drive value across our portfolio of adjacent businesses to deliver more of BNY to our clients. We increasingly see that the true power of BNY's client franchise exists in the combination of capabilities across our leading Security Services, Market and Wealth Services, and Investments and Wealth businesses. We have the ability to enhance this and to deliver more to our clients by bringing new innovative solutions to the market from across the seams of these businesses. As an example, we recently announced the
```

*Rank 3 -- `BK_2023_Q1_prepared_remarks_200_012` -- transcript `BK_2023_Q1` -- NOT one of the question's own transcript_ids*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 -- `BK_2023_Q3_prepared_remarks_200_018` -- transcript `BK_2023_Q3` -- NOT one of the question's own transcript_ids*

```
as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and
```

*Rank 5 -- `BK_2024_Q1_prepared_remarks_200_010` -- transcript `BK_2024_Q1` -- ONE OF the question's own transcript_ids*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 48.8 | `BK_2024_Q1_prepared_remarks_200_010` | BK_2024_Q1 | yes |
| 5 | `BK_2024_Q3_prepared_remarks_200_004`, `BK_2023_Q1_prepared_remarks_200_012`, `BK_2023_Q3_prepared_remarks_200_018`, `BK_2024_Q1_prepared_remarks_200_010` | BK_2023_Q1, BK_2023_Q3, BK_2024_Q1, BK_2024_Q3 | yes |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 29: `ref_them_04` / `chunk200_dense`

- **question_id:** ref_them_04
- **condition:** chunk200_dense
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Gold anchor(s):**
> 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven
> operating leverage this quarter as expenses decreased 4%, driven by actions taken to right size

**Generated answer, verbatim:**

```
Based on the provided context, Bank of America described achieving 170 basis points of operating leverage in 2023, noting that heightened quarterly expense levels were driven lower throughout the year. Additionally, Fifth Third Bancorp (FITB) projected that its income statement performance trajectory would deliver positive operating leverage in the fourth quarter of 2024.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `C_2023_Q4_prepared_remarks_200_010` -- transcript `C_2023_Q4` -- NOT one of the question's own transcript_ids*

```
investors through both of these channels. As I reflect on the year, I also want to note that we were a source of strength for the system and for clients during a volatile period for the banking sector and geopolitically and I'm very proud of how our people around the world performed during challenging times. 2024 looks to be similar to 2023 in terms of the macro environment with moderating rates and inflation. We expect to see growth slowing globally with the US well positioned to withstand a run-of-the-mill recession should one materialize. With a strong balance sheet, ample liquidity and diligent risk management we are well positioned to support our clients through whatever environment comes to path. Moreover, we think environments like these play to our strengths, given how far we are down the path of our simplification and divestitures. 2024 will be a turning point as we will be able to completely focus on the performance of our five businesses and our transformation. I
```

*Rank 2 -- `BAC_2023_Q4_prepared_remarks_200_005` -- transcript `BAC_2023_Q4` -- ONE OF the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as
```

*Rank 3 -- `MTB_2024_Q4_prepared_remarks_200_003` -- transcript `MTB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
us to have such a successful year. In 2024, we focused on four priorities, including building our New England and Long Island markets, optimizing our resources through simplification, making our systems and processes resilient and scalable, and continuing to develop and scale our risk management. The progress we made on these priorities related and related enterprise initiatives will allow the bank to continue to grow and scale in coming years. Our focus on fundamentals is reflected in several of our financial accomplishments in 2024. We executed our financial plan for the year and the results met or exceeded the outlook we discussed last January for NII, fee income, expenses, and average loans and deposits. We made significant progress on our CRE concentration, reaching what we believe is a target level. Our capital levels continue to grow through the year and remain strong, as we restarted our share repurchase program in the third quarter. We actively managed our interest rate sensitivity through our hedging program and securities portfolio
```

*Rank 4 -- `FITB_2024_Q2_prepared_remarks_200_018` -- transcript `FITB_2024_Q2` -- NOT one of the question's own transcript_ids*

```
strength in commercial payments and wealth and asset management and a modest increase in commercial banking revenue. We expect third quarter total adjusted non-interest expenses to be up 1% compared to the second quarter, due to the impact of the previously discussed investments in branches, technology, and sales personnel. Third quarter net charge-offs are projected to be in the 40 basis points to 45 basis point range. As mentioned in the [four-year] (ph) outlook, loan growth and mix are expected to drive a provision build, which should be around $25 million in the third quarter, assuming no change to the economic outlook. The trajectory of our income statement performance should deliver positive operating leverage in the fourth quarter 2024 and a net interest income exit rate for the year that positions us for record results in 2025, assuming no major economic or interest rate outlook changes. Finally, moving to capital. With our consistent and strong earnings, we expect to execute share repurchases of $200 million per quarter
```

*Rank 5 -- `MS_2024_Q4_prepared_remarks_200_015` -- transcript `MS_2024_Q4` -- NOT one of the question's own transcript_ids*

```
products. 2024 commenced with strong debt underwriting activity, followed by M&A announcements that picked up in the second half, and ended with increased equity underwriting activity as the IPO market posted its highest volumes since 2021. Fourth quarter investment banking revenues were $1.6 billion. Results were largely driven by accelerating strength in equity underwriting as follow-on and IPO issuance saw meaningful improvements across -- over the comparison period. We also saw corporates and sponsors take advantage of constructive markets in the quarter. Advisory revenues improved year-over-year on higher completed M&A transactions. Looking ahead to 2025, our M&A pipelines are healthy and diversified, outpacing recent years. Financial sponsors are joining corporates to drive activity, evaluating exit opportunities for long held assets. CEO and boardroom confidence continues to improve as valuations stabilize and financing markets remain strong. Our business is well positioned for a strong continued rebound in deal making activity. Turning to equity. We
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 170 | `BAC_2023_Q4_prepared_remarks_200_005` | BAC_2023_Q4 | yes |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 30: `ref_comp_08` / `chunk500_bm25`

- **question_id:** ref_comp_08
- **condition:** chunk500_bm25
- **category:** comparative
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?

**Gold anchor(s):**
> return on tangible common equity was 17.41% and tangible book value per share increased 3%
> book value per share, excluding AOCI, increased 10% compared to the year

**Generated answer, verbatim:**

```
In the third quarter of 2023, M&T described its tangible book value per share as increasing by 3% compared to the end of June. The provided context does not contain information regarding how Fifth Third described its tangible book value per share for that specific quarter.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2023_Q1_prepared_remarks_500_000` -- transcript `FITB_2023_Q1` -- NOT one of the question's own transcript_ids*

```
Chris Doll: Good morning everyone. Welcome to Fifth Third’s First Quarter 2023 Earnings Call. This morning our President and CEO, Tim Spence and CFO, Jamie Leonard will provide an overview of our first quarter results and outlook. Our Treasurer, Bryan Preston has also joined for the Q&A portion of the call. Please review the cautionary statements and our materials which can be found on our earnings release and presentation. These materials contain information regarding to the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third’s performance. These statements speak only as of April 20th 2023 and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris. And good morning, everyone. Thank you for joining us today. The past six weeks have seen a great deal of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide impact of quantitative tightening and normal seasonal pressures. Our key credit metrics remain near historical lows with net charge-offs of 26 basis points coming in at the low end of our guidance range. NPAs NPLs and early stage delinquency ratios remained below normalized levels, and criticized assets decrease modestly during the quarter. Moreover, we accomplished all this while also being recognized by Ethisphere as one of only two U.S. banks on their world's most ethical companies
```

*Rank 2 -- `MTB_2024_Q3_prepared_remarks_500_001` -- transcript `MTB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
emissions. Turning to Slide 5, our employees and products continue to receive awards from consumer, business, and trade organizations. We're into Slide 7, which shows the results of the third quarter. As noted in this morning's press release, we released our third quarter results as we continue to make progress on the plans we laid out in January. There are several successes to highlight. [Net interest margin and non-interest] (ph) income grew sequentially as we continue to grow loans while reducing our CRE concentration. In fact, since the fourth quarter of 2023, we have grown average loans by nearly $2 billion while reducing CRE by over $4 billion and growing C&I and consumer loans. Funding costs was well managed in this quarter with a 4 basis point decline in the cost of interest bearing liabilities. We restarted our share repurchase program in the third quarter and executed $200 million in share repurchases and grew our CET1 ratio to over 11.5%. Non-interest income reached a high point in the third quarter, if we exclude the prior gains on our two divestitures. This was achieved by even considering the foregone fee income from those two sold businesses, demonstrating the resiliency and strength of our diversified business model. Asset quality continued to improve this quarter with reduction in both non-accrual balances and commercial credit size loans and net charge-offs below the full year outlook. Now let's look at the specifics for the third quarter. Diluted GAAP earnings per share were $4.02 for the third quarter, improved from $3.73 in the second quarter. Net income for the quarter was $721 million compared to $655 million in the linked quarter, an increase of 10%. M&T's third quarter results produced an ROA and ROCE of 1.37% and 10.26% respectively. The CET1 ratio remains strong, growing at 11.54% at the end of the third quarter and tangible book value first year grew 5%. Of note, the third quarter included a discrete tax benefit of $14 million or an $0.08 EPS benefit. Slide 8 includes supplemental reporting of M&T's results on a net operating and tangible basis. M&T's net operating income for the third quarter was $731 million compared with $665 million in the linked quarter. Diluted net operating
```

*Rank 3 -- `MTB_2023_Q3_prepared_remarks_500_002` -- transcript `MTB_2023_Q3` -- ONE OF the question's own transcript_ids*

```
98 for the third quarter, up 13% from last year’s similar quarter. Now, let’s review our net operating results for the quarter on Slide 9. M&T’s net operating income for the third quarter, which excludes intangible amortization was $702 million and diluted net operating earnings per share, was $4.05. Net operating return on tangible common equity was 17.41% and tangible book value per share increased 3% compared to the end of June. On Slide 10, you will see that diluted GAAP earnings per share, was down 21% from linked quarter. Recall our results from the second quarter of last year indicated an after-tax $157 million gain from the sales of CIT business in April. Excluding this gain, GAAP net income and diluted earnings per share were down 3% compared to the linked quarter. On a GAAP basis, M&T’s third quarter results produced an ROA and ROE of 1.33% and 10.99% respectively. Next, we will look a little deeper into the underlying trends that generated the third quarter results. Please turn to Slide 11. Taxable equivalent net interest income was $1.79 billion in the third quarter, down $23 million from linked quarter. This decline was driven largely by higher interest rates on consumer deposit funding. An unfavorable funding mix change partially offset by higher interest rates on earning assets and 1 additional day. The net interest margin for the past quarter was 3.79%, down 12 basis points from linked quarter. The primary drivers of the decrease to the margin were an unfavorable deposit mix shift, which reduced margin by 7 basis points; the net impact from higher interest rates on customer deposits, net benefit from higher rates on earning assets which we estimate reduced the margin by 6 basis points. The remaining 1 basis point was due to higher non-accrual interest, net of the impact of 1 additional day. Turning to Slide 12. Average earning assets increased $1.5 billion from the linked quarter, due largely to the strong deposit growth that drove the $3 billion growth at the Fed. Average loans declined $928 million and average investment securities declined $630 million. Turning to Slide 13 to talk about average loans. Total loans and leases averaged $132.6 million for the third quarter of 2023, down 1% compared to the linked quarter. Looking at loans by category, on
```

*Rank 4 -- `FITB_2023_Q3_prepared_remarks_500_000` -- transcript `FITB_2023_Q3` -- ONE OF the question's own transcript_ids*

```
Operator: Good morning. My name is Rob and I will be your conference operator today. At this time, I would like to welcome everyone to the Fifth Third Bancorp Third Quarter 2023 Earnings Conference Call. [Operator Instructions] Chris Doll, Head of Investor Relations. You may begin your conference.

Chris Doll: Good morning, everyone. Welcome to the Fifth Third's third quarter 2023 earnings call. This morning, our President and CEO, Tim Spence; and CFO, Jamie Leonard, will provide an overview of our third quarter results and outlook. Our Treasurer, Bryan Preston; and Chief Credit Officer, Greg Schroeck, have also joined us for the Q&A portion of the call. Please review the cautionary statements on our materials, which can be found in our earnings release and presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results as well as forward-looking statements about Fifth Third's performance. These statements speak only as of October 19, 2023, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris, and good morning, everyone. We believe that great banks distinguish themselves not by how they perform in benign environments, but rather by how they navigate challenging ones. That is why we focus on stability, profitability, and growth in that order. It is also why I am so pleased that our key return and profitability metrics remain resilient despite the market-related headwinds that all banks are facing. Earlier today, we reported earnings per share of $0.91 or $0.92 excluding a one set impact from our Visa swap, reflecting strong PPNR results and favorable credit outcomes. We generated an adjusted return on tangible common equity ex-AOCI of nearly 16%, which increased 50 basis points sequentially, and a return on assets of 1.26%. We generated strong fee growth compared to the year ago quarter, supported by a more diverse range of fee income streams than peers, and our investments in treasury management, capital markets, and wealth management. Our third quarter total non-interest expense increased less than 2% compared to the year ago quarter, and we generated an adjusted efficiency ratio below 55%. In the last four years, we have managed expenses to the lowest growth rate
```

*Rank 5 -- `FITB_2023_Q4_prepared_remarks_500_001` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
AOCI of 15.9% and an adjusted efficiency ratio of 55.9%. All among the best of our peers. We also continue to take market share organically by growing our customer base and deepening relationships. We grew consumer households by 3% overall punctuated by 6% growth in the Southeast. In commercial, we added a record number of new quality middle market relationships up 11% over the prior year. As a result, we grew or maintained our deposit market share position in all 40 of our largest MSAs. As we turn the page to 2024, we remain focused on differentiating Fifth Third based on the strength and consistency of our financial performance by prioritizing stability, profitability, and growth in that order. Bryan will take you through the detail on the fourth quarter and our outlook for the year shortly. But before that, I would like to touch on a few points. The first of these is the strength of our balance sheet. Our defensive positioning and decision to move quickly to adapt to proposed regulatory changes have put us in a position to play offense in 2024. Having achieved full Category 1 LCR compliance on August 31st and maintained it since, our liquidity position is very strong. We completed our RWA diet in the fourth quarter and accreted nearly 50 basis points of CET1, putting us on pace to reach a 10.5% CET1 ratio by mid-year 2024. Given our strong earnings profile and the significant rally in interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 3 | `FITB_2023_Q1_prepared_remarks_500_000`, `MTB_2024_Q3_prepared_remarks_500_001`, `MTB_2023_Q3_prepared_remarks_500_002`, `FITB_2023_Q3_prepared_remarks_500_000`, `FITB_2023_Q4_prepared_remarks_500_001` | FITB_2023_Q1, FITB_2023_Q3, FITB_2023_Q4, MTB_2023_Q3, MTB_2024_Q3 | yes |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 31: `ref_fact_10` / `chunk500_dense`

- **question_id:** ref_fact_10
- **condition:** chunk500_dense
- **category:** factual
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> What was PNC's AOCI position at the end of the third quarter of 2023, and what had it been at the end of the prior quarter?

**Gold anchor(s):**
> AOCI was a negative $10.3 billion compared to a negative $9.5 billion at June 30,

**Generated answer, verbatim:**

```
At the end of the third quarter of 2023, PNC’s AOCI was negative $10.3 billion, compared to a negative $9.5 billion at the end of the prior quarter (June 30).
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2023_Q4_prepared_remarks_500_001` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
AOCI of 15.9% and an adjusted efficiency ratio of 55.9%. All among the best of our peers. We also continue to take market share organically by growing our customer base and deepening relationships. We grew consumer households by 3% overall punctuated by 6% growth in the Southeast. In commercial, we added a record number of new quality middle market relationships up 11% over the prior year. As a result, we grew or maintained our deposit market share position in all 40 of our largest MSAs. As we turn the page to 2024, we remain focused on differentiating Fifth Third based on the strength and consistency of our financial performance by prioritizing stability, profitability, and growth in that order. Bryan will take you through the detail on the fourth quarter and our outlook for the year shortly. But before that, I would like to touch on a few points. The first of these is the strength of our balance sheet. Our defensive positioning and decision to move quickly to adapt to proposed regulatory changes have put us in a position to play offense in 2024. Having achieved full Category 1 LCR compliance on August 31st and maintained it since, our liquidity position is very strong. We completed our RWA diet in the fourth quarter and accreted nearly 50 basis points of CET1, putting us on pace to reach a 10.5% CET1 ratio by mid-year 2024. Given our strong earnings profile and the significant rally in interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

*Rank 2 -- `PNC_2023_Q4_prepared_remarks_500_001` -- transcript `PNC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
. Expense discipline remains a top priority for us and accordingly we are targeting stable expenses for 2024 even as we continue to invest in key growth initiatives. Fourth, our credit quality remained strong during the quarter, reflecting our thoughtful approach us to growing our balance sheet. While we continue to expect credit charge offs to increase over time, particularly in the CRE office segment, we’re adequately reserved. Finally, during the fourth quarter, we increased our capital position, saw solid improvement in our AOCI intangible book value and repurchased a modest amount of shares. In summary, we run our company with a focus on delivering through the cycle performance and feel very good about our strategy, our capabilities and the strength of our balance sheet as we enter 2024. And we believe we are well positioned to drive growth and deliver shareholder value in the coming year and beyond. As always, I want to thank our employees for everything they do to meet the needs of our customers and make our success possible.  And with that, I'll turn it over to Rob.

Rob Reilly: Thanks, Bill, and good morning, everyone. Our balance sheet is on Slide 3 and is presented on an average basis and compared to the third quarter. Loans were up 2% and averaged $325 billion, which includes the acquired Signature capital commitment loans. Investment securities declined $2 billion or 2%. Cash balances at the Federal Reserve increased $4 billion to $42 billion and deposits increased $1.4 billion and averaged $424 billion. Borrowed funds increased $5 billion to $73 billion, driven by higher FHLB borrowings and parent company senior debt issuances. At year end, P&C was fully compliant with the proposed holding company long term debt requirements. And we expect to reach compliance with the bank level metrics through our normal course of funding well in advance of the phase in period. AOCI improved $2.6 billion to negative $7.7 billion at quarter end, primarily reflecting the impact of favorable interest rate movements during the quarter. Accordingly, tangible book value increased to $85.08 per common share, up 9% linked quarter and 18% compared to the same period a year ago. We remain well capitalized with an estimated CET1 ratio of 9.9% as of December 31st, which increased 10 basis points linked quarter. Our estimated fully phased in expanded risk based CET1 ratio based on the new proposed capital rules would be approximately 8
```

*Rank 3 -- `PNC_2023_Q3_prepared_remarks_500_001` -- transcript `PNC_2023_Q3` -- ONE OF the question's own transcript_ids*

```
growth markets and technology. In addition, earlier this month, we began executing on staff reductions, which will reduce our 2024 expenses by $325 million and will fall to the bottom-line. All told, we are implementing more than $725 million of expense management actions that will have impact on 2024. While decisions involving personnel are never easy, we believe they will help us more effectively and efficiently deliver for our customers and our stakeholders, and we'll continue to be diligent in our expense management going forward. And with that, I'll turn it over to Rob.

Rob Reilly: Thanks, Bill, and good morning, everyone. Our balance sheet is on Slide 3 and is presented on an average basis and comparing to the second quarter. Loans were down 2% and averaged $320 billion. Investment securities declined $1 billion or 1%. Cash balances at the Federal Reserve increased $7 billion to $38 billion. Deposits of $423 billion declined $3 billion or 1%. Borrowed funds increased $2 billion, primarily due to senior debt issuances near the end of the second quarter. At quarter-end, AOCI was a negative $10.3 billion compared to a negative $9.5 billion at June 30, reflecting higher interest rates. However, tangible book value increased to $78.16 per common share as retained earnings growth exceeded the negative impact of AOCI. Common dividends in the quarter totaled approximately $600 million. And we remain well capitalized with an estimated CET1 ratio of 9.8% as of September 30, 2023, which increased 30 basis points linked quarter. Slide 4 shows our loans in more detail. Third quarter loans averaged $320 billion and increased $6.5 billion or 2% compared to the same period a year ago, reflecting growth in both commercial and consumer loans. Compared to the second quarter, average loan balances declined 2% as growth in consumer was more than offset by a decline in commercial. Consumer loans grew approximately $500 million, reflecting higher residential mortgage and credit card balances. Commercial loans averaged $218 billion, a decline of $5.5 billion, driven by lower utilization as well as paydowns outpacing new production. Loan yields increased 18 basis points to 5.75% in the third quarter, predominantly driven by the higher rate environment. Slide 5 covers our deposits in more detail. Average deposits decreased $3 billion, or 1%, due to a
```

*Rank 4 -- `FITB_2024_Q3_prepared_remarks_500_006` -- transcript `FITB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
exceeding our buffered minimum of 7.7%, reflecting strong capital levels. Our pro-forma CET1 ratio, including the AOCI impact of the securities portfolio is 8.7%. We expect continued improvement in the unrealized losses in our securities portfolio, given that 59% of the AFS portfolio is in bullet or locked out securities, which provides a high degree of certainty to our principal cash flow expectations. Assuming the forward curve is realized, approximately 24% of the AOCI related to securities losses will accrete back into equity by the end of 2025, increasing tangible book value per share by 6% before considering any future earnings. 61% of the securities related AOCI should accrete back to equity by the end of 2028. During the quarter, we completed $200 million in share repurchases, which reduced our share count by 4.9 million shares. As we assess our capital priorities, we continue to believe that 10.5% is an appropriate near-term operating level. Moving to our current outlook, we anticipate continued growth in NII and NIM during the Q4, with NII up 1% sequentially, reflecting the impact of lower deposit rates and the continued benefit of fixed rate asset repricing, partially offset by the decrease in yield from our floating rate loan portfolio. This outlook assumes a 25 basis point cut in November and a 50 basis point cut in December. We would not expect any change to this outlook if fewer rate cuts were to occur. We expect average total loan balances to be stable to up 1% from the third quarter, with middle market and auto production offsetting mix demand in other asset classes. Fourth quarter adjusted noninterest income is anticipated to rise 3% to 4% compared to the strong Q3, largely due to a continued rebound in capital markets revenue and continued growth in commercial payments. Additionally, we expect fourth quarter TRA revenue to be $10 million down from $22 million in the fourth quarter of 2023. Fourth quarter total adjusted noninterest expenses are expected to be stable compared to the third quarter as the increases in revenue-based compensation and the investments in branches and technology are largely offset by efficiencies achieved in other areas. Fourth quarter net charge-offs are projected to be similar or slightly down from the third quarter. Given the expected increase in loans during the fourth quarter, we anticipate an ACL build of $20
```

*Rank 5 -- `PNC_2023_Q2_prepared_remarks_500_005` -- transcript `PNC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
essentially stable with March 31.  While overall credit quality remains strong across our portfolio, the office category within commercial real estate continues to be a key area of concern. As expected, we saw increases in charge offs related to office during the quarter. However, the portfolio metrics remain largely similar to those presented in our comprehensive view last quarter. Naturally, we'll continue to monitor and review our assumptions to ensure they reflect real time market conditions and a full update is included in the appendix slides.  In summary, PNC reported a solid second quarter 2023. In regard to our view of the overall economy, we're expecting a mild recession starting in early 2024 with a contraction in real GDP of less than 1%. Our rate path assumption includes a 25 basis point increase in the Fed funds rate in July. Following that, we expect the Fed to pause rate actions until March 2024 when we expect the Fed to begin to cut rates.  Looking ahead, our outlook for the third quarter of 2023 compared to the second quarter of 2023 is as follows: We expect average loans to decline approximately 1%; net interest income to be down 3% to 4%; non-interest income to be up 10% to 11%. Taking the component pieces, we expect total revenue to be up approximately 1%. We expect total non-interest expense to be stable and we expect second quarter net charge offs to be between $200 million and $250 million.  Considering our reported operating results for the first half of 2023, third quarter expectations and current economic forecasts for the full year 2023 compared to full year 2022, we expect spot loans to be relatively stable, which equates to average loan growth of 5% to 6%; total revenue growth to be approximately 2% to 2.5%. Inside of that, our expectation is for net interest income to be in the range of up 5% to 6%. This is a move to the lower end of our previous guidance, largely driven by anticipated deposit costs moving a bit faster than we expected and slightly lower loan growth expectations.  We expect non-interest income to decline 2% to 4%, which is down from our earlier expectations of stable. This change is resulting from softer than expected capital markets revenue in the second quarter and $127 million of Visa related charges that have been incurred year-to-date. Expenses are expected to be up approximately 2%. Credit quality is trending better than expected, and we
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 10.3 | `PNC_2023_Q3_prepared_remarks_500_001` | PNC_2023_Q3 | yes |
| 9.5 | `PNC_2023_Q3_prepared_remarks_500_001` | PNC_2023_Q3 | yes |
| 30 | `FITB_2023_Q4_prepared_remarks_500_001`, `PNC_2023_Q3_prepared_remarks_500_001` | FITB_2023_Q4, PNC_2023_Q3 | yes |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 32: `ref_them_02` / `chunk500_hybrid`

- **question_id:** ref_them_02
- **condition:** chunk500_hybrid
- **category:** thematic
- **case:** C
- **current outcome label:** answered_grounded_correct

**Question:**
> How did banks characterise the uncertainty around the Basel III endgame proposal over 2023 and 2024, and how did it affect their capital actions?

**Gold anchor(s):**
> capital, while uncertainty about the Basel III Endgame prevails, our capital position remains very robust
> pace of buybacks will likely remain modest in light of the Basel III

**Generated answer, verbatim:**

```
Based on the provided context, banks characterized the uncertainty surrounding the Basel III endgame proposal as significant, disconcerting, and lacking detailed analysis to support the magnitude of proposed capital increases. They described the proposals as "overcalibrated," "conceptually flawed" (specifically regarding GSIB surcharges), and potentially procyclical. Executives noted that the absence of a fix to the GSIB clause presented an indefinite headwind and that the rules, if implemented as proposed, would negatively impact US competitiveness, increase credit costs, and shift activity to shadow banking.

Regarding capital actions, this uncertainty led banks to maintain higher-than-normal capital cushions and moderate share repurchases:
*   **JPMorgan Chase** stated that the pace of buybacks would likely remain modest in light of the proposal and indicated they would continue to reassess the buyback trajectory as circumstances evolved. They estimated the proposal could increase their Risk-Weighted Assets (RWA) by approximately 30% ($500 billion) and capital requirements by about 25% ($50 billion).
*   **Goldman Sachs** noted that they were operating at the wider end of their CET1 range to signal flexibility and address the uncertainty regarding both the quantum and timing of the Basel III endgame resolution. They maintained a prudent buffer designed to support returning capital to shareholders while accounting for lingering regulatory uncertainties, with some comments suggesting the rules might not take effect until 2025.
*   **Morgan Stanley** highlighted that there were "plenty of unknowns" and different views on the need for additional capital, noting that an extensive comment period would follow the proposal.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `JPM_2023_Q3_prepared_remarks_500_001` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
Expenses of $20.9 billion were up $1.7 billion or 9% year-on-year, primarily driven by ongoing growth and front office and technology staffing, as well as wage inflation and higher legal expense. And credit costs were $1.4 billion, predominantly driven by net charge-offs in Card, and included a $102 million net reserve release, driven by changes in the central scenario, primarily offset by card loan growth. On to balance sheet and capital on Page 3. We ended the quarter with a CET1 ratio of 14.3%, up about 50 basis points versus the prior quarter as the benefit of net income less capital distributions was partially offset by AOCI. We had $2 billion of net share repurchases this quarter and the pace of buybacks will likely remain modest in light of the Basel III endgame proposal. In line with our capital hierarchy, we will continue to reassess the buyback trajectory as circumstances evolve or opportunities emerge. And on the topic of the Basel III endgame, you'll see that we added a couple of pages on it. So, let's cover that now, starting on Page 4. Given the significance of this proposal for us, the broader industry as well as households and businesses as end-users, we thought it was important to spend time discussing it. And while we know there is interest in having us quantify the expected impact of this proposal in a lot of granular detail, it's important to start by asking why the proposed increase is so large given the repeated statement over time by policymakers that banks are well-capitalized and well-positioned to deal with stress. Given that context, the absence of detailed analysis supporting a capital increase of this magnitude is disconcerting and there's a lot that does not make sense to us. Starting with RWA, we've already said we expect the firm's RWA to increase by around 30% or $500 billion, which results in capital requirements increasing by about 25% or $50 billion. One immediate thing to point out is that at 4.5% GSIB, a $500 billion increase in RWA requires $22.5 billion of additional capital with no change in our systemic risk footprint. We've been on the record for a long time that GSIB was conceptually flawed and miscalibrated originally. Since implementation, the failure to address economic growth despite the Fed themselves acknowledging this
```

*Rank 2 -- `GS_2024_Q2_qa_500_008` -- transcript `GS_2024_Q2` -- NOT one of the question's own transcript_ids*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution. It sounds from some of Powell's latest comments that, that may not be something that comes into effect until perhaps into 2025, but we are sort of maintaining a level of cushion that think is appropriate in light of what we know and we don't know about the future opportunity set for Goldman Sachs, but that buffer is designed to support clients return capital shareholders, while maintaining a prudent buffer with some of the lingering uncertainty with respect to future regulatory input.

Steven Chubak: Helpful color. Thanks for taking my questions.

Dennis Coleman: Thank you.

Operator: We'll go next to Devin Ryan with Citizens JMP.

Devin Ryan: All right, great. Good morning, David and Dennis. A couple questions on AWM progress. So the first one is on the alts business specifically, and you're tracking obviously well ahead of the fundraising targets relative to when you set the $1 billion medium term target for annual incentive fees? And now with over $500 billion in alts AUM and obviously growing, that would seem pretty conservative. So I appreciate there's a lot of work to do to generate the returns ahead here, but how should we think about the underlying assumptions for incentive fees in a more normal harvesting environment, just given the mixed shift and the growth that you're seeing in AUM there?

Dennis Coleman: So Devin, I think it's a good question, and I think we share your expectation that, that's going
```

*Rank 3 -- `JPM_2023_Q3_prepared_remarks_500_002` -- transcript `JPM_2023_Q3` -- ONE OF the question's own transcript_ids*

```
problem at the outset has made matters worse. And now all of those problems are being applied to an additional $500 billion of RWA. Our view is that the combined proposals could have adjusted the surcharge levels to keep dollars of capital associated GSIB buffer constant rather than simply multiplying the RWA increase by the existing surcharges. Another lens on the proposed increases is the introduction of RWA for operational risk and its clear overlap with op risk losses already capitalized through the stress capital Buffer. Although there is limited disclosure from the Fed on this point, we have estimated that we have about $15 billion of operational risk capital embedded in the SCB based on the information the Fed does disclose. Once we capitalize for this new op risk RWA, our required capital will go up by around $30 billion without any change to our portfolio. Now let's turn to Page 5, which shows the impact of the actual and proposed capital rules over the last few years. Zooming out from the details of this most recent proposal, this page reminds us of what's happened since 2017. Since then, SA-CCR and the stress capital buffer have been adopted and our GSIB surcharge will increase to 4.5%. So assuming the Basel III endgame and GSIB proposals are finalized in their current form, we would see a 45% increase in our capital requirements relative to that 2017 starting point. This illustrates again how overcalibrated these proposals are and it's not done yet. We still expect the Fed to incorporate CECL into CCAR, which will likely increase the SCB. And, of course, given the absence of a fix to the GSIB clause, it continues to present a headwind into the indefinite future. And aside from those dynamics, there remains the long-standing issue of procyclicality in the overall capital [Technical Difficulty]. We think it's also important to point out that the agencies did actually have a choice here. While it may technically be true that the proposal is Basel compliant, Basel compliant does not mandate a 25% increase in capital requirements. Implementing the Basel III endgame consistently with how the Europeans have by retaining credit risk modeling and also addressing the compounding effects of GSIB and SCB would have achieved Basel compliance without creating this unnecessary increase in capital requirements. As you would expect, we will continue to engage and forcefully advocate during the comment period and beyond in a great deal of
```

*Rank 4 -- `GS_2023_Q3_prepared_remarks_500_002` -- transcript `GS_2023_Q3` -- NOT one of the question's own transcript_ids*

```
data has come in above estimates, driving market expectations of higher for longer interest rates. And there still are a number of sectors in the economy that have yet to absorb the impact of higher rates, especially in light of the further tightening in financial conditions we've seen over the last quarter. At the same time, there has been an escalation of geopolitical stresses around the globe, the [indiscernible] war in Ukraine, tensions with China and now the conflict in the Middle East. Overall levels of risk are more elevated than we've seen in quite some time. While we don't know where this will all lead, it could impact economic growth and stability in the U.S. and around the world, and we remain cautiously positioned. Before I turn it over to Denis, I'd like to spend a moment on Basel III Endgame proposal and reiterate my views on it. We, of course, support sensible regulation and the desire to ensure we have a safe and sound financial system. There are some who have recently said we need to address the lessons from the 2008 financial crisis, which is driving the needs of much higher regulations. But frankly speaking, the rules, as proposed, go way too far and do not account for the vast array of improvements made by the largest banks as a result of Dodd-Frank and other reforms. Not only have banks doubled capital over the last 15 years, have improved the quality of capital, increased liquidity, simplified businesses that have been subjected to ongoing annual stress tests. Requiring too much capital will have negative consequences. I believe if these rules are implemented, three things will happen. First, the cost of credit will go up for businesses of all sizes from large corporations to small businesses. Second, more activity will move to the unregulated shadow banking sector. Policies that incentivize a transfer of risk outside the regulated banking system could, in fact, increase systemic risk. And third, US competitiveness will go down. Our capital markets are the deepest and the most liquid in the world. They're the engine of our economy as access to capital allows for innovation and growth across the country. Our competitive standing as the leading global economy would be negatively impacted by this proposal. The net result of these proposed rules would be slower economic growth in the US, material improvement in the -- soundness of the banking system. We, alongside clients and others in the industry, have been engaging heavily
```

*Rank 5 -- `MS_2023_Q2_qa_500_000` -- transcript `MS_2023_Q2` -- NOT one of the question's own transcript_ids*

```
Operator: [Operator Instructions] We'll take our first question from Ebrahim Poonawala with Bank of America. Your line is now open. Please go ahead.

Ebrahim Poonawala: Thank you, and good morning.

James Gorman: Good morning.

Ebrahim Poonawala: I guess maybe first question, James, for you. Thanks for the update on the succession. As we think about what you built in terms of the franchise, and I think you talked about the unfolding Basel Endgame rules that are expected over the next week or two, from a shareholder perspective, do you see these rules as game-changing where investors will have to reevaluate the value proposition of Morgan Stanley as a franchise? And you, as a management team, would have to review strategic targets that you've laid out? Give us a sense. And I know plenty of unknowns. But I think the question we get from shareholders is the comfort around the ability of the firm to manage through what could be pretty radical changes.

James Gorman: Well, it's an important question. And you're right, I have made comments on it. Let's sort of set the table of where we are right now. We've had a lot of speculation based off of what the Basel III Endgame looks like. By the way, I'm not sure it's actually being implemented fully in Europe, just to say. I think the U.S. banks actually have more capital, but putting that knit aside, we did get the speech from the Vice Chair. I think it's important to look at the title of that speech, which was holistic capital review. So, it's taking into account all of the CCAR, stress tests, SCB buffers and the like as this stuff is implemented. Secondly, we haven't seen the actual rules. I mean, I guess there will be a proposal coming out, as you said, in a couple of weeks. There will be an extensive comment period. There is clearly very different views as to the need for the U.S. banking system to accrete more capital. In fact, if you look at the test of the last few years, what happened with the regional banks, what -- Silicon Valley First Republic Signature, what happened during COVID, what's happened during this period of high inflation, what's happened with the biggest rate increase
```

**Per-claim numeric trace:**

| claim | found verbatim in | transcript(s) | one of question's own transcript_ids? |
|---|---|---|---|
| 30 | `JPM_2023_Q3_prepared_remarks_500_001`, `JPM_2023_Q3_prepared_remarks_500_002` | JPM_2023_Q3 | yes |
| 500 | `JPM_2023_Q3_prepared_remarks_500_001`, `GS_2024_Q2_qa_500_008`, `JPM_2023_Q3_prepared_remarks_500_002` | GS_2024_Q2, JPM_2023_Q3 | yes |
| 25 | `JPM_2023_Q3_prepared_remarks_500_001`, `GS_2024_Q2_qa_500_008`, `JPM_2023_Q3_prepared_remarks_500_002` | GS_2024_Q2, JPM_2023_Q3 | yes |
| 50 | `JPM_2023_Q3_prepared_remarks_500_001`, `GS_2024_Q2_qa_500_008`, `JPM_2023_Q3_prepared_remarks_500_002` | GS_2024_Q2, JPM_2023_Q3 | yes |
| 1 | `JPM_2023_Q3_prepared_remarks_500_001`, `GS_2024_Q2_qa_500_008`, `JPM_2023_Q3_prepared_remarks_500_002`, `GS_2023_Q3_prepared_remarks_500_002` | GS_2023_Q3, GS_2024_Q2, JPM_2023_Q3 | yes |
| 2025 | `GS_2024_Q2_qa_500_008` | GS_2024_Q2 | no |

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

## Stratum 6 -- Case C abstentions, sample of 8 of 15 (over-conservative refusal candidates)

### Item 33: `ref_comp_06` / `chunk200_bm25`

- **question_id:** ref_comp_06
- **condition:** chunk200_bm25
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> How did Bank of America and Fifth Third each describe their operating leverage and the revenue growth behind it in the first quarter of 2023?

**Gold anchor(s):**
> our seventh straight quarter of operating leverage, led by a 13% year-over-year
> nine points of year-over-year positive operating leverage driven by an 18% increase

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `FITB_2023_Q1_prepared_remarks_200_001` -- transcript `FITB_2023_Q1` -- ONE OF the question's own transcript_ids*

```
of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide
```

*Rank 2 -- `FITB_2023_Q4_prepared_remarks_200_005` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
profitability. Expense discipline, strong returns, and positive operating leverage remain core areas of focus for Fifth Third. Supported by our technology modernization investments and a focus on leaning out key value streams, we reduced full-time equivalent employee headcount by 4% from our peak in 2023 to the end of the year without the need for a company-wide expense program. The run rate benefits of these efforts put us in a position to sustain the peer-leading annualized expense growth that we have averaged the past several years, even as we continue to invest for growth. While the carryover effect of the RWA diet makes it unfeasible for the full year, we do anticipate returning to positive operating leverage in the second half of 2024. The third point I'd like to highlight is about growth. Our strategies have been consistent, building out our Southeast markets, producing a strong fee to total revenue mix, and leveraging software that differentiates our product offerings and improves productivity
```

*Rank 3 -- `BAC_2024_Q3_prepared_remarks_200_003` -- transcript `BAC_2024_Q3` -- NOT one of the question's own transcript_ids*

```
than pre-pandemic levels. This does not surprise us what with the dramatic increase in the cost of borrowing for small and medium-sized businesses. They aren't being indolent, they want to grow. They are simply being more careful and worry a final demand will hold. Therefore, they are being cost conscious across the board. So how did Bank of America do against this backdrop? At Bank of America, our commitment to responsible growth remains unwavering, and this quarter is another illustration of that. We grew, we did it the right way. In the third quarter, Bank of America generated $25.5 billion in revenue and earned $6.9 billion in net income after tax. Year-to-date, we've generated net income of just over $20 billion. Four quarters ago, we called that a bottom would occur in our net interest income in the second quarter of 2024. Even with a rate environment that has bounced around quite a bit since we
```

*Rank 4 -- `FITB_2023_Q4_prepared_remarks_200_001` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of January 19, 2024, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Matt, and good morning everyone. At Fifth Third, we believe that great banks distinguish themselves based on how they navigate challenging and uncertain operating environment. 2023 was certainly a challenging year for the industry, but I am very pleased with how we measured up. A defensive balance sheet positioning, strong execution, and multiyear strategic investments produce top-quartile profitability, the best core deposit growth, and the best total shareholder return among all regional peers who did not participate in an FDIC-assisted transaction. We generated an all-time record full-year revenue of $8.7 billion. Deposits grew 5% compared
```

*Rank 5 -- `BAC_2023_Q2_prepared_remarks_200_010` -- transcript `BAC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
of payments through CashPro App are up 20%. As you can see, every line of business is delivering strong organic growth. Investments made in technology have enabled us to grow industry leading positions in digital tools, while enabling our clients to do great things and making us more efficient. This provides for a very satisfied, stable customer and client base with Bank of America's primary provider. And by doing with a digital application, that also produces operating leverage. On Slide 7, you can see our streak of operating leverage continued in the second quarter of 2023. We're now back in eight quarters in a row. The chart on Slide 7 covers the 8.5 years at 34 quarters, and all but eight of those quarters and you can see those identified. Six of which were in the heart of the pandemic, we've achieved operating leverage. Operating leverage is that simple task of growing revenue at a better growth rate and expense. As I said, Alastair's is
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 34: `ref_comp_08` / `chunk200_dense`

- **question_id:** ref_comp_08
- **condition:** chunk200_dense
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?

**Gold anchor(s):**
> return on tangible common equity was 17.41% and tangible book value per share increased 3%
> book value per share, excluding AOCI, increased 10% compared to the year

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `MTB_2024_Q3_prepared_remarks_200_004` -- transcript `MTB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
s look at the specifics for the third quarter. Diluted GAAP earnings per share were $4.02 for the third quarter, improved from $3.73 in the second quarter. Net income for the quarter was $721 million compared to $655 million in the linked quarter, an increase of 10%. M&T's third quarter results produced an ROA and ROCE of 1.37% and 10.26% respectively. The CET1 ratio remains strong, growing at 11.54% at the end of the third quarter and tangible book value first year grew 5%. Of note, the third quarter included a discrete tax benefit of $14 million or an $0.08 EPS benefit. Slide 8 includes supplemental reporting of M&T's results on a net operating and tangible basis. M&T's net operating income for the third quarter was $731 million compared with $665 million in the linked quarter. Diluted net operating
```

*Rank 2 -- `FITB_2024_Q1_prepared_remarks_200_001` -- transcript `FITB_2024_Q1` -- NOT one of the question's own transcript_ids*

```
presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of April 19, 2024. And Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Tim Spence: Thanks, Matt, and good morning, everyone. At Fifth Third, we believe that great banks distinguish themselves not by how they perform in benign environments, but rather by how they navigate challenging ones. In that sense, the uncertainty we face in the current environment provides us with an opportunity to demonstrate that our focus on stability, profitability and growth in that order will produce consistently strong, some might even say boring, financial results. This morning, we reported earnings per share of $0.70, or $0.76 excluding the Visa,
```

*Rank 3 -- `MTB_2023_Q3_prepared_remarks_200_005` -- transcript `MTB_2023_Q3` -- ONE OF the question's own transcript_ids*

```
98 for the third quarter, up 13% from last year’s similar quarter. Now, let’s review our net operating results for the quarter on Slide 9. M&T’s net operating income for the third quarter, which excludes intangible amortization was $702 million and diluted net operating earnings per share, was $4.05. Net operating return on tangible common equity was 17.41% and tangible book value per share increased 3% compared to the end of June. On Slide 10, you will see that diluted GAAP earnings per share, was down 21% from linked quarter. Recall our results from the second quarter of last year indicated an after-tax $157 million gain from the sales of CIT business in April. Excluding this gain, GAAP net income and diluted earnings per share were down 3% compared to the linked quarter. On a GAAP basis, M&T’s third quarter results produced an ROA and
```

*Rank 4 -- `FITB_2024_Q4_prepared_remarks_200_001` -- transcript `FITB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
in our earnings release and presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of January 21, 2025, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Tim Spence: Thanks, Matt, and good morning, everyone. At Fifth Third, we believe great banks distinguish themselves not by how they perform in benign environments, but rather by how they navigate uncertain ones. They achieved this through a diversified business mix, defensive balance sheet positioning, and by obsessing over the details in day-to-day operations while investing for the long-term. This morning, we reported earnings per share of $0.85 or $0.90, excluding certain items outlined on Page 2 of the
```

*Rank 5 -- `MTB_2024_Q4_prepared_remarks_200_006` -- transcript `MTB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
growing to 11.67% at the end of the fourth quarter and tangible book value per share grew 1%. The fourth quarter included several notable items, a securities gain of $18 million or $0.08 per share related to the sale of noncore investments, expense associated with redemption of certain M&T trust preferred obligations amounting to $20 million or $0.09 per share. This action has a three-year earn back. Corporate real estate optimization related to expenses amounting to $27 million or $0.12 per share and a pension-related credit within expenses amounting to $12 million or $0.05 per share benefit. Slide 10 includes supplemental reporting of M&T's results on net operating or tangible basis. M&T's net operating income for the fourth quarter was $691 million compared to $731 million in the linked quarter. Diluted net operating earnings per share were $3.92 for the recent quarter, down from $
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 35: `ref_comp_11` / `chunk200_hybrid`

- **question_id:** ref_comp_11
- **condition:** chunk200_hybrid
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> What drove the fall in BNY Mellon's reported expenses and M&T's non-interest expenses in the third quarter of 2023?

**Gold anchor(s):**
> a reported basis, primarily reflecting the goodwill impairment associated with our investment management reporting unit
> $1.28 billion in the third quarter of this year, down $15 million

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `MTB_2023_Q1_prepared_remarks_200_020` -- transcript `MTB_2023_Q1` -- NOT one of the question's own transcript_ids*

```
the sale of the M&T Insurance Agency in the fourth quarter of 2022 as well as securities losses, net interest income -- sorry, noninterest income was $2.23 billion in 2022. We expect 2023 noninterest income growth to be in the 7% to 9% range compared to the $2.23 billion in 2022. This outlook for noninterest income includes the impact of a bulk purchase of residential mortgage servicing rights that we completed at the end of this year's first quarter. Turning to expenses. We anticipate expenses, excluding merger-related costs, the charitable contribution and intangible amortization to be up 11% to 13% when compared to the $4.52 billion during 2022. Recall that approximately half of this increase reflects an extra quarter of People's United expenses. In addition, this outlook for net operating expenses includes the impact of the previously noted mortgage servicing rights purchase. We do not anti
```

*Rank 2 -- `BK_2023_Q2_prepared_remarks_200_003` -- transcript `BK_2023_Q2` -- NOT one of the question's own transcript_ids*

```
m proud of our people who are embracing the task of making BNY Mellon a more efficient and scalable company, which gives me confidence in our ability to deliver tangible results in 2023 and beyond. Remember, in January, we committed to essentially cut expense growth in half this year, roughly 4% growth excluding notable items in 2023, compared to roughly 8% ex currency in 2022. Halfway through the year, I'm pleased to report that we're on track even a little ahead of our plans. Second, the strength of our balance sheet, the resiliency of our business model, and our proactive balance sheet management continue to differentiate us with clients and create value for our shareholders. Net interest, revenue and deposits were both bright spots in the quarter. And the Federal Reserve's 2023 bank stress test demonstrated our capacity to withstand an extreme stress scenario. As a result of the test, our preliminary stress capital buffer requirement remains at the regulatory floor of 2.5%
```

*Rank 3 -- `MTB_2023_Q3_prepared_remarks_200_010` -- transcript `MTB_2023_Q3` -- ONE OF the question's own transcript_ids*

```
-interest income. Please turn to Slide 16. Non-interest income totaled $560 million in the third quarter compared to $803 million in the linked quarter. As noted earlier, the second quarter included $225 million from the sale of the CIT business. Excluding this gain, third quarter non-interest income decreased $18 million compared to the second quarter driven predominantly by $15 million related to one month of the CIT trust revenues included in the previous quarter. Other revenues categories were largely unchanged from the linked quarter. Turning to Slide 17 for expenses. Non-interest expenses were $1.28 billion in the third quarter of this year, down $15 million from the linked quarter. That decrease in expense was due to $11 million in lower compensation and benefit costs, reflecting lower average headcount, lower expenses for contracted resources and over time. $6 million lower in other cost of operations, largely reflecting lower sub-advisory fees as a result of the sale of the CIT business
```

*Rank 4 -- `BK_2023_Q3_prepared_remarks_200_002` -- transcript `BK_2023_Q3` -- ONE OF the question's own transcript_ids*

```
continue to deliver uninterrupted service to our clients. Our hearts go out to colleagues, clients, and community members in the region. Now I'll share some brief comments about our financial results for the third quarter and we'll then give a quick overview of some of our strategic priorities. BNY Mellon delivered solid financial performance and continued progress on the steady transformation of our company. As you can see on Slide 2 of the financial highlights presentation, we reported earnings per share of $1.22 versus $0.39 in the third quarter of last year. Excluding notable items, which primarily impacted last year's results, EPS of $1.27 increased by 5% year-over-year. We generated a return on tangible common equity of 20% on $4.4 billion of revenue, up 2% year-over-year and a pre-tax margin of 29% in the third quarter. These results once again highlight the efficacy of our prudent and pro
```

*Rank 5 -- `PNC_2024_Q4_prepared_remarks_200_011` -- transcript `PNC_2024_Q4` -- NOT one of the question's own transcript_ids*

```
third quarter activity. Card and cash management fees were stable as higher Treasury management revenue was offset by credit card origination incentives. Lending and deposit services revenue grew $10 million, or 3%, due to increased customer activity. Mortgage revenue declined $59 million linked quarter, primarily due to elevated [RMSR] (ph) hedge gains in the third quarter. And our other noninterest income increased $106 million, reflecting a less negative impact from Visa derivative activity. Turning to Slide 10. Full year non-interest expense decreased by $488 million or 3%. Core non-interest expense was down $152 million or 1% compared to 2023. As a result, we generated positive operating leverage on a reported basis, as well as adjusted for non-core expenses. Fourth quarter non-interest expense of $3.5 billion increased $179 million or 5%. As I mentioned, the quarter included $79 million of non-core expenses, which reflected $97 million of
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 36: `ref_comp_08` / `chunk200_hybrid`

- **question_id:** ref_comp_08
- **condition:** chunk200_hybrid
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?

**Gold anchor(s):**
> return on tangible common equity was 17.41% and tangible book value per share increased 3%
> book value per share, excluding AOCI, increased 10% compared to the year

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `MTB_2024_Q3_prepared_remarks_200_004` -- transcript `MTB_2024_Q3` -- NOT one of the question's own transcript_ids*

```
s look at the specifics for the third quarter. Diluted GAAP earnings per share were $4.02 for the third quarter, improved from $3.73 in the second quarter. Net income for the quarter was $721 million compared to $655 million in the linked quarter, an increase of 10%. M&T's third quarter results produced an ROA and ROCE of 1.37% and 10.26% respectively. The CET1 ratio remains strong, growing at 11.54% at the end of the third quarter and tangible book value first year grew 5%. Of note, the third quarter included a discrete tax benefit of $14 million or an $0.08 EPS benefit. Slide 8 includes supplemental reporting of M&T's results on a net operating and tangible basis. M&T's net operating income for the third quarter was $731 million compared with $665 million in the linked quarter. Diluted net operating
```

*Rank 2 -- `MTB_2023_Q3_prepared_remarks_200_005` -- transcript `MTB_2023_Q3` -- ONE OF the question's own transcript_ids*

```
98 for the third quarter, up 13% from last year’s similar quarter. Now, let’s review our net operating results for the quarter on Slide 9. M&T’s net operating income for the third quarter, which excludes intangible amortization was $702 million and diluted net operating earnings per share, was $4.05. Net operating return on tangible common equity was 17.41% and tangible book value per share increased 3% compared to the end of June. On Slide 10, you will see that diluted GAAP earnings per share, was down 21% from linked quarter. Recall our results from the second quarter of last year indicated an after-tax $157 million gain from the sales of CIT business in April. Excluding this gain, GAAP net income and diluted earnings per share were down 3% compared to the linked quarter. On a GAAP basis, M&T’s third quarter results produced an ROA and
```

*Rank 3 -- `MTB_2024_Q4_prepared_remarks_200_006` -- transcript `MTB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
growing to 11.67% at the end of the fourth quarter and tangible book value per share grew 1%. The fourth quarter included several notable items, a securities gain of $18 million or $0.08 per share related to the sale of noncore investments, expense associated with redemption of certain M&T trust preferred obligations amounting to $20 million or $0.09 per share. This action has a three-year earn back. Corporate real estate optimization related to expenses amounting to $27 million or $0.12 per share and a pension-related credit within expenses amounting to $12 million or $0.05 per share benefit. Slide 10 includes supplemental reporting of M&T's results on net operating or tangible basis. M&T's net operating income for the fourth quarter was $691 million compared to $731 million in the linked quarter. Diluted net operating earnings per share were $3.92 for the recent quarter, down from $
```

*Rank 4 -- `FITB_2024_Q1_prepared_remarks_200_001` -- transcript `FITB_2024_Q1` -- NOT one of the question's own transcript_ids*

```
presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of April 19, 2024. And Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Tim Spence: Thanks, Matt, and good morning, everyone. At Fifth Third, we believe that great banks distinguish themselves not by how they perform in benign environments, but rather by how they navigate challenging ones. In that sense, the uncertainty we face in the current environment provides us with an opportunity to demonstrate that our focus on stability, profitability and growth in that order will produce consistently strong, some might even say boring, financial results. This morning, we reported earnings per share of $0.70, or $0.76 excluding the Visa,
```

*Rank 5 -- `FITB_2024_Q4_prepared_remarks_200_001` -- transcript `FITB_2024_Q4` -- NOT one of the question's own transcript_ids*

```
in our earnings release and presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of January 21, 2025, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Tim Spence: Thanks, Matt, and good morning, everyone. At Fifth Third, we believe great banks distinguish themselves not by how they perform in benign environments, but rather by how they navigate uncertain ones. They achieved this through a diversified business mix, defensive balance sheet positioning, and by obsessing over the details in day-to-day operations while investing for the long-term. This morning, we reported earnings per share of $0.85 or $0.90, excluding certain items outlined on Page 2 of the
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 37: `ref_comp_02` / `chunk500_bm25`

- **question_id:** ref_comp_02
- **condition:** chunk500_bm25
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> How did Bank of America's and Huntington's positions on office real estate exposure differ in the first quarter of 2024, in charge-offs and in portfolio reduction?

**Gold anchor(s):**
> charge-offs increased $191 million versus the fourth quarter, driven by commercial real estate losses
> the office portfolio by about $500 million over the course of the last

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BAC_2023_Q2_prepared_remarks_500_012` -- transcript `BAC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
to 213,000. That's some good work after peaking at 218,000 in January. Our summer interns will leave us in the third quarter, and hopefully many will return as full-time associates next summer. And at the same time in Q3, we welcomed back about 2,600 new full-time hires as college grads, many of whom interned with us last summer. And that's a very diverse class of associates who are excited to join the company. As we look forward to next quarter, we would expect the third quarter expense to more fully benefit from the second quarter head count reduction, even as we remain in a mode of modest hiring for client-facing positions. Additionally, the proposed notice of special assessment from the FDIC to recover losses from the failures of Silicon Valley and signature banks could add $1.9 billion expense for us, $1.5 billion after tax, and we just remain unsure at this point of timing to record that expense. Let's now move to credit, and we'll turn to Slide 17. Net charge-offs of $869 million increased $62 million from the first quarter, and the increase was driven by credit card losses as higher late-stage delinquencies flowed through to charge-offs. For context, the credit card net charge-off rate was 2.6% in Q2, and remains well below the 3.03% pre-pandemic rate in the fourth quarter of '19. Provision expense was $1.1 billion in Q2, and that included a $256 million further reserve build, that's driven by loan growth, particularly in credit card, and it reflects a macroeconomic outlook that on a weighted basis continues to include an unemployment rate that rises to north of 5% in 2024. On Slide 18, we highlight the credit quality metrics for both our consumer and commercial portfolios. On consumer, we note we continue to see asset quality metrics come off the bottom, and they remain below historical averages. Overall commercial net charge-offs were flat from first quarter. And within commercial we saw a decrease in C&I losses that was offset by an increase in charge-offs related to commercial real estate office exposures. As a reminder, commercial real estate office credit exposure represents less than 2% of our total loans, and this is an area where we've been quite intentional around our client selection, portfolio concentration, and deal structure over many
```

*Rank 2 -- `BAC_2024_Q1_prepared_remarks_500_009` -- transcript `BAC_2024_Q1` -- ONE OF the question's own transcript_ids*

```
306 million from the fourth quarter, driven by continued credit card seasoning and commercial real estate office exposures as swift revaluations from current appraisals and resolutions drove higher charge-offs. The net charge-off ratio was 58 basis points, a 13 basis point increase from the fourth quarter. On Slide 12, we show you the credit quality metrics for both our consumer and commercial portfolios. Consumer net charge-offs increased $150 million versus the fourth quarter from the flow-through of higher late stage credit card delinquencies. We included a credit card delinquency slide, No. 28 in our appendix, and we’re encouraged by the trend of delinquencies because the late stage increases slowed and early stage delinquencies improved as well, and that leads us to believe we should begin to see consumer net charge-offs start to level out over the next quarter or so. All of this is still well within our risk appetite and our expectations, and it’s consistent with the normalization of credit we discussed with you in prior calls. Commercial net charge-offs increased $191 million versus the fourth quarter, driven by commercial real estate losses and office exposures. On office losses this quarter, we recorded charge-offs on 16 office loans. Four were a result of sales activity, i.e. final resolution, seven were from losses that we expect on exposures that are in the process of expected resolution in the course of the next 90 days, and the rest we took as a result of refreshed valuations. We use a continuous and thorough loan-by-loan analysis and we’re quick to recognize impacts in the commercial real estate office space through our risk ratings, and that’s resulted in several downgrades in the last few quarters. As a result of these quick actions and our downgrades in categorization, we’ve also refreshed the valuation of our reservable criticized properties, and we’ve taken appropriate reserves and charge-offs in the process. Roughly one-third of our office exposure is now categorized as reservable criticized, and importantly the pace of the increase in reservable criticized exposures has slowed each quarter since the second quarter of last year, so we believe the losses on these office properties have been front-loaded and largely reserved. We expect the losses to move lower in the second quarter and we expect a notable decline in the second half of the year
```

*Rank 3 -- `WFC_2023_Q2_prepared_remarks_500_004` -- transcript `WFC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
expect to repurchase more common stock this year, we believe continuing to maintain significant excess capital is appropriate until there's more clarity on the new capital requirements that Charlie highlighted. Our liquidity position remained strong in the second quarter with our liquidity coverage ratio approximately 23 percentage points above the regulatory minimum. Turning to credit quality on Slide 5. Overall credit quality remained strong, but as expected, net loan charge-offs continued to increase from historically low levels and were 32 basis points of average loans in the second quarter. Commercial net loan charge offs increased $137 million from the first quarter to 15 basis points of average loans. Approximately half of the increase was in commercial banking where the losses were borrower-specific with little signs of systematic weakness across the portfolio. The rest of the increase was driven by higher losses in commercial real estate, primarily in the office portfolio. I'll share some more details on the CRE office exposure on the next slide. Consumer net loan charge-offs increased modestly, up $23 million from the first quarter to 58 basis points of average loans. The increase primarily came from the credit card portfolio as residential mortgage loans continue to have net recoveries and auto losses declined. While consumer credit performance remained solid overall, and we’ve continued to take incremental credit tightening actions across the portfolios, we expect consumer net loan charge-offs will continue to gradually increase. Non-performing assets increased 14% from the first quarter as lower non-accrual loans across the consumer portfolios were more than offset by higher commercial non-accrual loans, primarily in the commercial real estate portfolio. Our allowance for credit losses increased $949 million in the second quarter, primarily from -- for commercial real estate office loans as well as for higher credit card balances. We've updated Slide 6, which highlights our commercial real estate portfolio. We had $154.3 billion of commercial real estate loans outstanding at the end of the second quarter with $33.1 billion of office loans, which were down modestly from the first quarter and represented 3% of our total loans outstanding. The office market continues to be weak and the composition of our office portfolio was relatively consistent with what we shared with you in the first quarter. As Charlie mentioned, our CRE teams are focused on surveillance and de-risking which includes reducing exposures and closely monitoring at-risk loans. This quarter, we added a table to this slide that breaks down our CRE office
```

*Rank 4 -- `PNC_2024_Q1_prepared_remarks_500_005` -- transcript `PNC_2024_Q1` -- NOT one of the question's own transcript_ids*

```
on Slide 11. While overall credit quality remains resilient, the pressure we anticipated within the commercial real estate office sector has continued. Non-performing loans increased $200 million or 9% linked quarter, almost entirely driven by commercial real estate, which increased $188 million. And inside of that, approximately $150 million was related to the CRE office portfolio. Total delinquencies of $1.3 billion decreased $109 million or 8% linked quarter, driven by lower consumer and commercial delinquencies. Net loan charge-offs were $243 million in the first quarter, and our annualized net charge-offs to average loans ratio was 30 basis points. Our allowance for credit losses totaled $5.4 billion or 1.7% of total loans on March 31, stable with December 31. Slide 12 provides more detail on our CRE office credit metrics. While NPLs have increased over the past few quarters, our criticized balances have remained relatively consistent. The migration of criticized loans to non-performing status is an expected outcome as we work to resolve the occupancy and rate challenges inherent to this portfolio. In the first quarter, net loan charge-offs within the CRE office portfolio were $50 million, essentially in line with the previous quarter level. Ultimately, we expect continued charge-offs on this portfolio, and accordingly we believe we are adequately reserved. As of March 31, our reserves on the office portfolio were 9.7% of total office loans and inside of that, 14.4% on the multitenant portfolio. Importantly, we continue to manage our exposure down and as a result, our balances declined 3%, or approximately $200 million linked quarter. In summary, PNC reported a solid first quarter 2024, and we're well positioned for the remainder of the year. Regarding our view of the overall economy, we're expecting economic expansion in the second half of the year, resulting in real GDP growth of approximately 2% in 2024, and unemployment to increase modestly to 4% by year end. We expect the Fed to cut rates 2 times in 2024, with a 25 basis point decrease in July and another in November. Looking at the second quarter of 2024 compared to the first quarter of 2024, we expect average loans to be stable, net interest income to be down approximately 1%. And as I mentioned previously, we expect NII and net interest margin to trough in the second
```

*Rank 5 -- `BAC_2024_Q2_prepared_remarks_500_005` -- transcript `BAC_2024_Q2` -- NOT one of the question's own transcript_ids*

```
-pandemic levels, even while our card customers have plenty of capacity to borrow. And importantly, because we're relation-based businesses, look at the right-hand slide at the bottom of page five. There you can see our deposit investment balances of our customers, who also have a card with us, remain 25% above their pre-pandemic levels, illustrating continued health of these customers. So if you think about consumer credit, the card charge-offs drive it, and they flattened out in terms of delinquencies, and we expect an improvement in the second-half. With regard to commercial real estate, our usual CRA credit exposure slide is included in our appendix. We continue to aggressively work through our loans in our modest CRA office portfolio. We saw a decrease in all the categories, a decrease in reservable criticized loans, a decrease in NPLs, and a decrease in net charge-offs. This supports our previous expectation that net charge-offs in the second-half of 2024 will be lower than the first-half of 2024. Our second quarter performance highlights Bank of America's ability to generate strong, sustainable growth through a combination of customer-centric strategies, innovation, strategic investments, and a commitment to a strong balance of risk and reward. We call that responsible growth. We're confident that focused approach will continue to drive long-term success and create value for you, our shareholders. Now I will turn it to Alistair for additional results.

Alastair Borthwick: Thank you, Brian, and I'm going to start on slide six of the earnings presentation. I'll touch on more highlights noted on slide six as we work through the material. I just want to say upfront that we delivered strong returns with return on average assets of 85 basis points and a return on tangible common equity of nearly 14%. So let's move to the balance sheet on slide seven, where you can see we ended the quarter at $3.26 trillion of total assets, relatively unchanged from the first quarter. And not much to note here apart from a mixed shift of lower securities balances, mostly offset by an increase in reverse repo and modest loan growth, as well as global markets client activity. On the funding side, deposits declined $36 billion on an ending basis, reflecting typical seasonal customer payments of income taxes. And as Brian noted, average deposits were still modestly higher. Liquid
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 38: `ref_comp_11` / `chunk500_dense`

- **question_id:** ref_comp_11
- **condition:** chunk500_dense
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> What drove the fall in BNY Mellon's reported expenses and M&T's non-interest expenses in the third quarter of 2023?

**Gold anchor(s):**
> a reported basis, primarily reflecting the goodwill impairment associated with our investment management reporting unit
> $1.28 billion in the third quarter of this year, down $15 million

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `MTB_2023_Q1_prepared_remarks_500_008` -- transcript `MTB_2023_Q1` -- NOT one of the question's own transcript_ids*

```
the sale of the M&T Insurance Agency in the fourth quarter of 2022 as well as securities losses, net interest income -- sorry, noninterest income was $2.23 billion in 2022. We expect 2023 noninterest income growth to be in the 7% to 9% range compared to the $2.23 billion in 2022. This outlook for noninterest income includes the impact of a bulk purchase of residential mortgage servicing rights that we completed at the end of this year's first quarter. Turning to expenses. We anticipate expenses, excluding merger-related costs, the charitable contribution and intangible amortization to be up 11% to 13% when compared to the $4.52 billion during 2022. Recall that approximately half of this increase reflects an extra quarter of People's United expenses. In addition, this outlook for net operating expenses includes the impact of the previously noted mortgage servicing rights purchase. We do not anticipate incurring any material merger-related costs in 2023 and intangible amortization is expected to be in the $60 million to $65 million range during 2023. Turning to credit. We expect credit losses to migrate towards M&T's long-term average of 33 basis points, although the quarterly cadence could be lumpy. Provision expense over the year will follow the CECL methodology and will be affected by changes in the macroeconomic outlook as well as loan balances. For 2023, we expect the taxable equivalent tax rate to be in the 25% range. Finally, turning to capital. M&T's common equity Tier 1 ratio of 10.15% at March 31, 2023, comfortably exceeds the required regulatory minimum threshold, which takes into account our stress capital buffer or SCB. We believe the current level of core capital exceeds that needed to safely run the company and to support lending in our communities. We plan to return excess capital to shareholders at a measured pace over the long term. However, in the near term, we plan to maintain a CET1 ratio slightly above the current level until the current economic uncertainty abates. With that, let's open up the call to questions before which Shelby will briefly review the instructions.
```

*Rank 2 -- `PNC_2023_Q3_prepared_remarks_500_003` -- transcript `PNC_2023_Q3` -- NOT one of the question's own transcript_ids*

```
revenue of $5.2 billion decreased $60 million, or 1%, compared to the second quarter of 2023. Net interest income declined $92 million, or 3%. And our net interest margin was 2.71%, a decline of 8 basis points. Noninterest income increased $32 million, or 2%, as higher fee income was partially offset by lower other noninterest income. Third quarter expenses decreased $127 million, or 4% linked quarter. Provision was $129 million in the third quarter. And our effective tax rate was 15.5%, which included a favorable impact of certain tax matters in the third quarter. For the full year, we now expect our tax rate to be approximately 16.5%. Turning to Slide 8, we highlight our revenue trends. Third quarter revenue was down $60 million, or 1%, compared with the second quarter. Net interest income of $3.4 billion decreased $92 million or 3%, as higher yields on interest earning assets were more than offset by increased funding costs. Fee income was $1.7 billion and increased $67 million or 4% linked quarter. The primary driver of the increase in fee income was residential and commercial mortgage revenue, which was up $103 million, the majority of which, or $97 million, was related to an increase in the valuation of net mortgage servicing rights. Partially offsetting this, capital markets and advisory revenue decreased $45 million, or 21%, driven by lower trading revenue. M&A advisory activity continued to remain softer in the third quarter despite robust pipelines. Going forward, we do expect this activity to increase in the fourth quarter, which is included in our guidance that I will cover in a few minutes. Other noninterest income of $94 million declined $35 million linked quarter, driven by lower private equity revenue and included negative Visa fair value adjustments totaling $51 million. As a reminder, at September 30, PNC owned 3.5 million Visa Class B shares with an unrecognized gain of approximately $1.3 billion. Turning to Slide 9, our third quarter expenses were down $127 million or 4% linked quarter, which in part reflected our increased CIP program. And we generated 3% positive operating leverage on both the year-to-date and the linked-quarter basis. Importantly, every expense category remained stable or declined compared to the second quarter of 2023. Our credit metrics
```

*Rank 3 -- `MTB_2023_Q3_prepared_remarks_500_004` -- transcript `MTB_2023_Q3` -- ONE OF the question's own transcript_ids*

```
-interest income. Please turn to Slide 16. Non-interest income totaled $560 million in the third quarter compared to $803 million in the linked quarter. As noted earlier, the second quarter included $225 million from the sale of the CIT business. Excluding this gain, third quarter non-interest income decreased $18 million compared to the second quarter driven predominantly by $15 million related to one month of the CIT trust revenues included in the previous quarter. Other revenues categories were largely unchanged from the linked quarter. Turning to Slide 17 for expenses. Non-interest expenses were $1.28 billion in the third quarter of this year, down $15 million from the linked quarter. That decrease in expense was due to $11 million in lower compensation and benefit costs, reflecting lower average headcount, lower expenses for contracted resources and over time. $6 million lower in other cost of operations, largely reflecting lower sub-advisory fees as a result of the sale of the CIT business, lower legal-related expenses partially offset by losses associated with certain retail banking activities. The efficiency ratio, which excludes intangible amortization and merger-related expenses from the numerator and security gains or losses from a denominator, was 53.7% in the recent quarter compared to 53.4% in the linked quarter after excluding the gain from the sale of the CIT business. Next, let’s turn to Slide 18 for credit. The allowance for credit losses amounted to $2.1 billion at the end of the third quarter, up $54 million from the end of the linked quarter. In the third quarter, we recorded a $150 million provision in credit losses, which was equal to the second quarter. Net charge-offs were $96 million in the third quarter compared to $127 million in the linked quarter. The reserve build was primarily reflective of softening CRE values and the variability in the timing and the amount of CRE charge-offs. At the end of the third quarter, non-accrual loans were $2.3 billion, a decrease of $94 million compared to the prior quarter and represent 1.77% of loans, down 6 basis points sequentially. As noted, net charge-offs for the recent quarter amounted to $96 million, significant charge-offs were tied in 4 large credits, 3 large office buildings in Washington, D.C., Boston and Connecticut and one large healthcare provider operating in multiple
```

*Rank 4 -- `FITB_2023_Q2_prepared_remarks_500_007` -- transcript `FITB_2023_Q2` -- NOT one of the question's own transcript_ids*

```
in 2023. Our outlook translates to total interest-bearing deposit costs increasing around 40 basis points in the third quarter and another 15 basis points or so in the fourth quarter. Our guidance assumes that our securities portfolio balances remained relatively stable between now and year-end. As a byproduct of strong deposit growth, combined with lower loan growth and stable securities balances, we expect to hold closer to $15 billion in cash and cash equivalents by year-end. We expect our loan-to-core deposit ratio to end the year in the mid-70s area. It will keep Fifth Third in a strong liquidity position in anticipation of more stringent regulatory environments. We expect third quarter NII to be down approximately 2% to 3% sequentially due to the continued impacts of the balance sheet dynamics I mentioned. We expect adjusted noninterest income to be stable in 2023, resulting from continued success, increasing market share due to our investments in talent and capabilities. with stronger gross treasury management, capital markets, wealth and asset management and mortgage servicing revenue to be offset by higher earnings credit rates on treasury management, subdued leasing remarketing revenue and a reduction in other fees due to lower TRA and private equity income this year. We expect our fourth quarter TRA revenue to decline from $46 million in 2022 to $22 million in 2023. We expect third quarter adjusted noninterest income to be down 3% to 4% compared to the second quarter. We expect to continue generating strong revenue across most fee captions, which we conservatively assume will be more than offset by a slight erosion in debt capital markets and mortgage revenue. reflecting the environmental headwinds as well as lower other noninterest income. We continue to expect full year adjusted noninterest expenses to be up 4% to 5% compared to 2022. If capital markets fees improve relative to our current expectations, we will likely land at the upper end of the range. Our expense outlook incorporates the FDIC insurance assessment rate change that went into effect on January 1, the mark-to-market impact on nonqualified deferred compensation plans which was a reductant in 2022 expenses but an increase in 2023 and full year impact of investments to grow the dividend finance and provide businesses. Excluding the FDIC assessment and NQDC impacts, we would expect our full year 2023 core expenses to be up 3%. Our guidance reflects continued
```

*Rank 5 -- `STT_2023_Q2_prepared_remarks_500_010` -- transcript `STT_2023_Q2` -- NOT one of the question's own transcript_ids*

```
also include a revenue headwind from the previously disclosed client exit. We expect management fees to be up around 0.5% to 1.5%. We expect front office software and data quarter-on-quarter to be down 7%, as we do not expect the level of on-premise renewals in 3Q that we saw this quarter. We expect the other fee revenue line to come in around $30 million to $35 million in 3Q which is higher than prior years but down post the accounting change impact in 2Q. Regarding NII, after three double-digit sequential increases in NII last year, we now expect NII to decrease 12% to 18% on a sequential-quarter basis, driven by lower deposit levels and continued rotation as rate hikes continue into 3Q. Our outlook assumes that average non-interest-bearing deposits declined by approximately $5 billion from 2Q to 3Q. As we look forward to 4Q, we do expect to see some moderation to the amount of deposit rotation as we work through most of our back-book and most central banks begin to pause. With that context, we expect that 4Q NII decline to be much less somewhere in the range of down 2% to 6% versus 3Q, and we expect NII to then stabilize around those levels, but it will depend on market conditions. And our expectation is that 4Q declines in non-interest-bearing deposits will be small as well likely in the down to a $3 billion range versus 3Q. Turning to expenses, we remain focused on controlling costs in this environment, and we expect to take action in 3Q to bend the cost curve. As such, we expect that expenses will be down 0.5% to 1% on a sequential-quarter basis and intend to continue to actively manage expenses. As always, this is on an ex-notables basis and we're keeping an eye on the FDIC assessment, which could be a 3Q notable item. And as I noted previously, given the accounting changes we adopted this quarter, we expect our effective tax rate to be between 21% and 22% for third quarter. With that let me hand the call back to Ron.

Ronald P. O'Hanley: Thanks, Eric. Operator, we can now open the call for questions.
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 39: `ref_comp_06` / `chunk500_dense`

- **question_id:** ref_comp_06
- **condition:** chunk500_dense
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> How did Bank of America and Fifth Third each describe their operating leverage and the revenue growth behind it in the first quarter of 2023?

**Gold anchor(s):**
> our seventh straight quarter of operating leverage, led by a 13% year-over-year
> nine points of year-over-year positive operating leverage driven by an 18% increase

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BAC_2023_Q4_prepared_remarks_500_002` -- transcript `BAC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 2 -- `FITB_2023_Q1_prepared_remarks_500_000` -- transcript `FITB_2023_Q1` -- ONE OF the question's own transcript_ids*

```
Chris Doll: Good morning everyone. Welcome to Fifth Third’s First Quarter 2023 Earnings Call. This morning our President and CEO, Tim Spence and CFO, Jamie Leonard will provide an overview of our first quarter results and outlook. Our Treasurer, Bryan Preston has also joined for the Q&A portion of the call. Please review the cautionary statements and our materials which can be found on our earnings release and presentation. These materials contain information regarding to the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third’s performance. These statements speak only as of April 20th 2023 and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris. And good morning, everyone. Thank you for joining us today. The past six weeks have seen a great deal of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide impact of quantitative tightening and normal seasonal pressures. Our key credit metrics remain near historical lows with net charge-offs of 26 basis points coming in at the low end of our guidance range. NPAs NPLs and early stage delinquency ratios remained below normalized levels, and criticized assets decrease modestly during the quarter. Moreover, we accomplished all this while also being recognized by Ethisphere as one of only two U.S. banks on their world's most ethical companies
```

*Rank 3 -- `FITB_2023_Q4_prepared_remarks_500_002` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
profitability. Expense discipline, strong returns, and positive operating leverage remain core areas of focus for Fifth Third. Supported by our technology modernization investments and a focus on leaning out key value streams, we reduced full-time equivalent employee headcount by 4% from our peak in 2023 to the end of the year without the need for a company-wide expense program. The run rate benefits of these efforts put us in a position to sustain the peer-leading annualized expense growth that we have averaged the past several years, even as we continue to invest for growth. While the carryover effect of the RWA diet makes it unfeasible for the full year, we do anticipate returning to positive operating leverage in the second half of 2024. The third point I'd like to highlight is about growth. Our strategies have been consistent, building out our Southeast markets, producing a strong fee to total revenue mix, and leveraging software that differentiates our product offerings and improves productivity. These are multi-year investments that cannot be replicated easily by competitors to one to two years of hiring a few new branches or small tuck-in acquisitions. In 2023, we opened 37 new branches concentrated in the Southeast, bringing us to 107 opened over the past five years. We plan to open another 31 branches in the Southeast in 2024. As a portfolio, these branches have continued to outperform our expectations on both household acquisition and deposit growth and should provide a tailwind for several years forward. We also continue to invest in treasury management, wealth and asset management, and capital markets. All three of these businesses grew for us in 2023. We expect mid-to-high single-digit growth in each in 2024. In treasury management, our acquisitions of Rize and Big Data Healthcare and the launch of Newline, our embedded payments business, should continue to support peer-leading performance. In wealth and asset management, Global Finance recently named our Private Bank as the Best US Regional Private Bank for the fifth consecutive year and Best Private Bank for Entrepreneurs globally for the first time. In our capital markets business, we have seen more robust activity levels to start the year, including an M&A pipeline that is 1.5 times the full-year revenue target embedded in our guidance. Overall, we expect 2024 to be a solid year of improving revenue trends and continued to expense discipline. Given what we believe to be a less certain outlook than the markets would imply,
```

*Rank 4 -- `FITB_2023_Q4_prepared_remarks_500_000` -- transcript `FITB_2023_Q4` -- NOT one of the question's own transcript_ids*

```
Operator: Hello and welcome to the Q4 2023 Fifth Third Bancorp Earnings Conference Call. All lines have been placed on mute to prevent any background noise. After the speakers' remarks, there will be a question-and-answer session. [Operator Instructions] I'll now turn the conference over to Matt Curoe, Director of Investor Relations. Please go ahead.

Matt Curoe: Good morning, everyone, and welcome to the Fifth Third's Fourth Quarter 2023 Earnings Call. This morning our Chairman, President, and CEO, Tim Spence; and CFO, Bryan Preston will provide an overview of our fourth quarter results and outlook; our Chief Operating Officer, Jamie Leonard and Chief Credit Officer, Greg Schroeck have also joined for the Q&A portion of the call. Please review the cautionary statements in our materials, which can be found in our earnings release and presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of January 19, 2024, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Matt, and good morning everyone. At Fifth Third, we believe that great banks distinguish themselves based on how they navigate challenging and uncertain operating environment. 2023 was certainly a challenging year for the industry, but I am very pleased with how we measured up. A defensive balance sheet positioning, strong execution, and multiyear strategic investments produce top-quartile profitability, the best core deposit growth, and the best total shareholder return among all regional peers who did not participate in an FDIC-assisted transaction. We generated an all-time record full-year revenue of $8.7 billion. Deposits grew 5% compared to an industry-wide decline of 3%. Credit performance was strong with net charge-offs remaining below historical averages. And although it would be foolish to expect it to repeat forever, in commercial real estate we experienced zero net charge-offs in 2023 and only two basis points in delinquent loans as of early January. These strong outcomes combined with our multi-year expense discipline produced a full-year adjusted return on assets of 1.25% and adjusted return on tangible common equity ex-
```

*Rank 5 -- `FITB_2023_Q3_prepared_remarks_500_001` -- transcript `FITB_2023_Q3` -- NOT one of the question's own transcript_ids*

```
among peers, despite also investing in growth by building more new branches, raising our minimum wage, modernizing our technology platforms, and acquiring four fintech companies. Expense management at Fifth Third is a continuous process and not a program. Since March of this year, full-time equivalent employee headcount is down 3.5%.  Turning to the balance sheet, we generated 4% average deposit growth compared to the year ago quarter versus a 5% decline for the industry. New relationship growth remains strong. Consumer households grew more than 2%, led by 6% growth in the Southeast, a continuation of our multi-year growth base. New middle market relationships added year-to-date remain 25% ahead of last year's record base.  Thanks to the release of the annual FDIC summary of deposits, the third quarter provides a unique opportunity to understand market share gains and losses on a metro area by metro area basis. This year, Fifth Third maintained or improved our market rank in every single one of our 40 largest MSAs.  In the Midwest, we maintained our #2 overall position behind JPMorgan Chase. In the Southeast, where we are just 4 years removed for opening our first next-gen branch, we have reached or are approaching target locational share in 8 of our original 11 focused markets. We intend to continue to open approximately 35 branches per year through 2028, at which time nearly 50% of our branches will be in Southeast markets. These market share gains are the byproduct of multiyear strategies that are not easily replicable by competitors. They include innovative operational deposit-oriented products like Momentum Banking, AI-driven customer acquisition strategies and the top quartile customer service model in addition to our investments in new branches.  Our key credit metrics remained strong during the quarter. Charge-offs were in line with our July expectations in both early stage delinquencies and non-performing assets improved sequentially. The ACL increased 3 basis points given slight changes to Moody's macroeconomic forecast.  Turning to liquidity and capital. We made significant progress against our goal to adapt early to expected changes in the regulatory framework. Our focused efforts throughout the bank enabled us to end the quarter with $103 billion in total liquidity sources and to achieve full Category 1 LCR compliance at the end of both August and September. During the quarter, we also made significant progress on our RWA optimization initiative. Total RWA declined 1% compared to the prior quarter
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

### Item 40: `ref_comp_02` / `chunk500_hybrid`

- **question_id:** ref_comp_02
- **condition:** chunk500_hybrid
- **category:** comparative
- **case:** C
- **current outcome label:** abstained

**Question:**
> How did Bank of America's and Huntington's positions on office real estate exposure differ in the first quarter of 2024, in charge-offs and in portfolio reduction?

**Gold anchor(s):**
> charge-offs increased $191 million versus the fourth quarter, driven by commercial real estate losses
> the office portfolio by about $500 million over the course of the last

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 -- `BAC_2024_Q1_prepared_remarks_500_009` -- transcript `BAC_2024_Q1` -- ONE OF the question's own transcript_ids*

```
306 million from the fourth quarter, driven by continued credit card seasoning and commercial real estate office exposures as swift revaluations from current appraisals and resolutions drove higher charge-offs. The net charge-off ratio was 58 basis points, a 13 basis point increase from the fourth quarter. On Slide 12, we show you the credit quality metrics for both our consumer and commercial portfolios. Consumer net charge-offs increased $150 million versus the fourth quarter from the flow-through of higher late stage credit card delinquencies. We included a credit card delinquency slide, No. 28 in our appendix, and we’re encouraged by the trend of delinquencies because the late stage increases slowed and early stage delinquencies improved as well, and that leads us to believe we should begin to see consumer net charge-offs start to level out over the next quarter or so. All of this is still well within our risk appetite and our expectations, and it’s consistent with the normalization of credit we discussed with you in prior calls. Commercial net charge-offs increased $191 million versus the fourth quarter, driven by commercial real estate losses and office exposures. On office losses this quarter, we recorded charge-offs on 16 office loans. Four were a result of sales activity, i.e. final resolution, seven were from losses that we expect on exposures that are in the process of expected resolution in the course of the next 90 days, and the rest we took as a result of refreshed valuations. We use a continuous and thorough loan-by-loan analysis and we’re quick to recognize impacts in the commercial real estate office space through our risk ratings, and that’s resulted in several downgrades in the last few quarters. As a result of these quick actions and our downgrades in categorization, we’ve also refreshed the valuation of our reservable criticized properties, and we’ve taken appropriate reserves and charge-offs in the process. Roughly one-third of our office exposure is now categorized as reservable criticized, and importantly the pace of the increase in reservable criticized exposures has slowed each quarter since the second quarter of last year, so we believe the losses on these office properties have been front-loaded and largely reserved. We expect the losses to move lower in the second quarter and we expect a notable decline in the second half of the year
```

*Rank 2 -- `WFC_2023_Q1_prepared_remarks_500_005` -- transcript `WFC_2023_Q1` -- NOT one of the question's own transcript_ids*

```
appropriate actions when warranted. We are also closely monitoring our commercial real estate office portfolio, and I'll share some more details on our exposure on the next slide. As expected, we've seen consumer delinquencies and losses gradually increase. Total consumer net loan charge-offs increased $60 million from the fourth quarter to 56 basis points of average loans, driven by an increase in the credit card portfolio. While most consumers remain resilient, we've seen some consumer financial health trends gradually weakening from a year ago, and we've continued to take credit taking actions to position the portfolio for a slowing economy. Nonperforming assets increased 7% from the fourth quarter, driven by higher commercial real estate nonaccrual loans over down 12% from a year ago due to lower residential mortgage nonaccrual loans. Of note, 87% of the nonaccrual loans in our commercial real estate portfolio were current on interest and 75% recurring on both principal and interest as of the end of the first quarter. Our allowance for credit losses increased $643 million in the first quarter, reflecting an increase for commercial real estate loans, primarily office loans as well as an increase for credit card model loans. Given the increased focus on commercial real estate loans, especially office, we provided more details on our portfolio on Slide 6. We have $154.7 billion of commercial real estate loans outstanding at the end of the first quarter with 35.7% of office loans, which represented 4% of our total loans outstanding.  The office market continues to show signs of weakness due to lower demand, higher financing costs and challenging capital market conditions. While we haven't seen this translate to meaningful loss content yet, we expect to see more stress over time. As you would expect, we have been derisking the office portfolio, which resulted in commitments declining 5% from a year ago, and we continue to proactively work with borrowers to manage our exposure, including structural enhancements and paydowns as warranted. As you can see in the slide, we've provided some additional data on the office portfolio, including approximately 12% is owner occupied. Therefore, the loan performance is mostly tied to the cash flow of the owner's operating business rather than rents paid by tenants. Nearly one third had recourse to a guarantor typically through a repayment guarantee. The portfolio is geographically diverse, and as you'd expect, the largest
```

*Rank 3 -- `WFC_2023_Q4_prepared_remarks_500_004` -- transcript `WFC_2023_Q4` -- NOT one of the question's own transcript_ids*

```
of prior period tax matters. Turning to capital and liquidity on Slide 5. Our CET1 ratio increased to 11.4% in the fourth quarter, 2.5 percentage points above our regulatory minimum plus buffers. This increase was driven by our earnings and an increase in accumulated other comprehensive income, reflecting lower interest rates and tighter mortgage-backed security spreads. During the fourth quarter, we repurchased $2.4 billion in common stock. We repurchased a total of $12 billion in common stock in 2023, and we currently expect to be able to repurchase more than this amount in 2024. We will continue to consider current market conditions, including interest rate movements, risk-weighted asset levels, stress test results as well as any potential economic uncertainty with respect to the amount and timing of share repurchases over the coming quarters. Turning to credit quality on Slide 7. As expected, net loan charge-offs increased, up 17 basis points from the third quarter to 53 basis points of average loans, driven by commercial real estate office and credit card loans. The increase in commercial net loan charge-offs reflected the higher losses in commercial real estate office, while losses in the rest of our commercial portfolio were stable from the third quarter. As expected, losses started to materialize in our commercial real estate office portfolio as market fundamentals remained weak. The losses were across a number of loans spread across various markets and were driven by borrower performance, lower appraisals were the result of properties or loans being sold at a loss. We substantially built reserves for this portfolio throughout 2023 as criticized and nonperforming assets increased. And while we expect additional losses in the coming quarters given the market fundamentals, and capital markets and liquidity challenges in this sector, the amounts will likely going to be uneven and episodic. Our commercial real estate team has a rigorous monitoring process and continues to derisk and reduce exposure, and we're using this information to evaluate our allowance, which I will discuss later. Consumer net loan charge-offs continued to increase and were up $118 million from the third quarter to 79 basis points of average loans. The increase was driven by the credit card portfolio, which performed as expected with increased losses driven by recent vintages maturing. Nonperforming assets increased 3% from the third quarter as growth in commercial nonaccrual loans more than offset declines in consumer. The increase in commercial real estate
```

*Rank 4 -- `PNC_2024_Q1_prepared_remarks_500_005` -- transcript `PNC_2024_Q1` -- NOT one of the question's own transcript_ids*

```
on Slide 11. While overall credit quality remains resilient, the pressure we anticipated within the commercial real estate office sector has continued. Non-performing loans increased $200 million or 9% linked quarter, almost entirely driven by commercial real estate, which increased $188 million. And inside of that, approximately $150 million was related to the CRE office portfolio. Total delinquencies of $1.3 billion decreased $109 million or 8% linked quarter, driven by lower consumer and commercial delinquencies. Net loan charge-offs were $243 million in the first quarter, and our annualized net charge-offs to average loans ratio was 30 basis points. Our allowance for credit losses totaled $5.4 billion or 1.7% of total loans on March 31, stable with December 31. Slide 12 provides more detail on our CRE office credit metrics. While NPLs have increased over the past few quarters, our criticized balances have remained relatively consistent. The migration of criticized loans to non-performing status is an expected outcome as we work to resolve the occupancy and rate challenges inherent to this portfolio. In the first quarter, net loan charge-offs within the CRE office portfolio were $50 million, essentially in line with the previous quarter level. Ultimately, we expect continued charge-offs on this portfolio, and accordingly we believe we are adequately reserved. As of March 31, our reserves on the office portfolio were 9.7% of total office loans and inside of that, 14.4% on the multitenant portfolio. Importantly, we continue to manage our exposure down and as a result, our balances declined 3%, or approximately $200 million linked quarter. In summary, PNC reported a solid first quarter 2024, and we're well positioned for the remainder of the year. Regarding our view of the overall economy, we're expecting economic expansion in the second half of the year, resulting in real GDP growth of approximately 2% in 2024, and unemployment to increase modestly to 4% by year end. We expect the Fed to cut rates 2 times in 2024, with a 25 basis point decrease in July and another in November. Looking at the second quarter of 2024 compared to the first quarter of 2024, we expect average loans to be stable, net interest income to be down approximately 1%. And as I mentioned previously, we expect NII and net interest margin to trough in the second
```

*Rank 5 -- `BAC_2023_Q2_prepared_remarks_500_012` -- transcript `BAC_2023_Q2` -- NOT one of the question's own transcript_ids*

```
to 213,000. That's some good work after peaking at 218,000 in January. Our summer interns will leave us in the third quarter, and hopefully many will return as full-time associates next summer. And at the same time in Q3, we welcomed back about 2,600 new full-time hires as college grads, many of whom interned with us last summer. And that's a very diverse class of associates who are excited to join the company. As we look forward to next quarter, we would expect the third quarter expense to more fully benefit from the second quarter head count reduction, even as we remain in a mode of modest hiring for client-facing positions. Additionally, the proposed notice of special assessment from the FDIC to recover losses from the failures of Silicon Valley and signature banks could add $1.9 billion expense for us, $1.5 billion after tax, and we just remain unsure at this point of timing to record that expense. Let's now move to credit, and we'll turn to Slide 17. Net charge-offs of $869 million increased $62 million from the first quarter, and the increase was driven by credit card losses as higher late-stage delinquencies flowed through to charge-offs. For context, the credit card net charge-off rate was 2.6% in Q2, and remains well below the 3.03% pre-pandemic rate in the fourth quarter of '19. Provision expense was $1.1 billion in Q2, and that included a $256 million further reserve build, that's driven by loan growth, particularly in credit card, and it reflects a macroeconomic outlook that on a weighted basis continues to include an unemployment rate that rises to north of 5% in 2024. On Slide 18, we highlight the credit quality metrics for both our consumer and commercial portfolios. On consumer, we note we continue to see asset quality metrics come off the bottom, and they remain below historical averages. Overall commercial net charge-offs were flat from first quarter. And within commercial we saw a decrease in C&I losses that was offset by an increase in charge-offs related to commercial real estate office exposures. As a reminder, commercial real estate office credit exposure represents less than 2% of our total loans, and this is an area where we've been quite intentional around our client selection, portfolio concentration, and deal structure over many
```

**Per-claim numeric trace:** not applicable (classified as abstained; no claims checked)

**Your verdict:** _______________________________________________

**Your failure-mode note:** _______________________________________________

---

