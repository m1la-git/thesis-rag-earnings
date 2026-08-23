"""Isolation tests for the third independent variable, indexing_representation.

These do not test that enrichment helps retrieval -- that is what the
experiment is for. They test the boundary the experiment's validity rests on:
the enriched string reaches the retrievers and NOTHING else.

README.md invariant 1 is the single most important constraint in this
change. Anchors are verbatim substrings of transcript prose, and coverage@5 /
MRR@5 mean what they mean for the six existing conditions only because a hit
is decided against raw chunk text. If enrichment text could ever satisfy an
anchor match, the two halves of the grid would stop being comparable and every
existing number would silently change meaning. The same applies downstream: the
generator must never see the prefix (or its context would differ between arms
for the same retrieved chunk), and the grounding checker must never accept a
number that appears only in metadata.

    python -m unittest tests.test_index_representation -v
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import evaluate  # noqa: E402
import generate  # noqa: E402
import index as index_mod  # noqa: E402
import run_experiment  # noqa: E402

TEXT_ONLY = index_mod.REPRESENTATION_TEXT_ONLY
ENRICHED = index_mod.REPRESENTATION_METADATA_ENRICHED


def chunk(text, chunk_id="JPM_2024_Q1_qa_200_007", **overrides):
    base = {
        "chunk_id": chunk_id,
        "transcript_id": "JPM_2024_Q1",
        "company": "JPMorgan Chase & Co.",
        "ticker": "JPM",
        "year": 2024,
        "quarter": 1,
        "section": "qa",
        "text": text,
        "n_tokens": len(index_mod.get_tokenizer()(text, add_special_tokens=False)["input_ids"]),
    }
    base.update(overrides)
    return base


class TestTextOnlyIsByteIdentical(unittest.TestCase):
    """README.md invariant 5: the six existing conditions are not re-run because
    text_only's indexed string is byte-identical to what the old code indexed.
    That is a property of the code, asserted here, not an assumption."""

    def test_build_index_text_returns_text_unchanged(self):
        for text in [
            "Net income of $18.1 billion, up 6% year over year.",
            "",
            "Unicode: — dashes, “quotes”, café, €1.5bn.",
            "Trailing whitespace and newlines\n\n  ",
            "A" * 5000,
        ]:
            with self.subTest(text=text[:30]):
                self.assertEqual(index_mod.build_index_text(chunk(text), TEXT_ONLY), text)

    def test_text_only_is_the_identity_not_a_copy_of_the_template(self):
        c = chunk("JPMorgan Chase & Co. (JPM) first quarter 2024 Q1 2024 question and answer")
        self.assertEqual(index_mod.build_index_text(c, TEXT_ONLY), c["text"])

    def test_text_only_stats_record_no_truncation(self):
        c = chunk("Net income of $18.1 billion.")
        _, stats = index_mod.build_index_text_with_stats(c, TEXT_ONLY)
        self.assertEqual(stats["prefix_tokens"], 0)
        self.assertFalse(stats["truncated"])
        self.assertEqual(stats["transcript_tokens_dropped"], 0)


class TestEnrichmentShape(unittest.TestCase):
    def test_enriched_is_one_line_a_blank_line_then_the_text(self):
        c = chunk("Net income of $18.1 billion.")
        enriched = index_mod.build_index_text(c, ENRICHED)
        prefix, blank, body = enriched.split("\n", 2)
        self.assertEqual(
            prefix, "JPMorgan Chase & Co. (JPM) first quarter 2024 Q1 2024 question and answer"
        )
        self.assertEqual(blank, "")
        self.assertEqual(body, c["text"])

    def test_enriched_drops_the_phrase_earnings_call(self):
        """It would appear on 100% of chunks, so its IDF is ~0 and it cannot
        discriminate -- the same argument that ruled out field labels."""
        self.assertNotIn("earnings call", index_mod.build_index_text(chunk("x"), ENRICHED).lower())

    def test_enriched_carries_period_in_both_prose_and_shorthand(self):
        enriched = index_mod.build_index_text(chunk("x"), ENRICHED)
        self.assertIn("first quarter 2024", enriched)
        self.assertIn("Q1 2024", enriched)

    def test_unknown_representation_raises(self):
        with self.assertRaises(ValueError):
            index_mod.build_index_text(chunk("x"), "enriched")

    def test_unknown_section_or_quarter_raises_rather_than_guessing(self):
        with self.assertRaises(ValueError):
            index_mod.build_index_text(chunk("x", section="appendix"), ENRICHED)
        with self.assertRaises(ValueError):
            index_mod.build_index_text(chunk("x", quarter=5), ENRICHED)


class TestTruncation(unittest.TestCase):
    """Truncation happens at build time so both retrievers consume the same
    content, not merely the same bytes: the encoder silently drops overflow
    while BM25 has no length limit."""

    def _long_chunk(self, n_words=1200):
        text = " ".join(f"word{i}" for i in range(n_words))
        return chunk(text)

    def test_enriched_string_never_exceeds_the_content_budget(self):
        c = self._long_chunk()
        enriched = index_mod.build_index_text(c, ENRICHED)
        n = len(index_mod.get_tokenizer()(enriched, add_special_tokens=False)["input_ids"])
        self.assertLessEqual(n, index_mod.MAX_CONTENT_TOKENS)

    def test_truncation_is_recorded_not_just_performed(self):
        c = self._long_chunk()
        _, stats = index_mod.build_index_text_with_stats(c, ENRICHED)
        self.assertTrue(stats["truncated"])
        self.assertGreater(stats["prefix_tokens"], 0)
        self.assertGreater(stats["transcript_tokens_dropped"], 0)
        self.assertEqual(
            stats["transcript_tokens_kept"] + stats["transcript_tokens_dropped"],
            stats["transcript_tokens_total"],
        )

    def test_short_chunks_are_not_truncated(self):
        _, stats = index_mod.build_index_text_with_stats(chunk("Net income of $18.1 billion."), ENRICHED)
        self.assertFalse(stats["truncated"])
        self.assertEqual(stats["transcript_tokens_dropped"], 0)

    def test_truncation_is_judged_against_the_standalone_token_count(self):
        """chunking.py counts a chunk's tokens inside its section's
        tokenization; re-tokenizing that substring alone can differ by a token
        where the boundary fell mid-word. Judging truncation against
        chunk["n_tokens"] therefore reported chunks as truncated that were
        returned whole -- ~20 per corpus at chunk_size=200, where the prefix
        leaves ~290 tokens of headroom and nothing can be cut."""
        text = "Net income of $18.1 billion for the quarter."
        c = chunk(text, n_tokens=999)  # deliberately disagrees with reality
        index_text, stats = index_mod.build_index_text_with_stats(c, ENRICHED)
        self.assertEqual(index_text.split(index_mod.ENRICHMENT_JOINER, 1)[1], text)
        self.assertFalse(stats["truncated"])
        self.assertEqual(stats["transcript_tokens_dropped"], 0)
        self.assertEqual(stats["chunk_n_tokens"], 999)

    def test_truncated_body_is_a_real_prefix_of_the_original_text(self):
        c = self._long_chunk()
        body = index_mod.build_index_text(c, ENRICHED).split("\n\n", 1)[1]
        self.assertTrue(c["text"].startswith(body))

    def test_truncation_does_not_touch_the_raw_text(self):
        """The whole point: truncation reduces retrievability, never
        scorability. chunk["text"] is what anchor matching reads."""
        c = self._long_chunk()
        before = c["text"]
        index_mod.attach_index_text([c], ENRICHED)
        self.assertEqual(c["text"], before)


class TestAnchorMatchingIsIsolatedFromIndexText(unittest.TestCase):
    """README.md invariant 1, the single most important constraint here."""

    def test_anchor_present_only_in_index_text_is_not_a_hit(self):
        anchor = "JPMorgan Chase & Co. (JPM) first quarter 2024"
        c = chunk("Revenue grew across the franchise this period.")
        index_mod.attach_index_text([c], ENRICHED)
        self.assertIn(anchor, c["index_text"])
        self.assertNotIn(anchor, c["text"])
        self.assertFalse(evaluate.chunk_matches_anchor(c, anchor))

    def test_a_hand_forged_index_text_still_cannot_manufacture_a_hit(self):
        anchor = "net income of $18.1 billion"
        c = chunk("No figures were disclosed on this call.")
        c["index_text"] = f"{anchor}\n\n{c['text']}"
        self.assertFalse(evaluate.chunk_matches_anchor(c, anchor))

    def test_real_anchor_in_text_is_still_a_hit_under_both_representations(self):
        anchor = "net income of $18.1 billion"
        c = chunk(f"We reported {anchor} for the quarter.")
        for representation in index_mod.INDEXING_REPRESENTATIONS:
            with self.subTest(representation=representation):
                index_mod.attach_index_text([c], representation)
                self.assertTrue(evaluate.chunk_matches_anchor(c, anchor))

    def test_first_match_rank_ignores_index_text(self):
        anchor = "assets under custody"
        decoy = chunk("Nothing relevant here.", chunk_id="BK_2024_Q1_qa_200_001")
        decoy["index_text"] = f"{anchor}\n\nNothing relevant here."
        real = chunk(f"Our {anchor} grew.", chunk_id="BK_2024_Q1_qa_200_002")
        real["index_text"] = real["text"]
        self.assertEqual(evaluate.first_match_rank([decoy, real], anchor), 2)


class TestAnchorMatchingOverTheRealBenchmark(unittest.TestCase):
    """The property above, checked over every real gold anchor rather than
    over hand-made fixtures: chunk_matches_anchor must return identical results
    under both representations for every (anchor, chunk) pair the benchmark
    actually produces. Chunks are built only for the transcripts the benchmark
    references -- no embedding model, no index."""

    @classmethod
    def setUpClass(cls):
        import pandas as pd

        import ingest
        from chunking import chunk_transcript
        from preprocess import preprocess_transcript

        questions = run_experiment.load_questions()
        cls.scored = run_experiment.scored_questions(questions)
        needed = sorted({tid for q in cls.scored for tid in q["transcript_ids"]})

        df = pd.read_parquet(ingest.TRANSCRIPTS_PATH)
        df = df[df["transcript_id"].isin(needed)]
        cls.chunks_by_size = {}
        for size in run_experiment.CHUNK_SIZES:
            chunks = []
            for _, row in df.iterrows():
                chunks.extend(chunk_transcript(preprocess_transcript(row), size))
            cls.chunks_by_size[size] = chunks

    def test_hit_decisions_are_identical_under_both_representations(self):
        n_pairs = 0
        n_hits = 0
        for size, chunks in self.chunks_by_size.items():
            text_only = [dict(c) for c in chunks]
            enriched = [dict(c) for c in chunks]
            index_mod.attach_index_text(text_only, TEXT_ONLY)
            index_mod.attach_index_text(enriched, ENRICHED)

            for q in self.scored:
                for anchor in evaluate.anchor_strings(q):
                    for a, b in zip(text_only, enriched):
                        hit_a = evaluate.chunk_matches_anchor(a, anchor)
                        hit_b = evaluate.chunk_matches_anchor(b, anchor)
                        n_pairs += 1
                        n_hits += int(hit_a)
                        if hit_a != hit_b:
                            self.fail(
                                f"chunk {a['chunk_id']} / anchor {anchor!r}: hit differs "
                                f"between representations ({hit_a} vs {hit_b})"
                            )
        self.assertGreater(n_pairs, 0)
        self.assertGreater(n_hits, 0, "no anchor matched anything -- the check proved nothing")

    def test_no_anchor_is_satisfied_by_metadata_alone(self):
        """A stronger form of the same claim: if any gold anchor were a
        substring of an enrichment prefix, enrichment could create hits."""
        for size, chunks in self.chunks_by_size.items():
            prefixes = {index_mod.build_enrichment_prefix(c) for c in chunks}
            for q in self.scored:
                for anchor in evaluate.anchor_strings(q):
                    for prefix in prefixes:
                        if anchor in prefix:
                            self.fail(
                                f"anchor {anchor!r} is contained in enrichment prefix {prefix!r} "
                                f"at chunk_size={size}"
                            )


class TestGeneratorNeverSeesTheEnrichment(unittest.TestCase):
    """The enriched string is index-side only. The generator's context must be
    byte-identical to what text_only would have shown for the same chunk, so
    any change in generation traces to WHICH chunks were retrieved rather than
    to what the model was told about them."""

    def test_format_context_contains_no_metadata_line(self):
        c = chunk("Net income of $18.1 billion.")
        index_mod.attach_index_text([c], ENRICHED)
        context = generate.format_context([c])
        self.assertIn(c["text"], context)
        self.assertNotIn("first quarter 2024", context)
        self.assertNotIn("JPMorgan Chase & Co. (JPM)", context)
        self.assertNotIn(c["index_text"], context)

    def test_context_is_identical_under_both_representations(self):
        text_only = chunk("Net income of $18.1 billion.")
        enriched = chunk("Net income of $18.1 billion.")
        index_mod.attach_index_text([text_only], TEXT_ONLY)
        index_mod.attach_index_text([enriched], ENRICHED)
        self.assertEqual(generate.format_context([text_only]), generate.format_context([enriched]))


class TestGroundingAndLoggingReadRawTextOnly(unittest.TestCase):
    def _question(self):
        return {
            "id": "q1",
            "category": "factual",
            "question": "What was the figure?",
            "transcript_ids": ["JPM_2024_Q1"],
            "gold_anchors": ["net income"],
            "reference_answer": "ref",
        }

    def test_numeric_claim_present_only_in_metadata_is_ungrounded(self):
        """evaluate.classify_outcome verifies claims against chunk["text"]. The
        enrichment prefix contains a year and a quarter number; if the checker
        read index_text, those digits could pass a claim the transcript never
        made."""
        c = chunk("Management declined to give a figure.")
        index_mod.attach_index_text([c], ENRICHED)
        self.assertIn("2024", c["index_text"])
        self.assertNotIn("2024", c["text"])
        result = evaluate.classify_outcome("The figure was 2024.", self._question(), [c])
        self.assertEqual(result["outcome"], evaluate.OUTCOME_UNGROUNDED)
        self.assertIn("2024", result["unsupported_claims"])

    def test_ngram_fallback_ignores_index_text(self):
        """The no-numeric-claims path (_shared_ngram_chunk_ids) must read raw
        text too, or an answer echoing the metadata line would look supported."""
        c = chunk("Management declined to comment on the outlook.")
        index_mod.attach_index_text([c], ENRICHED)
        answer = "JPMorgan Chase & Co. (JPM) first quarter question and answer session"
        self.assertIn("first quarter", c["index_text"])
        self.assertEqual(evaluate._shared_ngram_chunk_ids(answer, [c]), set())

    def test_ranking_log_records_raw_text_and_leaks_no_index_text(self):
        c = chunk("Net income of $18.1 billion.")
        index_mod.attach_index_text([c], ENRICHED)
        log = run_experiment._ranking_log([{**c, "score": 0.9}])
        self.assertEqual(log[0]["text"], c["text"])
        self.assertNotIn("index_text", log[0])
        self.assertEqual(set(log[0]), {"rank", "chunk_id", "score", "text"})


class TestIndexBuildGuards(unittest.TestCase):
    def test_embed_and_bm25_refuse_to_fall_back_to_text(self):
        """No fallback to chunk["text"]: that would index a text_only run under
        an enriched label -- a control masquerading as a result."""
        chunks = [chunk("Net income of $18.1 billion.")]
        with self.assertRaises(KeyError):
            index_mod.build_bm25_index(chunks)
        with self.assertRaises(KeyError):
            index_mod._index_texts(chunks)

    def test_control_arm_guard_catches_a_quietly_enriched_baseline(self):
        chunks = [chunk("Net income of $18.1 billion.")]
        index_mod.attach_index_text(chunks, TEXT_ONLY)
        index_mod.assert_control_arm_unenriched(chunks)  # should not raise

        index_mod.attach_index_text(chunks, ENRICHED)
        with self.assertRaises(AssertionError):
            index_mod.assert_control_arm_unenriched(chunks)

    def test_both_retrievers_receive_the_identical_string(self):
        """Invariant 3: index_text is computed once per chunk and shared, so
        dense and BM25 cannot diverge."""
        chunks = [chunk("Net income of $18.1 billion.")]
        index_mod.attach_index_text(chunks, ENRICHED)
        self.assertEqual(index_mod._index_texts(chunks), [chunks[0]["index_text"]])


class TestFrozenFormatMatchesConfig(unittest.TestCase):
    """Invariant 2: one format, one place in the code, cross-checked against
    configs/base.json -- the same discipline query_prefix already has."""

    def test_every_real_condition_config_validates(self):
        for path in run_experiment.discover_condition_configs():
            config = run_experiment.load_config(path)
            with self.subTest(condition=config["condition_id"]):
                run_experiment.validate_config_matches_code(config)


if __name__ == "__main__":
    unittest.main()
