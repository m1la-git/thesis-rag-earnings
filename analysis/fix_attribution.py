"""Counterfactual: which scorer fix is load-bearing for each Case C flip?

The question
------------
`analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md` verified that **Fix 2 caused none of the 15
Case B `answered_ungrounded` flips** -- all 14 numeric ones trace to Fix 1's
comma regex, the 15th to Fix 3. But the re-scoring also produced **4 Case C
flips** (`answered_ungrounded -> answered_grounded_correct`) that were never
attributed to an individual fix.

That matters because Fix 2 is the *exclusion* rule (drop a claim that is both
trivial and echoed by the question), and a flip INTO `correct` is the most
flattering direction available. The defensible claim is that the ungrounded
collapse is instrument repair, not an exclusion rule quietly improving results.
So: is Fix 2 necessary for any of these four?

Method
------
Re-scores ONLY those four records under the full 2x2 of Fix 1 x Fix 2, holding
Fix 3 off (and asserting it is inert for all four -- none of them is an
abstention, so it must be):

    neither     pre-fix baseline
    fix1_only   corrected comma regex, no exclusion rule
    fix2_only   old comma regex, exclusion rule active
    both        post-fix

Read as:
    flips under fix1_only but not fix2_only -> Fix 1 sufficient, Fix 2 not needed
    flips only under `both`                 -> the two are JOINTLY necessary
    flips under fix2_only                   -> Fix 2 sufficient (worst case)

Trust
-----
The classifier is re-implemented here so the fixes can be toggled, which risks
drifting from the real one. Two assertions close that gap, and the script fails
loudly rather than reporting a drifted number:

  * `both` must reproduce `evaluate.classify_outcome`'s LIVE output;
  * `neither` must reproduce the PRE-fix persisted label in
    `results/tables/prefix/generation_outcomes.csv`.

In the `fix2_only` counterfactual the question's own claims are extracted with
the SAME (old) regex as the answer's -- Fix 2 alone would have been built on
the then-current regex. Using the corrected regex there would smuggle in half
of Fix 1.

Read-only: reads generations, Stage 1 rankings, the benchmark and both outcome
tables. Writes nothing.

Usage
-----
    python analysis/fix_attribution.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

import evaluate  # noqa: E402
from generate import ABSTENTION  # noqa: E402
from model_paths import (  # noqa: E402
    generation_outcomes_path,
    prefix_generation_outcomes_path,
)
from run_generation import generation_cache_path  # noqa: E402

STAGE1_DIR = REPO_ROOT / "results" / "retrieval"
BENCHMARK_PATH = REPO_ROOT / "benchmark" / "questions.jsonl"
# POST_TABLE is model-scoped, resolved per --model. PRE_TABLE is the frozen
# pre-fix q4 table: historical, nothing writes there, deliberately not scoped.
PRE_TABLE = prefix_generation_outcomes_path()
MODEL = "qwen3.8-27b@q4_k_xl"

# The four Case C ungrounded -> answered_grounded_correct flips.
TARGETS = [
    ("chunk200_bm25", "ref_fact_05"),
    ("chunk200_bm25", "ref_fact_09"),
    ("chunk200_dense", "ref_them_15"),
    ("chunk500_hybrid", "ref_them_04"),
]

# Fix 1: the OLD regex treated any comma right after a digit run as a possible
# thousands separator, so "2023," in ordinary prose was captured comma-and-all.
PRE_FIX1_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
POST_FIX1_RE = evaluate._NUMBER_RE

CONFIGS = [
    ("neither", False, False),
    ("fix1_only", True, False),
    ("fix2_only", False, True),
    ("both", True, True),
]


def extract_claims(text: str, fix1: bool) -> list[str]:
    return (POST_FIX1_RE if fix1 else PRE_FIX1_RE).findall(text)


def classify(answer: str, question: dict, chunks: list[dict],
             fix1: bool, fix2: bool, fix3: bool = False) -> dict:
    """`evaluate.classify_outcome` with all three fixes independently toggleable.

    Structurally identical to the real one apart from the toggles; the
    assertions in `main` are what prove that.
    """
    abstained = (
        evaluate.contains_abstention_sentence(answer) if fix3 else answer == ABSTENTION
    )
    if abstained:
        return {"outcome": evaluate.OUTCOME_ABSTAINED, "unsupported_claims": [], "verified": []}

    claims = extract_claims(answer, fix1)
    if fix2:
        echoed = set(extract_claims(question["question"], fix1))
        claims = [c for c in claims if not (evaluate.is_trivial_claim(c) and c in echoed)]

    if claims:
        supporting: set[str] = set()
        unsupported = []
        verified = []
        for claim in claims:
            hit = False
            for chunk in chunks:
                if claim in chunk["text"]:
                    supporting.add(chunk["chunk_id"])
                    hit = True
            (verified if hit else unsupported).append(claim)
        basis = "numeric"
    else:
        supporting = evaluate._shared_ngram_chunk_ids(answer, chunks)
        unsupported, verified = [], []
        basis = "ngram_fallback"
        if not supporting:
            return {"outcome": evaluate.OUTCOME_UNGROUNDED, "unsupported_claims": [],
                    "verified": [], "grounding_basis": basis, "claims": claims}

    if unsupported:
        return {"outcome": evaluate.OUTCOME_UNGROUNDED, "unsupported_claims": unsupported,
                "verified": verified, "grounding_basis": basis, "claims": claims}

    targets = set(question.get("transcript_ids") or [])
    supporting_transcripts = {evaluate.transcript_id_from_chunk_id(c) for c in supporting}
    on_target = bool(supporting_transcripts & targets)
    return {
        "outcome": evaluate.OUTCOME_GROUNDED_CORRECT if on_target else evaluate.OUTCOME_GROUNDED_OFFTARGET,
        "unsupported_claims": [],
        "verified": verified,
        "grounding_basis": basis,
        "claims": claims,
        "supporting_transcripts": sorted(supporting_transcripts),
    }


def load_table(path: Path, model: str) -> dict:
    """One outcome table, restricted to one generator.

    Filtering is mandatory here: an unfiltered read after a second generator
    has run would key (condition_id, question_id) across two models and the
    later one would silently win the dict.
    """
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("model") == model]
    if not rows:
        raise SystemExit(f"no rows in {path} for model {model!r}")
    return {(r["condition_id"], r["question_id"]): r for r in rows}


def load_stage1_top5(condition_id: str, question_id: str) -> list[dict]:
    path = STAGE1_DIR / f"{condition_id}.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("_type") == "question_result" and rec["question_id"] == question_id:
            return [{"chunk_id": c["chunk_id"], "text": c["text"]} for c in rec["ranking"][:5]]
    raise KeyError(f"{question_id} not in {path}")


CASE_A_DIR = REPO_ROOT / "results" / "generation" / "case_a_retrieval"
UNANSWERABLE_QIDS = {"ref_unans_01", "ref_unans_02", "ref_unans_03", "ref_unans_05", "ref_unans_06"}

# The PRE-fix table is a frozen q4 artifact: it records what the scorer produced
# BEFORE the three fixes of 2026-09-03, on the records that existed then. No
# other generator has one and none ever will, because the fixes were found and
# made once, on q4. This script is therefore a statement about the INSTRUMENT,
# not about the reported generator, and stays a q4-only artifact -- see
# README.md, "Generator runs".
PREFIX_MODEL = "qwen3.8-27b@q4_k_xl"


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


DECOMPOSE_CONFIGS = [
    ("neither", False, False, False),
    ("fix1_only", True, False, False),
    ("fix2_only", False, True, False),
    ("fix3_only", False, False, True),
    ("all", True, True, True),
]


def top5_for(condition_id: str, question_id: str) -> list[dict]:
    """Retrieved top-5 for any record, answerable or not.

    Case A questions were never retrieved for by Stage 1 (correctly -- they are
    not retrieval-scored), so their chunks come from run_generation's separate
    case_a_retrieval cache.
    """
    if question_id in UNANSWERABLE_QIDS:
        cached = json.loads((CASE_A_DIR / f"{condition_id}.json").read_text(encoding="utf-8"))
        return cached[question_id]["top5_chunks"]
    return load_stage1_top5(condition_id, question_id)


def decompose(questions: dict, pre: dict, post: dict) -> int:
    """Attribute EVERY departure from `answered_ungrounded` to a single fix.

    The published decomposition (17 Fix 1 / 1 Fix 3 / 1 Fix 2) is only as good
    as its weakest link, and the 14 Case B numeric flips were previously
    attributed in prose by `analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md` rather than by this
    harness. This runs the counterfactual over all of them so the whole
    decomposition is verified by the same mechanism, not partly inherited.

    SCOPE. The comparison is pre-fix vs post-fix, so it can only cover records
    that EXIST on both sides. The pre-fix table is a frozen historical artifact
    of the six `text_only` conditions; the `metadata_enriched` conditions were
    generated long after the scorer fixes and have no pre-fix counterpart, so
    they are outside this question by construction rather than missing from it.
    The scope is narrowed explicitly and announced -- silently iterating the
    post table would raise a KeyError on the first enriched record, which is
    exactly what it did once the enriched arm landed.
    """
    pre_conditions = sorted({c for c, _ in pre})
    post_conditions = sorted({c for c, _ in post})
    excluded = sorted(set(post_conditions) - set(pre_conditions))

    print(f"SCOPE: {len(pre_conditions)} condition(s) present in BOTH the pre-fix and post-fix "
          f"tables: {pre_conditions}")
    if excluded:
        print(f"       {len(excluded)} post-fix condition(s) EXCLUDED, having no pre-fix "
              f"counterpart: {excluded}")
        print("       These were generated after the scorer fixes, so there is no pre/post "
              "comparison to make for them. This is a property of the question, not a gap.")

    comparable = {k for k in post if k in pre}
    ungrounded_pre = sorted(k for k, r in pre.items() if r["outcome"] == evaluate.OUTCOME_UNGROUNDED)
    entered = sorted(
        k for k in comparable
        if post[k]["outcome"] == evaluate.OUTCOME_UNGROUNDED
        and pre[k]["outcome"] != evaluate.OUTCOME_UNGROUNDED
    )

    print(f"\nRecords with pre-fix outcome = answered_ungrounded: {len(ungrounded_pre)}")
    print(f"Records that ENTERED answered_ungrounded: {len(entered)}")

    tally = {"fix1": [], "fix2": [], "fix3": [], "ambiguous": [], "jointly_necessary": [], "no_flip": []}
    rows = []

    for condition_id, question_id in ungrounded_pre:
        answer = json.loads(
            generation_cache_path(MODEL, condition_id, question_id).read_text(encoding="utf-8")
        )["raw_response"]
        question = questions[question_id]
        chunks = top5_for(condition_id, question_id)

        outcomes = {
            name: classify(answer, question, chunks, f1, f2, f3)["outcome"]
            for name, f1, f2, f3 in DECOMPOSE_CONFIGS
        }

        live = evaluate.classify_outcome(answer, question, chunks)["outcome"]
        if outcomes["all"] != live:
            raise AssertionError(
                f"{condition_id}/{question_id}: 'all' gives {outcomes['all']!r}, live scorer gives "
                f"{live!r} -- harness drift"
            )
        if outcomes["all"] != post[(condition_id, question_id)]["outcome"]:
            raise AssertionError(f"{condition_id}/{question_id}: 'all' != persisted post-fix label")
        if outcomes["neither"] != pre[(condition_id, question_id)]["outcome"]:
            raise AssertionError(f"{condition_id}/{question_id}: 'neither' != persisted pre-fix label")

        base = outcomes["neither"]
        singles = ("fix1_only", "fix2_only", "fix3_only")
        if outcomes["all"] == base:
            bucket = "no_flip"
            note = ""
        else:
            # Attribute on REPRODUCING THE POST-FIX LABEL, not merely on moving
            # the record off `answered_ungrounded`. The two rules disagree for
            # chunk500_hybrid/ref_them_07, a soft abstention: Fix 3 alone gives
            # the actual post-fix label (`abstained`), while Fix 1 alone would
            # also have moved it off ungrounded but to `offtarget`. Only Fix 3
            # explains where the record actually ended up.
            reproducing = [n for n in singles if outcomes[n] == outcomes["all"]]
            movers = [n for n in singles if outcomes[n] != base]
            if len(reproducing) == 1:
                bucket = reproducing[0].replace("_only", "")
            elif not reproducing:
                bucket = "jointly_necessary"
            else:
                bucket = "ambiguous"
            others = [n.replace("_only", "") for n in movers if n not in reproducing]
            note = f"(also moved off ungrounded by {', '.join(others)}, to a different label)" if others else ""
        tally[bucket].append(f"{condition_id}/{question_id}")
        rows.append((condition_id, question_id, pre[(condition_id, question_id)]["case"],
                     base, outcomes["all"], bucket + (" " + note if note else "")))

    print(f"\n{'record':<34} {'case':<5} {'pre':<20} {'post':<28} attributed to")
    for condition_id, question_id, case, base, final, bucket in rows:
        print(f"{condition_id + '/' + question_id:<34} {case:<5} {base:<20} {final:<28} {bucket}")

    n_flips = sum(len(v) for k, v in tally.items() if k != "no_flip")
    print("\n" + "=" * 78)
    print("DEPARTURES FROM answered_ungrounded")
    print(f"  left the label : {n_flips}")
    print(f"  entered        : {len(entered)}")

    # Rule A -- "which single fix reproduces the POST-FIX LABEL".
    print("\nRule A: attributed by which single fix reproduces the post-fix label")
    for key, label in (("fix1", "Fix 1 (comma regex)"), ("fix3", "Fix 3 (soft abstention)"),
                       ("fix2", "Fix 2 (question-echoed trivial exclusion)")):
        print(f"  {label:<45} {len(tally[key]):>2}  {tally[key] if len(tally[key]) <= 3 else ''}")
    for key in ("ambiguous", "jointly_necessary"):
        if tally[key]:
            print(f"  {key:<45} {len(tally[key]):>2}  {tally[key]}")

    # Rule B -- "which single fix is SUFFICIENT to leave answered_ungrounded",
    # regardless of where the record then lands. This is the rule that matches
    # the sentence "N records left the answered_ungrounded label"; it differs
    # from Rule A on exactly the records printed below.
    rule_b: dict[str, list[str]] = {"fix1": [], "fix2": [], "fix3": [], "none": []}
    for condition_id, question_id, case, base, final, bucket in rows:
        if bucket.startswith("no_flip"):
            continue
        answer = json.loads(
            generation_cache_path(MODEL, condition_id, question_id).read_text(encoding="utf-8")
        )["raw_response"]
        chunks = top5_for(condition_id, question_id)
        movers = [
            n.replace("_only", "")
            for n, f1, f2, f3 in DECOMPOSE_CONFIGS
            if n.endswith("_only")
            and classify(answer, questions[question_id], chunks, f1, f2, f3)["outcome"] != base
        ]
        # Fix 1 first: where more than one fix suffices, the comma regex is the
        # one that repairs the mis-extraction the ungrounded verdict rested on.
        key = "fix1" if "fix1" in movers else (movers[0] if movers else "none")
        rule_b[key].append(f"{condition_id}/{question_id}")

    print("\nRule B: attributed by which single fix suffices to LEAVE answered_ungrounded")
    for key, label in (("fix1", "Fix 1 (comma regex)"), ("fix3", "Fix 3 (soft abstention)"),
                       ("fix2", "Fix 2 (question-echoed trivial exclusion)"),
                       ("none", "no single fix suffices")):
        print(f"  {label:<45} {len(rule_b[key]):>2}  {rule_b[key] if len(rule_b[key]) <= 3 else ''}")

    # Rule C -- the REPORTED decomposition: Rule A, falling back to Rule B for
    # a record where no single fix reproduces the post-fix label. This answers
    # "which fix explains where this record ended up, and failing that, which
    # one got it out of `answered_ungrounded`" -- the most informative of the
    # three, and the one whose counts are quoted in README.md and
    # analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md.
    rule_c = {"fix1": list(tally["fix1"]), "fix2": list(tally["fix2"]), "fix3": list(tally["fix3"])}
    for record in tally["jointly_necessary"] + tally["ambiguous"]:
        for key in ("fix1", "fix2", "fix3"):
            if record in rule_b[key]:
                rule_c[key].append(record)
                break

    print("\nRule C (REPORTED): Rule A, falling back to Rule B where no single fix")
    print("                   reproduces the post-fix label")
    for key, label in (("fix1", "Fix 1 (comma regex)"), ("fix3", "Fix 3 (soft abstention)"),
                       ("fix2", "Fix 2 (question-echoed trivial exclusion)")):
        print(f"  {label:<45} {len(rule_c[key]):>2}  {rule_c[key] if len(rule_c[key]) <= 3 else ''}")

    print(f"\n  stayed ungrounded (no flip)                   {len(tally['no_flip']):>2}  {tally['no_flip']}")

    print("\nInvariant checks (rule-independent):")
    checks = [
        ("19 records left answered_ungrounded", n_flips == 19),
        ("0 records entered answered_ungrounded", not entered),
        ("Rule C decomposition is 17 Fix 1 / 1 Fix 3 / 1 Fix 2",
         (len(rule_c["fix1"]), len(rule_c["fix3"]), len(rule_c["fix2"])) == (17, 1, 1)),
        ("Fix 2 reproduces the post-fix label for exactly 1 record",
         tally["fix2"] == ["chunk200_bm25/ref_fact_05"]),
        ("Fix 2 suffices to leave ungrounded for exactly 1 record",
         rule_b["fix2"] == ["chunk200_bm25/ref_fact_05"]),
        ("that record is Case C, so Fix 2 caused 0 of the 15 Case B flips",
         all(r[2] != "B" for r in rows if r[1] == "ref_fact_05" and r[0] == "chunk200_bm25")),
    ]
    for label, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    return 0 if all(ok for _, ok in checks) else 1


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    global MODEL
    parser.add_argument("--decompose", action="store_true",
                        help="attribute every departure from answered_ungrounded across all 270")
    parser.add_argument("--model", default=MODEL,
                        help=f"generator model to analyse (default: {MODEL})")
    args = parser.parse_args()
    assert_prefix_model(args.model)
    MODEL = args.model  # trace() reads this module-level value for cache paths

    questions = {
        json.loads(l)["id"]: json.loads(l)
        for l in BENCHMARK_PATH.read_text(encoding="utf-8").splitlines()
        if l.strip()
    }
    pre = load_table(PRE_TABLE, args.model)
    post = load_table(generation_outcomes_path(args.model), args.model)

    if args.decompose:
        return decompose(questions, pre, post)

    print("Counterfactual fix attribution -- 4 Case C ungrounded -> correct flips")
    print("=" * 78)

    summary = []
    for condition_id, question_id in TARGETS:
        record = json.loads(
            generation_cache_path(MODEL, condition_id, question_id).read_text(encoding="utf-8")
        )
        answer = record["raw_response"]
        question = questions[question_id]
        chunks = load_stage1_top5(condition_id, question_id)

        # Fix 3 must be inert here: none of these four is an abstention.
        if evaluate.contains_abstention_sentence(answer):
            raise AssertionError(
                f"{condition_id}/{question_id} contains the canonical abstention sentence -- "
                "Fix 3 is NOT inert for this record and this counterfactual measures the wrong thing"
            )

        outcomes = {}
        details = {}
        for name, fix1, fix2 in CONFIGS:
            result = classify(answer, question, chunks, fix1, fix2)
            outcomes[name] = result["outcome"]
            details[name] = result

        # Trust assertions.
        live = evaluate.classify_outcome(answer, question, chunks)["outcome"]
        if outcomes["both"] != live:
            raise AssertionError(
                f"{condition_id}/{question_id}: 'both' config gives {outcomes['both']!r} but the "
                f"real evaluate.classify_outcome gives {live!r} -- the harness has drifted"
            )
        if outcomes["both"] != post[(condition_id, question_id)]["outcome"]:
            raise AssertionError(f"{condition_id}/{question_id}: 'both' != persisted post-fix label")
        if outcomes["neither"] != pre[(condition_id, question_id)]["outcome"]:
            raise AssertionError(
                f"{condition_id}/{question_id}: 'neither' gives {outcomes['neither']!r} but the "
                f"persisted PRE-fix label is {pre[(condition_id, question_id)]['outcome']!r}"
            )

        flipped = {n: outcomes[n] != outcomes["neither"] for n, _, _ in CONFIGS}
        if flipped["fix1_only"] and not flipped["fix2_only"]:
            verdict = "FIX 1 alone is sufficient; Fix 2 not necessary"
        elif flipped["fix2_only"] and not flipped["fix1_only"]:
            verdict = "FIX 2 alone is sufficient -- Fix 2 IS load-bearing"
        elif flipped["fix1_only"] and flipped["fix2_only"]:
            verdict = "EITHER fix alone is sufficient -- Fix 2 is sufficient but not necessary"
        elif flipped["both"]:
            verdict = "JOINTLY NECESSARY -- neither fix alone flips it; Fix 2 IS load-bearing"
        else:
            verdict = "no flip (unexpected)"

        print(f"\n{condition_id} / {question_id}   (question: {question['question'][:70]}...)")
        print(f"  question's own numeric claims (post-fix regex): "
              f"{sorted(set(extract_claims(question['question'], True)))}")
        for name, _, _ in CONFIGS:
            d = details[name]
            print(f"    {name:<10} -> {d['outcome']:<28} "
                  f"checked={d.get('claims', [])} unsupported={d['unsupported_claims']}")
        print(f"  VERDICT: {verdict}")

        # Per-claim: which claims changed verification status, and by which
        # mechanism. A claim can stop being unsupported two ways, and they must
        # not be confused: Fix 1 changes the claim's STRING (dropping a
        # trailing sentence comma) so it now matches the context, while Fix 2
        # removes the claim from the checked set entirely. Fix 2 can only be
        # credited in a config where Fix 2 is actually on -- attributing an
        # exclusion to it under fix1_only would invent an effect.
        # Attribution is purely OBSERVATIONAL -- read off each config's own
        # checked/unsupported sets. Re-deriving Fix 2's rule here would be a
        # second implementation of it and can disagree with what the config
        # actually did: `is_trivial_claim("2023,")` is False (that is precisely
        # the pre-Fix-1 bug), so a normalized re-test would wrongly report the
        # claim as excluded in a config where it was still checked and failed.
        base_unsup = set(details["neither"]["unsupported_claims"])
        for name, fix1, fix2 in CONFIGS:
            if name == "neither":
                continue
            now_unsup = set(details[name]["unsupported_claims"])
            checked = set(details[name].get("claims", []))

            repaired, excluded, still = [], [], []
            for claim in sorted(base_unsup):
                normalized = POST_FIX1_RE.findall(claim)
                normalized = normalized[0] if normalized else claim
                if claim in now_unsup or normalized in now_unsup:
                    still.append(claim)
                elif normalized in checked and normalized != claim:
                    repaired.append(f"{claim!r}->{normalized!r}")
                elif claim in checked:
                    repaired.append(repr(claim))
                else:
                    excluded.append(claim)

            bits = []
            if repaired:
                bits.append(f"re-extracted, then found in context (Fix 1): {', '.join(repaired)}")
            if excluded:
                bits.append(f"excluded from checking (Fix 2): {excluded}")
            if still:
                bits.append(f"still unsupported: {still}")
            print(f"    under {name:<10}: {'; '.join(bits)}")

        summary.append((condition_id, question_id, verdict, outcomes))

    print("\n" + "=" * 78)
    print("SUMMARY (2x2 cell per record)")
    print(f"{'record':<34} {'fix1_only':<12} {'fix2_only':<12} {'both':<12}")
    for condition_id, question_id, verdict, outcomes in summary:
        short = {
            evaluate.OUTCOME_UNGROUNDED: "ungrounded",
            evaluate.OUTCOME_GROUNDED_CORRECT: "correct",
            evaluate.OUTCOME_GROUNDED_OFFTARGET: "offtarget",
            evaluate.OUTCOME_ABSTAINED: "abstained",
        }
        print(f"{condition_id + '/' + question_id:<34} "
              f"{short[outcomes['fix1_only']]:<12} {short[outcomes['fix2_only']]:<12} "
              f"{short[outcomes['both']]:<12}")

    fix2_loadbearing = [s for s in summary if "load-bearing" in s[2]]
    print()
    if fix2_loadbearing:
        print(f"Fix 2 IS load-bearing for {len(fix2_loadbearing)}/4 Case C flips: "
              f"{[s[0] + '/' + s[1] for s in fix2_loadbearing]}")
        print('=> The true sentence is: "Fix 2 caused zero of the 15 CASE B flips."')
        print('   The unqualified "zero of the flips" claim is FALSE.')
    else:
        print("Fix 2 is load-bearing for NONE of the 4 Case C flips.")
        print('=> The unqualified claim holds across Case B and Case C alike.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
