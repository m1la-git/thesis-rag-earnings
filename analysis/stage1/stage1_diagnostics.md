# Stage 1 retrieval diagnostics

Investigation only — no code, benchmark, corpus, or chunking changes made in this pass.
All numbers below come from the persisted grid in `results/retrieval/*.jsonl` (the run
committed nothing changes retrieval behaviour) plus read-only inspection of the code and
the frozen corpus/benchmark. Where a script was needed to compute something, it ran
existing functions from `src/` unmodified.

**Bottom line up front:** all 7 plumbing checks in Part 2 pass, with evidence, not just
a conclusion. But the ceiling analysis in Part 3 does **not** cleanly confirm "the top-5
window is the binding constraint" as the single explanation for low coverage. It reveals
two distinct effects, and the larger of the two is not a top-5-window story — see the
verdict at the end before deciding whether to commit.

---

## Corpus scale (context for interpreting top-5-of-N)

| chunk_size | total chunks (128 transcripts) | mean chunks / transcript |
|---|---|---|
| 200 | 7,918 | 61.9 |
| 500 | 3,239 | 25.3 |

Every question retrieves against the **entire 128-transcript corpus** (`retrieval_scope:
"corpus"`, per `configs/base.json` and its explicit rationale — scoping to a
question's own transcripts would make retrieval trivial). So "top-5" is 5 slots out of
~7,900 (200-token) or ~3,200 (500-token) candidates, most of which are earnings-call
boilerplate that recurs, near-verbatim, across 16 companies × 8 quarters.

---

## Part 1 — Numbers from the persisted grid

### anchor_coverage_at_5 and MRR@5, by condition × category

| condition | category | n | coverage@5 | MRR@5 |
|---|---|--:|--:|--:|
| chunk200_bm25 | factual | 14 | 0.214 | 0.110 |
| chunk200_bm25 | thematic | 15 | 0.067 | 0.019 |
| chunk200_bm25 | comparative | 11 | 0.091 | 0.068 |
| chunk200_dense | factual | 14 | 0.143 | 0.086 |
| chunk200_dense | thematic | 15 | 0.056 | 0.024 |
| chunk200_dense | comparative | 11 | 0.045 | 0.015 |
| chunk200_hybrid | factual | 14 | **0.286** | 0.171 |
| chunk200_hybrid | thematic | 15 | 0.067 | 0.044 |
| chunk200_hybrid | comparative | 11 | 0.136 | 0.049 |
| chunk500_bm25 | factual | 14 | 0.214 | 0.121 |
| chunk500_bm25 | thematic | 15 | 0.033 | 0.011 |
| chunk500_bm25 | comparative | 11 | 0.182 | 0.098 |
| chunk500_dense | factual | 14 | 0.071 | 0.024 |
| chunk500_dense | thematic | 15 | 0.100 | 0.078 |
| chunk500_dense | comparative | 11 | 0.182 | 0.129 |
| chunk500_hybrid | factual | 14 | 0.143 | 0.107 |
| chunk500_hybrid | thematic | 15 | 0.100 | 0.083 |
| chunk500_hybrid | comparative | 11 | 0.182 | 0.145 |

**Expected-shape check (factual materially higher than thematic):** holds in 5 of 6
conditions. The exception is `chunk500_dense` (factual 0.071 < thematic 0.100) — with
n=14/15 that's a 1–2-question swing either way, plausible sampling noise rather than a
signal, but noted rather than smoothed over.

### By `chunk_size_sensitive`

| condition | sensitive | n | coverage@5 | MRR@5 |
|---|---|--:|--:|--:|
| chunk200_bm25 | True | 7 | 0.214 | 0.046 |
| chunk200_bm25 | False | 33 | 0.106 | 0.068 |
| chunk200_dense | True | 7 | 0.262 | 0.194 |
| chunk200_dense | False | 33 | 0.045 | 0.011 |
| chunk200_hybrid | True | 7 | 0.357 | 0.243 |
| chunk200_hybrid | False | 33 | 0.121 | 0.058 |
| chunk500_bm25 | True | 7 | 0.000 | 0.000 |
| chunk500_bm25 | False | 33 | 0.167 | 0.089 |
| chunk500_dense | True | 7 | 0.071 | 0.071 |
| chunk500_dense | False | 33 | 0.121 | 0.073 |
| chunk500_hybrid | True | 7 | 0.214 | 0.143 |
| chunk500_hybrid | False | 33 | 0.121 | 0.102 |

### Distribution of per-question coverage@5 within each category

Format: `value:count`. Achievable levels differ by question (1, 2 or 3 anchors), so the
same coverage value means different things across rows — read counts, not the value set,
as comparable.

| condition | category | n | distribution |
|---|---|--:|---|
| chunk200_bm25 | factual | 14 | 0.0:11, 1.0:3 |
| chunk200_bm25 | thematic | 15 | 0.0:13, 0.5:2 |
| chunk200_bm25 | comparative | 11 | 0.0:9, 0.5:2 |
| chunk200_dense | factual | 14 | 0.0:12, 1.0:2 |
| chunk200_dense | thematic | 15 | 0.0:13, 0.33:1, 0.5:1 |
| chunk200_dense | comparative | 11 | 0.0:10, 0.5:1 |
| chunk200_hybrid | factual | 14 | 0.0:10, 1.0:4 |
| chunk200_hybrid | thematic | 15 | 0.0:13, 0.5:2 |
| chunk200_hybrid | comparative | 11 | 0.0:8, 0.5:3 |
| chunk500_bm25 | factual | 14 | 0.0:11, 1.0:3 |
| chunk500_bm25 | thematic | 15 | 0.0:14, 0.5:1 |
| chunk500_bm25 | comparative | 11 | 0.0:7, 0.5:4 |
| chunk500_dense | factual | 14 | 0.0:13, 1.0:1 |
| chunk500_dense | thematic | 15 | 0.0:12, 0.5:3 |
| chunk500_dense | comparative | 11 | 0.0:7, 0.5:4 |
| chunk500_hybrid | factual | 14 | 0.0:12, 1.0:2 |
| chunk500_hybrid | thematic | 15 | 0.0:12, 0.5:3 |
| chunk500_hybrid | comparative | 11 | 0.0:7, 0.5:4 |

No thematic or comparative question ever hits full coverage (all its anchors) in any
condition — every non-zero thematic/comparative score is partial. That's consistent with
the intended design (3-anchor thematic questions need all 3 specific chunks in the top 5)
but worth naming explicitly: at this corpus scale, full multi-anchor coverage essentially
never happens.

---

## Part 2 — Plumbing checks

| # | Check | Verdict |
|---|---|---|
| 1 | BGE query-prefix asymmetry | **PASS** |
| 2 | Embedding truncation | **PASS** |
| 3 | Normalisation / index geometry | **PASS** |
| 4 | BM25 tokenisation | **PASS** (self-consistent, see caveat below) |
| 5 | Anchor-to-chunk mapping | **PASS** |
| 6 | Query construction | **PASS** |
| 7 | Index/chunk-set identity | **PASS** |

### 1. BGE query-prefix asymmetry — PASS

Code (`src/index.py`): `embed_chunks` calls `model.encode(texts, ...)` with no prefix;
`embed_query` calls `model.encode(QUERY_PREFIX + query, ...)`.

Empirical (same sample text through both paths):

| comparison | cosine sim | expected |
|---|--:|---|
| `embed_chunks(text)` vs `embed_query(text)` | 0.9666 | < 1.0 (must differ) |
| `embed_query(text)` vs manual `encode(PREFIX+text)` | 1.0000001 | ≈ 1.0 (prefix *is* applied to queries) |
| `embed_chunks([text])` vs manual `encode(text)`, no prefix | 1.0000000 | ≈ 1.0 (chunks get *no* prefix) |
| `embed_query(text)` vs manual `encode(text)`, no prefix | 0.9666 | < 1.0 (query embedding ≠ bare embedding) |

Both directions of the asymmetry are confirmed at runtime, not just read from source.

### 2. Embedding truncation — PASS

`model.max_seq_length = 512`, tokenizer `model_max_length = 512`.

| chunk_size | n chunks | n_tokens min/mean/median/max | chunks where n_tokens+2 > 512 |
|---|--:|---|--:|
| 200 | 7,918 | 2 / 196.7 / 200 / 200 | 0 |
| 500 | 3,239 | 2 / 480.8 / 500 / 500 | 0 |

Cross-checked the 5 largest chunks at each size by re-tokenizing the actual stored
`text` with the SentenceTransformer's own tokenizer, `add_special_tokens=True` (what
`encode()` actually does): 500-token chunks land at exactly 502 tokens including
CLS/SEP, comfortably under the 512 cap. No chunk is silently truncated at either
chunk_size; this specifically clears the 500-token condition of a truncation confound.

### 3. Normalisation / index geometry — PASS

`build_faiss_index` uses `IndexFlatIP` (inner product) with the docstring claim that
this equals cosine because embeddings are pre-normalized. Verified directly:

- `||chunk_vec|| = 1.000000`, `||query_vec|| = 1.000000` for the sample text
- 20 further chunk embeddings: min/max/mean norm all exactly `1.000000`

Both sides of the index get the same normalization treatment; inner product and cosine
coincide as claimed.

### 4. BM25 tokenisation — PASS, with a characteristic worth naming

`tokenize_for_bm25` is `re.findall(r"[a-z0-9]+", text.lower())` — strips `$`, `%`,
hyphens, and decimal points, so `"$48.8 trillion"` becomes tokens `48`, `8`, `trillion`
and `"year-over-year"` becomes `year`, `over`, `year`. This is applied identically to
the query and to chunk text (same function, same call site both sides — see check 6), so
it is internally self-consistent: whatever a number becomes on one side, it becomes the
same thing on the other.

Four factual examples (question tokens ∩ anchor tokens):

| id | question→anchor token overlap |
|---|---|
| ref_fact_01 | administration, and, assets, custody, of, under, were |
| ref_fact_02 | eps, full, guidance, to, year |
| ref_fact_03 | of, the *(only stopwords — see below)* |
| ref_fact_04 | fees, management, on, were, year |

**Caveat, not a bug:** for `ref_fact_03` ("How much did Morgan Stanley report in
advisory revenues...?" / anchor `"$638 million, benefiting from..."`), the dollar figure
that answers the question is never in the question text — the question asks "how much,"
the anchor states the number. BM25 can only find that chunk via the surrounding entity/
topic terms (Morgan Stanley, advisory, revenues, quarter), not the figure itself. This is
inherent to how these questions are phrased, not a tokenizer defect — flagging it because
it partly explains factual-category misses independent of anything in Part 2.

### 5. Anchor-to-chunk mapping — PASS

Printed the full containing chunk, both chunk sizes, for 3 factual + 2 thematic + 2
comparative anchors (7 anchors, 12 transcript-anchor pairs since thematic/comparative
span multiple transcripts). All 12 are topically correct — the containing chunk is
visibly the right passage (e.g. `ref_fact_01`'s $48.8T anchor sits inside BNY Mellon's
consolidated-results paragraph; `ref_comp_02`'s office-portfolio anchor sits inside
Huntington's Q&A answer about the office book) — no boundary artifacts, no chunk that
merely happens to contain the string out of context. Full transcript excerpts are in the
scratchpad run log if needed; omitted here for length.

### 6. Query construction — PASS

`run_experiment.py`'s only call site: `retrieve_mod.retrieve(q["question"], strategy,
faiss_index, bm25_index, chunks, k=depth_cap)` — the literal benchmark `question` string,
nothing appended. `retrieve_dense` passes `query` straight to `embed_query`;
`retrieve_bm25` passes it straight to `tokenize_for_bm25`. No metadata, category label,
or transcript_id is concatenated anywhere in the path. Confirmed by reading both call
sites and printing the exact 5 sample strings sent (e.g. `ref_fact_05`: `"How large was
the Walmart-related build that Capital One called out as an adjusting item in the second
quarter of 2024?"` — question text only).

### 7. Index/chunk-set identity — PASS

Built the chunk set two ways and compared: (a) the full 128-transcript corpus chunking
`run_experiment.build_corpus_chunks` actually uses, filtered down to the 53 transcripts
the 40 scored questions reference; (b) the anchor-reachability check's own chunking,
which only ever processes those 53 transcripts. Chunking is per-transcript and stateless,
so these should be identical if both paths call the same functions the same way.

| chunk_size | (a) chunk_ids | (b) chunk_ids | ids identical | full content (id+text) hash identical |
|---|--:|--:|---|---|
| 200 | 3,464 | 3,464 | True | True |
| 500 | 1,410 | 1,410 | True | True |

Also confirmed `run_meta.n_corpus_chunks` is identical across all 3 strategies sharing a
chunk_size (7,918 @200 for bm25/dense/hybrid; 3,239 @500 for all three) — the single
per-size index build is genuinely being reused, not silently rebuilt per condition.

---

## Part 3 — Ceiling analysis (from the logged 50-deep rankings)

### coverage@k, by condition × category

| condition | category | n_anchors | cov@5 | cov@10 | cov@20 | cov@50 |
|---|---|--:|--:|--:|--:|--:|
| chunk200_bm25 | factual | 14 | 0.214 | 0.429 | 0.500 | 0.571 |
| chunk200_bm25 | thematic | 38 | 0.053 | 0.079 | 0.105 | 0.132 |
| chunk200_bm25 | comparative | 22 | 0.091 | 0.091 | 0.227 | 0.409 |
| chunk200_dense | factual | 14 | 0.143 | 0.214 | 0.214 | 0.429 |
| chunk200_dense | thematic | 38 | 0.053 | 0.105 | 0.184 | 0.316 |
| chunk200_dense | comparative | 22 | 0.045 | 0.136 | 0.227 | 0.364 |
| chunk200_hybrid | factual | 14 | 0.286 | 0.357 | 0.429 | 0.643 |
| chunk200_hybrid | thematic | 38 | 0.053 | 0.132 | 0.184 | 0.342 |
| chunk200_hybrid | comparative | 22 | 0.136 | 0.182 | 0.182 | 0.409 |
| chunk500_bm25 | factual | 14 | 0.214 | 0.286 | 0.286 | 0.429 |
| chunk500_bm25 | thematic | 38 | 0.026 | 0.079 | 0.132 | 0.342 |
| chunk500_bm25 | comparative | 22 | 0.182 | 0.227 | 0.318 | 0.500 |
| chunk500_dense | factual | 14 | 0.071 | 0.214 | 0.357 | 0.429 |
| chunk500_dense | thematic | 38 | 0.079 | 0.105 | 0.211 | 0.289 |
| chunk500_dense | comparative | 22 | 0.182 | 0.227 | 0.318 | 0.409 |
| chunk500_hybrid | factual | 14 | 0.143 | 0.357 | 0.429 | 0.571 |
| chunk500_hybrid | thematic | 38 | 0.079 | 0.184 | 0.263 | 0.368 |
| chunk500_hybrid | comparative | 22 | 0.182 | 0.273 | 0.409 | 0.455 |

(n_anchors counts each anchor once per question it belongs to, so thematic/comparative —
which have 2–3 anchors per question — show n=38/22 rather than 15/11.)

Note the anchor-level `mean(anchor rank ≤ k)` figures here are not identical to the
per-question `anchor_coverage_at_5` averages in Part 1 (which average *within* a question
first) — both are legitimate views; this table answers "how deep do we have to go," Part
1 answers "how well does a typical question do."

### Rank distribution of first match, by condition (all 74 anchors)

| condition | matched@50 | unmatched@50 | median rank | Q1 | Q3 | matched but missed top-5 (rank 6–50) |
|---|--:|--:|--:|--:|--:|--:|
| chunk200_bm25 | 22 | **52** | 10.0 | 4 | 30 | 15 |
| chunk200_dense | 26 | **48** | 19.0 | 7 | 38 | 21 |
| chunk200_hybrid | 31 | **43** | 15 | 5 | 33 | 22 |
| chunk500_bm25 | 30 | **44** | 18.5 | 5 | 33 | 22 |
| chunk500_dense | 26 | **48** | 11.5 | 3 | 18 | 18 |
| chunk500_hybrid | 32 | **42** | 9.0 | 5 | 19 | 23 |

**This is the finding that complicates the original hypothesis.** Only 22–32 of the 74
anchors (30–43%) are found *anywhere* in the top 50 out of ~3,200–7,900 candidates, in
any given condition. 42–52 anchors per condition are not surfaced at all within depth 50.
Two effects are present simultaneously, and they are not the same size:

- **A genuine top-5-window effect** — 15–23 anchors per condition *are* found by depth
  50 but miss the top 5. This part of the hypothesis holds.
- **A larger "not found even at depth 50" effect** — 42–52 anchors per condition, roughly
  60–70% of all anchors, aren't in the ranking at all even 10x deeper than the scored
  window. This is *not* a top-5-window story; something else is capping recall before
  rank 50 is even reached.

Per-category breakdown (same data, split by category) shows the unmatched-at-50 share is
worst for thematic questions specifically (`chunk200_bm25`: 33 of 38 thematic anchors
never surface in the top 50) — consistent with thematic questions needing 2–3 *specific*
company/quarter chunks on a topic many other companies also discuss.

### Why: concrete inspection of unmatched-at-50 cases

Pulled the actual top-10 retrieved chunks (from the logged ranking, no re-run) for
`ref_them_01` ("How did banks report the impact of the FDIC special assessment...") under
`chunk200_bm25` and `chunk200_dense`. The gold anchors point at COF_2023_Q4, BAC_2024_Q2,
and BK_2023_Q4. Neither condition surfaces any of the 3 target chunks within the top 10
— but the top 10 in both cases is **not off-topic**: BM25's top 10 includes MTB, JPM,
C, WFC, BAC(Q4, not Q2), and GS all discussing quarterly expense levels; dense's top 10
even includes `BAC_2024_Q4_prepared_remarks_200_018` and `BK_2024_Q4_prepared_remarks
_200_015`, i.e. the **same two companies as two of the gold anchors, one quarter off**,
plus `FITB_2023_Q2_...` explicitly mentioning "the increased FDIC assessment."

Every one of the 16 banks in the corpus discussed the FDIC special assessment (it was an
industry-wide one-time charge in this exact window), so the corpus contains on the order
of a dozen-plus near-duplicate "we took a charge for the FDIC special assessment" chunks
competing for 5 (or even 50) slots — and the annotator's 3 chosen transcripts are just 3
specific instances among many structurally similar ones. The retriever isn't confused or
broken; it's correctly finding *a* right-topic chunk, often from a right-company
wrong-quarter chunk, and the correct instance is crowded out by volume of near-duplicates,
not by a retrieval defect.

`ref_them_02` (Basel III) shows a second, related pattern: dense's top 10 includes
**four different chunks from JPM_2023_Q3 itself** (ranks 1, 5, 6, 9) — the correct
transcript — none of which is `JPM_2023_Q3_prepared_remarks_200_003`, the one chunk that
actually contains the annotated anchor sentence. JPM's own transcript devotes several
consecutive chunks to Basel III ("we added a couple of pages on it"); the retriever finds
the right transcript and the right topic repeatedly, just not the one specific sentence
the annotator anchored on, among several equally on-topic candidates from the same
transcript.

Both are real, characterizable retrieval-difficulty effects tied to this corpus's design
(16 same-sector companies, repeatedly discussing the same industry-wide events in similar
language) — not evidence of a bug. But they are a different phenomenon from "right passage,
just outside top 5," and should be named as such rather than folded into the top-5-window
narrative.

### Anchors matched at any depth (of 74), per condition

| condition | matched anywhere ≤50 |
|---|---|
| chunk200_bm25 | 22/74 |
| chunk200_dense | 26/74 |
| chunk200_hybrid | 31/74 |
| chunk500_bm25 | 30/74 |
| chunk500_dense | 26/74 |
| chunk500_hybrid | 32/74 |

Anchor reachability (Part 2 context) already proved all 74 anchors exist in some single
chunk; this table is the retrieval side of the question, and it's a much lower number
than 74 in every condition.

---

## Part 4 — Strategy contrast on the same anchors

### Counts: one strategy misses top-5, another catches it (within the same chunk_size)

| chunk_size | dense misses, BM25 catches | BM25 misses, dense catches | dense misses, hybrid catches | BM25 misses, hybrid catches |
|---|--:|--:|--:|--:|
| 200 | 4 | 2 | 5 | 3 |
| 500 | 4 | 4 | 3 | 4 |

### Examples (chunk_size=200)

**Dense misses top-5, BM25 catches it:**

| question | anchor (truncated) | dense rank | BM25 rank |
|---|---|--:|--:|
| ref_fact_01 | custody and our administration of $48.8 trillion... | 42 | 5 |
| ref_fact_05 | quarter, as you said, first, we had the effect of Walmart... | unmatched@50 | 1 |
| ref_them_02 | pace of buybacks will likely remain modest in light of the Basel III | 19 | 3 |
| ref_comp_06 | nine points of year-over-year positive operating leverage... | 20 | 1 |

**BM25 misses top-5, dense catches it:**

| question | anchor (truncated) | BM25 rank | dense rank |
|---|---|--:|--:|
| ref_fact_12 | our strong fee-based revenue growth, up 15%... | 6 | 1 |
| ref_them_15 | themes, technology spend was $3 billion in the quarter... | unmatched@50 | 3 |

### Does hybrid dominate the union of dense and BM25? — No, it trades off

This is the part the summary claim needs quantified rather than asserted:

| chunk_size | union(dense, bm25) hit@5 | hybrid hit@5 | anchors union caught that hybrid then LOSES |
|---|--:|--:|--:|
| 200 | 9 | 9 | 2 |
| 500 | **12** | **9** | 5 |

At chunk_size=500, hybrid (9) is strictly *worse* than simply taking whichever of dense
or BM25 caught each anchor (12) — RRF fusion dilutes a strong single-strategy signal by
averaging in the other strategy's weak one for that specific anchor. Concrete example:
`ref_fact_05` at 500 tokens — BM25 alone ranks it **1**, dense doesn't find it in 50, and
hybrid's fused rank is **7** (a miss), because dense's near-total absence pulls the fused
rank down even though BM25 alone nailed it. Four more such cases at 500 tokens
(`ref_fact_08`, `ref_fact_10`, `ref_them_07`, plus the one above), two at 200 tokens
(`ref_them_02`, `ref_them_15`).

So: hybrid *does* recover some anchors neither single strategy catches (2 at 200, 2 at
500 — real, but smaller than the headline "recovers dense's misses" framing suggested),
and it *also* loses some anchors that one single strategy had outright. Net effect on
`hit@5` count is a wash at 200 tokens and a net loss at 500 tokens, in this specific
40-question, 74-anchor sample. This is worth stating plainly rather than repeating the
earlier, unquantified "BM25/hybrid recovers dense's misses" claim as-is.

---

## Verdict

**Part 2 (plumbing): 7/7 PASS**, each with runtime evidence, not just a code read. The
BGE prefix is applied to queries and withheld from chunks in both directions; no chunk is
truncated at either chunk_size; embeddings and the FAISS index are both correctly
normalized; BM25 tokenizes query and chunk text identically; every inspected anchor sits
in a topically correct chunk; the exact question string (nothing else) reaches both
retrievers; and the chunk set the retriever searches is byte-identical to the one the
reachability check validated. No bug surfaced.

**Part 3 (ceiling) does not simply confirm "top-5 window is the binding constraint."**
It confirms that story for a minority of misses (15–23 anchors per condition, out of 74,
are found by depth 50 but outside top 5 — genuinely a top-5-window effect). But the
majority of misses — 42–52 anchors per condition, 60–70% — are not found even at depth
50, and that is a different, larger effect: this 16-company, single-sector corpus
contains many near-duplicate mentions of the same industry-wide events (FDIC special
assessment, Basel III, buybacks, CET1) across companies and quarters, so the specific
annotated instance competes against a field of structurally similar competitors for
placement, deep past rank 50 in most cases. Concretely demonstrated on two thematic
questions where the top-10 in every failing condition is topically on-target (often the
right company, wrong quarter, or the right transcript, wrong chunk) rather than
off-topic — the retriever isn't malfunctioning, it's discriminating among near-duplicates
at a difficulty this corpus design produces by construction.

**Part 4 quantifies the hybrid claim rather than asserting it:** hybrid does recover a
handful of anchors neither single strategy catches (2 per chunk_size), but it also drops
anchors a single strategy caught outright (2 at 200 tokens, 5 at 500 tokens) — a net wash
or net loss on raw hit@5 count in this sample, not a clean "hybrid recovers the union."

**Recommendation:** no plumbing bug to fix — Stage 1's retrieval/scoring pipeline is
doing what it's supposed to. The low headline coverage numbers are real and explainable,
but the explanation is "this corpus has heavy cross-company topical redundancy under
full-corpus retrieval scope," not purely "the top-5 window is too narrow." That's a
finding worth stating in the thesis in those terms — and a materially different framing
than the one-line "dense misses, BM25/hybrid recovers" hypothesis this diagnostic pass
was launched to check. Decision on committing Stage 1 as-is is yours to make with this
picture in hand.

---

# Follow-up diagnostics (Parts 5–6)

Second investigation-only pass, same rules as above: no code, config, benchmark, corpus,
or chunking changes. Everything below is derived from the persisted grid
(`results/retrieval/*.jsonl`) and read-only inspection of the code and frozen corpus.

## Part 5 — Is the discriminating information in the indexed text at all?

### 5.1 What actually gets indexed (both retrievers, verbatim)

Three sample chunks from `BK_2024_Q1`, chunk_size=200:

| chunk_id | metadata on the chunk RECORD | string passed to `model.encode()` | tokens passed to `BM25Okapi` |
|---|---|---|---|
| `BK_2024_Q1_prepared_remarks_200_000` | company="The Bank of New York Mellon Corporation", ticker="BK", date="2024-04-16", year=2024, quarter=1, section="prepared_remarks" | `"Operator: Good morning and welcome to the 2024 First Quarter Earnings Conference Call hosted by BNY Mellon. At this time..."` | `['operator','good','morning','and','welcome','to','the','2024','first','quarter','earnings','conference','call','hosted','by','bny','mellon',...]` |
| `BK_2024_Q1_prepared_remarks_200_001` | same metadata | `"looking statements and non-GAAP measures. Actual results may differ materially..."` | `['looking','statements','and','non','gaap','measures','actual','results','may','differ',...]` |
| `BK_2024_Q1_prepared_remarks_200_002` | same metadata | `"year provided a mostly constructive operating environment with global markets..."` | `['year','provided','a','mostly','constructive','operating','environment',...]` |

**Both retrievers index exactly `c["text"]` and nothing else** — confirmed by reading the
call sites (`index.embed_chunks`: `texts = [c["text"] for c in chunks]`;
`index.build_bm25_index`: `tokenized = [tokenize_for_bm25(c["text"]) for c in chunks]`).
`company`, `ticker`, `date`, `year`, `quarter`, `section`, `speakers` are all present as
keys on the chunk **record** (used for filtering/logging/metadata elsewhere) but **none
of them is concatenated into the string either retriever actually sees**. This is
identical for BM25 and dense — they don't differ on this point, only on how they process
the same bare `c["text"]`.

The first sample chunk is the lucky case: it's chunk 0 of the call, so it happens to
contain the operator's scripted "welcome to the 2024 First Quarter Earnings Conference
Call hosted by BNY Mellon" line, which mentions both company and quarter. That's a
property of being chunk 0, not something structural — chunks 1 and 2 immediately after
it contain neither company nor quarter reference at all.

### 5.2 Proportion of the 74 gold chunks containing company / period signal

Methodology: for each of the 74 (question, anchor) pairs, the containing chunk was
identified per chunk_size (same method as Part 2 check 5). `company_match` = a
hand-curated alias for the transcript's ticker (e.g. BK → "BNY Mellon" / "Bank of New
York Mellon" / "BNY") appears in the chunk text, case-insensitive. `period_match` = an
ordinal-quarter phrase matching the transcript's actual quarter ("first quarter" for Q1,
etc.), a `Qn` token, or the quarter-end month name appears in the chunk text. This is a
heuristic, not an exhaustive check — reported as a lower bound, and transparently so.

| chunk_size | category | n | company% | period% | both% |
|---|---|--:|--:|--:|--:|
| 200 | factual | 14 | 21.4% | 35.7% | 7.1% |
| 200 | thematic | 38 | 18.4% | 44.7% | 7.9% |
| 200 | comparative | 22 | 18.2% | 50.0% | 13.6% |
| 200 | **ALL** | 74 | **18.9%** | **44.6%** | **9.5%** |
| 500 | factual | 14 | 21.4% | 57.1% | 14.3% |
| 500 | thematic | 38 | 31.6% | 71.1% | 21.1% |
| 500 | comparative | 22 | 31.8% | 68.2% | 27.3% |
| 500 | **ALL** | 74 | **29.7%** | **67.6%** | **21.6%** |

(n counts each anchor once per its own question — thematic/comparative have 2–3 anchors
per question, hence n=38/22 rather than 15/11, matching Part 3's convention.)

At 200 tokens, fewer than 1 in 5 gold chunks even mentions the company by name, and fewer
than 1 in 10 has **both** company and quarter. Company mentions are structurally rare in
these transcripts: a company's own name is typically said once, by the operator, at the
very top of the call — after that, speakers say "we," "our," "this quarter," not the
company name. A 200-token slice from the middle of a 60+-chunk transcript has a real
chance of catching neither. Doubling chunk length to 500 tokens roughly doubles both
rates (30% company, 68% period) simply by covering more surrounding text, but even then
under a quarter of gold chunks carry both signals.

### 5.3 Consequence: does missing company/period actually cost rank?

Split each chunk_size's 74 gold chunks into "neither" (no company, no period in the
indexed text) vs. "at least one," then compare retrieval outcomes for that same set of
anchors under each strategy.

**chunk_size=200** (34 "neither" / 40 "at least one"):

| strategy | group | n | matched@50 | matched@50 rate | hit@5 | hit@5 rate | median rank (matched) |
|---|---|--:|--:|--:|--:|--:|--:|
| bm25 | neither | 34 | 7 | 20.6% | 2 | 5.9% | 17 |
| bm25 | at-least-one | 40 | 15 | 37.5% | 5 | 12.5% | 6 |
| dense | neither | 34 | 9 | 26.5% | 1 | 2.9% | 30 |
| dense | at-least-one | 40 | 17 | 42.5% | 4 | 10.0% | 17 |
| hybrid | neither | 34 | 12 | 35.3% | 2 | 5.9% | 31.5 |
| hybrid | at-least-one | 40 | 19 | 47.5% | 7 | 17.5% | 15 |

Consistent across all 3 strategies at 200 tokens: the "at least one" group is found more
often (higher matched@50 rate), ranks higher when found (lower median rank), and lands in
the top 5 roughly 2–3x as often as the "neither" group.

**chunk_size=500** (18 "neither" / 56 "at least one"):

| strategy | group | n | matched@50 | matched@50 rate | hit@5 | hit@5 rate | median rank (matched) |
|---|---|--:|--:|--:|--:|--:|--:|
| bm25 | neither | 18 | 6 | 33.3% | 2 | 11.1% | 8.0 |
| bm25 | at-least-one | 56 | 24 | 42.9% | 6 | 10.7% | 21.5 |
| dense | neither | 18 | 4 | 22.2% | 1 | 5.6% | 12.5 |
| dense | at-least-one | 56 | 22 | 39.3% | 7 | 12.5% | 11.5 |
| hybrid | neither | 18 | 6 | 33.3% | 2 | 11.1% | 7.0 |
| hybrid | at-least-one | 56 | 26 | 46.4% | 7 | 12.5% | 10.0 |

At 500 tokens the matched@50-rate gap persists in the same direction (at-least-one always
higher) but is smaller, and the hit@5-rate gap mostly closes (bm25 even reverses,
11.1% vs 10.7%, within noise at n=18). Two things dilute the signal at 500 tokens: (a)
the "neither" group shrinks to 18 anchors, so single-anchor swings move the rate a lot;
(b) longer chunks carry more surrounding context regardless of company/period mentions,
which helps the "neither" group too and narrows the gap.

### 5.4 Reading

Company and period are attached to every chunk **record** but never enter the string
either retriever indexes. For the 40–43% (200-token) to 68–70% (500-token) of gold chunks
missing one or both signals, no retrieval strategy — dense, BM25, or hybrid — has any
lexical or semantic access to the one piece of information that would disambiguate the
correct instance from ~127 other structurally similar company-quarters. The presence of
company/period text is **necessary but not sufficient**: even the "at-least-one" group
only reaches 10–17.5% hit@5, because (a) many *other* chunks in the corpus also happen to
mention *a* company and *a* quarter (just not the right one), and (b) neither retriever
weights a company-name token any differently than a topic-word token — it's one token
among ~200–500 competing on equal footing.

This is a **cleaner and more defensible finding than "topical redundancy"**, exactly as
you anticipated: it's not merely that the corpus discusses similar things repeatedly, but
that the one piece of text that would let a retriever discriminate among those similar
things is frequently **absent from the indexed representation by construction** — a
property of the chunking/indexing design (verbatim text only, no metadata injection),
not a defect in any one retriever. No strategy choice among dense/BM25/hybrid can fix a
signal that isn't in the text to begin with; this sets a structural ceiling that is
largely independent of the retrieval-strategy variable, which is itself a relevant
finding for the RQ1 write-up.

---

## Part 6 — Are the six conditions actually distinguishable?

> **SUPERSEDED — population, not method.** Every number in Part 6 describes the
> **six `text_only` conditions** as they stood before the `metadata_enriched` arm
> existed. The grid is now **12 conditions**, so "the six conditions are not
> statistically distinguishable" is a statement about the `text_only` half only and
> must not be quoted as describing the experiment as a whole.
>
> **Extended by `analysis/stage1/stage1_statistics_12cond.md`**, which uses this method
> unchanged, reproduces every value below exactly, and then reports three families:
> representation (each enriched condition against its matched `text_only`
> counterpart), chunk size and strategy within `text_only` (a replication of Part 6),
> and chunk size and strategy within `metadata_enriched`.
>
> Part 6 is **left unmodified below this note** as the historical `text_only` record.


Per-question paired scores for all 6 conditions (used to derive every comparison below)
are saved to `analysis/stage1/stage1_scores_long.csv` (240 rows: condition_id × question_id,
both metrics, category and chunk_size_sensitive included) — pivot condition_id against
question_id for any pairwise diff not tabulated below.

**Method:** paired Wilcoxon signed-rank test (`scipy.stats.wilcoxon`, `zero_method=
"wilcox"`, two-sided), since every condition faces the identical 40 questions and scores
are bounded, discrete, non-normal. Win/loss/tie counts are reported first per your
instruction, since with n=40 and mostly-zero scores they carry more information than a
p-value. Effect size `r = z / sqrt(n_nonzero)` from the normal approximation, reported
only when `n_nonzero ≥ 10` (below that the normal approximation itself is unreliable, so
`r` is left as n/a rather than printed as a false-precision number).

**Effect-size parameterization (added during the rebuild; the numbers below were always
computed this way).** `z` is the **textbook normal approximation with neither a tie
correction nor a continuity correction**:

```
z = (W - n(n+1)/4) / sqrt(n(n+1)(2n+1)/24)      n = n_nonzero
```

This is stated explicitly because **recomputing with scipy's defaults will not match**:
`scipy.stats.wilcoxon(..., method="approx")` applies a tie correction and returns
`r = −0.274` where this document prints **−0.268** (`chunk200_dense` vs `chunk500_bm25`,
coverage). The same gap appears in every row carrying an `r`. A reader who reproduces
with `method="approx"` and finds a third-decimal disagreement is seeing that tie
correction, **not an error in these numbers**. The uncorrected form above reproduces
every published `r` in Part 6 exactly, and is what
`analysis/rebuild_statistics.py::_wilcoxon_z` implements.

**Multiple comparisons:** **each metric forms its own Holm-Bonferroni family of 15
tests** (the 15 pairwise condition comparisons); `anchor_coverage_at_5` and
`mean_reciprocal_rank_at_5` are corrected separately, not pooled into a single family of
30. Both raw and Holm-adjusted p are reported per your instruction not to pick one
silently. Categories and the pooled set are treated as separate families (not corrected
against each other).

> **Correction, identified during the generator rebuild.** This paragraph previously
> described the family as "15 pairwise conditions × 2 metrics = 30 tests". That was a
> misdescription of the prose, not of the numbers: **every published value in 6.1–6.2 was
> always computed at family size 15, per metric.** The arithmetic is checkable on the
> smallest p in each table — coverage `chunk200_dense vs chunk200_hybrid` raw 0.0434 is
> printed as Holm **0.651 = 0.0434 × 15** (family size 30 would give 1.000), and the MRR
> equivalent raw 0.0150 is printed as **0.225 = 0.0150 × 15** (30 would give 0.449).
> Family size 15 reproduces all 30 published cells exactly; family size 30 reproduces 28
> of 30. **No number below was recomputed or altered — only this description was wrong.**
>
> **No conclusion changes at either family size**: zero comparisons are Holm-significant
> under both, since the smallest adjusted p is 0.225 at size 15 and 0.449 at size 30,
> both far above 0.05. The correction matters for reproducibility, not for any finding.

*(Aside, not a Part-6 finding: this analysis needed `scipy`, which is installed in the
venv but not listed in `requirements.txt`. Harmless for a one-off diagnostic; flagging
because every dependency must be pinned, so if Wilcoxon-style testing becomes
a permanent part of the analysis pipeline rather than a diagnostic one-off, `scipy` needs
adding there. Not fixed here per the "report and stop" instruction.)*

### 6.1–6.2 Pooled pairwise comparisons, all 15 pairs (n=40)

**anchor_coverage_at_5:**

| pair | win | loss | tie | n≠0 | W | p (raw) | p (Holm) | r |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| chunk200_bm25 vs chunk200_dense | 4 | 2 | 34 | 6 | 6.0 | 0.339 | 1.000 | n/a |
| chunk200_bm25 vs chunk200_hybrid | 1 | 3 | 36 | 4 | 2.0 | 0.257 | 1.000 | n/a |
| chunk200_bm25 vs chunk500_bm25 | 3 | 4 | 33 | 7 | 13.0 | 0.862 | 1.000 | n/a |
| chunk200_bm25 vs chunk500_dense | 3 | 4 | 33 | 7 | 11.5 | 0.665 | 1.000 | n/a |
| chunk200_bm25 vs chunk500_hybrid | 2 | 4 | 34 | 6 | 10.0 | 0.915 | 1.000 | n/a |
| chunk200_dense vs chunk200_hybrid | 1 | 5 | 34 | 6 | 1.0 | **0.043** | 0.651 | n/a |
| chunk200_dense vs chunk500_bm25 | 4 | 7 | 29 | 11 | 23.0 | 0.364 | 1.000 | −0.268 |
| chunk200_dense vs chunk500_dense | 3 | 6 | 31 | 9 | 17.0 | 0.506 | 1.000 | n/a |
| chunk200_dense vs chunk500_hybrid | 3 | 7 | 30 | 10 | 18.0 | 0.323 | 1.000 | −0.306 |
| chunk200_hybrid vs chunk500_bm25 | 6 | 5 | 29 | 11 | 28.5 | 0.681 | 1.000 | −0.121 |
| chunk200_hybrid vs chunk500_dense | 5 | 4 | 31 | 9 | 14.5 | 0.330 | 1.000 | n/a |
| chunk200_hybrid vs chunk500_hybrid | 3 | 3 | 34 | 6 | 7.5 | 0.516 | 1.000 | n/a |
| chunk500_bm25 vs chunk500_dense | 4 | 4 | 32 | 8 | 14.0 | 0.566 | 1.000 | n/a |
| chunk500_bm25 vs chunk500_hybrid | 3 | 4 | 33 | 7 | 13.5 | 0.931 | 1.000 | n/a |
| chunk500_dense vs chunk500_hybrid | 2 | 3 | 35 | 5 | 5.5 | 0.581 | 1.000 | n/a |

**mean_reciprocal_rank_at_5:**

| pair | win | loss | tie | n≠0 | W | p (raw) | p (Holm) | r |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| chunk200_bm25 vs chunk200_dense | 6 | 3 | 31 | 9 | 13.5 | 0.286 | 1.000 | n/a |
| chunk200_bm25 vs chunk200_hybrid | 3 | 5 | 32 | 8 | 13.5 | 0.526 | 1.000 | n/a |
| chunk200_bm25 vs chunk500_bm25 | 4 | 4 | 32 | 8 | 14.5 | 0.624 | 1.000 | n/a |
| chunk200_bm25 vs chunk500_dense | 4 | 6 | 30 | 10 | 21.0 | 0.507 | 1.000 | −0.210 |
| chunk200_bm25 vs chunk500_hybrid | 2 | 8 | 30 | 10 | 14.5 | 0.185 | 1.000 | −0.419 |
| chunk200_dense vs chunk200_hybrid | 1 | 8 | 31 | 9 | 2.0 | **0.015** | 0.225 | n/a |
| chunk200_dense vs chunk500_bm25 | 4 | 7 | 29 | 11 | 22.5 | 0.349 | 1.000 | −0.281 |
| chunk200_dense vs chunk500_dense | 3 | 8 | 29 | 11 | 16.0 | 0.130 | 1.000 | −0.456 |
| chunk200_dense vs chunk500_hybrid | 3 | 9 | 28 | 12 | 16.5 | 0.076 | 1.000 | −0.510 |
| chunk200_hybrid vs chunk500_bm25 | 7 | 7 | 26 | 14 | 52.0 | 0.975 | 1.000 | −0.008 |
| chunk200_hybrid vs chunk500_dense | 5 | 6 | 29 | 11 | 32.5 | 0.965 | 1.000 | −0.013 |
| chunk200_hybrid vs chunk500_hybrid | 4 | 7 | 29 | 11 | 24.0 | 0.422 | 1.000 | −0.241 |
| chunk500_bm25 vs chunk500_dense | 5 | 6 | 29 | 11 | 29.0 | 0.721 | 1.000 | −0.107 |
| chunk500_bm25 vs chunk500_hybrid | 3 | 8 | 29 | 11 | 16.0 | 0.130 | 1.000 | −0.456 |
| chunk500_dense vs chunk500_hybrid | 3 | 5 | 32 | 8 | 11.5 | 0.362 | 1.000 | n/a |

**No pairwise comparison survives Holm correction.** The smallest raw p (`chunk200_dense`
vs `chunk200_hybrid`, coverage, p=0.043) is nominally under 0.05 uncorrected but adjusts
to 0.651 under Holm. Tie counts dominate every row (29–37 of 40 questions tied, mostly at
0–0 — both conditions scoring zero on the same question) — the effective sample feeding
each test is usually 4–14 non-tied questions, not 40.

### 6.3 Within factual (n=14) and thematic (n=15)

Both categories are sparser than pooled and no pairwise test approaches significance in
either. Summary (full 15-pair × 2-metric tables for each category, plus comparative as a
supplementary third, are in the run log — omitted here since every p-Holm is 1.000):

| category | metric | min p (raw) across 15 pairs | pair | n≠0 for that pair |
|---|---|--:|---|--:|
| factual | coverage | 0.157 | chunk200_dense vs chunk200_hybrid | 2 |
| factual | MRR | 0.102 | chunk200_dense vs chunk200_hybrid | 3 |
| thematic | coverage | 0.157 | chunk500_bm25 vs chunk500_dense / vs chunk500_hybrid | 2 |
| thematic | MRR | 0.109 | chunk200_bm25 vs chunk500_hybrid | 3 |
| comparative (supplementary) | coverage | 0.250 | several tied at this p | 3 |
| comparative (supplementary) | MRR | 0.125 | chunk200_dense vs chunk500_dense/hybrid | 4 |

At category granularity, `n≠0` (non-tied questions feeding the test) drops to 1–6 out of
14–15 for most pairs — most questions in most category/condition pairs score identically
(usually 0–0). No p value gets close to 0.05 even uncorrected. Full per-pair tables are
reproducible from `stage1_scores_long.csv`.

### 6.4 Main effects

**Chunk size (200 vs 500), collapsed across strategy** — per-question mean over the 3
strategies at each size, n=40 independent units:

| metric | win (500>200) | loss (200>500) | tie | n≠0 | W | p | r |
|---|--:|--:|--:|--:|--:|--:|--:|
| anchor_coverage_at_5 | 6 | 9 | 25 | 15 | 52.0 | 0.649 | −0.117 |
| mean_reciprocal_rank_at_5 | 4 | 13 | 23 | 17 | 44.0 | 0.124 | **−0.373** |

MRR is the closest thing to a directional signal for chunk size in this whole analysis:
13 of 17 non-tied questions favor 500 tokens over 200, a moderate effect size (r=−0.37),
but p=0.124 — not significant at n=40, and this is a single test so no correction issue,
but it doesn't clear the conventional bar either. Worth watching, not worth claiming.

**Strategy (dense / bm25 / hybrid), collapsed across chunk size** — per-question mean
over the 2 chunk sizes per strategy, n=40, 3 pairwise comparisons per metric,
Holm-corrected within each metric:

| metric | pair | win | loss | tie | n≠0 | W | p (raw) | p (Holm) | r |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| coverage | dense vs bm25 | 6 | 7 | 27 | 13 | 34.5 | 0.434 | 0.868 | −0.213 |
| coverage | dense vs hybrid | 3 | 6 | 31 | 9 | 10.5 | 0.150 | 0.450 | n/a |
| coverage | bm25 vs hybrid | 4 | 5 | 31 | 9 | 17.0 | 0.500 | 0.868 | n/a |
| MRR | dense vs bm25 | 8 | 8 | 24 | 16 | 64.5 | 0.856 | 0.856 | −0.045 |
| MRR | dense vs hybrid | 3 | 10 | 27 | 13 | 19.0 | 0.064 | 0.192 | **−0.514** |
| MRR | bm25 vs hybrid | 4 | 10 | 26 | 14 | 25.0 | 0.084 | 0.192 | **−0.461** |

Hybrid trends ahead of both single strategies on MRR (loses to dense on only 3/13
non-tied questions, to bm25 on only 4/14), with the largest effect sizes in the entire
analysis (r=−0.51, −0.46) — but neither survives Holm correction (p_Holm=0.192 for both).
This is the strategy-side echo of the chunk-size MRR trend above: a real-looking
direction that this sample size cannot certify.

### 6.5 The 7 chunk_size_sensitive items, per-item (no test — n too small)

| question_id | bm25 200→500 | dense 200→500 | hybrid 200→500 |
|---|---|---|---|
| ref_comp_01 | 0.000 → 0.000 | 0.000 → 0.000 | 0.000 → 0.000 |
| ref_comp_04 | 0.000 → 0.000 | 0.000 → 0.000 | 0.000 → 0.000 |
| ref_fact_01 | 1.000 → 0.000 (↓) | 0.000 → 0.000 | 1.000 → 1.000 |
| ref_fact_12 | 0.000 → 0.000 | 1.000 → 0.000 (↓) | 1.000 → 0.000 (↓) |
| ref_them_03 | 0.000 → 0.000 | 0.000 → 0.000 | 0.000 → 0.000 |
| ref_them_04 | 0.500 → 0.000 (↓) | 0.500 → 0.500 | 0.500 → 0.500 |
| ref_them_15 | 0.000 → 0.000 | 0.333 → 0.000 (↓) | 0.000 → 0.000 |

(coverage@5 shown; MRR moves in the same direction on every cell — see
`stage1_scores_long.csv`.)

**3 of the 7 items selected specifically to exercise chunk_size (`ref_comp_01`,
`ref_comp_04`, `ref_them_03`) show literally zero score in every strategy at both chunk
sizes** — not a chunk-size effect, just a floor for every condition on those 3 questions.
Of the remaining 4 that do move, **every observed change is 500 tokens performing worse
or equal to 200**, never better — the opposite direction from the pooled-mean MRR trend
in 6.4, which leaned (weakly, non-significantly) toward 500. With n=4 informative items
this is not a basis for a directional claim either way; it mainly shows that "selected as
chunk_size_sensitive" during annotation didn't guarantee an observable difference at this
scale, and where a difference is observed, it isn't uniform in direction with the
pooled-mean trend.

---

## Verdict on Parts 5–6

**Part 5:** the mechanism is now precise enough to write down. Metadata (company, ticker,
date, quarter, section) is attached to every chunk record but is **never part of the
indexed string** for either retriever — confirmed by reading both call sites and printing
the literal strings. Across the 74 gold chunks, only 9.5% (200 tokens) to 21.6% (500
tokens) contain **both** company and period signal in the indexed text; 41–46% (200
tokens) contain neither. Chunks with at least one signal are found more often and rank
better, consistently across all 3 strategies at 200 tokens (less cleanly at 500, where
longer context dilutes the gap). This is a structural property of the chunking/indexing
design — verbatim text only, no metadata injection — not a defect in any single
retriever, and no choice among dense/BM25/hybrid can fully compensate for a signal that
isn't in the indexed text to begin with.

**Part 6, stated plainly: the six conditions are not statistically distinguishable at
n=40.** Every one of the 15 pooled pairwise comparisons, on both metrics, fails to
survive Holm correction; the same holds within factual and thematic separately (where the
number of non-tied questions per pair often drops to 1–6). The two main effects — chunk
size and strategy, each collapsed the other way — come closer: hybrid trending ahead of
both single strategies on MRR (r≈−0.5) and 500 tokens trending ahead of 200 on MRR
(r=−0.37), but neither clears significance at this n, and the 7 chunk_size_sensitive
items don't reinforce the 500-token direction (of the 4 that move at all, all 4 move
toward 200 being *better*, not worse). This is a valid result to report as-is: at the
current 40-question benchmark, the experiment does not yet have the power to separate the
six conditions from each other, even though it does separate "found something" from
"found nothing" (Part 3's coverage@50 numbers). That is a statement about statistical
power at this n, not about whether real differences exist between the conditions.

