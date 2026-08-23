"""Unit tests for src/run_experiment.py's own logic: config validation,
aggregation, and the sanity checks. Metric correctness is already covered by
tests/test_evaluate.py -- these tests only exercise plumbing this file adds.

    python -m unittest discover -s tests -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import run_experiment as re  # noqa: E402


def question(id_, category, anchors=None, transcript_ids=None, **extra):
    return {
        "id": id_,
        "category": category,
        "question": f"question {id_}",
        "transcript_ids": transcript_ids or ["T1"],
        "gold_anchors": anchors if anchors is not None else (["anchor text"] if category != "unanswerable" else []),
        "reference_answer": None if category == "unanswerable" else "ref",
        "difficulty_level": extra.pop("difficulty_level", "medium"),
        "chunk_size_sensitive": extra.pop("chunk_size_sensitive", False),
        **extra,
    }


def record(question_id, category, coverage, mrr, chunk_size_sensitive=False):
    return {
        "_type": "question_result",
        "question_id": question_id,
        "category": category,
        "chunk_size_sensitive": chunk_size_sensitive,
        "difficulty_level": "medium",
        "retrieval_metrics": {"anchor_coverage_at_5": coverage, "mean_reciprocal_rank_at_5": mrr},
    }


def run_meta(condition_id, chunk_size, strategy, indexing_representation=None):
    """A persisted run_meta line.

    `indexing_representation` is omitted by default on purpose: the six
    conditions persisted before that field existed have no such key, and the
    code must keep reading them (as text_only) rather than requiring a re-run.
    """
    meta = {
        "_type": "run_meta",
        "condition_id": condition_id,
        "chunk_size": chunk_size,
        "retrieval_strategy": strategy,
    }
    if indexing_representation is not None:
        meta["indexing_representation"] = indexing_representation
    return meta


def valid_config(**overrides):
    """A resolved config that agrees with the code on every cross-checked value.

    Built from the code's own constants so a test cannot pass by restating a
    stale copy of the frozen enrichment format. Tests override one key at a
    time to check that the drift detection actually fires.
    """
    config = {
        "top_k": re.evaluate.TOP_K,
        "embedding_model": re.EMBEDDING_MODEL_NAME,
        "query_prefix": re.index_mod.QUERY_PREFIX,
        "rrf_k": re.retrieve_mod.RRF_K,
        "retrieval_scope": "corpus",
        "similarity_metric": "cosine_bge_small",
        "chunk_size": 200,
        "retrieval_strategy": "dense",
        "indexing_representation": "text_only",
        "indexing_enrichment_prefix_template": re.index_mod.ENRICHMENT_PREFIX_TEMPLATE,
        "indexing_enrichment_joiner": re.index_mod.ENRICHMENT_JOINER,
        "indexing_quarter_prose": {str(k): v for k, v in re.index_mod.QUARTER_PROSE.items()},
        "indexing_section_labels": dict(re.index_mod.SECTION_LABELS),
        "max_content_tokens": re.index_mod.MAX_CONTENT_TOKENS,
    }
    config.update(overrides)
    return config


class TestConfigValidation(unittest.TestCase):
    def test_condition_file_may_only_override_allowed_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "base.json").write_text(json.dumps({"top_k": 5}), encoding="utf-8")
            (tmp_path / "bad.json").write_text(
                json.dumps({"extends": "base.json", "condition_id": "bad", "chunk_size": 200,
                            "retrieval_strategy": "dense", "top_k": 10}),
                encoding="utf-8",
            )
            original_dir = re.CONFIGS_DIR
            re.CONFIGS_DIR = tmp_path
            try:
                with self.assertRaises(AssertionError):
                    re.load_config(tmp_path / "bad.json")
            finally:
                re.CONFIGS_DIR = original_dir

    def test_condition_file_extends_and_overrides_merge(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "base.json").write_text(json.dumps({"top_k": 5, "seed": 1}), encoding="utf-8")
            (tmp_path / "good.json").write_text(
                json.dumps({"extends": "base.json", "condition_id": "good", "chunk_size": 200,
                            "retrieval_strategy": "dense"}),
                encoding="utf-8",
            )
            original_dir = re.CONFIGS_DIR
            re.CONFIGS_DIR = tmp_path
            try:
                resolved = re.load_config(tmp_path / "good.json")
            finally:
                re.CONFIGS_DIR = original_dir
            self.assertEqual(resolved["top_k"], 5)
            self.assertEqual(resolved["seed"], 1)
            self.assertEqual(resolved["chunk_size"], 200)
            self.assertEqual(resolved["retrieval_strategy"], "dense")

    def test_validate_config_matches_code_passes_for_real_base_config(self):
        re.validate_config_matches_code(valid_config())  # should not raise

    def test_validate_config_matches_code_catches_drift(self):
        with self.assertRaises(AssertionError):
            re.validate_config_matches_code(valid_config(top_k=re.evaluate.TOP_K + 1))

    def test_validate_config_catches_enrichment_format_drift(self):
        """The frozen enrichment format is cross-checked exactly like
        query_prefix: a config claiming a format the code does not implement
        would make every enriched run log lie about what produced it."""
        for key, bad in [
            ("indexing_enrichment_prefix_template", "{ticker} {year}"),
            ("indexing_enrichment_joiner", " "),
            ("indexing_quarter_prose", {"1": "Q1", "2": "Q2", "3": "Q3", "4": "Q4"}),
            ("indexing_section_labels", {"prepared_remarks": "prepared", "qa": "qa"}),
            ("max_content_tokens", 502),
        ]:
            with self.subTest(key=key), self.assertRaises(AssertionError):
                re.validate_config_matches_code(valid_config(**{key: bad}))

    def test_validate_config_rejects_unknown_indexing_representation(self):
        with self.assertRaises(AssertionError):
            re.validate_config_matches_code(valid_config(indexing_representation="enriched"))

    def test_validate_config_rejects_unsupported_retrieval_scope(self):
        with self.assertRaises(AssertionError):
            re.validate_config_matches_code(valid_config(retrieval_scope="transcript"))


class TestAggregateBreakdowns(unittest.TestCase):
    def test_breakdowns_cover_overall_category_and_sensitivity(self):
        meta = run_meta("chunk200_dense", 200, "dense")
        records = [
            record("q1", "factual", 1.0, 1.0, chunk_size_sensitive=True),
            record("q2", "factual", 0.0, 0.0, chunk_size_sensitive=False),
            record("q3", "thematic", 0.5, 0.5, chunk_size_sensitive=False),
        ]
        rows = re.aggregate_breakdowns(meta, records)
        breakdowns = {(r["breakdown_type"], r["breakdown_value"], r["metric"]) for r in rows}

        self.assertIn(("overall_not_cross_category_comparable", "all", "anchor_coverage_at_5"), breakdowns)
        self.assertIn(("category", "factual", "anchor_coverage_at_5"), breakdowns)
        self.assertIn(("category", "thematic", "anchor_coverage_at_5"), breakdowns)
        self.assertIn(("chunk_size_sensitive", "True", "anchor_coverage_at_5"), breakdowns)
        self.assertIn(("chunk_size_sensitive", "False", "anchor_coverage_at_5"), breakdowns)

        factual_row = next(
            r for r in rows if r["breakdown_type"] == "category" and r["breakdown_value"] == "factual"
            and r["metric"] == "anchor_coverage_at_5"
        )
        self.assertAlmostEqual(factual_row["value"], 0.5)
        self.assertEqual(factual_row["n_scored"], 2)

    def test_overall_breakdown_is_labeled_not_comparable(self):
        meta = run_meta("chunk200_dense", 200, "dense")
        records = [record("q1", "factual", 1.0, 1.0)]
        rows = re.aggregate_breakdowns(meta, records)
        overall_types = {r["breakdown_type"] for r in rows if r["breakdown_value"] == "all"}
        self.assertEqual(overall_types, {"overall_not_cross_category_comparable"})


class TestSanityChecks(unittest.TestCase):
    def _questions(self):
        return [
            question("q1", "factual", difficulty_level="easy"),
            question("q2", "factual", difficulty_level="hard"),
            question("q3", "thematic", chunk_size_sensitive=True),
            question("q4", "unanswerable", anchors=[], transcript_ids=[]),
        ]

    def test_unanswerable_exclusion_passes_when_n_scored_matches(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (
                run_meta("chunk200_dense", 200, "dense"),
                [record("q1", "factual", 1.0, 1.0), record("q2", "factual", 0.0, 0.0), record("q3", "thematic", 0.5, 0.5)],
            )
        }
        re.check_unanswerable_exclusion(questions, persisted)  # should not raise

    def test_unanswerable_exclusion_fails_on_wrong_n_scored(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (
                run_meta("chunk200_dense", 200, "dense"),
                [record("q1", "factual", 1.0, 1.0)],  # only 1, expected 3 scored questions
            )
        }
        with self.assertRaises(re.SanityCheckFailure):
            re.check_unanswerable_exclusion(questions, persisted)

    def test_non_degenerate_passes_when_an_easy_factual_hits_full_coverage(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (run_meta("chunk200_dense", 200, "dense"), [record("q1", "factual", 1.0, 1.0)])
        }
        re.check_non_degenerate(questions, persisted)  # should not raise

    def test_non_degenerate_fails_when_nothing_scores_well(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (run_meta("chunk200_dense", 200, "dense"), [record("q1", "factual", 0.3, 0.2)])
        }
        with self.assertRaises(re.SanityCheckFailure):
            re.check_non_degenerate(questions, persisted)

    def test_grid_completeness_skips_when_conditions_missing(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (run_meta("chunk200_dense", 200, "dense"), [record("q1", "factual", 1.0, 1.0)])
        }
        result = re.check_grid_completeness(questions, persisted)
        self.assertIn("SKIPPED", result)

    def test_chunk_size_sensitivity_fails_on_zero_variation(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (
                run_meta("chunk200_dense", 200, "dense"),
                [record("q3", "thematic", 0.5, 0.5, chunk_size_sensitive=True)],
            ),
            "chunk500_dense": (
                run_meta("chunk500_dense", 500, "dense"),
                [record("q3", "thematic", 0.5, 0.5, chunk_size_sensitive=True)],
            ),
        }
        with self.assertRaises(re.SanityCheckFailure):
            re.check_chunk_size_sensitivity(questions, persisted)

    def test_chunk_size_sensitivity_passes_on_nonzero_variation(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (
                run_meta("chunk200_dense", 200, "dense"),
                [record("q3", "thematic", 0.5, 0.5, chunk_size_sensitive=True)],
            ),
            "chunk500_dense": (
                run_meta("chunk500_dense", 500, "dense"),
                [record("q3", "thematic", 1.0, 1.0, chunk_size_sensitive=True)],
            ),
        }
        re.check_chunk_size_sensitivity(questions, persisted)  # should not raise

    def test_chunk_size_sensitivity_skips_with_only_one_chunk_size(self):
        questions = self._questions()
        persisted = {
            "chunk200_dense": (
                run_meta("chunk200_dense", 200, "dense"),
                [record("q3", "thematic", 0.5, 0.5, chunk_size_sensitive=True)],
            )
        }
        result = re.check_chunk_size_sensitivity(questions, persisted)
        self.assertIn("SKIPPED", result)


class TestAnchorAndRankingHelpers(unittest.TestCase):
    def test_anchor_detail_records_matched_rank_and_chunk_id(self):
        retrieved = [
            {"chunk_id": "c1", "text": "irrelevant filler"},
            {"chunk_id": "c2", "text": "contains the target anchor text right here"},
            {"chunk_id": "c3", "text": "irrelevant filler"},
        ]
        q = question("q1", "factual", anchors=["target anchor text"])
        detail = re._anchor_detail(retrieved, q)
        self.assertEqual(len(detail), 1)
        self.assertTrue(detail[0]["matched"])
        self.assertEqual(detail[0]["chunk_id"], "c2")
        self.assertEqual(detail[0]["rank"], 2)

    def test_anchor_detail_reports_unmatched_as_none(self):
        retrieved = [{"chunk_id": "c1", "text": "irrelevant filler"}]
        q = question("q1", "factual", anchors=["never appears anywhere"])
        detail = re._anchor_detail(retrieved, q)
        self.assertFalse(detail[0]["matched"])
        self.assertIsNone(detail[0]["chunk_id"])
        self.assertIsNone(detail[0]["rank"])

    def test_ranking_log_preserves_rank_order_and_fields(self):
        retrieved = [
            {"chunk_id": "c1", "text": "a", "score": 0.9, "extra": "ignored"},
            {"chunk_id": "c2", "text": "b", "score": 0.5},
        ]
        log = re._ranking_log(retrieved)
        self.assertEqual(log[0], {"rank": 1, "chunk_id": "c1", "score": 0.9, "text": "a"})
        self.assertEqual(log[1], {"rank": 2, "chunk_id": "c2", "score": 0.5, "text": "b"})


class TestDiscoverConditionConfigs(unittest.TestCase):
    def test_discovers_exactly_twelve_real_condition_files(self):
        paths = re.discover_condition_configs()
        self.assertEqual(len(paths), 12)
        self.assertEqual(re.N_CONDITIONS, 12)
        stems = {p.stem for p in paths}
        expected = {
            f"chunk{size}_{strategy}" + ("" if representation == "text_only" else "_enriched")
            for size in re.CHUNK_SIZES
            for strategy in re.STRATEGIES
            for representation in re.REPRESENTATIONS
        }
        self.assertEqual(stems, expected)

    def test_existing_six_condition_ids_are_unchanged(self):
        """The text_only half keeps its original names, so the persisted
        results, the analysis tables and the generation cache all still key on
        the same condition_ids they were written under."""
        stems = {p.stem for p in re.discover_condition_configs()}
        for size in re.CHUNK_SIZES:
            for strategy in re.STRATEGIES:
                self.assertIn(f"chunk{size}_{strategy}", stems)

    def test_condition_ids_are_unique_across_the_whole_grid(self):
        """Analysis scripts key rows by (question_id, condition_id). That is
        only safe if condition_id alone distinguishes all 12 conditions."""
        ids = [re.load_config(p)["condition_id"] for p in re.discover_condition_configs()]
        self.assertEqual(len(set(ids)), len(ids))
        self.assertEqual(len(ids), 12)

    def test_every_condition_declares_a_valid_indexing_representation(self):
        for path in re.discover_condition_configs():
            config = re.load_config(path)
            with self.subTest(condition=config["condition_id"]):
                self.assertIn(config["indexing_representation"], re.REPRESENTATIONS)
                expected = "metadata_enriched" if path.stem.endswith("_enriched") else "text_only"
                self.assertEqual(config["indexing_representation"], expected)


if __name__ == "__main__":
    unittest.main()
