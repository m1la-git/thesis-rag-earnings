"""Stage 1: retrieval-only evaluation over the 2x3x2 experiment grid.

No generation, no LLM calls, no API cost. Runs the 40 answerable benchmark
questions (factual + thematic + comparative) through each of the 12 conditions
(chunk_size in {200, 500} x retrieval_strategy in {dense, bm25, hybrid} x
indexing_representation in {text_only, metadata_enriched}),
scores retrieval with the existing functions in evaluate.py, and writes a
full audit trail per (condition, question) pair so the logged rankings can
later feed the M5 error taxonomy without re-running anything.

Read-only against every frozen artifact: benchmark/questions.jsonl,
data/corpus_manifest.json, data/processed/transcripts.parquet, and the
chunking/indexing/retrieval/evaluation code in src/. This script only reads
those and writes to results/.

Held constant across all 12 conditions (validated against the code that
actually implements each, not just asserted in JSON -- see
validate_config_matches_code): top_k, the embedding model, the BGE query
prefix, RRF's k, retrieval_scope ("corpus" -- every chunk of all 128
transcripts is a retrieval candidate, not scoped to a question's own
transcript_ids), and the anchor-hit rule (evaluate.chunk_matches_anchor:
exact substring, no normalisation). The ONLY things that vary between
conditions are chunk_size, retrieval_strategy and indexing_representation,
each config file overriding exactly those three keys over configs/base.json.
The six text_only conditions are the original grid, unchanged and not re-run:
under text_only the indexed string is chunk["text"] byte for byte.

Each chunk_size's corpus is chunked ONCE per invocation and shared by both
indexing representations (chunk boundaries and chunk IDs are frozen and
identical in both arms; only the indexed string differs). Each (chunk_size,
indexing_representation) arm is indexed once and reused across all three
strategies for that arm (4 embedding passes for the whole grid, not 12) --
there is no disk cache, because a cache key cannot capture every code path
that produces a chunk (chunking.py, preprocess.py, the embedding model)
without becoming as much machinery as it would save.

Usage
-----
    python src/run_experiment.py                  # all 12 conditions
    python src/run_experiment.py --condition chunk200_dense
    python src/run_experiment.py --verify          # sanity checks only, no run

Output
------
    results/index_text/chunk{size}_{representation}.jsonl
                                              per-chunk prefix_tokens /
                                              truncated / tokens-dropped record,
                                              one file per (size, representation)
    results/retrieval/{condition_id}.jsonl   one run-meta line + 40 question
                                              records; rewritten (not appended)
                                              on every run of that condition
    results/tables/retrieval_metrics.csv     tidy long-format aggregates,
                                              rebuilt from whatever condition
                                              files currently exist on disk
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import evaluate  # noqa: E402
import index as index_mod  # noqa: E402
import ingest  # noqa: E402
import retrieve as retrieve_mod  # noqa: E402
from chunking import EMBEDDING_MODEL_NAME, chunk_transcript  # noqa: E402
from preprocess import preprocess_transcript  # noqa: E402

CONFIGS_DIR = REPO_ROOT / "configs"
BENCHMARK_PATH = REPO_ROOT / "benchmark" / "questions.jsonl"
RETRIEVAL_RESULTS_DIR = REPO_ROOT / "results" / "retrieval"
TABLES_DIR = REPO_ROOT / "results" / "tables"
INDEX_TEXT_STATS_DIR = REPO_ROOT / "results" / "index_text"

# The one place the grid is declared: every configs/chunk*.json file is one
# condition. Nothing below hardcodes a chunk_size/strategy combination.
CHUNK_SIZES = (200, 500)
STRATEGIES = ("dense", "bm25", "hybrid")
REPRESENTATIONS = index_mod.INDEXING_REPRESENTATIONS  # ("text_only", "metadata_enriched")
N_CONDITIONS = len(CHUNK_SIZES) * len(STRATEGIES) * len(REPRESENTATIONS)

# Results persisted before indexing_representation existed have no such key.
# They are the text_only half of the grid by construction, so they are read
# with this default rather than re-run -- see README.md invariant 5.
DEFAULT_REPRESENTATION = index_mod.REPRESENTATION_TEXT_ONLY

RANKING_DEPTH_CAP = 50
ALLOWED_CONDITION_KEYS = {
    "extends",
    "condition_id",
    "chunk_size",
    "retrieval_strategy",
    "indexing_representation",
}


# ---------------------------------------------------------------------------
# Config loading and validation
# ---------------------------------------------------------------------------


def _strip_notes(d: dict) -> dict:
    return {k: v for k, v in d.items() if not k.startswith("_")}


def discover_condition_configs() -> list[Path]:
    """Every condition file in configs/, sorted for a deterministic order."""
    paths = sorted(CONFIGS_DIR.glob("chunk*.json"))
    if len(paths) != N_CONDITIONS:
        raise AssertionError(
            f"expected {N_CONDITIONS} condition configs in {CONFIGS_DIR} "
            f"({len(CHUNK_SIZES)} chunk sizes x {len(STRATEGIES)} strategies x "
            f"{len(REPRESENTATIONS)} indexing representations), "
            f"found {len(paths)}: {[p.name for p in paths]}"
        )
    return paths


def load_config(path: Path) -> dict:
    """Resolve a condition config against its `extends` base.

    Enforces the vary-one-thing-at-a-time rule at the file level: a condition
    file may only override the three independent variables -- chunk_size,
    retrieval_strategy and indexing_representation -- plus the identifying
    extends/condition_id keys. Anything else means a condition is silently
    diverging from the others in a way the design forbids.
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    extra_keys = set(_strip_notes(raw)) - ALLOWED_CONDITION_KEYS
    if extra_keys:
        raise AssertionError(
            f"{path.name} overrides {sorted(extra_keys)}, but a condition file may only set "
            f"{sorted(ALLOWED_CONDITION_KEYS)} -- everything else must come from base.json"
        )

    base_path = CONFIGS_DIR / raw["extends"]
    base = json.loads(base_path.read_text(encoding="utf-8"))

    resolved = {**_strip_notes(base), **_strip_notes(raw)}
    resolved["_source_files"] = [base_path.name, path.name]
    return resolved


def validate_config_matches_code(config: dict) -> None:
    """Assert every value config claims to hold constant is what the code uses.

    Without this, base.json could claim rrf_k=60 while retrieve.py used a
    different constant, and the run log would silently lie about what
    produced its numbers -- the one failure mode worse than a wrong result.
    """
    checks = [
        ("top_k", config["top_k"], evaluate.TOP_K, "evaluate.TOP_K"),
        ("top_k", config["top_k"], retrieve_mod.TOP_K, "retrieve.TOP_K"),
        ("embedding_model", config["embedding_model"], EMBEDDING_MODEL_NAME, "chunking.EMBEDDING_MODEL_NAME"),
        ("query_prefix", config["query_prefix"], index_mod.QUERY_PREFIX, "index.QUERY_PREFIX"),
        ("rrf_k", config["rrf_k"], retrieve_mod.RRF_K, "retrieve.RRF_K"),
        # The frozen enrichment format, cross-checked exactly the way
        # query_prefix is. README.md invariant 2 requires the format to live in
        # one place in the code and be verified against the config; a drift here
        # would mean the run log documents a format the run did not use.
        (
            "indexing_enrichment_prefix_template",
            config["indexing_enrichment_prefix_template"],
            index_mod.ENRICHMENT_PREFIX_TEMPLATE,
            "index.ENRICHMENT_PREFIX_TEMPLATE",
        ),
        (
            "indexing_enrichment_joiner",
            config["indexing_enrichment_joiner"],
            index_mod.ENRICHMENT_JOINER,
            "index.ENRICHMENT_JOINER",
        ),
        (
            "indexing_quarter_prose",
            {int(k): v for k, v in config["indexing_quarter_prose"].items()},
            index_mod.QUARTER_PROSE,
            "index.QUARTER_PROSE",
        ),
        (
            "indexing_section_labels",
            config["indexing_section_labels"],
            index_mod.SECTION_LABELS,
            "index.SECTION_LABELS",
        ),
        (
            "max_content_tokens",
            config["max_content_tokens"],
            index_mod.MAX_CONTENT_TOKENS,
            "index.MAX_CONTENT_TOKENS",
        ),
    ]
    for key, config_value, code_value, code_name in checks:
        if config_value != code_value:
            raise AssertionError(
                f"config {key}={config_value!r} does not match {code_name}={code_value!r} -- "
                "the config and the code it claims to hold constant have drifted apart"
            )

    if config["retrieval_scope"] != "corpus":
        raise AssertionError(
            f"retrieval_scope={config['retrieval_scope']!r} is not implemented; this runner always "
            "retrieves against the full corpus, per the retrieval_scope note in configs/base.json"
        )
    if config["similarity_metric"] != "cosine_bge_small":
        raise AssertionError(
            f"similarity_metric={config['similarity_metric']!r} is not implemented (Stage 1 does not "
            "score similarity at all, but a config that already claims an unsupported value is a bug)"
        )
    if config["chunk_size"] not in CHUNK_SIZES:
        raise AssertionError(f"chunk_size={config['chunk_size']!r} not in {CHUNK_SIZES}")
    if config["retrieval_strategy"] not in STRATEGIES:
        raise AssertionError(f"retrieval_strategy={config['retrieval_strategy']!r} not in {STRATEGIES}")
    if config["indexing_representation"] not in REPRESENTATIONS:
        raise AssertionError(
            f"indexing_representation={config['indexing_representation']!r} not in {REPRESENTATIONS}"
        )


# ---------------------------------------------------------------------------
# Frozen-input hashing (traceability, and a no-network drift check)
# ---------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_corpus_matches_manifest() -> dict:
    """Re-hash the local parquet and diff it against the committed manifest.

    No network call (check_remote=False equivalent) -- this only confirms the
    parquet this process is about to chunk is the exact frozen corpus, not
    that the frozen corpus still matches the Hugging Face revision (that is
    `python src/ingest.py --verify`'s job, and is out of scope for a
    retrieval-only runner).
    """
    import pandas as pd

    manifest = ingest.load_manifest()
    df = pd.read_parquet(ingest.TRANSCRIPTS_PATH)
    problems = ingest.diff_against_manifest(df, manifest, "local parquet")
    if problems:
        raise AssertionError(
            "local transcripts.parquet does not match the committed corpus_manifest.json:\n"
            + "\n".join(problems)
        )
    return manifest


# ---------------------------------------------------------------------------
# Benchmark loading
# ---------------------------------------------------------------------------


def load_questions() -> list[dict]:
    lines = [line for line in BENCHMARK_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [json.loads(line) for line in lines]


def scored_questions(questions: list[dict]) -> list[dict]:
    """The 40 answerable questions Stage 1 actually retrieves for.

    Unanswerable items are excluded here, at the source, rather than scored
    and then discarded -- evaluate.is_retrieval_scored is still the single
    guard; this is just where the runner applies it.
    """
    return [q for q in questions if evaluate.is_retrieval_scored(q)]


# ---------------------------------------------------------------------------
# Corpus chunking / indexing (once per chunk_size, reused across strategies)
# ---------------------------------------------------------------------------


def build_corpus_chunks(chunk_size: int) -> list[dict]:
    """Chunk every transcript in the frozen corpus at `chunk_size` tokens."""
    import pandas as pd

    df = pd.read_parquet(ingest.TRANSCRIPTS_PATH)
    chunks: list[dict] = []
    for _, row in df.iterrows():
        records = preprocess_transcript(row)
        chunks.extend(chunk_transcript(records, chunk_size))
    return chunks


def build_indexes(chunks: list[dict], representation: str):
    """FAISS + BM25 indexes over one chunk set. Order matches `chunks`.

    Computes `index_text` ONCE, here, and hands the identical string to both
    retrievers -- README.md invariant 3. Returns the per-chunk truncation stats
    alongside the indexes so the caller can persist them.

    Both arms are guarded. The treatment arm is guarded inside
    `index.embed_chunks` / `index.build_bm25_index`, which raise rather than
    fall back to `chunk["text"]`. The control arm is guarded here: under
    `text_only`, `index_text` must equal `chunk["text"]` byte for byte, so a
    config typo cannot quietly enrich the baseline.
    """
    stats = index_mod.attach_index_text(chunks, representation)
    if representation == index_mod.REPRESENTATION_TEXT_ONLY:
        index_mod.assert_control_arm_unenriched(chunks)

    embeddings = index_mod.embed_chunks(chunks)
    faiss_index = index_mod.build_faiss_index(embeddings)
    bm25_index = index_mod.build_bm25_index(chunks)
    return faiss_index, bm25_index, stats


def write_index_text_stats(chunk_size: int, representation: str, stats: list[dict]) -> Path:
    """Persist per-chunk truncation bookkeeping for one (size, representation).

    Truncation has to be recorded, not just performed: under
    `metadata_enriched` the prefix pushes 500-token chunks past the encoder's
    content budget and some transcript tokens are dropped from what is indexed.
    Written once per (chunk_size, representation) rather than per condition,
    because it does not depend on the retrieval strategy.
    """
    INDEX_TEXT_STATS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = INDEX_TEXT_STATS_DIR / f"chunk{chunk_size}_{representation}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for row in stats:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return out_path


# ---------------------------------------------------------------------------
# Per-condition run
# ---------------------------------------------------------------------------


def _ranking_log(retrieved: list[dict]) -> list[dict]:
    return [
        {"rank": i + 1, "chunk_id": c["chunk_id"], "score": c["score"], "text": c["text"]}
        for i, c in enumerate(retrieved)
    ]


def _anchor_detail(retrieved: list[dict], question: dict) -> list[dict]:
    """Per-anchor match detail against the FULL logged ranking (not top-5)."""
    detail = []
    for anchor in evaluate.anchor_strings(question):
        rank = evaluate.first_match_rank(retrieved, anchor, k=len(retrieved))
        detail.append(
            {
                "anchor": anchor,
                "matched": rank is not None,
                "chunk_id": retrieved[rank - 1]["chunk_id"] if rank is not None else None,
                "rank": rank,
            }
        )
    return detail


def run_condition(
    config: dict,
    chunks: list[dict],
    faiss_index,
    bm25_index,
    questions: list[dict],
    manifest_sha256: str,
    benchmark_sha256: str,
) -> tuple[dict, list[dict]]:
    """Run one condition over all scored questions. Returns (run_meta, records)."""
    strategy = config["retrieval_strategy"]
    depth_cap = min(RANKING_DEPTH_CAP, len(chunks))

    run_meta = {
        "_type": "run_meta",
        "condition_id": config["condition_id"],
        "chunk_size": config["chunk_size"],
        "retrieval_strategy": strategy,
        "indexing_representation": config["indexing_representation"],
        "embedding_model": config["embedding_model"],
        "top_k": config["top_k"],
        "rrf_k": config["rrf_k"] if strategy == "hybrid" else None,
        "seed": config["seed"],
        "ranking_depth_cap": depth_cap,
        "n_corpus_chunks": len(chunks),
        "n_questions": len(questions),
        "corpus_manifest_sha256": manifest_sha256,
        "benchmark_file_sha256": benchmark_sha256,
        "config_source_files": config["_source_files"],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    records = []
    for q in questions:
        retrieved = retrieve_mod.retrieve(q["question"], strategy, faiss_index, bm25_index, chunks, k=depth_cap)
        top_k = retrieved[: config["top_k"]]

        record = {
            "_type": "question_result",
            "condition_id": config["condition_id"],
            "chunk_size": config["chunk_size"],
            "retrieval_strategy": strategy,
            "question_id": q["id"],
            "category": q["category"],
            "chunk_size_sensitive": q.get("chunk_size_sensitive"),
            "difficulty_level": q.get("difficulty_level"),
            "retrieval_difficulty": q.get("retrieval_difficulty"),
            "faithfulness_difficulty": q.get("faithfulness_difficulty"),
            "subtype": q.get("subtype"),
            "transcript_ids": q["transcript_ids"],
            "retrieval_metrics": evaluate.score_retrieval(q, top_k, k=config["top_k"]),
            "anchor_detail": _anchor_detail(retrieved, q),
            "ranking": _ranking_log(retrieved),
        }
        records.append(record)

    return run_meta, records


def write_condition_results(run_meta: dict, records: list[dict]) -> Path:
    """Write one condition's run-meta + records, overwriting cleanly."""
    RETRIEVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RETRIEVAL_RESULTS_DIR / f"{run_meta['condition_id']}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(run_meta, ensure_ascii=False) + "\n")
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return out_path


# ---------------------------------------------------------------------------
# Reading back persisted results (used by aggregation and sanity checks alike,
# so --verify and a normal run report on exactly the same data)
# ---------------------------------------------------------------------------


def read_condition_file(path: Path) -> tuple[dict, list[dict]]:
    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    meta = next(line for line in lines if line["_type"] == "run_meta")
    records = [line for line in lines if line["_type"] == "question_result"]
    return meta, records


def read_all_persisted_results() -> dict[str, tuple[dict, list[dict]]]:
    """condition_id -> (run_meta, records) for every condition file currently on disk."""
    if not RETRIEVAL_RESULTS_DIR.exists():
        return {}
    out = {}
    for path in sorted(RETRIEVAL_RESULTS_DIR.glob("*.jsonl")):
        meta, records = read_condition_file(path)
        out[meta["condition_id"]] = (meta, records)
    return out


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

METRICS = ("anchor_coverage_at_5", "mean_reciprocal_rank_at_5")


def aggregate_breakdowns(run_meta: dict, records: list[dict]) -> list[dict]:
    """Tidy long-format rows: overall, by category, by chunk_size_sensitive.

    Overall is included but explicitly labeled non-cross-category-comparable
    -- factual questions score 0/1, multi-anchor items score across several
    levels, so a mean across categories is not a headline figure. It exists
    here only so check_unanswerable_exclusion has an n_scored=40 to check.
    """
    rows: list[dict] = []

    def emit(breakdown_type: str, breakdown_value: str, subset: list[dict]) -> None:
        scores = [r["retrieval_metrics"] for r in subset]
        agg = evaluate.aggregate_retrieval(scores)
        for metric in METRICS:
            rows.append(
                {
                    "condition_id": run_meta["condition_id"],
                    "chunk_size": run_meta["chunk_size"],
                    "retrieval_strategy": run_meta["retrieval_strategy"],
                    "indexing_representation": run_meta.get("indexing_representation", DEFAULT_REPRESENTATION),
                    "breakdown_type": breakdown_type,
                    "breakdown_value": breakdown_value,
                    "metric": metric,
                    "value": agg[metric],
                    "n_scored": agg[f"{metric}_n_scored"],
                }
            )

    emit("overall_not_cross_category_comparable", "all", records)
    for category in ("factual", "thematic", "comparative"):
        emit("category", category, [r for r in records if r["category"] == category])
    for flag in (True, False):
        emit("chunk_size_sensitive", str(flag), [r for r in records if r["chunk_size_sensitive"] == flag])

    return rows


def write_tables(all_rows: list[dict]) -> Path:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TABLES_DIR / "retrieval_metrics.csv"
    fieldnames = [
        "condition_id",
        "chunk_size",
        "retrieval_strategy",
        "indexing_representation",
        "breakdown_type",
        "breakdown_value",
        "metric",
        "value",
        "n_scored",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    return out_path


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------


class SanityCheckFailure(Exception):
    pass


def check_anchor_reachability(questions: list[dict]) -> str:
    """Every gold anchor of every scored question matches at least one chunk,
    scoped to its own transcript_ids, under BOTH 200 and 500 token chunking.

    Rebuilds chunks only for the transcripts referenced by scored questions
    (not the full 128-transcript corpus) since this check needs chunk text,
    not an index -- it runs in seconds and needs no embedding model.
    """
    import pandas as pd

    scored = scored_questions(questions)
    needed = sorted({tid for q in scored for tid in q["transcript_ids"]})
    df = pd.read_parquet(ingest.TRANSCRIPTS_PATH)
    df = df[df["transcript_id"].isin(needed)]

    chunks_by_size: dict[int, dict[str, list[dict]]] = {size: {} for size in CHUNK_SIZES}
    for _, row in df.iterrows():
        records = preprocess_transcript(row)
        for size in CHUNK_SIZES:
            chunks_by_size[size][row["transcript_id"]] = chunk_transcript(records, size)

    failures = []
    for q in scored:
        for anchor in evaluate.anchor_strings(q):
            for size in CHUNK_SIZES:
                hit = any(
                    evaluate.chunk_matches_anchor(c, anchor)
                    for tid in q["transcript_ids"]
                    for c in chunks_by_size[size].get(tid, [])
                )
                if not hit:
                    failures.append(f"{q['id']}: anchor {anchor!r} not reachable under chunk_size={size}")

    if failures:
        raise SanityCheckFailure(
            f"anchor reachability: {len(failures)} anchor(s) unreachable\n" + "\n".join(failures)
        )
    n_anchors = sum(len(evaluate.anchor_strings(q)) for q in scored)
    return f"anchor reachability: {n_anchors}/{n_anchors} anchors reachable under both chunk sizes ({len(scored)} questions)"


def check_unanswerable_exclusion(questions: list[dict], persisted: dict) -> str:
    n_scored_expected = len(scored_questions(questions))
    problems = []
    for condition_id, (run_meta, records) in persisted.items():
        agg = evaluate.aggregate_retrieval([r["retrieval_metrics"] for r in records])
        if agg["anchor_coverage_at_5_n_scored"] != n_scored_expected:
            problems.append(
                f"{condition_id}: n_scored={agg['anchor_coverage_at_5_n_scored']}, expected {n_scored_expected}"
            )
        if any(r["category"] not in evaluate.RETRIEVAL_SCORED_CATEGORIES for r in records):
            problems.append(f"{condition_id}: an unanswerable question leaked into the retrieval-scored records")
    if problems:
        raise SanityCheckFailure("unanswerable exclusion:\n" + "\n".join(problems))
    return f"unanswerable exclusion: n_scored={n_scored_expected} in every persisted condition, no unanswerable leakage"


def check_grid_completeness(questions: list[dict], persisted: dict) -> str:
    """Only meaningful once all 12 conditions have been persisted; reports
    partial-grid status rather than failing when fewer are present, since a
    single --condition run is a legitimate use of this script.
    """
    expected_conditions = {p.stem for p in discover_condition_configs()}
    have_conditions = set(persisted)
    if have_conditions != expected_conditions:
        missing = expected_conditions - have_conditions
        return (
            f"grid completeness: SKIPPED -- {len(have_conditions)}/{N_CONDITIONS} conditions "
            f"persisted, missing {sorted(missing)}"
        )

    n_scored = len(scored_questions(questions))
    seen_pairs = set()
    duplicates = []
    for condition_id, (_, records) in persisted.items():
        for r in records:
            pair = (condition_id, r["question_id"])
            if pair in seen_pairs:
                duplicates.append(pair)
            seen_pairs.add(pair)

    total_rows = sum(len(records) for _, records in persisted.values())
    expected_total = N_CONDITIONS * n_scored
    if total_rows != expected_total or duplicates:
        raise SanityCheckFailure(
            f"grid completeness: {total_rows} rows, expected {expected_total}; "
            f"{len(duplicates)} duplicate (condition, question) pairs: {duplicates[:5]}"
        )
    return (
        f"grid completeness: {total_rows}/{expected_total} rows, "
        f"{N_CONDITIONS}/{N_CONDITIONS} conditions, no duplicates"
    )


def check_non_degenerate(questions: list[dict], persisted: dict) -> str:
    if not persisted:
        return "non-degenerate output: SKIPPED -- no persisted conditions"

    easy_factual_ids = {
        q["id"] for q in scored_questions(questions) if q["category"] == "factual" and q.get("difficulty_level") == "easy"
    }
    hits = [
        (condition_id, r["question_id"])
        for condition_id, (_, records) in persisted.items()
        for r in records
        if r["question_id"] in easy_factual_ids and r["retrieval_metrics"]["anchor_coverage_at_5"] == 1.0
    ]
    if not hits:
        raise SanityCheckFailure(
            f"non-degenerate output: none of {len(easy_factual_ids)} easy factual questions reached "
            "coverage 1.0 in any persisted condition -- suspect a plumbing bug, not weak retrieval"
        )
    return f"non-degenerate output: {len(hits)} (condition, easy-factual-question) pair(s) reached coverage 1.0"


def check_chunk_size_sensitivity(questions: list[dict], persisted: dict) -> str:
    sensitive_ids = {q["id"] for q in scored_questions(questions) if q.get("chunk_size_sensitive")}

    # Keyed by (strategy, representation, chunk_size), NOT (strategy, chunk_size).
    # With 12 conditions the two representations share every (strategy, size)
    # pair, so the narrower key silently overwrote one arm with the other and
    # the check then passed while comparing chunk200_dense against
    # chunk500_dense_enriched -- a 200-vs-500 delta confounded with
    # text_only-vs-enriched. The representation has to be part of the key for
    # this check to be comparing what it claims to compare.
    by_arm_size: dict[tuple[str, str, int], dict[str, dict]] = {}
    for condition_id, (run_meta, records) in persisted.items():
        key = (
            run_meta["retrieval_strategy"],
            run_meta.get("indexing_representation", DEFAULT_REPRESENTATION),
            run_meta["chunk_size"],
        )
        if key in by_arm_size:
            raise SanityCheckFailure(
                f"chunk-size sensitivity: two persisted conditions share the arm key {key} "
                f"({condition_id} collides) -- one would overwrite the other"
            )
        by_arm_size[key] = {r["question_id"]: r["retrieval_metrics"] for r in records if r["question_id"] in sensitive_ids}

    arms_with_both_sizes = [
        (strategy, representation)
        for strategy in STRATEGIES
        for representation in REPRESENTATIONS
        if (strategy, representation, 200) in by_arm_size and (strategy, representation, 500) in by_arm_size
    ]
    if not arms_with_both_sizes:
        return (
            "chunk-size sensitivity: SKIPPED -- need both chunk sizes persisted for at least one "
            "(strategy, indexing_representation) arm"
        )

    deltas = []
    for strategy, representation in arms_with_both_sizes:
        scores_200 = by_arm_size[(strategy, representation, 200)]
        scores_500 = by_arm_size[(strategy, representation, 500)]
        for qid in sensitive_ids:
            for metric in METRICS:
                v200 = scores_200.get(qid, {}).get(metric)
                v500 = scores_500.get(qid, {}).get(metric)
                if v200 is not None and v500 is not None:
                    deltas.append(
                        {
                            "strategy": strategy,
                            "indexing_representation": representation,
                            "question_id": qid,
                            "metric": metric,
                            "delta": v500 - v200,
                        }
                    )

    total_variation = sum(abs(d["delta"]) for d in deltas)
    if total_variation == 0.0:
        raise SanityCheckFailure(
            f"chunk-size sensitivity: all {len(deltas)} 200-vs-500 deltas on the "
            f"{len(sensitive_ids)} chunk_size_sensitive items are exactly zero across "
            f"{arms_with_both_sizes} -- investigate before trusting this run"
        )
    return (
        f"chunk-size sensitivity: {len(sensitive_ids)} items x {len(arms_with_both_sizes)} arm(s) "
        f"{arms_with_both_sizes}, mean |delta|={total_variation / len(deltas):.3f} over "
        f"{len(deltas)} (strategy, representation, item, metric) tuples"
    )


def run_sanity_checks(questions: list[dict], persisted: dict) -> list[str]:
    """Run every check; collect failures instead of stopping at the first one
    so a single run reports everything wrong, not just the first problem.
    """
    checks = [
        lambda: check_anchor_reachability(questions),
        lambda: check_unanswerable_exclusion(questions, persisted),
        lambda: check_grid_completeness(questions, persisted),
        lambda: check_non_degenerate(questions, persisted),
        lambda: check_chunk_size_sensitivity(questions, persisted),
    ]
    results = []
    failures = []
    for check in checks:
        try:
            results.append("PASS: " + check())
        except SanityCheckFailure as e:
            results.append("FAIL: " + str(e))
            failures.append(str(e))

    print("\n".join(results))
    if failures:
        raise SanityCheckFailure(f"{len(failures)} sanity check(s) failed")
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--condition", help="condition_id to run (e.g. chunk200_dense); omit to run all 12"
    )
    parser.add_argument("--verify", action="store_true", help="run sanity checks against persisted results only, no retrieval")
    args = parser.parse_args()

    questions = load_questions()
    scored = scored_questions(questions)

    if args.verify:
        persisted = read_all_persisted_results()
        print(f"verifying {len(persisted)} persisted condition(s) against {len(scored)} scored questions\n")
        try:
            run_sanity_checks(questions, persisted)
        except SanityCheckFailure:
            return 1
        return 0

    manifest = verify_corpus_matches_manifest()
    manifest_sha256 = sha256_file(ingest.MANIFEST_PATH)
    benchmark_sha256 = sha256_file(BENCHMARK_PATH)
    print(f"corpus verified against manifest ({manifest['n_transcripts']} transcripts, "
          f"revision {manifest['revision'][:12]})")

    all_config_paths = discover_condition_configs()
    if args.condition:
        all_config_paths = [p for p in all_config_paths if p.stem == args.condition]
        if not all_config_paths:
            raise SystemExit(f"no condition config named {args.condition!r} in {CONFIGS_DIR}")

    configs = [load_config(p) for p in all_config_paths]
    for config in configs:
        validate_config_matches_code(config)

    # Grouped by (chunk_size, indexing_representation): the chunk set depends
    # only on chunk_size, but the indexed string depends on both, so each arm
    # needs its own embedding pass. Chunking is done once per size and reused
    # across that size's representations -- chunk boundaries and chunk IDs are
    # frozen and identical in both arms; only the indexed string differs.
    configs_by_arm: dict[tuple[int, str], list[dict]] = {}
    for config in configs:
        configs_by_arm.setdefault((config["chunk_size"], config["indexing_representation"]), []).append(config)

    chunks_by_size: dict[int, list[dict]] = {}
    for (chunk_size, representation), arm_configs in sorted(configs_by_arm.items()):
        if chunk_size not in chunks_by_size:
            print(f"\nchunk_size={chunk_size}: chunking full corpus...")
            chunks_by_size[chunk_size] = build_corpus_chunks(chunk_size)
        chunks = chunks_by_size[chunk_size]

        print(
            f"\nchunk_size={chunk_size}, indexing_representation={representation}: "
            f"{len(chunks)} chunks; building FAISS + BM25 indexes..."
        )
        faiss_index, bm25_index, index_stats = build_indexes(chunks, representation)
        stats_path = write_index_text_stats(chunk_size, representation, index_stats)
        n_truncated = sum(1 for row in index_stats if row["truncated"])
        print(
            f"  index_text: {n_truncated}/{len(index_stats)} chunk(s) truncated "
            f"-> {stats_path.relative_to(REPO_ROOT)}"
        )

        for config in arm_configs:
            print(f"  running {config['condition_id']} ({config['retrieval_strategy']})...")
            run_meta, records = run_condition(
                config, chunks, faiss_index, bm25_index, scored, manifest_sha256, benchmark_sha256
            )
            out_path = write_condition_results(run_meta, records)
            print(f"    -> {out_path.relative_to(REPO_ROOT)} ({len(records)} records)")

    persisted = read_all_persisted_results()
    all_rows = []
    for condition_id, (run_meta, records) in persisted.items():
        all_rows.extend(aggregate_breakdowns(run_meta, records))
    table_path = write_tables(all_rows)
    print(f"\naggregates -> {table_path.relative_to(REPO_ROOT)} ({len(all_rows)} rows)")

    print()
    try:
        run_sanity_checks(questions, persisted)
    except SanityCheckFailure:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
