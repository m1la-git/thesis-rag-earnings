"""Unit tests for the retrieval metrics in src/evaluate.py.

Stdlib unittest rather than pytest: the project pins every dependency for
reproducibility, and these tests are pure arithmetic that needs no new one.

    python -m unittest discover -s tests -v
"""

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import evaluate  # noqa: E402


def chunk(text: str) -> dict:
    """Minimal chunk stand-in; only `text` matters to the hit rule."""
    return {"text": text}


def ranked(*texts: str) -> list[dict]:
    """A retrieved list in rank order, rank 1 first."""
    return [chunk(t) for t in texts]


# A distinct filler that contains none of the anchors used below.
MISS = "unrelated commentary about the weather"


class TestSingleAnchor(unittest.TestCase):
    def test_matched_at_rank_1_scores_one(self):
        retrieved = ranked("net income of $18.1 billion this quarter", MISS, MISS, MISS, MISS)
        anchors = ["net income of $18.1 billion"]
        self.assertEqual(evaluate.anchor_coverage_at_5(retrieved, anchors), 1.0)
        self.assertEqual(evaluate.mean_reciprocal_rank_at_5(retrieved, anchors), 1.0)

    def test_unmatched_scores_zero_not_none(self):
        retrieved = ranked(MISS, MISS, MISS, MISS, MISS)
        anchors = ["net income of $18.1 billion"]
        self.assertEqual(evaluate.anchor_coverage_at_5(retrieved, anchors), 0.0)
        self.assertEqual(evaluate.mean_reciprocal_rank_at_5(retrieved, anchors), 0.0)

    def test_reduces_to_standard_mrr_at_rank_3(self):
        retrieved = ranked(MISS, MISS, "contains anchor alpha here", MISS, MISS)
        self.assertAlmostEqual(
            evaluate.mean_reciprocal_rank_at_5(retrieved, ["anchor alpha"]), 1 / 3
        )


class TestMultiAnchorFractional(unittest.TestCase):
    """The rule the strict all-anchors version was replaced by."""

    def setUp(self):
        # alpha at rank 2, beta at rank 4, gamma absent entirely.
        self.retrieved = ranked(
            MISS,
            "chunk carrying anchor alpha",
            MISS,
            "chunk carrying anchor beta",
            MISS,
        )
        self.anchors = ["anchor alpha", "anchor beta", "anchor gamma"]

    def test_two_of_three_matched_gives_fractional_coverage(self):
        self.assertAlmostEqual(
            evaluate.anchor_coverage_at_5(self.retrieved, self.anchors), 2 / 3, places=3
        )

    def test_mrr_is_mean_of_per_anchor_contributions(self):
        expected = (0.5 + 0.25 + 0.0) / 3
        self.assertAlmostEqual(
            evaluate.mean_reciprocal_rank_at_5(self.retrieved, self.anchors), expected
        )

    def test_partial_retrieval_never_earns_full_credit(self):
        coverage = evaluate.anchor_coverage_at_5(self.retrieved, self.anchors)
        mrr = evaluate.mean_reciprocal_rank_at_5(self.retrieved, self.anchors)
        self.assertLess(coverage, 1.0)
        self.assertLess(mrr, 1.0)
        self.assertGreater(coverage, 0.0)
        self.assertGreater(mrr, 0.0)

    def test_comparative_one_of_two_companies_scores_about_half(self):
        retrieved = ranked("JPM evidence anchor one", MISS, MISS, MISS, MISS)
        anchors = ["anchor one", "anchor two"]
        self.assertEqual(evaluate.anchor_coverage_at_5(retrieved, anchors), 0.5)
        self.assertEqual(evaluate.mean_reciprocal_rank_at_5(retrieved, anchors), 0.5)


class TestCutoff(unittest.TestCase):
    def test_match_below_rank_5_does_not_count(self):
        retrieved = ranked(MISS, MISS, MISS, MISS, MISS, "late chunk with anchor alpha")
        anchors = ["anchor alpha"]
        self.assertEqual(evaluate.anchor_coverage_at_5(retrieved, anchors), 0.0)
        self.assertEqual(evaluate.mean_reciprocal_rank_at_5(retrieved, anchors), 0.0)

    def test_top_k_matches_retrieve_module(self):
        """evaluate.TOP_K duplicates retrieve.TOP_K; this catches drift."""
        import retrieve

        self.assertEqual(evaluate.TOP_K, retrieve.TOP_K)


class TestUnanswerableExcluded(unittest.TestCase):
    def test_metrics_return_none_not_zero(self):
        retrieved = ranked(MISS, MISS, MISS, MISS, MISS)
        self.assertIsNone(evaluate.anchor_coverage_at_5(retrieved, []))
        self.assertIsNone(evaluate.mean_reciprocal_rank_at_5(retrieved, []))

    def test_score_retrieval_excludes_unanswerable(self):
        question = {"id": "U001", "category": "unanswerable", "gold_anchors": []}
        scores = evaluate.score_retrieval(question, ranked(MISS))
        self.assertIsNone(scores["anchor_coverage_at_5"])
        self.assertIsNone(scores["mean_reciprocal_rank_at_5"])

    def test_excluded_from_denominator_not_counted_as_zero(self):
        """A perfect answerable question plus an unanswerable one averages 1.0."""
        scores = [
            {"anchor_coverage_at_5": 1.0, "mean_reciprocal_rank_at_5": 1.0},
            {"anchor_coverage_at_5": None, "mean_reciprocal_rank_at_5": None},
        ]
        aggregate = evaluate.aggregate_retrieval(scores)
        self.assertEqual(aggregate["anchor_coverage_at_5"], 1.0)
        self.assertEqual(aggregate["mean_reciprocal_rank_at_5"], 1.0)
        self.assertEqual(aggregate["anchor_coverage_at_5_n_scored"], 1)
        self.assertEqual(aggregate["n_questions"], 2)
        self.assertEqual(aggregate["n_excluded"], 1)

    def test_answerable_question_without_anchors_raises(self):
        question = {"id": "F001", "category": "factual", "gold_anchors": []}
        with self.assertRaises(ValueError):
            evaluate.score_retrieval(question, ranked(MISS))


class TestSimilarityPathSkipsNullReference(unittest.TestCase):
    """The answer-similarity metric must never receive a null reference answer.

    Unanswerable records carry reference_answer: null, so BERTScore or an
    embedding cosine against them would raise rather than score. These tests
    exist so the guard cannot be forgotten when run_experiment.py is written.
    """

    def test_unanswerable_is_not_similarity_scored(self):
        question = {
            "id": "unans_01",
            "category": "unanswerable",
            "gold_anchors": [],
            "reference_answer": None,
        }
        self.assertFalse(evaluate.is_similarity_scored(question))

    def test_answerable_with_a_reference_answer_is_similarity_scored(self):
        question = {
            "id": "fact_01",
            "category": "factual",
            "gold_anchors": ["net income of $18.1 billion"],
            "reference_answer": "JPMorgan reported net income of $18.1 billion.",
        }
        self.assertTrue(evaluate.is_similarity_scored(question))

    def test_null_reference_answer_is_skipped_whatever_the_category(self):
        """Belt and braces: a null reference is skipped even if mis-categorised."""
        question = {
            "id": "fact_99",
            "category": "factual",
            "gold_anchors": ["anchor alpha"],
            "reference_answer": None,
        }
        self.assertFalse(evaluate.is_similarity_scored(question))

    def test_every_unanswerable_record_in_the_benchmark_is_skipped(self):
        """Run the guard over the real benchmark file, not a fixture."""
        benchmark = REPO_ROOT / "benchmark" / "questions.jsonl"
        if not benchmark.exists():
            self.skipTest("benchmark/questions.jsonl not built yet")
        records = [json.loads(line) for line in benchmark.read_text(encoding="utf-8").splitlines() if line.strip()]
        unanswerable = [r for r in records if r["category"] == "unanswerable"]
        self.assertTrue(unanswerable, "expected unanswerable records in the benchmark")
        for record in unanswerable:
            self.assertIsNone(record["reference_answer"], record["id"])
            self.assertFalse(evaluate.is_similarity_scored(record), record["id"])
        answerable = [r for r in records if r["category"] != "unanswerable"]
        for record in answerable:
            self.assertTrue(evaluate.is_similarity_scored(record), record["id"])


class TestUniformAcrossCategories(unittest.TestCase):
    def test_same_inputs_score_identically_in_every_category(self):
        retrieved = ranked(MISS, "chunk carrying anchor alpha", MISS, MISS, MISS)
        anchors = ["anchor alpha", "anchor beta"]
        results = []
        for category in evaluate.RETRIEVAL_SCORED_CATEGORIES:
            question = {"id": "Q", "category": category, "gold_anchors": anchors}
            results.append(evaluate.score_retrieval(question, retrieved))
        self.assertEqual(len(results), 3)
        for result in results[1:]:
            self.assertEqual(result, results[0])


class TestHitRuleIsShared(unittest.TestCase):
    def test_exact_case_sensitive_substring(self):
        self.assertTrue(evaluate.chunk_matches_anchor(chunk("a b c"), "b c"))
        self.assertFalse(evaluate.chunk_matches_anchor(chunk("a b c"), "B C"))

    def test_curly_and_straight_apostrophes_are_distinct(self):
        """Normalising here would silently break one spelling or the other."""
        self.assertTrue(evaluate.chunk_matches_anchor(chunk("we’re up"), "we’re up"))
        self.assertFalse(evaluate.chunk_matches_anchor(chunk("we’re up"), "we're up"))

    def test_metrics_agree_with_the_hit_rule(self):
        retrieved = ranked("chunk carrying anchor alpha")
        matched = evaluate.chunk_matches_anchor(retrieved[0], "anchor alpha")
        coverage = evaluate.anchor_coverage_at_5(retrieved, ["anchor alpha"])
        self.assertEqual(matched, coverage == 1.0)


# ---------------------------------------------------------------------------
# Stage 2: case (A/B/C) and outcome classification
# ---------------------------------------------------------------------------


def rchunk(chunk_id: str, text: str) -> dict:
    """A retrieved chunk with the chunk_id transcript_id_from_chunk_id and
    classify_outcome actually need, on top of the bare `chunk()` helper above."""
    return {"chunk_id": chunk_id, "text": text}


def question(id_, category, transcript_ids=None, reference_answer="ref answer", question_text=""):
    return {
        "id": id_,
        "category": category,
        "question": question_text,
        "transcript_ids": transcript_ids if transcript_ids is not None else ([] if category == "unanswerable" else ["AAA_2024_Q1"]),
        "reference_answer": None if category == "unanswerable" else reference_answer,
    }


class TestClassifyCase(unittest.TestCase):
    def test_unanswerable_is_case_a_regardless_of_coverage_value(self):
        q = question("q1", "unanswerable")
        self.assertEqual(evaluate.classify_case(q, None), evaluate.CASE_A)

    def test_answerable_zero_coverage_is_case_b(self):
        q = question("q1", "factual")
        self.assertEqual(evaluate.classify_case(q, 0.0), evaluate.CASE_B)

    def test_answerable_partial_coverage_is_case_c(self):
        q = question("q1", "thematic")
        self.assertEqual(evaluate.classify_case(q, 0.5), evaluate.CASE_C)

    def test_answerable_full_coverage_is_case_c(self):
        q = question("q1", "factual")
        self.assertEqual(evaluate.classify_case(q, 1.0), evaluate.CASE_C)


class TestTranscriptIdFromChunkId(unittest.TestCase):
    def test_prepared_remarks_section(self):
        self.assertEqual(
            evaluate.transcript_id_from_chunk_id("BAC_2024_Q4_prepared_remarks_200_018"), "BAC_2024_Q4"
        )

    def test_qa_section(self):
        self.assertEqual(evaluate.transcript_id_from_chunk_id("GS_2024_Q2_qa_200_020"), "GS_2024_Q2")

    def test_500_chunk_size_and_multi_digit_index(self):
        self.assertEqual(
            evaluate.transcript_id_from_chunk_id("JPM_2023_Q3_prepared_remarks_500_012"), "JPM_2023_Q3"
        )

    def test_no_recognised_section_marker_raises(self):
        with self.assertRaises(ValueError):
            evaluate.transcript_id_from_chunk_id("not_a_real_chunk_id")


class TestExtractNumericClaims(unittest.TestCase):
    def test_finds_plain_and_decimal_numbers(self):
        self.assertEqual(
            evaluate.extract_numeric_claims("up 5% to $48.8 trillion, or 289 million"),
            ["5", "48.8", "289"],
        )

    def test_no_numbers_returns_empty_list(self):
        self.assertEqual(evaluate.extract_numeric_claims("banks characterised the uncertainty as significant"), [])


class TestClassifyOutcomeAbstained(unittest.TestCase):
    def test_exact_abstention_string_is_abstained(self):
        q = question("q1", "factual")
        result = evaluate.classify_outcome(evaluate.ABSTENTION, q, [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "irrelevant")])
        self.assertEqual(result["outcome"], evaluate.OUTCOME_ABSTAINED)
        self.assertEqual(result["supporting_chunk_ids"], [])


class TestClassifyOutcomeGrounded(unittest.TestCase):
    def test_all_numbers_present_and_on_target_transcript_is_correct(self):
        q = question("q1", "factual", transcript_ids=["AAA_2024_Q1"])
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "net income of $18.1 billion, up 5%")]
        answer = "Net income was $18.1 billion, up 5% year-over-year."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_CORRECT)
        self.assertEqual(result["supporting_chunk_ids"], ["AAA_2024_Q1_prepared_remarks_200_000"])
        self.assertEqual(result["unsupported_claims"], [])

    def test_all_numbers_present_but_off_target_transcript_is_offtarget(self):
        """The ref_them_01 pattern: fully grounded in real retrieved text, but
        every supporting chunk belongs to a transcript the question never asked about."""
        q = question("q1", "thematic", transcript_ids=["AAA_2024_Q1"])
        retrieved = [rchunk("ZZZ_2023_Q4_prepared_remarks_200_000", "expenses rose 20% driven by the FDIC charge")]
        answer = "Expenses rose 20%, driven by the FDIC special assessment charge."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_OFFTARGET)
        self.assertEqual(result["supporting_chunk_ids"], ["ZZZ_2023_Q4_prepared_remarks_200_000"])

    def test_at_least_one_supporting_chunk_on_target_is_enough_for_correct(self):
        """A synthesis answer spanning several companies is still "correct" if
        AT LEAST ONE supporting chunk is from a target transcript -- it need
        not be every supporting chunk."""
        q = question("q1", "thematic", transcript_ids=["AAA_2024_Q1", "BBB_2023_Q3"])
        retrieved = [
            rchunk("AAA_2024_Q1_prepared_remarks_200_000", "revenue up 10%"),
            rchunk("CCC_2023_Q2_prepared_remarks_200_000", "expenses up 3%"),
        ]
        answer = "Revenue rose 10% while, elsewhere, expenses rose 3%."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_CORRECT)
        self.assertEqual(
            set(result["supporting_chunk_ids"]),
            {"AAA_2024_Q1_prepared_remarks_200_000", "CCC_2023_Q2_prepared_remarks_200_000"},
        )

    def test_a_number_absent_from_every_retrieved_chunk_is_ungrounded(self):
        q = question("q1", "factual", transcript_ids=["AAA_2024_Q1"])
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "net income of $18.1 billion")]
        answer = "Net income was $99.9 billion."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_UNGROUNDED)
        self.assertEqual(result["unsupported_claims"], ["99.9"])

    def test_one_supported_one_unsupported_number_is_ungrounded_not_partial_credit(self):
        """Any single fabricated figure sinks the whole answer to ungrounded --
        there is no partial-credit outcome, by design."""
        q = question("q1", "factual", transcript_ids=["AAA_2024_Q1"])
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "net income of $18.1 billion")]
        answer = "Net income was $18.1 billion, up 42% year-over-year."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_UNGROUNDED)
        self.assertEqual(result["unsupported_claims"], ["42"])

    def test_partial_context_multi_anchor_correct_with_no_fabrication_for_missing_part(self):
        """The rule: for a partial-context item, correct means correct as
        far as context supports, with no fabrication for the missing part.
        Falls out of the same on-target rule with no special-casing: the
        answer only claims what the present (on-target) chunk supports."""
        q = question("q1", "comparative", transcript_ids=["AAA_2024_Q1", "BBB_2023_Q3"])
        # only AAA's chunk was retrieved -- BBB's gold anchor is absent from top-5
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "operating leverage of 170 basis points")]
        answer = "AAA reported 170 basis points of operating leverage."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_CORRECT)

    def test_case_a_correct_is_impossible_because_transcript_ids_is_empty(self):
        """Unanswerable questions carry transcript_ids: [], so the on-target
        intersection can never be non-empty -- any grounded, answered Case A
        response is mechanically offtarget, never correct."""
        q = question("q1", "unanswerable")
        retrieved = [rchunk("ZZZ_2023_Q1_prepared_remarks_200_000", "revenue grew 8%")]
        answer = "Revenue grew 8%."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_OFFTARGET)

    def test_no_numeric_claims_falls_back_to_shared_ngram_and_can_be_grounded(self):
        q = question("q1", "thematic", transcript_ids=["AAA_2024_Q1"])
        shared_phrase = "characterised the uncertainty as significant and unresolved"
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", f"management {shared_phrase} going forward")]
        answer = f"Management {shared_phrase}."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_CORRECT)
        self.assertEqual(result["grounding_basis"], "ngram_fallback (answer has no numeric claims)")

    def test_no_numeric_claims_and_no_shared_phrase_is_ungrounded(self):
        q = question("q1", "thematic", transcript_ids=["AAA_2024_Q1"])
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "completely unrelated filler text about the weather today")]
        answer = "Management expressed strong confidence in the long-term outlook overall."
        result = evaluate.classify_outcome(answer, q, retrieved)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_UNGROUNDED)


class TestIsBertscoreScored(unittest.TestCase):
    def test_case_c_answered_is_scored(self):
        q = question("q1", "factual")
        self.assertTrue(evaluate.is_bertscore_scored(q, evaluate.CASE_C, evaluate.OUTCOME_GROUNDED_CORRECT))

    def test_case_c_abstained_is_not_scored(self):
        q = question("q1", "factual")
        self.assertFalse(evaluate.is_bertscore_scored(q, evaluate.CASE_C, evaluate.OUTCOME_ABSTAINED))

    def test_case_b_is_never_scored_even_if_answered(self):
        q = question("q1", "factual")
        self.assertFalse(evaluate.is_bertscore_scored(q, evaluate.CASE_B, evaluate.OUTCOME_GROUNDED_OFFTARGET))

    def test_case_a_is_never_scored(self):
        q = question("q1", "unanswerable")
        self.assertFalse(evaluate.is_bertscore_scored(q, evaluate.CASE_A, evaluate.OUTCOME_GROUNDED_OFFTARGET))

    def test_case_c_answered_but_null_reference_is_not_scored(self):
        """Belt and braces, mirroring is_similarity_scored: a Case C record
        somehow carrying a null reference_answer must not be scored either."""
        q = question("q1", "factual")
        q["reference_answer"] = None
        self.assertFalse(evaluate.is_bertscore_scored(q, evaluate.CASE_C, evaluate.OUTCOME_GROUNDED_CORRECT))


class TestClassifyCaseOutcomeAndAggregate(unittest.TestCase):
    def test_classify_case_outcome_combines_both(self):
        q = question("q1", "factual", transcript_ids=["AAA_2024_Q1"])
        retrieved = [rchunk("AAA_2024_Q1_prepared_remarks_200_000", "net income of $18.1 billion")]
        result = evaluate.classify_case_outcome(q, 1.0, "Net income was $18.1 billion.", retrieved)
        self.assertEqual(result["case"], evaluate.CASE_C)
        self.assertEqual(result["outcome"], evaluate.OUTCOME_GROUNDED_CORRECT)

    def test_aggregate_breaks_out_by_case_not_pooled(self):
        records = [
            {"case": "A", "outcome": evaluate.OUTCOME_ABSTAINED},
            {"case": "A", "outcome": evaluate.OUTCOME_ABSTAINED},
            {"case": "B", "outcome": evaluate.OUTCOME_ABSTAINED},
            {"case": "B", "outcome": evaluate.OUTCOME_GROUNDED_OFFTARGET},
            {"case": "C", "outcome": evaluate.OUTCOME_GROUNDED_CORRECT},
        ]
        agg = evaluate.aggregate_case_outcomes(records)
        self.assertEqual(agg["A"], {evaluate.OUTCOME_ABSTAINED: 2})
        self.assertEqual(agg["B"], {evaluate.OUTCOME_ABSTAINED: 1, evaluate.OUTCOME_GROUNDED_OFFTARGET: 1})
        self.assertEqual(agg["C"], {evaluate.OUTCOME_GROUNDED_CORRECT: 1})


# ---------------------------------------------------------------------------
# Fix 1: extract_numeric_claims's comma handling
# ---------------------------------------------------------------------------


class TestExtractNumericClaimsFix1TrailingComma(unittest.TestCase):
    def test_bare_year_followed_by_sentence_comma_drops_the_comma(self):
        self.assertEqual(evaluate.extract_numeric_claims("second quarter of 2023, representing"), ["2023"])

    def test_thousands_grouped_number_keeps_its_commas(self):
        self.assertEqual(evaluate.extract_numeric_claims("a total of $1,500 today"), ["1,500"])

    def test_comma_followed_by_fewer_than_three_digits_is_not_a_separator(self):
        self.assertEqual(evaluate.extract_numeric_claims("a ratio of 1,5 percent"), ["1", "5"])

    def test_trailing_comma_at_end_of_sentence(self):
        self.assertEqual(evaluate.extract_numeric_claims("Revenue was $500,"), ["500"])

    def test_number_at_end_of_string_with_no_trailing_punctuation(self):
        self.assertEqual(evaluate.extract_numeric_claims("BlackRock reported $190"), ["190"])

    def test_multi_group_thousands_separator_still_works(self):
        self.assertEqual(evaluate.extract_numeric_claims("$1,234,567 total"), ["1,234,567"])

    def test_comma_grouped_number_with_decimal_suffix(self):
        self.assertEqual(evaluate.extract_numeric_claims("$1,234.56 total"), ["1,234.56"])


# ---------------------------------------------------------------------------
# Fix 2: question-echoed trivial claims
# ---------------------------------------------------------------------------


class TestQuestionEchoedTrivialClaims(unittest.TestCase):
    def test_year_present_in_question_is_excluded(self):
        claims = evaluate.extract_numeric_claims("The figure was $190 million in 2024.")
        filtered = evaluate.filter_question_echoed_trivial_claims(claims, "What happened in 2024?")
        self.assertEqual(filtered, ["190"])

    def test_same_year_absent_from_question_is_verified(self):
        claims = evaluate.extract_numeric_claims("The figure was $190 million in 2023.")
        filtered = evaluate.filter_question_echoed_trivial_claims(claims, "What happened in 2024?")
        self.assertEqual(sorted(filtered), ["190", "2023"])

    def test_substantive_figure_that_looks_like_a_year_is_never_excluded(self):
        """"$2,024 million" is comma-grouped (Fix 1 keeps the comma), so it is
        never trivial regardless of whether "2024" is in the question."""
        claims = evaluate.extract_numeric_claims("Revenue was $2,024 million.")
        self.assertEqual(claims, ["2,024"])
        filtered = evaluate.filter_question_echoed_trivial_claims(claims, "What was revenue in 2024?")
        self.assertEqual(filtered, ["2,024"])

    def test_quarter_integer_in_question_is_excluded(self):
        claims = evaluate.extract_numeric_claims("Capital One reported $826 million in Q2 2024.")
        filtered = evaluate.filter_question_echoed_trivial_claims(claims, "What was the build called out in Q2 2024?")
        self.assertEqual(filtered, ["826"])

    def test_trivial_claim_not_echoed_by_question_is_still_verified(self):
        """A year the model introduces on its own (not in the question) is a
        real claim and must not be excluded."""
        claims = evaluate.extract_numeric_claims("This started back in 2019.")
        filtered = evaluate.filter_question_echoed_trivial_claims(claims, "How did the bank perform?")
        self.assertEqual(filtered, ["2019"])

    def test_is_trivial_claim_boundaries(self):
        self.assertTrue(evaluate.is_trivial_claim("1"))
        self.assertTrue(evaluate.is_trivial_claim("4"))
        self.assertTrue(evaluate.is_trivial_claim("2000"))
        self.assertTrue(evaluate.is_trivial_claim("2030"))
        self.assertFalse(evaluate.is_trivial_claim("5"))
        self.assertFalse(evaluate.is_trivial_claim("1999"))
        self.assertFalse(evaluate.is_trivial_claim("2031"))
        self.assertFalse(evaluate.is_trivial_claim("190"))
        self.assertFalse(evaluate.is_trivial_claim("2,024"))


# ---------------------------------------------------------------------------
# Fix 3: soft abstention detection
# ---------------------------------------------------------------------------


class TestContainsAbstentionSentence(unittest.TestCase):
    def test_exact_equality_still_counts(self):
        self.assertTrue(evaluate.contains_abstention_sentence(evaluate.ABSTENTION))

    def test_canonical_sentence_after_a_preamble(self):
        text = "Based on the provided context, there is no information about this. " + evaluate.ABSTENTION
        self.assertTrue(evaluate.contains_abstention_sentence(text))

    def test_canonical_sentence_before_trailing_text(self):
        text = evaluate.ABSTENTION + " Let me know if you have another question."
        self.assertTrue(evaluate.contains_abstention_sentence(text))

    def test_not_present_at_all(self):
        self.assertFalse(evaluate.contains_abstention_sentence("I don't know."))

    def test_glued_to_preceding_word_does_not_count(self):
        """Strict boundary check -- alphanumeric directly touching the
        canonical sentence means it's a fragment inside another word, not a
        complete sentence. Punctuation before it (e.g. "Answer: <sentence>")
        is a valid boundary and does count -- only letter/digit adjacency doesn't."""
        self.assertFalse(evaluate.contains_abstention_sentence("Yes" + evaluate.ABSTENTION))
        self.assertTrue(evaluate.contains_abstention_sentence("Answer: " + evaluate.ABSTENTION))

    def test_glued_to_following_word_does_not_count(self):
        self.assertFalse(evaluate.contains_abstention_sentence(evaluate.ABSTENTION + "Thanks"))

    def test_paraphrased_decline_in_the_models_own_words_is_not_detected(self):
        """Deliberately not recognised -- see the docstring: mechanical only,
        no semantic matching for a decline that never uses the exact sentence."""
        self.assertFalse(evaluate.contains_abstention_sentence(
            "I'm sorry, but I don't have enough information in the context to answer that."
        ))


class TestClassifyOutcomeUsesSoftAbstention(unittest.TestCase):
    def test_preamble_plus_canonical_sentence_classifies_as_abstained(self):
        q = question("q1", "factual", transcript_ids=["AAA_2024_Q1"])
        answer = "There is no information about this in the provided context. " + evaluate.ABSTENTION
        result = evaluate.classify_outcome(answer, q, [])
        self.assertEqual(result["outcome"], evaluate.OUTCOME_ABSTAINED)


if __name__ == "__main__":
    unittest.main()
