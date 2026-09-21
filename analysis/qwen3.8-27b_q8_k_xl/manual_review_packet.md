# Manual review packet

Generator: `qwen3.8-27b@q8_k_xl`. 48 items, drawn from the 12-condition grid by a
seeded mechanical rule (seed `20260906`) and shuffled into a single reading order.

Assembled material only: no verdict, no failure-mode label, no proposed
categories, no commentary. Stratum membership is deliberately NOT shown here --
it is in `manual_review_packet_manifest.csv` beside this file, so the sampling rationale is
auditable without being visible while reading.

Chunk text is the raw chunk text the generator was given, never the
metadata-enriched index string; chunk ids are asserted against each
generation record's own `retrieved_chunk_ids`.

---

## 1. `ref_them_02` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_them_02
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks characterise the uncertainty around the Basel III endgame proposal over 2023 and 2024, and how did it affect their capital actions?

**Generated answer, verbatim:**

```
Based on the provided context, banks characterized the uncertainty surrounding the Basel III endgame as significant, noting that while there was favorable momentum in press reports and regulator comments by mid-2024, substantial uncertainty remained regarding both the quantum (magnitude) and timing of its resolution. In 2023, the proposal was described as "overcalibrated," with concerns raised about procyclicality and the compounding effects of GSIB surcharges and stress capital buffers, which were projected to increase capital requirements by up to 45% relative to a 2017 baseline if finalized in their current form.

This uncertainty directly affected capital actions:
*   **Goldman Sachs** operated at the wider end of its CET1 range (running with 90 bps of cushion, above normal) specifically to signal flexibility and address the remaining uncertainties regarding the Basel III endgame.
*   **JPMorgan Chase** maintained a modest pace of share repurchases in light of the proposal, stating they would continue to reassess their buyback trajectory as circumstances evolved. They also emphasized that implementing the rules consistently with European approaches (retaining credit risk modeling) could have achieved compliance without the proposed unnecessary increase in capital requirements.
*   **Morgan Stanley** noted a lack of clarity on whether the endgame was being fully implemented in Europe and highlighted that actual U.S. bank capital levels were higher than speculated, while awaiting specific rule proposals and engaging with regulators during the comment period.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `GS_2024_Q2_qa_200_020`*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution
```

*Rank 2 — `JPM_2023_Q3_prepared_remarks_200_006`*

```
ing out from the details of this most recent proposal, this page reminds us of what's happened since 2017. Since then, SA-CCR and the stress capital buffer have been adopted and our GSIB surcharge will increase to 4.5%. So assuming the Basel III endgame and GSIB proposals are finalized in their current form, we would see a 45% increase in our capital requirements relative to that 2017 starting point. This illustrates again how overcalibrated these proposals are and it's not done yet. We still expect the Fed to incorporate CECL into CCAR, which will likely increase the SCB. And, of course, given the absence of a fix to the GSIB clause, it continues to present a headwind into the indefinite future. And aside from those dynamics, there remains the long-standing issue of procyclicality in the overall capital [Technical Difficulty]. We think it's also important to point out that the agencies did
```

*Rank 3 — `MS_2023_Q2_qa_200_001`*

```
the firm to manage through what could be pretty radical changes.

James Gorman: Well, it's an important question. And you're right, I have made comments on it. Let's sort of set the table of where we are right now. We've had a lot of speculation based off of what the Basel III Endgame looks like. By the way, I'm not sure it's actually being implemented fully in Europe, just to say. I think the U.S. banks actually have more capital, but putting that knit aside, we did get the speech from the Vice Chair. I think it's important to look at the title of that speech, which was holistic capital review. So, it's taking into account all of the CCAR, stress tests, SCB buffers and the like as this stuff is implemented. Secondly, we haven't seen the actual rules. I mean, I guess there will be a proposal coming out,
```

*Rank 4 — `JPM_2023_Q3_prepared_remarks_200_003`*

```
. We ended the quarter with a CET1 ratio of 14.3%, up about 50 basis points versus the prior quarter as the benefit of net income less capital distributions was partially offset by AOCI. We had $2 billion of net share repurchases this quarter and the pace of buybacks will likely remain modest in light of the Basel III endgame proposal. In line with our capital hierarchy, we will continue to reassess the buyback trajectory as circumstances evolve or opportunities emerge. And on the topic of the Basel III endgame, you'll see that we added a couple of pages on it. So, let's cover that now, starting on Page 4. Given the significance of this proposal for us, the broader industry as well as households and businesses as end-users, we thought it was important to spend time discussing it. And while we know there is interest in having us quantify the expected impact of this proposal in a lot of granular detail,
```

*Rank 5 — `JPM_2023_Q3_prepared_remarks_200_007`*

```
actually have a choice here. While it may technically be true that the proposal is Basel compliant, Basel compliant does not mandate a 25% increase in capital requirements. Implementing the Basel III endgame consistently with how the Europeans have by retaining credit risk modeling and also addressing the compounding effects of GSIB and SCB would have achieved Basel compliance without creating this unnecessary increase in capital requirements. As you would expect, we will continue to engage and forcefully advocate during the comment period and beyond in a great deal of technical detail. For the purposes of this call, we wanted to make the equally important broader plans about both the level of capital increase and the flaws in the construct of the framework itself since coherent design is critical to the framework's durability over time. The current proposal exacerbates existing features that discourage beneficial scale and diversification. If it goes through as written, there will likely be significant impacts on pricing and availability of credit for businesses and consumers. In addition, the ongoing and persistent
```

verdict: faithful

failure mode: none — one undated inference ("by mid-2024"); Check-3 flag looks like a thematic-question artifact

notes: All claims trace (GS 90bps ch1; JPM 45%/2017, modest buybacks, European approach ch2/4/5; MS ch3), and both halves of the question are answered. One unsupported inference: "by mid-2024" — no date appears in the GS chunk. The Check-3 flag looks like an artifact of a question that asks about "banks" generally while the anchors sit on JPM. Label agrees.

---

## 2. `ref_them_10` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_them_10
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> What did banks say about credit card growth and card credit performance over 2023 and 2024?

**Generated answer, verbatim:**

```
Based on the provided context, banks described credit card growth and credit performance as follows:

*   **American Express (AXP):** In late 2023/early 2024, AXP reported year-over-year loan and card member receivables growth of 13%. They expected this elevated growth to moderate through 2024 but remain modestly faster than billings. Regarding credit performance, AXP cited "strong and best-in-class" metrics attributed to high customer quality and disciplined risk management, though they noted that write-off and delinquency rates continued to tick up in the quarter. In Q1 2024, AXP highlighted that revolving balances on their charge product were the fastest-growing segment of their lending products with the best credit performance among their lending offerings.
*   **JPMorgan Chase (JPM):** In Q3 2024, JPM reported Card Services revenue up 11% year-on-year, driven by higher card net interest income on higher revolving balances. Card outstandings increased by 11% due to strong account acquisition and the normalization of revolve. Credit costs were $2.8 billion, with net charge-offs rising $520 million year-over-year to $1.9 billion, largely reflecting higher revolving balances.
*   **Wells Fargo (WFC):** In Q4 2024, Wells Fargo indicated that early vintages of new credit card products launched approximately 3.5 years prior were beginning to mature and become more profitable, though they noted it was still "early days" for this profitability to fully appear in the P&L.
*   **Capital One (COF):** In Q1 2024, Capital One mentioned seeing good growth opportunities in the card business while discussing the consumer environment and merger applications.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `AXP_2023_Q4_prepared_remarks_200_012`*

```
, we are pleased with the continued strong engagement and loyalty of our card members across the globe. As we think about 2024, we are assuming a spend environment similar to what we've seen in the past few quarters. Now moving on to loans and card member receivables on slide seven. We saw a year-over-year growth of 13%. We expect this growth, which has been elevated versus pre-pandemic levels to continue to moderate as we progress through the 2024, but to still grow modestly faster than billings. Turning next to credit and provision on slide eight through 10. First and most importantly, we continue to see strong and best-in-class credit metrics. We attribute this performance to the high credit quality of our customer base, our robust risk management practices, and our disciplined growth strategy. As we had expected, our write-off and delinquency rates did continue to tick up this quarter, as you see on slide right.
```

*Rank 2 — `WFC_2024_Q4_qa_200_002`*

```
credit card profitability. When you're in growth mode, credit card experience is a drag from accounting on the upfront acquisition costs and provision. Where are you on card profitability now? Is that an upside driver to ROE? Is more of the balances roll off teasers and some of that upfront expense wanes.

Mike Santomassimo: Yes, certainly is. I think as you look backwards a little bit, we started launching the new products 3.5 years ago. So, the first of the vintages came on starting in August -- July, August, a few years ago. And so, we're just starting to kind of see those earliest vintages mature and become more profitable. So, we're still early days in terms of seeing that profitability really come through in the P&L. I'd say, obviously, the factors you got to think about as you sort of look through that is the credit box and the credit performance,
```

*Rank 3 — `AXP_2024_Q1_qa_200_024`*

```
that is available on our charge product. It's a service that a lot of card members are taking advantage of. It's the opportunity for them to revolve some of their transactions or part of their balance, their performance is very strong. It's actually the segment of our balances that is the fastest growing. And from -- I would say from a performance standpoint, because that product, but that service is attached to our charge card products, so typically premium card members the credit performance is also the best that we have in our lending products. So it's a very efficient way for us to grow balances by extending credit to premium card members. And the first question, I forgot was funding? And so the funding mix is still -- it's still evolving towards more deposits -- and as you know, deposits is, for us, they're the most effective and the most economical source of fund. And it's a very stable source of
```

*Rank 4 — `COF_2024_Q1_qa_200_003`*

```
merger applications with both the Fed and the OCC and we are engaged with the -- sorry, with the DOJ as they, of course, play a key role in advising the Fed and the OCC on competition questions. We believe our applications make a very compelling case for approval. We believe strongly that this merger will increase competition among banks and credit card issuers and payment networks, and provide significant benefits for consumers, merchants and the communities that we serve. While some have raised concerns about competition, we believe that the facts in favor of the deal will be compelling.

Mihir Bhatia: Got it. That is helpful. Just turning back to the health of the consumer for a second for my follow-up. If you could just talk a little bit about the environment for card acquisitions, you did mention, I think, that the growth you see good growth opportunities in the card business. So wondering if you can expand on that. Maybe talk about just some of the puts and takes
```

*Rank 5 — `JPM_2024_Q3_prepared_remarks_200_004`*

```
by lower servicing and production revenue. Turning to Card Services and Auto. Revenue was up 11% year-on-year, driven by higher card NII on higher revolving balances. Card outstandings were up 11% due to strong account acquisition and the continued normalization of revolve. And in Auto, originations were $10 billion, down 2%, while maintaining strong margins and high quality credit. Expenses of $9.6 billion were up 5% year-on-year, predominantly driven by higher field and technology compensation, as well as growth in marketing. In terms of credit performance this quarter, credit costs were $2.8 billion driven by card and reflected net charge offs of $1.9 billion, up $520 million year-on-year and a net reserve build of $876 million predominantly from higher revolving balances. Next the Commercial and Investment Bank on page five. The CIB reported net income of $5.7 billion on revenue of $17
```

verdict: faithful

failure mode: none — the offtarget label reflects which transcripts were retrieved, not the answer

notes: Every figure traces and every company is right (AXP ch1/ch3, JPM ch5, WFC ch2, COF ch4); it genuinely answers the question. The quarter labels ("In Q3 2024, JPM...") are asserted rather than stated in the chunks — inferred, and here correct. "offtarget" is about which transcripts were retrieved, not about this answer.

---

## 3. `ref_them_04` / `chunk500_dense_enriched`

- **condition:** chunk500_dense_enriched
- **arm:** enriched
- **question_id:** ref_them_04
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Generated answer, verbatim:**

```
In late 2023 and early 2024, the banks described their progress on positive operating leverage as follows:

*   **Fifth Third (FITB):** The bank stated that while the carryover effect of its Risk-Weighted Asset (RWA) diet made full-year positive operating leverage unfeasible in 2023, it anticipated returning to positive operating leverage in the second half of 2024. This was supported by expense discipline and a 4% reduction in full-time equivalent headcount from its 2023 peak without a company-wide expense program.
*   **Bank of America (BAC):** The bank reported achieving 170 basis points of operating leverage for the full year 2023. This was driven by heightened quarterly expense levels being lowered throughout the year despite continued investments in growth, alongside record organic customer activity and digital engagement.
*   **U.S. Bancorp (USB):** In early 2024 (Q3 2024 context), the bank reported positive operating leverage of approximately 30 basis points for Q3 2024. It indicated that fourth-quarter 2024 positive operating leverage would be north of 1% and expected this trend to continue expanding into 2025.
*   **M&T Bank (MTB):** In early 2024, management expressed confidence in achieving positive operating leverage for 2025, noting that while fourth-quarter 2023 expenses increased slightly due to projects and corporate-wide incentives, the company had strong momentum and expected 2025 to be a better year than 2024.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `FITB_2023_Q4_prepared_remarks_500_002`*

```
profitability. Expense discipline, strong returns, and positive operating leverage remain core areas of focus for Fifth Third. Supported by our technology modernization investments and a focus on leaning out key value streams, we reduced full-time equivalent employee headcount by 4% from our peak in 2023 to the end of the year without the need for a company-wide expense program. The run rate benefits of these efforts put us in a position to sustain the peer-leading annualized expense growth that we have averaged the past several years, even as we continue to invest for growth. While the carryover effect of the RWA diet makes it unfeasible for the full year, we do anticipate returning to positive operating leverage in the second half of 2024. The third point I'd like to highlight is about growth. Our strategies have been consistent, building out our Southeast markets, producing a strong fee to total revenue mix, and leveraging software that differentiates our product offerings and improves productivity. These are multi-year investments that cannot be replicated easily by competitors to one to two years of hiring a few new branches or small tuck-in acquisitions. In 2023, we opened 37 new branches concentrated in the Southeast, bringing us to 107 opened over the past five years. We plan to open another 31 branches in the Southeast in 2024. As a portfolio, these branches have continued to outperform our expectations on both household acquisition and deposit growth and should provide a tailwind for several years forward. We also continue to invest in treasury management, wealth and asset management, and capital markets. All three of these businesses grew for us in 2023. We expect mid-to-high single-digit growth in each in 2024. In treasury management, our acquisitions of Rize and Big Data Healthcare and the launch of Newline, our embedded payments business, should continue to support peer-leading performance. In wealth and asset management, Global Finance recently named our Private Bank as the Best US Regional Private Bank for the fifth consecutive year and Best Private Bank for Entrepreneurs globally for the first time. In our capital markets business, we have seen more robust activity levels to start the year, including an M&A pipeline that is 1.5 times the full-year revenue target embedded in our guidance. Overall, we expect 2024 to be a solid year of improving revenue trends and continued to expense discipline. Given what we believe to be a less certain outlook than the markets would imply,
```

*Rank 2 — `BAC_2023_Q4_prepared_remarks_500_002`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 3 — `MTB_2024_Q3_qa_500_011`*

```
ble.

Daryl Bible: Yes. So we are still putting 2025 together. I do believe we will have positive operating leverage for 2025. Whether we are 150 or 200, I think you're in the neighborhood of where plan will end out, but we are on 100% have kind of figured out and everybody's agreed to it, but we will get there. I feel very confident we will get there from that. If you look at the expenses that we guided, they were up a little bit in the fourth quarter. It is mainly due to projects that we have. We have a fair amount of projects going on in the company, and we are making a lot of progress. We do have an increase there. The other thing that we are doing is -- we've had a pretty good year from a performance perspective, both financially. We made good progress on our asset quality and good loan and deposit growth and just improving and getting good some of our priorities accomplished. So we actually are increasing our corporate-wide incentives in the fourth quarter for payout for everybody for a good year. That said, I still feel that 2025 is going to be a better year than 2024 to be honest with you. We continue to have a lot more work to do and make progress. But we have a lot of positive momentum now and need to reward the people that are making it happen in the company and feel good about that.

John Pancari: Great. All right. Thank you. That's helpful. And then on the credit side, your loan loss reserve ratio as a percentage of loans ticked down a bit or so this quarter, I guess around 162 basis points where it stands now. Where do you see that trending here? You cited the expected decline and criticized that you will see in the quarter and then a pretty good trajectory there. Fair to assume continued modest decline here in that ratio? Is that fair to assume as you look out?

Daryl Bible: Yes. I think when you look at it, this past quarter we had some good macro factor positives with creepy being much more positive and that helped drive and downward drop in criticized, which is good. I think as you look forward though, we are growing all of our lending categories, so you have a mix change that you're seeing occur in the balance sheet. And that mix change is more heavy on the consumer side. Consumers definitely have for the most part, higher overall spreads and
```

*Rank 4 — `BAC_2023_Q2_qa_500_008`*

```
: We'll go next to Erika Najarian with UBS. Your line is open.

Brian Moynihan: Hi Erica, you might be on mute. Catherine, maybe we can come back to Erica.

Operator: Absolutely. We'll go next to Betsy Graseck with Morgan Stanley. Your line is open.

Betsy Graseck: Hi, good morning.

Brian Moynihan: Good morning, Betsy.

Betsy Graseck: A couple of questions. One on the operating leverage that I know you discussed earlier. I mean, in the past, when you had the record number of consecutive quarters of positive operating leverage, it seemed like it was being driven primarily [technical difficulty] a lot of inputs, but 1 of the big drivers was consolidation of branches. And now it's an investment spend environment in branches. So I'm just wondering if there is - if you would agree with that. And if there's a different way that you're going to be delivering this positive operating leverage as you're increasing investment spend in one of the core platforms of the company.

Brian Moynihan: Betsy, that's kind of what I said earlier. It's been gotten by different ways in different periods of time. But even in the last year, the numbers of branches, I think dropped about from 3,900 to 3,800 and change. And so even as we deployed new ones. And so you're consolidating branches in markets you've been in a long time with lots of branches. The ATM count continues to drift down. But importantly, if you go to the digital pages and look at the activity levels by customers - and you're speaking mostly the consumer business, but affects all customer bases. And you see things like Zelle transactions far exceeding checks. Remember that - what that means is that we don't have to process a check on the back end of that. And so, and then your process it, push it through. So all that continues to grow very quickly and continues to change the overall operating costs in our consumer business. Our cost of operating plus the cost of pays and deposits is still 130-odd basis points or whatever, it's very strong. If you go where the big moves are coming as what we're doing in the markets business, for example, in terms of deeper, deeper digitization, it was always - equity trading was already digit
```

*Rank 5 — `USB_2024_Q3_qa_500_002`*

```
have anything contemplated at this particular point in time.

John Pancari: Okay. All right. Thank you. And then separately, on the expense side, you put up some pretty good positive operating leverage this quarter, and you implied that fourth quarter you'll see that as well. And I believe at the Investor Day, you expressed confidence in continued positive operating leverage. As you look at 2025, can you maybe help us get a sense of the magnitude of that operating leverage that you think is reasonable as you enter 2025 and longer-term, I believe The Street is looking at about 150 basis points to 200 basis points operating leverage next year. Wanted to get your thoughts on that as we look at your return profile in the coming years?

Andy Cecere: Yeah. Thanks, John. This is Andy. So as you saw, we reported positive operating leverage of approximately 30 basis points in Q3 here. The guidance that John provided would indicate that our expectation for positive operating leverage in the fourth quarter of '24 will be north of 1%, and we would expect it to continue to expand from there into 2025. So, building upon that 1-plus-percent into '25, exactly where we'll get, we'll give more guidance as we get the forward-looking guidance as we think about '25 across the categories.

John Pancari: Great. Very helpful, Andy. Thank you.

Andy Cecere: You bet.

Operator: Your next question comes from Betsy Graseck from Morgan Stanley. Your line is now open.

Betsy Graseck: Hey, good morning.

Andy Cecere: Hey, Betsy.

Betsy Graseck: Yeah. Just to -- one follow-up on that is, in the guidance for 4Q, you indicated expenses [at total of] (ph) $16.8 billion. And I know in the past, you had been saying $16.8 billion or less. So, is there anything we should take-away from that very ever so slight guidance change?

John Stern: Hey, Betsy, it's John. So, I think it's just reflective of we're in the third -- we're complete with the third quarter, we're at the fourth quarter right now. We have a very good line-of-sight in terms of where our expense base will be. And so we were just being more precise with that particular number.
```

verdict: unfaithful

failure mode: period misattribution — USB and MTB material from Q3 2024 dated "early 2024", pulling it inside the asked window

notes: Figures all trace (FITB ch1, BAC ch2, USB ch5, MTB ch3), but two period errors: USB is labelled "early 2024 (Q3 2024 context)" and MTB "in early 2024" — both are Q3 2024. Both items also fall outside the asked "late 2023 and early 2024" window, and the mislabelling makes them look in-window. Grounded but not responsive; the label cannot see this. Compare item 7, same question, periods stated correctly.

---

## 4. `ref_fact_05` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_fact_05
- **category:** factual
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** single (1 anchor) (coverage@5 = 1)
- **Check 3 flag:** not flagged

**Question:**

> How large was the Walmart-related build that Capital One called out as an adjusting item in the second quarter of 2024?

**Generated answer, verbatim:**

```
The Walmart-related build that Capital One called out as an adjusting item in the second quarter of 2024 was $826 million.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `COF_2024_Q2_qa_200_000`*

```
Operator: Thank you. [Operator Instructions] Our first question comes from Sanjay Sakhrani with KBW. You may proceed.

Sanjay Sakhrani: Thanks. Rich, Andrew, just looking at the credit metrics, as Rich mentioned, it seems like the trends are pretty favorable. I mean, in most segments things are improving, if not stable. And then the U.S. card, there is an improving trend in that second derivative. I'm just curious how we should think about reserve rate going forward because I think even excluding the Walmart impact, the reserve rate went higher.

Andrew Young: Sure, Sanjay. Well, let me start by covering this quarter's allowance and then I'll talk about the future. So in the quarter, as you said, first, we had the effect of Walmart, the $826 million build that we spelled out as an adjusting item. We also reserved for the growth we saw in the quarter. Beyond that coverage in
```

*Rank 2 — `COF_2024_Q3_prepared_remarks_200_002`*

```
, everyone. I will start on Slide 3 of tonight's presentation. In the third quarter, Capital One earned $1.8 billion or $4.41 per diluted common share. Included in the results for the quarter were adjusting items related to Discover integration costs and a small downward revision to our FDIC special assessment estimate. Net of these adjusting items, third quarter earnings per share were $4.51. Pre-provision earnings in the third quarter increased 3% from the second quarter to $4.7 billion. Revenue in the linked quarter increased 5%, driven by higher net interest income. Non-interest expense increased 7%, driven by increases in both operating expense and marketing spend. Provision for credit losses was $2.5 billion in the quarter, down $1.4 billion relative to the prior quarter. The quarterly decrease was primarily driven by the absence of the second quarter's one-time allowance build for the termination of the Walmart partnership, a decline in the
```

*Rank 3 — `COF_2024_Q4_prepared_remarks_200_002`*

```
, I'll turn the call over to Mr. Young. Andrew?

Andrew Young: Thanks, Jeff, and good afternoon, everyone. I will start on slide three of tonight's presentation. In the fourth quarter, Capital One earned $1.1 billion or $2.67 per diluted common share. For the full year, Capital One earned $4.8 billion or $11.59 per share. Included in the results for the fourth quarter were adjusting items related to discover integration costs and a legal reserve build. Net of these adjusting items, fourth-quarter earnings per share were $3.09. Full-year adjusted earnings per share were $13.96. We also had one notable item in the quarter, which was $100 million of accelerated philanthropy contributions. Pre-provision earnings of $4.1 billion in the fourth quarter were down 13% from the third quarter, driven by higher non-interest expense. The linked quarter increase in non-interest expense was driven
```

*Rank 4 — `COF_2024_Q2_prepared_remarks_200_002`*

```
Thanks, Jeff, and good afternoon, everyone. I will start on Slide 3 of tonight's presentation. In the second quarter, Capital One earned $597 million or $1.38 per diluted common share. Included in the results for the quarter were adjusting items related to the Walmart partnership termination, Discover integration costs, and an accrual for our updated estimate of the FDIC's special assessment. Net of these adjusting items, second quarter earnings per share were $3.14. Relative to the prior quarter, period end loans held for investment increased 1%, while average loans were flat. Ending deposits were flat versus last quarter, while average deposits increased 1%. Our percentage of FDIC insured deposits increased 1 percentage point to 83% of total deposits. Pre-provision earnings in the second quarter increased 7% from the first quarter. Revenue in the linked quarter increased 1%, driven by higher net and non-interest income, while non-interest expense decreased 4
```

*Rank 5 — `COF_2024_Q4_qa_200_027`*

```
ago when we announced it. And so as we get to legal day one and put the marks on the balance sheet, we'll provide updates on the relevant metrics at that point.

Jeff Norris: Next question, please.

Operator: Our next question comes from Mihir Bhatia with Bank of America. You may proceed.

Mihir Bhatia: Good afternoon and thank you for taking my questions. I wanted to start first by just talking about NIM a little bit. You called out the Walmart impact this quarter. Any other call-outs for the quarter? It just feels banks have been quite disciplined about lowering saving accounts interest rates as the Fed has reduced rates? Do you think that continues or are you starting to see some demand for deposits or deposit competition ramping as we start contemplating loan growth here into 2025? I guess just related to that, if you could just talk about some of the puts and takes on NIM in 2025 that'd be great?
```

verdict: faithful

failure mode: none

notes: Exact, minimal, correct: $826m, ch1 rank 1, no padding. Answers precisely what was asked. Label agrees. Useful as the clean baseline for the rest.

---

## 5. `ref_them_08` / `chunk200_bm25`

- **condition:** chunk200_bm25
- **arm:** text_only
- **question_id:** ref_them_08
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did firms describe momentum in net inflows, AUM and client investment assets during 2023?

**Generated answer, verbatim:**

```
Based on the provided context, firms described their performance regarding net inflows, AUM, and client investment assets for 2023 as follows:

*   **JPMorgan Chase:** Reported record client asset net inflows of $489 billion for the year. Assets Under Management (AUM) reached $3.4 trillion and client assets reached $5 trillion, both up 24% year-on-year, driven by continued net inflows and higher market levels. Net long-term inflows were $140 billion for the full year, while liquidity saw net inflows of $242 billion.
*   **BlackRock:** Full-year total net inflows were $289 billion, positive across active and index strategies as well as regions. The firm generated industry-leading ETF net inflows of $186 billion in 2023, representing 6% organic asset growth.
*   **Bank of America:** While specific full-year 2023 AUM figures were not detailed in the text, it noted that Firmwide Assets Under Custody (AUCA) of $52.1 trillion were up 9% year-over-year (referenced in Q4 2024 remarks comparing to prior periods), reflecting higher market values and client inflows. It also highlighted that AUM of $2 trillion was up 3% year-over-year, primarily due to higher market values.
*   **State Street:** The context provided for State Street focuses on Q1 2024 performance (such as cash net inflows of $9 billion and record ETF AUM of $1.4 trillion) rather than describing the specific momentum or totals for the full year 2023, other than noting a "strong finish" at year-end 2023 that benefited Q1 2024 management fees.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `JPM_2023_Q4_prepared_remarks_200_009`*

```
by higher compensation, including performance-based incentives, continued growth in our private banking advisor teams, the impact of closing JPMorgan Asset Management China acquisition, and the continued investment in global shares. For the quarter, net long-term inflows were $12 billion, positive across equities and fixed income, and $140 billion for the full year. In liquidity, we saw net inflows of $49 billion for the quarter and net inflows of $242 billion for the full year. And we had record client asset net inflows of $489 billion for the year. AUM of $3.4 trillion and client assets of $5 trillion were both up 24% year-on-year, driven by continued net inflows and higher market levels. And finally, loans were up 2% quarter-on-quarter and deposits were up 7% quarter-on-quarter. Turning to Corporate on Page 9. Corporate reported a net loss of $
```

*Rank 2 — `BK_2024_Q4_prepared_remarks_200_016`*

```
client activity, and higher market values. Investment management and performance fees were also up 9%, driven by higher market values, partially offset by the mix of AUM flows. Firmwide AUCA of $52.1 trillion were up 9% year-over-year, reflecting higher market values, client inflows, and net-new business, partially offset by the unfavorable impact of a stronger US dollar. Assets under management of $2 trillion were up 3% year-over-year, primarily reflecting higher market values, partially offset by the unfavorable impact of the stronger dollar. Foreign exchange revenue increased by 24%, driven by higher client volumes. Investment in other revenue was $140 million in the quarter. As a reminder, the fourth quarter of 2023 included a $144 million reduction in investment and other revenue related to a fair-value adjustment of a receivable. Excluding notable items, the year-over-year decrease primarily reflects the absence of strategic
```

*Rank 3 — `BLK_2023_Q4_prepared_remarks_200_014`*

```
Directors declared a quarterly cash dividend of $5.10 per share, representing an increase of 2% over the 2023 level. At present, based on capital spending plans for the year, and subject to market conditions, including the relative valuation of our stock price, we're targeting the purchase of $1.5 billion of shares during 2024. Full year total net inflows of $289 billion were positive across active and index as well as regions, led by $156 billion of net inflows from clients in the United States, and we had 70 products across our ETF and mutual fund ranges with over $1 billion in net inflows. BlackRock generated industry-leading ETF net inflows of $186 billion in 2023, representing 6% organic asset growth led by $112 billion of net inflows into our bond ETFs. Fourth quarter ETF net inflows of $88 billion reflected significant momentum into year-end helped by seasonal tax
```

*Rank 4 — `STT_2024_Q1_prepared_remarks_200_007`*

```
ed by higher equity markets, the strategic actions we have taken to position our asset management business for growth, and the benefits of the strong finish in step-off point at year-end 2023. 1Q 2024 management fees of $510 million are the highest since the first quarter of 2022. While GA experienced total aggregate outflows in Q1, this was driven by the impact of a large, but expected single client redemption within the institutional business. We saw continued momentum in the defined contribution business driven by our target day franchise. Encouragingly, we saw cash net inflows of $9 billion in the quarter, the fourth consecutive quarter of positive net inflows of our cash business. ETF AUM reached a record $1.4 trillion at quarter end with GA continuing to gather net inflows and expand market share within U.S. low-cost ETFs. Now let me spend a moment on our continuing productivity efforts. We have a detailed set of initiatives
```

*Rank 5 — `BLK_2024_Q4_prepared_remarks_200_002`*

```
investment capability expansion, technology, and scale. We executed breakthrough investment offerings and industry-leading partnerships. 2024 marks a quantum leap forward for BlackRock against our long-term value creation objectives and an invigoration of the future of asset management and technology services for our clients. We've spoken all year about how organic growth momentum and overall client sentiment has been improving. BlackRock saw record net inflows in 2024, powered by two back-to-back record flows quarters in the second half. Our annual revenue, operating income, and earnings per share each grew double digits. We made disciplined investments for profitable growth, delivering 280 basis points of margin expansion as our AUM grew to a new high of nearly $11.6 trillion. We enter 2025 from a position of strength, having generated 7% annualized organic base fee growth in the fourth quarter, our highest in three years. Our record client activity and the accelerating organic revenue growth we saw in 2024, they
```

verdict: unfaithful

failure mode: company misattribution — BNY Mellon (BK_2024_Q4) reported as Bank of America

notes: JPM (ch1) and BLK (ch3) figures all correct. But the third bullet attributes ch2 — BK_2024_Q4, BNY Mellon — to Bank of America; those are BNY's AUCA and AUM. The State Street bullet is honest that its context is Q1 2024. The label says nothing about the substitution. Compare items 6, 35, 41.

---

## 6. `ref_them_08` / `chunk500_dense`

- **condition:** chunk500_dense
- **arm:** text_only
- **question_id:** ref_them_08
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did firms describe momentum in net inflows, AUM and client investment assets during 2023?

**Generated answer, verbatim:**

```
Based on the provided context, firms described momentum in net inflows, AUM, and client investment assets during 2023 as follows:

**BlackRock (BLK)**
*   **Net Inflows:** The firm reported $32 billion in institutional net inflows for 2023, led by active strategies. Cash management saw $79 billion in net inflows for the year, while private markets attracted $14 billion in net inflows driven by infrastructure and private credit. Retail clients experienced net outflows of $8 billion for the full year, primarily due to allocations away from rate-sensitive strategies, though this was partially offset by record $12 billion in net inflows into Aperio.
*   **AUM:** Cash and liquidity AUM grew 14% (over $90 billion) year-over-year. Aperio’s AUM grew 95% since acquisition to reach $80 billion. The planned acquisition of GIP is expected to triple BlackRock’s infrastructure client assets to a pro forma $150 billion platform.

**Morgan Stanley (MS)**
*   **Net Inflows:** Long-term net outflows were approximately $7 billion for the full year, driven by headwinds in active equity growth strategies. However, fee-based flows remained strong, with adviser-led flows originating from workplace relationships reaching $28 billion in Q1 alone (double the prior year). The combined Parametric brand saw net inflows of over $5 billion in Q4.
*   **AUM:** Total AUM increased to $1.5 trillion by the end of 2023, supported by higher asset values. In Q1, total AUM was reported at $1.4 trillion.

**Bank of America (BK)**
*   **Net Inflows/Outflows:** The firm noted cumulative net outflows in its investment management segment for the year, which were partially offset by higher market values and a weaker dollar. In Q4 specifically, there were $7 billion in net inflows into short-term strategies and $4 billion into long-term active strategies, while index strategies saw $10 billion in net outflows.
*   **AUM/Client Assets:** Investment management AUM of $2 trillion increased by 8% year-over-year. Wealth management client assets grew 16% year-over-year to $312 billion, reflecting higher equity market values and cumulative net inflows.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BLK_2023_Q4_prepared_remarks_500_006`*

```
trades and portfolio reallocations. We saw $28 billion of net inflows into precision exposures as institutional clients use these highly liquid instruments to re-risk in the quarter. With Safe-Haven cash providing positive returns. Full year and fourth quarter retail net outflows of $8 billion and $9 billion, respectively, were primarily due to allocations out of rising rate sensitive strategies namely liquid alternatives and flexible bond funds. This was partially offset by strength in Aperio, which saw record net inflows of $12 billion in 2023. Aperio AUM since acquisition has grown 95% to $80 billion. BlackRock's institutional business generated net inflows of $32 billion in 2023, led by active net inflows of $87 billion including the funding of several significant outsourcing mandates throughout the year. Index net outflows of $55 billion were driven by redemptions from our low fee equity strategies as several large clients adjusted their allocations or redeemed for cash needs. Finally, BlackRock's cash management platform saw $33 billion of net inflows in the fourth quarter and $79 billion of net inflows in 2023. We're pleased with the continued strong growth in our cash and liquidity business with year-end AUM up 14% or over $90 billion year-on-year. We're leveraging our scale and integrated cash offerings to engage with clients who are using these products not only to manage liquidity, but also to earn attractive returns. Demand for private markets remain strong, with $14 billion of net inflows into BlackRock illiquid strategies during the year driven by infrastructure and private credit. We continue to expect these categories to be our primary growth drivers in the coming years. Turning to our planned acquisition of GIP this is an exciting day for us, our new partners, our clients and our shareholders. The combination will mark a transformational change in our private market scale and growth. GIP is the world's leading independent infrastructure manager with current client AUM of over $100 billion and fee-based AUM of over $60 billion. The acquisition will create a highly complementary pro forma $150 billion infrastructure platform post-closing tripling BlackRock's infrastructure client assets. The integration will nearly double our private markets management fees to over $1.5 billion and add over $400 million in post-tax annual FRE with FRE margins
```

*Rank 2 — `MS_2023_Q4_prepared_remarks_500_009`*

```
our channels. Second -- migrate assets to advice. Third -- deepen existing client relationships with enhanced capabilities including new products and solutions, and finally, realize scale benefits of our investments over time. These efforts are well underway. In the year, we grew client relationships by over 600,000 across the franchise. This was led by success in the workplace channel, as we continue to win corporate plans and add participants in stock plan. In the prior three years, we saw an average of $50 billion of workplace assets migrate to the investor led -- the advisor led channel on an annual basis. This year, client migration was up 25% year-over-year despite economic headwinds, and on the product side, our financial advisors are offering clients investment opportunities such as private credit, private equity, and all their other alternatives. Bringing wealth and investment management closer together will create greater opportunities for ongoing product creation. As we move forward and transition from integration to optimization for client experience, we expect to see greater scale benefits from our investments over time. Investment management reported full year results of $5.4 billion and fourth quarter revenues of $1.5 billion. AUM increased year-over-year to $1.5 trillion, supported by higher asset values. Long-term net inflows of approximately $7 billion -- excuse me, long term net outflows of approximately $7 billion were driven by headwinds in our [MSIM] active equity growth strategies. Within alternatives and solutions, we continue to see demand for parametric customized portfolios across both equity and fixed income strategies as more retail clients seek customized solutions. Liquidity overlay services had outflows of $6.6 billion. Weaker institutional liquidity flows were partially offset by demand for parametric's overlay product and the combined parametric brand, inclusive of overlay and its retail offering had net inflows of over $5 billion again this quarter, underscoring the strength of our differentiated customized offering. Fourth quarter asset management and related fees of $1.4 billion increased slightly versus last year. Quarterly performance based income and other revenues were $61 million. Gains in U.S. private equity and infrastructure offset losses in real estate, reflecting the benefits of diversification in the franchise. Turning to the balance sheet, total spot assets were $1.2 trillion. Standardized RWAs increased by $13 billion sequentially to $457 billion, as we actively supported clients.
```

*Rank 3 — `MS_2023_Q3_prepared_remarks_500_004`*

```
. The multi-year buildup of assets provide a foundational pipeline into our advisor led channel, evidence by fee-based flows of $22.5 billion in the third quarter alone. Asset management revenues of $3.6 billion increased 7% year-over-year. Higher average assets and the impact of cumulative positive fee-based flows over the past year drove the increase. Transactional revenues excluding DCP were $820 million, up 7% year-over-year. Results reflect opportunistic deployment of new capital by retail clients into alternatives, particularly into private equity and private credit. Bank lending balances roughly flat versus the prior quarter. Growth in mortgages and tailored lending offset paydowns and securities-based lending. Total deposits of $340 billion remain stable, compared to the prior quarter. Still, the deposit mix has shifted as clients continue to allocate rate-sensitive cash to higher-yielding cash alternatives available on the platform, including our expanded savings offering. In addition, the quarter saw consistent positive monthly inflows into equity markets from sweep balances, ongoing evidence of the improvement of the retail client sentiment. Net interest income was $2 billion. The sequential decline reflects a continued shift in the deposit mix. Looking towards the rest of this year, based on where we exited the quarter, we expect NII to trend lower. The magnitude will be a function of our deposit mix and the trajectory of rates. The wealth management business model is focused on steady asset aggregation, delivering strong solutions and advice to clients, while growing durable fees and expanding margin through the cycle. We are continuing to invest in our industry-leading position and the sustainability of our long-term growth. As the backdrop recovers, advisors remain well-positioned to capture greater asset opportunity supported by our multi-channel model that was built to attract new client relationships. Turning to investment management, revenues of $1.3 billion increased 14%, compared to the prior year, supported by higher asset management revenues. Total AUM ended at $1.4 trillion. Long-term net outflows of approximately $7 billion were driven predominantly by headwinds to our [Technical Difficulty] active equity growth strategies, which continue to see redemption consistent with the industry. Including the segment's outflows, year-to-date long-term flows across the franchise were slightly positive. Within alternatives and solutions, we continue to see demand for parametric customized portfolios across both equity and fixed
```

*Rank 4 — `MS_2023_Q1_prepared_remarks_500_004`*

```
18%. Over time, we believe clients will reinvest these balances across more assets when the market outlook improves. In the interim, given our broad product offerings, clients are choosing to invest in cash with Morgan Stanley through the cycle, positioning us to provide them with more reinvestment choices down the road. Net interest income was $2.2 billion, up 40% year-over-year. Results reflect the impact of higher interest rates and lower sweep balances. Fee-based flows of $22 billion were strong. Asset management revenues were $3.4 billion, down 7% versus last year, reflecting lower market levels. Transactional revenues were $921 million. Excluding the impact of DCP, revenues were down 12% versus last year due to fewer new issuance opportunities and reduced activity levels compared to the beginning of 2022. Lending balances declined this quarter to $144 billion, led by pay-downs in securities-based lending, reflecting the higher interest rate environment. Importantly, our strategy is working and we are seeing channel migration from workplace to adviser-led. Adviser-led flows, originating from workplace relationships reached $28 billion in this quarter alone, double versus this time last year and this compares to the approximate $50 billion we saw annually over the past 3 years. Furthermore, almost 90% of these flows were from assets held away, also consistent with what we have seen historically. Our strategy remains in place to best serve our clients and support the firm’s path to reach $10 trillion in client assets. Moving to Investment Management, revenues of $1.3 billion declined 3% year-over-year, primarily on lower AUM due to the decline of asset values and the cumulative effect of outflows over the prior year. Total AUM ended at $1.4 trillion. Long-term net outflows were $2.4 billion as equity outflows moderated in the quarter. In fixed income, outflows in floating rate loans were partially offset by high yield and emerging markets. Finally, alternatives and solutions delivered strength, driven mostly by demand for Parametric’s fixed income customized portfolios as well as inflows into private credit. Liquidity and overlay services had inflows of $13.9 billion. Positive liquidity inflows of $37 billion were partially offset by outflows related to a single client relationship. Asset management and related fees decreased versus the prior year to $1
```

*Rank 5 — `BK_2023_Q4_prepared_remarks_500_007`*

```
under management of $2 trillion increased by 8% year-over-year, reflecting higher market values and the weaker dollar, partially offset by cumulative net outflows. In the quarter, we saw $7 billion of net inflows into short-term strategies and $4 billion of net inflows into long-term active strategies, while we saw $10 billion of net outflows from index strategies. Wealth management client assets of $312 billion increased by 16% year-over-year, reflecting higher equity market values and cumulative net inflows. Page 12 shows the results of the other segments. Total revenue improved year-over-year, primarily reflecting the absence of a net loss from repositioning the securities portfolio recorded in the fourth quarter of 2022, and expenses of $693 million included $505 million related to the FDIC special assessment. Having reviewed our results, I will now turn to Page 14, and our current outlook for 2024. We're entering the year on a strong footing and we set ourselves up determined to at least break even from an operating leverage perspective. Considering our healthy pipeline across the businesses, we expect fee revenue growth to turn positive in 2024. With regards to net interest revenue, our expectation for an approximately 10% decrease year-over-year is based on the assumption of market-implied forward interest rates and we assume ongoing quantitative tightening puts further downward pressure on deposit balances. We intend to keep expenses excluding notable items, roughly flat in 2024. And finally, with regard to capital management, we expect to return north of 100% of 2024 earnings to common shareholders through dividends and buybacks. As Robin discussed earlier, 2023 was a foundational year for us. We took decisive actions to demonstrate some early evidence of our ability to deliver stronger financial performance, and importantly, we've developed a clear roadmap for our multi-year transformation. Over the next couple of slides, we'll provide you our medium-term financial targets for the firm and some of the most impactful actions we're taking to keep delivering on our goals. Page 15 summarizes our consolidated targets. It is our goal to improve the firm's pre-tax margin to 33% and our ROTCE to 23% over the medium-term, while maintaining a strong balance sheet. I'll double-click on our business segments in a moment, but along our three strategic pillars, there are a number
```

verdict: unfaithful

failure mode: company misattribution — BNY Mellon (BK_2023_Q4) reported as Bank of America, ticker printed beside the wrong name

notes: BLK (ch1) and MS (ch2/ch3/ch4) figures all correct. Again "Bank of America (BK)" for ch5 = BK_2023_Q4, BNY Mellon — the same substitution as item 5 in a different condition. The answer prints the BK ticker beside the wrong name, so the mechanism is visible: it is mapping the ticker to a name.

---

## 7. `ref_them_04` / `chunk500_hybrid_enriched`

- **condition:** chunk500_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_them_04
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Generated answer, verbatim:**

```
Based on the provided context, the banks described their progress on positive operating leverage as follows:

*   **Bank of America** achieved 170 basis points of operating leverage in 2023. This was driven by heightened quarterly expense levels being lowered throughout the year due to good expense discipline and headcount reductions, even while continuing investments in growth.
*   **Fifth Third Bank** stated that while the carryover effect of their Risk-Weighted Asset (RWA) diet made full-year positive operating leverage unfeasible for 2023, they anticipated returning to positive operating leverage in the second half of 2024. By late 2024, they confirmed they had returned to positive operating leverage in the fourth quarter on both a sequential and year-over-year basis.
*   **U.S. Bancorp** delivered 190 basis points of positive operating leverage in the fourth quarter of 2024. They guided for positive operating leverage of at least 200 basis points year-over-year for the first quarter of 2025 and greater than 200 basis points for full-year 2025 (excluding security gains or losses).
*   **M&T Bank** expressed confidence in achieving positive operating leverage for 2025, estimating it would be in the neighborhood of 150 to 200 basis points.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BAC_2023_Q4_prepared_remarks_500_002`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 2 — `USB_2024_Q4_prepared_remarks_500_003`*

```
5 forward-looking guidance on Slide 15. Starting with the first quarter 2025 guidance, net interest income is expected to be relatively stable to the fourth quarter of 2024, excluding the impact of fewer days. As a reminder, the first quarter has two fewer days than the fourth quarter. Total non-interest expense is expected to be relatively stable to the fourth quarter level of approximately $4.2 billion as adjusted. We expect to deliver positive operating leverage in the first quarter of 200 basis points or more on a year-over-year basis. I'll now provide full-year 2025 guidance. Total revenue growth on an adjusted basis is estimated to be in the range of 3% to 5% compared to the full year 2024. We expect to achieve positive operating leverage excluding the impact of security gains or losses of greater than 200 basis points for the full year. I'll now hand it back over to Andy for closing remarks.

Andy Cecere: Thanks, John. 2024 was a pivotal year for the company in many ways and it marked a very important inflection point in our story. Going into the year, there was much uncertainty with respect to the broader macroeconomic environment, persistent inflation, significant rate volatility, political and regulatory headwinds to name a few, but we effectively managed through the changes and most importantly executed on our strategic objectives. Fourth quarter results showcase our commitment to execution which was highlighted by our delivery of 190 basis points of positive operating leverage. As credit quality continued to stabilize and we prudently manage our capital position, it was effective balance sheet management, our financial discipline, and expanding interconnectedness across the franchise that enabled us to fully deliver the strong results we did this quarter and fully expect that momentum to continue into 2025. Finally, I'd like to extend our thoughts to those impacted by the devastating and ongoing wildfires in Los Angeles. We are closely monitoring the situation and have teams across the Bank involved in our collective response efforts to help best support our employees, customers, and their communities. Let me close by thanking our employees for their continued dedication to our clients, communities, and shareholders in what was a meaningful year for the company. We will now open up the call for Q&A.
```

*Rank 3 — `FITB_2023_Q4_prepared_remarks_500_002`*

```
profitability. Expense discipline, strong returns, and positive operating leverage remain core areas of focus for Fifth Third. Supported by our technology modernization investments and a focus on leaning out key value streams, we reduced full-time equivalent employee headcount by 4% from our peak in 2023 to the end of the year without the need for a company-wide expense program. The run rate benefits of these efforts put us in a position to sustain the peer-leading annualized expense growth that we have averaged the past several years, even as we continue to invest for growth. While the carryover effect of the RWA diet makes it unfeasible for the full year, we do anticipate returning to positive operating leverage in the second half of 2024. The third point I'd like to highlight is about growth. Our strategies have been consistent, building out our Southeast markets, producing a strong fee to total revenue mix, and leveraging software that differentiates our product offerings and improves productivity. These are multi-year investments that cannot be replicated easily by competitors to one to two years of hiring a few new branches or small tuck-in acquisitions. In 2023, we opened 37 new branches concentrated in the Southeast, bringing us to 107 opened over the past five years. We plan to open another 31 branches in the Southeast in 2024. As a portfolio, these branches have continued to outperform our expectations on both household acquisition and deposit growth and should provide a tailwind for several years forward. We also continue to invest in treasury management, wealth and asset management, and capital markets. All three of these businesses grew for us in 2023. We expect mid-to-high single-digit growth in each in 2024. In treasury management, our acquisitions of Rize and Big Data Healthcare and the launch of Newline, our embedded payments business, should continue to support peer-leading performance. In wealth and asset management, Global Finance recently named our Private Bank as the Best US Regional Private Bank for the fifth consecutive year and Best Private Bank for Entrepreneurs globally for the first time. In our capital markets business, we have seen more robust activity levels to start the year, including an M&A pipeline that is 1.5 times the full-year revenue target embedded in our guidance. Overall, we expect 2024 to be a solid year of improving revenue trends and continued to expense discipline. Given what we believe to be a less certain outlook than the markets would imply,
```

*Rank 4 — `FITB_2024_Q4_prepared_remarks_500_001`*

```
growth, regulation and capital markets activity all changed significantly. Despite this, we delivered strong and predictable results. Our full year return on assets of 1.17%, return on tangible common equity, excluding AOCI, of 14%, and efficiency ratio of 57.1%, all finished among the top in our peer group. We were one of only a few banks to achieve full year guidance for NII, fees, expenses, PPNR and net charge-offs that was provided back in January. Our NIM inflected in the first quarter as we said it would. NII inflected in the second quarter as we said it would. We returned to positive operating leverage in the fourth quarter on both a sequential and a year-over-year basis, as we said we would. We resumed share repurchases in the second quarter, and raised our dividend in the third quarter. In total, for the year, we returned $1.6 billion of capital to our shareholders, while also increasing our CET1 ratio by more than 20 basis points. Competitive barriers are exceedingly difficult to build in the banking business. The only way we know how to build them is to invest continuously in a limited number of strategies over a sustained period of time. Our growth strategies are well-known and have been consistent for several years now. Their impact is evidenced in our 2024 results and reflected in the third-party accolades that we received during the year. Our investments to expand our Southeast branch footprint and in our differentiated momentum banking platform continued to drive outsized growth in granular low cost deposits. For the second consecutive year, Fifth Third was number one among all large banks in year-over-year retail deposit growth measured on a cap deposit basis. We generated year-over-year household growth of 2.3%, punctuated by 6% growth in the Southeast. And we also won JD Power's Retail Banking Satisfaction Award for the Florida region. The 31 de novo branch locations we opened in 2024 and the 60 new branches we expect to open in the Southeast in 2025, should set us up well to continue to gain market share. On lending, our investments to generate granular diversified loan originations without compromising on pricing or risk gained momentum throughout the year and contributed to a strong finish. On a sequential end-of-period basis, we grew loans 3%, or a bit more than 1% faster than the HA. Growth was balanced
```

*Rank 5 — `MTB_2024_Q3_qa_500_011`*

```
ble.

Daryl Bible: Yes. So we are still putting 2025 together. I do believe we will have positive operating leverage for 2025. Whether we are 150 or 200, I think you're in the neighborhood of where plan will end out, but we are on 100% have kind of figured out and everybody's agreed to it, but we will get there. I feel very confident we will get there from that. If you look at the expenses that we guided, they were up a little bit in the fourth quarter. It is mainly due to projects that we have. We have a fair amount of projects going on in the company, and we are making a lot of progress. We do have an increase there. The other thing that we are doing is -- we've had a pretty good year from a performance perspective, both financially. We made good progress on our asset quality and good loan and deposit growth and just improving and getting good some of our priorities accomplished. So we actually are increasing our corporate-wide incentives in the fourth quarter for payout for everybody for a good year. That said, I still feel that 2025 is going to be a better year than 2024 to be honest with you. We continue to have a lot more work to do and make progress. But we have a lot of positive momentum now and need to reward the people that are making it happen in the company and feel good about that.

John Pancari: Great. All right. Thank you. That's helpful. And then on the credit side, your loan loss reserve ratio as a percentage of loans ticked down a bit or so this quarter, I guess around 162 basis points where it stands now. Where do you see that trending here? You cited the expected decline and criticized that you will see in the quarter and then a pretty good trajectory there. Fair to assume continued modest decline here in that ratio? Is that fair to assume as you look out?

Daryl Bible: Yes. I think when you look at it, this past quarter we had some good macro factor positives with creepy being much more positive and that helped drive and downward drop in criticized, which is good. I think as you look forward though, we are growing all of our lending categories, so you have a mix change that you're seeing occur in the balance sheet. And that mix change is more heavy on the consumer side. Consumers definitely have for the most part, higher overall spreads and
```

verdict: faithful

failure mode: scope drift — three of four items outside the asked window, but correctly dated

notes: Same question as item 3. All four banks correct and periods stated correctly (BAC ch1, FITB ch3+ch4, USB ch2, MTB ch5). Three of four items are 2024/2025, outside the asked window — but here the answer says so rather than relabelling them to fit. Same label as item 3; not the same quality.

---

## 8. `ref_them_01` / `chunk200_bm25`

- **condition:** chunk200_bm25
- **arm:** text_only
- **question_id:** ref_them_01
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did banks report the impact of the FDIC special assessment on their expenses in late 2023 and the first half of 2024?

**Generated answer, verbatim:**

```
Based on the provided context, banks reported the impact of the FDIC special assessment as a significant driver of expense increases or noted its absence when comparing periods:

*   **M&T Bank (MTB):** In Q1 2024, expenses included $29 million related to the FDIC special assessment. This was compared to $5 million in Q2 2024. When calculating the adjusted efficiency ratio for Q2, they excluded this impact.
*   **JPMorgan Chase (JPM):** In Q4 2024, expenses were down year-on-year predominantly due to the absence of the $2.9 billion FDIC Special Assessment that had been recorded in the prior year (Q4 2023).
*   **Citigroup (C):** In Q4 2024, expenses were down 18% largely driven by the absence of the FDIC special assessment from the prior year. For full-year 2023, they reported that excluding the FDIC special assessment and divestiture-related impacts, expenses were $54.3 billion.
*   **Wells Fargo (WFC):** In Q1 2024, non-interest expense increased 5% from a year ago, driven in part by the FDIC special assessment. They noted that excluding this specific expense, their full-year 2024 non-interest expense guidance remained unchanged at approximately $52.6 billion.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MTB_2024_Q2_prepared_remarks_200_011`*

```
million to $764 million, reflecting seasonally elevated expenses in the first quarter, offset by the full quarter impact of annual merit increases. The second quarter included $5 million related to the FDIC special assessment compared to $29 million in the prior quarter. Other cost of operations decreased $18 million to $116 million from lower supplemental executive retirement costs and lower losses on lease terminations. The adjusted efficiency ratio, excluding the impact of the FDIC special assessment, was 55.1% compared to 59.6% in the first quarter. Next, let's turn to Slide 16 for credit. Net charge-offs for the quarter totaled $137 million or 41 basis points, down from 42 basis points in the linked quarter. The three largest charge-offs were $40 million combined and represent C&I loans that span industries including services, manufacturing and retail. The CRE charge-offs, including charge offs within the office portfolio, remain at manageable levels through the first half of the
```

*Rank 2 — `JPM_2024_Q4_prepared_remarks_200_009`*

```
-on-year, driven by the impact of lower rates, largely offset by balance sheet actions, primarily securities reinvestment activity. NII was a net loss of $30 million compared to the net loss of $668 million in the prior year, driven by lower net investment securities losses this quarter. And expenses of $550 million were down $3 billion year-on-year, predominantly driven by the absence of the FDIC Special Assessment of $2.9 billion in the prior year. With that, let's pivot to the outlook, starting with NII on Page 9. We expect 2025 NII ex-markets to be approximately $90 billion. Going through the drivers, as usual, the outlook assumes that rates follow the forward curve. It's worth noting that the NII decrease is driven by both the cut expected in 2025 and the impact of the 100 basis points of cuts in the back half of 2024. You can see on the page that
```

*Rank 3 — `C_2024_Q4_prepared_remarks_200_010`*

```
and RoTCE of 6.1% or $19.6 billion of revenues generating positive operating leverage for the firm and in each of our businesses. Total revenues were up 12% driven by growth in each of our businesses and a smaller impact of Argentina currency devaluation. Net interest income excluding markets was roughly flat with growth in USPB and wealth offset by declines in corporate other and banking. Non-interest revenues excluding markets was up 40% driven by continued strong fee momentum across services, banking and wealth along with lower partner payments in USPB as well as a smaller impact of Argentina currency devaluation. And total markets revenues were up 36%. Expenses were $13.2 billion, down 18%, largely driven by the absence of the FDIC special assessment and restructuring charge in the prior year. Excluding the impact of the FDIC special assessment and divestiture related impacts, expenses were down 7% driven by the absence of the restructuring charge in the prior year and savings associated
```

*Rank 4 — `C_2023_Q4_prepared_remarks_200_017`*

```
of our investments in digital acquisition and customer engagement. Total revenues, excluding divestitures, came in at $77.1 billion, below our guidance of $78 billion to $79 billion for the year, largely due to the impact of the Argentina devaluation, softer markets performance, particularly in December and losses on loan hedges. However, NIIX ex-markets came in at $47.6 billion in line with our guidance. Despite the challenging environment and the impact of the Argentina devaluation, we grew firm-wide revenues by approximately 4% ex-divestitures in line with our Investor Day target, demonstrating the benefit of our diversified business model and the investments we've been making. On slide nine, we show full year expense trends from 2021 to 2023, excluding the FDIC special assessment and divestiture-related impacts, full year expenses were $54.3 billion for 2023 in line with our guidance. As I mentioned, this includes roughly $780 million
```

*Rank 5 — `WFC_2024_Q1_prepared_remarks_200_012`*

```
Slide 7, first quarter non-interest expense increased 5% from a year ago, driven by higher operating losses, the FDIC special assessment, an increase in revenue related compensation, predominantly due to higher investment advisory fees in our wealth and investment management business and higher technology and equipment expense. These increases were partially offset by the impact of efficiency initiatives, including lower professional and outside services expense, which declined 10% from a year ago. The higher operating losses were driven by customer remediation accruals for a small number of historical matters that we are working hard to get behind us. The increase in personnel expense from the fourth quarter was driven by approximately $650 million of seasonally higher expenses in the first quarter, including payroll taxes, restricted stock expense for retirement eligible employees and 401(k) matching contributions. Not including expense for the FDIC special assessment in the first quarter, our full year 2024 non-interest expense guidance is unchanged and is still expected to be approximately $52.6 billion
```

verdict: faithful

failure mode: none

notes: All four companies and both quarters correct (MTB ch1, JPM ch2, Citi ch3/ch4, WFC ch5). The M&T sentence inverts the chunk's framing but still assigns $29m to Q1 and $5m to Q2 correctly. Directly responsive; "offtarget" here reflects retrieval targeting, not the answer.

---

## 9. `ref_them_15` / `chunk500_bm25_enriched`

- **condition:** chunk500_bm25_enriched
- **arm:** enriched
- **question_id:** ref_them_15
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How much did banks say they were spending on technology over 2023 and 2024, and how did that spend and related G&A expense change?

**Generated answer, verbatim:**

```
Based on the provided context, there is no specific dollar amount stated for total bank technology spending across 2023 and 2024. However, JPMorgan indicated in its Q3 2023 earnings call that it was still going through its budget process but remained "in the ballpark" of a consensus estimate of **$88 billion** for investment/tech spend over the next year (implying 2024).

Regarding changes in spending and G&A expense:
*   **JPMorgan:** In Q3 2023, management noted that tech spending includes "sine qua non" items like cybersecurity and data center resiliency. By Q2 2024, a question referenced JPMorgan spending **$17 billion a year** to improve the company (including digital banking, back-office automation, and AI).
*   **BlackRock:** In Q1 2024, total expense increased 8% year-over-year. G&A expense increased 6% due to the timing of technology investment spend in the prior year. In Q3 2024, BlackRock expected a low to mid-single digit percentage increase in core G&A expense for 2024, with Q4 reflecting planned technology investment spend consistent with Q3 levels.
*   **Fifth Third Bank (FITB):** In Q1 2023, the bank reported a continued ramp-up in technology costs associated with core conversion projects (new ledger, CD platform, nCino). The total multi-year spend for these conversions was estimated to reach as much as **$100 million**, with less than half being capitalized.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BLK_2024_Q1_prepared_remarks_500_002`*

```
awards that vest in the first quarter of each year. We continue to estimate that 25% is a reasonable projected tax run rate for the remainder of 2024, though the actual effective tax rate may differ because of non-recurring or discrete items or potential changes in tax legislation. First quarter base fee in securities lending revenue of $3.8 billion was up 8% year-over-year and up 5% sequentially driven by the positive impact of market beta on average AUM and positive organic base fee growth. On an equivalent day count basis, our annualized effective fee rate was 3/10 of a basis point lower compared to the fourth quarter. This was mainly due to the relative outperformance of lower fee U.S. equity markets, client preferences for lower fee U.S. exposures and lower securities lending revenue. Performance fees of $204 million increased from a year ago, primarily reflecting higher revenue from alternatives. Quarterly technology services revenue was up 11% compared to a year ago, reflecting sustained demand for our Aladdin technology offerings. Annual contract value or ACV increased 9% year-over-year. Beginning in the first quarter of 2024, earnings recognized from minority investments accounted for under equity method will be presented as part of our non-operating results. Advisory and other revenue increased from a year ago, primarily reflecting this change. In addition, as many of you know, we updated the presentation of expense line items by including a new sales asset and account income statement caption. This category includes distribution and servicing costs, direct fund expense and sub-advisory and other sales asset and account-based expense. Sub-advisory and other expense, which are variable non-compensation expenses associated with asset and revenue growth was previously reported within general and administration expense. We believe this change provides investors a clearer view of both BlackRock's variable non-compensation expense and G&A, which represents more fixed costs. It represents how we'll execute on our financial rubric of aligning investment spend with our highest conviction growth areas, variabilizing more of our expense base and generating fixed cost scale. Total expense increased 8% year-over-year, reflecting higher compensation, G&A and sales asset and account expense. Employee compensation and benefit expense was up 11%, primarily reflecting higher incentive compensation as a result of higher operating income and performance fees. G&A expense increased 6% due to the timing of technology investment spend in the prior year. Sequentially
```

*Rank 2 — `FITB_2023_Q1_qa_500_011`*

```
, the March Madness at all impact the progression of the conversion of the timing of the expected conversion? And then lastly, can you maybe help us with the sizing up of the cost of the conversion and how much is expected to be capitalized?

James Leonard: Yes, John it’s Jamie. Thanks for the question. As you saw in the expense numbers, this quarter, we did have continued ramp up in technology cost that ultimately is a good thing, because it means we’re getting things accomplished. And we continue to track on all of our deadlines for this year. We have new ledger going in in the third quarter, followed by CD platform as well as continued rollout of the nCino platform across the commercial business. And then we’re really at this point about halfway through the game, because 2024, 2025 has additional deadlines associated with it on ATM and TM billing as well as the core checking conversion, but so far, so good. We do capitalize and follow the appropriate accounting standards on the total spend here. I think the spend over a multiyear period could reach as much as $100 million, of which a little less than half would be capitalized. And from there, I think you just continue to see us invest in cloud core technology. And that’s part of what’s driving that expense growth. You’re seeing both in the first quarter and for the year.

John Pancari: Got it. Thank you, Jamie very helpful.

Operator: Our next question comes from the line of Manan Gosalia from Morgan Stanley. Please proceed.

Manan Gosalia: Hey, good morning. I was wondering if you could give us some more color on why you expect deposits to grow as we get into the remainder of the year, what are you seeing in your underlying account openings and conversations with clients that gives you the confidence in that outcome? I guess my question is, why shouldn’t some of these new deposits just go back to the banks, where they have longer relationships? So once the volatility in the in the system settles down.

Timothy Spence: Yes good question. So I don’t think we took a lot of deposit share from banks that were non-operational in nature. The new accounts that we opened Manan were linked to treasury management sales and inclusive of our embedded banking business. And we’re had been on the sales pipeline, in some cases for as long as
```

*Rank 3 — `BLK_2024_Q3_prepared_remarks_500_004`*

```
expense increased 6% compared to a year ago, driven by higher direct fund expense. Direct fund expense increased 7% year-over-year and 6% sequentially, primarily as a result of higher average ETF AUM. Our as adjusted operating margin of 45.8% was up 350 basis points from a year ago, reflecting the positive impact of markets on revenue, significantly higher performance fees, and organic base fee growth. As markets improve, we've executed on our financial rubric, aligning controllable expense and organic growth, adding more resilience to our operating margin through greater variabilization of expenses and driving fixed cost scale. This approach is yielding profitable growth and operating leverage. In line with our guidance in January and excluding the impact of Global Infrastructure Partners, Preqin and related transaction costs, at present we would expect our headcount to be broadly flat in 2024. And we would also expect a low to mid-single digit percentage increase in 2024 core G&A expense. In line with this outlook, we would also expect Q4 core G&A to reflect execution of planned technology investment spend at levels more consistent with Q3 and seasonal increases in marketing spend. We welcomed approximately 400 new colleagues to BlackRock following the close of the GIP transaction. Inclusive of the GIP acquisition impact, at present, we'd expect full-year core G&A expense growth to be closer to the high end of the previously communicated range of a low to mid-single digit percentage increase. Our capital management strategy remains first to invest in our business, to either scale strategic growth initiatives or drive operational efficiency, and then to return excess cash to shareholders through a combination of dividends and share repurchases. At times, we may make inorganic investments where we see an opportunity to accelerate growth and support our strategic initiatives. At the closing of the GIP transaction, we issued and delivered approximately 6.9 million shares of BlackRock common stock, subject to a two-year lockup period. Approximately 30% of the total consideration for the transaction or 5 million shares is deferred and is expected to be issued in approximately five years based on achievement of certain performance milestones. We repurchased $375 million worth of common shares in the third quarter. At present, based on our capital spending plans for the year and subject to market and other conditions, we still anticipate repurchasing at least $375 million of
```

*Rank 4 — `JPM_2023_Q3_qa_500_014`*

```
businesses in different ways. Some have been quite successful, like Stripe in payments. And so we want to be very good and very competitive. Some of that tech spending is things which are almost a sine qua non, which is cybersecurity, data center resiliency, regulatory requirements and things like that, which we simply are going to do and be very, very good at to protect the company.

Mike Mayo: As it relates to AI specifically, which is the talk of the town, I guess the consensus among people outside the banking industry is that banks will not win that battle, including JPMorgan. You won't control the front end. What are you doing with AI to make a difference now? Or is this simply a moonshot?

Jamie Dimon: Well, I don't agree with that statement. Banks have an extraordinary amount of proprietary data in addition to when you do like a large language model, that's public data. It's looking at everything in the Internet or everything that's ever been published or something like that. But AI is an extraordinarily good tool to use. We just put a woman who is running at our table. So it's data analytics, AI, et cetera. And there are multiple types of AI. So we use AI for risk, fraud, marketing, prospecting. And the management team is getting better and better and say, how can we use data to do a better job to reduce errors, to serve clients better, to have a salesperson have co-pilots. They know why even the clients calling us something like that. And so we simply have to do it. Does it create opportunity for disruptors to come in? Yeah, of course. That’s always been true with technology and -- but we'll be quite good at it.

Mike Mayo: And then lastly, I think you had made a mention at a conference about investment spend or tech spend over the next year. Where do you stand on that?

Jeremy Barnum: Yeah. No, because you did ask a little bit about the expense outlook for next year. So I think at the conference, we said I think the consensus was $88 billion, but we're still going through budget process, et cetera, et cetera. So that's still true. I think we're still kind of in the ballpark, but I would say at the margin, there
```

*Rank 5 — `JPM_2024_Q2_qa_500_012`*

```
, well, we might want to have a lot more capital here. I mean at some point, if you're spending $17 billion a year to improve the company, if you're gaining share with digital banking, if you're automating the back office, if you're moving ahead with AI, if you're doing all these things that I think you say others aren't doing, why wouldn't those returns go higher over time? Or do you just assume you'll be competing those benefits away? Thanks.

Jeremy Barnum: Yes. I mean, I think in short, Mike, and we've talked about this a lot and Jamie has talked about this a lot, it is a very, very, very competitive market. And we are very happy with our performance. We are very happy with the share we've taken. And 17% is like an amazing number actually. And like to be able to do that, given how robust the competition is from banks, from non-banks, from US banks, from foreign banks and all of the different businesses that we compete in, is something that we're really proud of. So the number has a range around it, obviously. So it's not a promise, it's not a guarantee and it can fluctuate. But we are very proud to be in the ballpark of being able to think that we can deliver it, again assuming a reasonable outcome on Basel III endgame. But it's a very, very, very competitive market across all of our products and services and regions and [line] (ph) segments.

Mike Mayo: All right. Thank you.

Operator: Next, we'll go to the line of Betsy Graseck from Morgan Stanley. Please go ahead.

Betsy Graseck: Hi, Jeremy.

Jeremy Barnum: Hi, Betsy.

Betsy Graseck: So I did want to ask one drill-down question on 2Q, and it is related to the dollar amount of buybacks that you did do. I think in the press release, right and the slide deck, it's $4.9 billion common stock net repurchases. So the question here is what's the governor for you on how much to do every quarter? And I mean I understand it is a function of okay, how much do we organically grow. But even with that, so you get the organic growth which
```

verdict: faithful

failure mode: none

notes: Opens by stating that no total tech-spend figure exists — correct. $88bn is correctly framed as a consensus number JPM was still budgeting against (ch4), and $17bn is attributed to the questioner rather than to management (ch5). BLK (ch1/ch3) and FITB (ch2) figures right. Careful about who said what.

---

## 10. `ref_them_15` / `chunk500_dense_enriched`

- **condition:** chunk500_dense_enriched
- **arm:** enriched
- **question_id:** ref_them_15
- **category:** thematic
- **case:** B
- **outcome label:** answered_ungrounded
- **coverage@5:** 0

**Question:**

> How much did banks say they were spending on technology over 2023 and 2024, and how did that spend and related G&A expense change?

**Generated answer, verbatim:**

```
Based on the provided context, here is the information regarding technology spending and General & Administrative (G&A) expenses for 2023 and 2024:

**Technology Spending:**
*   **Citigroup (C):** Invested over **$12 billion** in technology in 2023. This was part of a broader transformation effort where roughly 30% of investments over the last three years were in technology, with a noted shift from consulting expenses to technology and compensation in 2023.
*   **Bank of America (BAC):** Increased annual technology initiatives spending from approximately **$2.5 billion** to **$3.8 billion** over the decade leading up to the discussion (referenced in Q2 2023 context). The text does not provide a specific total for 2024 tech spend, but notes continued investment in new tech initiatives and digital transformation.
*   **M&T Bank (MTB):** Did not specify a dollar amount for technology spending in 2023 or 2024, but noted that they spent "a fair amount of money" on significant projects in 2024 and are doing the same in 2025. They identified cloud/data centers, a new general ledger system, and commercial services as major investments.

**G&A / Non-Interest Expense Changes:**
*   **Bank of America (BAC):** Reported adjusted expense of **$15.6 billion** in Q4 2023, which was down $199 million from the third quarter and only $94 million higher than Q4 2022. For Q1 2024, they expected expenses to rise to approximately **$16.4 billion** due to seasonal elevation, payroll taxes, merit increases, and revenue-related costs. They expect quarterly expense to decline from Q1 2024 as the year progresses.
*   **Citigroup (C):** Full-year 2023 expenses were **$54.3 billion**, in line with guidance. This included roughly $780 million in restructuring costs and approximately $730 million in additional severance costs. Expense growth was driven by transformation, business-led investments, volume-related expenses, and risk/controls investments, partially offset by productivity savings.
*   **Wells Fargo (WFC):** Reported non-interest expense of **$55.6 billion** in 2023 (including a $1.9 billion FDIC special assessment). Excluding the assessment, expenses were **$53.6 billion**. For 2024, they expect severance to be approximately $1.3 billion lower, revenue-related expenses to increase by at least $300 million, and all other expenses to be flat. They anticipate approximately **$2.7 billion** in gross expense reductions from efficiency initiatives in 2024.
*   **M&T Bank (MTB):** The context does not provide specific dollar figures for total G&A or non-interest expense for 2023 or 2024, only qualitative statements about disciplined spending and major investment projects.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BAC_2023_Q4_prepared_remarks_500_010`*

```
book. And that assumes no expected change in balance sheet levels or mix relative to our baseline forecast, and 93% of that sensitivity is driven by short rates. The 100 basis point down scenario is $3.1 billion. Let's turn to expense and we'll use Slide 11 for the discussion. And we reported $15.6 billion in adjusted expense this quarter, which excludes the FDIC assessment. This was in line with our projection from last quarter and down $199 million from the third quarter, driven by reductions in headcount earlier in the year and seasonally lower revenue-related expense. These reductions outpace the continued investments that we're making to drive growth. Our average headcount was down from the third quarter to 213,000 people, and that's good work after peaking at 218,000 last January. We lowered our headcount through the year by 5,000 and did so without taking an outsized severance charge as we used attrition to lower our headcount along the way. One more point to acknowledge the good work of our teams on expense, Q4 '23 adjusted expense of $15.6 billion is only $94 million higher than the fourth quarter of '22. And just remember, we began 2023 with a $125 million lift in quarterly FDIC expense. So through some good operational excellence work and otherwise, we've managed through all of the additional costs of investments in new tech initiatives and merit and financial center openings, as well as some stronger revenue and higher marketing costs. As we look forward to next quarter, we expect to see the more typical Q1 seasonal elevation in expense of $700 million to $800 million compared to Q4. So we believe expense will be around $16.4 billion in the first quarter. That includes elevated payroll tax expense and the expected costs of higher revenue in both sales and trading and wealth management, as well as merit cost increases. And as we move through 2024, we expect the quarterly expense to decline from Q1, reflecting a drop in the elevated payroll tax expense and revenue changes, as well as some additional operational excellence initiative work. Continued digital transformation and adoption is also going to help us as we go through the year. Now turn to credit, and I'll use Slide 12 for that. Provision expense was $1.1 billion in the fourth quarter and it included an $88 million reserve release due to a modestly improved macroeconomic
```

*Rank 2 — `MTB_2024_Q4_qa_500_005`*

```
separate question on the 4 priorities you laid out on Slide 23. As we think about the expense outlook for this year, you have some larger tech projects going on, does that set the stage for sort of lower expenses, more efficiencies over the next few years? Or do you think the level of investment spend is likely to continue for the medium term as we think about where efficiency ratio or op lev are headed?

Daryl Bible: Yes. So when you look at our expenses, first, I want to just thank all of my colleagues in the company. We had 2024, and we spent a fair amount of money on some significant projects. We're doing the same thing again in 2025. But we're very disciplined here and doing what's best for the corporate good of the company. So I really appreciate everybody taking that sentiment and doing that. When I look at 2025 and beyond, right now, we have 6, I would say, major investments going on in the company. Out of those 6 investments, I call 3 of them as really big investments that will happen once every several decades. So if you look at cloud and data center -- 3 new data centers, you don't do that very often. That's probably every 10 to 20 years. We're putting in a new general ledger system, a financial system, that's also probably every 10 or 20 years. From a commercial perspective, we've really close to finishing up our corporate services and fulfillment of how we manage risk in that area. Still working on commercial services. But once we get that done and completed, that won't get changed probably for another decade or so. So those are really big investments. But once we get them done, I think those will fall off. I think you have other investments that we're making as well at the same time as we invest in data and analytics. We're always going to be investing in data analytics. That's just core to the customers, how we serve our customers and all that that is critical of what we do. Our digital is basically table stakes. We have to continue to improve and offer really good digital services and all that. So that's good. Treasury management and other things that support our clients are things we will continue to invest in over time. So what I look at it is we got a big comp we're going through right now with some major projects.
```

*Rank 3 — `C_2023_Q4_prepared_remarks_500_007`*

```
uation, we grew firm-wide revenues by approximately 4% ex-divestitures in line with our Investor Day target, demonstrating the benefit of our diversified business model and the investments we've been making. On slide nine, we show full year expense trends from 2021 to 2023, excluding the FDIC special assessment and divestiture-related impacts, full year expenses were $54.3 billion for 2023 in line with our guidance. As I mentioned, this includes roughly $780 million of restructuring costs associated with our organizational simplification and additional severance costs of approximately $730 million, which included actions to address stranded costs and start to right-size the businesses. Relative to the prior year, expense growth continued to be driven by transformation and business-led investments, volume-related expenses and other investments in risk and controls and technology, partially offset by productivity savings and a reduction in expenses and legacy franchises within all other. Over the past few years, we've been investing across these themes, which has not only impacted the performance of the firm, but also the businesses. On slide 10, we show the components of our transformation and technology spend from 2021 to 2023. Over the past three years, we have invested significantly in our infrastructure, platforms, applications, processes and data. As you can see in the bar chart at the top of the slide, roughly 30% of our transformation investments over the last three years were in technology, with the remainder related to non-tech employees and consultants. In 2023, we've seen a shift from consulting expenses to technology and compensation as we've gotten deeper into the execution of our transformation. And you should expect to see this trend continue. In total, we invested over $12 billion in technology in 2023. Beyond transformation, our technology investments are also focused on digital innovation, new product development, client experience enhancements and areas that support our infrastructure like cloud and cyber. On slide 11, we show key consumer and corporate credit metrics. Across branded cards and retail services, approximately 80% of our card loans are to consumers with FICO scores of 680 or higher. And across both portfolios, NCL rates have reached pre-COVID levels, but we continue to be well reserved with a reserve to funded loan ratio of 7.7%. In our corporate portfolio, the majority of our exposure is investment grade, which is reflected in our low level of nonaccrual loans at 63 basis points of
```

*Rank 4 — `WFC_2023_Q4_prepared_remarks_500_009`*

```
in consumer banking and lending deposits, as well as continued mix shift from lower yielding products to higher yielding, deposits in our other deposit gathering businesses are expected to be relatively stable and market funding will replace the decline in consumer deposits as needed. We currently expect that net interest income will trough towards the end of this year. As we’ve done in prior years, we are also assuming the asset cap will remain in place throughout the year. Ultimately, the amount of net interest income we earn in 2024 will depend on a variety of factors, which many of which are uncertain, including the absolute level of rates, the shape of the yield curve, deposit balances, mix and pricing and loan demand. Turning to our 2024 expense expectations on Slide 19. We started our focus on efficiency initiatives three years ago and we’ve successfully delivered on our commitment of approximately $10 billion of gross expense saves. Through our efficiency initiatives we have reduced headcount every quarter since third quarter of 2020 and headcount is down 16% since the end of 2020. Looking at our expectations for this year and following the waterfall on the slide from left to right. We reported $55.6 billion of non-interest expense in 2023, which included the $1.9 billion FDIC special assessment. Excluding this item, expenses would have been $53.6 billion, which we believe is a good starting point for discussion of 2024 expenses. Looking at the next bar, we expect severance expense to be approximately $1.3 billion lower, driven by the $969 million expense we took in the fourth quarter for planned actions, we expect expenses to increase by at least $300 million due to higher revenue related expense, driven by wealth and investment management, revenue related expenses will ultimately be a function of activity and market levels, and therefore could be higher or lower than this estimate. At this point, we expect all other expenses to be flat, though there are significant efficiencies and increased investments included in this expectation. We expect approximately $2.7 billion of gross expense reductions in 2024 due to the efficiency initiatives. We highlight in the slide some of the areas where we anticipate additional savings and continue to believe we have more opportunities beyond 2024. Similar to prior years, the resources needed to address our risk and control work are separate from our efficiency initiatives and we will continue to make significant investments in our risk and control infrastructure. While we remain focused on executing on our efficiency
```

*Rank 5 — `BAC_2023_Q2_qa_500_002`*

```
last year to the fourth quarter this year, it gets you relatively flat year-over-year, and as your revenues flatten out because interest-rate movements flatten out, you'll see that as we decline in the quarters, that'll be strong. So, as we think about it - as we think about the forward, we think about the ability to control headcount and have expenses continue to come down, but they're going to stay at a level that's relatively consistent where we are now over time, and the goal is then to grow revenue faster than expense. We've been doing it for many decades, you can see that in our data. And - but the way we do it differs from five years ago to 10 years ago to last year, and that the ability to move the branch configuration around when we had 6,000 branches down to 4,000, or 3,900, 3,800, now it is different from 3,800 to where it might end up. And so, you should expect us to continue to engineer by applying massive amounts of technology. Erica saves a lot of transactional activity, Zelle saves a lot of transactional activity deposits by mobile phone saves a lot of activity. All that goes on, and then what we're offsetting with that is from the decade you talk about we probably went from $2.5 billion of technology initiatives a year to $3.8 billion, and we went - we have a lot more revenue that is compensated for, thinking about in the wealth management business, and those are things we fight all the time. So, we expect to manage expenses in-line with revenue. As we got to '19, we told you that we're going to have to start growing expenses at a modest growth rate relative to the revenue growth rate will outgrow the economy on revenue expense and grow a couple 100 basis points lower, it kind of going to be back in that mode frankly, it just with inflation they kicked up and now we have flattened them back out, and then we'll get back in sync as we move to '24 and beyond.

Alastair Borthwick: Glenn, look, the only thing I would just add to what Brian just said. We put up 16.2 in the first quarter, we were 16-ish this quarter obviously. We kind of feel like next quarter just with all the work that we've done
```

verdict: faithful

failure mode: date verified as though it were a figure — the answer normalises the context's "'22" to "2022"

notes: Every figure traces (Citi ch3, BAC ch1/ch5, MTB ch2, WFC ch4), companies and periods right, and the BAC decade figure correctly tagged "Q2 2023 context". The single flagged claim is "2022", from "$94 million higher than Q4 2022" — a correct reading of ch1's "$94 million higher than the fourth quarter of '22". Mechanism, checked in the scorer: extract_numeric_claims treats a date as a numeric claim, and Fix 2 exempts a trivial year ONLY when the question itself supplies it. This year came from the context, not the question, so it is verified like a quantity — and "2022" appears nowhere in the five chunks in that form. One correctly-read date decides the record.

---

## 11. `ref_unans_01` / `chunk500_bm25_enriched`

- **condition:** chunk500_bm25_enriched
- **arm:** enriched
- **question_id:** ref_unans_01
- **category:** unanswerable
- **case:** A
- **outcome label:** answered_ungrounded
- **coverage@5:** n/a (unanswerable; excluded from retrieval metrics)

**Question:**

> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Generated answer, verbatim:**

```
Northern Trust’s firm-wide assets under custody and/or administration were $48.8 trillion in the first quarter of 2024, representing a 5% increase year-over-year. In the first quarter of 2023, these assets stood at $46.6 trillion, which was up 2% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `STT_2023_Q1_qa_500_018`*

```
that that there is a range of revenue growth in our different fee categories. We've described back office as growing towards the -- traditional back office growing closer to the lower single-digit revenue growth. We've described middle and front office, which would include CRD at high single-digit growth. There will be years when it could be double-digit revenue growth. So that's what we said about that category -- this category. I think what we see in particular in software is the on-premise revenues over time will -- may not be as heavy, but we do see real momentum in the combination of the software enabled and SaaS. But all in, that should grow in the higher-single digit revenues typically though there'll be some range around that in a given year.

Vivek Juneja: Okay. And then going back to this question that's come up on the large amount of new business that remains to be installed in servicing, and you said you should see a pickup in 2Q. Ron and Eric, what's your expectation for how much of that do you expect would get installed over the course of this year, 2Q, 3Q, 4Q? And by the time we exit this year, how much should be done? And therefore, what benefit should there be to [indiscernible] from that?

Eric Aboaf: Yeah. I think, Vivek, there are a couple of ways to think about that because what happens here is that it gets onboarded on -- in tranches. So we might onboard the assets under custody, administration, but there are multiple services that we're often providing for those assets. So we had a couple of wins over the last year or two years with $1 trillion. Those $1 trillion wins would have had some custody, some accounting, they might have had some performance analytics. They would have had some middle office services in many cases because they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it
```

*Rank 2 — `BK_2023_Q1_prepared_remarks_500_004`*

```
performance remains solid, AUM flows were mixed with strength in fixed income and LDI strategies partly offset by outflows in other long-term strategies. During the quarter, our U.K. investment manager Newton launched five future legacy funds, its first range of risk-rated sustainable multi-asset funds to support growth in the U.K. retirement market. And back in the U.S., the Dreyfus Bold share class, which we introduced last year, has now raised over $4 billion in AUM. In summary, over the past few months, I've spoken about our combination of client trust at scale platforms, client-focused culture and resilience as a powerful foundation on which we can build. I'm also proud that our culture has been front and center in recent weeks as our people have risen to the occasion, responding commercially and working tirelessly to enable successful outcomes for our clients in these uncertain times. I view this client-first culture as the key to make more out of our diversified portfolio of adjacent businesses. While we are the world's largest custodian and a trust bank, the contributions from Clearance and Collateral Management, Pershing, Treasury Services and Issuer Services are differentiating in our client value proposition. With that, let me officially welcome Dermot to his first earnings call. Dermot, over to you.

Dermot McDonogh: Thank you, Robin, for the introduction, and good morning, everyone. It's a privilege to be here, and I look forward to working with you all. I'll start on Page 3 of the presentation with some additional details on our consolidated financial results in the first quarter. Total revenue was $4.4 billion, up 11% year-over-year. This reflects fee revenue being flat as headwinds from lower market value, a stronger dollar and the sale of Alcentra, which closed in November last year, were offset by significant improvement in fee waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.
```

*Rank 3 — `BK_2023_Q3_prepared_remarks_500_007`*

```
.1 billion, up 1% year-over-year. Fee revenue was flat. 2% growth in investment services fees was offset by a 19% decline in foreign exchange revenue on the back of lower volatility and volumes. Net interest revenue was up 12%. In asset servicing, investment services fees were up 3%, driven by higher market values, healthy net new business, and a weaker dollar, partially offset by lower client transaction activity. The strength of our balance sheet, as well as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and net interest revenue increased by 6%. In Pershing, investment services fees were up 2%, reflecting higher fees on sweep balances, partially upset by the impact of lost business and lower transaction volumes consistent with the decline in US equity exchange volumes. Despite the continued headwind from the ongoing deconversion of the regional bank client highlighted in the second quarter, Pershing saw $23 billion of net new assets on the platform this quarter, reflecting positive momentum in the underlying business. As Robin mentioned earlier, the momentum around Wove is building with both new and existing clients. While at the same time, ongoing investments in the core Pershing platform to enhance advisor experience and lead with innovative solutions have positioned us well to capitalize on the heightened pace of change in the RIA community. In Treasury services, investment services fees decreased by 1% as growth from higher client activity was offset by higher earnings credits for non-interest bearing deposit balances. In clearance and collateral management, investment services fees were up
```

*Rank 4 — `BK_2024_Q1_prepared_remarks_500_004`*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year, both largely reflecting higher market values. Investment and other revenue was $182 million in the quarter. Effective January 1, we adopted new accounting guidance for our investments in renewable energy projects resulting in an approximately $50 million increase to investment and other revenue. We have restated prior periods in our earnings materials to provide you with like-for-like, year-over-year and sequential comparisons. The adoption of this new accounting guidance is largely neutral to net income and earnings per share, as the increase in provision for income taxes roughly equals the increase in investment and other revenue. Net interest income decreased by 8% year-over-year, primarily reflecting changes in the composition of deposits, partially offset by the impact of higher interest rates. Expenses were up 2% year-over-year on a reported basis and up 1% excluding notable items, primarily severance expense. Growth was from incremental investments and employee merit increases offset by efficiency savings. Provision for credit losses was $27 million in the quarter, primarily driven by reserve increases related to commercial real estate exposure. As Robin mentioned earlier, we reported earnings per share of a $1.25 up 11% year-over-year, a pre-tax margin of 29% and a return on tangible common equity of 20.7%. Excluding notable items, earnings per share were $1.29, up 14% year-over-year. Pre-tax margin was 30%, and our return on tangible common equity was 21.
```

*Rank 5 — `BK_2024_Q1_prepared_remarks_500_006`*

```
supplement that we filed on March 26th for detailed reconciliations to previous disclosures. Now, starting with Security Services on Page 6. Security services reported total revenue of $2.1 billion, up 1% year-over-year. Investment services fees were up 8% year-over-year. In asset servicing, investment services fees were up 8%, driven by higher market values, net new business and higher client activity. We've remained focused on deal margins, and as a result the year-over-year impact of repricing on fee growth was de-minimis. Consistent with past quarters, we continue to see particular success with our ETF offering. ETF assets under custody and/or administration surpassed $2 trillion this quarter up over 40% year-over-year on the back of higher market values, net new business and client flows, and the number of funds serviced was up 16% year-over-year. While the pace of alternative fund launches was slower than in the prior year quarter, investment services fees for alternatives were up over 10% on a year-over-year basis. Throughout the quarter, we saw broad-based strength across client segments, products and regions. In issuer services, investment services fees were up 11% reflecting net new business across both depository receipts and corporate trust, as well as higher cancellation fees in depository receipts. Foreign exchange revenue was down 11% year-over-year and net interest income was down 12%. Expenses of $1.5 billion were flat year-over-year, reflecting incremental investments, as well as the impact of employee merit increases offset by efficiency savings. Pre-tax income was $591 million, a 4% increase year-over-year, and pre-tax margin expanded to 28%. Next, Market and Wealth Services on Page 7. Market and Wealth Services reported total revenue of $1.5 billion, up 3% year-over-year. Total investment services fees were up 7% year-over-year. In Pershing, investment services fees were up 3%, reflecting higher market values and client activity, partially offset by the impact of business lost in the prior year. Net new assets were negative $2 billion for the quarter, reflecting the ongoing deconversion of the before-mentioned lost business. Client demand for our Wealth Advisor platform, Wove, continues to be strong. In the first quarter, we signed nine additional client agreements,
```

verdict: should have abstained

failure mode: company substitution on an unanswerable question — BNY Mellon's AUCA reported as Northern Trust's

notes: Should have abstained. $48.8tn/+5% and $46.6tn/+2% are BNY Mellon's (ch4, ch2), presented as Northern Trust's — a company not in the corpus — with no hedging. The scorer's unsupported claim is "2023", a bare year; the actual failure, the company substitution, is invisible to it. Compare item 24, where the same figure is asked about BNY and answered correctly.

---

## 12. `ref_comp_08` / `chunk200_bm25`

- **condition:** chunk200_bm25
- **arm:** text_only
- **question_id:** ref_comp_08
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MTB_2024_Q3_prepared_remarks_200_004`*

```
s look at the specifics for the third quarter. Diluted GAAP earnings per share were $4.02 for the third quarter, improved from $3.73 in the second quarter. Net income for the quarter was $721 million compared to $655 million in the linked quarter, an increase of 10%. M&T's third quarter results produced an ROA and ROCE of 1.37% and 10.26% respectively. The CET1 ratio remains strong, growing at 11.54% at the end of the third quarter and tangible book value first year grew 5%. Of note, the third quarter included a discrete tax benefit of $14 million or an $0.08 EPS benefit. Slide 8 includes supplemental reporting of M&T's results on a net operating and tangible basis. M&T's net operating income for the third quarter was $731 million compared with $665 million in the linked quarter. Diluted net operating
```

*Rank 2 — `MTB_2023_Q3_prepared_remarks_200_005`*

```
98 for the third quarter, up 13% from last year’s similar quarter. Now, let’s review our net operating results for the quarter on Slide 9. M&T’s net operating income for the third quarter, which excludes intangible amortization was $702 million and diluted net operating earnings per share, was $4.05. Net operating return on tangible common equity was 17.41% and tangible book value per share increased 3% compared to the end of June. On Slide 10, you will see that diluted GAAP earnings per share, was down 21% from linked quarter. Recall our results from the second quarter of last year indicated an after-tax $157 million gain from the sales of CIT business in April. Excluding this gain, GAAP net income and diluted earnings per share were down 3% compared to the linked quarter. On a GAAP basis, M&T’s third quarter results produced an ROA and
```

*Rank 3 — `MTB_2024_Q4_prepared_remarks_200_004`*

```
to shift our balance sheet toward a more rate neutral position. We manage credit risk meaningfully reducing nonaccrual and commercial criticized balances, and having net charge-offs come in largely in line with our expectations. Best focus on the fundamentals positions M&T for 2025 and beyond, and is reflected in our 2024 results with net operating earnings per share of $14.88. ROTA and ROTCE of 1.3% and 14.54%, and 11% growth in tangible book value per share. Turn to Slide 9, which shows the results for the fourth quarter. Our fourth quarter results reflect the continuation of a strong performance we have through the year. There are several successes to highlight. NII was largely stable compared to the third quarter, even considering a 100 basis points in rate cuts since the start of the easing cycle in September. Average total loans grew for the fifth consecutive quarter demonstrating our ability to more than offset the plan reduction in our CRE concentration.
```

*Rank 4 — `FITB_2023_Q4_prepared_remarks_200_004`*

```
interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

*Rank 5 — `MTB_2024_Q4_prepared_remarks_200_006`*

```
growing to 11.67% at the end of the fourth quarter and tangible book value per share grew 1%. The fourth quarter included several notable items, a securities gain of $18 million or $0.08 per share related to the sale of noncore investments, expense associated with redemption of certain M&T trust preferred obligations amounting to $20 million or $0.09 per share. This action has a three-year earn back. Corporate real estate optimization related to expenses amounting to $27 million or $0.12 per share and a pension-related credit within expenses amounting to $12 million or $0.05 per share benefit. Slide 10 includes supplemental reporting of M&T's results on net operating or tangible basis. M&T's net operating income for the fourth quarter was $691 million compared to $731 million in the linked quarter. Diluted net operating earnings per share were $3.92 for the recent quarter, down from $
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: M&T's half is in ch2 verbatim ("tangible book value per share increased 3% compared to the end of June", MTB_2023_Q3). Fifth Third appears only at Q4 2023 — outside the asked quarter — so the comparison the question asks for cannot be made from this context. Answering the M&T half alone would not have answered the question.

---

## 13. `ref_them_04` / `chunk200_bm25`

- **condition:** chunk200_bm25
- **arm:** text_only
- **question_id:** ref_them_04
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Generated answer, verbatim:**

```
In late 2023, Bank of America reported achieving 170 basis points of operating leverage for the full year, attributing this to expense discipline that lowered quarterly expense levels throughout the year. U.S. Bancorp indicated that by the end of the fourth quarter of 2023, it would be on a run rate recognizing $900 million in savings, which was expected to support flat expenses between 2023 and 2024 and contribute to positive operating leverage. Barings (BK) stated its commitment to delivering aggregate positive operating leverage in the following year, citing confidence derived from ongoing investments and platform development. By early 2024, State Street reported generating both positive fee and total operating leverage in the third quarter of that period, noting that this performance was better than expected relative to the same period in 2023.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BK_2023_Q3_qa_200_019`*

```
approach across the company. We've got KYC as an example as well. We used to do KYC in each of our businesses. We're bringing that together to have a KYC platform. So there are a lot of proof points that we've got in various stages of development here in addition to the actual pilots that we did, specifically for a platform's operating model.

Mike Mayo: So when you add it all together you said next year you expect to have positive operating leverage, is that in aggregate or positive fee operating leverage and how can you have such confidence at this stage?

Robin Vince: So look we're committed to positive operating leverage over time. And I don't want my second year as CEO to be one where we have negative operating leverage. So we are focused on positive operating leverage next year. That's aggregate operating leverage to answer your question. And one of the reasons why we have confidence in that is because we've been investing on
```

*Rank 2 — `USB_2023_Q3_qa_200_009`*

```
next coming year. But that's embedded into our full year guidance of flat expenses between 2023 and 2024.

Andy Cecere: So Mike, the way I think about it, this is Andy, by the end of the fourth quarter, we will be on a run rate recognizing $900 million of savings, which will be fully reflected in 2024 in our expense base. And that is consistent with how we think about a relatively flat 23% to 24% expense base, including those savings plus investments we'll continue to make in the business.

Mike Mayo: And then the big question then is, so if you have flat 2024 expenses, do you think you can get to positive operating leverage? Or is it too early or too many moving parts? Because this is the sweet spot of the merger savings coming up, right, by the next quarter.

Andy Cecere: It is a sweet spot, Mike, you're absolutely right. And the savings are great.
```

*Rank 3 — `BK_2023_Q1_prepared_remarks_200_006`*

```
-over-year, and we generated a healthy return on tangible common equity of 20%. And given how in focused capital and liquidity are at the moment, I'll note that our Tier 1 leverage ratio as well as our liquidity coverage ratio remains strong and unchanged compared to the prior quarter, well above regulatory requirements and our own management buffers. Stepping back for a moment, I'm encouraged by the early progress that we are seeing around the Company to deliver on the commitment that we made to you back in January. First, we are bending the cost curve. Our first quarter expense growth came in marginally better than our initial internal plan and we remain firmly committed to cutting our core expense growth by roughly half this year compared to 2022 on a constant currency basis. Second, in line with our outlook for the year, we continued to derive healthy growth in net interest revenue. Third, we delivered positive operating leverage on a year-over-year basis. And fourth, we returned
```

*Rank 4 — `BAC_2023_Q4_prepared_remarks_200_005`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as
```

*Rank 5 — `STT_2024_Q3_prepared_remarks_200_002`*

```
afternoon, everyone. Our third quarter results, which we released earlier this morning, demonstrate the accelerating financial performance and strong business momentum we are achieving this year, which in turn positions State Street well for future growth. We achieved robust fee and total revenue growth and generated positive fee and total operating leverage in 3Q, which, when combined with increased capital return quarter-on-quarter, drove strong earnings growth for our shareholders on both the year-over-year and sequential basis, with quarterly EPS reaching the highest on record. In addition to strong 3Q results, our year-to-date results also highlight the strength of our franchise and financial performance in three quarters of the way through the year, with solid fee and total revenue growth and good expense discipline driving better than expected positive fee and positive total operating leverage, as well as strong earnings growth relative to the same period in 2023 and excluding notable items. The operating environment in the third quarter was dynamic. While global equity and fixed income markets moved notably
```

verdict: unfaithful

failure mode: company misattribution — "Barings" attached to BK (BNY Mellon) content; plus STT dated "early 2024" from a Q3 2024 chunk

notes: BAC (ch4) and USB (ch2) correct. Ch1 is BK_2023_Q3 — Robin Vince, BNY Mellon — rendered as "Barings (BK)". Checked: "Barings" appears in none of the five chunks, in no Stage 1 retrieval output, and zero times in the raw corpus, so it is not lifted from the STT chunk or any other; the model supplied it from outside the context. Same class as items 5, 6, 14, 30 and 44 all the same — a real company name attached to another company's content. STT content is right (ch5) but dated "early 2024" when the chunk is Q3 2024. Labelled answered_grounded_correct: a wrong company name is not something a numeric check can see.

---

## 14. `ref_them_12` / `chunk200_dense`

- **condition:** chunk200_dense
- **arm:** text_only
- **question_id:** ref_them_12
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> What did firms say during 2023 about their wealth management businesses and the investment behind them?

**Generated answer, verbatim:**

```
Based on the provided context, firms discussed their wealth management businesses and related investments in the following ways:

*   **Bank of New York Mellon (BNY):** The company stated that 2024 would be a turning point allowing it to completely focus on the performance of its five businesses, including wealth management, as well as its transformation.
*   **Goldman Sachs:** Management noted good year-over-year growth in wealth for both the full year and the fourth quarter. They expressed confidence in continuing to grow Asset & Wealth Management (AWM) management and other fees at a high-single-digit rate over the next several years, citing optionality to raise and grow management fees across asset and wealth management subsegments.
*   **Bank of America:** The firm highlighted that it is making significant investments in its wealth management segment, noting that they are "beginning to see green shoots" from these efforts. This was part of a broader strategy of investing in all segments to drive efficiency and growth following 2023 being described as a foundational year for planning and investment.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `C_2023_Q4_prepared_remarks_200_010`*

```
investors through both of these channels. As I reflect on the year, I also want to note that we were a source of strength for the system and for clients during a volatile period for the banking sector and geopolitically and I'm very proud of how our people around the world performed during challenging times. 2024 looks to be similar to 2023 in terms of the macro environment with moderating rates and inflation. We expect to see growth slowing globally with the US well positioned to withstand a run-of-the-mill recession should one materialize. With a strong balance sheet, ample liquidity and diligent risk management we are well positioned to support our clients through whatever environment comes to path. Moreover, we think environments like these play to our strengths, given how far we are down the path of our simplification and divestitures. 2024 will be a turning point as we will be able to completely focus on the performance of our five businesses and our transformation. I
```

*Rank 2 — `FITB_2023_Q4_prepared_remarks_200_008`*

```
.

Bryan Preston: Thanks, Tim, and thank you to everyone joining us today. 2023 was a very different year than what we were expecting 12 months ago. For Fifth Third, our success in outperforming this year was driven by our intentional actions to create and maintain flexibility for navigating uncertainty. As we enter 2024, we are very pleased with the results from 2023 and how we continue to be well-positioned for a wide range of economic outcomes. We have optionality in our balance sheet and diversification on our business mix that will allow us to adapt to changing environments. As Tim mentioned, achieving this positioning requires discipline and years of deliberate investments. Our full-year financial performance in 2023 benefited from this long-term investment. Fifth Third delivered industry-leading deposit growth of 5%, record revenue of $8.7 billion, and 100 basis points of capital accretion during the year, all while maintaining expense and credit discipline. We delivered another solid quarter
```

*Rank 3 — `GS_2024_Q4_qa_200_032`*

```
, we saw good growth year-over-year, both for the year and the fourth quarter. There was a little bit higher growth in wealth, both in the fourth quarter and the year. I guess, as you look at those businesses going forward, do you expect to see a divergence in either of those segments or do you think that consistently, they will both grow at similar levels?

Denis Coleman: So look, there are obviously different idiosyncratic factors within both the asset management and the wealth management sectors. We obviously like the optionality to continue to raise and grow our management fees across both of those subsegments. And we re-underwrite our expectation that we will continue to grow AWM management and other fees, high-single digits over the next several years. We've obviously outpaced that recently, but we sort of would re-underwrite our forward growth expectations to be high-single digits.

Operator: Thank you. We'll go next
```

*Rank 4 — `BK_2023_Q4_qa_200_001`*

```
it, if you take the comments stock both Rob and I have prepared and we've just laid out over the last 30 to 35 minutes, you can see truly that 2023 was a foundational year. We did a lot of kind of exploratory work, detailed planning. We've made a bunch of investments, both which will drive efficiency and which will drive growth. We've talked over the last few quarters about Wove, which we launched last June, and in my prepared remarks, I talked about $30 million to $40 million of revenue this year. So I would say we are making investments in all of our segments, and you can also see is in investments in wealth management, where we are beginning to see green shoots, and you can see, we're making a lot of investments in our security and services business, modernizing our platforms. So I would say you're going to see us quarter-by-quarter and I think over time as
```

*Rank 5 — `WFC_2023_Q4_prepared_remarks_200_006`*

```
our middle market clients with access to alternative sources of capital, another example of how we're providing solutions for our clients. Investing in our business and introducing new products and services remains a priority in 2024, and Mike will highlight some of the opportunities later on the call. In 2023, we also continued to take a closer look at the businesses that were not in sync with our strategic priorities. As I mentioned, we simplified the home lending business, which included exiting the correspondent business. We are reducing the size of our servicing portfolio as well as optimizing our retail team to align with our narrower customer focus. In the third quarter, we sold private equity investments in certain Norwest Equity Partners and Norwest Mezzanine Partners funds. We also continue to invest in the communities we serve throughout the year, and you can see many examples at the beginning of our slide presentation. As we look forward, our business performance remains sensitive to interest rates and the health of the U.S. economy
```

verdict: unfaithful

failure mode: company misattribution x2 — Citi's line given to BNY, BNY's line given to Bank of America

notes: Two of three bullets misattribute. "Bank of New York Mellon (BNY)" is given Citigroup's line from ch1 (C_2023_Q4, "2024 will be a turning point... five businesses"), and "Bank of America" is given BNY's "green shoots" from ch4 (BK_2023_Q4). GS (ch3) is right. The text is real; the speakers are swapped.

---

## 15. `ref_comp_01` / `chunk500_dense_enriched`

- **condition:** chunk500_dense_enriched
- **arm:** enriched
- **question_id:** ref_comp_01
- **category:** comparative
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did Goldman Sachs and Citi differ in how they characterised Basel III endgame uncertainty in late 2023 and early 2024?

**Generated answer, verbatim:**

```
Goldman Sachs characterized the Basel III Endgame uncertainty as a factor requiring them to maintain capital cushions above their normal range (specifically running with 90 bps of cushion) to signal flexibility and support client returns while addressing lingering regulatory ambiguity regarding both the quantum and timing of the rules. In contrast, Citi described its capital position as "very robust" despite the prevailing uncertainty, noting that it ended Q3 2024 with a CET1 ratio of 13.7% (which was $14 billion above regulatory minimums in late 2023) and continued to return capital through dividends and buybacks while actively working on mitigating actions for potentially high capital requirements.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `GS_2024_Q2_qa_500_008`*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution. It sounds from some of Powell's latest comments that, that may not be something that comes into effect until perhaps into 2025, but we are sort of maintaining a level of cushion that think is appropriate in light of what we know and we don't know about the future opportunity set for Goldman Sachs, but that buffer is designed to support clients return capital shareholders, while maintaining a prudent buffer with some of the lingering uncertainty with respect to future regulatory input.

Steven Chubak: Helpful color. Thanks for taking my questions.

Dennis Coleman: Thank you.

Operator: We'll go next to Devin Ryan with Citizens JMP.

Devin Ryan: All right, great. Good morning, David and Dennis. A couple questions on AWM progress. So the first one is on the alts business specifically, and you're tracking obviously well ahead of the fundraising targets relative to when you set the $1 billion medium term target for annual incentive fees? And now with over $500 billion in alts AUM and obviously growing, that would seem pretty conservative. So I appreciate there's a lot of work to do to generate the returns ahead here, but how should we think about the underlying assumptions for incentive fees in a more normal harvesting environment, just given the mixed shift and the growth that you're seeing in AUM there?

Dennis Coleman: So Devin, I think it's a good question, and I think we share your expectation that, that's going
```

*Rank 2 — `C_2024_Q3_prepared_remarks_500_003`*

```
in line with our expectations. In terms of capital, while uncertainty about the Basel III Endgame prevails, our capital position remains very robust and we ended the quarter with a CET1 ratio of 13.7%. During the quarter, we returned $2.1 billion in capital, including the repurchase of $1 billion of common shares. We will continue to repurchase stock as we evaluate the right level on a quarterly basis. As you know, our transformation is our number one priority. This quarter, we closed another longstanding consent order, which related to the effectiveness of our anti-money laundering systems. We have increased our investments in areas where we have not made sufficient progress such as data quality management. I and the management team remain steadfast and determined to get this transformation right and to get this done. We will close out this pivotal year with momentum and with determination to continue to improve performance in each business and the firm overall. We are committed to meeting our revenue and expense targets for the year, as well as our return target for the medium term. I am very proud of our senior leadership and the entire organization as we demonstrate the potential of our unique global franchise. It is a privilege to lead this firm. With that, I would like to turn it over to Mark, and then we will be delighted, as always, to take your questions.

Mark Mason: Thanks, Jane, and good morning, everyone. I'm going to start with the firm-wide financial results, focusing on year-over-year comparisons for the third quarter unless I indicate otherwise. And then spend a little more time on the businesses. On Slide 5, we show financial results for the full firm. For the quarter, we reported net income of approximately $3.2 billion, EPS of $1.51, and an RoTCE of 7% on $20.3 billion of revenues. Total revenues were up 1% on a reported basis. Excluding divestiture-related impacts, revenues were up 3%, driven by growth across each of our businesses. As you can see on the bottom-left side of the page, net interest income, excluding markets was down 1% year-over-year, largely due to lower interest rates in Argentina. And non-interest revenue, excluding markets was up 9% as we continued to see strong fee momentum across services, banking, and wealth. Year-to-date revenues were up 1% on a
```

*Rank 3 — `GS_2023_Q3_prepared_remarks_500_002`*

```
data has come in above estimates, driving market expectations of higher for longer interest rates. And there still are a number of sectors in the economy that have yet to absorb the impact of higher rates, especially in light of the further tightening in financial conditions we've seen over the last quarter. At the same time, there has been an escalation of geopolitical stresses around the globe, the [indiscernible] war in Ukraine, tensions with China and now the conflict in the Middle East. Overall levels of risk are more elevated than we've seen in quite some time. While we don't know where this will all lead, it could impact economic growth and stability in the U.S. and around the world, and we remain cautiously positioned. Before I turn it over to Denis, I'd like to spend a moment on Basel III Endgame proposal and reiterate my views on it. We, of course, support sensible regulation and the desire to ensure we have a safe and sound financial system. There are some who have recently said we need to address the lessons from the 2008 financial crisis, which is driving the needs of much higher regulations. But frankly speaking, the rules, as proposed, go way too far and do not account for the vast array of improvements made by the largest banks as a result of Dodd-Frank and other reforms. Not only have banks doubled capital over the last 15 years, have improved the quality of capital, increased liquidity, simplified businesses that have been subjected to ongoing annual stress tests. Requiring too much capital will have negative consequences. I believe if these rules are implemented, three things will happen. First, the cost of credit will go up for businesses of all sizes from large corporations to small businesses. Second, more activity will move to the unregulated shadow banking sector. Policies that incentivize a transfer of risk outside the regulated banking system could, in fact, increase systemic risk. And third, US competitiveness will go down. Our capital markets are the deepest and the most liquid in the world. They're the engine of our economy as access to capital allows for innovation and growth across the country. Our competitive standing as the leading global economy would be negatively impacted by this proposal. The net result of these proposed rules would be slower economic growth in the US, material improvement in the -- soundness of the banking system. We, alongside clients and others in the industry, have been engaging heavily
```

*Rank 4 — `C_2023_Q3_prepared_remarks_500_003`*

```
5%, which is $14 billion above our regulatory minimum and still includes a 100 bps internal management buffer. During the quarter, we returned $1.5 billion to our shareholders through common dividends and stock buybacks. We continue to evaluate buybacks quarter-by-quarter. And I expect we will continue to do a modest level in the fourth quarter, subject to approval by our Board. And while the ultimate impact of potentially high capital requirements won't be known until the Basel III end game is finalized, we have been actively working through, mitigating actions. As you can see on Slide 3, we are relentless in executing our strategy. This quarter, we closed on the sale of our Taiwan consumer business, and that's the second largest of the Asia consumer divestitures. And earlier this week, we announced that we will sell our consumer wealth portfolio in China to HSBC. And this includes approximately $2.6 billion in assets under management and $1 billion of deposits. In the fourth quarter, we expect to close down the sale of our Indonesia consumer business. In terms of the International consumer businesses, we are exiting. In addition to the three wind-down market, we have restarted the sales process in Poland and we remain on-track to separate Mexico next year, followed by an IPO in 2025. Transformation remains our number one priority. We're deep into the large body of work of automating manual controls and processes, consolidating fragmented tech platforms, and upgrading our data architecture. We're committed to doing this the right way, knowing it will take time to meet our regulators' expectations and to deliver a modern, more efficient infrastructure. Last month, we announced consequential changes that align our organizational structure with our strategy and changes how we run the bank. I said at the Investor Day, the organizational simplification would follow the divestitures. The changes will eliminate layers, duplication and complexity, allowing us to operate the bank more agilely and freeing our people up to focus on clients and execution. Elevating the five core businesses to my leadership team will enable me to drive greater accountability and sustainable results, so to bring it to life. The actions we've taken in the last few weeks will eliminate over 15% of the regional and functional roles at the top two layers of the company. It also take out 60 committees, which frees up over tens of thousands of people hours annually
```

*Rank 5 — `GS_2023_Q3_qa_500_012`*

```
further buyback. But at the moment, we'd like -- we're going to be a little bit more cautious and have a little bit more clarity around the capital rules before we flow ahead.

Mike Mayo: All right thank you.

Operator: We'll move to our next question from Ryan Kenny with Morgan Stanley. The floor is yours.

Ryan Kenny: Hi. Good morning. Thanks for taking my question. So wanted to follow up on the earlier questions on markets, maybe asked another way. So trading revenues are clearly extremely strong. Industry wallet and both fixed income and equities is tracking well above pre-pandemic levels, and you've been taking share. But looking forward, is there any scenario related to Basel Endgame where we see industry wallet size shrink? And as you think about higher for longer rates, how do you expect that, that impacts the various trading businesses?

David Solomon: Look, I think the intermediation activity for large institutions and corporations and governments around the world continues. The growth of the government in the world continues. The market capital world continues to grow and expand. I can't and I won't speculate on exactly where the final Basel rules wind up and how everyone optimizes through all that, but I don't think anything is changing in intermediation. And the need to finance the positions and the activities of so many of our clients is growing. And so I continue to think for leading players that have scale and global footprint and are in a leading position in these markets businesses, I think they're very well positioned in these market businesses. Of course, there will be ups and downs in those businesses. But I think the businesses will continue to perform very, very well.

Ryan Kenny: Thank you.

Operator: Our next question comes from Devin Ryan with JMP Securities. Please go ahead.

Devin Ryan: Thank you. Good morning, David and Denis. Want to come back to Wealth Management. I know that the sale of Personal Financial Management is a small business. But just if you can remind us how and where you want to compete in Wealth Management moving forward. And David, maybe give a little more color on some of those growth opportunities you alluded to that you're seeing there across the globe. Thank you.

David Solomon: Yes. So I appreciate that question, Devin. Our focus is on ultra-high net worth management where we have a leading franchise. I just
```

verdict: faithful

failure mode: out-of-window sourcing — Q2/Q3 2024 characterisations presented for a late-2023/early-2024 question

notes: Both companies correct and figures trace (GS ch1; Citi ch2/ch4). But the headline characterisations come from GS Q2 2024 and Citi Q3 2024, outside the asked window; only the $14bn is tagged "late 2023". A reasonable answer carrying a label about retrieval targeting.

---

## 16. `ref_fact_09` / `chunk500_dense_enriched`

- **condition:** chunk500_dense_enriched
- **arm:** enriched
- **question_id:** ref_fact_09
- **category:** factual
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** single (1 anchor) (coverage@5 = 1)
- **Check 3 flag:** not flagged

**Question:**

> What were M&T's average loans and leases in the second quarter of 2023, and how did they move?

**Generated answer, verbatim:**

```
M&T's total average loans and leases were $133.5 billion during the second quarter of 2023, representing an increase of $1.5 billion compared to the first quarter.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MTB_2023_Q2_prepared_remarks_500_003`*

```
was partially impacted from the mix change to the higher cost funding, which we estimate reduced the margin by 18 basis points. Higher yields on earning assets, net of rates on deposit funding benefited the margin by four basis points. Turning to slide 12. Capital levels remained strong with the CET1 ratio to the end of the second quarter at 10.58%. Average earning assets increased $1.9 billion or 1% from the first quarter to the second quarter due largely to the $1.5 billion growth in average loans and $1 billion increase in average investment securities. Turning to slide 13, we talk about the drivers on the loan growth. The total average loans and leases were $133.5 billion during the second quarter, up $1.5 billion compared to the linked-quarter. Looking at the loans by category on an average basis compared to the first quarter. Commercial and industrial loans increased 5% to $44.5 billion. We continue to see in our dealer and specialty businesses. Plus, we are adding new customers as we grow market share in legacy and new markets. During the second quarter, average commercial real estate loans decreased 1% to $44.9 billion. The decline was driven largely by lower construction loan balances. Average residential real estate loans were $23.8 billion, essentially flat compared to the first quarter of this year. Average consumer loans were down 1% to $20.3 billion, driven by lower activity due to rising interest rates. Turning to slide 14. Average investment securities increased to $28.6 billion during the second quarter due to the large part to purchases late at the end of the first quarter. The duration of the investment securities book at the end of June is 3.9 years and the unrealized pre-tax loss on the available for sale was only $441 million. At the end of June, cash and interest-bearing deposits at bank and the investment securities totaled $56.9 billion. Turning to slide 15. Deposit outflows during the second quarter on an average basis accounted for $2.1 billion or 1.3% in line with industry trends. Consistent with our experience prior to rising rates, the increased competition for deposits and customer behavior is leading to a mix shift with the deposit base to higher cost deposits. Comparing the second to first quarters, average demand deposits declined $5.7 billion. Savings and interest-bearing checking deposits decreased $843 million while deposits while time deposits increased $4.
```

*Rank 2 — `MTB_2023_Q1_prepared_remarks_500_007`*

```
fund earning asset growth. We expect continued intense competition for deposits in the face of industry-wide outflows. Full year average total deposit balances are expected to be down low single digits compared to the $158.5 billion average during 2022. During the first quarter, we issued $3.5 billion in senior debt and we'll utilize the combination of FHLB funding and senior debt over the course of this year as needed to ensure that we can continue to meet the loan demands of our customers. We continue to expect the deposit mix to shift toward higher cost deposits with declines expected in demand deposits and growth in time and on balance sheet suite. This is expected to translate to a through-the-cycle interest-bearing deposit beta in the high 30% to low 40% range.  Taking all of these factors into account, we anticipate the net interest margin to be slightly below 4% for the full year of 2023 and to continue to migrate towards the long-term range we have been discussing for the past couple of quarters. Next, let's discuss the drivers of earning asset growth. We currently plan to grow the securities portfolio by $2 billion compared to the $28 billion balance at the end of March of this year with the addition of longer duration mortgage-backed securities throughout the year. Looking at average loans. We expect average loan and lease balances during 2023 to grow in the 10% to 12% range when compared to the 2022 full year average of $119.3 billion. We anticipate growth to continue in the second quarter. and then for average balances to be flat to slightly down over the second half of the year. This implies total average loan and lease balances in the fourth quarter of 2023 to be up 1% to 3% and from the $129.4 billion average during fourth quarter of 2022.  The mix of C&I, CRE and consumer loans, inclusive of consumer real estate, is almost one-third each as of the end of March. We expect this trend to shift slightly as C&I growth outpaces CRE. As we have seen over the past three quarters, Higher levels of interest rates are expected to slow down the growth in our consumer loan book in 2023. After these average loans grew 2% in the first quarter, we expect the indirect portfolio to be relatively flat over the remainder of the year. Turning to fees. Excluding the $136 million gain on
```

*Rank 3 — `MTB_2023_Q2_prepared_remarks_500_006`*

```
points in the first quarter. This brings our year-to-date net charge-offs to 30 basis points, which is below our long-term average of 33 basis points. As we have noted previously, we expect net charge-offs to be lumpy on a quarter-to-quarter basis. This is the result of a unique nature of each property and borrower. In order to identify emerging issues that could lead to loan grade adjustments, we continue to perform ongoing rate risk, resizing risk, tenant sensitivities on commercial real estate portfolios on a quarterly basis. This work is reflected in our criticized loan portfolio. Loans 90 days past due on which we continue to accrue interest or $380 million at the end of the first quarter compared to $407 million sequentially and total 43% of these loans 90 days past due loans were guaranteed by the government or government related entities. Turning to slide 19 for capital. M&T Cet1 ratio at the end of June was an estimated 10.58% compared to 10.16% at the end of the first quarter. The increase was due in part to higher net income and in repurchasing shares in the second quarter. In June, tangible common shareholder equity totaled $15.2 billion, up 3% from the end of the prior quarter. Tangible book value per share accounted at $91.58, up 3% from the end of the first quarter. In late June, the Federal Reserve released results from the annual bank stress test. While this was an off year for Category IV banks, given the timing of the People's United acquisition, M&T participated in the stress test this year. Our preliminary stress test capital buffer or SCB is estimated to be 4%. Using the SCB, which is in effect from October 1st, 2023 to September 30th of 2024 will be subject to 8.5% CET1 ratio. Now turning to slide 20 for the outlook. As we look forward to the second quarter of this year, we believe we are well positioned to navigate through a challenging economic conditions. However, the rapidly changing interest rate expectations, combined with continued pressure on funding, affect our outlook for the full year 2023. The 2023 outlook reflects the impact of the sale of the M&T insurance agency that closed in October of last year and the sale of the CIT business that closed in April of this year. First, let's talk about net
```

*Rank 4 — `MTB_2023_Q3_prepared_remarks_500_005`*

```
properties in Western New York and Pennsylvania. Annualized net charge-offs as a percentage of total loans were 29 basis points for the third quarter compared to 38 basis points in the second quarter. This brings our year-to-date net charge-off rate to 30 basis points, which is below our long-term average of 33 basis points. We continue to assess the impact on future maturities and our investor real estate portfolio due to the level of interest rates, the impact of value declines and emerging tenancy issues. Continued targeted deep portfolio values in office, healthcare and multifamily portfolios are being done to identify any new emerging issues. When we file our upcoming Form 10-Q in the few weeks, we will estimate the level of criticized loans will be up to mid to high single-digit percent as compared to the end of June largely due to increases in investor real estate. Reflective of the financial strength and portfolio diversification of the CRE borrowers, almost 90% of the criticized loans are paying as agreed. Loans 90 days past due on which we continue to accrue interest were $354 million at the end of this quarter compared to $380 million sequentially and total of 76% of these 90 days past due loans were guaranteed by government-related entities. Turning to Slide 19 for capital. M&T’s CIT ratio at the end of September was an estimated 10.94% compared to 10.59% at the end of the second quarter. The increase was due in part to the continuation of the pause of repurchasing shares. At the end of September, based upon the proposed capital rules, the negative AOCI impact on the CET1 ratio from variable-for-sale securities and pension-related components would be approximately 36 basis points. Now turning to Slide 20 for outlook. With three quarters in the books, we will focus on the outlook for the fourth quarter. First, let’s talk about the economic outlook. The economic environment was supportive in the third quarter, and we were cautiously optimistic heading into the last quarter of this year. In the third quarter, the overall economy continued to expand, thanks to the strong consumer spending and steady capital expenditures by businesses, though the housing market continues to struggle in the high-rate environment. Encouragingly, inflation continued to slow in label markets, while still tight improved substantially with steady hiring while age pressures dissipated. Looking ahead to the fourth quarter, we are cautiously optimistic that the economy will
```

*Rank 5 — `MTB_2023_Q3_prepared_remarks_500_003`*

```
average basis compared to the second quarter, C&I loans increased slightly to $44.6 billion. We continue to see growth in dealer and specialty businesses. During the third quarter, average CRE loans decreased by 2% to $44.2 billion. This decline was driven largely by our continued strategy to reduce on-balance sheet exposure to this asset class. We have chosen to modernize our suite of products and services to offer more alternatives to better serve customers and to do so in a more capital-efficient manner possible. Average residential real estate was $23.6 billion, down 1%, largely due to portfolio pay-downs. Average customer loans were down slightly to $20.2 billion. The decline was driven by lower auto loan and HELOC balances, partially offset by the growth in recreational finance and credit card loans. Turning to Slide 14. Average investment securities decreased to $28 billion during the third quarter. The duration of the investment securities book at the end of September was 3.9 years and the unrealized pre-tax available-for-sale portfolio was only $447 million. At the end of the third quarter, cash held at the Fed and investment securities totaled $59.2 billion, representing 28% of total assets. Turning to Slide 15. We continue to focus on growing deposits with our customers and we are pleased with the growth in both average and end-of-period customer deposits. Average total deposits grew $3.3 billion. However, consistent with our experience in prior rising rate environments, increased competition for deposits and customer behavior continues to mix shift within the deposit base to higher cost deposits. Average customer deposits increased $1 billion. The customer deposit mix to migrate to average demand deposits declined $2.3 billion in favor of commercial sweeps and customer money market savings and time deposits. Average broker deposits increased $3.2 billion, while federal home loan bank advances decreased $2.2 billion. On average, brokered money market had now increased $800 million. Brokered time increased $1.5 billion. Broker deposits represent just one of the several funding vehicles that we can employ in our management of the balance sheet. At September 30 of this year, broker deposits represented 8% of our outstanding deposits and short-term borrowings. The pace and reduction in demand deposits seem to have decreased during the quarter. Our determined focus on retaining and growing customer deposits yielded positive results during the quarter. Next, let’s discuss non
```

verdict: faithful

failure mode: none

notes: Exact and complete: $133.5bn, up $1.5bn versus Q1 (ch1 rank 1, verbatim), answering both parts of the question. Label agrees.

---

## 17. `ref_them_12` / `chunk200_hybrid`

- **condition:** chunk200_hybrid
- **arm:** text_only
- **question_id:** ref_them_12
- **category:** thematic
- **case:** B
- **outcome label:** answered_ungrounded
- **coverage@5:** 0

**Question:**

> What did firms say during 2023 about their wealth management businesses and the investment behind them?

**Generated answer, verbatim:**

```
Based on the provided context, several firms discussed their wealth management businesses and related investments for 2023:

*   **Wells Fargo (WFC):** The firm stated that revenue growth from investments in Wealth and Investment Management would help fund additional investments. They noted that these drivers were intended to close performance gaps and improve returns.
*   **Morgan Stanley (MS):** The company highlighted that its wealth and investment management business line generated operating leverage and high returns during the 2020–2022 period following acquisitions of E*TRADE and Eaton Vance. In 2023, despite challenges, the firm’s business model produced consistent results, contributing to $54 billion in total revenues and a 13% return on tangible common equity.
*   **Goldman Sachs (GS):** The firm reported driving solid investment performance and consistent growth in its Asset & Wealth Management segment. This included growth in durable revenue bases such as management fees, other fees, and private banking and lending revenues. Additionally, Goldman surpassed its five-year alternatives fundraising target one year early.
*   **Bank of New York Mellon (BK):** The firm indicated it was making investments in wealth management where they were "beginning to see green shoots." These investments are part of a broader strategy that includes modernizing platforms and driving efficiency across all segments.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `WFC_2023_Q4_prepared_remarks_200_029`*

```
, and help drive growth. We expect the revenue growth that these investments should generate in businesses like Corporate Investment Banking and Wealth And Investment Management will help fund additional investments. So, we have many drivers to close the gap and improve returns. In summary, our results in 2023 demonstrated our commitment to improving our financial performance. We grew revenue, reduced expenses, increased capital returns to shareholders and maintained our strong capital position. We will now take your questions.
```

*Rank 2 — `MS_2023_Q4_prepared_remarks_200_002`*

```
equities. During this period, we also acquired Solium, which was a step toward leadership in the corporate stock plan space. Then in 2020 to '22, the COVID years, we achieved incremental scale in both wealth and investment management with the acquisitions of E*TRADE and Eaton Vance, giving us a leading self-directed platform and pushing forward in investment solutions. During this period, each of the two major business lines -- wealth and investment management and institutional securities generated operating leverage and high returns. Transformed Morgan Stanley today has tripled client assets in its durable businesses with significant opportunities for further growth. Notwithstanding 2023's geopolitical, macroeconomic and industry challenges, the firm's business model generated consistent results. In 2023, firm revenues were $54 billion with $12 billion of PBT, double the averages of 2009 to '14. Our return on tangible common equity was a solid 13%, inclusive of notable items that reduced returns by over 100 basis points
```

*Rank 3 — `GS_2023_Q4_prepared_remarks_200_003`*

```
scaled business with over $2.8 trillion in assets under supervision and where we see significant opportunity for further growth. Across these two businesses, our extraordinary talent and unmatched execution are bolstered by our One Goldman Sachs operating ethos. On page three, we lay out our progress across a number of key priorities that we discussed at our most recent Investor Day in February 2023. Global Banking & Markets, we've maintained and strengthened our leadership positions across investment banking. In FICC and equities, we have improved our standing with the top 150 clients. We generated record total financing revenues across these businesses in 2023 and have demonstrated impressive growth over the last four years. In Asset & Wealth Management, we've driven solid investment performance and consistent growth in a more durable revenue base of management, other fees, and private banking and lending revenues. This past year, we reduced our historical principal investments by $13 billion, and also surpassed our five-year alternatives fundraising target one year
```

*Rank 4 — `BK_2023_Q4_qa_200_001`*

```
it, if you take the comments stock both Rob and I have prepared and we've just laid out over the last 30 to 35 minutes, you can see truly that 2023 was a foundational year. We did a lot of kind of exploratory work, detailed planning. We've made a bunch of investments, both which will drive efficiency and which will drive growth. We've talked over the last few quarters about Wove, which we launched last June, and in my prepared remarks, I talked about $30 million to $40 million of revenue this year. So I would say we are making investments in all of our segments, and you can also see is in investments in wealth management, where we are beginning to see green shoots, and you can see, we're making a lot of investments in our security and services business, modernizing our platforms. So I would say you're going to see us quarter-by-quarter and I think over time as
```

*Rank 5 — `STT_2023_Q4_prepared_remarks_200_002`*

```
as of today, and we disclaim any obligation to update them, even if our views change.  Now, let me turn it over to Ron.

Ron O'Hanley: Thank you, Ilene, and good morning, everyone. Earlier today, we released our fourth quarter and full year 2023 financial results. As I reflect on 2023, the operating environment was dynamic with a complex set of challenges for the world's investors and for our industry, and I am proud of how we carefully navigated State Street through various headwinds, while continuing to execute against our strategic agenda. We focused and delivered on that agenda in three key areas; achieve strong sales wins across our businesses, drive strategic change in our investment services business and remain disciplined on productivity and broader cost management. Further on that last point, during 2023, we implemented key productivity actions and announced additional efficiency measures that will enable us to enhance the productivity of our operating model in 2024 and the years ahead. We
```

verdict: faithful

failure mode: date verified as though it were a figure — the answer normalises the context's "'22" to "2022"

notes: All four bullets correct, including BK correctly named "Bank of New York Mellon" (ch4) — the same chunk item 14 gave to Bank of America. The single flagged claim is "2022", from "the 2020–2022 period", a correct reading of ch2's "in 2020 to '22, the COVID years". Same mechanism as item 10: a context-derived date, exempt from Fix 2 because the question did not supply it, checked as if it were a figure. Set beside item 13 — the scorer sinks this answer over a date and passes that one with a company that does not exist in the corpus.

---

## 18. `ref_comp_07` / `chunk200_dense_enriched`

- **condition:** chunk200_dense_enriched
- **arm:** enriched
- **question_id:** ref_comp_07
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did PNC and U.S. Bancorp each frame their 2024 expense plans on their third-quarter 2023 calls?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `PNC_2023_Q3_prepared_remarks_200_002`*

```
such as the Signature Bank loans that we recently acquired. Finally, we are focused on expense management, particularly in the current environment, and have taken actions to maintain disciplined expense control. We increased our Continuous Improvement goal last quarter from $400 million to $450 million, and we are on track to achieve that goal in 2023. Looking ahead, we expect to have CIP savings within a similar range for 2024. And as a reminder, we used savings from this program to fund investments in key growth markets and technology. In addition, earlier this month, we began executing on staff reductions, which will reduce our 2024 expenses by $325 million and will fall to the bottom-line. All told, we are implementing more than $725 million of expense management actions that will have impact on 2024. While decisions involving personnel are never easy, we believe they will help us more effectively and efficiently deliver for our customers and our stakeholders, and we'll continue to be diligent in
```

*Rank 2 — `PNC_2023_Q3_prepared_remarks_200_015`*

```
do expect a 2024 annual CIP goal of similar magnitude to the 2023 program. Our CIP efforts over the years have allowed us to substantially invest in our company while still delivering low single digit annual expense growth. However, the current environment poses meaningful pressures necessitating expense control measures beyond our annual CIP program. As a result, we took a hard look at our organizational structure and identified opportunities to operate more efficiently through staff reductions, which we began implementing earlier this month. This initiative will decrease the workforce by 4% and is expected to reduce 2024 expenses by approximately $325 million. One-time costs associated with this plan are expected to be approximately $150 million and will be incurred during the fourth quarter of 2023. We believe these actions will position PNC for stronger efficiency going forward. As a result, even though our budgeting cycle isn't complete, we have an objective to keep core expenses stable in 2024, which by definition would exclude the fourth quarter one-
```

*Rank 3 — `PNC_2023_Q4_prepared_remarks_200_011`*

```
Notably, in 2023, we reduced our non-branch footprint by 2 million square feet, or approximately 17%. For the full year, core non-interest expense of $13.3 billion increased $177 million or 1%. Expense growth was well controlled due in part to the $50 million midyear increase in our CIP goal to $450 million, which we exceeded. As a result, we generated 41 basis points of adjusted positive operating leverage for the full year. Looking forward to 2024, our annual CIP target is $425 million. This program funds a significant portion of our ongoing business and technology investments. And as of year-end, we completed actions related to the workforce reduction that will drive $325 million of cost savings in 2024.  Taken together, we're implementing $750 million of expense management actions, all of which are reflected in our 2024 guidance that I will cover in a few minutes. Our credit metrics are presented on Slide 10. While
```

*Rank 4 — `PNC_2023_Q3_prepared_remarks_200_016`*

```
time charges. In summary, PNC reported a solid third quarter 2023. In regard to our view of the overall economy, we're expecting a mild recession starting in the first half of 2024, with a contraction in real GDP of less than 1%. We expect the federal funds rate to remain unchanged in the near term between 5.25% and 5.5% through mid-2024 when we expect the Fed to begin cutting rates. Looking ahead, our outlook for the fourth quarter of 2023 compared to the third quarter of 2023 is as follows. We expect average loans to be up approximately 3%, including the acquisition of the Signature Bank capital commitment facilities. Net interest income to be down 1% to 2%. Fee income to be up approximately 1% as increased capital markets activity is expected to more than offset the impact of the elevated MSR hedge gains during the third quarter. Other noninterest income to be in the range of $150 million and $
```

*Rank 5 — `PNC_2023_Q4_prepared_remarks_200_002`*

```
closed on the acquisition of the capital commitment loans from Signature, which is immediately accretive to earnings. Secondly, as we expected, we saw meaningful growth from non-interest income during the fourth quarter, driven primarily by a rebound in capital markets and advisory fees. Third, we completed the actions to reduce our workforce and we are positioned to realize $325 million of expense savings in 2024. This is in addition to our CIP savings target for 2024 that Rob will discuss in a few minutes. Expense discipline remains a top priority for us and accordingly we are targeting stable expenses for 2024 even as we continue to invest in key growth initiatives. Fourth, our credit quality remained strong during the quarter, reflecting our thoughtful approach us to growing our balance sheet. While we continue to expect credit charge offs to increase over time, particularly in the CRE office segment, we’re adequately reserved. Finally, during the fourth quarter, we increased our capital position, saw solid improvement in our AOCI int
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: All five chunks are PNC; U.S. Bancorp does not appear at all. PNC's Q3 2023 expense plan is complete in context ($450m CIP goal, $325m staff reductions, >$725m total), but a two-company comparison cannot be built from one company.

---

## 19. `ref_comp_12` / `chunk200_dense_enriched`

- **condition:** chunk200_dense_enriched
- **arm:** enriched
- **question_id:** ref_comp_12
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did PNC's and Capital One's net interest margins compare in 2024?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `PNC_2024_Q1_prepared_remarks_200_016`*

```
year 2024 compared to the full year 2023, we expect average loan growth of approximately 1%. Total revenue to be stable to down 2%. Inside of that, our expectation is for net interest income to be down in the range of 4% to 5%, and non-interest income to be up 4% to 6%. Core non-interest expense, which excludes the FDIC assessment, is expected to be stable and we expect our affected tax rate to be approximately 18.5%. And with that, Bill and I are ready to take your questions.
```

*Rank 2 — `PNC_2024_Q1_prepared_remarks_200_010`*

```
205 million or 6%. Provision was $155 million in the first quarter, reflecting portfolio activity and improved macroeconomic factors, and our effective tax rate was 18.8%. Turning to Slide 9. We highlight our revenue trends. First quarter revenue was down $216 million or 4%, driven by lower net interest income and in part a seasonal decline in fee income. Net interest income of $3.3 billion declined $139 million or 4%, reflecting increased funding costs, lower loan balances, and one less day in the quarter. Fee income was $1.7 billion and decreased $74 million or 4% linked quarter. Looking at the detail. Asset management and brokerage revenue was up $4 million or 1%, reflecting higher average equity markets. Capital markets and advisory fees declined $50 million or 16%, driven by lower M&A advisory activity, off elevated fourth quarter levels, partially offset by higher underwriting fees. Card and cash management decreased $17 million or
```

*Rank 3 — `PNC_2024_Q1_prepared_remarks_200_009`*

```
and into 2025. Turning to the income statement on Slide 8. First quarter net income was $1.3 billion or $3.10 per share, which included a pretax, non-core, non-interest expense of $130 million or $103 million after tax related to the increased FDIC special assess assessment. Excluding non-core expenses, adjusted EPS was $3.36 per share. Total revenue of $5.1 billion decreased $216 million or 4% compared to the fourth quarter of 2023. Net interest income declined by $139 million or 4%, and our net interest margin was 2.57%, a decline of 9 basis points, resulting primarily from higher funding costs. Non-interest income decreased $77 million or 4%. Non-interest expense of $3.3 billion declined $740 million or 18%, and included $130 million FDIC special assessment. Importantly, core non-interest expense was $3.2 billion and decreased $
```

*Rank 4 — `PNC_2024_Q1_prepared_remarks_200_011`*

```
2%, driven by seasonally lower consumer transaction volumes, partially offset by higher treasury management fees. Lending and deposit related fees declined $9 million or 3%, reflecting the reduction of customer fees on certain checking products. Residential and commercial mortgage revenue declined $2 million or 1%, and included lower residential mortgage activity. Other non-interest income of $135 million decreased $3 million or 2%, reflecting lower gains on sales. The first quarter also included a negative $7 million Visa fair value adjustment compared to a negative $100 million adjustment in the fourth quarter. Turning to Slide 10. Our core non-interest expense at $3.2 billion decreased $205 million or 6% linked quarter, reflecting strong expense management. Importantly, compared to the first quarter of 2023, core non-interest expense declined $117 million or 4%, with a decline in every expense category. This broad-based result reflects the impact of expense actions taken in 2023. As we've previously stated
```

*Rank 5 — `PNC_2024_Q1_prepared_remarks_200_002`*

```
a multiyear investment of nearly $1 billion in our branch network to renovate more than 1,200 locations and open new branches in key locations, including Austin, Dallas, Denver, Houston, Miami and San Antonio. Second, expenses were well managed during the quarter. As we've indicated, expense discipline remains a top priority, and we are on track to maintain stable core expenses in 2024. Third, credit quality remains stable during the quarter. The office portfolio remains an area of focus, but we are adequately reserved overall, and particularly with respect to CRE. We believe our thoughtful approach to managing risk, customer selection and long-term relationship development will continue to serve us well. And fourth, we continue to build on our strong liquidity and capital position during the quarter, providing us with a financial strength and flexibility to help us support our clients grow our businesses and capitalize on future opportunities. In summary, we delivered solid results during the first quarter and positioned ourselves well for the balance
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: All five chunks are PNC_2024_Q1; Capital One does not appear. PNC's NIM (2.57%, down 9bps) is in ch3, but there is no second margin to compare it against.

---

## 20. `ref_comp_01` / `chunk200_hybrid`

- **condition:** chunk200_hybrid
- **arm:** text_only
- **question_id:** ref_comp_01
- **category:** comparative
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did Goldman Sachs and Citi differ in how they characterised Basel III endgame uncertainty in late 2023 and early 2024?

**Generated answer, verbatim:**

```
Based on the provided context, Goldman Sachs characterized the Basel III endgame uncertainty as a factor that would be resolved through "significant modifications" to the proposed rule, which they expected would provide them with "materially more flexibility on capital deployment." In contrast, Citi’s prepared remarks in late 2023 did not explicitly characterize the Basel III endgame; instead, Jane Fraser focused on the company's progress in simplifying its structure and executing its strategy, noting that the fourth quarter was "clearly very disappointing" without specifically attributing it to Basel III uncertainty in the provided text.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `GS_2024_Q2_qa_200_020`*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution
```

*Rank 2 — `USB_2023_Q4_qa_200_016`*

```
. And now you're sitting here with 9.9% CET1. No longer have to be a Category II bank early, and all the color that we're getting from Washington is that Basel III endgame will be at least delayed, if not soften significantly. As you think about maybe just one more hurdle ahead over the near term in terms of the DFAST, how are you thinking about where U.S.-based proper CET1 ratio is in terms of the minimum looking forward to a future where maybe capital is a little bit tighter, but you're also growing? And do you feel like you're now on offense and all the sort of the balance sheet management that was designed to optimize capital is fully behind you?

Andy Cecere: Yeah, Erika, as John mentioned, I think our balance sheet optimization efforts are behind us. Our focus on capital accretion will be from earnings as we go into 2024 and forward. As
```

*Rank 3 — `JPM_2023_Q3_prepared_remarks_200_017`*

```
political situation, economic outlook, rate environment, deposit reprice and the impact of the Basel III endgame proposal are as prominent now as they have been in the recent past. But as always, we continue to prepare for a range of scenarios and are focused on being there for our clients and customers when they need us most. And with that, let's open the line for Q&A.
```

*Rank 4 — `GS_2024_Q1_prepared_remarks_200_014`*

```
. Given expectations for significant modifications to the Basel III proposed rule, we should have materially more flexibility on capital deployment. We also remain committed to paying our shareholders a sustainable and growing dividend. In conclusion, our first quarter results reflect the strength of our leading global banking and markets franchise and our growing Asset & Wealth Management business. Simply put, we are delivering on the things we said we would do. We are focused on our strategic objectives and the execution focus areas for 2024 that we laid out in January, which will help our businesses produce mid-teens returns through the cycle. We are confident in our ability to deliver for shareholders while continuing to support our clients and remain optimistic about the future opportunity set for Goldman Sachs. With that, we'll now open up the line for questions.
```

*Rank 5 — `C_2023_Q4_prepared_remarks_200_001`*

```
subject to uncertainty and changes in circumstances. Actual results may differ materially from these statements due to a variety of factors, including those described in our earnings materials, as well as in our SEC filings. And with that, I'll turn it over to Jane.

Jane Fraser: Thank you, Jenn, and a very Happy New Year to everyone, and I hope you all had a good break. At Citi, we're back at it. And given the notable items and our new financial reporting structure, we've got a lot to cover today, so I'm going to get right to it. 2023 was a foundational year in which we made substantial progress, simplifying Citi and executing the strategy we laid out at Investor Day. With that said, the fourth quarter was clearly very disappointing. Today, I'm going to provide a high-level view on our progress in 2023, discuss our Q4 results and finish with our priorities for '
```

verdict: faithful

failure mode: none — scored offtarget on transcript targeting, not on grounding

notes: Both companies right, both in window (GS Q1 2024 ch4; Citi Q4 2023 ch5), quotes accurate. Notable: it reports that Citi's remarks did not characterise Basel III rather than inventing a characterisation. Correcting my own first note: this record is answered_grounded_offtarget with 0 unsupported claims, NOT ungrounded — the n-gram fallback decided which chunks counted as supporting, and none belonged to the question's own transcript_ids. So there is no scorer false positive here, unlike item 40 where the same fallback produced an ungrounded verdict.

---

## 21. `ref_them_06` / `chunk500_dense`

- **condition:** chunk500_dense
- **arm:** text_only
- **question_id:** ref_them_06
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> What efficiency ratio levels and targets did banks discuss across 2023 and 2024?

**Generated answer, verbatim:**

```
Based on the provided context, the following efficiency ratios and targets were discussed:

*   **Capital One (COF):** Reported an annual operating efficiency ratio of **43.54%** for full-year 2023 (net of adjustments). For 2024, they expect this ratio to be **flat to modestly down** compared to 2023.
*   **PNC:** While not providing a specific percentage target, PNC stated an objective to keep **core expenses stable in 2024**. This goal is intended to position the bank for stronger efficiency following workforce reductions and expense control measures beyond their annual CIP program.
*   **Citigroup (C):** Did not provide a specific operating efficiency ratio percentage or target in the provided text, but noted that 2024 will be a turning point allowing them to focus on business performance and transformation benefits.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `WFC_2023_Q4_prepared_remarks_500_009`*

```
in consumer banking and lending deposits, as well as continued mix shift from lower yielding products to higher yielding, deposits in our other deposit gathering businesses are expected to be relatively stable and market funding will replace the decline in consumer deposits as needed. We currently expect that net interest income will trough towards the end of this year. As we’ve done in prior years, we are also assuming the asset cap will remain in place throughout the year. Ultimately, the amount of net interest income we earn in 2024 will depend on a variety of factors, which many of which are uncertain, including the absolute level of rates, the shape of the yield curve, deposit balances, mix and pricing and loan demand. Turning to our 2024 expense expectations on Slide 19. We started our focus on efficiency initiatives three years ago and we’ve successfully delivered on our commitment of approximately $10 billion of gross expense saves. Through our efficiency initiatives we have reduced headcount every quarter since third quarter of 2020 and headcount is down 16% since the end of 2020. Looking at our expectations for this year and following the waterfall on the slide from left to right. We reported $55.6 billion of non-interest expense in 2023, which included the $1.9 billion FDIC special assessment. Excluding this item, expenses would have been $53.6 billion, which we believe is a good starting point for discussion of 2024 expenses. Looking at the next bar, we expect severance expense to be approximately $1.3 billion lower, driven by the $969 million expense we took in the fourth quarter for planned actions, we expect expenses to increase by at least $300 million due to higher revenue related expense, driven by wealth and investment management, revenue related expenses will ultimately be a function of activity and market levels, and therefore could be higher or lower than this estimate. At this point, we expect all other expenses to be flat, though there are significant efficiencies and increased investments included in this expectation. We expect approximately $2.7 billion of gross expense reductions in 2024 due to the efficiency initiatives. We highlight in the slide some of the areas where we anticipate additional savings and continue to believe we have more opportunities beyond 2024. Similar to prior years, the resources needed to address our risk and control work are separate from our efficiency initiatives and we will continue to make significant investments in our risk and control infrastructure. While we remain focused on executing on our efficiency
```

*Rank 2 — `COF_2023_Q4_prepared_remarks_500_005`*

```
. On a monthly basis auto delinquency rate and charge-off rate had been tracking normal seasonal patterns since the first half of 2023 and continued to do so through December. Slide 13 shows fourth-quarter results for our Commercial Banking business. Compared to the linked-quarter, ending loan balances decreased about 1%. Average loans were also down about 1%. The modest declines are largely the result of choices we made earlier in the year to tighten credit. Ending deposits were down about 9% from the linked quarter. Average deposits were down about 7%. The declines are largely driven by our continuing choices to manage down selected less attractive commercial deposit balances. Reducing these less attractive deposits also drove the 14 basis point linked-quarter improvement in our average rate paid on commercial deposits. Fourth-quarter revenue was down 5% from the linked quarter. Non-interest expense was also down about 5%. The Commercial Banking annualized charge-off rate for the fourth quarter increased 28 basis points from the third quarter to 0.53%. The Commercial Banking criticized performing loan rate was 8.81%, up 73 basis points compared to the linked quarter. The criticized non-performing loan rate was down 6 basis points to 0.84%. Commercial Banking credit trends were largely driven by continuing pressure in our commercial office portfolio. Slide 17 of the fourth-quarter 2023 results presentation shows additional information about the remaining commercial office portfolio, which is less than 1% of our total loans. In closing, we continued to deliver solid results in the fourth quarter. We posted another strong quarter of top line growth in domestic card revenue, purchase volume, and loans. Domestic card and auto delinquency trends were in line with normal seasonal patterns, a continuing indicator of stabilizing consumer credit results. We grew consumer deposits and total deposits. And we added liquidity and maintained capital to further strengthen our already strong and resilient balance sheet. Our annual operating efficiency ratio, net of adjustments for the full year 2023, was 43.54%. In 2023, we saw incremental opportunities and made choices to grow revenue and tightly manage costs to achieve a 99 basis point improvement in our annual operating efficiency ratio. The actual improvement was better than the “modest improvement” growth we had been expecting. Over the last decade, we've driven significant operating efficiency improvement even as we've invested to transform our technology. And we continue to drive for efficiency improvement over time. For the full
```

*Rank 3 — `PNC_2023_Q3_prepared_remarks_500_006`*

```
do expect a 2024 annual CIP goal of similar magnitude to the 2023 program. Our CIP efforts over the years have allowed us to substantially invest in our company while still delivering low single digit annual expense growth. However, the current environment poses meaningful pressures necessitating expense control measures beyond our annual CIP program. As a result, we took a hard look at our organizational structure and identified opportunities to operate more efficiently through staff reductions, which we began implementing earlier this month. This initiative will decrease the workforce by 4% and is expected to reduce 2024 expenses by approximately $325 million. One-time costs associated with this plan are expected to be approximately $150 million and will be incurred during the fourth quarter of 2023. We believe these actions will position PNC for stronger efficiency going forward. As a result, even though our budgeting cycle isn't complete, we have an objective to keep core expenses stable in 2024, which by definition would exclude the fourth quarter one-time charges. In summary, PNC reported a solid third quarter 2023. In regard to our view of the overall economy, we're expecting a mild recession starting in the first half of 2024, with a contraction in real GDP of less than 1%. We expect the federal funds rate to remain unchanged in the near term between 5.25% and 5.5% through mid-2024 when we expect the Fed to begin cutting rates. Looking ahead, our outlook for the fourth quarter of 2023 compared to the third quarter of 2023 is as follows. We expect average loans to be up approximately 3%, including the acquisition of the Signature Bank capital commitment facilities. Net interest income to be down 1% to 2%. Fee income to be up approximately 1% as increased capital markets activity is expected to more than offset the impact of the elevated MSR hedge gains during the third quarter. Other noninterest income to be in the range of $150 million and $200 million, excluding net securities and Visa activity. We expect total core non-interest expense to be up 3% to 4%, which excludes charges related to the workforce reduction. Additionally, this guidance does not contemplate the pending FDIC special assessment, which could occur during the fourth quarter. And we expect fourth quarter net charge-offs to be between $200 million and $250 million. And with that, Bill and I are ready to take your questions.
```

*Rank 4 — `COF_2023_Q4_prepared_remarks_500_006`*

```
-year 2024, we expect annual operating efficiency ratio, net of adjustments, will be flat to modestly down compared to 2023. Our expectation includes the partial year impact of the proposed CFPB late fee rule, assuming that rule takes effect in October 2024. Pulling way up, our modern technology capabilities are generating an expanding set of opportunities across our businesses. We continue to drive improvements in underwriting, modeling, and marketing, as we increasingly leverage machine learning at scale. And our tech engine drives growth, efficiency improvement, and enduring value creation over the long term. We remain well-positioned to deliver compelling long-term shareholder value and to thrive in a broad range of possible economic scenarios. And now we'll be happy to answer your questions. Jeff?

Jeff Norris: Thank you, Rich. We’ll now start the Q&A session. As a courtesy to other investors and analysts who may wish to ask a question, please limit yourself to one question plus a single follow-up. So if you have any questions after the Q&A session, the Investor Relations team will be available after the call. Amy, please start the Q&A.
```

*Rank 5 — `C_2023_Q4_prepared_remarks_500_004`*

```
investors through both of these channels. As I reflect on the year, I also want to note that we were a source of strength for the system and for clients during a volatile period for the banking sector and geopolitically and I'm very proud of how our people around the world performed during challenging times. 2024 looks to be similar to 2023 in terms of the macro environment with moderating rates and inflation. We expect to see growth slowing globally with the US well positioned to withstand a run-of-the-mill recession should one materialize. With a strong balance sheet, ample liquidity and diligent risk management we are well positioned to support our clients through whatever environment comes to path. Moreover, we think environments like these play to our strengths, given how far we are down the path of our simplification and divestitures. 2024 will be a turning point as we will be able to completely focus on the performance of our five businesses and our transformation. I recognize the importance of this year and I am highly confident that we will see the benefits of the actions we've taken through the momentum of our businesses. Backed by investments in key products we believe we can continue to grow revenues ex-divestitures by 4% to 5% over the medium term. Overall, we remain confident in our ability to adapt to the evolving capital and macro environment to reach our medium-term return targets and return capital to our shareholders whilst continuing the investments needed in our information. With that, I'd like to turn it over to Mark, and then we will be delighted, as always, to take your questions.

Mark Mason: Thanks, Jane, and good morning, everyone. We have a lot to cover on today's call. I'm going to start with the fourth quarter and full year firm-wide financial results, focusing on year-over-year comparisons, unless I indicate otherwise. I'll also focus on our guidance for 2024 and end with the path to our medium-term return target. The presentation of our results reflects the changes we've made in conjunction with our organizational simplification, including reporting legacy franchises and corporate other in all other. However, before I go into the results, let me walk you through some of the notable items that impacted the quarter that were included in the 8-K we recently filed. At the top right of slide seven, we show these items on a pre-tax basis. The F
```

verdict: faithful

failure mode: none — WFC omitted, but it gives no ratio either

notes: COF's 43.54% and the flat-to-modestly-down 2024 guide both correct (ch2, ch4). The PNC and Citi bullets correctly state that no ratio was given. WFC (ch1) is ignored, though it gives no ratio either. Reports absence rather than filling it.

---

## 22. `ref_them_10` / `chunk500_hybrid_enriched`

- **condition:** chunk500_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_them_10
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> What did banks say about credit card growth and card credit performance over 2023 and 2024?

**Generated answer, verbatim:**

```
Based on the provided transcripts, bank executives discussed credit card growth and credit performance for 2023 and 2024 as follows:

**Credit Card Growth**
*   **Capital One (COF):** Overall purchase volume growth was driven by an expanding branded card customer base, which includes both consumer and small business segments. While spend per customer in the consumer business remained largely flat through 2023 and the first half of 2024, it began to pick up midway through 2024 and grew further in Q4 2024. In Q2 2023, domestic card purchase volume was up 7% year-over-year, primarily powered by customer base growth rather than increased spend per account.
*   **American Express (AXP):** Total revenues were up 15% for the full year 2023 on an FX-adjusted basis. Discount revenue grew 9% for the full year 2023, driven by spending trends. Net card fee revenues grew 20% for the full year 2023. For 2024, American Express expected further momentum in net card fee revenue growth supported by product innovation and a focus on premium value propositions.

**Card Credit Performance**
*   **Capital One (COF):** Management noted that recent originations have shown stability in performance, with risk levels remaining mostly stable vintage over vintage. The front book of new origination vintages continued to perform in line with pre-pandemic levels. In Q4 2024, the charge-off rate was up 45 basis points sequentially, while the 30-plus delinquency rate remained flat compared to the prior quarter.
*   **American Express (AXP):** The company reported "strong and best-in-class credit metrics" in Q4 2023, attributing this to high customer credit quality and disciplined risk management. Write-off and delinquency rates ticked up slightly in Q4 2023 as expected. For 2024, American Express anticipated that delinquency and write-off rates would remain strong with only modest increases. The reserve rate at the end of Q4 2023 was 2.8% of total loans and card member receivables, which is approximately 10 basis points below pre-pandemic levels.
*   **JPMorgan Chase (JPM):** The bank expected its 2024 card net charge-off rate to be below 3.5%, consistent with previous guidance.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `COF_2024_Q4_qa_500_017`*

```
, your Credit Card purchase volume growth on a like account basis has picked up. I'm just trying to get a sense if this is a Q4 blip or are you thinking that the consumer is actually more confident here after the election? And are you seeing that same improvement in consumer and small business as well?

Richard Fairbank: Well, we have -- if we think about our purchase volume, our growth in overall purchase volume continues to be driven by growth in our branded card customer base and the branded card includes both our consumer and our small business. The growth that you see and that we've seen for several years now is certainly a thing powering. It has been a strength in originations and some strength in originations at the higher end of the market. But the other way to think about your question is at a customer level, what you know, on a per customer basis, what's been happening to spend growth. And even as our spend metrics were growing over overall, the spend growth per customer in our consumer business have been largely -- they had been largely flat through 2023 and really the first-half of 2024. And then they started to pick up midway through last year and they grew further in Q4. And I don't have in front of me the small business card numbers. They're embedded in the numbers that I gave you. So the fact that we have seen spend per customer finally pick up here is striking, whether it will continue and exactly what's driving it is hard to say, but I did want to point out that positive trajectory as the year finished off.

Don Fandetti: Got it. And Andrew, you touched on this, but your '24 vintage, can you talk a little bit about how you're feeling -- how you're seeing that shape up in terms of credit performance? I've seen some industry data that shows delinquencies are still pretty high for '24?

Andrew Young: Yes, Don, why don't I take that. So recent originations in our card business, we continue to see stability in the performance of our originations. It's really striking here. We've been calling this out consistently over the past few years. Vintage over vintage, we're seeing mostly stable risk levels over time. And also striking is our overall front book of new origination vintages continues to perform in line with pre-pandemic
```

*Rank 2 — `AXP_2023_Q4_prepared_remarks_500_005`*

```
4, but to still grow modestly faster than billings. Turning next to credit and provision on slide eight through 10. First and most importantly, we continue to see strong and best-in-class credit metrics. We attribute this performance to the high credit quality of our customer base, our robust risk management practices, and our disciplined growth strategy. As we had expected, our write-off and delinquency rates did continue to tick up this quarter, as you see on slide right. Going forward, we expect to see this delinquency and write-off rates remains strong with modest increases in 2024. Turning now to the accounting of this credit performance on slide nine. The modest increase in our card member loans and receivables delinquency rate combined with the quarter-over-quarter growth loan balances resulted in a $400 million reserve build. This reserve build combined with net write-offs drove $1.4 billion of provision expense in the fourth quarter. As you see on slide 10, we ended the fourth quarter with $5.4 billion of reserves, representing 2.8% of our total loans and card member receivables and continuing to reflect the premium nature of our card member base. This reserve rate remains about 10 basis points below the level we had pre-pandemic or day-one CECL. We continue to expect the reserve rate to increase a bit as we move through 2024, similar to the modest increases we've seen over the past few quarters. Moving next to revenue on slide 11. Total revenues were up 11% year-over-year in the fourth quarter and up 15% for the full-year on an FX adjusted basis. Our largest revenue line, discount revenue grew 5% year-over-year in Q4, and 9% for the full-year, as you can see on slide 12. This growth is mostly driven by the spending trends we discussed earlier. Net card fee revenues were up 17% year-over-year in the fourth quarter and 20% for the full-year, as you can see on slide 13. As we expected, growth continued to moderate a bit this quarter from the high levels we saw earlier this year, reflecting our cycle of product refreshes. In 2024, we expect to exit the year with some further momentum compared to the current growth supported by continued product innovation and our focus on premium value propositions. We currently have plans to ref
```

*Rank 3 — `COF_2023_Q2_qa_500_004`*

```
in the 4s, but staying in the 4s through 2024. That compares to our assumption last quarter of, I believe, it was 5.1%. But remember that our models tend to use the change in unemployment rates or the rate of job creation, which we're forecasting to come down to nearly 0, rather than the level of unemployment. And so it's not just about those factors, too, in our allowance. We're also considering downside scenarios that are much more severe than that baseline.

Sanjay Sakhrani: Okay. Rich, I asked this question to one of your competitors earlier. But can you just pinpoint what's exactly attractive about the growth you're seeing in card today versus in the past? They are also growing at a pretty rapid rate. And obviously, you guys have been very successful at growing this business over time, but the market remains competitive. You talked about the credit normalization. There's obviously a potential for economic challenges. I'm just trying to think through the risks.

Richard Fairbank: So Sanjay, there certainly are things to be worried about. The economy is unusual and has aspects of a lot of strength and a lot of concern. The credit normalization, we all see it. And so I'm going to make the worry case just slightly here for a second, the credit normalization has -- credit is still at very attractive levels, but it still has an upward slope to it, and nobody -- well, we certainly don't feel in a position to predict exactly where that settles out. And so we'll have to keep that very much front and center. And the market is very competitive, absolutely.

Operator: Our next question comes from Don Fandetti with Wells Fargo.

Donald Fandetti: Yes. Rich, can you talk about what you're seeing on credit card spend growth rates recently in terms of the like-for-like account basis, I know it was sort of flat to down last quarter. And do you think that we'll continue to see moderation?

Richard Fairbank: So let's pull up, first of all, our Domestic Card purchase volume was up 7% year-over-year. But that's -- to your question, Don, that's really powered by the growth in our customer base. When you look at spend per customer, this has moderated and is now generally flat from
```

*Rank 4 — `JPM_2023_Q4_prepared_remarks_500_005`*

```
the page, we've highlighted some firmwide drivers. Thematically, the biggest driver is what I might call business growth writ large. Within that, narrowly defined volume and revenue-related growth represents about $1 billion of the increase across the company as a result of an improved NIR outlook, compared to about $400 million in 2023. But in addition, the ongoing growth of the company, which continues to produce share gains and additional profitability, is coming with increased expense across a range of categories. The quantum of investment increase is comparable to last year's increase and is driven by all the same themes, bankers, branches, advisors, technology as well as marketing. Net-net, First Republic produces a modest increase in expenses, but with a significantly lower 2024 exit run rate as the result of business integration efforts. Finally, despite significantly lower inflation outlook in the economy as a whole, we still see some residual effects of inflation flowing through most of our expense categories. It's worth noting that both the general business growth and investment growth include decisions that have been executed both in response to market conditions during 2023 and to support the future growth and profitability of the company. We've included the fourth quarter 2023 exit rate on the page to illustrate that a significant portion of the year-on-year increase in expense is already in the run rate. Now, let's turn to Page 12 and cover credit and wrap up. On credit, we continue to expect the 2024 card net charge-off rate to be below 3.5%, consistent with Investor Day guidance. So in closing, we shouldn't leave 2023 without noting what an outstanding year it was, producing record revenue and net income despite some notable significant items. We're very proud of what we accomplished this year and want to thank everyone who made it possible. At the same time, we emphasized throughout 2023 the extent to which we were over-earning, as indicated by an ROTCE that is 4% above our through-the-cycle target. As we turn to 2024, it shouldn't be surprising that our outlook has us beginning to march down the path towards normalization of our returns. But despite the expected dissipation of the 2023 tailwinds and the presence of significant economic and geopolitical uncertainties, we remain optimistic about this franchise's ability to produce superior returns through a broad range of environments. And this management team remains laser
```

*Rank 5 — `COF_2024_Q4_prepared_remarks_500_003`*

```
, down 8 basis points from the prior year. As a reminder, the end of the Walmart loss-sharing agreement did not have a meaningful impact on delinquency rate. On a sequential-quarter basis, the charge-off rate was up 45 basis points. The 30-plus delinquency rate was flat compared to the linked quarter. Domestic Card non-interest expense was up 13% compared to the fourth quarter of 2023. Operating expense and marketing both increased year-over-year. Total company marketing expense in the quarter was $1.4 billion, up 10% year-over-year. Our choices in Domestic Card are the biggest driver of total company marketing. We continue to see compelling growth opportunities in our Domestic Card business. Our marketing continues to deliver strong new account growth across the Domestic Card business. Compared to the fourth quarter of 2023, Domestic Card marketing in the quarter included higher media spend and increased investment in premium benefits and differentiated customer experiences like our travel portal, airport lounges, and Capital One Shopping. Slide 12 shows fourth-quarter results in our Consumer Banking business. Auto originations were up 53% from the prior-year quarter. A portion of this growth can be attributed to overall market growth, while the remainder is the result of our strong position to pursue resilient growth in the current marketplace. As a reminder, our choices to tighten credit and pull back in anticipation of credit score inflation and declining vehicle values were still in effect in the fourth quarter of 2023, resulting in relatively low originations. These choices also drove out really basically they drove strong and stable credit performance that positioned us to lean into current marketplace opportunities and return to originations growth in 2024. With four consecutive quarters of origination growth in 2024, Consumer Banking loan balances returned to growth in the fourth quarter. Ending loans increased $2.7 billion or about 4% year-over-year and average loans were up 1%. On a linked-quarter basis, ending loans were up 2% and average loans were up 1%. Compared to the year-ago quarter, ending consumer deposits grew about 7% and average consumer deposits were up about 8%. Consumer Banking revenue for the quarter was up about 1% year-over-year. Growth in loans and deposits was partially offset by a higher year-over-year average deposit interest rate. Non-interest expense was up about 10% compared to the fourth quarter of 2023, driven largely
```

verdict: faithful

failure mode: none

notes: Every figure traces and every company and quarter is right (COF ch1/ch3/ch5, AXP ch2, JPM ch4), covering both growth and credit performance as asked. One of the strongest answers in the set.

---

## 23. `ref_them_09` / `chunk500_bm25_enriched`

- **condition:** chunk500_bm25_enriched
- **arm:** enriched
- **question_id:** ref_them_09
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> What net interest margin levels did banks report in 2023 and 2024, on reported and adjusted bases, and which way were they moving?

**Generated answer, verbatim:**

```
Based on the provided context, the following net interest margin (NIM) levels and trends were reported:

*   **M&T Bank (Q1 2024):** Reported a NIM of **3.52%**, which was down 9 basis points from the linked quarter. The decrease was driven by lower non-accrual interest, interest rate swaps, higher liquidity/cash moving into securities, and deposit mix/pricing, partially offset by asset repricing benefits.
*   **Huntington Bancshares (Q2 2023):** Anticipated a NIM of approximately **3%** by Q4 2023 (plus or minus a few basis points). The company indicated that NIM outlooks were stable to rising during 2024.
*   **Bank of America (2024):** While specific quarterly NIM percentages are not explicitly stated, the bank reported that net interest income (NII) bottomed out in Q2 2024 and increased by Q4 2024 ($13.9 billion to $14.5 billion on an FTE basis). The company expected to report record NII in 2025, implying a positive trajectory for interest income generation following the bottoming out of margins/income in mid-2024.

The context does not provide specific adjusted NIM figures or detailed NIM percentages for U.S. Bancorp or American Express.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MTB_2024_Q1_prepared_remarks_500_001`*

```
Long Island through the second phase of our Amplify Fund. We do this when our communities are successful, so is our business. Turning to Slide 4, we are excited to see how deeply we embedded sustainability across the bank and into our products and services. We have included several sustainability accomplishments from our upcoming 2023 Sustainability Report and look forward to sharing more when we release the complete report this quarter. Turning to Slide 6, which shows the results for the first quarter. The quarter was highlighted by strong C&I and consumer loan growth. PPNR was a solid $891 million. Expense control remains a key focus and was evident as adjusted expenses increased only 0.6% compared to the first quarter of 2023. Diluted GAAP earnings per share were $3.02 for the quarter. If we exclude the additional FDIC special assessment, adjusted diluted earnings per share were $3.15. On an adjusted basis, M&T's first quarter results produced an ROA and ROCE of 1.05% and 8.49%, respectively. The CET1 ratio remains strong, growing to 11.07% at the end of the first quarter and tangible book-value share grew 1% to $99.54. Next, we walk a little deeper into the underlying trends that generated our first-quarter results. Please turn to Slide 8. Taxable-equivalent net interest income was $1.7 billion in the first quarter, down 2% from linked quarter. The net interest margin was 3.52%, down 9 basis points from the linked quarter. The primary drivers for the decrease to the margin were a negative 6 basis points from lower non-accrual interest and the impact of interest rate swaps, a negative 3 basis points from higher liquidity and cash moving into securities, negative 3 basis points from our deposit mix and pricing, and a positive 3 basis points from all other items, including the benefit of asset repricing in the investment portfolio and consumer loans. Turning to Slide 9 to look at the average balance sheet trends. Average investment securities increased $1.1 billion to $28.6 billion, reflecting the reinvestment of maturing security balances and a measured shift of a portion of our cash balances into investment securities. Average interest-bearing deposits at the Fed increased approximately $0.5 billion to $30.7 billion as our decision to have more liquidity on the balance sheet was largely offset by the
```

*Rank 2 — `HBAN_2023_Q2_prepared_remarks_500_004`*

```
3 and into 2024. The 2 primary scenarios we incorporate include: one which is represented by the forward yield curve and another which assumes rates stay higher for longer and end 2024, approximately 75 basis points higher than the forward. We think this is the most likely range for short-term rates over the next 6 quarters. Based on this range, we anticipate net interest margin of approximately 3% by Q4, plus or minus a few basis points. This would equate to core net interest income on a dollar basis for the fourth quarter to be down approximately 1% to 2% from Q2 levels. As we look out further into 2024, clearly, the trends will depend on both those interest rate scenarios and what is happening with the broader economy and industry factors, including loan demand and deposit growth. That said, our modeling indicates NIM outlooks are stable to rising during 2024 which, coupled with earning asset growth, is expected to drive net interest income dollar expansion as we move through 2024. Turning to Slide 12; cost of deposits moved higher in the quarter to 1.57%. Our cumulative beta through Q2 is 32%, up 7 percentage points from the prior quarter, in line with our expectations and prior guidance. As I mentioned, we continue to expect cumulative deposit beta of approximately 40%. Turning to Slide 13; on the securities portfolio, we saw another step-up in reported yields quarter-over-quarter. We did not reinvest cash flows from securities in the second quarter as we allowed those proceeds to remain in cash given the attractive short-term rates. Cash and securities balances on average increased by $5 billion from the prior quarter as we maintained higher cash levels in the quarter. As of June 30, on an ending basis, cash and securities totaled $52 billion, representing a more normalized level as we go forward into Q3. Turning to Slide 14; our contingent liquidity continues to be robust. Our 2 primary sources of liquidity, cash and borrowing capacity at the FHLB and Federal Reserve represented $11 billion and $77 billion, respectively, at the end of Q2. At quarter end, this pool of available liquidity represented 205% of total uninsured deposits, a peer-leading coverage. Turning to Slide 15; our hedging program is dynamic, continually optimized and well diversified. Our objectives are to protect capital in uprate scenarios and protect NIM in downrate scenarios
```

*Rank 3 — `USB_2023_Q3_qa_500_008`*

```
there's two sets of rules that are yet to be finalized and coming down. Number one, are the Basel III end game finalization of rules, which will, in one shape -- one way shape or form increased capital levels. And the second is clarity on CCAR. We'll set those targets once we have clarity on those two items.

Erika Najarian: And so just to follow up here. At least until June 2024 CCAR results, regardless of how quickly you build the capital, either on an adjusted or on a GAAP basis, you're going to continue to be at pause on the buyback until at least the until we see the CCAR and the SEB?

Andy Cecere: That's my expectation, Erika. We want clarity on the finalization of the Basel III and the CCAR importantly. So, we'll be continuing to build capital and determine our capital targets and buffers and all that activity once we have more clear clarity in the finalization of the rules.

Erika Najarian: Got it. That's very clear. And just one more for John, if I may. In terms of the net interest income trajectory, I think the fourth quarter is good news, especially relative to what we thought two days ago, which would be more RWA mitigation. As we think about the RWA mitigation ahead that's less impactful to EPS, should we think about it similar to what we saw early in the year in terms of securitization? Are you more actively -- are you going to continue to use credit linked notes, which I assume has cost you 12.5% or so of the pool, plus SOFR and the spread. And as we think about those dynamics, do you feel like you have to warehouse more liquidity as we anticipate LCR rules for regional banks? Because we're also hearing that there could be pretty significant haircuts on how they're thinking about HTM as HQLA.

John Stern: Sure. Erika, so maybe I'll start with your point. On LCR, we will -- in addition to what Andy said on the capital side, we're going to have to wait and see what it is on the liquidity side in terms of any potential changes that come out of LCR. We feel very comfortable that we'll be able to achieve whatever that change is and feel that
```

*Rank 4 — `BAC_2024_Q4_prepared_remarks_500_001`*

```
, let's turn to earnings starting on page two of the presentation. This morning, we reported $6.7 billion in net income, that is $0.82 in EPS for the fourth quarter. That was a solid finish to another good year at Bank of America. We grew revenue on a year-over-year basis in every category in quarter four. We saw good loan and deposit growth, and Alastair is going to walk you through some of the details of the quarter in a moment, but I want to thank our team for another great year. For the full-year of 2024, we generated $102 billion of revenue and reported net income of $27.1 billion of EPS of $3.21. We produced 83 basis points return on assets and 13% return on tangible common equity. We generated these results working from a strong balance sheet that allowed us to support clients and economies continue to grow. The economy appears to be now settled into a 2% to 3% GDP-type growth environment. It has healthy employment levels in the resilient consumer. The immensity of the American consumer can be seen in our data. So far in the first two weeks in January, they're spending money at 4% to 5% clip over last year, similar to what they did in the fourth quarter. In our business side, the clients are profitable, they're liquid, and seeing good productivity. We ended the year with $953 billion in liquidity. We also ended with $201 billion of regulatory CET1 capital and a CET1 ratio of 11.9%, leaving us nearly 115 basis points of excess capital as we begin 2025. For Bank of America, the year was characterized by a few important highlights that played out as expected and were consistent with our communications to you throughout the year. First, we saw net interest income bottom out at $13.9 billion on an FTE basis in the second quarter of 2024. We ended the year with a fourth quarter on the same FTE basis at $14.5 billion, then that was a bit better than we expected. This obviously provides a great starting point for 2025, and based on the assumptions Alastair is going to discuss a little later, we should report record NII in 2025. So how did we do that? We drove organic growth in all the businesses, and that we have highlighted on Slide 3. We saw continued growth
```

*Rank 5 — `AXP_2023_Q1_prepared_remarks_500_005`*

```
quarter as we moved past much of the volatility in this line item that CECIL reserve builds the releases caused during the pandemic. As you see on Slide 11, we ended the first quarter with $4.4 billion of reserves representing 2.5% of our total loans and card member receivables. This reserve rate remains about 40 basis points and below the levels we had pre-pandemic or day one CECIL. We expect this reserve rate to continue to increase as we move through 2023, but to remain below pre-pandemic levels. Moving next to revenue on Slide 12, total revenues were up 22% year-over-year in the first quarter or 23% on an FX adjusted basis. Before I get into more details about our largest revenue drivers in the next few slides, I would note that service fees and other revenue was up 34% in the quarter, driven largely by the year-over-year increases in travel-related revenues that accompanied the tremendous demand we've seen for travel. As you can see on Slide 13, our largest [indiscernible] line discount revenue grew 17% year-over-year in Q1 on an FX adjusted basis, which similar to spending volumes, growth is just above last quarter’s growth rate. Net card fee revenues were up 23% year-over-year in the first quarter on an FX adjusted basis as you can see on Slide 14. Growth, which did moderate slightly this quarter as expected from the extremely high level we saw last quarter remains quite strong. This growth continues driven largely by bringing new accounts onto our fee paying products as a result of the investments we've made in our premium value propositions. This quarter, we acquired 3.4 million new cards demonstrating the demand we're seeing, especially for our premium fee-based products. Moving on to Slide 15, you can see that net interest income was up 36% year-over-year, on a FX adjusted basis accelerating versus last quarter, primarily due to the growth in our revolving loan balances. I'd also note that net yield on our card member loans increased 50 basis points sequentially reaching pre-pandemic levels this quarter as our customers increase their revolving balances. We have been able to increase our net yield while maintaining net right off rates below pre-pandemic levels, expanding our net credit margin. To sum up on revenues, on Slide 16, we're tracking
```

verdict: faithful

failure mode: none

notes: M&T (ch1), Huntington (ch2) and BAC (ch4) all correct. It keeps NII and NIM apart for BAC instead of inventing a margin, and states plainly that no adjusted-NIM figures exist for USB or AXP.

---

## 24. `ref_fact_01` / `chunk200_hybrid_enriched`

- **condition:** chunk200_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_fact_01
- **category:** factual
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** single (1 anchor) (coverage@5 = 1)
- **Check 3 flag:** not flagged

**Question:**

> What were BNY Mellon's assets under custody and administration in the first quarter of 2024, and how did they change?

**Generated answer, verbatim:**

```
In the first quarter of 2024, BNY Mellon’s firm-wide assets under custody and/or administration were $48.8 trillion, representing a 5% increase year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BK_2024_Q3_prepared_remarks_200_004`*

```
ciencies from running our company in new and better ways. Pre-tax margin and return on tangible common equity improved year-over-year to 33% and 23%, respectively. For the first time in our history, we reported over $50 trillion of assets under custody and/or administration at the end of the quarter. Now, custody is not something we are, but it is something important that we do. This number one market position improves our unique vantage point as a global financial services company, and it provides opportunity to drive value across our portfolio of adjacent businesses to deliver more of BNY to our clients. We increasingly see that the true power of BNY's client franchise exists in the combination of capabilities across our leading Security Services, Market and Wealth Services, and Investments and Wealth businesses. We have the ability to enhance this and to deliver more to our clients by bringing new innovative solutions to the market from across the seams of these businesses. As an example, we recently announced the
```

*Rank 2 — `BK_2024_Q1_prepared_remarks_200_010`*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year
```

*Rank 3 — `BK_2023_Q1_prepared_remarks_200_012`*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 — `BK_2024_Q1_prepared_remarks_200_015`*

```
supplement that we filed on March 26th for detailed reconciliations to previous disclosures. Now, starting with Security Services on Page 6. Security services reported total revenue of $2.1 billion, up 1% year-over-year. Investment services fees were up 8% year-over-year. In asset servicing, investment services fees were up 8%, driven by higher market values, net new business and higher client activity. We've remained focused on deal margins, and as a result the year-over-year impact of repricing on fee growth was de-minimis. Consistent with past quarters, we continue to see particular success with our ETF offering. ETF assets under custody and/or administration surpassed $2 trillion this quarter up over 40% year-over-year on the back of higher market values, net new business and client flows, and the number of funds serviced was up 16% year-over-year. While the pace of alternative fund launches was slower
```

*Rank 5 — `BK_2024_Q1_prepared_remarks_200_005`*

```
our clients and shareholders. As you know, we are maturing our ONE BNY Mellon initiative by implementing this mentality into the nuts and bolts processes across the company. For example, we recently announced that Ashton Thomas Securities, an independent broker dealer and registered investment advisor, will use clearing and custody services from Pershing and BNY Mellon precision direct indexing capabilities from investment management. This is a great example of multiple lines of business working together to provide holistic solutions for clients. As we continue to grow our client roster, we also know that delivering more to our existing clients represents a significant opportunity. As another example, last month we expanded on a long-standing relationship with CIFC, an alternative credit specialist and existing client of ours in asset servicing and corporate trust to bring their US direct lending strategy onto our global distribution platform. This also speaks to the incremental value that asset servicing can bring to our asset manager clients, by allowing them to tap into BNY Mellon's global distribution platform
```

verdict: faithful

failure mode: none

notes: Exact: $48.8tn, up 5% year-over-year (ch2). This is the same figure the model gave as Northern Trust's in items 11, 26, 27 and 38 — asked about the right company it answers correctly, so that failure is about not abstaining, not about misreading.

---

## 25. `ref_fact_14` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_fact_14
- **category:** factual
- **case:** C
- **outcome label:** abstained
- **coverage group:** single (1 anchor) (coverage@5 = 1)

**Question:**

> How much did BlackRock report in active equity net inflows on its third-quarter 2023 call?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BLK_2023_Q3_qa_200_014`*

```
of funds and growth outlook you think for both, obviously, alternatives, but then also the active equity segment?

Martin Small: Thanks very much for the question. So, when I think about the active equities business at BlackRock, we had continued to see a very strong active equity business over the last three years. We've generated over $30 billion in active equity net inflows, while our average AUM has grown by 34%. And so, while, again, quarter-to-quarter and year-on-year, we'd fully expect to see, particularly in this environment, some rotations out of equities and into cash, which has been the main theme, I think, of this call and the many others, we still see really strong growth in the business. And we think it's fundamentally a big part of client portfolios. I do think over time, in our product strategy, you've seen we've been adding,
```

*Rank 2 — `BLK_2023_Q3_prepared_remarks_200_005`*

```
that we don't strive to be the fastest grower in any given quarter, but we continue to drive durable, consistent organic growth, well above our peer group over the long-term. Third quarter total net inflows were $3 billion and included $49 billion of lower fee institutional index equity redemptions driven by client-specific index allocation changes. Institutional index equity represents less than 3% of BlackRock's total base fees. These lower fee strategies are often only a portion of our clients' overall relationships with BlackRock. For example, results included in the $19 billion redemption from a single client, but the clients working with us to extend its mandates and active strategies. Total quarterly annualized organic base fee decay of 2% reflected net outflows from higher fee precision ETFs and redemptions in active equity and retail liquid alternatives offerings. Third quarter revenue of $4.5 billion was 5% higher year-over-year driven by organic growth, the impact of market and
```

*Rank 3 — `BLK_2023_Q3_prepared_remarks_200_011`*

```
industry environment. Momentum in our ETF business continued with $29 billion of net inflows in the third quarter, led by core equity and fixed income ETF net inflows of $34 billion and $12 billion, respectively. Overall, ETF flows were impacted by redemptions concentrated in certain market-driven precision and fixed income products. The fourth quarter has historically been the strongest quarter of ETF flows for BlackRock when we've seen on average 35% of our annual ETF net inflows. BlackRock typically has been a large beneficiary of ETF industry seasonality related to year-end rebalancing and tax planning. In line with these historical results, we'd expect to see an acceleration in iShares ETF flows as we get closer to the end of 2023. With safe haven cash providing positive returns, retail net outflows of $4 billion primarily reflected industry pressure in active equities and liquid alternatives, partially offset
```

*Rank 4 — `BLK_2024_Q2_prepared_remarks_200_012`*

```
by fixed income and core equity ETFs, which saw $34 billion and $32 billion of net inflows, respectively. Precision ETFs added net inflows of $14 billion in the quarter, as clients reassessed their tactical portfolio allocations, adding exposures to growth equity. BlackRock's Bitcoin ETF continues to lead, gathering another $4 billion in the second quarter for $18 billion of net inflows in its first six months. Retail net inflows of $6 billion reflected continued strength in Aperio and broad-based net inflows into active fixed income. Aperio recently crossed the $100 billion AUM milestone, logging over 20% organic growth since we acquired the business a little over three years ago. As fee-based fiduciary wealth advisors grow across the world, managed model portfolios are the main way in which wealth managers are looking to scale their practices and better serve their clients. BlackRock has the leading models
```

*Rank 5 — `BLK_2023_Q4_prepared_remarks_200_033`*

```
will see a $2 billion investment in the climate opportunities across BlackRock's private debt and infrastructure equity strategies. This is one of our largest ever private markets mandates. It adds on to our very strong track record investing in the transition, including in emerging markets and extend our over $100 billion transition investment platform. BlackRock's global network of relationships, data, analytics and flexible, adaptable capital means we could source unique deals for our clients and mobilize assets and accelerate innovation and economic growth. Our active investment insights, our expertise, our strong investment performance, similarly differentiating BlackRock to the markets. We saw nearly $60 billion of active net inflows in 2023 compared to an industry outflows. Across our active franchise, BlackRock has delivered durable investment performance with 87% and 92% of fundamental equity and taxable fixed income AUM above benchmarks or peer medium for the past 5-year period. In ETF, BlackRock generated an industry-leading
```

verdict: correct abstention

failure mode: benchmark defect — the gold anchor is a three-year cumulative, and the reference answer drops that scope

notes: The gold anchor is "over $30 billion in active equity net inflows, while our average AUM has grown", from ch1. Its source sentence is preceded in the same chunk by "over the last three years" — the $30bn is a three-year cumulative, not a Q3 2023 flow. The reference answer ("BlackRock reported over $30 billion in active equity net inflows on its third-quarter 2023 call") drops that qualifier, so a correct answer to the question as read would state a three-year figure as if it answered a question about a quarter. The annotator note flags a basis concern ("a narrower slice than the headline") but not the period. Declining is defensible; the item needs the anchor or the question rescoped before it can score anything.

---

## 26. `ref_unans_01` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_unans_01
- **category:** unanswerable
- **case:** A
- **outcome label:** answered_ungrounded
- **coverage@5:** n/a (unanswerable; excluded from retrieval metrics)

**Question:**

> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Generated answer, verbatim:**

```
Northern Trust’s firm-wide assets under custody and/or administration were $48.8 billion in the first quarter of 2024, representing a 5% increase year-over-year. In the first quarter of 2023, these assets stood at $46.6 trillion, which was up 2% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `STT_2023_Q1_qa_200_047`*

```
they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it won't be quite at that level because the revenues come through over time as you get the different, I'll call it, layers of services that are provided associated with those -- that assets under custody, administration. But what we'll do is we'll -- I think it's -- that may be some kind of broad perspective. What we'll try to do each quarter is give you more and more visibility as we get to those implementation points because, remember,
```

*Rank 2 — `BK_2023_Q3_prepared_remarks_200_018`*

```
as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and
```

*Rank 3 — `BK_2023_Q1_prepared_remarks_200_012`*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 — `STT_2023_Q1_qa_200_046`*

```
said you should see a pickup in 2Q. Ron and Eric, what's your expectation for how much of that do you expect would get installed over the course of this year, 2Q, 3Q, 4Q? And by the time we exit this year, how much should be done? And therefore, what benefit should there be to [indiscernible] from that?

Eric Aboaf: Yeah. I think, Vivek, there are a couple of ways to think about that because what happens here is that it gets onboarded on -- in tranches. So we might onboard the assets under custody, administration, but there are multiple services that we're often providing for those assets. So we had a couple of wins over the last year or two years with $1 trillion. Those $1 trillion wins would have had some custody, some accounting, they might have had some performance analytics. They would have had some middle office services in many cases because
```

*Rank 5 — `BK_2024_Q1_prepared_remarks_200_010`*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year
```

verdict: should have abstained

failure mode: company substitution, plus a unit error ($48.8 billion vs. trillion) leaving the answer self-inconsistent

notes: Same substitution as item 11, plus a unit error: "$48.8 billion" against ch5's "$48.8 trillion", which leaves the answer inconsistent with its own "$46.6 trillion". The scorer flags neither — "48.8" matches as a string regardless of unit.

---

## 27. `ref_unans_01` / `chunk500_bm25`

- **condition:** chunk500_bm25
- **arm:** text_only
- **question_id:** ref_unans_01
- **category:** unanswerable
- **case:** A
- **outcome label:** answered_ungrounded
- **coverage@5:** n/a (unanswerable; excluded from retrieval metrics)

**Question:**

> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Generated answer, verbatim:**

```
In the first quarter of 2024, Northern Trust’s firm-wide assets under custody and/or administration were $48.8 trillion, representing a 5% increase year-over-year. In the first quarter of 2023, these assets stood at $46.6 trillion, which was up 2% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BK_2023_Q1_prepared_remarks_500_004`*

```
performance remains solid, AUM flows were mixed with strength in fixed income and LDI strategies partly offset by outflows in other long-term strategies. During the quarter, our U.K. investment manager Newton launched five future legacy funds, its first range of risk-rated sustainable multi-asset funds to support growth in the U.K. retirement market. And back in the U.S., the Dreyfus Bold share class, which we introduced last year, has now raised over $4 billion in AUM. In summary, over the past few months, I've spoken about our combination of client trust at scale platforms, client-focused culture and resilience as a powerful foundation on which we can build. I'm also proud that our culture has been front and center in recent weeks as our people have risen to the occasion, responding commercially and working tirelessly to enable successful outcomes for our clients in these uncertain times. I view this client-first culture as the key to make more out of our diversified portfolio of adjacent businesses. While we are the world's largest custodian and a trust bank, the contributions from Clearance and Collateral Management, Pershing, Treasury Services and Issuer Services are differentiating in our client value proposition. With that, let me officially welcome Dermot to his first earnings call. Dermot, over to you.

Dermot McDonogh: Thank you, Robin, for the introduction, and good morning, everyone. It's a privilege to be here, and I look forward to working with you all. I'll start on Page 3 of the presentation with some additional details on our consolidated financial results in the first quarter. Total revenue was $4.4 billion, up 11% year-over-year. This reflects fee revenue being flat as headwinds from lower market value, a stronger dollar and the sale of Alcentra, which closed in November last year, were offset by significant improvement in fee waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.
```

*Rank 2 — `STT_2023_Q1_qa_500_018`*

```
that that there is a range of revenue growth in our different fee categories. We've described back office as growing towards the -- traditional back office growing closer to the lower single-digit revenue growth. We've described middle and front office, which would include CRD at high single-digit growth. There will be years when it could be double-digit revenue growth. So that's what we said about that category -- this category. I think what we see in particular in software is the on-premise revenues over time will -- may not be as heavy, but we do see real momentum in the combination of the software enabled and SaaS. But all in, that should grow in the higher-single digit revenues typically though there'll be some range around that in a given year.

Vivek Juneja: Okay. And then going back to this question that's come up on the large amount of new business that remains to be installed in servicing, and you said you should see a pickup in 2Q. Ron and Eric, what's your expectation for how much of that do you expect would get installed over the course of this year, 2Q, 3Q, 4Q? And by the time we exit this year, how much should be done? And therefore, what benefit should there be to [indiscernible] from that?

Eric Aboaf: Yeah. I think, Vivek, there are a couple of ways to think about that because what happens here is that it gets onboarded on -- in tranches. So we might onboard the assets under custody, administration, but there are multiple services that we're often providing for those assets. So we had a couple of wins over the last year or two years with $1 trillion. Those $1 trillion wins would have had some custody, some accounting, they might have had some performance analytics. They would have had some middle office services in many cases because they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it
```

*Rank 3 — `BK_2023_Q3_prepared_remarks_500_007`*

```
.1 billion, up 1% year-over-year. Fee revenue was flat. 2% growth in investment services fees was offset by a 19% decline in foreign exchange revenue on the back of lower volatility and volumes. Net interest revenue was up 12%. In asset servicing, investment services fees were up 3%, driven by higher market values, healthy net new business, and a weaker dollar, partially offset by lower client transaction activity. The strength of our balance sheet, as well as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and net interest revenue increased by 6%. In Pershing, investment services fees were up 2%, reflecting higher fees on sweep balances, partially upset by the impact of lost business and lower transaction volumes consistent with the decline in US equity exchange volumes. Despite the continued headwind from the ongoing deconversion of the regional bank client highlighted in the second quarter, Pershing saw $23 billion of net new assets on the platform this quarter, reflecting positive momentum in the underlying business. As Robin mentioned earlier, the momentum around Wove is building with both new and existing clients. While at the same time, ongoing investments in the core Pershing platform to enhance advisor experience and lead with innovative solutions have positioned us well to capitalize on the heightened pace of change in the RIA community. In Treasury services, investment services fees decreased by 1% as growth from higher client activity was offset by higher earnings credits for non-interest bearing deposit balances. In clearance and collateral management, investment services fees were up
```

*Rank 4 — `BK_2024_Q1_prepared_remarks_500_004`*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year, both largely reflecting higher market values. Investment and other revenue was $182 million in the quarter. Effective January 1, we adopted new accounting guidance for our investments in renewable energy projects resulting in an approximately $50 million increase to investment and other revenue. We have restated prior periods in our earnings materials to provide you with like-for-like, year-over-year and sequential comparisons. The adoption of this new accounting guidance is largely neutral to net income and earnings per share, as the increase in provision for income taxes roughly equals the increase in investment and other revenue. Net interest income decreased by 8% year-over-year, primarily reflecting changes in the composition of deposits, partially offset by the impact of higher interest rates. Expenses were up 2% year-over-year on a reported basis and up 1% excluding notable items, primarily severance expense. Growth was from incremental investments and employee merit increases offset by efficiency savings. Provision for credit losses was $27 million in the quarter, primarily driven by reserve increases related to commercial real estate exposure. As Robin mentioned earlier, we reported earnings per share of a $1.25 up 11% year-over-year, a pre-tax margin of 29% and a return on tangible common equity of 20.7%. Excluding notable items, earnings per share were $1.29, up 14% year-over-year. Pre-tax margin was 30%, and our return on tangible common equity was 21.
```

*Rank 5 — `BK_2024_Q1_prepared_remarks_500_006`*

```
supplement that we filed on March 26th for detailed reconciliations to previous disclosures. Now, starting with Security Services on Page 6. Security services reported total revenue of $2.1 billion, up 1% year-over-year. Investment services fees were up 8% year-over-year. In asset servicing, investment services fees were up 8%, driven by higher market values, net new business and higher client activity. We've remained focused on deal margins, and as a result the year-over-year impact of repricing on fee growth was de-minimis. Consistent with past quarters, we continue to see particular success with our ETF offering. ETF assets under custody and/or administration surpassed $2 trillion this quarter up over 40% year-over-year on the back of higher market values, net new business and client flows, and the number of funds serviced was up 16% year-over-year. While the pace of alternative fund launches was slower than in the prior year quarter, investment services fees for alternatives were up over 10% on a year-over-year basis. Throughout the quarter, we saw broad-based strength across client segments, products and regions. In issuer services, investment services fees were up 11% reflecting net new business across both depository receipts and corporate trust, as well as higher cancellation fees in depository receipts. Foreign exchange revenue was down 11% year-over-year and net interest income was down 12%. Expenses of $1.5 billion were flat year-over-year, reflecting incremental investments, as well as the impact of employee merit increases offset by efficiency savings. Pre-tax income was $591 million, a 4% increase year-over-year, and pre-tax margin expanded to 28%. Next, Market and Wealth Services on Page 7. Market and Wealth Services reported total revenue of $1.5 billion, up 3% year-over-year. Total investment services fees were up 7% year-over-year. In Pershing, investment services fees were up 3%, reflecting higher market values and client activity, partially offset by the impact of business lost in the prior year. Net new assets were negative $2 billion for the quarter, reflecting the ongoing deconversion of the before-mentioned lost business. Client demand for our Wealth Advisor platform, Wove, continues to be strong. In the first quarter, we signed nine additional client agreements,
```

verdict: should have abstained

failure mode: company substitution — BNY Mellon's AUCA reported as Northern Trust's

notes: Same as items 11 and 26, with units correct here. Three conditions, one fabrication.

---

## 28. `ref_them_09` / `chunk200_hybrid_enriched`

- **condition:** chunk200_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_them_09
- **category:** thematic
- **case:** B
- **outcome label:** answered_ungrounded
- **coverage@5:** 0

**Question:**

> What net interest margin levels did banks report in 2023 and 2024, on reported and adjusted bases, and which way were they moving?

**Generated answer, verbatim:**

```
Based on the provided context, here are the reported net interest margin (NIM) levels and trends for 2023 and 2024:

**Huntington Bancshares (HBAN)**
*   **Q4 2023:** The bank anticipated NIM to be between **305 basis points and 310 basis points**. This was an increase of 5 to 10 basis points compared to previous guidance.
*   **2024 Outlook:** Management modeled NIM to trend **flat to higher** from the Q4 2023 endpoint. By Q4 2024, they anticipated NIM of approximately **3% (300 basis points)**, plus or minus a few basis points.

**First Interstate BancSystem (FITB)**
*   **Q1 2024:** Net interest margin improved by **1 basis point** sequentially. This was noted as the first sequential improvement since Q4 2022. The text does not provide specific NIM levels for 2023, only noting that the Q1 2024 increase was driven by higher yields on new fixed-rate consumer loans and day count benefits, partially offset by deposit migration to interest-bearing accounts.

**U.S. Bancorp (USB)**
*   **Q4 2023:** The context provides net interest income figures ($4.14 billion annualized) but does not explicitly state the specific NIM percentage level for Q4 2023 or 2024. It notes that NIM reflected market dynamics including deposit pricing pressure and unfavorable shifts in deposit mix, partially offset by better earning asset spreads.

**Summary of Direction:**
*   **HBAN:** Moving from a higher point in late 2023 (approx. 305-310 bps) to a slightly lower or stable level in late 2024 (approx. 300 bps), with the full-year 2024 trend described as flat to rising relative to the Q4 2023 start.
*   **FITB:** Moving upward sequentially in Q1 2024 (+1 bps).
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `USB_2023_Q4_prepared_remarks_200_006`*

```
interest margin reflected market dynamics including deposit pricing pressure and unfavorable shifts in the deposit mix, partially offset by better earning asset spreads and improved total funding mix. In the first quarter of 2024, we expect net interest income on a fully-taxable equivalent basis to be in the range of $4.0 billion to $4.1 billion. For the full year 2024, we expect net interest income on a fully-taxable equivalent basis to be consistent with our annualized fourth quarter 2023 net interest income level of approximately $4.14 billion to up slightly. Slide 10 highlights trends in noninterest income. Noninterest income, as adjusted, increased 12.1% on a year-over-year basis, driven by new account growth and deepening relationships across the business. Year-over-year payment service revenue benefited by continued strength in consumer and business spending activities, while increases in trust and investment management fees and commercial product revenue were driven by underlying
```

*Rank 2 — `HBAN_2023_Q2_prepared_remarks_200_010`*

```
3 and into 2024. The 2 primary scenarios we incorporate include: one which is represented by the forward yield curve and another which assumes rates stay higher for longer and end 2024, approximately 75 basis points higher than the forward. We think this is the most likely range for short-term rates over the next 6 quarters. Based on this range, we anticipate net interest margin of approximately 3% by Q4, plus or minus a few basis points. This would equate to core net interest income on a dollar basis for the fourth quarter to be down approximately 1% to 2% from Q2 levels. As we look out further into 2024, clearly, the trends will depend on both those interest rate scenarios and what is happening with the broader economy and industry factors, including loan demand and deposit growth. That said, our modeling indicates NIM outlooks are stable to rising during 2024 which, coupled with earning asset growth, is expected to drive net interest income dollar expansion as
```

*Rank 3 — `FITB_2023_Q4_qa_200_028`*

```
, obviously, the overall charge-off outlook for this year is fairly benign 35 to 45 basis points. Any more color in terms of drivers of call it, the midpoint of that range versus 2023 levels?

Greg Schroeck: I think we're going to continue to see a lot of what we saw in 2024 with what we saw in 2023, right? We don't have any significant trends geographically or by product. And so what we saw in 2023 was a little bit more episodic. And based on what we're seeing on the C&I side right now, I mean, our borrowers have done a nice job both on the executing on the revenue expense management side, there's obviously margin compression. But overall, as Tim said earlier, they're looking for the same things we're looking for, which is what is the Fed going to do and when. We hear a lot about labor costs, so they're
```

*Rank 4 — `FITB_2024_Q1_prepared_remarks_200_008`*

```
economic and interest rate environments. Net interest margin improved 1 basis point for the quarter. Increased yields on new production of fixed rate consumer loans and day count benefits contribute to the growth and were partially offset by the deposit balance migration from demand to interest-bearing accounts. This increase in NIM is the first sequential improvement since the fourth quarter of 2022. Excluding the impacts of security gains and the Visa total return swap, adjusted non-interest income decreased 1% from a year ago quarter due to lower revenue in commercial banking, leasing and mortgage, partially offset by strong growth in treasury management and wealth and asset management fees, where both saw double-digit revenue growth over the prior year. The securities gains of $10 million reflected the mark-to-market impact of our non-qualified deferred compensation plan, which is more than offset in compensation expense. Adjusted non-interest expense decreased 1% compared to the year ago quarter due to our continued focus on expense discipline and the ongoing benefits from our process
```

*Rank 5 — `HBAN_2023_Q3_prepared_remarks_200_010`*

```
loan growth and funding mix continue to perform very well. These factors resulted in the margin coming in better than we had expected when we shared our outlook in July. We continue to analyze multiple potential interest rate scenarios. The basis of our planning and guidance continues to be a central set of those scenarios that is bounded on the low end by the forward yield curve and at the high end by a scenario that projects rates stay higher for longer. The higher for longer scenario today assumes one additional rate increase in 2023, flat Fed funds through October of 2024, and ends 2024 approximately 75 basis points higher than the forward curve. With the move and rates higher, we now anticipate net interest margin for the fourth quarter to be around 305 basis points to 310 basis points. This is 5 basis points to 10 basis points higher than the level we shared previously. Looking further out, our modeling continues to indicate 2024 NIM trending flat to higher from the Q4 2023 endpoint. Turning to
```

verdict: unfaithful

failure mode: wrong company name (FITB as First Interstate) and wrong year (Q4 2023 guidance given as Q4 2024), which inverts the stated direction

notes: Two real errors, neither caught. "First Interstate BancSystem (FITB)" — FITB is Fifth Third, and the content from ch4 is Fifth Third's. And ch2's "approximately 3% by Q4" is Huntington guiding to Q4 2023, given here as Q4 2024, which makes the closing "Summary of Direction" (305-310 falling to 300) wrong. The flagged claim is instead "300", the model's own basis-point gloss on 3%.

---

## 29. `ref_them_09` / `chunk500_hybrid_enriched`

- **condition:** chunk500_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_them_09
- **category:** thematic
- **case:** B
- **outcome label:** answered_ungrounded
- **coverage@5:** 0

**Question:**

> What net interest margin levels did banks report in 2023 and 2024, on reported and adjusted bases, and which way were they moving?

**Generated answer, verbatim:**

```
Based on the provided context, here are the reported Net Interest Margin (NIM) levels and trends for the specified banks:

**Huntington Bancshares (HBAN)**
*   **2023 Q4:** The bank indicated that if a lower rate scenario played out with cuts as early as March 2024, the margin would remain near the level seen in Q4 2023. While the exact Q4 2023 NIM percentage is not explicitly stated in this chunk, it serves as the baseline for the 2024 outlook.
*   **2024 Outlook:** The bank expects a net interest margin between **3% and 3.1%** for each quarter of 2024 under the lower rate scenario (five cuts). If rates stay "higher for longer" (three cuts), they expect the margin to expand up to **10 basis points above** that range (i.e., approximately 3.1% to 3.2%).
*   **Trend:** The NIM is expected to be stable or slightly rising depending on the interest rate scenario, with dollar-based net interest income troughing in Q1 2024 before expanding sequentially.

**Bank of America (BAC)**
*   **2023 Q4:** The net interest yield declined by 14 basis points to **197 basis points**.
*   **Trend:** NII was expected to decline slightly in Q1 and Q2 2024 due to rate curve shifts and fewer days, but begin to grow sequentially in the second half of 2024.

**JPMorgan Chase (JPM)**
*   **Reported/Adjusted Levels:** The text does not provide a specific percentage for NIM. It reports that Q3 2023 NII ex-Markets run rate was $94 billion and guides full-year 2024 NII ex-Markets to approximately $88 billion, implying sequential quarterly declines throughout 2024 due to lower rates (six cuts assumed).
*   **Trend:** The bank is asset-sensitive, so lower rates are expected to decrease NII.

**U.S. Bancorp (USB)**
*   **2023 Q4:** The net interest margin was **2.78%**, representing a 3 basis point decline from the prior quarter.
*   **Trend:** The decline in Q4 2023 was driven by deposit pricing pressure and unfavorable mix shifts, partially offset by better earning asset spreads. For 2024, NII is expected to be consistent with or slightly up from the annualized Q4 2023 level (~$4.14 billion), suggesting a stable margin environment.

**Note on Adjusted Bases:** The provided context does not distinguish between "reported" and "adjusted" Net Interest Margin percentages for any of the banks; it primarily discusses NII (Net Interest Income) in dollar terms or NIM as a single reported metric.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `HBAN_2023_Q2_prepared_remarks_500_004`*

```
3 and into 2024. The 2 primary scenarios we incorporate include: one which is represented by the forward yield curve and another which assumes rates stay higher for longer and end 2024, approximately 75 basis points higher than the forward. We think this is the most likely range for short-term rates over the next 6 quarters. Based on this range, we anticipate net interest margin of approximately 3% by Q4, plus or minus a few basis points. This would equate to core net interest income on a dollar basis for the fourth quarter to be down approximately 1% to 2% from Q2 levels. As we look out further into 2024, clearly, the trends will depend on both those interest rate scenarios and what is happening with the broader economy and industry factors, including loan demand and deposit growth. That said, our modeling indicates NIM outlooks are stable to rising during 2024 which, coupled with earning asset growth, is expected to drive net interest income dollar expansion as we move through 2024. Turning to Slide 12; cost of deposits moved higher in the quarter to 1.57%. Our cumulative beta through Q2 is 32%, up 7 percentage points from the prior quarter, in line with our expectations and prior guidance. As I mentioned, we continue to expect cumulative deposit beta of approximately 40%. Turning to Slide 13; on the securities portfolio, we saw another step-up in reported yields quarter-over-quarter. We did not reinvest cash flows from securities in the second quarter as we allowed those proceeds to remain in cash given the attractive short-term rates. Cash and securities balances on average increased by $5 billion from the prior quarter as we maintained higher cash levels in the quarter. As of June 30, on an ending basis, cash and securities totaled $52 billion, representing a more normalized level as we go forward into Q3. Turning to Slide 14; our contingent liquidity continues to be robust. Our 2 primary sources of liquidity, cash and borrowing capacity at the FHLB and Federal Reserve represented $11 billion and $77 billion, respectively, at the end of Q2. At quarter end, this pool of available liquidity represented 205% of total uninsured deposits, a peer-leading coverage. Turning to Slide 15; our hedging program is dynamic, continually optimized and well diversified. Our objectives are to protect capital in uprate scenarios and protect NIM in downrate scenarios
```

*Rank 2 — `BAC_2023_Q4_prepared_remarks_500_009`*

```
interest-rate reductions we've seen in the fourth quarter, we experienced an improvement of more than $30 billion in the valuation of the hold-to-maturity securities. So, let's turn our focus to NII performance using Slide 10. And a strong finish to the year helped us report $57.5 billion in NII on a fully tax-equivalent basis for the full year of 2023. That's up 9% compared to 2022. On an FTE basis, we reported $14.1 billion in NII, which was modestly better than we told you to expect last quarter driven by modestly better deposit growth. The $14.1 billion was a decline of $400 million from the third quarter, driven by the unfavorable impacts of deposits and related pricing and lower global markets NII, partially offset by higher rates benefiting asset yields. And as we look forward, given that we've got one less day of interest in the first quarter and that's worth about $125 million to $150 million, and given the rate curve shift, we believe the first quarter will be somewhere between $100 million and $200 million lower than the fourth quarter. It could move a touch lower in Q2 and then we believe it should begin to grow sequentially in the second half of 2024. So very consistent with our prior guidance. With regard to the forward view I just provided, let me note a few other caveats. It would include an assumption that interest rates in the forward curve materialize. And the forward curve today has six cuts compared to last quarter when we had three cuts in the 2024 curve. So it's bouncing around a little and shifted in the past quarter. Forward view also includes our expectation of low to mid-single-digit loan growth and some moderate growth in deposits as we move into the back half of 2024. Given our recent deposit and loan performance, we continue to feel good about these assumptions. Before moving away, it's worth noting our net interest yield declined 14 basis points to 197 basis points. And that's driven by the decline in NII, as well as higher average earning assets, reflecting prior period builds of cash and cash-like securities. Turning to asset sensitivity and focusing on a forward yield curve basis, the plus 100 basis point parallel shift at December 31st was $3.5 billion of expected NII over the next 12 months, coming from our banking
```

*Rank 3 — `JPM_2023_Q4_prepared_remarks_500_004`*

```
689 million. Revenue of $1.8 billion was up $597 million year-on-year. NII of $2.5 billion was up $1.2 billion year-on-year due to the impact of higher rates and balance sheet mix. NIR was a net loss of $687 million compared to the net loss of $115 million, and included the net investment securities losses I mentioned upfront. And expenses of $3.4 billion were up $3 billion year-on-year, predominantly driven by the FDIC special assessment. With that, let's pivot to the outlook for 2024, starting with NII on Page 10. We expect 2024 NII ex-Markets to be approximately $88 billion. Going through the drivers, the outlook assumes that rates follow the forward curve, which currently includes six cuts this year. On deposits, we expect balances to be very modestly down from current levels. While lower rates should decrease repricing pressure, we remain asset sensitive, and therefore the lower rates will decrease NII, resulting in more normal deposit margins. We expect strong loan growth in Card to continue, but not at the same pace as 2023. Still, this should help offset some of the impact of lower rates. Outside of Card, loan growth will likely remain muted. It's important to note that we just reported a quarterly NII ex-Markets run rate of $94 billion. Combining that with the full-year guidance of approximately $88 billion implies meaningful sequential quarterly declines throughout 2024, consistent with what we've been telling you for some time. And keep in mind that many of the sources of uncertainty that we've highlighted previously surrounding the NII outlook remain. And on total NII, we expect it to be approximately $90 billion for the full-year, reflecting an increase in Markets NII which, as always, you should think of as largely offset in NIR. Now, let's turn to expenses on Page 11. We expect 2024 adjusted expense to be about $90 billion. You'll see on the slide we provided detail by line of business. Generally, you can see that both in dollar terms and in percentage terms, the expense growth is aligned to where the greatest opportunities are, both in terms of share and available returns. And of course, you'll hear more at Investor Day and between now and then. On the right-hand side of
```

*Rank 4 — `HBAN_2023_Q4_prepared_remarks_500_004`*

```
We have seen notable increases in fixed asset portfolio yields thus far in the rate cycle. Even as the forward curve forecast lower short-term rates, many of our fixed-rate loan portfolios retained substantial upside repricing opportunity for some time to come. We forecast approximately $13 billion to $15 billion of fixed-rate loan repricing opportunity in 2024, with an estimated yield benefit of approximately 350 basis points. Slide 14 provides the drivers of our spread revenue growth. As a reminder, we continue to analyze and develop action plans for a wide range of potential economic and interest rate scenarios. The basis of our planning and guidance continues to be a central set of those scenarios that is bounded on the lower end by a scenario which includes five rate cuts in 2024. The higher scenario assumes rates stay higher for longer and tracks closely with the Fed's dot plot from year end. This scenario assumes three cuts in 2024. We continue to be focused on managing net interest margin in a tighter corridor. Should the lower rate scenario play out and we see rate cuts as early as March, that will likely result in a margin over the course of the year within a range near the level we saw in the fourth quarter. This would equate to a net interest margin between 3% and 3.1% for each quarter of 2024. If the higher for longer scenario comes to pass, we expect the margin to expand and at a level that is up to 10 basis points above that. As we saw in December, the outlook for longer-term interest rates also moved lower significantly. There were a number of benefits from this lower market rate outlook. First, it resulted in higher capital levels given AOCI accretion, which supports our accelerated loan growth outlook now. Second, it provides for easing deposit competition over time. Third, it provides credit support for borrowers with the potential for locking in lower long-term rates. However, the rate outlook is incrementally more challenging for full-year spread revenue than the levels we had seen underlying our guidance in December. Net of these items, including the forecasted pace of loan growth, we now expect net interest income on a dollar basis to trough in the first quarter before expanding sequentially from that level over the course of the year. Turning to Slide 15, our contingent and available liquidity continues to be robust at $93 billion and has grown quarter-over-quarter. At quarter end, we continue to benefit from a
```

*Rank 5 — `USB_2023_Q4_prepared_remarks_500_002`*

```
strong deposit balances in the third quarter, we moderated our deposit pricing somewhat in the fourth quarter even as we grew consumer deposits by 1%. During the quarter, we rebalanced a portion of our securities portfolio, which provided risk-weighted asset relief and improved our overall earnings trajectory. The average yield on total investment securities portfolio increased to 2.97% for the fourth quarter, a 55 basis point increase compared to a year earlier. As of December 31, the ending balance on the total investment securities portfolio was $161 billion. During the quarter, effective duration on the available for sale portfolio declined to less than three years as unrealized losses, net of tax, improved by approximately $2 billion given the movement in rates and repositioning. Turning to Slide 9, net interest income on a fully-taxable equivalent basis declined 3.0% linked quarter, driven by a modest decline in the net interest margin of 2.78%. The 3 basis point decline in the net interest margin reflected market dynamics including deposit pricing pressure and unfavorable shifts in the deposit mix, partially offset by better earning asset spreads and improved total funding mix. In the first quarter of 2024, we expect net interest income on a fully-taxable equivalent basis to be in the range of $4.0 billion to $4.1 billion. For the full year 2024, we expect net interest income on a fully-taxable equivalent basis to be consistent with our annualized fourth quarter 2023 net interest income level of approximately $4.14 billion to up slightly. Slide 10 highlights trends in noninterest income. Noninterest income, as adjusted, increased 12.1% on a year-over-year basis, driven by new account growth and deepening relationships across the business. Year-over-year payment service revenue benefited by continued strength in consumer and business spending activities, while increases in trust and investment management fees and commercial product revenue were driven by underlying market activity, a full fourth quarter with Union Bank, and core growth. Turning to Slide 11, noninterest expenses, as adjusted, decreased by 1.0% on a linked-quarter basis, driven by lower compensation-related expense that was partially offset by strategic investments in marketing and business development. Slide 12 highlights our credit quality performance. Asset quality metrics trended in-line with expectations, and key metrics continue to normalize toward pre-pandemic levels. Our ratio
```

verdict: faithful

failure mode: none — the flagged claim is the model's own arithmetic, correctly flagged by the stated rule

notes: Accurate throughout (HBAN ch4, BAC ch2, JPM ch3, USB ch5), and honest that the context never separates reported from adjusted NIM. The flagged claim is "3.2", from "up to 10 basis points above that range (i.e., approximately 3.1% to 3.2%)". Checked: 3.2 appears in no chunk in any form — it is the model's own addition, explicitly marked "i.e.". So the outcome label is CORRECT under the documented rule (every numeric claim must appear verbatim); what it does not capture is that a transparent derivation is not a fabrication. A limitation of the rule, not a defect in its implementation.

---

## 30. `ref_comp_10` / `chunk500_bm25`

- **condition:** chunk500_bm25
- **arm:** text_only
- **question_id:** ref_comp_10
- **category:** comparative
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did PNC and Fifth Third each treat AOCI when describing their capital and tangible book value per share during 2023?

**Generated answer, verbatim:**

```
Based on the provided context, **PNC** reported a negative AOCI of $9.5 billion at quarter-end in Q2 2023, which resulted in a tangible book value of $77.80 per common share (a 5% increase year-over-year). The text does not explicitly state that PNC adjusted its capital ratios or TBVPS by excluding AOCI for this specific metric, though it notes the negative balance.

**Fifth Third** treated AOCI as a significant factor affecting tangible book value per share (TBVPS) and regulatory capital in multiple quarters during 2023:
*   **Q1:** The company noted that OCI impacts reduced their adjusted CET1 ratio to 7.6% (compared to the reported 9.55%) and lowered their Tangible Common Equity (TCE) ratio by 13 basis points due to higher cash balances. They explicitly stated that adjusting for AOCI, their TCE ratio was 7.27% and TBVPS increased to $9.23.
*   **Q2:** The company highlighted that TBVPS *excluding* AOCI increased 11% compared to the year-ago quarter. They also projected that approximately 36% of their current unrealized loss position (AOCI) would accrete back into equity by the end of 2024.
*   **Q3:** Management discussed how the AOCI mark erodes tangible book value per share but noted that if rates fell, there would be significant TBVPS accretion. They also modeled the capital impact of fully phased-in AOCI on CET1 at approximately 125 basis points by Q3 2028.
*   **Q4:** The company reported that TBVPS grew nearly 30% in the quarter, partly due to a rally in interest rates reducing the negative AOCI mark. They also moved $12.6 billion of securities to held-to-maturity to de-risk potential AOCI volatility to capital by about 30%.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `FITB_2023_Q3_qa_500_002`*

```
we know our portfolio is going to pay down.  And we know that this is going to be very manageable from a regulatory capital perspective. When we model the capital impact at a fully phased-in level on AOCI, the impact on CET1 is about 125 basis points when you reach the third quarter of 2028 and that's why we continue to accrete CET1 is to be able to have sufficient regulatory capital for that world. And in fact, should rates get north of 8%. We would still be maintaining a CET1 well above regulatory minimums would be over 8% CET1 in that environment.  So we feel good about how we're positioned, how we will roll down the curve and ultimately, the regulatory capital. It's just one of the challenges in this environment with everything in AFS is that you have that mark on the tangible book value per share, that erosion. But at the same time, should rates fall. I think all of you would be very pleased with how much tangible book value accretion, we would report in that environment.

TimothySpence: And Scott, if I just put a point on the last thing, Jamie you said. I mean, we believe investors want us to do what is best for managing the business and for recognizing the fact that options have value but if you believe that the AOCI mark is weighing on the stock, then the other way to look at it is the burn down is 25% accretion in tangible book value per share in the next two years, just given the current outlook on rates, which is a pretty unique buying opportunity, be the other way to look at it.

ScottSiefers: Yes, I agree. All right. That's perfect. So Tim and Jamie, thank you both.

Operator: And your next question comes from the line of Erika Najarian from UBS.

ErikaNajarian: Jamie, this first one is for you. Not to belabor the earlier point, but all the PPNR metrics and balance sheet metrics look great and also did the forward look? And I guess, if you could just explain what happened in the quarter, I think given that your portfolio -- your securities portfolio is 61% CMBS. I think investors that know you well, expected not as much negative convexity -- was there something unique that happened in this quarter in the portfolio that -- where the AOCI was that
```

*Rank 2 — `FITB_2023_Q4_prepared_remarks_500_001`*

```
AOCI of 15.9% and an adjusted efficiency ratio of 55.9%. All among the best of our peers. We also continue to take market share organically by growing our customer base and deepening relationships. We grew consumer households by 3% overall punctuated by 6% growth in the Southeast. In commercial, we added a record number of new quality middle market relationships up 11% over the prior year. As a result, we grew or maintained our deposit market share position in all 40 of our largest MSAs. As we turn the page to 2024, we remain focused on differentiating Fifth Third based on the strength and consistency of our financial performance by prioritizing stability, profitability, and growth in that order. Bryan will take you through the detail on the fourth quarter and our outlook for the year shortly. But before that, I would like to touch on a few points. The first of these is the strength of our balance sheet. Our defensive positioning and decision to move quickly to adapt to proposed regulatory changes have put us in a position to play offense in 2024. Having achieved full Category 1 LCR compliance on August 31st and maintained it since, our liquidity position is very strong. We completed our RWA diet in the fourth quarter and accreted nearly 50 basis points of CET1, putting us on pace to reach a 10.5% CET1 ratio by mid-year 2024. Given our strong earnings profile and the significant rally in interest rates in December, our tangible book value per share grew nearly 30% during the fourth quarter. At the beginning of January, we moved $12.6 billion of securities to held-to-maturity, representing roughly one quarter of our AFS portfolio. We expect this move will de-risk potential AOCI volatility to capital by about 30% in the event that market rates rise again. If the economic outlook remains stable and the capital rules are finalized, no worse than the current NPR. These actions put us in a position to resume share repurchases of up to $300 million to $400 million in the second half of 2024, including $100 million to $200 million as early as the beginning of the third quarter. Should the final rules prove less stringent than the initial proposals, we'll have additional flexibility in deploying excess capital and liquidity to further improve profitability and position Fifth Third for growth. The second point I'd like to highlight is
```

*Rank 3 — `FITB_2023_Q2_prepared_remarks_500_005`*

```
closely and believe the overall impact on Fifth Third will be limited. We had deemphasized office even before the pandemic, and we are not currently pursuing new office CRE originations. From an overall credit management perspective, we have continually improved the granularity and diversification of our loan portfolios through a focus on generating and maintaining high-quality relationships. As many of you know, we have been and remain cautious in our economic outlook. We tightened underwriting standards during COVID, including stressing credits to an up 200-basis-point scenario off the forward curve, which limited our growth but improved the stability of our balance sheet. Since we began tightening underwriting standards, roughly 90% of our commercial portfolio has been re-underwritten. Our criticized assets have been stable over the past several quarters. Across all loan categories, we continue to closely monitor exposures where inflation and higher rates may cause stress. Moving to the ACL. Our reserves increased $87 million, reflecting the impacts of dividend finance and Moody's macroeconomic forecast, which eroded slightly. The ACL ratio increased nine basis points sequentially. As you know, we incorporate Moody's macroeconomic scenarios when evaluating our allowance. The base economic scenario from Moody's assumes the unemployment rate reaches 4.3%, while the downside scenario incorporates a peak unemployment rate of 7.8%. We maintained our scenario weightings of 80% to the base and 10% to each of the upside and downside scenarios. Moving to capital. Our CET1 ratio increased 25 basis points sequentially, ending the quarter at over 9.5%. Our capital position reflects our ability to build capital quickly through our strong earnings generation. Our tangible book value per share, excluding AOCI, increased 11% compared to the year ago quarter. We continue to expect a meaningful improvement in our unrealized loss position, assuming the forward curve plays out, resulting in approximately 36% of our current loss position accreting back into equity by the end of 2024 and approximately 50% by the end of 2025. Looking forward, we expect to build capital at an accelerated pace given our RWA optimization initiatives and by extending our share buyback pause. As Tim mentioned, we will postpone repurchases until we have more clarity on the regulatory environment in order to determine the new level of required capital dollars. Assuming we do not buy back shares through year-end, we would antici
```

*Rank 4 — `PNC_2023_Q2_prepared_remarks_500_001`*

```
are taking a hard look at opportunities for even further expense improvements across the franchise.  Third, credit quality for the quarter remained strong reflecting our diversified lending franchise and our focus on developing valuable, sustainable businesses based on long term customer relationships.  And finally, I'd like to thank our employees for their efforts and contributions during the quarter.  And with that, I'll turn it over to Rob.

Robert Reilly: Thanks, Bill, and good morning, everyone. Our balance sheet is on Slide 3 and we're presenting on an average basis and comparing to the first quarter. Loans were stable at $325 billion. Investment securities declined $2 billion or 2%. Cash balances at the Federal Reserve were $31 billion and decreased $3 billion, deposits of $426 billion declined $10 billion or 2%. Borrowed funds increased $3 billion. As an aside, since 2021, we've been deliberate in issuing TLAC compliant debt. So we're confident we'll meet the upcoming TLAC requirements through our normal course of funding.  At quarter end, AOCI was a negative $9.5 billion, and tangible book value was $77.80 per common share, an increase of 5% compared to the same period a year ago. We remain well capitalized with an estimated CET1 ratio of 9.5% as of June 30, 2023, which increased 30 basis points linked quarter. We returned approximately $700 million of capital to shareholders in the quarter, which included $600 million of common dividends and approximately a $100 million of share repurchases or 1.1 million shares.  And as Bill just mentioned, our Board recently approved a $0.05 increase to our quarterly cash dividend on common stock, raising the dividend to a $1.55 per share. Our recent CCAR results underscore the strength of our balance sheet. And as previously announced, our current stress capital buffer of 2.9% will improve to the regulatory minimum of 2.5% for the four quarter period beginning in October 2023. Due to the expected issuance by the Federal banking agencies of proposed rules to adjust the Basel III capital framework, share repurchase activity in the third quarter is expected to remain modest. We will continue to monitor this and may adjust share repurchase activity as appropriate.  Slide 4 shows our loans in more detail. Second quarter loans averaged $325 billion and increased $20 billion or 6% compared
```

*Rank 5 — `HBAN_2023_Q1_prepared_remarks_500_006`*

```
to Slide 18. GAAP noninterest expense increased by $9 million. Adjusted for notable items, core expenses decreased by $18 million, driven by lower personnel expense, primarily as a result of reduced incentives and revenue driven compensation. We're proactively managing expenses and have taken actions over the last several quarters to orient to a low level of expense growth in order to deliver positive operating leverage and self-fund strategic investments. Slide 19 recaps our capital position. Common equity Tier 1 increased to 9.55% and has increased sequentially for three quarters. OCI impacts to common equity Tier 1 resulted in an adjusted CET1 ratio of 7.6%. As a reminder, the reported regulatory capital framework does not include OCI impacts in the capital calculation. Our tangible common equity ratio, or TCE, increased 22 basis points to 5.7%. Note that we were holding higher cash balances at the end of Q1, which reduced the TCE ratio by 13 basis points. Adjusting for AOCI, our TCE ratio was 7.27%. Tangible book value per share increased by 7% from the prior quarter to $7.32. Adjusting for AOCI, tangible book value increased to $9.23, and has increased for the past four quarters. Our capital management strategy for the balance of 2023 will result in expanding capital over the course of the year, while maintaining our top priority to fund high-return loan growth. We intend to grow CET1 to the top end of our 9% to 10% operating range by the end of the year. We believe this is a prudent approach given the dynamic environment.  Based on our expectation for continued loan growth, we do not expect to utilize the share repurchase program during 2023. Turning to Slide 20. Our capital plus reserves is top quartile in the peer group and gives us substantial total loss absorption capacity. On Slide 21, credit quality continues to perform very well. As mentioned, net charge-offs were 19 basis points for the quarter. This was higher than last quarter by 2 basis points and up 12 basis points from the prior year as charge-offs continue to normalize.  Non-performing assets declined from the previous quarter and have reduced for seven consecutive quarters. Allowance for credit losses was flat at 1.9% of total loans. Turning to Slide 22. We have provided incremental disclosures on our commercial real estate balances. This
```

verdict: unfaithful

failure mode: company misattribution — Huntington's Q1 2023 capital metrics reported as Fifth Third's, on a comparative question

notes: PNC correct (ch4). Fifth Third's Q2, Q3 and Q4 bullets correct (ch3, ch1, ch2). The Q1 bullet — adjusted CET1 7.6%, TCE 7.27%, TBVPS $9.23 — is Huntington's, from ch5 (HBAN_2023_Q1), presented as Fifth Third's. A full paragraph of one bank's capital metrics under another's name, on a comparative question, labelled answered_grounded_correct.

---

## 31. `ref_them_04` / `chunk200_hybrid`

- **condition:** chunk200_hybrid
- **arm:** text_only
- **question_id:** ref_them_04
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Generated answer, verbatim:**

```
In late 2023, Bank of America reported achieving 170 basis points of operating leverage, driven by expense discipline that reduced headcount and expenses every quarter despite strong revenue growth. In early 2024, Bank of New York Mellon (BNY) stated it started the year determined to at least break even on operating leverage, a goal considered ambitious due to an expected 10% net interest income (NII) headwind. BNY ultimately delivered 968 basis points of positive operating leverage on a reported basis for the full year 2024. Additionally, U.S. Bank indicated in late 2024 that it expected to achieve greater than 200 basis points of positive operating leverage for the full year 2025, following approximately 30 basis points of positive operating leverage in Q3 2024 and 190 basis points in Q4 2024.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BAC_2023_Q4_prepared_remarks_200_005`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as
```

*Rank 2 — `BK_2024_Q4_prepared_remarks_200_006`*

```
. We've worked hard to say what we do and to do what we say. And so, turning to Page 4, I'm pleased that in 2024, we once again met or exceeded our financial goals for the year. We are confident that BNY can deliver positive operating leverage across a wide range of scenarios and so we started 2024 determined to at least breakeven from an operating leverage perspective. That was an ambitious goal at the time, considering that our revenue outlook at the beginning of the year foresaw an approximately 10% NII headwind to largely offset growth in fee revenue. Therefore, we had to set up to keep expenses, excluding notable items roughly flat, while at the same time self-funding incremental investments in the business. Dermot will discuss the financials in more detail, but in summary, in 2024, we delivered 968 basis points of positive operating leverage on a reported basis and 288 basis points, excluding notable items. We grew
```

*Rank 3 — `USB_2024_Q3_qa_200_005`*

```
have anything contemplated at this particular point in time.

John Pancari: Okay. All right. Thank you. And then separately, on the expense side, you put up some pretty good positive operating leverage this quarter, and you implied that fourth quarter you'll see that as well. And I believe at the Investor Day, you expressed confidence in continued positive operating leverage. As you look at 2025, can you maybe help us get a sense of the magnitude of that operating leverage that you think is reasonable as you enter 2025 and longer-term, I believe The Street is looking at about 150 basis points to 200 basis points operating leverage next year. Wanted to get your thoughts on that as we look at your return profile in the coming years?

Andy Cecere: Yeah. Thanks, John. This is Andy. So as you saw, we reported positive operating leverage of approximately 30 basis points in Q3 here. The guidance that John provided would indicate that our expectation for positive operating leverage
```

*Rank 4 — `USB_2024_Q4_prepared_remarks_200_008`*

```
more on a year-over-year basis. I'll now provide full-year 2025 guidance. Total revenue growth on an adjusted basis is estimated to be in the range of 3% to 5% compared to the full year 2024. We expect to achieve positive operating leverage excluding the impact of security gains or losses of greater than 200 basis points for the full year. I'll now hand it back over to Andy for closing remarks.

Andy Cecere: Thanks, John. 2024 was a pivotal year for the company in many ways and it marked a very important inflection point in our story. Going into the year, there was much uncertainty with respect to the broader macroeconomic environment, persistent inflation, significant rate volatility, political and regulatory headwinds to name a few, but we effectively managed through the changes and most importantly executed on our strategic objectives. Fourth quarter results showcase our commitment to execution which was highlighted by our delivery of 190 basis points of positive operating
```

*Rank 5 — `BK_2024_Q2_prepared_remarks_200_020`*

```
macroeconomic and interest rate environment, as well as the size of our balance sheet. To wrap up, we enter the second half of the year on the back of solid fee growth, a better than expected NII performance to date, and continued expense discipline, which gives us incremental confidence in our ability to drive positive operating leverage in 2024. With that, Operator, can you please open the line for Q&A?
```

verdict: faithful

failure mode: selective omission — 968bps reported quoted, 288bps excluding notable items dropped from the same sentence

notes: All correct, including BNY named correctly (ch2) and USB's three figures (ch3, ch4). One selective omission: ch2 gives 968bps reported and 288bps excluding notable items, and only the larger figure is quoted. Same drift beyond the asked window as items 3 and 7.

---

## 32. `ref_them_07` / `chunk200_dense_enriched`

- **condition:** chunk200_dense_enriched
- **arm:** enriched
- **question_id:** ref_them_07
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks describe deposit growth in the second quarter of 2023?

**Generated answer, verbatim:**

```
In the second quarter of 2023, Fifth Third Bank reported that total period-end deposits increased by 1% sequentially and 2% year-over-year, outperforming the broader banking industry which saw a 5% decline. This growth was driven by deliberate strategies including expanding distribution in Southeast markets (adding over 70 de novo branches since 2019), launching innovative products like Momentum Banking, and focusing on primary household growth, which resulted in 3% year-over-year net household growth in the consumer segment. Additionally, Fifth Third added a record number of new middle-market commercial relationships, up 30% from 2022.

Bank of America described its deposit results as finding stability, noting that this was a good result given normal tax seasonality and monetary policy actions. The bank highlighted that it maintained over $1 trillion in high-quality consumer deposits, which remained $274 billion above pre-pandemic levels. However, Bank of America noted that the decline in consumer deposits during the quarter was driven by higher debt payments, increased spending, and seasonal tax activity.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `FITB_2023_Q2_prepared_remarks_200_003`*

```
Fifth Third's total period-end deposits increased 1% sequentially and increased 2% year-over-year as compared to a 5% decline for the HA [ph] over the same period. Our commercial banking and commercial banking business segments both generated period-end deposit growth. Given the year-over-year decline in deposit system-wide, it's reasonable to ask how Fifth Third has continued to outperform. The answers are deliberate multiyear strategies to expand distribution in our Southeast markets to launch innovative operational deposit-oriented solutions like momentum banking and our treasury management offerings and our sustained focus on primary household growth. We have added over 70 de novo branches in our Southeast footprint since 2019, more than any other bank except JPMorgan. As a portfolio, these branches are outperforming their original business cases on deposit production with several producing at a rate of 200% to 300% of plan. In consumer, we generated year-over-year net household growth of 3%
```

*Rank 2 — `FITB_2023_Q2_prepared_remarks_200_004`*

```
once again this quarter, continuing a strong multiyear trend and punctuated by 7% year-on-year growth in the Southeast and continued success in our Momentum banking product. In commercial, we have added a record number of new quality middle-market relationships this year, up 30% from 2022. Our embedded payments business, Newline, has also been a strong catalyst for deposit growth. We expect the environment in the back half of the year to remain highly competitive for deposits. While we will continue to protect our house relationships and manage to a strong and stable liquidity profile, we will not match a rational pricing competition in a way that prioritizes headline growth over profitability. Turning to pending regulation. We are taking steps to adapt our balance sheet in anticipation of higher capital and liquidity requirements across the industry. We finished the second quarter with a CET1 ratio of 9.5% having accreted around 90 basis points of capital from retained earnings over the course of the past
```

*Rank 3 — `BAC_2023_Q2_prepared_remarks_200_019`*

```
several elements of our deposits seeming to find stability. Given the normal tax seasonality impacts on deposit balances in Q2 and the monetary policy actions, we believe this is a good result. I want to use the other three charts on the page to illustrate the different trends across the last quarter, and more specifically in each line-of-business. In consumer, looking at the top right chart, you see the difference in the movement through the quarter between the balances of low to no interest checking accounts and the higher-yielding non-checking accounts. Here you can also see the low levels of our more rate-sensitive balances in consumer investments and CD balances. And they're both broken out here. In total, we've got still more than $1 trillion in high quality consumer deposits, which remains $274 billion, above pre-pandemic levels. In the second quarter that decline in consumer deposits was driven by higher debt payments, higher spend and seasonal tax activity.
```

*Rank 4 — `FITB_2023_Q2_prepared_remarks_200_016`*

```
footprint auto and specialty lending channels, combined with portfolio residential mortgages, partially offset by growth from dividend finance. We currently expect to need approximately $4 billion in dividend loans for this year, which is a modest decrease from our previous expectations. We continue to expect to grow deposits in the back half of 2023, assuming stable or even slightly tighter market liquidity conditions Consistent with our track record over the past year of taking market share and maintaining high levels of core operating relationships in both consumer and commercial. Within that, we continue to expect migration from DDA into interest-bearing products throughout the remainder of 2023 with the mix of demand deposits to total core deposits declining from 30% in the second quarter to 27% by year-end as we discussed last month. For the third quarter of 2023, we expect average total loan balances to decline 1% to 2% sequentially with commercial down in the low single digits area and consumer stable to slightly down. We expect average deposits to
```

*Rank 5 — `FITB_2023_Q2_prepared_remarks_200_011`*

```
finance, offset by declines in indirect auto and residential mortgage. Average total deposits were flat compared to the prior quarter as increases in CDs and interest checking balances were offset by a decline in demand deposits. By segment, consumer deposits increased 1% and commercial deposits decreased 1%, while wealth and asset management deposits declined 12%, reflecting the impact of tax payments as well as clients' alternative investment options. June activity reflected continued momentum such that period-end total deposits were up 1% compared to the prior quarter. Notably, we have grown deposits 2% since the end of last June compared to a 5% decline for the top 25 banks as shown in the Fed's H8 data. Moving to credit. As Tim mentioned, credit trends were stable with our key credit metrics remaining below normalized levels. The net charge-off ratio of 29 basis points increased three basis points compared to the prior quarter. The NPA ratio of 54 basis points was up three basis points compared to the prior quarter
```

verdict: faithful

failure mode: none

notes: Both companies right, both in Q2 2023, every figure traces (FITB ch1/ch2, BAC ch3). Directly on-question with no scope drift. Label agrees.

---

## 33. `ref_comp_06` / `chunk500_hybrid`

- **condition:** chunk500_hybrid
- **arm:** text_only
- **question_id:** ref_comp_06
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did Bank of America and Fifth Third each describe their operating leverage and the revenue growth behind it in the first quarter of 2023?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `FITB_2023_Q1_prepared_remarks_500_000`*

```
Chris Doll: Good morning everyone. Welcome to Fifth Third’s First Quarter 2023 Earnings Call. This morning our President and CEO, Tim Spence and CFO, Jamie Leonard will provide an overview of our first quarter results and outlook. Our Treasurer, Bryan Preston has also joined for the Q&A portion of the call. Please review the cautionary statements and our materials which can be found on our earnings release and presentation. These materials contain information regarding to the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third’s performance. These statements speak only as of April 20th 2023 and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris. And good morning, everyone. Thank you for joining us today. The past six weeks have seen a great deal of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide impact of quantitative tightening and normal seasonal pressures. Our key credit metrics remain near historical lows with net charge-offs of 26 basis points coming in at the low end of our guidance range. NPAs NPLs and early stage delinquency ratios remained below normalized levels, and criticized assets decrease modestly during the quarter. Moreover, we accomplished all this while also being recognized by Ethisphere as one of only two U.S. banks on their world's most ethical companies
```

*Rank 2 — `BAC_2023_Q4_prepared_remarks_500_002`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 3 — `FITB_2023_Q4_prepared_remarks_500_002`*

```
profitability. Expense discipline, strong returns, and positive operating leverage remain core areas of focus for Fifth Third. Supported by our technology modernization investments and a focus on leaning out key value streams, we reduced full-time equivalent employee headcount by 4% from our peak in 2023 to the end of the year without the need for a company-wide expense program. The run rate benefits of these efforts put us in a position to sustain the peer-leading annualized expense growth that we have averaged the past several years, even as we continue to invest for growth. While the carryover effect of the RWA diet makes it unfeasible for the full year, we do anticipate returning to positive operating leverage in the second half of 2024. The third point I'd like to highlight is about growth. Our strategies have been consistent, building out our Southeast markets, producing a strong fee to total revenue mix, and leveraging software that differentiates our product offerings and improves productivity. These are multi-year investments that cannot be replicated easily by competitors to one to two years of hiring a few new branches or small tuck-in acquisitions. In 2023, we opened 37 new branches concentrated in the Southeast, bringing us to 107 opened over the past five years. We plan to open another 31 branches in the Southeast in 2024. As a portfolio, these branches have continued to outperform our expectations on both household acquisition and deposit growth and should provide a tailwind for several years forward. We also continue to invest in treasury management, wealth and asset management, and capital markets. All three of these businesses grew for us in 2023. We expect mid-to-high single-digit growth in each in 2024. In treasury management, our acquisitions of Rize and Big Data Healthcare and the launch of Newline, our embedded payments business, should continue to support peer-leading performance. In wealth and asset management, Global Finance recently named our Private Bank as the Best US Regional Private Bank for the fifth consecutive year and Best Private Bank for Entrepreneurs globally for the first time. In our capital markets business, we have seen more robust activity levels to start the year, including an M&A pipeline that is 1.5 times the full-year revenue target embedded in our guidance. Overall, we expect 2024 to be a solid year of improving revenue trends and continued to expense discipline. Given what we believe to be a less certain outlook than the markets would imply,
```

*Rank 4 — `FITB_2023_Q4_prepared_remarks_500_000`*

```
Operator: Hello and welcome to the Q4 2023 Fifth Third Bancorp Earnings Conference Call. All lines have been placed on mute to prevent any background noise. After the speakers' remarks, there will be a question-and-answer session. [Operator Instructions] I'll now turn the conference over to Matt Curoe, Director of Investor Relations. Please go ahead.

Matt Curoe: Good morning, everyone, and welcome to the Fifth Third's Fourth Quarter 2023 Earnings Call. This morning our Chairman, President, and CEO, Tim Spence; and CFO, Bryan Preston will provide an overview of our fourth quarter results and outlook; our Chief Operating Officer, Jamie Leonard and Chief Credit Officer, Greg Schroeck have also joined for the Q&A portion of the call. Please review the cautionary statements in our materials, which can be found in our earnings release and presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of January 19, 2024, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Matt, and good morning everyone. At Fifth Third, we believe that great banks distinguish themselves based on how they navigate challenging and uncertain operating environment. 2023 was certainly a challenging year for the industry, but I am very pleased with how we measured up. A defensive balance sheet positioning, strong execution, and multiyear strategic investments produce top-quartile profitability, the best core deposit growth, and the best total shareholder return among all regional peers who did not participate in an FDIC-assisted transaction. We generated an all-time record full-year revenue of $8.7 billion. Deposits grew 5% compared to an industry-wide decline of 3%. Credit performance was strong with net charge-offs remaining below historical averages. And although it would be foolish to expect it to repeat forever, in commercial real estate we experienced zero net charge-offs in 2023 and only two basis points in delinquent loans as of early January. These strong outcomes combined with our multi-year expense discipline produced a full-year adjusted return on assets of 1.25% and adjusted return on tangible common equity ex-
```

*Rank 5 — `BAC_2023_Q2_prepared_remarks_500_004`*

```
of payments through CashPro App are up 20%. As you can see, every line of business is delivering strong organic growth. Investments made in technology have enabled us to grow industry leading positions in digital tools, while enabling our clients to do great things and making us more efficient. This provides for a very satisfied, stable customer and client base with Bank of America's primary provider. And by doing with a digital application, that also produces operating leverage. On Slide 7, you can see our streak of operating leverage continued in the second quarter of 2023. We're now back in eight quarters in a row. The chart on Slide 7 covers the 8.5 years at 34 quarters, and all but eight of those quarters and you can see those identified. Six of which were in the heart of the pandemic, we've achieved operating leverage. Operating leverage is that simple task of growing revenue at a better growth rate and expense. As I said, Alastair's is going to discuss with you our good and declining expansion trajectory which sets us up to continue to provide operating leverage, even with the shift in economy. In sum, in the quarter, we delivered earnings that are 19% higher and a 15% return on tangible common equity that was driven by continued strong organic growth and operating leverage in a volatile economic environment. Alastair is going to talk to you about a bit more strength we see ahead in our net interest income for the balance of the year and that provides a better start as we think about 2024. You're going hear our expectations for the quarterly decline expenses in the following quarters for the rest of '23, even as we keep investing, and you hear about the resilience of credit and strong trajectory in capital, this all positions us well to continue both our streaks of organic growth and operating leverage. With that, let me turn it over to Alastair.

Alastair Borthwick: Thank you, Brian. And on Slide 8, we list the more detailed highlights of the quarter, and then Slide 9 presents a summary income statement, so I'm going to refer to both of those. For the quarter, we generated $7.4 billion in net income, and that resulted in $0.88 per diluted share. A year-over-year revenue growth of 11% was led by a 14% improvement in net interest income, coupled with a strong 10% increase in sales and trading results ex-
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: Ch1, at rank 1, is FITB_2023_Q1 and contains exactly the Fifth Third half — "nine points of year-over-year positive operating leverage driven by an 18% increase in revenue". Bank of America appears only at Q4 2023 and Q2 2023, never Q1 2023, so the comparison is unmakeable from this context.

---

## 34. `ref_comp_08` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_comp_08
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MTB_2023_Q3_prepared_remarks_200_005`*

```
98 for the third quarter, up 13% from last year’s similar quarter. Now, let’s review our net operating results for the quarter on Slide 9. M&T’s net operating income for the third quarter, which excludes intangible amortization was $702 million and diluted net operating earnings per share, was $4.05. Net operating return on tangible common equity was 17.41% and tangible book value per share increased 3% compared to the end of June. On Slide 10, you will see that diluted GAAP earnings per share, was down 21% from linked quarter. Recall our results from the second quarter of last year indicated an after-tax $157 million gain from the sales of CIT business in April. Excluding this gain, GAAP net income and diluted earnings per share were down 3% compared to the linked quarter. On a GAAP basis, M&T’s third quarter results produced an ROA and
```

*Rank 2 — `MTB_2023_Q1_prepared_remarks_200_002`*

```
charge-offs still below our long-term average. Capital levels remained strong with the CET1 ratio estimated to end the first quarter at 10.15%. During the quarter, we repurchased $600 million in common shares which represented 2% of our outstanding common stock, and the Board approved an 8% or $0.10 per share increase in the quarterly common dividend to $1.30 per share. Tangible common equity per share increased 3% to $88.81 per share. In addition, April 1 marked the one-year anniversary of the closing of the People's United acquisition. We're pleased with the results of the largest acquisition in our company's history. The tangible book value dilution was only 4% and has been earned back already. Merger costs were less than anticipated at the time of announcement. Targeted expense synergies have largely been realized and are now in the run rate. As a result of these, the above, the return
```

*Rank 3 — `FITB_2023_Q3_qa_200_006`*

```
all of you would be very pleased with how much tangible book value accretion, we would report in that environment.

TimothySpence: And Scott, if I just put a point on the last thing, Jamie you said. I mean, we believe investors want us to do what is best for managing the business and for recognizing the fact that options have value but if you believe that the AOCI mark is weighing on the stock, then the other way to look at it is the burn down is 25% accretion in tangible book value per share in the next two years, just given the current outlook on rates, which is a pretty unique buying opportunity, be the other way to look at it.

ScottSiefers: Yes, I agree. All right. That's perfect. So Tim and Jamie, thank you both.

Operator: And your next question comes from the line of Erika Najarian from UBS.

ErikaNajarian: Jamie, this first one is for you
```

*Rank 4 — `MTB_2024_Q4_prepared_remarks_200_004`*

```
to shift our balance sheet toward a more rate neutral position. We manage credit risk meaningfully reducing nonaccrual and commercial criticized balances, and having net charge-offs come in largely in line with our expectations. Best focus on the fundamentals positions M&T for 2025 and beyond, and is reflected in our 2024 results with net operating earnings per share of $14.88. ROTA and ROTCE of 1.3% and 14.54%, and 11% growth in tangible book value per share. Turn to Slide 9, which shows the results for the fourth quarter. Our fourth quarter results reflect the continuation of a strong performance we have through the year. There are several successes to highlight. NII was largely stable compared to the third quarter, even considering a 100 basis points in rate cuts since the start of the easing cycle in September. Average total loans grew for the fifth consecutive quarter demonstrating our ability to more than offset the plan reduction in our CRE concentration.
```

*Rank 5 — `MTB_2024_Q3_prepared_remarks_200_004`*

```
s look at the specifics for the third quarter. Diluted GAAP earnings per share were $4.02 for the third quarter, improved from $3.73 in the second quarter. Net income for the quarter was $721 million compared to $655 million in the linked quarter, an increase of 10%. M&T's third quarter results produced an ROA and ROCE of 1.37% and 10.26% respectively. The CET1 ratio remains strong, growing at 11.54% at the end of the third quarter and tangible book value first year grew 5%. Of note, the third quarter included a discrete tax benefit of $14 million or an $0.08 EPS benefit. Slide 8 includes supplemental reporting of M&T's results on a net operating and tangible basis. M&T's net operating income for the third quarter was $731 million compared with $665 million in the linked quarter. Diluted net operating
```

verdict: over-conservative abstention

failure mode: declines although BOTH sides are present in the asked quarter — the one case here where the conjunction was satisfiable

notes: Unlike items 12 and 36, this condition retrieved both halves for Q3 2023: ch1 (MTB_2023_Q3) has M&T's "tangible book value per share increased 3% compared to the end of June", and ch3 (FITB_2023_Q3_qa) has Fifth Third discussing TBVPS accretion and the AOCI burn-down. The comparison was makeable and was declined anyway. The strongest abstention case in the packet.

---

## 35. `ref_them_08` / `chunk200_dense`

- **condition:** chunk200_dense
- **arm:** text_only
- **question_id:** ref_them_08
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did firms describe momentum in net inflows, AUM and client investment assets during 2023?

**Generated answer, verbatim:**

```
Based on the provided context, firms described momentum in net inflows, AUM, and client investment assets during 2023 as follows:

*   **Morgan Stanley:** In Q1 2023, adviser-led flows originating from workplace relationships reached $28 billion, doubling year-over-year. However, Investment Management revenues declined 3% in Q1 due to lower AUM and cumulative outflows over the prior year, with total AUM ending at $1.4 trillion. For the full year 2023 (reported in Q4 remarks), AUM increased year-over-year to $1.5 trillion supported by higher asset values, but long-term net outflows were approximately $7 billion, driven by headwinds in active equity growth strategies. Client migration from workplace to adviser-led channels was up 25% year-over-year.
*   **BlackRock:** In Q4 2023, the firm reported $28 billion of net inflows into precision exposures. Full-year retail net outflows were $8 billion, primarily due to allocations out of rising rate-sensitive strategies, partially offset by record net inflows of $12 billion in Aperio. The institutional business generated net inflows of $32 billion for the full year 2023, led by active net inflows of $87 billion, while index net outflows were $55 billion due to redemptions from low-fee equity strategies.
*   **State Street (STT):** While specific 2023 quarterly details are limited in the text, Q1 2024 remarks noted that management fees were the highest since Q1 2022, aided by a "strong finish" at year-end 2023. The firm also reported four consecutive quarters of positive net inflows in its cash business leading into early 2024.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MS_2023_Q1_prepared_remarks_200_011`*

```
environment. Importantly, our strategy is working and we are seeing channel migration from workplace to adviser-led. Adviser-led flows, originating from workplace relationships reached $28 billion in this quarter alone, double versus this time last year and this compares to the approximate $50 billion we saw annually over the past 3 years. Furthermore, almost 90% of these flows were from assets held away, also consistent with what we have seen historically. Our strategy remains in place to best serve our clients and support the firm’s path to reach $10 trillion in client assets. Moving to Investment Management, revenues of $1.3 billion declined 3% year-over-year, primarily on lower AUM due to the decline of asset values and the cumulative effect of outflows over the prior year. Total AUM ended at $1.4 trillion. Long-term net outflows were $2.4 billion as equity outflows moderated in the quarter. In fixed income, outflows
```

*Rank 2 — `BLK_2024_Q3_prepared_remarks_200_017`*

```
part of the global economy. In my conversations with clients and policymakers around the world, I hear how more and more countries recognize the power of American capital markets and would like to build their own type of capital markets. Record government deficits and tighter bank lending means people, companies, and countries will increasingly turn to markets to finance their retirements, their business, and their economies. The growth and prosperity generating power of the capital markets will remain a dominant economic trend in the coming decades. And BlackRock will be an important player in that growth. The opportunities ahead are never been better than we've seen now. We see this through unique deals and partnerships with BlackRock at the center and are an accelerating client activity. 2024 net inflows have already surpassed the full year net inflows of both 2022 and 2023. The asset we manage on behalf of our clients reached a new high, ending the third quarter at $11.5 trillion. AUM has grown $2
```

*Rank 3 — `STT_2024_Q1_prepared_remarks_200_007`*

```
ed by higher equity markets, the strategic actions we have taken to position our asset management business for growth, and the benefits of the strong finish in step-off point at year-end 2023. 1Q 2024 management fees of $510 million are the highest since the first quarter of 2022. While GA experienced total aggregate outflows in Q1, this was driven by the impact of a large, but expected single client redemption within the institutional business. We saw continued momentum in the defined contribution business driven by our target day franchise. Encouragingly, we saw cash net inflows of $9 billion in the quarter, the fourth consecutive quarter of positive net inflows of our cash business. ETF AUM reached a record $1.4 trillion at quarter end with GA continuing to gather net inflows and expand market share within U.S. low-cost ETFs. Now let me spend a moment on our continuing productivity efforts. We have a detailed set of initiatives
```

*Rank 4 — `MS_2023_Q4_prepared_remarks_200_023`*

```
billion of workplace assets migrate to the investor led -- the advisor led channel on an annual basis. This year, client migration was up 25% year-over-year despite economic headwinds, and on the product side, our financial advisors are offering clients investment opportunities such as private credit, private equity, and all their other alternatives. Bringing wealth and investment management closer together will create greater opportunities for ongoing product creation. As we move forward and transition from integration to optimization for client experience, we expect to see greater scale benefits from our investments over time. Investment management reported full year results of $5.4 billion and fourth quarter revenues of $1.5 billion. AUM increased year-over-year to $1.5 trillion, supported by higher asset values. Long-term net inflows of approximately $7 billion -- excuse me, long term net outflows of approximately $7 billion were driven by headwinds in our [MSIM] active equity growth strategies.
```

*Rank 5 — `BLK_2023_Q4_prepared_remarks_200_015`*

```
trades and portfolio reallocations. We saw $28 billion of net inflows into precision exposures as institutional clients use these highly liquid instruments to re-risk in the quarter. With Safe-Haven cash providing positive returns. Full year and fourth quarter retail net outflows of $8 billion and $9 billion, respectively, were primarily due to allocations out of rising rate sensitive strategies namely liquid alternatives and flexible bond funds. This was partially offset by strength in Aperio, which saw record net inflows of $12 billion in 2023. Aperio AUM since acquisition has grown 95% to $80 billion. BlackRock's institutional business generated net inflows of $32 billion in 2023, led by active net inflows of $87 billion including the funding of several significant outsourcing mandates throughout the year. Index net outflows of $55 billion were driven by redemptions from our low fee equity strategies as several large clients adjusted their allocations
```

verdict: faithful

failure mode: none

notes: All correct — MS (ch1, ch4), BLK (ch5) — and honest that the STT material is Q1 2024 rather than 2023. No misattribution here, unlike items 5 and 6 on the same question; note that no BNY chunk was retrieved in this one.

---

## 36. `ref_comp_08` / `chunk500_hybrid_enriched`

- **condition:** chunk500_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_comp_08
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MTB_2023_Q3_prepared_remarks_500_002`*

```
98 for the third quarter, up 13% from last year’s similar quarter. Now, let’s review our net operating results for the quarter on Slide 9. M&T’s net operating income for the third quarter, which excludes intangible amortization was $702 million and diluted net operating earnings per share, was $4.05. Net operating return on tangible common equity was 17.41% and tangible book value per share increased 3% compared to the end of June. On Slide 10, you will see that diluted GAAP earnings per share, was down 21% from linked quarter. Recall our results from the second quarter of last year indicated an after-tax $157 million gain from the sales of CIT business in April. Excluding this gain, GAAP net income and diluted earnings per share were down 3% compared to the linked quarter. On a GAAP basis, M&T’s third quarter results produced an ROA and ROE of 1.33% and 10.99% respectively. Next, we will look a little deeper into the underlying trends that generated the third quarter results. Please turn to Slide 11. Taxable equivalent net interest income was $1.79 billion in the third quarter, down $23 million from linked quarter. This decline was driven largely by higher interest rates on consumer deposit funding. An unfavorable funding mix change partially offset by higher interest rates on earning assets and 1 additional day. The net interest margin for the past quarter was 3.79%, down 12 basis points from linked quarter. The primary drivers of the decrease to the margin were an unfavorable deposit mix shift, which reduced margin by 7 basis points; the net impact from higher interest rates on customer deposits, net benefit from higher rates on earning assets which we estimate reduced the margin by 6 basis points. The remaining 1 basis point was due to higher non-accrual interest, net of the impact of 1 additional day. Turning to Slide 12. Average earning assets increased $1.5 billion from the linked quarter, due largely to the strong deposit growth that drove the $3 billion growth at the Fed. Average loans declined $928 million and average investment securities declined $630 million. Turning to Slide 13 to talk about average loans. Total loans and leases averaged $132.6 million for the third quarter of 2023, down 1% compared to the linked quarter. Looking at loans by category, on
```

*Rank 2 — `MTB_2023_Q1_prepared_remarks_500_001`*

```
per share. In addition, April 1 marked the one-year anniversary of the closing of the People's United acquisition. We're pleased with the results of the largest acquisition in our company's history. The tangible book value dilution was only 4% and has been earned back already. Merger costs were less than anticipated at the time of announcement. Targeted expense synergies have largely been realized and are now in the run rate. As a result of these, the above, the return on investment and EPS accretion have exceeded those expected at the time the deal was announced. Let's take a look at the first quarter results. Diluted GAAP earnings per common share were $4.01 for the first quarter of 2023, down 7% compared with $4.29 in the fourth quarter of 2022. Net income for the quarter was $702 million, 8% lower than the $765 million in the linked quarter. On a GAAP basis, M&T's first quarter results produced an annualized rate of return on average assets of 1.4%, and an annualized rate of return on average common equity of 11.74%.  This compares with rates of 1.53% and 12.59%, respectively, in the previous quarter. Included in GAAP results were after-tax expenses from the amortization of intangible assets amounting to $13 million in the first quarter and $14 million in the sequential quarter, representing $0.08 per common share in both quarters. Pretax merger-related expenses of $45 million related to the People's United acquisition were included in the fourth quarter's GAAP results. These merger-related charges translate to $33 million after tax or $0.20 per common share. There were no merger-related expenses in this year's first quarter.  In accordance with the SEC's guidelines, this morning's press release contains a reconciliation of GAAP and non-GAAP results including tangible assets and equity. Consistent with our long-term practice, M&T provides supplemental reporting of its results on a net operating or tangible basis, from which we have only ever excluded the after-tax effect of amortization of intangible assets as well as any gains or expenses associated with mergers and acquisitions. We believe this information provides investors with a better picture of the long-term earnings power of the institution. M&T's net
```

*Rank 3 — `MTB_2024_Q3_prepared_remarks_500_001`*

```
emissions. Turning to Slide 5, our employees and products continue to receive awards from consumer, business, and trade organizations. We're into Slide 7, which shows the results of the third quarter. As noted in this morning's press release, we released our third quarter results as we continue to make progress on the plans we laid out in January. There are several successes to highlight. [Net interest margin and non-interest] (ph) income grew sequentially as we continue to grow loans while reducing our CRE concentration. In fact, since the fourth quarter of 2023, we have grown average loans by nearly $2 billion while reducing CRE by over $4 billion and growing C&I and consumer loans. Funding costs was well managed in this quarter with a 4 basis point decline in the cost of interest bearing liabilities. We restarted our share repurchase program in the third quarter and executed $200 million in share repurchases and grew our CET1 ratio to over 11.5%. Non-interest income reached a high point in the third quarter, if we exclude the prior gains on our two divestitures. This was achieved by even considering the foregone fee income from those two sold businesses, demonstrating the resiliency and strength of our diversified business model. Asset quality continued to improve this quarter with reduction in both non-accrual balances and commercial credit size loans and net charge-offs below the full year outlook. Now let's look at the specifics for the third quarter. Diluted GAAP earnings per share were $4.02 for the third quarter, improved from $3.73 in the second quarter. Net income for the quarter was $721 million compared to $655 million in the linked quarter, an increase of 10%. M&T's third quarter results produced an ROA and ROCE of 1.37% and 10.26% respectively. The CET1 ratio remains strong, growing at 11.54% at the end of the third quarter and tangible book value first year grew 5%. Of note, the third quarter included a discrete tax benefit of $14 million or an $0.08 EPS benefit. Slide 8 includes supplemental reporting of M&T's results on a net operating and tangible basis. M&T's net operating income for the third quarter was $731 million compared with $665 million in the linked quarter. Diluted net operating
```

*Rank 4 — `FITB_2023_Q1_prepared_remarks_500_000`*

```
Chris Doll: Good morning everyone. Welcome to Fifth Third’s First Quarter 2023 Earnings Call. This morning our President and CEO, Tim Spence and CFO, Jamie Leonard will provide an overview of our first quarter results and outlook. Our Treasurer, Bryan Preston has also joined for the Q&A portion of the call. Please review the cautionary statements and our materials which can be found on our earnings release and presentation. These materials contain information regarding to the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third’s performance. These statements speak only as of April 20th 2023 and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris. And good morning, everyone. Thank you for joining us today. The past six weeks have seen a great deal of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide impact of quantitative tightening and normal seasonal pressures. Our key credit metrics remain near historical lows with net charge-offs of 26 basis points coming in at the low end of our guidance range. NPAs NPLs and early stage delinquency ratios remained below normalized levels, and criticized assets decrease modestly during the quarter. Moreover, we accomplished all this while also being recognized by Ethisphere as one of only two U.S. banks on their world's most ethical companies
```

*Rank 5 — `MTB_2023_Q2_prepared_remarks_500_006`*

```
points in the first quarter. This brings our year-to-date net charge-offs to 30 basis points, which is below our long-term average of 33 basis points. As we have noted previously, we expect net charge-offs to be lumpy on a quarter-to-quarter basis. This is the result of a unique nature of each property and borrower. In order to identify emerging issues that could lead to loan grade adjustments, we continue to perform ongoing rate risk, resizing risk, tenant sensitivities on commercial real estate portfolios on a quarterly basis. This work is reflected in our criticized loan portfolio. Loans 90 days past due on which we continue to accrue interest or $380 million at the end of the first quarter compared to $407 million sequentially and total 43% of these loans 90 days past due loans were guaranteed by the government or government related entities. Turning to slide 19 for capital. M&T Cet1 ratio at the end of June was an estimated 10.58% compared to 10.16% at the end of the first quarter. The increase was due in part to higher net income and in repurchasing shares in the second quarter. In June, tangible common shareholder equity totaled $15.2 billion, up 3% from the end of the prior quarter. Tangible book value per share accounted at $91.58, up 3% from the end of the first quarter. In late June, the Federal Reserve released results from the annual bank stress test. While this was an off year for Category IV banks, given the timing of the People's United acquisition, M&T participated in the stress test this year. Our preliminary stress test capital buffer or SCB is estimated to be 4%. Using the SCB, which is in effect from October 1st, 2023 to September 30th of 2024 will be subject to 8.5% CET1 ratio. Now turning to slide 20 for the outlook. As we look forward to the second quarter of this year, we believe we are well positioned to navigate through a challenging economic conditions. However, the rapidly changing interest rate expectations, combined with continued pressure on funding, affect our outlook for the full year 2023. The 2023 outlook reflects the impact of the sale of the M&T insurance agency that closed in October of last year and the sale of the CIT business that closed in April of this year. First, let's talk about net
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: Ch1 (MTB_2023_Q3) holds the M&T half verbatim; Fifth Third appears only at Q1 2023. Same shape as item 12 under a different condition — one side in period, one side not.

---

## 37. `ref_them_02` / `chunk500_dense`

- **condition:** chunk500_dense
- **arm:** text_only
- **question_id:** ref_them_02
- **category:** thematic
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)
- **Check 3 flag:** flagged

**Question:**

> How did banks characterise the uncertainty around the Basel III endgame proposal over 2023 and 2024, and how did it affect their capital actions?

**Generated answer, verbatim:**

```
Based on the provided transcripts, banks characterized the uncertainty surrounding the Basel III Endgame proposal as significant, disconcerting, and lacking in detailed analysis to support the magnitude of proposed capital increases. They described the rules as going "way too far," potentially increasing systemic risk by pushing activity into shadow banking, raising credit costs, and reducing U.S. competitiveness. Specific concerns included a lack of clarity on the timing (with some expecting effects not until 2025 or later) and the quantum of the final rules.

This uncertainty directly affected their capital actions in the following ways:
*   **JPMorgan Chase:** Maintained a modest pace for share buybacks, stating they would continue to reassess the trajectory as circumstances evolved. They noted that while they expected RWA to increase by around 30% ($500 billion), leading to higher capital requirements, they found the proposed increase disconcerting given prior statements about banks being well-capitalized.
*   **Goldman Sachs:** Maintained a wider-than-normal CET1 cushion (90 bps above normal) to signal flexibility and address the lingering uncertainty regarding both the quantum and timing of the proposal's resolution. This buffer was designed to support client returns and shareholder capital while maintaining prudence.
*   **U.S. Bank:** Delayed more aggressive buybacks until there was greater clarity on Basel III and other capital rules, though they planned modest buybacks in the near term. They cited loan growth, final capital rules, and rating agencies as factors influencing their capital distribution decisions, noting that CAT II thresholds were not expected until 2027.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `JPM_2023_Q2_prepared_remarks_500_006`*

```
on capital from the pending finalization of the Basel III rules. Nonetheless, despite the likely headwinds ahead, we remain optimistic about the Company's ability to continue delivering excellent performance through a range of scenarios. With that, operator, please open the line for Q&A.
```

*Rank 2 — `GS_2023_Q3_prepared_remarks_500_002`*

```
data has come in above estimates, driving market expectations of higher for longer interest rates. And there still are a number of sectors in the economy that have yet to absorb the impact of higher rates, especially in light of the further tightening in financial conditions we've seen over the last quarter. At the same time, there has been an escalation of geopolitical stresses around the globe, the [indiscernible] war in Ukraine, tensions with China and now the conflict in the Middle East. Overall levels of risk are more elevated than we've seen in quite some time. While we don't know where this will all lead, it could impact economic growth and stability in the U.S. and around the world, and we remain cautiously positioned. Before I turn it over to Denis, I'd like to spend a moment on Basel III Endgame proposal and reiterate my views on it. We, of course, support sensible regulation and the desire to ensure we have a safe and sound financial system. There are some who have recently said we need to address the lessons from the 2008 financial crisis, which is driving the needs of much higher regulations. But frankly speaking, the rules, as proposed, go way too far and do not account for the vast array of improvements made by the largest banks as a result of Dodd-Frank and other reforms. Not only have banks doubled capital over the last 15 years, have improved the quality of capital, increased liquidity, simplified businesses that have been subjected to ongoing annual stress tests. Requiring too much capital will have negative consequences. I believe if these rules are implemented, three things will happen. First, the cost of credit will go up for businesses of all sizes from large corporations to small businesses. Second, more activity will move to the unregulated shadow banking sector. Policies that incentivize a transfer of risk outside the regulated banking system could, in fact, increase systemic risk. And third, US competitiveness will go down. Our capital markets are the deepest and the most liquid in the world. They're the engine of our economy as access to capital allows for innovation and growth across the country. Our competitive standing as the leading global economy would be negatively impacted by this proposal. The net result of these proposed rules would be slower economic growth in the US, material improvement in the -- soundness of the banking system. We, alongside clients and others in the industry, have been engaging heavily
```

*Rank 3 — `JPM_2023_Q3_prepared_remarks_500_001`*

```
Expenses of $20.9 billion were up $1.7 billion or 9% year-on-year, primarily driven by ongoing growth and front office and technology staffing, as well as wage inflation and higher legal expense. And credit costs were $1.4 billion, predominantly driven by net charge-offs in Card, and included a $102 million net reserve release, driven by changes in the central scenario, primarily offset by card loan growth. On to balance sheet and capital on Page 3. We ended the quarter with a CET1 ratio of 14.3%, up about 50 basis points versus the prior quarter as the benefit of net income less capital distributions was partially offset by AOCI. We had $2 billion of net share repurchases this quarter and the pace of buybacks will likely remain modest in light of the Basel III endgame proposal. In line with our capital hierarchy, we will continue to reassess the buyback trajectory as circumstances evolve or opportunities emerge. And on the topic of the Basel III endgame, you'll see that we added a couple of pages on it. So, let's cover that now, starting on Page 4. Given the significance of this proposal for us, the broader industry as well as households and businesses as end-users, we thought it was important to spend time discussing it. And while we know there is interest in having us quantify the expected impact of this proposal in a lot of granular detail, it's important to start by asking why the proposed increase is so large given the repeated statement over time by policymakers that banks are well-capitalized and well-positioned to deal with stress. Given that context, the absence of detailed analysis supporting a capital increase of this magnitude is disconcerting and there's a lot that does not make sense to us. Starting with RWA, we've already said we expect the firm's RWA to increase by around 30% or $500 billion, which results in capital requirements increasing by about 25% or $50 billion. One immediate thing to point out is that at 4.5% GSIB, a $500 billion increase in RWA requires $22.5 billion of additional capital with no change in our systemic risk footprint. We've been on the record for a long time that GSIB was conceptually flawed and miscalibrated originally. Since implementation, the failure to address economic growth despite the Fed themselves acknowledging this
```

*Rank 4 — `GS_2024_Q2_qa_500_008`*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution. It sounds from some of Powell's latest comments that, that may not be something that comes into effect until perhaps into 2025, but we are sort of maintaining a level of cushion that think is appropriate in light of what we know and we don't know about the future opportunity set for Goldman Sachs, but that buffer is designed to support clients return capital shareholders, while maintaining a prudent buffer with some of the lingering uncertainty with respect to future regulatory input.

Steven Chubak: Helpful color. Thanks for taking my questions.

Dennis Coleman: Thank you.

Operator: We'll go next to Devin Ryan with Citizens JMP.

Devin Ryan: All right, great. Good morning, David and Dennis. A couple questions on AWM progress. So the first one is on the alts business specifically, and you're tracking obviously well ahead of the fundraising targets relative to when you set the $1 billion medium term target for annual incentive fees? And now with over $500 billion in alts AUM and obviously growing, that would seem pretty conservative. So I appreciate there's a lot of work to do to generate the returns ahead here, but how should we think about the underlying assumptions for incentive fees in a more normal harvesting environment, just given the mixed shift and the growth that you're seeing in AUM there?

Dennis Coleman: So Devin, I think it's a good question, and I think we share your expectation that, that's going
```

*Rank 5 — `USB_2024_Q3_qa_500_006`*

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

verdict: faithful

failure mode: none — GS and JPM language merged into one "banks characterized" opening, acceptable for a thematic question

notes: All correct and well attributed (JPM ch3, GS ch2/ch4, USB ch5), covering both characterisation and capital actions. The opening paragraph merges GS's and JPM's language into a single "banks characterized..." — acceptable for a thematic question, though "way too far" is Solomon's alone.

---

## 38. `ref_unans_01` / `chunk200_bm25`

- **condition:** chunk200_bm25
- **arm:** text_only
- **question_id:** ref_unans_01
- **category:** unanswerable
- **case:** A
- **outcome label:** answered_ungrounded
- **coverage@5:** n/a (unanswerable; excluded from retrieval metrics)

**Question:**

> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Generated answer, verbatim:**

```
Based on the provided context, there are two different reporting periods for Northern Trust (BK):

1.  In Q3 2023, ETFs Assets Under Custody/Administration were up over 20% year-over-year. The total assets under custody/administration and related investment services fees grew in the mid-single digit percentage range.
2.  In Q1 2024, firm-wide assets under custody and administration were $48.8 trillion, which was up 5% year-over-year.

(Note: The context also mentions Q1 2023 figures of $46.6 trillion, up 2% year-over-year, but the most recent specific figure provided is for Q1 2024.)
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BK_2023_Q3_prepared_remarks_200_018`*

```
as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and
```

*Rank 2 — `STT_2023_Q1_qa_200_047`*

```
they were Alpha mandates. So there is three, four or five kind of, I'll call it, revenue installations, right, for each of the balances that sit there when we describe them as assets under custody and administration. I think roughly, our view is that we'd expect about half of the backlog in custody and administration to come through during the course of this year. I'll say that roughly, right? It tends to vary. And then the revenue pieces, it won't be quite at that level because the revenues come through over time as you get the different, I'll call it, layers of services that are provided associated with those -- that assets under custody, administration. But what we'll do is we'll -- I think it's -- that may be some kind of broad perspective. What we'll try to do each quarter is give you more and more visibility as we get to those implementation points because, remember,
```

*Rank 3 — `BK_2023_Q1_prepared_remarks_200_012`*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 — `STT_2023_Q1_qa_200_046`*

```
said you should see a pickup in 2Q. Ron and Eric, what's your expectation for how much of that do you expect would get installed over the course of this year, 2Q, 3Q, 4Q? And by the time we exit this year, how much should be done? And therefore, what benefit should there be to [indiscernible] from that?

Eric Aboaf: Yeah. I think, Vivek, there are a couple of ways to think about that because what happens here is that it gets onboarded on -- in tranches. So we might onboard the assets under custody, administration, but there are multiple services that we're often providing for those assets. So we had a couple of wins over the last year or two years with $1 trillion. Those $1 trillion wins would have had some custody, some accounting, they might have had some performance analytics. They would have had some middle office services in many cases because
```

*Rank 5 — `BK_2024_Q1_prepared_remarks_200_010`*

```
the transformation of our company is a multi-year endeavor but we've started 2024, the year of our 240th anniversary, with a sense of excitement and determination around what's possible. Now over to you, Dermot.

Dermot McDonogh: Thank you, Robin, and good morning everyone. Referring to Page 3 of the presentation, I'll start with our consolidated financial results for the quarter. Total revenue of $4.5 billion was up 3% year-over-year. Fee revenue was up 5%. This reflects 8% growth in investment services fees on the back of higher market values, increased client activity and net new business, partially offset by a 14% decline in foreign exchange revenue, as a result of lower market volatility. Firm-wide assets under custody and our administration of $48.8 trillion were up 5% year-over-year, and assets under management of $2 trillion were up 6% year-over-year
```

verdict: should have abstained

failure mode: company substitution, mechanism stated outright: "Northern Trust (BK)"

notes: Same fabrication as items 11, 26 and 27, and here the mechanism is stated outright: "there are two different reporting periods for Northern Trust (BK)". It is mapping the BK ticker onto the name in the question. Everything after that is BNY's real data.

---

## 39. `ref_unans_01` / `chunk200_dense`

- **condition:** chunk200_dense
- **arm:** text_only
- **question_id:** ref_unans_01
- **category:** unanswerable
- **case:** A
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** n/a (unanswerable; excluded from retrieval metrics)

**Question:**

> What were Northern Trust's assets under custody and administration, and how did they change year-over-year?

**Generated answer, verbatim:**

```
Northern Trust’s firm-wide assets under custody and/or administration were $46.6 trillion, which increased by 2% year-over-year.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BK_2023_Q3_qa_200_044`*

```
underneath the hood that is nuanced, that is different by different segments. Like if you think about asset servicing, our issuer services as a segment made up of three businesses, asset servicing, depository receipts, and corporate trust. Corporate trust as a business tends to attract a higher level of NIBs due to the nature of that business. Q3 would have been a seasonally quieter period for that business. Debt issuance activity was more muted. So that would explain a little bit of that. And asset servicing, let's just say how clients are behaving with us at the moment in the ecosystem, but I wouldn't really call anything out that is kind of noticeably different. And we kind of think about our deposits as one platform, kind of centrally managed under one roof, and that's how we kind of manage it.

Brian Bedell: Okay, great. And then just maybe just to follow up on the, actually in the other investment and other revenue
```

*Rank 2 — `MS_2023_Q3_qa_200_008`*

```
. You're right, you know, from a -- if you think about the self-directed client versus a advisory-based client that we've had in the historical wealth management franchise, one has proven to be somewhat of a stickier deposit base than you would see on the wealth management side. And I think that, you know, on the -- what I would say is the traditional wealth management side that we had historically had. So that does provide you with a sense of what's going on in terms of which client base is seeing that. On the potential growth of NII going forward, again, that's part of the same asset gathering strategy. Some proportion of these assets as they come over, be that into the self-directed or the advice-based relationship, will be held in some sort of transactional cash. So that will be supportive over time of NII to some degree from a deposit perspective. But that also provides us with lending capabilities and opportunities
```

*Rank 3 — `BK_2023_Q1_prepared_remarks_200_012`*

```
waivers and the absence of a notable item last year related to Russia. Firm-wide assets under custody and/or administration of $46.6 trillion increased by 2% year-over-year. Growth from new and existing clients more than offset the stiff headwinds from lower market values and currency translation, a real testament to the strength and diversification of our franchise. Quarter-over-quarter, assets under custody and/or administration increased by 5%. Assets under management of $1.9 trillion decreased by 16% year-over-year. Here, the impact of lower market values and the stronger dollar was tempered by cumulative net inflows over the 12 months. Quarter-over-quarter, assets under management increased by 4%. Investment and other revenue was $79 million, and included another strong quarter of fixed income trading on the back of elevated volatility and greater demand for U.S. treasuries. And net interest revenue increased by 62% year-
```

*Rank 4 — `BK_2023_Q3_prepared_remarks_200_018`*

```
as the stability, breadth, and depth of our solutions remain clear differentiators that position us well with clients, confronted with a persistently challenging market environment and an evolving competitive landscape. For example, ETFs, Assets Under Custody/Administration, were up over 20% year-over-year and the number of funds serviced on our platform continued to grow at a healthy clip. In all, assets under custody/administration and related investment services fees, both grew in the mid-single digit percentage range despite the number of fund launches having slowed significantly over the past year. With Issuer Services, investment services fees were down 2%. Growth from net new business and corporate trust was more than offset by the absence of fees from elevated depository receipt cancellation activity in the third quarter of last year. Next, Market and Wealth Services on Page 8. Market and Wealth Services reported total revenue of $1.4 billion, up 6% year-over-year. Fee revenue was up 5%, and
```

*Rank 5 — `MS_2024_Q4_prepared_remarks_200_019`*

```
the quarterly margin by approximately 140 basis points. Asset management revenues in the quarter set a new record of $4.4 billion, showcasing the progress we have made to durable fee-based revenues. With each quarter this year, asset management revenues saw sequential improvement, powered by constructive markets and consistently strong fee-based flows. Fourth quarter fee-based flows were $35 billion. Importantly, over the last two years, we have seen an increase in the number and the pace of assets migrating from advisor-led brokerage accounts to fee-based accounts. We remain an industry leader in organic growth. Net new assets for the quarter were $57 billion. Full year NNA of $252 billion represents approximately 5% annual growth of beginning period assets. This year, our advisor-led channel drove the results, benefiting from both existing clients and new clients coming to the firm. Transactional revenues for the quarter were $1 billion. Excluding the impact of DCP, transactional revenues represent the highest level
```

verdict: should have abstained

failure mode: company substitution — BNY Mellon's AUCA reported as Northern Trust's; scored offtarget where the identical failure scored ungrounded

notes: Same substitution as items 11, 26, 27 and 38: BNY's $46.6tn/+2% (ch3) presented as Northern Trust's. The label differs only because no bare year went unmatched here — nothing about the answer differs in kind. Four instances of one failure carry two different outcome labels for a reason unrelated to the failure, which is the clearest evidence in the packet that the outcome label is not tracking company identity at all.

---

## 40. `ref_comp_01` / `chunk200_dense_enriched`

- **condition:** chunk200_dense_enriched
- **arm:** enriched
- **question_id:** ref_comp_01
- **category:** comparative
- **case:** C
- **outcome label:** answered_ungrounded
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did Goldman Sachs and Citi differ in how they characterised Basel III endgame uncertainty in late 2023 and early 2024?

**Generated answer, verbatim:**

```
Based on the provided context, Goldman Sachs characterized the Basel III Endgame as "fluid" and noted that if implemented as proposed, it would have varying effects across different businesses, with certain activities meaningfully impacting end users. In contrast, Citi described the situation by stating that the proposal had not yet been finalized or put into place, emphasizing that they were waiting to see how it evolved alongside the CCAR process before making further capital decisions.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `GS_2023_Q3_qa_200_011`*

```
.

Operator: We'll move to our next question from Christian Bolu with Autonomous Research. Please go ahead.

Christian Bolu: Good morning. Just another one on Basel III Endgame. I appreciate that you think it's going to change and all that. But now that you've had a chance to digest the actual proposal as is, any more color on how you think it affects the competitiveness of your markets businesses? Are there any particular businesses that are more or less impacted? And then maybe give us some color on potential mitigation actions.

David Solomon: Sure, Christian. I appreciate it. I mean, I'm going to talk very high level because, again, this is all fluid. But obviously, if these rules went in place the way they're proposed, they would have an effect of the businesses. But it's different from business to business. There are certain activities that would meaningfully impact end users, whether they're corporates or
```

*Rank 2 — `GS_2024_Q2_qa_200_020`*

```
asked about the SEB. Really just wanted to better understand, Dennis, since you noted that you're running with 90 bps of cushion, which is actually above normal. Just how you're handicapping the additional uncertainty related to Basel III endgame. There's certainly been some favorable momentum per the press reports and even some public comments from regulators? But just want to better understand, given the uncertainty around both the SEB and Basel III endgame, where you're comfortable running on a CET1 basis over the near to medium term?

Dennis Coleman: Sure, thanks and I appreciate that question. I think obviously there's been a lot of changes, there's been some changes and expectations. And I think in highlighting that we are operating at the wider end of our range, it is to signal flexibility. And certainly embedded in that is to address some of the uncertainty which does remain with respect to Basel III endgame, both the quantum and timing of its resolution
```

*Rank 3 — `GS_2023_Q3_prepared_remarks_200_005`*

```
data has come in above estimates, driving market expectations of higher for longer interest rates. And there still are a number of sectors in the economy that have yet to absorb the impact of higher rates, especially in light of the further tightening in financial conditions we've seen over the last quarter. At the same time, there has been an escalation of geopolitical stresses around the globe, the [indiscernible] war in Ukraine, tensions with China and now the conflict in the Middle East. Overall levels of risk are more elevated than we've seen in quite some time. While we don't know where this will all lead, it could impact economic growth and stability in the U.S. and around the world, and we remain cautiously positioned. Before I turn it over to Denis, I'd like to spend a moment on Basel III Endgame proposal and reiterate my views on it. We, of course, support sensible regulation and the desire to ensure
```

*Rank 4 — `C_2024_Q1_qa_200_021`*

```
how the Basel III endgame proposal could evolve, but that hasn't happened yet. It's not finalized. It's not in place yet. And so we want to see how that continues to play out. We're obviously in the midst of a CCAR process. We want to see how that evolves. And we'll continue to take the buyback decision on a quarter-by-quarter basis, but we recognize that there's an opportunity there and we'll get after it just as soon as it makes good sense for us.

Operator: Our next question is from Erika Najarian at UBS. Please unmute your line and ask your question.

Erika Najarian: Hi. Good afternoon. Hey. So, you know, clearly the theme of this -- that's emerging on the Q&A is, you know, a healthy skepticism about the revenue targets in-line with the, in light of the expense declines, which you
```

*Rank 5 — `C_2023_Q2_prepared_remarks_200_008`*

```
that we will start to bend the curve on an absolute basis by the end of 2024 and continue to bring down expenses over the medium term. Let me end with capital. Well, you won't be shocked to hear that we were disappointed with the increase to our stress capital buffer. We have engaged in active dialogue with the Fed to better understand the differences between our model and theirs in terms of noninterest revenue. And the industry awaits further clarity on capital requirements and importantly, their implementation timing from the holistic review the regulators have undertaken and the expected Basel III Endgame NPR. There is still uncertainty as to what the final rules will be, and we, like the rest of the industry, will need to work through the implications. The exit of 14 international consumer markets, coupled with the results of our transformation investments and change in business mix will help reduce our capital ratios. In addition, we have other levers to pull over time, such as capital allocation, DTA utilization
```

verdict: faithful

failure mode: none — no numeric claims, and the n-gram fallback cannot see a faithful paraphrase

notes: Both companies right, both quotes accurate and in window (GS ch1 "fluid" / "meaningfully impact end users"; Citi ch4 "not finalized. It's not in place yet" / CCAR). Checked: the answer contains zero numeric claims, so grounding falls to _shared_ngram_chunk_ids, which returns an EMPTY set — the answer paraphrases around short quotations and shares no 6-word verbatim run with any chunk. The label is what the rule specifies; the rule requires copying, and this answer reads rather than copies.

---

## 41. `ref_them_08` / `chunk500_dense_enriched`

- **condition:** chunk500_dense_enriched
- **arm:** enriched
- **question_id:** ref_them_08
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did firms describe momentum in net inflows, AUM and client investment assets during 2023?

**Generated answer, verbatim:**

```
Based on the provided context, firms described momentum in net inflows, AUM, and client investment assets during 2023 as follows:

**Morgan Stanley (MS)**
*   **Net Inflows/Flows:** The firm reported fee-based flows of $22.5 billion in Q3 alone. While Investment Management experienced long-term net outflows of approximately $7 billion in both Q3 and Q4 due to headwinds in active equity growth strategies, year-to-date long-term flows across the franchise were slightly positive as of Q3. In Q1, fee-based flows were strong at $22 billion, though long-term net outflows were $2.4 billion.
*   **AUM:** Total AUM ended at $1.4 trillion in both Q1 and Q3. By Q4, AUM increased year-over-year to $1.5 trillion, supported by higher asset values.
*   **Client Investment Assets/Relationships:** The firm grew client relationships by over 600,000 across the franchise during the year, led by success in the workplace channel. Client migration from workplace to advisor-led channels was up 25% year-over-year. Total deposits remained stable at $340 billion in Q3, though the mix shifted toward higher-yielding cash alternatives.

**BlackRock (BLK)**
*   **Net Inflows:** The institutional business generated net inflows of $32 billion in 2023, led by active net inflows of $87 billion. However, index strategies saw net outflows of $55 billion. Retail clients experienced net outflows of $8 billion for the full year and $9 billion in Q4, primarily due to allocations out of rising rate-sensitive strategies. The cash management platform saw significant growth with $79 billion in net inflows for 2023 and $33 billion in Q4 alone. Private markets (illiquid strategies) attracted $14 billion in net inflows during the year.
*   **AUM:** Year-end AUM for the cash and liquidity business was up 14% year-on-year, adding over $90 billion. Aperio’s AUM grew 95% since acquisition to reach $80 billion. The planned acquisition of GIP is expected to create a pro forma infrastructure platform with client assets of $150 billion.
*   **Client Investment Assets:** Demand for private markets remained strong, driven by infrastructure and private credit. Institutional clients used precision exposures to re-risk, resulting in $28 billion of net inflows into these instruments in Q4.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MS_2023_Q3_prepared_remarks_500_004`*

```
. The multi-year buildup of assets provide a foundational pipeline into our advisor led channel, evidence by fee-based flows of $22.5 billion in the third quarter alone. Asset management revenues of $3.6 billion increased 7% year-over-year. Higher average assets and the impact of cumulative positive fee-based flows over the past year drove the increase. Transactional revenues excluding DCP were $820 million, up 7% year-over-year. Results reflect opportunistic deployment of new capital by retail clients into alternatives, particularly into private equity and private credit. Bank lending balances roughly flat versus the prior quarter. Growth in mortgages and tailored lending offset paydowns and securities-based lending. Total deposits of $340 billion remain stable, compared to the prior quarter. Still, the deposit mix has shifted as clients continue to allocate rate-sensitive cash to higher-yielding cash alternatives available on the platform, including our expanded savings offering. In addition, the quarter saw consistent positive monthly inflows into equity markets from sweep balances, ongoing evidence of the improvement of the retail client sentiment. Net interest income was $2 billion. The sequential decline reflects a continued shift in the deposit mix. Looking towards the rest of this year, based on where we exited the quarter, we expect NII to trend lower. The magnitude will be a function of our deposit mix and the trajectory of rates. The wealth management business model is focused on steady asset aggregation, delivering strong solutions and advice to clients, while growing durable fees and expanding margin through the cycle. We are continuing to invest in our industry-leading position and the sustainability of our long-term growth. As the backdrop recovers, advisors remain well-positioned to capture greater asset opportunity supported by our multi-channel model that was built to attract new client relationships. Turning to investment management, revenues of $1.3 billion increased 14%, compared to the prior year, supported by higher asset management revenues. Total AUM ended at $1.4 trillion. Long-term net outflows of approximately $7 billion were driven predominantly by headwinds to our [Technical Difficulty] active equity growth strategies, which continue to see redemption consistent with the industry. Including the segment's outflows, year-to-date long-term flows across the franchise were slightly positive. Within alternatives and solutions, we continue to see demand for parametric customized portfolios across both equity and fixed
```

*Rank 2 — `MS_2023_Q4_prepared_remarks_500_009`*

```
our channels. Second -- migrate assets to advice. Third -- deepen existing client relationships with enhanced capabilities including new products and solutions, and finally, realize scale benefits of our investments over time. These efforts are well underway. In the year, we grew client relationships by over 600,000 across the franchise. This was led by success in the workplace channel, as we continue to win corporate plans and add participants in stock plan. In the prior three years, we saw an average of $50 billion of workplace assets migrate to the investor led -- the advisor led channel on an annual basis. This year, client migration was up 25% year-over-year despite economic headwinds, and on the product side, our financial advisors are offering clients investment opportunities such as private credit, private equity, and all their other alternatives. Bringing wealth and investment management closer together will create greater opportunities for ongoing product creation. As we move forward and transition from integration to optimization for client experience, we expect to see greater scale benefits from our investments over time. Investment management reported full year results of $5.4 billion and fourth quarter revenues of $1.5 billion. AUM increased year-over-year to $1.5 trillion, supported by higher asset values. Long-term net inflows of approximately $7 billion -- excuse me, long term net outflows of approximately $7 billion were driven by headwinds in our [MSIM] active equity growth strategies. Within alternatives and solutions, we continue to see demand for parametric customized portfolios across both equity and fixed income strategies as more retail clients seek customized solutions. Liquidity overlay services had outflows of $6.6 billion. Weaker institutional liquidity flows were partially offset by demand for parametric's overlay product and the combined parametric brand, inclusive of overlay and its retail offering had net inflows of over $5 billion again this quarter, underscoring the strength of our differentiated customized offering. Fourth quarter asset management and related fees of $1.4 billion increased slightly versus last year. Quarterly performance based income and other revenues were $61 million. Gains in U.S. private equity and infrastructure offset losses in real estate, reflecting the benefits of diversification in the franchise. Turning to the balance sheet, total spot assets were $1.2 trillion. Standardized RWAs increased by $13 billion sequentially to $457 billion, as we actively supported clients.
```

*Rank 3 — `BLK_2023_Q4_prepared_remarks_500_006`*

```
trades and portfolio reallocations. We saw $28 billion of net inflows into precision exposures as institutional clients use these highly liquid instruments to re-risk in the quarter. With Safe-Haven cash providing positive returns. Full year and fourth quarter retail net outflows of $8 billion and $9 billion, respectively, were primarily due to allocations out of rising rate sensitive strategies namely liquid alternatives and flexible bond funds. This was partially offset by strength in Aperio, which saw record net inflows of $12 billion in 2023. Aperio AUM since acquisition has grown 95% to $80 billion. BlackRock's institutional business generated net inflows of $32 billion in 2023, led by active net inflows of $87 billion including the funding of several significant outsourcing mandates throughout the year. Index net outflows of $55 billion were driven by redemptions from our low fee equity strategies as several large clients adjusted their allocations or redeemed for cash needs. Finally, BlackRock's cash management platform saw $33 billion of net inflows in the fourth quarter and $79 billion of net inflows in 2023. We're pleased with the continued strong growth in our cash and liquidity business with year-end AUM up 14% or over $90 billion year-on-year. We're leveraging our scale and integrated cash offerings to engage with clients who are using these products not only to manage liquidity, but also to earn attractive returns. Demand for private markets remain strong, with $14 billion of net inflows into BlackRock illiquid strategies during the year driven by infrastructure and private credit. We continue to expect these categories to be our primary growth drivers in the coming years. Turning to our planned acquisition of GIP this is an exciting day for us, our new partners, our clients and our shareholders. The combination will mark a transformational change in our private market scale and growth. GIP is the world's leading independent infrastructure manager with current client AUM of over $100 billion and fee-based AUM of over $60 billion. The acquisition will create a highly complementary pro forma $150 billion infrastructure platform post-closing tripling BlackRock's infrastructure client assets. The integration will nearly double our private markets management fees to over $1.5 billion and add over $400 million in post-tax annual FRE with FRE margins
```

*Rank 4 — `MS_2023_Q1_prepared_remarks_500_004`*

```
18%. Over time, we believe clients will reinvest these balances across more assets when the market outlook improves. In the interim, given our broad product offerings, clients are choosing to invest in cash with Morgan Stanley through the cycle, positioning us to provide them with more reinvestment choices down the road. Net interest income was $2.2 billion, up 40% year-over-year. Results reflect the impact of higher interest rates and lower sweep balances. Fee-based flows of $22 billion were strong. Asset management revenues were $3.4 billion, down 7% versus last year, reflecting lower market levels. Transactional revenues were $921 million. Excluding the impact of DCP, revenues were down 12% versus last year due to fewer new issuance opportunities and reduced activity levels compared to the beginning of 2022. Lending balances declined this quarter to $144 billion, led by pay-downs in securities-based lending, reflecting the higher interest rate environment. Importantly, our strategy is working and we are seeing channel migration from workplace to adviser-led. Adviser-led flows, originating from workplace relationships reached $28 billion in this quarter alone, double versus this time last year and this compares to the approximate $50 billion we saw annually over the past 3 years. Furthermore, almost 90% of these flows were from assets held away, also consistent with what we have seen historically. Our strategy remains in place to best serve our clients and support the firm’s path to reach $10 trillion in client assets. Moving to Investment Management, revenues of $1.3 billion declined 3% year-over-year, primarily on lower AUM due to the decline of asset values and the cumulative effect of outflows over the prior year. Total AUM ended at $1.4 trillion. Long-term net outflows were $2.4 billion as equity outflows moderated in the quarter. In fixed income, outflows in floating rate loans were partially offset by high yield and emerging markets. Finally, alternatives and solutions delivered strength, driven mostly by demand for Parametric’s fixed income customized portfolios as well as inflows into private credit. Liquidity and overlay services had inflows of $13.9 billion. Positive liquidity inflows of $37 billion were partially offset by outflows related to a single client relationship. Asset management and related fees decreased versus the prior year to $1
```

*Rank 5 — `MS_2023_Q3_qa_500_000`*

```
Operator: We are now ready to take any questions. [Operator Instructions] We'll go first to Christian Bolu with Autonomous Research.

Christian Bolu: Good morning, James and Sharon. I wanted to just touch on wealth management, a bit of a longer-term question here. As you mentioned, you've enjoyed really strong organic growth in that segment over the last few years. But it doesn't appear to be translating to revenue growth. If I look at the wealth management revenues excluding NII, it hasn't really grown in three years, despite gathering significant amount of assets? So curious how you're thinking about the flow through from AUM or asset growth to revenues? And then maybe more broadly how you're thinking about the unit economics of your asset gathering strategy?

Sharon Yeshaya: Sure, actually I think that interestingly enough Christian I'm pretty impressed with the resiliency that we've seen in the business. This is literally the explanation of the funnel that we've talked about. If you look back over the course of the last year alone $260 billion or $235 billion of assets that we've captured. Then look at the fee-based flows, right? We continue to see increased fee-based flows. This past year, if you exclude the asset acquisitions that we had over the last couple of years, we are basically at some of the historical highs of seeing fee-based growth as we move forward. You're looking at times since COVID, where we obviously had very high retail engagement, and you've been able to offset, even with a decline in NII, offset those growths to asset-based, asset management revenues as you move forward. It's that, that we are trying to grow. We're trying to continue to grow our asset management fees over time and make sure that we have the right solutions in place to offer our clients. Now let's take that forward. We have this mixed environment. You have 23% of our retail client assets sitting in cash, that is 5% higher, right, from the 18% on historical averages. We've begun to see retail investors put their cash into markets. The last four months -- in consecutively, we've seen that movement into the market. This quarter alone, we began to see alternative growth in the new products, the growth in transactional revenues. We haven't seen that since the first
```

verdict: faithful

failure mode: none

notes: Every figure across both companies traces, with periods and quarters correct (MS ch1/ch2/ch4, BLK ch3). The most complete synthesis in the packet. Again no BNY chunk retrieved and no misattribution — the same pattern as item 35, against items 5 and 6.

---

## 42. `ref_comp_12` / `chunk500_dense_enriched`

- **condition:** chunk500_dense_enriched
- **arm:** enriched
- **question_id:** ref_comp_12
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did PNC's and Capital One's net interest margins compare in 2024?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `PNC_2024_Q1_prepared_remarks_500_002`*

```
likelihood of potentially substantial changes to the Basel III endgame NPR under the currently proposed capital rules, our estimated fully phased in expanded risk-based CET1 ratio would be approximately 8.3% as of March 31, 2024. We continue to be well positioned with capital flexibility. Share repurchases approximated $135 million or roughly 1 million shares. And when combined with $624 million of common dividends, we returned $759 million of capital to shareholders during the quarter. Slide 5 shows our loans in more detail. Compared to the fourth quarter, average loan balances decreased 1%, primarily driven by lower commercial loan balances. Commercial loans were $219 billion, a decrease of $3.4 billion, driven by lower utilization as well as soft loan demand. Within the corporate and institutional bank, utilization rates have remained below 2023 year-end levels and have not increased in the first quarter as is historically typical. We expect utilization to increase throughout the year. Notably, each percent of utilization within CNIB equates to $4 billion of loan growth. Consumer loans declined approximately $600 million, driven by lower credit card and home equity balances, and total loan yields increased 7 basis points to 6.01% in the first quarter. Slide 6 details our investment, security and swap portfolios. Average investment securities of $135 billion decreased 1% as curtailed purchase activity was more than offset by portfolio paydowns and maturities. The securities portfolio yield increased 3 basis points to 2.62%, reflecting the run-off of lower yielding securities. As of March 31, the securities portfolio duration was four years. Our receive fixed swaps pointed to the commercial loan book totaled $37 billion on March 31. The weighted average receive fixed rate of our swap portfolio increased 20 basis points to 2.3% and the duration of the portfolio was two years. Through the end of 2024, 13% of our securities and swap portfolio is scheduled to mature, which will allow us to reinvest into higher yielding assets, providing a meaningful benefit to net interest income in the second half of the year. Accumulated other comprehensive income was negative $8 billion at March 31, which will accrete back as our securities and swaps mature, resulting in continued tangible book value growth. Slide 7 covers our deposits in more detail. Average deposits decreased $4 billion to $420 billion during the quarter, as growth in consumer deposits was more than offset by a seasonal
```

*Rank 2 — `PNC_2024_Q1_prepared_remarks_500_004`*

```
205 million or 6%. Provision was $155 million in the first quarter, reflecting portfolio activity and improved macroeconomic factors, and our effective tax rate was 18.8%. Turning to Slide 9. We highlight our revenue trends. First quarter revenue was down $216 million or 4%, driven by lower net interest income and in part a seasonal decline in fee income. Net interest income of $3.3 billion declined $139 million or 4%, reflecting increased funding costs, lower loan balances, and one less day in the quarter. Fee income was $1.7 billion and decreased $74 million or 4% linked quarter. Looking at the detail. Asset management and brokerage revenue was up $4 million or 1%, reflecting higher average equity markets. Capital markets and advisory fees declined $50 million or 16%, driven by lower M&A advisory activity, off elevated fourth quarter levels, partially offset by higher underwriting fees. Card and cash management decreased $17 million or 2%, driven by seasonally lower consumer transaction volumes, partially offset by higher treasury management fees. Lending and deposit related fees declined $9 million or 3%, reflecting the reduction of customer fees on certain checking products. Residential and commercial mortgage revenue declined $2 million or 1%, and included lower residential mortgage activity. Other non-interest income of $135 million decreased $3 million or 2%, reflecting lower gains on sales. The first quarter also included a negative $7 million Visa fair value adjustment compared to a negative $100 million adjustment in the fourth quarter. Turning to Slide 10. Our core non-interest expense at $3.2 billion decreased $205 million or 6% linked quarter, reflecting strong expense management. Importantly, compared to the first quarter of 2023, core non-interest expense declined $117 million or 4%, with a decline in every expense category. This broad-based result reflects the impact of expense actions taken in 2023. As we've previously stated, we implemented expense management actions that will drive $750 million of cost savings in 2024. These actions include the $325 million workforce reduction effort last year, which was realized in our first quarter expense run rate, and our $425 million 2024 continuous improvement program goal, which we're well on track to achieve. We remain diligent in our expense management efforts, and these actions give us confidence that will keep our year-over-year expenses stable. Our credit metrics are presented
```

*Rank 3 — `PNC_2024_Q1_prepared_remarks_500_006`*

```
quarter. Fee income to be up 1% to 2%. Other non-interest income to be in the range of $150 million and $200 million, excluding Visa activity. Taking the component pieces of revenue together, we expect total revenue to be stable. We expect total core non-interest expense to be up 2% to 4%. We expect second quarter net charge-offs to be between $225 million and $275 million. As a reminder, PNC owns 3.5 million Visa class B shares with an unrecognized gain of approximately $1.6 billion. Under the terms of Visa's current exchange program scheduled to close on or about May 3, Class B shareholders will have the opportunity to monetize 50% of their holdings. We've not included the impact of monetizing the Visa gain in our forecast. Turning to Slide 14. Our full year 2024 guidance is unchanged from our January earnings call. And as a reminder, for the full year 2024 compared to the full year 2023, we expect average loan growth of approximately 1%. Total revenue to be stable to down 2%. Inside of that, our expectation is for net interest income to be down in the range of 4% to 5%, and non-interest income to be up 4% to 6%. Core non-interest expense, which excludes the FDIC assessment, is expected to be stable and we expect our affected tax rate to be approximately 18.5%. And with that, Bill and I are ready to take your questions.
```

*Rank 4 — `PNC_2024_Q4_prepared_remarks_500_004`*

```
tax rate was 14.6%, which included $60 million of income tax benefits related to the resolution of certain tax matters. Turning to slide 9, we highlight our revenue trends. On a full-year basis, we generated record revenue of $21.6 billion, as lower net interest income was more than offset by 6% growth in non-interest income. Looking at the linked quarter comparison, revenue increased $135 million, driven by higher net interest income. Net interest income of $3.5 billion increased $113 million, or 3%, driven by lower funding costs and the continued benefit of fixed rate asset repricing. Fee income was $1.9 billion and decreased $84 million, or 4% linked quarter. Looking at the detail, asset management and brokerage income declined $9 million, or 2%, reflecting lower annuity sales, partially offset by the benefit of higher average equity markets. Capital markets and advisory fees decreased $23 million or 6% reflecting elevated third quarter activity. Card and cash management fees were stable as higher Treasury management revenue was offset by credit card origination incentives. Lending and deposit services revenue grew $10 million, or 3%, due to increased customer activity. Mortgage revenue declined $59 million linked quarter, primarily due to elevated [RMSR] (ph) hedge gains in the third quarter. And our other noninterest income increased $106 million, reflecting a less negative impact from Visa derivative activity. Turning to Slide 10. Full year non-interest expense decreased by $488 million or 3%. Core non-interest expense was down $152 million or 1% compared to 2023. As a result, we generated positive operating leverage on a reported basis, as well as adjusted for non-core expenses. Fourth quarter non-interest expense of $3.5 billion increased $179 million or 5%. As I mentioned, the quarter included $79 million of non-core expenses, which reflected $97 million of asset impairments, partially offset by an $18 million reduction to the FDIC special assessment. The asset impairments included a number of items and were primarily related to various technology investments. Core non-interest expense increased $100 million or 3% linked quarter, largely due to seasonality and higher marketing spend. As you know, we had a 2024 goal of $450 million in cost savings through our continuous improvement program, which we exceeded. Looking forward to 2025, our annual CIP target
```

*Rank 5 — `PNC_2024_Q1_prepared_remarks_500_003`*

```
decline in commercial deposits. Regarding mix, consolidated, non-interest-bearing deposits were 24% in the first quarter, down slightly from 25% in the fourth quarter. Notably, on a spot basis in the first quarter, non-interest-bearing deposits had the smallest dollar decline since the Fed began raising rates in 2022, which gives us confidence that the non-interest-bearing portion of our deposits has largely stabilized. Our rate paid on interest-bearing deposits increased to 2.6% during the first quarter, up from 2.48% in the prior quarter. And as of March 31, our cumulative deposit beta was 45% and consistent with our expectations. We believe our deposit betas have approached their peak levels, although, we do expect some potential drift higher through the period leading up to a Fed rate cut, which we currently expect to occur in July. In regard to the timing and amount of potential rate cuts, we recognize there's a lot of fluidity and uncertainty. However, our 2024 NII will largely be unaffected by any short-term interest rate movement or lack thereof. This is because our floating rate assets are aligned with our floating rate liabilities, including our high beta commercial interest-bearing deposits and our long-term debt, which is almost entirely swapped to floating rates. Importantly, going forward, we've remained well positioned for the NII benefit of repricing low yielding fixed rate securities and loans maturing during the latter half of 2024 and into 2025. Turning to the income statement on Slide 8. First quarter net income was $1.3 billion or $3.10 per share, which included a pretax, non-core, non-interest expense of $130 million or $103 million after tax related to the increased FDIC special assess assessment. Excluding non-core expenses, adjusted EPS was $3.36 per share. Total revenue of $5.1 billion decreased $216 million or 4% compared to the fourth quarter of 2023. Net interest income declined by $139 million or 4%, and our net interest margin was 2.57%, a decline of 9 basis points, resulting primarily from higher funding costs. Non-interest income decreased $77 million or 4%. Non-interest expense of $3.3 billion declined $740 million or 18%, and included $130 million FDIC special assessment. Importantly, core non-interest expense was $3.2 billion and decreased $
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: All five chunks are PNC and PNC's NIM is in ch5; Capital One is absent. Second condition of this question with the same one-sided retrieval.

---

## 43. `ref_fact_03` / `chunk500_hybrid_enriched`

- **condition:** chunk500_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_fact_03
- **category:** factual
- **case:** C
- **outcome label:** answered_grounded_correct
- **coverage group:** single (1 anchor) (coverage@5 = 1)
- **Check 3 flag:** not flagged

**Question:**

> How much did Morgan Stanley report in advisory revenues for the first quarter of 2023?

**Generated answer, verbatim:**

```
Morgan Stanley reported $638 million in advisory revenues for the first quarter of 2023.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `MS_2023_Q1_prepared_remarks_500_002`*

```
strong prior year. Fixed income and equity results partially offset weakness in banking as we helped our clients intermediate markets through this period of heightened uncertainty. From a regional perspective, Asia delivered its third highest quarter ever with strength in areas of both fixed income and equity aided by the policy dynamics in Japan and the China reopening. Investment Banking revenues decreased year-over-year to $1.2 billion, solid revenue in advisory supported results while ongoing market volatility continued to pressure equity and non-investment grade underwriting. Advisory revenues were $638 million, benefiting from the completion of previously announced transactions. Revenues were down versus the strong prior year on the back of lower announced volumes in 2022. Equity underwriting revenues were $202 million, down 22%, largely as a result of depressed IPO activity. While IPO and follow-on activity remained muted, issuers selectively access market windows. Fixed income underwriting revenues were $407 million. Results were supported by an open investment grade market and opportunistic loan activity. Clients are engaged as we help them navigate an uncertain backdrop and our investment banking backlog is building. Financial sponsors continue to look for opportunities to invest. Within underwriting, we are encouraged by the issuance activity during constructive windows. Of course, further conversion from pipeline to realized is predicated on clarity around macroeconomic conditions, stable financing markets and increased corporate confidence. Equity revenues were $2.7 billion, a solid quarter against an uncertain and volatile backdrop. We continue to be a leader in this business and the results reflect our global and diversified footprint. Cash revenues decreased versus the prior first quarter on lower global volumes. Derivatives results were solid compared to a strong quarter last year as we help navigate – as we help clients navigate challenging markets. Prime brokerage revenues were down as equity market levels declined. Clients remained engaged and balances increased steadily throughout the quarter. Fixed income revenues of $2.6 billion were strong, though lower versus the prior year’s elevated result, which was impacted by the beginning of the Fed rate hiking cycle and a start of the war in Ukraine. This quarter’s performance was driven by rates and credit. Macro revenues were down modestly year-over-year with relative strength in rates versus foreign exchange in the comparison period. The volatility created by varying expectations around global central bank policy aided results across regions. Micro results were up versus the prior year, supported by client engagement. Commodity revenues moderated meaningfully
```

*Rank 2 — `MS_2023_Q1_prepared_remarks_500_001`*

```
d and we saw strength in Parametric and also in the liquidity product. Overall margin in the Wealth Management business was 26%, impacted by modest increases in credit reserves, slightly lower growth of NII versus forecast and ongoing integration expenses. We continue to focus on the levers within our control with an eye towards expense management. In ISG, underwriting and M&A remain very subdued. As I have said previously, these are revenues delayed, not dead. Already, we are seeing a growing M&A pipeline and some spring-like signs of new issuance emerging. That said, it largely remains a back half 2023 and full year 2024 story. On the positive side, our fixed income and equity trading teams performed very well in managing through some historic rate moves. Total trading revenues were solid. I expect the markets to remain choppy through this earnings season and for the next several months. However, absent any geopolitical surprise or limited progress on bringing down inflation, I think 2023 is likely to end on a constructive note in most areas. Morgan Stanley is very well positioned not just for 2023, but for several years ahead as we see significant growth opportunities across all three of our client platforms. I will now pass it over to Sharon for more details on the first quarter.

Sharon Yeshaya: Thank you, and good morning. The firm produced revenues of $14.5 billion in the first quarter, our EPS was $1.70, and our ROTCE was 16.9%. The firm’s results demonstrated the durability of our business model, evidenced by the resilient ROTCE, robust asset consolidation and wealth and our stable capital and liquidity levels. In institutional securities, fixed income and equity supported our clients while navigating volatile markets. Wealth Management showcased $110 billion of net new assets and investment management continued to benefit from the investments we have made to diversify our offerings. The firm’s first quarter efficiency ratio was 72%. Deferred cash-based compensation plans negatively impacted our firm’s efficiency ratio by approximately 60 basis points. Ongoing technology and marketing and business development investments as well as higher litigation costs increased operational expenses versus the prior year. Given the broader market uncertainty and the inflationary environment, expense management remains a priority, although we continue to prioritize investments in our long-term goals. Now to the businesses. Institutional Securities revenues were $6.8 billion, an 11% decline from the very
```

*Rank 3 — `MS_2023_Q3_prepared_remarks_500_002`*

```
in the third quarter were solid against a mixed market backdrop. The firm's year-to-date efficiency ratio was 75%. Together, severance and DCP impacted the year-to-date efficiency ratio by nearly 150 basis points. As we invest for growth, our integration efforts have remained a priority. Integration-related expenses were $68 million in the third quarter, and we anticipate a similar amount in the fourth quarter as previously communicated. Now to the businesses. Institutional securities revenues were $5.7 billion, declining 3% versus the prior year. Equity and fixed income results were in line with long-term historical averages. Investment banking revenues remained depressed on lower volume. However, leading indicators across advisory and underwriting progress positively, evidenced by a notable increase of Morgan Stanley's announced volumes in the third quarter on a year-over-year basis. Investment banking revenues decreased to $938 million. The change to the previous year was driven by lower results in advisory and debt underwriting. Advisory revenues of $449 million reflected a decline in completed transactions, due to lower announced volumes in prior periods. Despite the weaker quarterly results, we continue to see broad sector diversification of our completed deals and the backlog reflects a similar pattern. Equity underwriting revenues were $237 million. Overall activity remained muted relative to historical averages. While increased confidence supported early September issuances, a hawkish tone from the Federal Reserve, and resulting moves in interest rates serve as a reminder that this market remains window-driven. Fixed income underwriting revenues were $252 million down versus the prior year, primarily reflecting lower non-investment grade events. We are encouraged by the growing client dialogue and bake-off activity across sectors and geographies. The pickup in our announced M&A volumes in the third quarter speak to the trends we've observed at the end of the last quarter. But the landscape continues to evolve. As we look ahead, corporate confidence will largely be determined by the overall health of the consumer and the stability of input costs. While risks remain, including geopolitical threats, the underlying trends suggest activity is building and there is a desire among clients to pursue their long-term strategic objectives. Equity revenues were $2.5 billion. The business performed in line with historical averages with relative strength in Europe and Asia. Prime brokerage revenues were solid. Client balances were modestly higher, compared to last year. The results reflect narrower spreads and the
```

*Rank 4 — `MS_2024_Q1_prepared_remarks_500_002`*

```
revenues, particularly asset management fees in the wealth management business, stronger capital markets and a continued focus on managing the full income statement, all contributed to results. The firm's first quarter efficiency ratio was 71%, illustrating the inherent operating leverage in the model and our ongoing efforts to consolidate our expense base following multiple years of integration. Efforts are evidenced by the year-over-year reduction in professional services and marketing and business development spend, lower legal expenses further supported the improvement in efficiency ratio. Now to the businesses. Institutional securities revenues of $7 billion were up 3% versus the prior year, reflecting strong performance across businesses. First quarter revenues underscore the power of the integrated firm as our cross divisional collaboration positioned us to capitalize on market opportunities. The geographical breadth continues to distinguish our franchise and puts us at the center of client activity as the backdrop improves across regions. Investment banking revenues were $1.4 billion for the first quarter, up 16% from the prior year. A pickup in both equity and fixed income underwriting supported results, offsetting the year-over-year decline in advisory. Leading indicators continued to progress positively, including the preliminary reemergence of sponsor activity. Advisory revenues of $461 million reflected a decline in completed M&A transactions. Equity underwriting revenues of $430 million more than doubled versus the prior year as IPO markets reopened for most of the quarter alongside conducive markets for follow-ons. Our global reach supported our ability to lead cross-border transactions, and we regained our premier leadership position in equity underwriting lead tables as global market volumes picked up. Fixed income underwriting increased year over year to $556 million, results were driven by strength in investment grade and noninvestment grade bond issuance as clients took advantage of tighter credit spreads. Looking ahead, we expect the steady build of this business to continue. We are encouraged by the health of the advisory and underwriting pipelines. While the uncertainty of the rate path and geopolitical developments may impact the near-term conversion of pipeline to realized, conditions should improve over time and the underlying trends suggest that confidence is increasing. We remain focused on expanding our reach through opportunistic hires, particularly as we continue to see diverse pipeline and increased sponsor activity. Turning to Equity, we continue to be a global leader in this business. Revenues were strong increasing 4% from the prior year to $2.8 billion. Results were supported by performance in
```

*Rank 5 — `MS_2023_Q1_prepared_remarks_500_003`*

```
compared to the robust results in the previous first quarter largely due to reduced volatility in European markets and the mild weather in the U.S. Other revenues of $245 million improved versus the prior year, largely driven by higher revenues on corporate lending activity and gains related to DCP. Turning to ISG lending and provisions, our allowance for credit losses on ISG loans and lending commitments increased to $1.3 billion. In the quarter, ISG provisions were $189 million and net charge-offs were $70 million. The increase in provisions was driven by the higher recessionary probability and worsening outlook for commercial real estate. The charge-offs were substantially all from a handful of specific loans. Turning to Wealth Management, revenues were $6.6 billion. Movements in DCP positively impacted revenues by approximately $100 million compared to a negative impact of nearly $300 million in last year’s first quarter. Net new asset growth of $110 billion was a standout as we continue to execute on our long-term strategy. Pre-tax profit was $1.7 billion and the PBT margin was 26.1%. The margin reflects a more favorable revenue mix offset by higher credit provisions and an increase in expenses as we continue to invest in our business, inclusive of integration-related expenses. Credit provisions were $78 million, including those that impacted revenue and the integration-related expenses for the quarter were $53 million, in line with our expectations. Forward growth drivers remain robust. Net new assets were very strong at $110 billion for the quarter, representing a 10% annualized growth rate of beginning period assets. While NNA will be lumpy and should be looked at on a full year basis, the results illustrate our ability to attract assets and the payoff of our investments to support growth. We saw contribution from all channels with notable strength in the adviser led channel, particularly amongst existing clients. The events in March and the rising interest rate environment over the past year impacted client behavior. Clients increased their allocation to cash equivalents such as money market funds and U.S. treasuries by over 60% versus last year. At the same time, deposits declined in the quarter by 3% to $341 billion. We believe investable assets stayed within Morgan Stanley as our clients worked with advisers to help navigate the volatile markets. Today, adviser-led assets invested in cash and cash equivalents stand at a peak of 23% compared to historical average of approximately
```

verdict: faithful

failure mode: none — right figure chosen against two plausible distractors

notes: Exact: $638m (ch1). Three plausible distractors were in context — $449m (Q3 2023) and $461m (Q1 2024) — and it took the right one. Label agrees.

---

## 44. `ref_them_04` / `chunk200_bm25_enriched`

- **condition:** chunk200_bm25_enriched
- **arm:** enriched
- **question_id:** ref_them_04
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did banks describe their progress on positive operating leverage in late 2023 and early 2024?

**Generated answer, verbatim:**

```
In late 2023, Bank of America’s CEO Robin Vince stated that the company was committed to achieving aggregate positive operating leverage for the following year, expressing confidence due to ongoing investments. In Q1 2024, Bank of America reported that it delivered positive operating leverage on both a reported basis and excluding notable items, with expenses growing by only 2% year-over-year compared to total revenue growth of 3%.

Additionally, in early 2024 (referencing the prior quarter's performance), another bank noted that it had delivered positive operating leverage year-over-year while bending its cost curve. In Q4 2024, a bank executive indicated confidence in providing a guide for at least 200 basis points of positive operating leverage, citing strong expense management and revenue inflection points. Bank of America also emphasized in late 2024 that total operating leverage is their "North Star," while they remain focused on delivering positive fee operating leverage through the cycle.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BK_2023_Q3_qa_200_019`*

```
approach across the company. We've got KYC as an example as well. We used to do KYC in each of our businesses. We're bringing that together to have a KYC platform. So there are a lot of proof points that we've got in various stages of development here in addition to the actual pilots that we did, specifically for a platform's operating model.

Mike Mayo: So when you add it all together you said next year you expect to have positive operating leverage, is that in aggregate or positive fee operating leverage and how can you have such confidence at this stage?

Robin Vince: So look we're committed to positive operating leverage over time. And I don't want my second year as CEO to be one where we have negative operating leverage. So we are focused on positive operating leverage next year. That's aggregate operating leverage to answer your question. And one of the reasons why we have confidence in that is because we've been investing on
```

*Rank 2 — `BK_2023_Q1_prepared_remarks_200_006`*

```
-over-year, and we generated a healthy return on tangible common equity of 20%. And given how in focused capital and liquidity are at the moment, I'll note that our Tier 1 leverage ratio as well as our liquidity coverage ratio remains strong and unchanged compared to the prior quarter, well above regulatory requirements and our own management buffers. Stepping back for a moment, I'm encouraged by the early progress that we are seeing around the Company to deliver on the commitment that we made to you back in January. First, we are bending the cost curve. Our first quarter expense growth came in marginally better than our initial internal plan and we remain firmly committed to cutting our core expense growth by roughly half this year compared to 2022 on a constant currency basis. Second, in line with our outlook for the year, we continued to derive healthy growth in net interest revenue. Third, we delivered positive operating leverage on a year-over-year basis. And fourth, we returned
```

*Rank 3 — `USB_2024_Q4_qa_200_024`*

```
on positive operating leverage. You said at least 200 basis points. I think after so long not having positive operating leverage, I think people are wondering, it's kind of a show me story. I think you might understand that. Under what scenario do you think you could have more than the 200 basis points guide? Some other banks are actually guiding higher today and you have a lot of tailwinds in the industry. So, how high could that go? Because the stock is down, people are questioning this. What would be your reaction?

Andy Cecere: Mike, what we wanted to do is to provide a guide that we have confidence in and that we're conservatively giving you numbers. I'm very confident in our ability to manage expense in this environment. And I'm very confident in the inflection point on the revenue components. So that's why we put a 200 basis point plus on that guide. So we'll hit 200 at least.
```

*Rank 4 — `BK_2024_Q1_prepared_remarks_200_003`*

```
back of positive operating leverage in the first quarter. We reported earnings per share of $1.25 up 11% year-over-year, and excluding notable items, earnings per share of $1.29 were up 14%. Total revenue of $4.5 billion was up 3% year-over-year. That included 8% growth in investment services fees, led by strength in asset servicing, issuer services, and clearance and collateral management, which more than offset revenue headwinds from muted volatility in FX markets and lower net interest income. Expenses of $3.2 billion were up 2% year-over-year and up 1% excluding notable items. Consistent with our goal to generate at least some operating leverage this year, in the first quarter, we did deliver positive operating leverage, both on a reported basis and excluding notable items. Our reported pre-tax margin was 29% or 30% excluding notable items, and we generated a 21% return on tangible common
```

*Rank 5 — `BK_2024_Q4_qa_200_024`*

```
about the fee operating leverage as well as a metric that you care about or not?

Dermot McDonogh: Thanks, Alex. So we do talk about total and we're very focused on delivering that consistently through the cycle and I also think about it in terms of fee operating leverage and we're also focused on delivering positive fee operating leverage as well. But look, as I said in my prepared remarks, total operating leverage is the North Star. There are a number of factors that go into that. NII, fees, expenses and with each of those categories, we have multiple levers that we can toggle. So we feel like we have flexibility over the inputs in terms of how we end up with that number and so I kind of think if you kind of take last year, 288 was a very good year and look, there was a reasonable amount of kind of positive contribution to that from NII and so we expect to deliver positive fee operating leverage through the cycle as
```

verdict: unfaithful

failure mode: company misattribution x3 plus a misattributed executive — every "Bank of America" here is BNY Mellon

notes: Every "Bank of America" here is BNY Mellon: Robin Vince is BNY's CEO (ch1), the Q1 2024 2%/3% figures are BK_2024_Q1 (ch4), and the "North Star" line is Dermot McDonogh (ch5). Three misattributions plus a named executive. Note the contrast inside the answer — it writes "another bank" and "a bank executive" where it was unsure, and names the wrong bank where it guessed.

---

## 45. `ref_them_11` / `chunk500_hybrid`

- **condition:** chunk500_hybrid
- **arm:** text_only
- **question_id:** ref_them_11
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How did banks characterise their net charge-off levels and direction in 2023 and 2024?

**Generated answer, verbatim:**

```
Based on the provided context, banks characterized their net charge-off (NCO) levels and direction as follows:

*   **Capital One (COF):** In Q4 2023, management declared that NCOs were "leveling off" or stabilizing. They noted that Q4 2023 NCOs were approximately 15% above 2018 levels and projected that NCOs would stabilize at about 15% above 2019 levels heading into 2024, with typical month-to-month volatility.
*   **Bank of America (BAC):** In 2023, NCOs "moved higher through the year off historic lows," but management stated they still compared "very favorably against historic averages." The bank characterized asset quality as solid.
*   **U.S. Bancorp (USB):** Management expected NCOs to continue to "normalize" in 2024. They noted that credit card NCOs were getting closer to pre-pandemic levels but would continue to move up slightly. For full-year 2024, they projected an NCO rate in the "mid-50s."
*   **Fifth Third Bancorp (FITB):** The net charge-off outlook for full-year 2024 remained in the range of 35 to 45 basis points.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `COF_2023_Q4_qa_500_008`*

```
, we feel confident declaring that our delinquencies have stabilized. And of course, delinquencies are our best leading indicator of credit performance. Our charge-offs have been catching up to the stabilizing trend in our delinquencies over the second half of 2023. But at this point, what we're declaring here is that our charge-offs are leveling off as well. Now, there's more month-to-month volatility in charge-offs than in delinquencies by quite a bit. Because every data point of delinquencies includes five months of delinquency inventories. And of course, charge-offs is looking at the relatively small number that falls off at the end of the last bucket. And there was also some noise in the fourth quarter of 2019, that makes it less reliable as a charge-off benchmark. So, we actually think 2018 is an even better benchmark for our charge-offs, for comparing our charge-offs in this fourth quarter that just happened to a past stable year. In the fourth quarter, our net charge-offs were about 15% above 2018 levels. And of course, 2018 rolled into 2019, so that's an appropriate benchmark to look at as we head into 2024 and compared to 2019. Now when we look ahead, extrapolating from our current delinquency inventories and recent flow rates, we conclude that our net charge-offs are stabilizing at about 15% above 2019, with of course some typical month-to-month volatility and normal seasonality. Now, of course, the seeds of this stabilization have been planted for quite a long time now and partly driven by the choices that we made back in 2020 and 2021. Coming out the pandemic, we were concerned about two trends. FinTechs were flooding the market, especially the subprime market with credit offers, creating the potential for credit worsening and adverse selection in our originations. We also anticipated that pandemic era stimulus and forbearance would temporarily inflate consumer credit scores and that these would revert over time. So, we tightened our underwriting in anticipation of these effects and we have continued to make adjustments at the margin since then. And the result has been striking, that with all the kind of changes, the normalization, all the noise over the last number of years, that there has been striking
```

*Rank 2 — `BAC_2023_Q4_prepared_remarks_500_002`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 3 — `USB_2023_Q4_qa_500_005`*

```
on what you saw this quarter in credit quality, on the NPA movement, particularly in commercial. And then, also, John, maybe just some thoughts on the potential charge-off trajectory as you see things migrate from NPA into charge-offs this year, what we should be thinking about? Thank you.

Terry Dolan: Yeah. Good morning, John. This is Terry Dolan. So, I'm going to take this question related to credit quality. Your first one is really related to non-performing assets and some of the things that we saw in the fourth quarter. If you end up going across the portfolio, generally pretty stable. We did see a couple of idiosyncratic loans that went into non-performing status. Both of those were kind of Union legacy sort of credits, so continue to kind of work through that. But I would also say that both of those are fairly well collateralized. So, we don't necessarily see a lot of charge-off content related to those idiosyncratic credits. When we look at net charge-offs and the trajectory, I would expect that -- we would expect that it will continue to kind of normalize. Credit card is kind of getting closer to pre-pandemic levels, but that will continue to move up a little bit. Our expectation is that for full year 2024, we'll probably be in kind of in the mid-50s in terms of the net charge-off rate.

John McDonald: Okay. Thanks, Terry. And then, John or Andy, just on the fee revenues, John ticked off on the fee revenues, a number of high-single digit kind of potential growers in '24. How do we think about kind of the ability to grow total fee revenues and what kind of base should we use for that? It looks like maybe the adjusted base for '23 was about $10.8 billion of fee revenues. Is that something you can grow off of that? Just trying to contextualize. Total revenue last year was around $28 billion. How should we think about the ability to grow revenues on fees and maybe total revenues this year?

John Stern: Yeah. So I mean, we had, as you mentioned, some of the fee numbers there. From a core fee perspective, we do expect to grow. I ticked off some of the areas in terms of payments, commercial products, trust and all sort of thing. Other --
```

*Rank 4 — `FITB_2024_Q2_prepared_remarks_500_006`*

```
the second half of 2024. Given the year-to-date trends in customer activity, we now expect full-year average total loans to be down 3% compared to 2023. Average total loans in the fourth quarter of 2024 are expected to be stable to up 1% compared to the fourth quarter of 2023, with similar performance in both the commercial and consumer portfolios. Customer demand is the primary driver of this change, given the interest rate environment and other economic uncertainties. If there's more economic optimism in the second half of the year, we would expect to see loan growth in-line or better than market growth. We are forecasting fourth quarter average core deposit growth of 2% to 3% when compared to the fourth quarter of 2023. Our forecast also assumes commercial revolver utilization and our cash and other short-term investments remain relatively stable throughout the remainder of 2024. We expect full-year adjusted non-interest income to be stable to down 1% in 2024, reflecting the impact of weaker than previously expected credit demand and customer hedging activities. We expect strong growth in commercial payments and wealth and asset management revenue to continue. In response to this expectation of lower customer activity in the second half. We expect to manage full year adjusted non-interest expense stable to 2023 levels. Our expense outlook assumes continued investments in technology with tech expense growth in the mid-single digits and sales additions in middle market, commercial payments, and wealth. We will open 30 to 35 new branches in our higher growth markets and have already closed a similar number of branches in 2024. Our outlook still projects an efficiency ratio of around 57% for the full year. For full year 2024, the net charge-off outlook remains in the 35 to 45 basis points range. While we expect to resume provision builds in connection with loan growth and mix in the second half of 2024, we expect the second half build to be less than the first half of 2024 release. Therefore, we expect full-year provision to be a 0 to $10 million release, assuming no change to credit quality of the portfolio or projected economic conditions. Moving to our quarterly outlook, we expect NII and NIM growth to continue in both the third and fourth quarter. We expect NII in the third quarter to be up 2% sequentially, reflecting the impact of slowing deposit cost pressures and the continued benefit of our fixed rate asset repricing. Our current outlook assumes interest
```

*Rank 5 — `COF_2024_Q3_prepared_remarks_500_004`*

```
2022, auto charge-offs have been strong and stable. Slide 13 shows third quarter results for our Commercial Banking business. Compared to the linked quarter, ending loan balances decreased about 2%. Average loans were down about 1%. The modest declines are largely the result of choices we made in 2023 to tighten credit. Ending deposits were up about 5% from the linked quarter. Average deposits were down about 1%. We continue to manage down selected less attractive commercial deposit balances. Third quarter revenue was up 1% from the linked quarter and non-interest expense was up by about 2%. The Commercial Banking annualized net charge-off rate for the third quarter increased 7 basis points from the sequential quarter to 0.22%. The Commercial Banking criticized performing loan rate was 7.66%, down 96 basis points compared to the linked quarter. The criticized non-performing loan rate increased 9 basis points to 1.55%. In closing, we continued to post strong results in the third quarter. We delivered another quarter of top-line growth in domestic card loans, purchase volume and revenue. In the auto business, we saw year-over-year growth in originations for the third consecutive quarter and consumer credit trends remained stable. Our year-to-date operating efficiency ratio, net of adjustments through September was 41.7%. We had guided to 2024 annual operating efficiency ratio, net of adjustments to be modestly down compared to the 43.5% we posted in 2023. Our view included the positive impact from the end of the revenue sharing related to the Walmart partnership and assumed the CFPB late fee rule would take effect in October. Looking forward, we now expect the full year 2024 annual operating efficiency ratio net of adjustments to be in the low 42s. We expect a sequential quarter increase in operating expense in the fourth quarter, that will be roughly in line with historical patterns as we continue to invest in our technology transformation. And we are no longer assuming that the CFPB late fee rule will be implemented in 2024, given ongoing uncertainty around industry litigation. Our view of 2024 marketing has not changed. We continue to lean into marketing to grow and to further strengthen our franchise. In the Domestic Card business, we continue to get traction in originations across our products and channels. In Consumer Banking, we're leaning into marketing to grow our digital first national banking franchise. We continue to expect total company marketing in the second half
```

verdict: faithful

failure mode: none

notes: All four banks correct with accurate quotes (COF ch1, BAC ch2, USB ch3, FITB ch4), answering both level and direction as asked.

---

## 46. `ref_them_05` / `chunk200_hybrid_enriched`

- **condition:** chunk200_hybrid_enriched
- **arm:** enriched
- **question_id:** ref_them_05
- **category:** thematic
- **case:** B
- **outcome label:** answered_grounded_offtarget
- **coverage@5:** 0

**Question:**

> How much did banks return through dividends and share repurchases in the third quarter of 2024, and how did the scale differ?

**Generated answer, verbatim:**

```
Based on the provided context, only two banks reported specific figures for the third quarter of 2024:

*   **State Street (STT):** Returned over **$670 million** in total capital to shareholders. This included **$450 million** in common share repurchases and implied dividends making up the remainder of the $670 million total (as the text states "In total, we returned over $670 million... equivalent to a total payout ratio of almost 100%").
*   **Fifth Third Bank (FITB):** Executed **$200 million** in share repurchases and increased its common dividend by 6% to **$0.37 per share**. The context does not provide the total dollar amount for dividends paid, only the per-share increase.

The scale differed significantly between these two institutions, with State Street returning over $670 million in total capital compared to Fifth Third Bank's reported $200 million in share repurchases alone (plus unspecified dividend totals). Other banks mentioned in the context (BlackRock and Bank of New York Mellon) provided data for 2023 or Q1/Q4 2024, not Q3 2024.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BLK_2023_Q4_prepared_remarks_200_013`*

```
committed to delivering a premium operating margin. Our capital management strategy remains consistent. We invest first either to scale strategic growth initiatives or drive operational efficiency and then return excess cash to our shareholders through a combination of dividends and share repurchases. In 2023, we returned over $4.5 billion to our shareholders through a combination of dividends and share repurchases. Share repurchases have been a consistent element of our capital management strategy. Since 2013, we've repurchased close to $15 billion of BlackRock stock, which generated an unlevered compound annual return of 14% for our shareholders. Over this time period, we reduced our share count by nearly 23 million shares or 13%. For the trailing five years, we've lowered our share count by 10 million shares completing $7.8 billion of share repurchases at an average price of $563 for an IRR of over 15%. BlackRock's Board of
```

*Rank 2 — `FITB_2024_Q4_prepared_remarks_200_021`*

```
$10 million to $25 million due to loan growth. Finally, we expect to execute $225 million in share repurchases in the first quarter, with future quarter share repurchases dependent on the level of loan growth. We will continue to target our CET1 ratio around 10.5%, while we await more clarity around the future of the capital rules and other regulations. In summary, with our resilient balance sheet, diversified revenue streams, and disciplined expense and credit risk management, 2025 is set to be a year of continuing long-term investments, record NII, positive operating leverage, and strong returns for our shareholders. With that, let me turn it over to Matt to open the call for Q&A.

Matt Curoe: Thanks, Bryan. Before we start Q&A, given the time we have this morning, we ask that you limit yourself to one question and one follow-up, and then return to the queue, if you
```

*Rank 3 — `FITB_2024_Q3_prepared_remarks_200_005`*

```
the way in terms of growth that is delinked from our balance sheet. Over 40% of all new commercial payments relationships added this year have been payments led with no credit attached. In our Wealth and Asset Management business, we achieved record quarterly revenues growing by 12% year-over-year. Total assets under management have grown $12 billion in the past year or up 21% to $69 billion. Our Fifth Third Private Bank, Fifth Third Securities, and Fifth Third Wealth Advisors business units all continue to generate strong performance. Turning to capital, our strong profitability and disciplined balance sheet management are providing growth capacity and the opportunity to increase capital return to shareholders. This quarter, we increased our common dividend by 6% to $0.37 per share and executed $200 million in share repurchases. Even with these actions, our CET1 ratio increased to 10.8%. This will allow us to increase share repurchases in the fourth quarter to $300 million
```

*Rank 4 — `STT_2024_Q3_prepared_remarks_200_017`*

```
generated from earnings combined with the benefit of lower rates on AOCI more than offset increased capital return and RWA growth as we supported our clients. As I just noted, we delivered on our goal to accelerate capital return in the third quarter with common share repurchases of $450 million, up from $200 million in the prior quarter and $100 million in Q1. But falling rate moves at the end of the quarter did create some unexpected excess capital. In total, we returned over $670 million of capital to our shareholders this quarter, equivalent to a total payout ratio of almost 100%. As we look ahead, we are planning for another quarter of healthy capital return in Q4, which we would expect to be somewhat higher than this quarter, subject to market conditions and other factors. As such, we continue to expect the full-year payout ratio for 2024 to be comfortably in the 80% to 90% range as we aim to strike the right balance between our capital
```

*Rank 5 — `BK_2023_Q3_prepared_remarks_200_014`*

```
on Page 4. Consistent with the prior quarter, we returned $450 million of capital to our shareholders through common share repurchases and we paid approximately $330 million of dividends to our common stockholders, reflecting our previously announced 14% dividend increase, which became effective in the third quarter. Taken together, we returned 82% of earnings to shareholders in the quarter, or 107% on a year-to-date basis. Our Tier 1 leverage ratio improved sequentially by approximately 40 basis points to 6.1% reflecting a decrease in average assets and an increase in Tier 1 capital driven by capital generated through earnings, net of capital returns through buybacks and dividends. Unrealized losses related to available for sale securities remained roughly unchanged in the quarter. The CET1 ratio was 11.4%, representing an approximately 30 basis points improvement compared with the prior quarter, reflecting lower risk weighted assets and an increase in CET1 capital. Just like our regulatory capital ratios, our
```

verdict: faithful

failure mode: none

notes: Correctly restricts to the two banks that report Q3 2024 (STT ch4, FITB ch3), gives the scale comparison the question asks for, and explains why BLK and BNY do not qualify — naming BNY correctly. The dividend residual is flagged as inferred rather than stated.

---

## 47. `ref_comp_02` / `chunk500_bm25_enriched`

- **condition:** chunk500_bm25_enriched
- **arm:** enriched
- **question_id:** ref_comp_02
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did Bank of America's and Huntington's positions on office real estate exposure differ in the first quarter of 2024, in charge-offs and in portfolio reduction?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BAC_2023_Q2_prepared_remarks_500_012`*

```
to 213,000. That's some good work after peaking at 218,000 in January. Our summer interns will leave us in the third quarter, and hopefully many will return as full-time associates next summer. And at the same time in Q3, we welcomed back about 2,600 new full-time hires as college grads, many of whom interned with us last summer. And that's a very diverse class of associates who are excited to join the company. As we look forward to next quarter, we would expect the third quarter expense to more fully benefit from the second quarter head count reduction, even as we remain in a mode of modest hiring for client-facing positions. Additionally, the proposed notice of special assessment from the FDIC to recover losses from the failures of Silicon Valley and signature banks could add $1.9 billion expense for us, $1.5 billion after tax, and we just remain unsure at this point of timing to record that expense. Let's now move to credit, and we'll turn to Slide 17. Net charge-offs of $869 million increased $62 million from the first quarter, and the increase was driven by credit card losses as higher late-stage delinquencies flowed through to charge-offs. For context, the credit card net charge-off rate was 2.6% in Q2, and remains well below the 3.03% pre-pandemic rate in the fourth quarter of '19. Provision expense was $1.1 billion in Q2, and that included a $256 million further reserve build, that's driven by loan growth, particularly in credit card, and it reflects a macroeconomic outlook that on a weighted basis continues to include an unemployment rate that rises to north of 5% in 2024. On Slide 18, we highlight the credit quality metrics for both our consumer and commercial portfolios. On consumer, we note we continue to see asset quality metrics come off the bottom, and they remain below historical averages. Overall commercial net charge-offs were flat from first quarter. And within commercial we saw a decrease in C&I losses that was offset by an increase in charge-offs related to commercial real estate office exposures. As a reminder, commercial real estate office credit exposure represents less than 2% of our total loans, and this is an area where we've been quite intentional around our client selection, portfolio concentration, and deal structure over many
```

*Rank 2 — `BAC_2024_Q1_prepared_remarks_500_009`*

```
306 million from the fourth quarter, driven by continued credit card seasoning and commercial real estate office exposures as swift revaluations from current appraisals and resolutions drove higher charge-offs. The net charge-off ratio was 58 basis points, a 13 basis point increase from the fourth quarter. On Slide 12, we show you the credit quality metrics for both our consumer and commercial portfolios. Consumer net charge-offs increased $150 million versus the fourth quarter from the flow-through of higher late stage credit card delinquencies. We included a credit card delinquency slide, No. 28 in our appendix, and we’re encouraged by the trend of delinquencies because the late stage increases slowed and early stage delinquencies improved as well, and that leads us to believe we should begin to see consumer net charge-offs start to level out over the next quarter or so. All of this is still well within our risk appetite and our expectations, and it’s consistent with the normalization of credit we discussed with you in prior calls. Commercial net charge-offs increased $191 million versus the fourth quarter, driven by commercial real estate losses and office exposures. On office losses this quarter, we recorded charge-offs on 16 office loans. Four were a result of sales activity, i.e. final resolution, seven were from losses that we expect on exposures that are in the process of expected resolution in the course of the next 90 days, and the rest we took as a result of refreshed valuations. We use a continuous and thorough loan-by-loan analysis and we’re quick to recognize impacts in the commercial real estate office space through our risk ratings, and that’s resulted in several downgrades in the last few quarters. As a result of these quick actions and our downgrades in categorization, we’ve also refreshed the valuation of our reservable criticized properties, and we’ve taken appropriate reserves and charge-offs in the process. Roughly one-third of our office exposure is now categorized as reservable criticized, and importantly the pace of the increase in reservable criticized exposures has slowed each quarter since the second quarter of last year, so we believe the losses on these office properties have been front-loaded and largely reserved. We expect the losses to move lower in the second quarter and we expect a notable decline in the second half of the year
```

*Rank 3 — `PNC_2024_Q1_prepared_remarks_500_005`*

```
on Slide 11. While overall credit quality remains resilient, the pressure we anticipated within the commercial real estate office sector has continued. Non-performing loans increased $200 million or 9% linked quarter, almost entirely driven by commercial real estate, which increased $188 million. And inside of that, approximately $150 million was related to the CRE office portfolio. Total delinquencies of $1.3 billion decreased $109 million or 8% linked quarter, driven by lower consumer and commercial delinquencies. Net loan charge-offs were $243 million in the first quarter, and our annualized net charge-offs to average loans ratio was 30 basis points. Our allowance for credit losses totaled $5.4 billion or 1.7% of total loans on March 31, stable with December 31. Slide 12 provides more detail on our CRE office credit metrics. While NPLs have increased over the past few quarters, our criticized balances have remained relatively consistent. The migration of criticized loans to non-performing status is an expected outcome as we work to resolve the occupancy and rate challenges inherent to this portfolio. In the first quarter, net loan charge-offs within the CRE office portfolio were $50 million, essentially in line with the previous quarter level. Ultimately, we expect continued charge-offs on this portfolio, and accordingly we believe we are adequately reserved. As of March 31, our reserves on the office portfolio were 9.7% of total office loans and inside of that, 14.4% on the multitenant portfolio. Importantly, we continue to manage our exposure down and as a result, our balances declined 3%, or approximately $200 million linked quarter. In summary, PNC reported a solid first quarter 2024, and we're well positioned for the remainder of the year. Regarding our view of the overall economy, we're expecting economic expansion in the second half of the year, resulting in real GDP growth of approximately 2% in 2024, and unemployment to increase modestly to 4% by year end. We expect the Fed to cut rates 2 times in 2024, with a 25 basis point decrease in July and another in November. Looking at the second quarter of 2024 compared to the first quarter of 2024, we expect average loans to be stable, net interest income to be down approximately 1%. And as I mentioned previously, we expect NII and net interest margin to trough in the second
```

*Rank 4 — `WFC_2023_Q2_prepared_remarks_500_004`*

```
expect to repurchase more common stock this year, we believe continuing to maintain significant excess capital is appropriate until there's more clarity on the new capital requirements that Charlie highlighted. Our liquidity position remained strong in the second quarter with our liquidity coverage ratio approximately 23 percentage points above the regulatory minimum. Turning to credit quality on Slide 5. Overall credit quality remained strong, but as expected, net loan charge-offs continued to increase from historically low levels and were 32 basis points of average loans in the second quarter. Commercial net loan charge offs increased $137 million from the first quarter to 15 basis points of average loans. Approximately half of the increase was in commercial banking where the losses were borrower-specific with little signs of systematic weakness across the portfolio. The rest of the increase was driven by higher losses in commercial real estate, primarily in the office portfolio. I'll share some more details on the CRE office exposure on the next slide. Consumer net loan charge-offs increased modestly, up $23 million from the first quarter to 58 basis points of average loans. The increase primarily came from the credit card portfolio as residential mortgage loans continue to have net recoveries and auto losses declined. While consumer credit performance remained solid overall, and we’ve continued to take incremental credit tightening actions across the portfolios, we expect consumer net loan charge-offs will continue to gradually increase. Non-performing assets increased 14% from the first quarter as lower non-accrual loans across the consumer portfolios were more than offset by higher commercial non-accrual loans, primarily in the commercial real estate portfolio. Our allowance for credit losses increased $949 million in the second quarter, primarily from -- for commercial real estate office loans as well as for higher credit card balances. We've updated Slide 6, which highlights our commercial real estate portfolio. We had $154.3 billion of commercial real estate loans outstanding at the end of the second quarter with $33.1 billion of office loans, which were down modestly from the first quarter and represented 3% of our total loans outstanding. The office market continues to be weak and the composition of our office portfolio was relatively consistent with what we shared with you in the first quarter. As Charlie mentioned, our CRE teams are focused on surveillance and de-risking which includes reducing exposures and closely monitoring at-risk loans. This quarter, we added a table to this slide that breaks down our CRE office
```

*Rank 5 — `BAC_2024_Q2_prepared_remarks_500_005`*

```
-pandemic levels, even while our card customers have plenty of capacity to borrow. And importantly, because we're relation-based businesses, look at the right-hand slide at the bottom of page five. There you can see our deposit investment balances of our customers, who also have a card with us, remain 25% above their pre-pandemic levels, illustrating continued health of these customers. So if you think about consumer credit, the card charge-offs drive it, and they flattened out in terms of delinquencies, and we expect an improvement in the second-half. With regard to commercial real estate, our usual CRA credit exposure slide is included in our appendix. We continue to aggressively work through our loans in our modest CRA office portfolio. We saw a decrease in all the categories, a decrease in reservable criticized loans, a decrease in NPLs, and a decrease in net charge-offs. This supports our previous expectation that net charge-offs in the second-half of 2024 will be lower than the first-half of 2024. Our second quarter performance highlights Bank of America's ability to generate strong, sustainable growth through a combination of customer-centric strategies, innovation, strategic investments, and a commitment to a strong balance of risk and reward. We call that responsible growth. We're confident that focused approach will continue to drive long-term success and create value for you, our shareholders. Now I will turn it to Alistair for additional results.

Alastair Borthwick: Thank you, Brian, and I'm going to start on slide six of the earnings presentation. I'll touch on more highlights noted on slide six as we work through the material. I just want to say upfront that we delivered strong returns with return on average assets of 85 basis points and a return on tangible common equity of nearly 14%. So let's move to the balance sheet on slide seven, where you can see we ended the quarter at $3.26 trillion of total assets, relatively unchanged from the first quarter. And not much to note here apart from a mixed shift of lower securities balances, mostly offset by an increase in reverse repo and modest loan growth, as well as global markets client activity. On the funding side, deposits declined $36 billion on an ending basis, reflecting typical seasonal customer payments of income taxes. And as Brian noted, average deposits were still modestly higher. Liquid
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: Ch2 is BAC_2024_Q1 with the full Bank of America side — 16 office loans charged off, roughly one-third of office exposure reservable criticized, NCO ratio 58bps. Huntington never appears; PNC and WFC arrive instead.

---

## 48. `ref_comp_06` / `chunk500_dense`

- **condition:** chunk500_dense
- **arm:** text_only
- **question_id:** ref_comp_06
- **category:** comparative
- **case:** C
- **outcome label:** abstained
- **coverage group:** partial (some but not all) (coverage@5 = 0.5)

**Question:**

> How did Bank of America and Fifth Third each describe their operating leverage and the revenue growth behind it in the first quarter of 2023?

**Generated answer, verbatim:**

```
The provided context does not contain enough information to answer this question.
```

**Retrieved chunks (top 5), verbatim:**

*Rank 1 — `BAC_2023_Q4_prepared_remarks_500_002`*

```
2022. On that adjusted basis, we generated a 90 basis point return on assets and a 15% return on tangible common equity. The year 2023 was characterized by a record organic customer activity, record digital customer engagement levels and satisfaction scores, strong but slowing NII during the course of the year, strong sales and trading up 7% year-over-year, operating leverage reflected good expense discipline, solid asset quality and a strong capital and liquidity position. All this was helped by the years of Bank of America's assiduous dedication to responsible growth. This helped us bring our headcount and expense down every quarter during 2023, in line with what we told you to expect early this year -- early last year. Adjusted full year revenue grew 5% on the back of 9% NII improvement and strong asset management fees and sales and trading results. We achieved 170 basis points of operating leverage in 2023 as heightened quarterly expense levels were driven lower throughout the year even as the investments in growth continued. Net charge-offs moved higher through the year off the historic lows, but they still compare very favorably against historic averages. One last point worth noting is the level of deposits. If you think back as we ended 2022 and entered 2023, the great debate was how much the pandemic surge in deposits would dissipate. But looking today, we ended 2023 with $1.924 trillion of deposits, only $7 billion less than we had at year-end '22 and 4% higher than the trough in May of this year. The total deposits -- the total average deposits in the fourth quarter remained 35% higher than they did in the quarter four of 2019. This has been tremendous works by our teams to drive our industry-leading market share, actually outperforming the industry across the four-year period, and again this year. While the economy appears to continue to normalize and rates continue to have some volatility, one thing that remains important is driving that organic growth. This client activity sticks to the ribs is what we want to spend a moment as I wrap up. On Slide 3, we highlight some of the successes in organic activity in our results for the year. Bank of America team is a powerful engine that's fueling results across all our businesses. I would note a couple of examples to try and connect the importance to our financials. It's easy to use the consumer business as an
```

*Rank 2 — `FITB_2023_Q1_prepared_remarks_500_000`*

```
Chris Doll: Good morning everyone. Welcome to Fifth Third’s First Quarter 2023 Earnings Call. This morning our President and CEO, Tim Spence and CFO, Jamie Leonard will provide an overview of our first quarter results and outlook. Our Treasurer, Bryan Preston has also joined for the Q&A portion of the call. Please review the cautionary statements and our materials which can be found on our earnings release and presentation. These materials contain information regarding to the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third’s performance. These statements speak only as of April 20th 2023 and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Jamie, we will open the call up for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Chris. And good morning, everyone. Thank you for joining us today. The past six weeks have seen a great deal of volatility in the banking sector. Markets have been trading on narratives over fundamentals and the term regional bank has been used to describe such a broad cross section of business models that it has lost any real descriptive value. While we at Fifth Third take any instability in our sector very seriously, there was no crisis inside our four walls. We’ve been running the company with the expectation for a higher, for a longer rate environment for many quarters now. We’ve consistently communicated in these calls and at investor conferences. As our first quarter results demonstrate our balance sheet remains well fortified, and our capacity to generate strong profitability through the cycle is strong. Excluding items noted in the release, we reported earnings per share of $0.83, a 20% increase compared to the year ago quarter. We generated nine points of year-over-year positive operating leverage driven by an 18% increase in revenue. During the quarter we held average and period end deposits flat sequentially despite the industry wide impact of quantitative tightening and normal seasonal pressures. Our key credit metrics remain near historical lows with net charge-offs of 26 basis points coming in at the low end of our guidance range. NPAs NPLs and early stage delinquency ratios remained below normalized levels, and criticized assets decrease modestly during the quarter. Moreover, we accomplished all this while also being recognized by Ethisphere as one of only two U.S. banks on their world's most ethical companies
```

*Rank 3 — `FITB_2023_Q4_prepared_remarks_500_002`*

```
profitability. Expense discipline, strong returns, and positive operating leverage remain core areas of focus for Fifth Third. Supported by our technology modernization investments and a focus on leaning out key value streams, we reduced full-time equivalent employee headcount by 4% from our peak in 2023 to the end of the year without the need for a company-wide expense program. The run rate benefits of these efforts put us in a position to sustain the peer-leading annualized expense growth that we have averaged the past several years, even as we continue to invest for growth. While the carryover effect of the RWA diet makes it unfeasible for the full year, we do anticipate returning to positive operating leverage in the second half of 2024. The third point I'd like to highlight is about growth. Our strategies have been consistent, building out our Southeast markets, producing a strong fee to total revenue mix, and leveraging software that differentiates our product offerings and improves productivity. These are multi-year investments that cannot be replicated easily by competitors to one to two years of hiring a few new branches or small tuck-in acquisitions. In 2023, we opened 37 new branches concentrated in the Southeast, bringing us to 107 opened over the past five years. We plan to open another 31 branches in the Southeast in 2024. As a portfolio, these branches have continued to outperform our expectations on both household acquisition and deposit growth and should provide a tailwind for several years forward. We also continue to invest in treasury management, wealth and asset management, and capital markets. All three of these businesses grew for us in 2023. We expect mid-to-high single-digit growth in each in 2024. In treasury management, our acquisitions of Rize and Big Data Healthcare and the launch of Newline, our embedded payments business, should continue to support peer-leading performance. In wealth and asset management, Global Finance recently named our Private Bank as the Best US Regional Private Bank for the fifth consecutive year and Best Private Bank for Entrepreneurs globally for the first time. In our capital markets business, we have seen more robust activity levels to start the year, including an M&A pipeline that is 1.5 times the full-year revenue target embedded in our guidance. Overall, we expect 2024 to be a solid year of improving revenue trends and continued to expense discipline. Given what we believe to be a less certain outlook than the markets would imply,
```

*Rank 4 — `FITB_2023_Q4_prepared_remarks_500_000`*

```
Operator: Hello and welcome to the Q4 2023 Fifth Third Bancorp Earnings Conference Call. All lines have been placed on mute to prevent any background noise. After the speakers' remarks, there will be a question-and-answer session. [Operator Instructions] I'll now turn the conference over to Matt Curoe, Director of Investor Relations. Please go ahead.

Matt Curoe: Good morning, everyone, and welcome to the Fifth Third's Fourth Quarter 2023 Earnings Call. This morning our Chairman, President, and CEO, Tim Spence; and CFO, Bryan Preston will provide an overview of our fourth quarter results and outlook; our Chief Operating Officer, Jamie Leonard and Chief Credit Officer, Greg Schroeck have also joined for the Q&A portion of the call. Please review the cautionary statements in our materials, which can be found in our earnings release and presentation. These materials contain information regarding the use of non-GAAP measures and reconciliations to the GAAP results, as well as forward-looking statements about Fifth Third's performance. These statements speak only as of January 19, 2024, and Fifth Third undertakes no obligation to update them. Following prepared remarks by Tim and Bryan, we will open up the call for questions. With that, let me turn it over to Tim.

Timothy Spence: Thanks, Matt, and good morning everyone. At Fifth Third, we believe that great banks distinguish themselves based on how they navigate challenging and uncertain operating environment. 2023 was certainly a challenging year for the industry, but I am very pleased with how we measured up. A defensive balance sheet positioning, strong execution, and multiyear strategic investments produce top-quartile profitability, the best core deposit growth, and the best total shareholder return among all regional peers who did not participate in an FDIC-assisted transaction. We generated an all-time record full-year revenue of $8.7 billion. Deposits grew 5% compared to an industry-wide decline of 3%. Credit performance was strong with net charge-offs remaining below historical averages. And although it would be foolish to expect it to repeat forever, in commercial real estate we experienced zero net charge-offs in 2023 and only two basis points in delinquent loans as of early January. These strong outcomes combined with our multi-year expense discipline produced a full-year adjusted return on assets of 1.25% and adjusted return on tangible common equity ex-
```

*Rank 5 — `FITB_2023_Q3_prepared_remarks_500_001`*

```
among peers, despite also investing in growth by building more new branches, raising our minimum wage, modernizing our technology platforms, and acquiring four fintech companies. Expense management at Fifth Third is a continuous process and not a program. Since March of this year, full-time equivalent employee headcount is down 3.5%.  Turning to the balance sheet, we generated 4% average deposit growth compared to the year ago quarter versus a 5% decline for the industry. New relationship growth remains strong. Consumer households grew more than 2%, led by 6% growth in the Southeast, a continuation of our multi-year growth base. New middle market relationships added year-to-date remain 25% ahead of last year's record base.  Thanks to the release of the annual FDIC summary of deposits, the third quarter provides a unique opportunity to understand market share gains and losses on a metro area by metro area basis. This year, Fifth Third maintained or improved our market rank in every single one of our 40 largest MSAs.  In the Midwest, we maintained our #2 overall position behind JPMorgan Chase. In the Southeast, where we are just 4 years removed for opening our first next-gen branch, we have reached or are approaching target locational share in 8 of our original 11 focused markets. We intend to continue to open approximately 35 branches per year through 2028, at which time nearly 50% of our branches will be in Southeast markets. These market share gains are the byproduct of multiyear strategies that are not easily replicable by competitors. They include innovative operational deposit-oriented products like Momentum Banking, AI-driven customer acquisition strategies and the top quartile customer service model in addition to our investments in new branches.  Our key credit metrics remained strong during the quarter. Charge-offs were in line with our July expectations in both early stage delinquencies and non-performing assets improved sequentially. The ACL increased 3 basis points given slight changes to Moody's macroeconomic forecast.  Turning to liquidity and capital. We made significant progress against our goal to adapt early to expected changes in the regulatory framework. Our focused efforts throughout the bank enabled us to end the quarter with $103 billion in total liquidity sources and to achieve full Category 1 LCR compliance at the end of both August and September. During the quarter, we also made significant progress on our RWA optimization initiative. Total RWA declined 1% compared to the prior quarter
```

verdict: correct abstention

failure mode: all-or-nothing on conjunctive questions (holds one side, declines the whole)

notes: Ch2 is the same FITB_2023_Q1 chunk as item 33, with the nine-points/18% sentence intact. Bank of America's Q1 2023 is again absent. Same question, different condition, same correct decline.

---

