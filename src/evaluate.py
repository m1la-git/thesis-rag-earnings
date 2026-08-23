"""Score retrieval and answer quality, and tag failure modes.

Computes **anchor coverage@5** and **MRR@5** against manually labeled gold
anchors, answer similarity (cosine over embeddings, descriptive-only on Case C)
against reference answers, and classifies each generation by ground-truth
**case** (A: unanswerable, B: answerable/gold-absent-from-top-5, C:
answerable/gold-present) crossed with a mechanically-derived **outcome**
(abstained / answered_grounded_correct / answered_grounded_offtarget /
answered_ungrounded) -- see `classify_case`, `classify_outcome`. This
mechanical outcome check is a coarse, fully-automatic proxy (verbatim numeric
substring tracing) for faithfulness, not a replacement for the deeper manual
faithfulness check on a subset, done by the researcher.

Gold anchors, not chunk IDs
---------------------------
A gold anchor is a short verbatim string (~5-15 words) lifted
character-for-character from the transcript. A retrieved chunk is a HIT when it
contains that string as a substring:

    hit = anchor in chunk["text"]

Exact, case-sensitive, no normalisation. The transcripts mix straight and curly
apostrophes and the anchors are copied from `analysis/benchmark_authoring/corpus_index.json`, whose
sentences are exact source slices -- normalising here would break the match for
one spelling or the other.

This rule is deliberately identical across both chunk sizes. Chunk IDs are not
stable across conditions (chunk 47 at 200 tokens is different text from chunk 47
at 500 tokens), so scoring against IDs would require re-annotating every question
per condition and would make the two chunk-size cells incomparable by
construction.

Metric definitions (SETTLED)
-----------------------------
Both metrics are FRACTIONAL over a question's gold anchors, and both apply
UNIFORMLY to factual, thematic and comparative questions. There are no
per-category special cases: a uniform rule is what makes comparison across
categories defensible.

    anchor_coverage_at_5
        (number of gold anchors matched within the top-5 retrieved chunks)
        / (total gold anchors for that question)
        Ranges 0.0 to 1.0.

    mean_reciprocal_rank_at_5
        For each gold anchor: r = 1-indexed rank of the first top-5 chunk
        containing it; contribution = 1/r if matched, else 0.
        The question's score is the MEAN of contributions across all its anchors.

Both reduce to their standard single-anchor forms. Partial retrieval therefore
earns partial credit but never full credit -- a comparative question retrieving
one of two companies scores approximately 0.5 on both.

This graded approach replaced a strict all-anchors-required rule. The strict
rule would have floored multi-anchor questions at zero across every
condition, eliminating their ability to discriminate between experimental
configurations -- and it was internally inconsistent once coverage became
fractional, since a question could score 0.67 coverage and 0.0 MRR.

Do not change these after any results-producing run has been scored -- it would
silently redefine a reported metric. Mirrored in README.md under "Measures".

Why "anchor coverage" and not "Recall@5"
-----------------------------------------
The name is deliberate. This is NOT textbook Recall@5, which would be binary per
query over a set of relevant documents. It is the fraction of a question's own
gold anchors found within the top 5. Calling it Recall@5 would invite a reader
to assume standard semantics and mis-read the numbers.

Unanswerable questions
----------------------
No anchors, and `reference_answer` is null. EXCLUDED from BOTH the retrieval
metrics AND answer similarity -- dropped from every metric denominator, never
scored as a miss. There is no passage to retrieve, so a zero
would be a phantom retrieval failure that drags down whichever condition
happened to be measured. Both metric functions return None for them, and
`aggregate_retrieval` skips Nones rather than counting them as 0.0. They are
scored only on abstention: an exact match against generate.ABSTENTION.

The same exclusion applies to the answer-similarity metric. An unanswerable
record carries `reference_answer: null`, so calling BERTScore or an embedding
cosine against it would raise rather than score. `is_similarity_scored()` is the
single guard for that path, mirroring `is_retrieval_scored()` for retrieval; the
experiment runner must consult it before scoring similarity. Covered by
tests/test_evaluate.py so it cannot be forgotten when run_experiment.py is built.
"""

import re

from generate import ABSTENTION

# Held constant across every condition of the grid. `retrieve.TOP_K` is the source of
# truth; it is duplicated here rather than imported because importing retrieve
# pulls in faiss and sentence-transformers (~12s) for a module that only does
# arithmetic. tests/test_evaluate.py asserts the two stay equal.
TOP_K = 5

RETRIEVAL_SCORED_CATEGORIES = ("factual", "thematic", "comparative")
UNANSWERABLE_CATEGORY = "unanswerable"


def anchor_strings(question: dict) -> list[str]:
    """The verbatim anchor strings of `question`, whatever shape they arrive in.

    `benchmark/questions.jsonl` stores `gold_anchors` as a plain list of
    strings; the transcript each anchor came from is recorded once per item in
    `transcript_ids`, since the hit rule is a substring test over chunk text and
    needs nothing else. Records of the form `{"transcript_id": ..., "anchor":
    ...}` are also accepted and unwrapped, because that is the shape the
    calibration material uses.

    This is the single place the two shapes meet, so the unwrapping cannot
    drift between the runner and the tests.
    """
    return [a["anchor"] if isinstance(a, dict) else a for a in (question.get("gold_anchors") or [])]


def chunk_matches_anchor(chunk: dict, anchor: str) -> bool:
    """True when `chunk` contains `anchor` verbatim.

    The single definition of a retrieval hit, shared by anchor coverage, MRR and
    the failure-mode tagger so the three can never disagree.
    """
    return anchor in chunk["text"]


def first_match_rank(retrieved_chunks: list[dict], anchor: str, k: int = TOP_K) -> int | None:
    """1-indexed rank of the first chunk in the top-k containing `anchor`.

    None when no chunk within the cutoff contains it. Both metrics are built on
    this, so a change to the cutoff cannot desynchronise them.
    """
    for rank, chunk in enumerate(retrieved_chunks[:k], start=1):
        if chunk_matches_anchor(chunk, anchor):
            return rank
    return None


def anchor_coverage_at_5(
    retrieved_chunks: list[dict], gold_anchors: list[str], k: int = TOP_K
) -> float | None:
    """Fraction of `gold_anchors` matched within the top-k chunks.

    Returns None when there are no anchors (unanswerable), which excludes the
    question from the metric rather than scoring it 0.0.
    """
    if not gold_anchors:
        return None
    matched = sum(1 for anchor in gold_anchors if first_match_rank(retrieved_chunks, anchor, k) is not None)
    return matched / len(gold_anchors)


def mean_reciprocal_rank_at_5(
    retrieved_chunks: list[dict], gold_anchors: list[str], k: int = TOP_K
) -> float | None:
    """Mean of per-anchor reciprocal ranks; unmatched anchors contribute 0.

    Returns None when there are no anchors (unanswerable), for the same reason
    as `anchor_coverage_at_5`.
    """
    if not gold_anchors:
        return None
    total = 0.0
    for anchor in gold_anchors:
        rank = first_match_rank(retrieved_chunks, anchor, k)
        if rank is not None:
            total += 1.0 / rank
    return total / len(gold_anchors)


def is_retrieval_scored(question: dict) -> bool:
    """Whether a question participates in the retrieval metrics at all."""
    return question["category"] != UNANSWERABLE_CATEGORY


def is_similarity_scored(question: dict) -> bool:
    """Whether a question participates in the answer-similarity metric.

    Unanswerable questions carry `reference_answer: null`, so BERTScore or an
    embedding cosine against them would raise rather than produce a number. They
    are scored only on abstention. This is the guard the experiment runner must
    call before the similarity path, exactly as `is_retrieval_scored` guards the
    retrieval path.
    """
    return (
        question["category"] != UNANSWERABLE_CATEGORY
        and question.get("reference_answer") is not None
    )


def score_retrieval(question: dict, retrieved_chunks: list[dict], k: int = TOP_K) -> dict:
    """Both retrieval metrics for one question.

    Unanswerable questions yield None for both. A retrieval-scored question with
    no anchors is an annotation error, not an exclusion, so it raises rather
    than silently vanishing from the denominator.
    """
    anchors = anchor_strings(question)
    if not is_retrieval_scored(question):
        return {"anchor_coverage_at_5": None, "mean_reciprocal_rank_at_5": None}
    if not anchors:
        raise ValueError(
            f"question {question.get('id')!r} is category {question['category']!r} "
            "but has no gold_anchors; only unanswerable questions may omit them"
        )
    return {
        "anchor_coverage_at_5": anchor_coverage_at_5(retrieved_chunks, anchors, k),
        "mean_reciprocal_rank_at_5": mean_reciprocal_rank_at_5(retrieved_chunks, anchors, k),
    }


def aggregate_retrieval(scores: list[dict]) -> dict:
    """Mean each metric over the questions that carry it.

    Nones are skipped, not counted as zero -- this is where the exclusion of
    unanswerable questions from the denominator actually happens.
    """
    aggregate: dict[str, float | int | None] = {}
    for metric in ("anchor_coverage_at_5", "mean_reciprocal_rank_at_5"):
        values = [s[metric] for s in scores if s.get(metric) is not None]
        aggregate[metric] = sum(values) / len(values) if values else None
        aggregate[f"{metric}_n_scored"] = len(values)
    aggregate["n_questions"] = len(scores)
    aggregate["n_excluded"] = len(scores) - aggregate["anchor_coverage_at_5_n_scored"]
    return aggregate


def abstained(answer: str) -> bool:
    """Exact match against the canonical abstention sentence.

    Deliberately exact: loosening it would change the metric definition for the
    unanswerable category mid-experiment. The local model backend is not guaranteed to reproduce
    the sentence verbatim; see README.md, "Scorer fixes and known defects".
    """
    return answer == ABSTENTION


def answer_similarity(answer: str, reference_answer: str) -> float:
    """Cosine similarity between `answer` and `reference_answer` embeddings.

    The design leaves the answer-quality metric as "cosine over embeddings, or
    BERTScore". This implements the cosine option, over the same
    `bge-small-en-v1.5` model the dense retriever already uses. The choice is
    deliberate and worth stating in the thesis: BERTScore would add a second
    model to pin, a second download, and a second set of version-sensitive
    numbers, for a metric that only has to rank answers against a fixed
    reference. Held constant across every condition either way -- it is a
    dependent variable, not a manipulated one.

    NO query prefix is applied to either side. BGE's instruction prefix marks
    the asymmetric query->passage direction; an answer against a reference
    answer is a symmetric comparison of two texts of the same kind, so
    prefixing one and not the other would tilt the embedding space for no
    reason.

    `index` is imported lazily: it pulls in faiss and sentence-transformers
    (~12s), and the rest of this module is pure arithmetic that must stay
    importable without them.

    Swap point: if BERTScore is ever adopted, replace this function body. Every
    caller goes through here, and `is_similarity_scored` stays the guard.
    """
    from index import get_embedding_model

    model = get_embedding_model()
    vectors = model.encode([answer, reference_answer], normalize_embeddings=True, convert_to_numpy=True)
    return float(vectors[0] @ vectors[1])


CASE_A = "A"  # unanswerable -- no gold anchors exist anywhere in the corpus
CASE_B = "B"  # answerable, but anchor_coverage_at_5 == 0 -- gold anchor absent from top-5
CASE_C = "C"  # answerable, anchor_coverage_at_5 > 0 -- at least one gold anchor in top-5

OUTCOME_ABSTAINED = "abstained"
OUTCOME_GROUNDED_CORRECT = "answered_grounded_correct"
OUTCOME_GROUNDED_OFFTARGET = "answered_grounded_offtarget"
OUTCOME_UNGROUNDED = "answered_ungrounded"


def classify_case(question: dict, coverage_at_5: float | None) -> str:
    """Case A/B/C per Stage 2's ground-truth partition (settled).

    Mechanical, from data already computed by `score_retrieval` -- no re-running
    retrieval, no re-matching anchors. `coverage_at_5` is that question's
    `anchor_coverage_at_5` (None for Case A, where the question is unanswerable
    and was never retrieval-scored in the first place).

        Case A: question["category"] == "unanswerable" (coverage_at_5 is None)
        Case B: coverage_at_5 == 0   -- gold anchor exists, retrieval missed it
        Case C: coverage_at_5 > 0    -- at least one gold anchor surfaced

    Correct behaviour by case: A -> abstain, B -> abstain (a confident answer
    is scored as ungrounded-or-offtarget by `classify_outcome`, never as
    "correct"), C -> answer, grounded in what was actually retrieved.
    """
    if not is_retrieval_scored(question):
        return CASE_A
    return CASE_B if coverage_at_5 == 0 else CASE_C


# Fix 1 (2026-09-03, traced in analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md Check 2): a comma
# is only a thousands separator when it groups exactly 3 digits at a time
# ("1,500", "1,234,567"). The old pattern `\d[\d,]*` treated ANY comma right
# after a digit run as separator-or-more, so "2023," (ordinary sentence
# punctuation) was captured as the literal claim "2023," -- a string unlikely
# to recur verbatim by chance, making support depend on punctuation rather
# than on the number itself. This alternation tries the strict comma-grouped
# form first (>=1 group of exactly ",ddd"), and only falls back to a bare
# digit run (no commas at all) when that fails -- so "2023," matches "2023"
# alone, "$1,500" still matches "1,500" whole, and "1,5" matches "1" and "5"
# separately rather than being glued by a comma that isn't a real separator.
_NUMBER_RE = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")
_WORD_RE = re.compile(r"\w+")
_NGRAM_FALLBACK_N = 6

# Fix 2 (2026-09-03, traced in analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md Check 2): a bare
# year or bare quarter-integer that the ANSWER merely echoes back from the
# QUESTION's own phrasing is not a claim worth verifying -- checking it just
# makes the outcome depend on whether some unrelated retrieved chunk happens
# to also spell out that same incidental digit (ref_fact_05's "2024" flip).
# This mirrors benchmark/benchmark_process.md's Rule 13 ("The question
# licence"): "The question is part of the item; a term the question supplies
# is not imported evidence." Applied here to numbers instead of metric terms:
# a number the question already supplies is not evidence the answer needs to
# import from a retrieved chunk. Deliberately narrow -- see `is_trivial_claim`.
_TRIVIAL_QUARTER_INTEGERS = {"1", "2", "3", "4"}
_TRIVIAL_YEAR_RANGE = range(2000, 2031)


def transcript_id_from_chunk_id(chunk_id: str) -> str:
    """Recover the transcript_id embedded in a chunk_id.

    chunking.py's chunk_id format is
    f"{transcript_id}_{section}_{chunk_size}_{chunk_index:03d}". transcript_id
    itself contains underscores (e.g. "AXP_2023_Q4"), so a naive split on "_"
    is ambiguous -- but `section` is always exactly one of preprocess.py's two
    constants, "prepared_remarks" or "qa" (SECTION_PREPARED / SECTION_QA), so
    splitting on the first occurrence of either marker is unambiguous.
    """
    for marker in ("_prepared_remarks_", "_qa_"):
        if marker in chunk_id:
            return chunk_id.split(marker)[0]
    raise ValueError(f"chunk_id {chunk_id!r} does not contain a recognised section marker")


def extract_numeric_claims(text: str) -> list[str]:
    """Every digit-sequence substring in `text` (proper thousands-grouped
    commas kept as part of the claim; sentence-punctuation commas are not --
    see the `_NUMBER_RE` comment above, Fix 1). No unit parsing. The primary
    grounding signal: this corpus is financial-figures dense, so a fabricated
    number is the highest-value thing to catch automatically, and a literal
    substring match is unambiguous to verify.

    Known limitation, stated plainly rather than hidden: this is verbatim
    matching, not semantic. "$1,900 million" in an answer will NOT match
    "$1.9 billion" in the context even if they mean the same thing -- a
    reformatted-but-correct number reads as unsupported. That is a
    conservative bias (more likely to flag ungrounded than to miss a real
    fabrication), and is exactly why this mechanical check does not replace
    the manual faithfulness check on a subset, done by the researcher -- it is a coarser, fully automatic proxy for the same question.
    """
    return _NUMBER_RE.findall(text)


def is_trivial_claim(claim: str) -> bool:
    """True only for a bare quarter-integer ("1".."4") or a bare 4-digit year
    in 2000-2030 -- see Fix 2 above. Deliberately narrow: a comma-grouped
    number ("2,024") is never trivial regardless of its digits, since Fix 1
    already keeps a real thousands-grouped figure distinct from a bare year;
    this is what makes "$2,024 million" verified rather than excluded even
    though "2024" might appear in the question. Nothing else is ever trivial
    -- a substantive figure that isn't a bare year/quarter integer is always
    checked, no matter how it looks.
    """
    return claim in _TRIVIAL_QUARTER_INTEGERS or (claim.isdigit() and len(claim) == 4 and int(claim) in _TRIVIAL_YEAR_RANGE)


def filter_question_echoed_trivial_claims(claims: list[str], question_text: str) -> list[str]:
    """Drop a claim only when it is BOTH trivial (`is_trivial_claim`) AND
    literally present among the question's own numeric claims -- Fix 2,
    applying Rule 13's "the question is part of the item" principle to
    numbers. A trivial-looking claim NOT echoed by the question (the model
    introduced that year/quarter number on its own) is still verified in
    full; only the intersection of trivial-and-echoed is ever dropped.
    """
    echoed = set(extract_numeric_claims(question_text))
    return [c for c in claims if not (is_trivial_claim(c) and c in echoed)]


def _shared_ngram_chunk_ids(answer: str, retrieved_chunks: list[dict], n: int = _NGRAM_FALLBACK_N) -> set[str]:
    """chunk_ids sharing at least one n-word verbatim (case-insensitive) run
    with `answer`. Fallback grounding signal for answers with no numeric
    claims at all (rare in this domain, but a qualitative/narrative answer
    should not default to "ungrounded" for lack of a number to check)."""
    words = _WORD_RE.findall(answer.lower())
    if len(words) < n:
        return set()
    windows = {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}
    matches = set()
    for chunk in retrieved_chunks:
        chunk_joined = " ".join(_WORD_RE.findall(chunk["text"].lower()))
        if any(w in chunk_joined for w in windows):
            matches.add(chunk["chunk_id"])
    return matches


def contains_abstention_sentence(text: str) -> bool:
    """Fix 3 (2026-09-03, traced in analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md Check 1's
    ref_comp_01 case): True when the exact canonical ABSTENTION sentence
    appears anywhere in `text` as a complete sentence -- not only when
    `text == ABSTENTION` (that exact-equality check is `abstained()`, kept
    unchanged as its own strict diagnostic). A model can decline in a
    preamble and still close with the verbatim canonical sentence; exact
    equality misses that entirely and the record falls through to the
    numeric-claim classifier, which then scores it on whatever incidental
    digits happen to be in the preamble.

    Deliberately mechanical and strict, per instruction: the canonical
    sentence must be present byte-for-byte (every occurrence is checked, not
    just the first), bounded on both sides by a non-alphanumeric character or
    the start/end of the string so it can't match as a fragment glued inside
    a different sentence or word. No fuzzy or semantic matching, and no
    attempt to recognise a decline phrased entirely in the model's own words
    -- that would be a judgement call, which this function must not make.
    """
    start = 0
    while True:
        idx = text.find(ABSTENTION, start)
        if idx == -1:
            return False
        before_ok = idx == 0 or not text[idx - 1].isalnum()
        end = idx + len(ABSTENTION)
        after_ok = end == len(text) or not text[end].isalnum()
        if before_ok and after_ok:
            return True
        start = idx + 1


def classify_outcome(answer: str, question: dict, retrieved_chunks: list[dict]) -> dict:
    """The four-way outcome (settled): abstained /
    answered_grounded_correct / answered_grounded_offtarget / answered_ungrounded.

    Abstention detection is `contains_abstention_sentence` (Fix 3), not exact
    equality -- a response can decline in its own words and still close with
    the verbatim canonical sentence. Claims are filtered through
    `filter_question_echoed_trivial_claims` (Fix 2) before verification, so a
    bare year/quarter-integer the answer only echoes from the question is not
    checked. Both are dated, traced fixes (analysis/qwen3.8-27b_q4_k_xl/stage2_diagnostics.md);
    see their own docstrings for the reasoning, not repeated here.

    "Grounded" means every (post-filter) numeric claim in the answer appears
    verbatim in the retrieved chunk text (see `extract_numeric_claims`'s docstring for
    what that does and doesn't catch); an answer with no numeric claims falls
    back to a shared-6-word-run check (`_shared_ngram_chunk_ids`) instead of
    defaulting to either outcome for lack of a number.

    "On-target" (-> _correct) vs "off-target" means: does at least one of the
    chunks that actually supported the answer's claims belong to one of the
    question's own `transcript_ids`? This is the ref_them_01/ref_them_02
    pattern from the development runs: the answer can be fully grounded in
    real retrieved text and still be about the wrong company/quarter, because
    coverage@5==0 only says the GOLD anchor didn't surface -- it says nothing
    about whether some OTHER chunk from the right transcript did.

    Expected shape, not enforced by this function (report, don't assert):
    answered_grounded_correct is IMPOSSIBLE for Case A (unanswerable
    questions carry `transcript_ids: []`, so the on-target intersection is
    always empty) and expected NEAR-EMPTY for Case B (coverage@5==0 means the
    specific gold sentence didn't surface, but the right transcript
    occasionally still does via a different chunk -- rare, not impossible).

    For a partial-context multi-anchor question (some anchors in top-5, some
    not), "correct" falls out of this same rule with no special-casing: if
    the answer only claims what the present chunks support (on-target chunk
    included) and invents nothing for the missing side, every claim traces
    and the on-target check passes -- exactly "correct as far as context
    supports, no fabrication for the missing part."
    """
    if contains_abstention_sentence(answer):
        return {"outcome": OUTCOME_ABSTAINED, "supporting_chunk_ids": [], "unsupported_claims": [], "grounding_basis": None}

    claims = extract_numeric_claims(answer)
    claims = filter_question_echoed_trivial_claims(claims, question["question"])
    if claims:
        supporting_chunk_ids: set[str] = set()
        unsupported_claims = []
        for claim in claims:
            hit = False
            for chunk in retrieved_chunks:
                if claim in chunk["text"]:
                    supporting_chunk_ids.add(chunk["chunk_id"])
                    hit = True
            if not hit:
                unsupported_claims.append(claim)
        grounding_basis = "numeric"
    else:
        supporting_chunk_ids = _shared_ngram_chunk_ids(answer, retrieved_chunks)
        unsupported_claims = []
        grounding_basis = "ngram_fallback (answer has no numeric claims)"
        if not supporting_chunk_ids:
            return {
                "outcome": OUTCOME_UNGROUNDED,
                "supporting_chunk_ids": [],
                "unsupported_claims": [],
                "grounding_basis": grounding_basis,
            }

    if unsupported_claims:
        return {
            "outcome": OUTCOME_UNGROUNDED,
            "supporting_chunk_ids": sorted(supporting_chunk_ids),
            "unsupported_claims": unsupported_claims,
            "grounding_basis": grounding_basis,
        }

    target_transcripts = set(question.get("transcript_ids") or [])
    supporting_transcripts = {transcript_id_from_chunk_id(cid) for cid in supporting_chunk_ids}
    on_target = bool(supporting_transcripts & target_transcripts)

    return {
        "outcome": OUTCOME_GROUNDED_CORRECT if on_target else OUTCOME_GROUNDED_OFFTARGET,
        "supporting_chunk_ids": sorted(supporting_chunk_ids),
        "unsupported_claims": [],
        "grounding_basis": grounding_basis,
    }


def is_bertscore_scored(question: dict, case: str, outcome: str) -> bool:
    """Whether a record participates in the descriptive BERTScore/cosine
    answer-similarity check (settled): Case C items that were
    actually answered (not abstained), and only those.

    Not a primary metric -- inapplicable to Case A/B by construction (an
    off-target or ungrounded answer scored against the intended reference
    answer would measure something confounded, not answer quality), and n is
    too small where it does apply to lean on statistically. Descriptive only.
    Mirrors `is_retrieval_scored` / `is_similarity_scored` as the single guard
    for this path.
    """
    return (
        case == CASE_C
        and outcome != OUTCOME_ABSTAINED
        and is_similarity_scored(question)
    )


def classify_case_outcome(question: dict, coverage_at_5: float | None, answer: str, retrieved_chunks: list[dict]) -> dict:
    """The single entry point Stage 2 should call: case + outcome + the
    supporting detail, in one record. `classify_case` and `classify_outcome`
    stay separately callable (and separately tested) because case depends
    only on Stage 1's persisted retrieval metrics while outcome depends on
    the generated answer -- keeping them apart means a generation re-run
    never has to re-derive the case.
    """
    case = classify_case(question, coverage_at_5)
    outcome = classify_outcome(answer, question, retrieved_chunks)
    return {"case": case, **outcome}


def aggregate_case_outcomes(records: list[dict]) -> dict[str, dict[str, int]]:
    """case -> outcome -> count, over a condition's records. Report broken out
    by case, not pooled -- pooling would average away exactly the
    distinction (Case A/B/C have different achievable outcomes) this taxonomy
    exists to preserve.
    """
    counts: dict[str, dict[str, int]] = {}
    for r in records:
        by_case = counts.setdefault(r["case"], {})
        by_case[r["outcome"]] = by_case.get(r["outcome"], 0) + 1
    return counts
