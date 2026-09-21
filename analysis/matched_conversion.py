"""Matched-subset Case C conversion: is the pooled jump real, or composition?

The problem
-----------
Case C membership is *defined* by whether the gold anchor reached the top-5, so
enrichment changes who is in Case C at the same time as it changes what the
generator does with them, and the enriched Case C set is the larger of the two.
Comparing the two pooled conversion rates therefore compares two different
populations, and if the items that enrichment newly admits are systematically
easier, the apparent gain could be composition rather than improvement.

This partitions the enriched Case C against its matched text_only counterpart,
per (chunk_size, strategy) pair, per question:

    intersection    Case C in BOTH arms   -- the like-for-like population
    newly entered   Case C in enriched only
    lost            Case C in text_only only

`intersection + lost` must equal the text_only Case C total and
`intersection + newly entered` the enriched total; both are asserted.

The conversion rate ON THE INTERSECTION, computed for both arms, is the
like-for-like comparison: same items, same questions, only the representation
differs.

Why a real effect is possible despite the generator never seeing metadata
-------------------------------------------------------------------------
`generate.format_context` reads `chunk["text"]`, never `index_text`, and
`run_generation.build_items` puts only `{chunk_id, text}` into `top5_chunks` --
so the enriched string is not in the prompt at all. But enrichment changes WHICH
five chunks are in the context window, and a top-5 with fewer off-company
distractors is a different (cleaner) prompt even though every individual chunk
is rendered identically. So the mechanism exists; this script measures whether
it shows up, without assuming either answer.

Assertions
----------
Beyond the partition reconciliation (a structural invariant), the run asserts
every figure this document publishes: `b` in all four scopes, the intersection
conversion counts behind the two headline rates, and BOTH McNemar results so the
anti-conservative one and the conservative one that replaced it cannot silently
diverge. It also asserts the MEMBERSHIP of b and c, not only their cardinality:
a pinned count can survive a swap in the underlying set, which is exactly what
happened under q8 when `c = 7` passed while one pair left and another entered.
Expectations are loaded per `--model` from
`analysis/expectations/{model_slug}.json`; the q4 set holds exactly the numbers
previously hardcoded here. A model with no set is announced as FIRST RUN and its
figures are reported as unpinned, never as passing. The script refuses to write
the document if a pinned figure or membership moves.

Read-only. Writes one Markdown report.

Usage
-----
    python analysis/matched_conversion.py
    python analysis/matched_conversion.py --model qwen3.8-27b@q8_k_xl
"""

from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

from scipy.stats import binomtest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from model_paths import (  # noqa: E402
    analysis_path, ensure_analysis_dir, expectations_path, generation_outcomes_path,
    load_expectations,
)

# Model-scoped: results/tables/{model_slug}/generation_outcomes.csv
# Resolved per --model so a q8 table is never read under a q4 label.
# Model-scoped via analysis_path(): q4 resolves to the existing
# analysis/qwen3.8-27b_q4_k_xl/matched_conversion.md; any other generator writes into its own
# analysis/{slug}/ subdirectory. Resolved in main() from --model.
OUT_MD_NAME = "matched_conversion.md"

DEFAULT_MODEL = "qwen3.8-27b@q4_k_xl"
BASE_CONDITIONS = ["chunk200_dense", "chunk200_bm25", "chunk200_hybrid",
                   "chunk500_dense", "chunk500_bm25", "chunk500_hybrid"]
CORRECT = "answered_grounded_correct"
OUTCOMES = ["abstained", CORRECT, "answered_grounded_offtarget", "answered_ungrounded"]
CATEGORIES = ["factual", "thematic", "comparative"]


def load(model: str) -> dict:
    """{(condition_id, question_id): row} for one model."""
    path = generation_outcomes_path(model)
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["model"] == model]
    if not rows:
        raise SystemExit(f"no rows in {path} for model {model!r}")
    return {(r["condition_id"], r["question_id"]): r for r in rows}


def _q_word(n: int) -> str:
    """"question"/"questions" -- the b-observation count is data-dependent."""
    return "question" if n == 1 else "questions"


def rate(n_correct: int, n: int) -> str:
    return f"{n_correct / n:.1%}" if n else "n/a"


def pooled_mcnemar(pairs, data, correct=CORRECT):
    """Exact McNemar over paired (text_only, enriched) observations.

    `b` = correct under text_only but not enriched; `c` = correct under
    enriched but not text_only. Concordant pairs carry no information for
    McNemar and are counted only for reporting.

    Uses the EXACT binomial form -- `binomtest(max(b, c), b + c, 0.5)`,
    two-sided -- not the chi-square approximation, which is unreliable at the
    single-digit discordant counts seen here. Same formulation as Stage 2's A1.
    """
    b = c = concordant = 0
    for base, q in pairs:
        t = data[(base, q)]["outcome"] == correct
        e = data[(f"{base}_enriched", q)]["outcome"] == correct
        if t and not e:
            b += 1
        elif e and not t:
            c += 1
        else:
            concordant += 1
    n_disc = b + c
    p = float(binomtest(max(b, c), n_disc, 0.5).pvalue) if n_disc else None
    return {"n_pairs": len(pairs), "b_textonly_only": b, "c_enriched_only": c,
            "concordant": concordant, "n_disc": n_disc, "p": p}


def question_level_mcnemar(pairs, data, correct=CORRECT, rule="all_pairs"):
    """Exact McNemar with each QUESTION contributing exactly one observation.

    The observation-level test above is anti-conservative: the 38 intersection
    observations come from only 13 distinct questions, so a question appearing
    in 5 condition pairs contributes 5 correlated observations that the binomial
    treats as 5 independent trials. Collapsing to one observation per question
    removes that dependence.

    Tie-breaking rule (`rule="all_pairs"`, the primary): a question is an
    enriched win if it is correct-under-enriched-and-not-text_only in a strict
    MAJORITY of the condition pairs where it appears in the intersection, a
    text_only win in the reverse case, and concordant otherwise -- which
    includes exact ties and, importantly, questions discordant in only a
    minority of their pairs. The denominator is all of the question's
    intersection pairs, not just its discordant ones.

    `rule="discordant_only"` is reported alongside as a sensitivity check: the
    majority is taken over the question's DISCORDANT pairs only, so a question
    discordant in 1 of 4 pairs still counts as a win rather than concordant.
    It is the more permissive of the two.
    """
    per_q: dict[str, list[int]] = {}
    for base, q in pairs:
        t = data[(base, q)]["outcome"] == correct
        e = data[(f"{base}_enriched", q)]["outcome"] == correct
        per_q.setdefault(q, []).append(0 if t == e else (-1 if t else 1))

    b = c = concordant = 0
    detail = []
    for q, votes in sorted(per_q.items()):
        enr = sum(1 for v in votes if v == 1)
        txt = sum(1 for v in votes if v == -1)
        denom = len(votes) if rule == "all_pairs" else (enr + txt)
        if denom and enr > denom / 2:
            c += 1; verdict = "enriched"
        elif denom and txt > denom / 2:
            b += 1; verdict = "text_only"
        else:
            concordant += 1; verdict = "concordant"
        detail.append({"question_id": q, "n_pairs": len(votes), "enriched_wins": enr,
                       "text_only_wins": txt, "verdict": verdict})

    n_disc = b + c
    p = float(binomtest(max(b, c), n_disc, 0.5).pvalue) if n_disc else None
    return {"n_questions": len(per_q), "b_textonly_only": b, "c_enriched_only": c,
            "concordant": concordant, "n_disc": n_disc, "p": p, "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"generator model to analyse (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    data = load(args.model)
    exp = load_expectations(args.model)
    first_run = exp is None
    questions = sorted({q for _, q in data})

    partition: dict[str, list[tuple[str, str]]] = {"intersection": [], "newly": [], "lost": []}
    per_pair: dict[str, dict[str, int]] = {}

    for base in BASE_CONDITIONS:
        enr = f"{base}_enriched"
        counts = collections.Counter()
        for q in questions:
            t, e = data.get((base, q)), data.get((enr, q))
            if t is None or e is None:
                continue
            in_t, in_e = t["case"] == "C", e["case"] == "C"
            if in_t and in_e:
                partition["intersection"].append((base, q)); counts["intersection"] += 1
            elif in_e:
                partition["newly"].append((base, q)); counts["newly"] += 1
            elif in_t:
                partition["lost"].append((base, q)); counts["lost"] += 1
        per_pair[base] = dict(counts)

    n_int = len(partition["intersection"])
    n_new = len(partition["newly"])
    n_lost = len(partition["lost"])
    total_t = sum(1 for k, r in data.items() if not k[0].endswith("_enriched") and r["case"] == "C")
    total_e = sum(1 for k, r in data.items() if k[0].endswith("_enriched") and r["case"] == "C")

    problems = []
    if n_int + n_lost != total_t:
        problems.append(f"intersection + lost = {n_int + n_lost}, text_only Case C total = {total_t}")
    if n_int + n_new != total_e:
        problems.append(f"intersection + newly = {n_int + n_new}, enriched Case C total = {total_e}")
    if problems:
        raise SystemExit("PARTITION DOES NOT RECONCILE:\n  " + "\n  ".join(problems))

    def outcome_counts(pairs, arm):
        c = collections.Counter()
        for base, q in pairs:
            cid = base if arm == "text_only" else f"{base}_enriched"
            c[data[(cid, q)]["outcome"]] += 1
        return c

    int_t, int_e = outcome_counts(partition["intersection"], "text_only"), outcome_counts(partition["intersection"], "enriched")
    new_e = outcome_counts(partition["newly"], "enriched")
    lost_t = outcome_counts(partition["lost"], "text_only")

    def cat_counts(pairs):
        c = collections.Counter(data[(b, q)]["category"] for b, q in pairs)
        return c

    lines = [
        "# Matched-subset Case C conversion",
        "",
        f"Model: `{args.model}`. Source: "
        f"`{generation_outcomes_path(args.model).relative_to(REPO_ROOT).as_posix()}`.",
        "",
        "Case C membership depends on whether the gold anchor reached the top-5, so the",
        "enriched and text_only Case C sets are different populations. Every enriched",
        "condition is compared against its matched text_only counterpart (same chunk size,",
        "same strategy), per question.",
        "",
        "**The generator never sees the enrichment.** `generate.format_context` renders",
        "`chunk[\"text\"]` only, `run_generation.build_items` puts only `{chunk_id, text}` into",
        "`top5_chunks`, and `src/generate.py` is byte-identical to its committed version --",
        "verified, not assumed. What enrichment changes is *which five chunks* occupy the",
        "context window, not how any one of them is rendered.",
        "",
        "## 1. Partition sizes",
        "",
        f"| set | n |", "|---|--:|",
        f"| intersection (Case C in both arms) | **{n_int}** |",
        f"| newly entered (enriched only) | **{n_new}** |",
        f"| lost (text_only only) | **{n_lost}** |",
        "",
        f"Reconciliation: intersection + lost = {n_int} + {n_lost} = **{n_int + n_lost}** "
        f"(text_only Case C total {total_t}); intersection + newly = {n_int} + {n_new} = "
        f"**{n_int + n_new}** (enriched Case C total {total_e}). Both check.",
        "",
        "Per matched pair:",
        "",
        "| matched pair | intersection | newly entered | lost | text_only C | enriched C |",
        "|---|--:|--:|--:|--:|--:|",
    ]
    for base in BASE_CONDITIONS:
        c = per_pair[base]
        i, n, l = c.get("intersection", 0), c.get("newly", 0), c.get("lost", 0)
        lines.append(f"| {base} | {i} | {n} | {l} | {i + l} | {i + n} |")

    lines += [
        "",
        "## 2. Conversion on the intersection — the like-for-like comparison",
        "",
        f"Same {n_int} (condition, question) items in both arms; only the representation differs.",
        "",
        "| arm | n | correct | abstained | offtarget | ungrounded | **rate** |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for label, c in (("text_only", int_t), ("enriched", int_e)):
        lines.append(f"| {label} | {n_int} | {c[CORRECT]} | {c['abstained']} | "
                     f"{c['answered_grounded_offtarget']} | {c['answered_ungrounded']} | "
                     f"**{rate(c[CORRECT], n_int)}** |")

    lines += [
        "",
        "## 3. Conversion on the newly-entered set",
        "",
        f"The {n_new} items that are Case C only under enrichment (no text_only counterpart,",
        "so a single-arm figure by construction).",
        "",
        "| set | n | correct | abstained | offtarget | ungrounded | rate |",
        "|---|--:|--:|--:|--:|--:|--:|",
        f"| newly entered (enriched) | {n_new} | {new_e[CORRECT]} | {new_e['abstained']} | "
        f"{new_e['answered_grounded_offtarget']} | {new_e['answered_ungrounded']} | "
        f"**{rate(new_e[CORRECT], n_new)}** |",
        f"| lost (text_only) | {n_lost} | {lost_t[CORRECT]} | {lost_t['abstained']} | "
        f"{lost_t['answered_grounded_offtarget']} | {lost_t['answered_ungrounded']} | "
        f"{rate(lost_t[CORRECT], n_lost)} |",
        "",
        "## 4. Category composition",
        "",
        "| category | intersection | newly entered | lost |",
        "|---|--:|--:|--:|",
    ]
    ci, cn, cl = cat_counts(partition["intersection"]), cat_counts(partition["newly"]), cat_counts(partition["lost"])
    for cat in CATEGORIES:
        lines.append(f"| {cat} | {ci[cat]} ({ci[cat]/n_int:.0%}) | {cn[cat]} ({cn[cat]/n_new:.0%}) | "
                     f"{cl[cat]} ({cl[cat]/n_lost:.0%} of {n_lost}) |" if n_lost else
                     f"| {cat} | {ci[cat]} ({ci[cat]/n_int:.0%}) | {cn[cat]} ({cn[cat]/n_new:.0%}) | 0 |")
    lines += [
        "",
        "Per-category conversion rate, intersection (both arms) vs newly entered:",
        "",
        "| category | intersection text_only | intersection enriched | newly entered |",
        "|---|--:|--:|--:|",
    ]
    for cat in CATEGORIES:
        ii = [(b, q) for b, q in partition["intersection"] if data[(b, q)]["category"] == cat]
        nn = [(b, q) for b, q in partition["newly"] if data[(b, q)]["category"] == cat]
        it = sum(1 for b, q in ii if data[(b, q)]["outcome"] == CORRECT)
        ie = sum(1 for b, q in ii if data[(f"{b}_enriched", q)]["outcome"] == CORRECT)
        ne = sum(1 for b, q in nn if data[(f"{b}_enriched", q)]["outcome"] == CORRECT)
        lines.append(f"| {cat} | {rate(it, len(ii))} (n={len(ii)}) | {rate(ie, len(ii))} (n={len(ii)}) | "
                     f"{rate(ne, len(nn))} (n={len(nn)}) |")
    lines.append("")

    # --- Section 5: both McNemar variants, side by side --------------------
    obs_per_q = collections.Counter(q for _, q in partition["intersection"])
    disc_detail = []
    for base, q in partition["intersection"]:
        t = data[(base, q)]["outcome"] == CORRECT
        e = data[(f"{base}_enriched", q)]["outcome"] == CORRECT
        if t != e:
            disc_detail.append((q, data[(base, q)]["category"], base,
                                "text_only" if t else "enriched"))

    lines += [
        "## 5. Is the conversion difference statistically supported?",
        "",
        "> **Specified after the descriptive result was seen.** These tests were added once",
        "> the section 2 conversion figures had been observed, to formalise an already-visible",
        "> pattern. They are **not pre-registered comparisons**; read them as descriptive of",
        "> this sample rather than confirmatory. Recorded so the artifact states the order of",
        "> operations.",
        "",
        "### 5.0 The independence problem, stated first",
        "",
        f"The {n_int} intersection observations come from only **{len(obs_per_q)} distinct "
        "questions** -- the same question contributes one observation per condition pair where",
        "it is Case C in both arms. Those observations are correlated: a question that converts",
        "well under enrichment tends to do so in every condition.",
        "",
        "| condition pairs contributed | questions |",
        "|---|--:|",
    ]
    for k, v in sorted(collections.Counter(obs_per_q.values()).items()):
        lines.append(f"| {k} | {v} |")
    lines += ["", "| category | observations | distinct questions |", "|---|--:|--:|"]
    for cat in CATEGORIES:
        obs = [(b, q) for b, q in partition["intersection"] if data[(b, q)]["category"] == cat]
        lines.append(f"| {cat} | {len(obs)} | {len({q for _, q in obs})} |")

    dq = collections.defaultdict(list)
    for q, cat, base, w in disc_detail:
        dq[q].append((cat, base, w))
    lines += [
        "",
        f"**The {len(disc_detail)} discordant observations come from only {len(dq)} distinct "
        "questions:**",
        "",
        "| question | category | discordant in | of its intersection pairs | winner | condition pairs |",
        "|---|---|--:|--:|---|---|",
    ]
    for q in sorted(dq):
        cat = dq[q][0][0]
        winners = sorted({w for _, _, w in dq[q]})
        lines.append(f"| `{q}` | {cat} | {len(dq[q])} | {obs_per_q[q]} | {', '.join(winners)} | "
                     f"{', '.join(b for _, b, _ in dq[q])} |")

    lines += [
        "",
        "### 5.1 Observation-level test -- **ANTI-CONSERVATIVE, do not quote alone**",
        "",
        "Each (question, chunk size, strategy) item is one trial. **The observations are not",
        "independent** (see 5.0), so the exact binomial treats correlated observations as",
        "independent trials and the p-values below are too small, possibly severely so.",
        "Retained for transparency, not as the headline.",
        "",
        "**Test: exact McNemar** -- `binomtest(max(b, c), b + c, 0.5)`, two-sided. Not the",
        "chi-square approximation; discordant counts are single-digit.",
        "",
        "| population | pairs | b (text_only only) | c (enriched only) | concordant | n disc | p (exact) |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    scopes = [("pooled", partition["intersection"])] + [
        (cat, [(b, q) for b, q in partition["intersection"] if data[(b, q)]["category"] == cat])
        for cat in CATEGORIES
    ]
    for label, pairs in scopes:
        if not pairs:
            lines.append(f"| {label} | 0 | - | - | - | - | n/a (empty) |")
            continue
        m = pooled_mcnemar(pairs, data)
        p_txt = "n/a (no discordant pairs)" if m["p"] is None else f"{m['p']:.4f}"
        lines.append(f"| {label} | {m['n_pairs']} | {m['b_textonly_only']} | {m['c_enriched_only']} | "
                     f"{m['concordant']} | {m['n_disc']} | {p_txt} |")

    lines += [
        "",
        "### 5.2 Question-level test -- **the conservative version, quote this one**",
        "",
        "Each question contributes exactly one observation. **Tie-breaking rule:** a question is",
        "an enriched win if it is correct-under-enriched-and-not-text_only in a strict majority",
        "of the condition pairs where it appears in the intersection; a text_only win in the",
        "reverse case; concordant otherwise -- which includes exact ties and questions discordant",
        "in only a minority of their pairs. The denominator is all of the question's intersection",
        "pairs, not only its discordant ones. Applied identically to every row.",
        "",
        "| population | questions | b (text_only only) | c (enriched only) | concordant | n disc | p (exact) |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for label, pairs in scopes:
        if not pairs:
            lines.append(f"| {label} | 0 | - | - | - | - | n/a (empty) |")
            continue
        m = question_level_mcnemar(pairs, data)
        p_txt = "n/a (no discordant questions)" if m["p"] is None else f"{m['p']:.4f}"
        lines.append(f"| {label} | {m['n_questions']} | {m['b_textonly_only']} | {m['c_enriched_only']} | "
                     f"{m['concordant']} | {m['n_disc']} | {p_txt} |")

    lines += [
        "",
        "**Sensitivity check** -- the same test with the majority taken over each question's",
        "DISCORDANT pairs only, so a question discordant in 1 of 4 pairs counts as a win rather",
        "than concordant. This is the more permissive rule; reported because it changes n.",
        "",
        "| population | questions | b | c | concordant | n disc | p (exact) |",
        "|---|--:|--:|--:|--:|--:|--:|",
    ]
    for label, pairs in scopes:
        if not pairs:
            continue
        m = question_level_mcnemar(pairs, data, rule="discordant_only")
        p_txt = "n/a" if m["p"] is None else f"{m['p']:.4f}"
        lines.append(f"| {label} | {m['n_questions']} | {m['b_textonly_only']} | {m['c_enriched_only']} | "
                     f"{m['concordant']} | {m['n_disc']} | {p_txt} |")

    pooled_q = question_level_mcnemar(partition["intersection"], data)
    pooled_o = pooled_mcnemar(partition["intersection"], data)
    q_p = "n/a" if pooled_q["p"] is None else f"{pooled_q['p']:.4f}"
    o_p = "n/a" if pooled_o["p"] is None else f"{pooled_o['p']:.4f}"
    # The b = 0 claim is CONDITIONAL on the computed values -- never hardcoded.
    #
    # It held at BOTH levels under q4, but only at question level under q8
    # (b = 2 observations) and under Flash-Next (b = 1). Emitting it unscoped
    # therefore published, in two arms, a claim this document's own 5.1 table
    # contradicts two sections earlier. The required wording: a
    # sentence claiming "no item converted under text_only but not under
    # metadata_enriched" must be scoped to the question level, or restated as a
    # count of observations and of the distinct questions they come from.
    #
    # Three branches, because all three states are reachable and only the first
    # supports the unscoped claim. The first reproduces the original sentence
    # verbatim so the arm where it is true (q4) regenerates byte-identically.
    b_obs = pooled_o["b_textonly_only"]
    b_qlev = pooled_q["b_textonly_only"]
    b_obs_questions = sorted({q for base, q in partition["intersection"]
                              if data[(base, q)]["outcome"] == CORRECT
                              and data[(f"{base}_enriched", q)]["outcome"] != CORRECT})
    if b_obs == 0 and b_qlev == 0:
        b_claim = (
            f"> **b = 0 everywhere.** Across all {n_int} matched observations and all "
            f"{len(obs_per_q)} distinct questions, in every category, **not one item was correct "
            "under `text_only` and incorrect under `metadata_enriched`.** Every discordant "
            "observation runs in the same direction. This is a property of the observed data, not an "
            "inference from a test, and it does not depend on the independence assumption that makes "
            "5.1 unsafe."
        )
    elif b_qlev == 0:
        b_claim = (
            f"> **b = 0 at the question level -- and ONLY there.** Across all {len(obs_per_q)} "
            "distinct questions, in every category, **not one was correct under `text_only` and "
            "incorrect under `metadata_enriched`.** At observation level that claim is FALSE and "
            f"must not be stated: {b_obs} of {n_int} matched observations, from "
            f"{len(b_obs_questions)} distinct {_q_word(len(b_obs_questions))} "
            f"({', '.join(b_obs_questions)}), converted "
            "under `text_only` but not under `metadata_enriched` -- each a minority within its own "
            "question, which is why each falls to `concordant` under the `all_pairs` tie-breaking "
            "rule in 5.2. Quote this scoped to the question level; an unscoped \"b = 0 everywhere\" "
            "contradicts 5.1 above. The scoped claim is a property of the observed data, not an "
            "inference from a test, and it does not depend on the independence assumption that "
            "makes 5.1 unsafe."
        )
    else:
        b_claim = (
            f"> **b is NOT zero at either level.** {b_obs} of {n_int} matched observations, from "
            f"{len(b_obs_questions)} distinct {_q_word(len(b_obs_questions))} "
            f"({', '.join(b_obs_questions)}), were "
            "correct under `text_only` and incorrect under `metadata_enriched`, and at question "
            f"level {b_qlev} of {len(obs_per_q)} questions resolve the same way. **The claim that "
            "no item converted under `text_only` but not under `metadata_enriched` does not hold "
            "at observation level or at question level, and must not be stated in either scope.** "
            "Discordant observations run in both directions here, so 5.1 and 5.2 carry the whole "
            "of what this comparison supports."
        )

    lines += [
        "",
        "### 5.3 What the two tests jointly support",
        "",
        f"The observation-level test gives p={o_p} pooled; the question-level test gives",
        f"p={q_p}. **The question-level test does not reach significance at any conventional",
        "threshold, and it is the one to quote.** The observation-level result is an artifact of",
        "counting correlated observations as independent trials. **There is no statistically",
        "supported claim here that enrichment improves Case C conversion on comparable items** --",
        f"{pooled_q['n_disc']} discordant questions cannot support one.",
        "",
        "**What does stand, independent of any test, as a descriptive fact:**",
        "",
        b_claim,
        "",
        "No multiple-comparison correction is applied within either table: each is one pooled",
        "test plus three category partitions of the same data, not independent families.",
        "",
    ]

    # --- Assert the published figures ---------------------------------------
    #
    # The partition reconciliation above is a structural invariant: it proves the
    # three sets are a partition, not that any reported number is still what was
    # published. Those are different failures. The figures below are the ones
    # quoted, and every one of them moves if a generation is re-scored or a
    # condition is re-run -- which is the side worth asserting.
    #
    # b = 0 comes first because it is the claim that survived when the
    # observation-level McNemar did not: no item was correct under text_only and
    # incorrect under metadata_enriched, in any category. It is a property of the
    # observed data rather than an inference, so it is the one figure here that
    # does not depend on a test's assumptions -- and the one most worth pinning.
    #
    # Both McNemar results are asserted together so they cannot silently diverge:
    # the anti-conservative observation-level p and the conservative
    # question-level p that replaced it as the reported result.
    #
    # Expectations are per-model DATA, loaded from
    # analysis/expectations/{model_slug}.json, NOT literals here. The q4 set
    # holds exactly the values that used to be hardcoded at this spot. A model
    # with no set is FIRST RUN: figures are computed and reported as UNPINNED,
    # never as passing, so a second generator can neither inherit q4's pins nor
    # quietly skip the check.
    obs = pooled_mcnemar(partition["intersection"], data)
    qlev = question_level_mcnemar(partition["intersection"], data)
    int_correct_t = sum(1 for b, q in partition["intersection"]
                        if data[(b, q)]["outcome"] == CORRECT)
    int_correct_e = sum(1 for b, q in partition["intersection"]
                        if data[(f"{b}_enriched", q)]["outcome"] == CORRECT)

    # MEMBERSHIP of b and c, not only their cardinality.
    #
    # Under q8 the pinned `c = 7` PASSED while one pair left the set and another
    # entered it: a count survived a two-item swap. A pinned count with an
    # unpinned population is precisely the hole this closes. Stored and compared
    # as SETS of "condition|question" strings, so ordering can never read as a
    # failure and a swap can never read as a pass.
    b_members, c_members = [], []
    for base, q in sorted(partition["intersection"]):
        t_ok = data[(base, q)]["outcome"] == CORRECT
        e_ok = data[(f"{base}_enriched", q)]["outcome"] == CORRECT
        if t_ok and not e_ok:
            b_members.append(f"{base}|{q}")
        elif e_ok and not t_ok:
            c_members.append(f"{base}|{q}")

    computed = [("b pooled (correct under text_only only)",
                 obs["b_textonly_only"])]
    for cat in CATEGORIES:
        cat_pairs = [(b, q) for b, q in partition["intersection"]
                     if data[(b, q)]["category"] == cat]
        computed.append((f"b {cat}", pooled_mcnemar(cat_pairs, data)["b_textonly_only"]))
    computed += [
        ("intersection n", n_int),
        ("intersection correct, text_only", int_correct_t),
        ("intersection correct, enriched", int_correct_e),
        ("observation-level McNemar c (enriched-only wins)", obs["c_enriched_only"]),
        ("observation-level McNemar p", round(obs["p"], 4)),
        ("question-level distinct questions", qlev["n_questions"]),
        ("question-level b", qlev["b_textonly_only"]),
        ("question-level c", qlev["c_enriched_only"]),
        ("question-level McNemar p", round(qlev["p"], 4)),
    ]

    failures = []
    if first_run:
        print(f"\n*** FIRST RUN -- no expectation set for model {args.model!r}.")
        print("*** Every figure below was COMPUTED AND NOT CHECKED against anything.")
        print(f"*** Pin deliberately by creating "
              f"{expectations_path(args.model).relative_to(REPO_ROOT).as_posix()}")
        print("Computed figures (unpinned):")
        for label, got in computed:
            print(f"  ----  {label:<52} {got}   unpinned")
        print(f"  ----  {'b membership':<52} {b_members or '(empty)'}")
        print(f"  ----  {'c membership':<52} {c_members or '(empty)'}")
    else:
        expected = exp["matched_conversion"]["figures"]
        members = exp["matched_conversion"]["membership"]
        print("Published figures:")
        for label, got in computed:
            exp_v = expected[label]
            ok_row = got == exp_v
            print(f"  {'PASS' if ok_row else 'FAIL'}  {label:<52} {got}   expected {exp_v}")
            if not ok_row:
                failures.append(f"{label}: computed {got}, expected {exp_v}")
        for label, got_set, exp_set in (
                ("b membership", b_members, members["b_textonly_only"]),
                ("c membership", c_members, members["c_enriched_only"])):
            ok_row = set(got_set) == set(exp_set)
            print(f"  {'PASS' if ok_row else 'FAIL'}  {label:<52} "
                  f"{len(got_set)} item(s)   expected {len(exp_set)}")
            if not ok_row:
                entered = sorted(set(got_set) - set(exp_set))
                left = sorted(set(exp_set) - set(got_set))
                print(f"        entered: {entered or '(none)'}")
                print(f"        left   : {left or '(none)'}")
                failures.append(f"{label}: entered {entered}, left {left}")
    if failures:
        print("\n  REFUSING TO WRITE -- a published figure has moved:")
        for f_ in failures:
            print(f"    {f_}")
        print("  This is a finding, not something to accommodate. Do not update the\n"
              "  expected values without establishing what changed underneath them.")
        return 1
    print("  all reproduce exactly\n" if not first_run
          else "  NOTHING CHECKED -- FIRST RUN, figures above are unpinned\n")

    if first_run:
        lines.insert(0, "> **FIRST RUN -- nothing was validated against.** No expectation "
                        f"set existed for model `{args.model}` when this was written, so "
                        "every figure below is COMPUTED AND UNCHECKED. Pin the model "
                        "deliberately before citing any of it.")
        lines.insert(1, "")
    ensure_analysis_dir(args.model)
    out_md = analysis_path(args.model, OUT_MD_NAME)
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"-> {out_md.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
