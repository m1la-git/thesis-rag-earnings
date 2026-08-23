"""Stage 2 full grid: generation over the condition grid, local Qwen only.

The generator is served locally through LM Studio; the model is named by
`LM_STUDIO_MODEL_NAME` and is part of every cache key (see README.md,
"Generator runs").

Architecture:

- For the 40 answerable questions, each condition's top-5 chunks come
  straight from Stage 1's persisted `results/retrieval/{condition_id}.jsonl`.
  Retrieval is NOT re-run for these.
- For the 5 unanswerable questions, Stage 1 never retrieved anything for them
  (correctly -- they're not retrieval-scored). Their retrieval is computed
  fresh, per condition, using that condition's own chunk_size/strategy, cached under
  results/generation/case_a_retrieval/{condition_id}.json -- never written
  into results/retrieval/ (Stage 1's directory).
- Each (chunk_size, indexing_representation) arm's FAISS/BM25 indexes are
  built once and reused across that arm's 3 strategies; chunking is done once
  per chunk_size and shared by both representations (mirrors
  run_experiment.py). Chunk boundaries and chunk IDs are identical in both
  arms -- only the indexed string differs.

Caching and crash safety: one JSON file per (model, condition_id, question_id)
under results/generation/{model_slug}/{condition_id}/{question_id}.json,
written the instant each generation completes -- not batched behind
asyncio.gather's all-or-nothing semantics. A per-item exception is caught and
logged, not raised, so one bad call can't take down the rest of a 45-item
batch. A re-run skips every entry already cached FOR THE MODEL BEING RUN: the
model is part of the key, and a record whose own `model` field disagrees with
the running model counts as a miss, so two generators can never share a cache
slot.

Scoring (case + outcome classification, plus descriptive BERTScore/cosine on
Case C) is a separate, fast, always-safe-to-rerun pass over whatever's cached
-- `--score-only` runs just that, no generation, no API/LM Studio calls.

Output location is scoped twice, because there are two ways to clobber a
published table. By MODEL: the tables live in results/tables/{model_slug}/,
mirroring the generation cache, so a run under a different generator cannot
overwrite another generator's published results. By CONDITION SET: a run over
any subset (i.e. `--condition`) nests one level deeper again, in
.../subset/{condition_ids}/, so a single-condition run cannot replace the
full-grid tables with its own 45 rows. `assert_no_model_mismatch` refuses the
write outright if a target file turns out to belong to another model anyway.

Usage:
    python src/run_generation.py                 generate (skips cached) + score
    python src/run_generation.py --condition chunk200_hybrid   one condition + score
    python src/run_generation.py --score-only     rescore cached generations only
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import evaluate  # noqa: E402
import generate as generate_mod  # noqa: E402
from generate import ABSTENTION, SYSTEM_PROMPT, TEMPERATURE, format_context  # noqa: E402
from model_paths import model_slug as _model_slug  # noqa: E402
from retrieve import retrieve as retrieve_fn  # noqa: E402
from run_experiment import (  # noqa: E402
    build_corpus_chunks,
    build_indexes,
    discover_condition_configs,
    load_config,
)

STAGE1_DIR = REPO_ROOT / "results" / "retrieval"
GEN_DIR = REPO_ROOT / "results" / "generation"
CASE_A_DIR = GEN_DIR / "case_a_retrieval"
TABLES_DIR = REPO_ROOT / "results" / "tables"
BENCHMARK_PATH = REPO_ROOT / "benchmark" / "questions.jsonl"

SEED = 20260831
LOCAL_MAX_CONCURRENCY = 4
PROMPT_HASH = hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest()[:16]
UNANSWERABLE_QIDS = ["ref_unans_01", "ref_unans_02", "ref_unans_03", "ref_unans_05", "ref_unans_06"]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


# `model_slug` is defined once, in src/model_paths.py, and re-exported here for
# the callers that already import it from this module. The cache is keyed by
# (model, condition_id, question_id): without the model dimension, switching
# generators silently reuses the previous model's answers under the new model's
# name, which is a fabricated result rather than a stale one.
model_slug = _model_slug


def current_model_name() -> str:
    return os.environ["LM_STUDIO_MODEL_NAME"]


def generation_cache_dir(model_name: str, condition_id: str) -> Path:
    return GEN_DIR / model_slug(model_name) / condition_id


def generation_cache_path(model_name: str, condition_id: str, question_id: str) -> Path:
    return generation_cache_dir(model_name, condition_id) / f"{question_id}.json"


def cached_generation(model_name: str, condition_id: str, question_id: str) -> dict | None:
    """A usable cache entry, or None (which the caller treats as a miss).

    A record whose own `model` field disagrees with the model being run is a
    MISS, not a hit, even though it sits in that model's directory -- the two
    can only disagree if a file was moved or hand-edited, and answering with
    another model's text under this model's label is exactly what the model
    dimension exists to prevent.
    """
    path = generation_cache_path(model_name, condition_id, question_id)
    if not path.exists():
        return None
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("model") != model_name:
        print(
            f"    cache MISS (model mismatch) {condition_id}/{question_id}: "
            f"file says {record.get('model')!r}, running {model_name!r}"
        )
        return None
    return record


def load_questions() -> dict:
    lines = [json.loads(l) for l in BENCHMARK_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    return {q["id"]: q for q in lines}


def load_stage1(condition_id: str) -> tuple[dict, dict]:
    """run_meta, {question_id: question_result} for one Stage 1 condition file."""
    lines = [json.loads(l) for l in (STAGE1_DIR / f"{condition_id}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    meta = next(l for l in lines if l["_type"] == "run_meta")
    recs = {l["question_id"]: l for l in lines if l["_type"] == "question_result"}
    return meta, recs


# ---------------------------------------------------------------------------
# Case A retrieval, generalised to every condition (not written to Stage 1)
# ---------------------------------------------------------------------------


def compute_case_a_retrieval(condition_id: str, strategy: str, chunks: list[dict], faiss_index, bm25_index, questions: dict) -> dict:
    cache_path = CASE_A_DIR / f"{condition_id}.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if set(cached) == set(UNANSWERABLE_QIDS):
            return cached

    out = {}
    for qid in UNANSWERABLE_QIDS:
        q = questions[qid]
        retrieved = retrieve_fn(q["question"], strategy, faiss_index, bm25_index, chunks, k=5)
        out[qid] = {"top5_chunks": [{"chunk_id": c["chunk_id"], "text": c["text"]} for c in retrieved]}

    CASE_A_DIR.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Item assembly
# ---------------------------------------------------------------------------


def build_items(condition_id: str, questions: dict, stage1_recs: dict, case_a: dict) -> list[dict]:
    items = []
    for qid in UNANSWERABLE_QIDS:
        q = questions[qid]
        items.append({
            "condition_id": condition_id, "question_id": qid, "question": q["question"],
            "category": q["category"], "coverage_at_5": None,
            "top5_chunks": case_a[qid]["top5_chunks"],
        })
    for qid, r in stage1_recs.items():
        q = questions[qid]
        items.append({
            "condition_id": condition_id, "question_id": qid, "question": q["question"],
            "category": q["category"], "coverage_at_5": r["retrieval_metrics"]["anchor_coverage_at_5"],
            "top5_chunks": [{"chunk_id": c["chunk_id"], "text": c["text"]} for c in r["ranking"][:5]],
        })
    return items


# ---------------------------------------------------------------------------
# Generation (async, bounded concurrency, per-item cache write, no gather-wide loss)
# ---------------------------------------------------------------------------


async def _call_local_seeded(query: str, chunks: list[dict], semaphore: asyncio.Semaphore) -> dict:
    """Mirrors generate._generate_local_async but adds `seed` for best-effort
    determinism -- not in generate.py itself so that module stays untouched
    and its existing tests/behaviour don't need re-verifying."""
    model_name = os.environ["LM_STUDIO_MODEL_NAME"]
    context = format_context(chunks)
    user_message = f"Context:\n\n{context}\n\nQuestion: {query}"

    async with semaphore:
        response = await generate_mod.get_local_async_client().chat.completions.create(
            model=model_name,
            temperature=TEMPERATURE,
            seed=SEED,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            extra_body={"reasoning_effort": "none"},
        )

    if not response.choices or not response.choices[0].message.content:
        raise RuntimeError(f"LM Studio returned an unexpected response shape: {response!r}")
    answer = response.choices[0].message.content.strip()
    return {"answer": answer, "model": model_name}


async def _run_item_async(item: dict, semaphore: asyncio.Semaphore) -> None:
    model_name = current_model_name()
    cache_path = generation_cache_path(model_name, item["condition_id"], item["question_id"])
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cached_generation(model_name, item["condition_id"], item["question_id"]) is not None:
        return

    t0 = time.monotonic()
    try:
        result = await _call_local_seeded(item["question"], item["top5_chunks"], semaphore)
    except Exception as e:
        print(f"    ERROR {item['condition_id']}/{item['question_id']}: {e!r}")
        return  # not cached -- a re-run retries it

    record = {
        "condition_id": item["condition_id"],
        "question_id": item["question_id"],
        "category": item["category"],
        "model": result["model"],
        "temperature": TEMPERATURE,
        "seed": SEED,
        "prompt_hash": PROMPT_HASH,
        "retrieved_chunk_ids": [c["chunk_id"] for c in item["top5_chunks"]],
        "raw_response": result["answer"],
        "latency_seconds": round(time.monotonic() - t0, 2),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    cache_path.write_text(json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"    {item['question_id']:16s} done ({record['latency_seconds']}s)")


async def run_condition_generation(condition_id: str, items: list[dict]) -> None:
    # generate_mod caches its AsyncOpenAI client at module scope, but each
    # condition here runs under its own asyncio.run() (its own event loop).
    # An httpx/aiohttp connection pool created under a previous, now-closed
    # loop is invalid in the new one -- the symptom is exactly what we saw:
    # the FIRST request of every condition after the first failing with
    # APIConnectionError while the rest of that same batch succeeds. Forcing
    # a fresh client per condition (own connection pool, own event loop)
    # fixes it at the source instead of papering over it with a retry.
    generate_mod._local_async_client = None

    semaphore = asyncio.Semaphore(LOCAL_MAX_CONCURRENCY)
    model_name = current_model_name()
    pending = [
        item
        for item in items
        if cached_generation(model_name, condition_id, item["question_id"]) is None
    ]
    if not pending:
        print(f"  {condition_id}: all {len(items)} generations already cached")
        return
    print(f"  {condition_id}: generating {len(pending)}/{len(items)} (rest cached)")
    await asyncio.gather(*(_run_item_async(item, semaphore) for item in pending))


# ---------------------------------------------------------------------------
# Scoring: case/outcome classification + descriptive BERTScore/cosine on Case C
# ---------------------------------------------------------------------------


def score_all(condition_ids: list[str], questions: dict) -> tuple[list[dict], dict]:
    """Score every condition that has cached generations. Returns (rows, coverage).

    `coverage` records which conditions were scored and which were skipped and
    why. Skipping used to be a bare `continue`: with 12 conditions in the grid
    and generation existing for only the 6 text_only ones, that silently
    reported on half the grid with nothing in the output saying so. A partial
    result that does not announce itself is the failure mode worth engineering
    against here, so the skip is now reported by the caller, in the console
    summary AND in a sidecar file next to the tables.
    """
    scored_rows = []
    scored, skipped = [], []
    model_name = current_model_name()
    for condition_id in condition_ids:
        stage1_meta, stage1_recs = load_stage1(condition_id)
        case_a = json.loads((CASE_A_DIR / f"{condition_id}.json").read_text(encoding="utf-8")) if (CASE_A_DIR / f"{condition_id}.json").exists() else {}
        items = build_items(condition_id, questions, stage1_recs, case_a) if case_a else []

        gen_dir = generation_cache_dir(model_name, condition_id)
        if not gen_dir.exists():
            reasons = []
            if not (CASE_A_DIR / f"{condition_id}.json").exists():
                reasons.append("no case_a_retrieval cache")
            reasons.append(f"no generation directory for model {model_name!r}")
            skipped.append({"condition_id": condition_id, "reason": "; ".join(reasons)})
            continue
        scored.append(condition_id)

        for gen_file in sorted(gen_dir.glob("*.json")):
            record = json.loads(gen_file.read_text(encoding="utf-8"))
            qid = record["question_id"]
            q = questions[qid]

            if qid in UNANSWERABLE_QIDS:
                coverage_at_5 = None
                retrieved_chunks = case_a.get(qid, {}).get("top5_chunks", [])
            else:
                coverage_at_5 = stage1_recs[qid]["retrieval_metrics"]["anchor_coverage_at_5"]
                retrieved_chunks = [{"chunk_id": c["chunk_id"], "text": c["text"]} for c in stage1_recs[qid]["ranking"][:5]]

            classification = evaluate.classify_case_outcome(q, coverage_at_5, record["raw_response"], retrieved_chunks)

            bertscore = None
            if evaluate.is_bertscore_scored(q, classification["case"], classification["outcome"]):
                bertscore = evaluate.answer_similarity(record["raw_response"], q["reference_answer"])

            scored_rows.append({
                "condition_id": condition_id,
                "chunk_size": stage1_meta["chunk_size"],
                "retrieval_strategy": stage1_meta["retrieval_strategy"],
                # Stage 1 files persisted before indexing_representation existed
                # carry no such key; they are the text_only half of the grid by
                # construction, so they are read with that default rather than
                # re-run (README.md invariant 5).
                "indexing_representation": stage1_meta.get("indexing_representation", "text_only"),
                "question_id": qid,
                "category": q["category"],
                "chunk_size_sensitive": q.get("chunk_size_sensitive"),
                "coverage_at_5": coverage_at_5,
                "case": classification["case"],
                "outcome": classification["outcome"],
                "grounding_basis": classification["grounding_basis"],
                "n_unsupported_claims": len(classification["unsupported_claims"]),
                "bertscore_cosine": bertscore,
                "model": record["model"],
                "abstained_exact_match": record["raw_response"] == ABSTENTION,
                "abstained_soft_match": evaluate.contains_abstention_sentence(record["raw_response"]),
            })
    coverage = {
        "model": model_name,
        "requested": list(condition_ids),
        "scored": scored,
        "skipped": skipped,
    }
    return scored_rows, coverage


def report_coverage(coverage: dict, n_rows: int) -> None:
    """Make partial coverage impossible to miss when reading the output."""
    n_req = len(coverage["requested"])
    n_scored = len(coverage["scored"])
    print("\n" + "=" * 72)
    print(f"COVERAGE: scored {n_scored} of {n_req} requested condition(s) "
          f"-- {n_rows} rows, model {coverage['model']!r}")
    print("=" * 72)
    for condition_id in coverage["scored"]:
        print(f"  SCORED   {condition_id}")
    for entry in coverage["skipped"]:
        print(f"  SKIPPED  {entry['condition_id']}  ({entry['reason']})")
    if coverage["skipped"]:
        print(f"\n  *** {len(coverage['skipped'])} of {n_req} conditions are NOT represented in "
              f"the tables written by this run. ***")
        print("  *** Any figure derived from them describes only the "
              f"{n_scored} condition(s) listed as SCORED. ***")


def write_coverage_file(coverage: dict, n_rows: int, model_name: str,
                       subset_label: str | None = None) -> Path:
    """Persist the same coverage record beside the tables.

    A sidecar rather than a column: `generation_outcomes.csv` has already been
    published from, and adding a column would change the schema of a table that
    is cited elsewhere. The coverage belongs with the tables, not inside them.
    """
    out_dir = output_dir(subset_label, model_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "generation_coverage.json"
    assert_no_model_mismatch(out_path, model_name)
    out_path.write_text(
        json.dumps({**coverage, "n_rows": n_rows,
                    "subset_label": subset_label,
                    "n_requested": len(coverage["requested"]),
                    "n_scored": len(coverage["scored"]),
                    "n_skipped": len(coverage["skipped"])}, indent=1),
        encoding="utf-8",
    )
    return out_path


# The published schema of results/tables/{model_slug}/generation_outcomes.csv, pinned.
#
# This used to be `list(rows[0].keys())`, i.e. whatever the scoring row dict
# happened to contain. That is how a field added to `score_all` for an unrelated
# reason (`indexing_representation`) silently changed the schema of an already-
# published table the first time it was regenerated -- 270 identical values, one
# extra column, and no diff until someone checked. Pinning the columns means a
# new field is available to the code without rewriting a published artifact, and
# changing this table's schema now has to be deliberate.
#
# `indexing_representation` is deliberately NOT here: it lives in the long-form
# analysis CSVs (analysis/rebuild_long_tables.py), which are the files meant to
# carry the third independent variable.
GENERATION_OUTCOMES_COLUMNS = [
    "condition_id", "chunk_size", "retrieval_strategy", "question_id", "category",
    "chunk_size_sensitive", "coverage_at_5", "case", "outcome", "grounding_basis",
    "n_unsupported_claims", "bertscore_cosine", "model",
    "abstained_exact_match", "abstained_soft_match",
]


def model_tables_dir(model_name: str) -> Path:
    """Published tables for ONE generator: results/tables/{model_slug}/.

    Mirrors the generation cache layout. Without this the tables carry no model
    dimension in their path, so a full-grid run under a different generator
    overwrites the previous generator's published tables in place -- and
    case_outcome_breakdown.csv carried no model identifier in its CONTENT
    either, so the overwrite would leave nothing to say which model produced it.
    """
    return TABLES_DIR / model_slug(model_name)


def output_dir(subset_label: str | None, model_name: str) -> Path:
    """Where this run's tables go.

    Two independent scopings, because there are two ways to clobber a published
    table: writing a different MODEL over it, and writing a partial CONDITION
    SET over it. Model always scopes the directory; a subset run nests one level
    deeper again.
    """
    base = model_tables_dir(model_name)
    return base if subset_label is None else base / "subset" / subset_label


def assert_no_model_mismatch(path: Path, model_name: str, field: str = "model") -> None:
    """Refuse to overwrite a table that belongs to a different generator.

    Belt-and-braces behind the path scoping: the paths make a collision
    impossible under normal use, and this catches the abnormal cases -- a
    hand-moved file, a hand-edited slug, a script pointed at the wrong
    directory. Refuses rather than warns: a silently mixed-model table looks
    correct, which is precisely the failure worth being loud about.
    """
    if not path.exists():
        return
    try:
        if path.suffix == ".json":
            found = {json.loads(path.read_text(encoding="utf-8")).get(field)}
        else:
            with path.open(newline="", encoding="utf-8") as f:
                found = {r.get(field) for r in csv.DictReader(f)}
        found.discard(None)
    except Exception:  # noqa: BLE001 -- an unreadable table is not a mismatch
        return
    other = found - {model_name}
    if other:
        raise SystemExit(
            f"REFUSING TO OVERWRITE {path}: it contains model(s) {sorted(other)}, "
            f"but this run is {model_name!r}. Writing here would replace one "
            "generator's published results with another's. Move or remove the "
            "existing file deliberately if that is really what you want."
        )


def write_scored_table(rows: list[dict], model_name: str, subset_label: str | None = None) -> Path:
    out_dir = output_dir(subset_label, model_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "generation_outcomes.csv"
    assert_no_model_mismatch(out_path, model_name)
    fieldnames = GENERATION_OUTCOMES_COLUMNS
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def write_breakdown_table(rows: list[dict], model_name: str, subset_label: str | None = None) -> Path:
    """condition_id x case x outcome counts -- the four-way breakdown, per
    condition, not pooled.

    Carries a `model` column. It previously carried no model identifier at all,
    so a copy of this file was unattributable once separated from its directory.
    """
    out_dir = output_dir(subset_label, model_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "case_outcome_breakdown.csv"
    assert_no_model_mismatch(out_path, model_name)

    counts: dict[tuple, int] = {}
    condition_ids = sorted({r["condition_id"] for r in rows})
    for r in rows:
        key = (r["condition_id"], r["case"], r["outcome"])
        counts[key] = counts.get(key, 0) + 1

    outcomes = [evaluate.OUTCOME_ABSTAINED, evaluate.OUTCOME_GROUNDED_CORRECT, evaluate.OUTCOME_GROUNDED_OFFTARGET, evaluate.OUTCOME_UNGROUNDED]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "condition_id", "case", "n_items"] + outcomes)
        for condition_id in condition_ids:
            for case in (evaluate.CASE_A, evaluate.CASE_B, evaluate.CASE_C):
                row_counts = [counts.get((condition_id, case, o), 0) for o in outcomes]
                n_items = sum(row_counts)
                if n_items == 0:
                    continue
                writer.writerow([model_name, condition_id, case, n_items] + row_counts)
    return out_path


def print_breakdown(rows: list[dict]) -> None:
    condition_ids = sorted({r["condition_id"] for r in rows})
    outcomes = [evaluate.OUTCOME_ABSTAINED, evaluate.OUTCOME_GROUNDED_CORRECT, evaluate.OUTCOME_GROUNDED_OFFTARGET, evaluate.OUTCOME_UNGROUNDED]
    for condition_id in condition_ids:
        print(f"\n{condition_id}")
        by_case: dict[str, dict[str, int]] = {}
        for r in rows:
            if r["condition_id"] != condition_id:
                continue
            by_case.setdefault(r["case"], {})
            by_case[r["case"]][r["outcome"]] = by_case[r["case"]].get(r["outcome"], 0) + 1
        header = f"  {'case':6s}" + "".join(f"{o:>28s}" for o in outcomes) + f"{'n':>6s}"
        print(header)
        for case in (evaluate.CASE_A, evaluate.CASE_B, evaluate.CASE_C):
            counts = by_case.get(case, {})
            row = [counts.get(o, 0) for o in outcomes]
            print(f"  {case:6s}" + "".join(f"{c:>28d}" for c in row) + f"{sum(row):>6d}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--condition",
        help="condition_id to run (e.g. chunk200_hybrid); omit to run every configured condition",
    )
    parser.add_argument("--score-only", action="store_true", help="rescore cached generations, no generation calls")
    args = parser.parse_args()

    questions = load_questions()
    full_grid_paths = discover_condition_configs()
    full_grid_ids = {load_config(p)["condition_id"] for p in full_grid_paths}

    all_config_paths = full_grid_paths
    if args.condition:
        all_config_paths = [p for p in full_grid_paths if p.stem == args.condition]
        if not all_config_paths:
            raise SystemExit(f"no condition config named {args.condition!r}")
    configs = [load_config(p) for p in all_config_paths]
    condition_ids = [c["condition_id"] for c in configs]

    # A run that covers fewer than the full grid writes to its own directory.
    # The published tables in results/tables/ describe all 12 conditions; a
    # single-condition invocation used to overwrite them with that one
    # condition's rows, silently replacing a 540-row table with 45.
    model_name = current_model_name()
    subset_label = None if set(condition_ids) == full_grid_ids else "_".join(sorted(condition_ids))
    print(f"tables for this run: {output_dir(subset_label, model_name).relative_to(REPO_ROOT)}/ "
          f"(model {model_name!r})")
    if subset_label is not None:
        print(f"SUBSET RUN: {len(condition_ids)} of {len(full_grid_ids)} conditions "
              f"({', '.join(sorted(condition_ids))}).")
        print(f"  The full-grid tables in "
              f"{model_tables_dir(model_name).relative_to(REPO_ROOT)}/ are NOT written by this run.")

    if not args.score_only:
        # Grouped by (chunk_size, indexing_representation), not chunk_size
        # alone: Case A retrieval has to run against the same index its own
        # condition uses, and the indexed string depends on the representation.
        configs_by_arm: dict[tuple[int, str], list[dict]] = {}
        for config in configs:
            configs_by_arm.setdefault((config["chunk_size"], config["indexing_representation"]), []).append(config)

        chunks_by_size: dict[int, list[dict]] = {}
        for (chunk_size, representation), arm_configs in sorted(configs_by_arm.items()):
            if chunk_size not in chunks_by_size:
                chunks_by_size[chunk_size] = build_corpus_chunks(chunk_size)
            chunks = chunks_by_size[chunk_size]
            print(f"\nchunk_size={chunk_size}, indexing_representation={representation}: building "
                  f"indexes (for the {len(arm_configs)} Case A retrieval(s) needed in this arm)...")
            faiss_index, bm25_index, _ = build_indexes(chunks, representation)

            for config in arm_configs:
                condition_id = config["condition_id"]
                strategy = config["retrieval_strategy"]
                print(f"\n=== {condition_id} ===")

                case_a = compute_case_a_retrieval(condition_id, strategy, chunks, faiss_index, bm25_index, questions)
                _, stage1_recs = load_stage1(condition_id)
                items = build_items(condition_id, questions, stage1_recs, case_a)

                asyncio.run(run_condition_generation(condition_id, items))

    print("\n" + "=" * 60)
    print("scoring...")
    rows, coverage = score_all(condition_ids, questions)
    if not rows:
        print("no cached generations found to score")
        report_coverage(coverage, 0)
        return 1

    table_path = write_scored_table(rows, model_name, subset_label)
    breakdown_path = write_breakdown_table(rows, model_name, subset_label)
    coverage_path = write_coverage_file(coverage, len(rows), model_name, subset_label)
    print(f"wrote {table_path.relative_to(REPO_ROOT)} ({len(rows)} rows)")
    print(f"wrote {breakdown_path.relative_to(REPO_ROOT)}")
    print(f"wrote {coverage_path.relative_to(REPO_ROOT)}")
    print_breakdown(rows)
    report_coverage(coverage, len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

