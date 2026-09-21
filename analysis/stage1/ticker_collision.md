# Ticker collision diagnostic

Corpus: 128 transcripts, 16 tickers, 7918 chunks @200 / 3239 chunks @500.

Tokenizer: `index.tokenize_for_bm25` = `re.findall(r"[a-z0-9]+", text.lower())`.
**There is no stopword list and no minimum token length** anywhere in the
pipeline, and `rank_bm25.BM25Okapi` adds none -- so every ticker survives
tokenization, including the single-letter one. IDF is read from the fitted
`BM25Okapi.idf`, not reimplemented. Sorted by IDF@200 ascending (least
discriminating first).

`bm25_idf_*` = **OOV** means the token is absent from the text_only
vocabulary entirely; `BM25Okapi` scores an unknown query term at 0 against
every chunk, so under `text_only` that ticker contributes nothing at all as
a search term.

`predicted_enriched_idf_*` is what that token's IDF becomes once the
enriched prefix puts the ticker in every chunk of its own company: document
frequency rises to the union of (chunks whose prose already contains it) and
(all of that company's chunks), which is ~1/16 of the collection. It is a
prediction from chunk counts, not a measurement of a built enriched index --
computed with `BM25Okapi`'s own IDF formula, asserted at run time to
reproduce the fitted values exactly.

| ticker | company | bm25_token | survives_tokenization | body_occurrences | n_distinct_companies_in_body | chunk_df_200 | bm25_idf_200 | chunk_df_500 | bm25_idf_500 | predicted_enriched_idf_200 | predicted_enriched_idf_500 | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | Citigroup Inc. | c | True | 213 | 13 | 161 | 3.8719 | 148 | 3.0358 | 2.1509 | 1.9056 | single_letter;common_english_word;appears_in_multiple_companies |
| PNC | The PNC Financial Services Group, Inc. | pnc | True | 88 | 1 | 55 | 4.9536 | 44 | 4.274 | 2.8987 | 2.8844 | - |
| MS | Morgan Stanley | ms | True | 15 | 4 | 15 | 6.2342 | 15 | 5.3377 | 2.7025 | 2.6718 | common_english_word;appears_in_multiple_companies |
| MTB | M&T Bank Corporation | mtb | True | 8 | 1 | 8 | 6.8359 | 8 | 5.9406 | 2.733 | 2.7401 | - |
| USB | U.S. Bancorp | usb | True | 8 | 1 | 7 | 6.9612 | 6 | 6.2095 | 2.8911 | 2.8782 | - |
| GS | The Goldman Sachs Group, Inc. | gs | True | 8 | 1 | 6 | 7.1044 | 6 | 6.2095 | 2.7374 | 2.724 | common_english_word |
| BK | The Bank of New York Mellon Corporation | bk | True | 4 | 1 | 4 | 7.4724 | 4 | 6.5779 | 2.479 | 2.4881 | common_english_word |
| JPM | JPMorgan Chase & Co. | jpm | True | 4 | 1 | 4 | 7.4724 | 4 | 6.5779 | 2.8271 | 2.8244 | - |
| BAC | Bank of America Corporation | bac | True | 1 | 1 | 1 | 8.5714 | 1 | 7.6774 | 2.4019 | 2.408 | - |
| FITB | Fifth Third Bancorp | fitb | True | 1 | 1 | 1 | 8.5714 | 1 | 7.6774 | 2.7374 | 2.7401 | - |
| AXP | American Express Company | axp | True | 0 | 0 | 0 | OOV | 0 | OOV | 2.876 | 2.866 | - |
| BLK | BlackRock, Inc. | blk | True | 0 | 0 | 0 | OOV | 0 | OOV | 2.7665 | 2.7675 | - |
| COF | Capital One Financial Corporation | cof | True | 0 | 0 | 0 | OOV | 0 | OOV | 2.9918 | 2.9741 | - |
| HBAN | Huntington Bancshares Incorporated | hban | True | 0 | 0 | 0 | OOV | 0 | OOV | 2.7871 | 2.7843 | - |
| STT | State Street Corporation | stt | True | 0 | 0 | 0 | OOV | 0 | OOV | 2.6178 | 2.6218 | - |
| WFC | Wells Fargo & Company | wfc | True | 0 | 0 | 0 | OOV | 0 | OOV | 2.6542 | 2.6515 | - |
