"""Check 3 (attribution exposure), re-run over the POST-fix label set.

What Check 3 asks
-----------------
`classify_outcome`'s grounding test verifies that a number in the answer appears
*somewhere* in the retrieved top-5, verbatim. It does NOT verify that the number
sitting next to a company name in the answer's own sentence came from that
company's transcript. Check 3 quantifies that exposure: how many items have at
least one **substantive** numeric claim supported ONLY by chunks from a
transcript that is not in the question's own `transcript_ids`.

Why it is being re-run
----------------------
The original Check 3 in `analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md` was computed on the
PRE-fix labels. Its populations -- Case C `answered_grounded_correct` n=26 and
`answered_grounded_offtarget` n=42 -- are the pre-fix figures. Post-fix they are
30 and 58, so "7 of 26 (27%)" cannot be quoted against any post-fix table, and
the four items promoted into Case C correct by the fixes were never traced at
all.

Method: unchanged
-----------------
Same rule as the original, deliberately including its own triviality
definition:

    substantive claim = a numeric claim that is NOT a bare year 2022-2026 and
                        NOT one of the bare digits 1-4

**That is the diagnostic's own rule and it is NOT `evaluate.is_trivial_claim`**,
which uses 2000-2030 and, via Fix 2, additionally requires the claim to be
echoed by the question. Keeping the original rule is what makes the pre/post
comparison a population change rather than a population change confounded with
a method change.

One thing that unavoidably differs: claim EXTRACTION now uses the corrected
Fix 1 regex, because the point is to characterise the current instrument. The
pre-fix run necessarily used the old regex. `--validate` therefore re-runs this
same code over the PRE-fix population with the PRE-fix regex and asserts it
reproduces the published 7/26 and 39/42 -- if it does, the implementation is
faithful and any difference in the post-fix numbers is a real change, not a
reimplementation artifact.

Output is written to a NEW file; the pre-fix version stays in
`stage2_diagnostics.md` as part of the audit trail.

Usage
-----
    python analysis/check3_attribution_postfix.py --validate
    python analysis/check3_attribution_postfix.py
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import evaluate  # noqa: E402
from model_paths import (  # noqa: E402
    analysis_path,
    generation_outcomes_path,
    prefix_generation_outcomes_path,
)
from run_generation import generation_cache_path  # noqa: E402

STAGE1_DIR = REPO_ROOT / "results" / "retrieval"
CASE_A_DIR = REPO_ROOT / "results" / "generation" / "case_a_retrieval"
BENCHMARK_PATH = REPO_ROOT / "benchmark" / "questions.jsonl"
# POST_TABLE is model-scoped, resolved per --model. PRE_TABLE is the frozen
# pre-fix q4 table: historical, nothing writes there, deliberately not scoped.
PRE_TABLE = prefix_generation_outcomes_path()
MODEL = "qwen3.8-27b@q4_k_xl"
# q4-only by nature (see assert_prefix_model), so these live in the q4
# directory rather than at the top of analysis/. Keyed off MODEL, which is the
# same generator PREFIX_MODEL names -- asserted below so the two cannot drift.
OUT_MD = analysis_path(MODEL, "check3_attribution_postfix.md")
OUT_CSV = analysis_path(MODEL, "check3_attribution_postfix.csv")

PRE_FIX1_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
POST_FIX1_RE = evaluate._NUMBER_RE

# The diagnostic's OWN triviality rule -- not evaluate.is_trivial_claim.
DIAGNOSTIC_TRIVIAL_YEARS = {str(y) for y in range(2022, 2027)}
DIAGNOSTIC_TRIVIAL_DIGITS = {"1", "2", "3", "4"}

# The four records promoted into Case C `answered_grounded_correct` by the
# fixes; never examined by the original Check 3.
NEWLY_PROMOTED = {
    ("chunk200_bm25", "ref_fact_05"),
    ("chunk200_bm25", "ref_fact_09"),
    ("chunk200_dense", "ref_them_15"),
    ("chunk500_hybrid", "ref_them_04"),
}

UNANSWERABLE_QIDS = {"ref_unans_01", "ref_unans_02", "ref_unans_03", "ref_unans_05", "ref_unans_06"}

# The PRE-fix table is a frozen q4 artifact: it records what the scorer produced
# BEFORE the three fixes of 2026-09-03, on the records that existed then. No
# other generator has one and none ever will, because the fixes were found and
# made once, on q4. This script is therefore a statement about the INSTRUMENT,
# not about the reported generator, and stays a q4-only artifact -- see
# README.md, "Generator runs".
PREFIX_MODEL = "qwen3.8-27b@q4_k_xl"
assert PREFIX_MODEL == MODEL, "the PRE table and this diagnostic must name one generator"


def assert_prefix_model(model: str) -> None:
    """Refuse a non-q4 model with an explanation, not a missing-file error."""
    if model != PREFIX_MODEL:
        raise SystemExit(
            "This diagnostic is a q4-only artifact and cannot run under "
            f"{model!r}.\n"
            "  It compares the PRE-fix and POST-fix label sets, and the PRE-fix\n"
            "  table is a frozen record of the scorer BEFORE the 2026-09-03 fixes.\n"
            "  No other generator has one, and none ever will.\n"
            "  It describes the scoring INSTRUMENT, not the reported generator, so\n"
            "  its absence from another generator's artifact set is correct, not a\n"
            "  gap. See README.md, \"Generator runs\"."
        )



def is_substantive(claim: str) -> bool:
    """The diagnostic's own triviality rule, applied to the NORMALIZED claim.

    Normalizing first matters only when re-running over the pre-fix regex,
    where a claim can arrive as `"2023,"` with the sentence comma attached
    (that is the Fix 1 bug). Testing the raw string against a set of bare years
    would let `"2023,"` through as "substantive", which defeats the rule's
    stated purpose -- bare years "recur too often to be distinguishing", and a
    trailing comma does not change that.

    This is the reconstruction that reproduces the published 7/26 and 39/42
    exactly; testing the un-normalized string gives 12/26 and 40/42, and the
    five extra Case C items are each flagged solely by a comma-suffixed year.
    Under the post-fix regex no claim carries a comma, so this is a no-op there.
    """
    normalized = POST_FIX1_RE.findall(claim)
    normalized = normalized[0] if normalized else claim
    return normalized not in DIAGNOSTIC_TRIVIAL_YEARS and normalized not in DIAGNOSTIC_TRIVIAL_DIGITS


def load_questions() -> dict:
    return {
        json.loads(l)["id"]: json.loads(l)
        for l in BENCHMARK_PATH.read_text(encoding="utf-8").splitlines()
        if l.strip()
    }


def load_table(path: Path, model: str | None = None) -> list[dict]:
    """Rows from one outcome table, optionally restricted to one generator.

    The model filter is not optional in spirit: once more than one generator
    has been run, an unfiltered read silently pools them into a single
    population that looks like a valid table and is not one.
    """
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if model is None:
        return rows
    kept = [r for r in rows if r.get("model") == model]
    if not kept:
        raise SystemExit(f"no rows in {path} for model {model!r}")
    return kept


_stage1_cache: dict[str, dict] = {}


def stage1_top5(condition_id: str, question_id: str) -> list[dict]:
    if condition_id not in _stage1_cache:
        recs = {}
        for line in (STAGE1_DIR / f"{condition_id}.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec.get("_type") == "question_result":
                recs[rec["question_id"]] = rec
        _stage1_cache[condition_id] = recs
    rec = _stage1_cache[condition_id][question_id]
    return [{"chunk_id": c["chunk_id"], "text": c["text"]} for c in rec["ranking"][:5]]


_case_a_cache: dict[str, dict] = {}


def case_a_top5(condition_id: str, question_id: str) -> list[dict]:
    if condition_id not in _case_a_cache:
        _case_a_cache[condition_id] = json.loads(
            (CASE_A_DIR / f"{condition_id}.json").read_text(encoding="utf-8")
        )
    return _case_a_cache[condition_id][question_id]["top5_chunks"]


def retrieved_chunks(condition_id: str, question_id: str) -> list[dict]:
    if question_id in UNANSWERABLE_QIDS:
        return case_a_top5(condition_id, question_id)
    return stage1_top5(condition_id, question_id)


def trace(row: dict, questions: dict, regex: re.Pattern) -> dict:
    """Per-claim attribution trace for one record.

    Flags the record when at least one substantive claim is supported ONLY by
    chunks whose transcript is not among the question's own `transcript_ids`.
    """
    condition_id, question_id = row["condition_id"], row["question_id"]
    question = questions[question_id]
    targets = set(question.get("transcript_ids") or [])
    chunks = retrieved_chunks(condition_id, question_id)
    answer = json.loads(
        generation_cache_path(MODEL, condition_id, question_id).read_text(encoding="utf-8")
    )["raw_response"]

    claims = [c for c in regex.findall(answer) if is_substantive(c)]

    offtarget_only = []
    for claim in dict.fromkeys(claims):  # de-duplicate, keep order
        supporting = {c["chunk_id"] for c in chunks if claim in c["text"]}
        if not supporting:
            continue  # unsupported entirely -- not this diagnostic's question
        transcripts = {evaluate.transcript_id_from_chunk_id(cid) for cid in supporting}
        if not (transcripts & targets):
            offtarget_only.append({"claim": claim, "supported_by": sorted(transcripts)})

    return {
        "model": row.get("model", MODEL),
        "condition_id": condition_id,
        "question_id": question_id,
        "case": row["case"],
        "outcome": row["outcome"],
        "n_substantive_claims": len(set(claims)),
        "n_offtarget_only_claims": len(offtarget_only),
        "flagged": bool(offtarget_only),
        "offtarget_only_claims": "; ".join(
            f"{d['claim']} -> {','.join(d['supported_by'])}" for d in offtarget_only
        ),
        "newly_promoted": (condition_id, question_id) in NEWLY_PROMOTED,
    }


TEXT_ONLY_CONDITIONS = [
    "chunk200_bm25", "chunk200_dense", "chunk200_hybrid",
    "chunk500_bm25", "chunk500_dense", "chunk500_hybrid",
]


def population(rows: list[dict], case: str | None, outcome: str) -> list[dict]:
    """The population for one (case, outcome), restricted to the text_only arm.

    The arm restriction is what keeps this a PRE-vs-POST comparison. The
    pre-fix table is a frozen artifact of the six text_only conditions -- the
    enriched arm was generated long afterwards -- so pooling both arms on the
    post-fix side compares 6 conditions against 12 and confounds the scorer
    fix with the addition of a whole experimental arm.

    That is exactly what happened once the enriched arm landed: this file
    silently went from reporting 9/30 and 55/58 to 20/109 and 109/114, purely
    by arm-pooling (30+79=109, 9+11=20, 58+56=114, 55+54=109 -- verified). The
    pre-fix side is text_only by nature and never moved, so only the post-fix
    side drifted, and `--validate` did not catch it because it asserted only
    the pre-fix figures. Both are fixed: the filter below, and the post-fix
    assertions in `main`.

    The enriched arm is reported separately, and correctly, by
    `analysis/check3_enriched.py`.
    """
    return [r for r in rows
            if r["outcome"] == outcome
            and (case is None or r["case"] == case)
            and r["condition_id"] in TEXT_ONLY_CONDITIONS]


def run(rows: list[dict], questions: dict, regex: re.Pattern) -> tuple[list[dict], list[dict]]:
    correct = [trace(r, questions, regex) for r in population(rows, "C", "answered_grounded_correct")]
    offtarget = [trace(r, questions, regex) for r in population(rows, None, "answered_grounded_offtarget")]
    return correct, offtarget


def pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.0f}%" if d else "n/a"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    global MODEL
    parser.add_argument("--validate", action="store_true",
                        help="reproduce the published pre-fix figures (7/26, 39/42) and exit")
    parser.add_argument("--model", default=MODEL,
                        help=f"generator model to analyse (default: {MODEL})")
    args = parser.parse_args()
    assert_prefix_model(args.model)
    MODEL = args.model  # trace() reads this module-level value for cache paths

    questions = load_questions()

    if args.validate:
        correct, offtarget = run(load_table(PRE_TABLE, args.model), questions, PRE_FIX1_RE)
        nc, no = sum(r["flagged"] for r in correct), sum(r["flagged"] for r in offtarget)
        print("Validation against the PUBLISHED pre-fix Check 3 "
              "(pre-fix labels, pre-fix regex):")
        print(f"  Case C correct : {nc}/{len(correct)} ({pct(nc, len(correct))})   expected 7/26 (27%)")
        print(f"  offtarget      : {no}/{len(offtarget)} ({pct(no, len(offtarget))})   expected 39/42 (93%)")
        ok = (nc, len(correct), no, len(offtarget)) == (7, 26, 39, 42)
        print("\n" + ("PASS: implementation reproduces the published figures exactly"
                      if ok else "MISMATCH: this implementation does NOT reproduce the published "
                                 "figures -- do not trust the post-fix numbers until reconciled"))
        return 0 if ok else 1

    correct, offtarget = run(load_table(generation_outcomes_path(args.model), args.model),
                             questions, POST_FIX1_RE)

    # Assert the POST-fix figures, not just the pre-fix ones. Without this the
    # population silently broadened when the enriched arm landed and --validate
    # still passed: it only ever checked the pre-fix side, which is text_only by
    # nature and therefore could not move.
    nc, no = sum(1 for r in correct if r["flagged"]), sum(1 for r in offtarget if r["flagged"])
    post_expected = [
        ("Case C answered_grounded_correct", nc, len(correct), 9, 30),
        ("answered_grounded_offtarget", no, len(offtarget), 55, 58),
    ]
    post_problems = [
        f"{label}: computed {f}/{n}, expected {ef}/{en}"
        for label, f, n, ef, en in post_expected if (f, n) != (ef, en)
    ]
    print("Post-fix figures (text_only arm, the published ones):")
    for label, f, n, ef, en in post_expected:
        print(f"  {label}: {f}/{n} ({pct(f, n)})   expected {ef}/{en}")
    if post_problems:
        print("\n  FAIL -- the published post-fix figures did not reproduce:")
        for pr in post_problems:
            print(f"    {pr}")
        print("  Refusing to write. Either the population changed (check the arm\n"
              "  filter in `population`) or the scored table did.")
        return 1
    print("  PASS -- both reproduce exactly")

    nc, no = sum(r["flagged"] for r in correct), sum(r["flagged"] for r in offtarget)
    promoted = [r for r in correct if r["newly_promoted"]]
    np_flagged = sum(r["flagged"] for r in promoted)

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(correct[0].keys()))
        writer.writeheader()
        writer.writerows(correct + offtarget)

    lines = [
        "# Check 3 (attribution exposure) — POST-fix label set",
        "",
        f"**Label set: POST-fix** (`{generation_outcomes_path(args.model).relative_to(REPO_ROOT).as_posix()}`), i.e. after",
        "the three scorer fixes of 2026-09-03. Populations: Case C",
        f"`answered_grounded_correct` **n={len(correct)}**, `answered_grounded_offtarget`",
        f"(all cases) **n={len(offtarget)}**.",
        "",
        "This **supersedes for post-fix purposes** the Check 3 table in",
        "`analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md`, which was computed on the **PRE-fix** label",
        "set (n=26 and n=42) and remains valid only as a statement about those labels.",
        "The earlier file is unmodified and stays part of the audit trail.",
        "",
        "## Method (unchanged from the original)",
        "",
        "An item is flagged when at least one **substantive** numeric claim in its answer",
        "is supported ONLY by chunks from a transcript outside the question's own",
        "`transcript_ids` — i.e. a figure the answer attaches to a company/quarter that",
        "cannot be verified as belonging there.",
        "",
        "`substantive` = not a bare year 2022–2026 and not a bare digit 1–4. **This is the",
        "diagnostic's own rule, deliberately preserved, and is NOT",
        "`evaluate.is_trivial_claim`** (2000–2030, plus Fix 2's echoed-by-question",
        "conjunct). Keeping the original rule is what makes the pre/post difference a",
        "population change rather than a population change confounded with a method change.",
        "",
        "Claim extraction uses the corrected (Fix 1) regex, since the point is to",
        "characterise the current instrument. `--validate` re-runs this same code over the",
        "pre-fix population with the pre-fix regex and reproduces the published 7/26 and",
        "39/42 exactly, so the implementation is faithful and the post-fix figures below",
        "are a real change rather than a reimplementation artifact.",
        "",
        "## Results",
        "",
        "| population | label set | n | flagged | % |",
        "|---|---|--:|--:|--:|",
        f"| Case C `answered_grounded_correct` | pre-fix (published) | 26 | 7 | 27% |",
        f"| Case C `answered_grounded_correct` | **post-fix** | **{len(correct)}** | **{nc}** | **{pct(nc, len(correct))}** |",
        f"| `answered_grounded_offtarget` (all cases) | pre-fix (published) | 42 | 39 | 93% |",
        f"| `answered_grounded_offtarget` (all cases) | **post-fix** | **{len(offtarget)}** | **{no}** | **{pct(no, len(offtarget))}** |",
        "",
        "## The four newly-promoted Case C records",
        "",
        "Promoted into `answered_grounded_correct` by the fixes, so never examined by the",
        f"original Check 3. **{np_flagged} of {len(promoted)} flagged.**",
        "",
        "| condition | question | substantive claims | off-target-only claims | flagged |",
        "|---|---|--:|---|---|",
    ]
    for r in sorted(promoted, key=lambda r: (r["condition_id"], r["question_id"])):
        lines.append(
            f"| {r['condition_id']} | {r['question_id']} | {r['n_substantive_claims']} | "
            f"{r['offtarget_only_claims'] or '—'} | {'**YES**' if r['flagged'] else 'no'} |"
        )

    lines += [
        "",
        "## Flagged Case C `answered_grounded_correct` items (post-fix)",
        "",
        "| condition | question | off-target-only claims |",
        "|---|---|---|",
    ]
    for r in sorted((r for r in correct if r["flagged"]), key=lambda r: (r["condition_id"], r["question_id"])):
        mark = " *(newly promoted)*" if r["newly_promoted"] else ""
        lines.append(f"| {r['condition_id']}{mark} | {r['question_id']} | {r['offtarget_only_claims']} |")

    lines += ["", f"Per-record detail for both populations: `{OUT_CSV.name}`.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines[lines.index("## Results"):]))
    print(f"-> {OUT_MD.relative_to(REPO_ROOT)}")
    print(f"-> {OUT_CSV.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
