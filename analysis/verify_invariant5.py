"""Verify README.md invariant 5: the six existing conditions need no re-run.

The claim is that adding `indexing_representation` changed nothing for the
`text_only` half of the grid, because under `text_only` the indexed string is
`chunk["text"]` byte for byte. A regression test asserts that property of
`build_index_text` directly; this script proves the stronger, end-to-end
version -- that the whole pipeline, re-run through the refactored code, still
produces the persisted results byte for byte.

"Verified byte-identical" is a stronger sentence for the thesis than "no-op by
construction", which is why this exists as well as the unit test.

Method
------
Re-runs the named conditions through the CURRENT code and compares against the
versions committed in git (`git show HEAD:results/retrieval/<id>.jsonl`), not
against whatever is on disk -- so a stray local edit cannot make the check pass.

Writes its output to a scratch directory and NEVER touches
`results/retrieval/`. Overwriting the persisted artifacts in place would defeat
the purpose: the committed files are the evidence being checked.

Two lines are compared differently, deliberately:

* the 40 `question_result` lines -- the actual results -- must be byte-identical.
* the `run_meta` line is compared field by field, ignoring `generated_at` (a
  wall-clock stamp) and the newly added `indexing_representation` key, whose
  absence in the committed files is exactly what invariant 5 predicts: they
  were written before the field existed and are the text_only arm by
  construction.

Usage
-----
    python analysis/verify_invariant5.py
    python analysis/verify_invariant5.py --condition chunk200_dense
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import ingest  # noqa: E402
import run_experiment as rx  # noqa: E402

# Both chunk sizes and all three retrieval strategies, so the BM25 path is
# covered as well as the dense one and the fusion path that depends on both.
DEFAULT_CONDITIONS = ("chunk200_dense", "chunk200_hybrid", "chunk500_bm25")

IGNORED_META_KEYS = {"generated_at", "indexing_representation"}


def committed_lines(condition_id: str) -> list[str]:
    rel = f"results/retrieval/{condition_id}.jsonl"
    out = subprocess.run(
        ["git", "show", f"HEAD:{rel}"], cwd=REPO_ROOT, capture_output=True, check=True
    )
    # Read as bytes and decode explicitly: git does not translate line endings
    # here, so this is the committed content exactly.
    return out.stdout.decode("utf-8").splitlines()


def serialize(run_meta: dict, records: list[dict]) -> list[str]:
    """Exactly what write_condition_results would write, as lines."""
    return [json.dumps(run_meta, ensure_ascii=False)] + [
        json.dumps(record, ensure_ascii=False) for record in records
    ]


def compare(condition_id: str, produced: list[str]) -> tuple[bool, list[str]]:
    expected = committed_lines(condition_id)
    notes: list[str] = []

    if len(produced) != len(expected):
        return False, [f"line count differs: produced {len(produced)}, committed {len(expected)}"]

    ok = True

    # run_meta: field-by-field, ignoring the wall clock and the new key.
    got_meta, want_meta = json.loads(produced[0]), json.loads(expected[0])
    added = set(got_meta) - set(want_meta)
    removed = set(want_meta) - set(got_meta)
    if removed:
        ok = False
        notes.append(f"run_meta LOST key(s): {sorted(removed)}")
    if added - IGNORED_META_KEYS:
        ok = False
        notes.append(f"run_meta gained unexpected key(s): {sorted(added - IGNORED_META_KEYS)}")
    if added & IGNORED_META_KEYS:
        notes.append(
            f"run_meta gained (expected, ignored): "
            f"{ {k: got_meta[k] for k in sorted(added & IGNORED_META_KEYS)} }"
        )
    for key in sorted(set(got_meta) & set(want_meta)):
        if key in IGNORED_META_KEYS:
            continue
        if got_meta[key] != want_meta[key]:
            ok = False
            notes.append(f"run_meta[{key!r}]: {want_meta[key]!r} -> {got_meta[key]!r}")

    # question_result lines: byte-identical, no exceptions.
    mismatches = [i for i in range(1, len(produced)) if produced[i] != expected[i]]
    if mismatches:
        ok = False
        first = mismatches[0]
        notes.append(
            f"{len(mismatches)}/{len(produced) - 1} question_result line(s) differ; "
            f"first at line {first + 1} "
            f"(question_id={json.loads(produced[first]).get('question_id')})"
        )
    else:
        notes.append(f"{len(produced) - 1}/{len(produced) - 1} question_result lines byte-identical")

    return ok, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", action="append", help="condition_id (repeatable)")
    args = parser.parse_args()
    condition_ids = args.condition or list(DEFAULT_CONDITIONS)

    questions = rx.load_questions()
    scored = rx.scored_questions(questions)
    manifest = rx.verify_corpus_matches_manifest()
    manifest_sha256 = rx.sha256_file(ingest.MANIFEST_PATH)
    benchmark_sha256 = rx.sha256_file(rx.BENCHMARK_PATH)
    print(f"corpus verified against manifest ({manifest['n_transcripts']} transcripts)")
    print(f"verifying: {condition_ids}\n")

    configs = [rx.load_config(rx.CONFIGS_DIR / f"{cid}.json") for cid in condition_ids]
    for config in configs:
        rx.validate_config_matches_code(config)
        if config["indexing_representation"] != "text_only":
            raise SystemExit(
                f"{config['condition_id']} is not a text_only condition; invariant 5 is a claim "
                "about the six existing conditions only"
            )

    by_size: dict[int, list[dict]] = {}
    for config in configs:
        by_size.setdefault(config["chunk_size"], []).append(config)

    scratch = Path(tempfile.mkdtemp(prefix="invariant5_"))
    results: dict[str, tuple[bool, list[str]]] = {}

    for chunk_size, size_configs in sorted(by_size.items()):
        print(f"chunk_size={chunk_size}: chunking + indexing (text_only)...")
        chunks = rx.build_corpus_chunks(chunk_size)
        faiss_index, bm25_index, _ = rx.build_indexes(chunks, "text_only")
        print(f"  {len(chunks)} chunks indexed")

        for config in size_configs:
            cid = config["condition_id"]
            print(f"  re-running {cid}...")
            run_meta, records = rx.run_condition(
                config, chunks, faiss_index, bm25_index, scored, manifest_sha256, benchmark_sha256
            )
            produced = serialize(run_meta, records)
            (scratch / f"{cid}.jsonl").write_text("\n".join(produced) + "\n", encoding="utf-8")
            results[cid] = compare(cid, produced)

    print(f"\nscratch output: {scratch}")
    print("\n=== invariant 5: re-run vs committed ===")
    all_ok = True
    for cid in condition_ids:
        ok, notes = results[cid]
        all_ok &= ok
        print(f"\n{cid}: {'PASS' if ok else 'FAIL'}")
        for note in notes:
            print(f"    {note}")

    print("\n" + ("PASS: every re-run condition matches its committed results"
                  if all_ok else "FAIL: at least one condition diverged"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
