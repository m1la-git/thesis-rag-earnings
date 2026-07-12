"""Load and filter earnings call transcripts from the Hugging Face dataset.

Pulls `kurry/sp500_earnings_transcripts` **at a pinned revision**, applies the
corpus selection criteria (sector, date window, ticker list) and data hygiene
rules (drop empty/broken transcripts, verify quarter completeness) fixed in
this module, and hands off a clean set of raw transcripts for preprocessing.
Does not chunk, embed, or index anything.

Downloads ~1.8GB from the Hugging Face Hub on first run; cached locally by the
`datasets` library afterward.

Why the corpus is hashed, not just listed
-----------------------------------------
Gold anchors are verbatim strings lifted from the transcript text (see
README.md, "Design"). An upstream revision that silently edits a transcript
would leave the transcript_id list identical while breaking every anchor inside
it -- an ID-only manifest cannot detect that. `data/corpus_manifest.json`
therefore records a SHA-256 of both `content` and `structured_content` per
transcript, alongside the pinned dataset revision.

Modes
-----
    python src/ingest.py                   full ingest: download, filter, write
                                           transcripts.parquet + the manifest
    python src/ingest.py --verify          re-ingest at the pinned revision and
                                           diff every hash against the committed
                                           manifest; exits non-zero on ANY drift
    python src/ingest.py --write-manifest  recompute the manifest from the local
                                           frozen parquet, no network. Upgrades an
                                           existing freeze to the hashed format
                                           without re-freezing it.
"""

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

import pandas as pd
from datasets import load_dataset

DATASET_NAME = "kurry/sp500_earnings_transcripts"

# Pinned so a re-ingest is reproducible. `load_dataset` without a revision
# tracks the branch head, which can move under the frozen corpus. Resolved via
# huggingface_hub.HfApi().dataset_info(DATASET_NAME).sha
DATASET_REVISION = "f3ded372da8d18dc6ad98955c4558e34b5fe6d45"

TICKERS = [
    "JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC",
    "COF", "BK", "STT", "AXP", "BLK", "MTB", "FITB", "HBAN",
]
YEARS = [2023, 2024]
QUARTERS = [1, 2, 3, 4]
MIN_CONTENT_CHARS = 1000

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TRANSCRIPTS_PATH = DATA_DIR / "processed" / "transcripts.parquet"
MANIFEST_PATH = DATA_DIR / "corpus_manifest.json"

HASH_ALGORITHM = "sha256"

OUTPUT_COLUMNS = [
    "symbol", "company_name", "year", "quarter", "date",
    "content", "structured_content", "transcript_id",
]


def load_transcripts() -> pd.DataFrame:
    """Load the pinned revision's train split into a DataFrame."""
    dataset = load_dataset(DATASET_NAME, split="train", revision=DATASET_REVISION)
    return dataset.to_pandas()


def filter_transcripts(df: pd.DataFrame) -> pd.DataFrame:
    """Restrict to the target tickers/years and drop empty/broken rows."""
    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["quarter"] = pd.to_numeric(
        df["quarter"].astype(str).str.extract(r"(\d+)", expand=False),
        errors="coerce",
    )
    df = df[df["symbol"].isin(TICKERS) & df["year"].isin(YEARS)]
    df = df[df["content"].notna() & (df["content"].str.len() >= MIN_CONTENT_CHARS)]
    df["year"] = df["year"].astype(int)
    df["quarter"] = df["quarter"].astype(int)
    return df


def add_transcript_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Attach a stable transcript_id: '{symbol}_{year}_Q{quarter}'."""
    df = df.copy()
    df["transcript_id"] = df["symbol"] + "_" + df["year"].astype(str) + "_Q" + df["quarter"].astype(str)
    return df


def check_completeness(df: pd.DataFrame) -> bool:
    """Verify every ticker has all 8 (year, quarter) combos present.

    Prints a report of any ticker missing quarters. Returns True only if all
    tickers are complete.
    """
    expected = {(year, quarter) for year in YEARS for quarter in QUARTERS}
    complete = True
    for ticker in TICKERS:
        present = set(
            zip(
                df.loc[df["symbol"] == ticker, "year"],
                df.loc[df["symbol"] == ticker, "quarter"],
            )
        )
        missing = sorted(expected - present)
        if missing:
            complete = False
            missing_str = ", ".join(f"{year} Q{quarter}" for year, quarter in missing)
            print(f"INCOMPLETE: {ticker} missing {missing_str}")
    return complete


# ---------------------------------------------------------------------------
# Content hashing
# ---------------------------------------------------------------------------


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_structured_content(structured_content) -> str:
    """Deterministic serialisation of a transcript's speaker turns.

    `structured_content` arrives as a numpy array of dicts, whose repr is not
    stable across library versions. Rebuilding it as JSON with fixed key order
    and no ASCII escaping makes the hash depend on the text alone -- which is
    what the gold anchors actually depend on.
    """
    turns = [{"speaker": turn["speaker"], "text": turn["text"]} for turn in structured_content]
    return json.dumps(turns, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def hash_transcripts(df: pd.DataFrame) -> list[dict]:
    """Per-transcript hash records, sorted by transcript_id."""
    records = [
        {
            "transcript_id": row["transcript_id"],
            "content_sha256": _sha256(row["content"]),
            "structured_content_sha256": _sha256(canonical_structured_content(row["structured_content"])),
        }
        for _, row in df.iterrows()
    ]
    return sorted(records, key=lambda r: r["transcript_id"])


def build_manifest(df: pd.DataFrame) -> dict:
    """The frozen-corpus record: what was selected, and exactly what text it held."""
    return {
        "dataset": DATASET_NAME,
        "revision": DATASET_REVISION,
        "hash_algorithm": HASH_ALGORITHM,
        "generated": date.today().isoformat(),
        "selection": {
            "tickers": sorted(TICKERS),
            "years": YEARS,
            "quarters": QUARTERS,
            "min_content_chars": MIN_CONTENT_CHARS,
        },
        "n_transcripts": len(df),
        "transcripts": hash_transcripts(df),
    }


def load_manifest() -> dict:
    """Read the committed manifest, rejecting the pre-hash format outright."""
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"missing {MANIFEST_PATH} -- run `python src/ingest.py` first")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if isinstance(manifest, list):
        raise SystemExit(
            f"{MANIFEST_PATH} is in the old ID-only format and carries no content hashes, "
            "so drift cannot be detected. Regenerate it with `python src/ingest.py --write-manifest`."
        )
    return manifest


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def save_outputs(df: pd.DataFrame) -> None:
    """Write the filtered records and the frozen manifest."""
    TRANSCRIPTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    df[OUTPUT_COLUMNS].to_parquet(TRANSCRIPTS_PATH, index=False)
    write_manifest(build_manifest(df))


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def diff_against_manifest(df: pd.DataFrame, manifest: dict, source: str) -> list[str]:
    """Compare a freshly-hashed DataFrame against the committed manifest.

    Returns a list of human-readable drift descriptions; empty means identical.
    """
    expected = {r["transcript_id"]: r for r in manifest["transcripts"]}
    actual = {r["transcript_id"]: r for r in hash_transcripts(df)}

    problems = []
    for missing in sorted(set(expected) - set(actual)):
        problems.append(f"[{source}] MISSING: {missing} is in the manifest but absent now")
    for extra in sorted(set(actual) - set(expected)):
        problems.append(f"[{source}] UNEXPECTED: {extra} appears now but is not in the manifest")
    for tid in sorted(set(expected) & set(actual)):
        for field in ("content_sha256", "structured_content_sha256"):
            if expected[tid][field] != actual[tid][field]:
                problems.append(
                    f"[{source}] TEXT CHANGED: {tid} {field}\n"
                    f"           manifest: {expected[tid][field]}\n"
                    f"           now:      {actual[tid][field]}"
                )
    return problems


def verify(check_remote: bool = True) -> None:
    """Re-derive the corpus and hard-fail on any drift from the committed manifest.

    Checks the local parquet (what the pipeline actually reads) and, unless
    disabled, re-ingests from the pinned Hugging Face revision. Any drift is an
    error, never a warning: a changed transcript silently invalidates every gold
    anchor inside it while leaving the ID list looking correct.
    """
    manifest = load_manifest()
    print(f"Manifest: {manifest['n_transcripts']} transcripts, "
          f"revision {manifest['revision'][:12]}, generated {manifest['generated']}")

    problems: list[str] = []

    if TRANSCRIPTS_PATH.exists():
        print(f"Verifying local {TRANSCRIPTS_PATH.name}...")
        problems += diff_against_manifest(pd.read_parquet(TRANSCRIPTS_PATH), manifest, "local parquet")
    else:
        problems.append(f"[local parquet] MISSING: {TRANSCRIPTS_PATH} does not exist")

    if check_remote:
        if manifest["revision"] != DATASET_REVISION:
            problems.append(
                f"[pin] REVISION CHANGED: manifest froze {manifest['revision']}, "
                f"ingest.py now pins {DATASET_REVISION}"
            )
        print(f"Re-ingesting {DATASET_NAME} at pinned revision {DATASET_REVISION[:12]}...")
        remote = add_transcript_ids(filter_transcripts(load_transcripts()))
        problems += diff_against_manifest(remote, manifest, "hugging face")

    if problems:
        print("\n" + "=" * 78)
        print("CORPUS DRIFT DETECTED -- THE FROZEN CORPUS NO LONGER MATCHES THE MANIFEST")
        print("=" * 78)
        for problem in problems:
            print(f"  {problem}")
        print("=" * 78)
        raise SystemExit(
            f"\n{len(problems)} problem(s). Every gold anchor is a verbatim substring of this "
            "text, so changed text silently invalidates annotations that still look valid.\n"
            "Do NOT regenerate the manifest to make this pass -- investigate the change first."
        )

    print(f"\nOK: all {manifest['n_transcripts']} transcripts match the manifest byte-for-byte.")


def print_summary(df: pd.DataFrame) -> None:
    print(f"\nTotal transcripts: {len(df)}")
    for ticker, count in df["symbol"].value_counts().sort_index().items():
        print(f"  {ticker}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--verify",
        action="store_true",
        help="re-ingest at the pinned revision and hard-fail on any drift from the manifest",
    )
    group.add_argument(
        "--write-manifest",
        action="store_true",
        help="recompute the manifest from the local frozen parquet (no network, no re-freeze)",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="with --verify, check the local parquet only and skip the Hugging Face re-ingest",
    )
    args = parser.parse_args()

    if args.verify:
        verify(check_remote=not args.local_only)
        return

    if args.write_manifest:
        if not TRANSCRIPTS_PATH.exists():
            raise SystemExit(f"missing {TRANSCRIPTS_PATH} -- nothing to hash")
        df = pd.read_parquet(TRANSCRIPTS_PATH)
        write_manifest(build_manifest(df))
        print(f"Wrote {MANIFEST_PATH} with {len(df)} content hashes (from the local frozen parquet).")
        return

    print(f"Loading dataset {DATASET_NAME} at revision {DATASET_REVISION[:12]} (split=train)...")
    df = load_transcripts()
    print(f"Loaded {len(df)} raw rows.")

    df = filter_transcripts(df)
    df = add_transcript_ids(df)
    print(f"{len(df)} rows remain after ticker/year filtering and dropping empty/broken rows.")

    if not check_completeness(df):
        print("\nOne or more tickers are missing quarters. Stopping without writing the manifest.")
        return

    save_outputs(df)
    print_summary(df)
    print(f"\nWrote {TRANSCRIPTS_PATH} and {MANIFEST_PATH}.")


if __name__ == "__main__":
    main()
