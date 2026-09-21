# Truncated-tail diagnostic (`metadata_enriched`, format P2)

How much transcript text the enrichment prefix pushes out of the indexed
string, at both chunk sizes. Budget: `index.MAX_CONTENT_TOKENS` = 510 content tokens (512 max_seq_length - 2 special tokens).

**Truncation reduces retrievability, not scorability.** Anchor matching runs
against raw `chunk["text"]`, which is never truncated, so an anchor in a
discarded tail still counts as a hit if its chunk is retrieved -- it is just
less likely to be retrieved on that anchor's own terms. These are exposure
numbers, not lost score.

## Chunks

| chunk_size | chunks | truncated | % truncated | prefix tokens (min/mean/max) | dropped tokens among truncated (mean/max) | total dropped |
|---|--:|--:|--:|--:|--:|--:|
| 200 | 7918 | 0 | 0.0% | 15/19.3/24 | 0.0/0 | 0 |
| 500 | 3239 | 2985 | 92.2% | 15/19.4/24 | 9.4/15 | 27955 |

## Gold anchors

`touching a tail` = at least one chunk containing the anchor has it wholly or
partly past the truncation point. `fully lost to the index` = EVERY chunk
containing that anchor does, so no chunk's indexed string carries it any more.

| chunk_size | anchors | touching a tail | fully lost to the index | questions with >=1 lost anchor | single-anchor questions fully lost |
|---|--:|--:|--:|--:|--:|
| 200 | 74 | 0 | 0 | 0 | 0  |
| 500 | 74 | 1 | 1 | 1 | 0  |

Per-anchor detail: `truncation_tail.csv`.
