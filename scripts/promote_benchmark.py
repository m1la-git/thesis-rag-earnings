"""Promote finalised reference candidates into benchmark/questions.jsonl.

Reads analysis/benchmark_authoring/reference_candidates.json (45 candidates, verified against the
frozen corpus by scripts/reference_candidates.py across twelve build-time rules)
and writes benchmark/questions.jsonl: one JSON object per line, matching the
benchmark schema.

This is a promotion, not a re-derivation. Every field is carried over from the
reference set as-is; nothing here re-slices an anchor or re-checks a hit rule --
that verification already happened in reference_candidates.py. What this script
adds is: renumbering ref_* IDs to benchmark IDs, converting gold_anchors from a
flat string list to the {transcript_id, anchor} object form (derivable
directly from provenance, so lossless), and a "source"/"promoted_at" stamp
recording where each record came from.

Usage:
    python scripts/promote_benchmark.py            write benchmark/questions.jsonl
    python scripts/promote_benchmark.py --verify    re-verify an existing file
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

REFERENCE_PATH = REPO_ROOT / "analysis" / "benchmark_authoring" / "reference_candidates.json"
BENCHMARK_PATH = REPO_ROOT / "benchmark" / "questions.jsonl"
ID_MAPPING_PATH = REPO_ROOT / "analysis" / "benchmark_authoring" / "id_mapping.json"

CATEGORY_PREFIX = {
    "factual": "fact",
    "thematic": "them",
    "comparative": "comp",
    "unanswerable": "unans",
}
CATEGORY_ORDER = ("factual", "thematic", "comparative", "unanswerable")


def renumber(candidates: list[dict]) -> tuple[list[dict], dict[str, str]]:
    """Assign sequential benchmark IDs within each category, in file order."""
    counters = {cat: 0 for cat in CATEGORY_PREFIX}
    mapping: dict[str, str] = {}
    renumbered = []
    for candidate in candidates:
        cat = candidate["category"]
        counters[cat] += 1
        new_id = f"{CATEGORY_PREFIX[cat]}_{counters[cat]:02d}"
        mapping[candidate["id"]] = new_id
        renumbered.append({**candidate, "_new_id": new_id})
    return renumbered, mapping


def to_gold_anchor_objects(candidate: dict) -> list[dict]:
    """The {transcript_id, anchor} form, derived from provenance.

    reference_candidates.json stores gold_anchors as a flat string list with the
    transcript association living in `provenance`; the schema pairs each
    anchor with its transcript directly, which is what a comparative question
    (multiple transcript_ids, one anchor per company) actually needs to be
    unambiguous. Order matches provenance order, which matches gold_anchors order
    by construction in reference_candidates.py.
    """
    return [
        {"transcript_id": p["transcript_id"], "anchor": p["anchor"]}
        for p in candidate["provenance"]
    ]


def build_record(candidate: dict, promoted_at: str) -> dict:
    """One benchmark/questions.jsonl line, in schema field order plus extras."""
    record = {
        "id": candidate["_new_id"],
        "category": candidate["category"],
        "question": candidate["question"],
        "transcript_ids": candidate["transcript_ids"],
        "gold_anchors": to_gold_anchor_objects(candidate),
        "reference_answer": candidate["reference_answer"] if candidate["category"] != "unanswerable" else None,
    }
    if candidate["category"] == "unanswerable":
        record["absence_type"] = candidate["absence_type"]
        record["absence_evidence"] = candidate["absence_evidence"]
        record["expected_retrieval"] = candidate["expected_retrieval"]
    record["provenance"] = candidate["provenance"]
    if "difficulty" in candidate:
        record["difficulty"] = candidate["difficulty"]
    record["notes"] = candidate["notes"]
    record["chunk_size_sensitive"] = candidate["chunk_size_sensitive"]
    record["source"] = "reference_candidates"
    record["promoted_at"] = promoted_at
    return record


def write_benchmark() -> None:
    data = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    candidates = data["candidates"]

    renumbered, mapping = renumber(candidates)
    promoted_at = datetime.date.today().isoformat()
    records = [build_record(c, promoted_at) for c in renumbered]

    BENCHMARK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with BENCHMARK_PATH.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    ID_MAPPING_PATH.write_text(
        json.dumps({"generated": promoted_at, "mapping": mapping}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(records)} records to {BENCHMARK_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote ID mapping to {ID_MAPPING_PATH.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# Verification -- re-checked against the frozen parquet, not against the
# reference JSON, so this cannot merely confirm the copy matched its source.
# ---------------------------------------------------------------------------


def load_records() -> list[dict]:
    records = []
    with BENCHMARK_PATH.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"line {line_number}: invalid JSON: {exc}")
    return records


_HYPHEN_GAP = re.compile(r"\w-\s+\w|\w\s+-\w")


def verify() -> None:
    from build_corpus_index import load_corpus, locate_chunks, build_chunk_locator
    from chunking import chunk_transcript
    from preprocess import preprocess_transcript, SECTION_PREPARED, SECTION_QA
    import evaluate

    records = load_records()
    from collections import Counter

    # Expected shape is DERIVED from the reference set, not hardcoded. The point
    # of this check is that the benchmark matches its source; a frozen constant
    # would go stale the moment the reference set legitimately changes, and would
    # then report a real match as a failure.
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))["candidates"]
    expected_cats = dict(Counter(c["category"] for c in reference))
    expected_dist = dict(Counter(len(c["provenance"]) for c in reference))
    expected_anchor_total = sum(len(c["provenance"]) for c in reference)
    expected_n = len(reference)

    # 1. line count and category counts
    print(f"1. line count: {len(records)} (expected {expected_n} from reference set) "
          f"-- {'OK' if len(records) == expected_n else 'FAIL'}")
    cat_counts = Counter(r["category"] for r in records)
    print(f"   category counts: {dict(cat_counts)} (expected {expected_cats}) "
          f"-- {'OK' if dict(cat_counts) == expected_cats else 'FAIL'}")

    # 6. valid JSONL (already proven by load_records not raising, but state it)
    print("6. JSONL validity: all lines parsed independently -- OK")

    # 5. unanswerable shape
    unans = [r for r in records if r["category"] == "unanswerable"]
    bad_shape = [r["id"] for r in unans if r["gold_anchors"] or r["transcript_ids"]]
    print(f"5. unanswerable empty gold_anchors/transcript_ids: "
          f"{'OK' if not bad_shape else 'FAIL -- ' + str(bad_shape)}")

    # 7. whitespace
    ws = []
    for r in records:
        for field in ("question", "reference_answer"):
            text = r.get(field) or ""
            if "  " in text or _HYPHEN_GAP.search(text):
                ws.append((r["id"], field))
    print(f"7. whitespace artefacts: {'none -- OK' if not ws else 'FAIL -- ' + str(ws)}")

    # 2, 3, 4: anchor-level checks against the frozen parquet directly
    print("Loading frozen corpus for anchor re-verification...")
    frame = load_corpus()
    rows = {row["transcript_id"]: row for _, row in frame.iterrows()}
    content = {tid: row["content"] for tid, row in rows.items()}

    locator_cache: dict[str, dict] = {}

    def locators_for(tid: str) -> dict:
        if tid not in locator_cache:
            records_ = preprocess_transcript(rows[tid])
            built = {}
            for size in (200, 500):
                chunks = chunk_transcript(records_, size)
                for section in (SECTION_PREPARED, SECTION_QA):
                    in_section = [c for c in chunks if c["section"] == section]
                    built[(size, section)] = build_chunk_locator(in_section)
            locator_cache[tid] = built
        return locator_cache[tid]

    total_anchors = 0
    verbatim_fail = []
    containment_fail = []
    for r in records:
        for p in r["provenance"]:
            total_anchors += 1
            tid = p["transcript_id"]
            anchor = p["anchor"]
            if tid not in content or anchor not in content[tid]:
                verbatim_fail.append((r["id"], tid))
                continue
            located = locate_chunks(anchor, locators_for(tid), p["section"])
            if len(located.get("chunk_ids@200", [])) != 1 or len(located.get("chunk_ids@500", [])) != 1:
                containment_fail.append((r["id"], tid))

    print(f"2. anchor verbatim against frozen parquet: {total_anchors} checked -- "
          f"{'OK' if not verbatim_fail else 'FAIL -- ' + str(verbatim_fail)}")
    mapping = json.loads(ID_MAPPING_PATH.read_text(encoding="utf-8"))["mapping"]
    by_new_id = {mapping[c["id"]]: c for c in reference}
    drift = []
    for r in records:
        ref = by_new_id.get(r["id"])
        if ref is None:
            drift.append((r["id"], "no reference candidate"))
            continue
        if [a["anchor"] for a in r["gold_anchors"]] != ref["gold_anchors"]:
            drift.append((r["id"], "gold_anchors differ from reference"))
        if r["question"] != ref["question"]:
            drift.append((r["id"], "question differs from reference"))
        ref_answer = ref["reference_answer"] if ref["category"] != "unanswerable" else None
        if r["reference_answer"] != ref_answer:
            drift.append((r["id"], "reference_answer differs from reference"))
    print(f"   benchmark matches reference set field-for-field: "
          f"{'OK' if not drift else 'FAIL -- ' + str(drift)}")

    print(f"3. anchor singly contained under both configs: "
          f"{'OK' if not containment_fail else 'FAIL -- ' + str(containment_fail)}")

    # 4. anchor count distribution
    dist = Counter(len(r["provenance"]) for r in records)
    anchor_total = sum(k * v for k, v in dist.items())
    print(f"4. anchor distribution: {dict(sorted(dist.items()))} "
          f"(expected {dict(sorted(expected_dist.items()))}) "
          f"-- {'OK' if dict(dist) == expected_dist else 'FAIL'}")
    print(f"   total anchors: {anchor_total} (expected {expected_anchor_total}) "
          f"-- {'OK' if anchor_total == expected_anchor_total else 'FAIL'}")

    # evaluate.py load-through
    print("\n--- evaluate.py scoring check (stub retrieval) ---")
    stub_hit = [{"text": "irrelevant filler chunk"}] * 5

    def stub_retrieval_for(record: dict) -> list[dict]:
        """A stub that hits every gold anchor at rank 1, for a numeric-scoring smoke test."""
        chunks = []
        for anchor in record["gold_anchors"]:
            chunks.append({"text": anchor["anchor"]})
        chunks += stub_hit
        return chunks[:5]

    all_numeric = True
    all_none = True
    scores = []
    for r in records:
        q = {"id": r["id"], "category": r["category"], "gold_anchors": [a["anchor"] for a in r["gold_anchors"]]}
        retrieved = stub_retrieval_for(r)
        result = evaluate.score_retrieval(q, retrieved)
        scores.append(result)
        if r["category"] == "unanswerable":
            if result["anchor_coverage_at_5"] is not None or result["mean_reciprocal_rank_at_5"] is not None:
                all_none = False
            if evaluate.is_retrieval_scored(q):
                all_none = False
        else:
            if not isinstance(result["anchor_coverage_at_5"], float) or not isinstance(result["mean_reciprocal_rank_at_5"], float):
                all_numeric = False
            if not evaluate.is_retrieval_scored(q):
                all_numeric = False

    print(f"answerable questions -> numeric coverage/MRR: {'OK' if all_numeric else 'FAIL'}")
    print(f"unanswerable questions -> None/None, is_retrieval_scored=False: {'OK' if all_none else 'FAIL'}")

    aggregate = evaluate.aggregate_retrieval(scores)
    n_answerable_ = expected_n - expected_cats.get("unanswerable", 0)
    n_unanswerable_ = expected_cats.get("unanswerable", 0)
    print(f"aggregate_retrieval: n_questions={aggregate['n_questions']} "
          f"n_scored={aggregate['anchor_coverage_at_5_n_scored']} n_excluded={aggregate['n_excluded']} "
          f"(expected n_scored={n_answerable_}, n_excluded={n_unanswerable_}) -- "
          f"{'OK' if aggregate['anchor_coverage_at_5_n_scored'] == n_answerable_ and aggregate['n_excluded'] == n_unanswerable_ else 'FAIL'}")

    n_answerable = expected_n - expected_cats.get("unanswerable", 0)
    n_unanswerable = expected_cats.get("unanswerable", 0)
    all_ok = (
        len(records) == expected_n and dict(cat_counts) == expected_cats
        and not bad_shape and not ws
        and not verbatim_fail and not containment_fail
        and dict(dist) == expected_dist and anchor_total == expected_anchor_total
        and not drift and all_numeric and all_none
        and aggregate["anchor_coverage_at_5_n_scored"] == n_answerable
        and aggregate["n_excluded"] == n_unanswerable
    )
    print(f"\n{'ALL CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED'}")
    if not all_ok:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verify", action="store_true", help="verify an existing benchmark/questions.jsonl")
    args = parser.parse_args()
    if args.verify:
        verify()
    else:
        write_benchmark()
        verify()


if __name__ == "__main__":
    main()
