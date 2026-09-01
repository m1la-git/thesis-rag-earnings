"""Generate verified REFERENCE candidate questions grounded in the frozen corpus.

NOT the benchmark. `benchmark/questions.jsonl` is authored by the researcher;
this file produces `analysis/benchmark_authoring/reference_candidates.{md,json}` as reference
material for calibration only. Nothing here is a gold label.

How anchors stay exact
----------------------
Anchors are never written by hand. Each candidate names a sentence by
(transcript_id, turn_index, sentence_char_start) -- all integers copied from
the corpus index -- plus a word range inside it. The anchor is then SLICED from
the source text by character offset, so it is exact by construction and cannot
drift by a smart quote, a collapsed space or a stray edit.

Every anchor is then verified against four conditions before anything is
written, and a candidate failing any of them is dropped rather than patched:

  1. the anchor occurs verbatim in the stated transcript's raw `content`
  2. it lies inside a single chunk under BOTH the 200- and 500-token configs,
     using the same whitespace-stripped section search as anchor_candidates.py
     (never a head/tail probe)
  3. it is at least MIN_EDGE_MARGIN_WORDS words clear of both ends of its
     source sentence, so it keeps headroom away from chunk edges
  4. its document frequency across all 128 transcripts is computed and reported,
     so an anchor that could match elsewhere is visible rather than hidden

Run `python scripts/reference_candidates.py --verify-only` to re-check every
candidate without rewriting the outputs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from build_corpus_index import (  # noqa: E402
    build_chunk_locator,
    detect_analysts,
    load_corpus,
    locate_chunks,
    split_sentence_spans,
)
from chunking import chunk_transcript  # noqa: E402
from preprocess import SECTION_PREPARED, SECTION_QA, preprocess_transcript  # noqa: E402

OUTPUT_DIR = REPO_ROOT / "analysis" / "benchmark_authoring"
CHUNK_SIZES = (200, 500)

# Mirrors evaluate.UNANSWERABLE_CATEGORY; imported there rather than here because
# evaluate imports generate, which loads .env and prints its backend on import.
UNANSWERABLE_CATEGORY = "unanswerable"

MIN_ANCHOR_WORDS = 5

# Conversational sentences trail off on prepositions far more than reporting
# prose, so Rule 3 rejected Q&A anchors disproportionately and the Q&A share
# collapsed. A longer ceiling lets a complete clause fit before a trailing
# preposition. Containment, edge margin and document frequency are unchanged.
MAX_ANCHOR_WORDS_BY_SECTION = {SECTION_PREPARED: 15, SECTION_QA: 20}
MIN_EDGE_MARGIN_WORDS = 2

# Rule 3. An anchor must read as a self-contained phrase, not a fragment cut
# mid-clause. The two edges need different rules.
#
# TAIL is strict: anything that grammatically requires a following word strands
# the text that completes it. "...increased by" loses the figure; "...lower than"
# loses the comparison; "...reflecting the goodwill associated with our" loses the
# noun. Determiners, pronouns and particles all fail here.
ANCHOR_TAIL_STOP = set("""
by and of to not the a an or but nor so as at on in for with from into over under
than that this these those which who whom whose when while if because
is are was were be been being am has have had do does did
will would can could may might must shall should
we our us you your they their it its he she his her my me
about after before during through between against above below up down out off
""".split())

# HEAD is narrower -- only where it genuinely produces an incomplete phrase. A
# determiner, possessive or particle opens a perfectly good phrase ("the credit
# card net charge-off rate rose...", "over $30 billion in net inflows"), so those
# are allowed. A preposition, conjunction, relative or bare auxiliary does not
# ("were $638 million, benefiting from...", "on deposits moved from...").
ANCHOR_HEAD_STOP = set("""
by and of to not or but nor so as at on in for with from into under than
that which who whom whose when while if because
is are was were be been being am has have had do does did
will would can could may might must shall should
""".split())

_WORD_RE = re.compile(r"\S+")


# ---------------------------------------------------------------------------
# Corpus access
# ---------------------------------------------------------------------------


class Corpus:
    """Sentence-level view of the frozen corpus with chunk containment."""

    def __init__(self) -> None:
        frame = load_corpus()
        self.rows = {row["transcript_id"]: row for _, row in frame.iterrows()}
        self.content = {tid: row["content"] for tid, row in self.rows.items()}
        self._records: dict[str, list[dict]] = {}
        self._locators: dict[str, dict] = {}
        self._analysts: dict[str, dict] = {}

    def records(self, transcript_id: str) -> list[dict]:
        if transcript_id not in self._records:
            if transcript_id not in self.rows:
                raise KeyError(f"unknown transcript_id: {transcript_id!r}")
            self._records[transcript_id] = preprocess_transcript(self.rows[transcript_id])
        return self._records[transcript_id]

    def locators(self, transcript_id: str) -> dict:
        if transcript_id not in self._locators:
            locators = {}
            for size in CHUNK_SIZES:
                chunks = chunk_transcript(self.records(transcript_id), size)
                for section in (SECTION_PREPARED, SECTION_QA):
                    in_section = [c for c in chunks if c["section"] == section]
                    locators[(size, section)] = build_chunk_locator(in_section)
            self._locators[transcript_id] = locators
        return self._locators[transcript_id]

    def sentence(self, transcript_id: str, turn_index: int, char_start: int) -> dict:
        """The sentence starting at `char_start` inside the given turn."""
        record = self.records(transcript_id)[turn_index]
        for start, end in split_sentence_spans(record["text"]):
            if start == char_start:
                return {
                    "text": record["text"][start:end],
                    "char_start": start,
                    "char_end": end,
                    "section": record["section"],
                    "speaker": record["speaker"],
                    "turn_index": turn_index,
                }
        raise ValueError(
            f"{transcript_id} turn {turn_index}: no sentence starts at char {char_start}"
        )

    def speaker_role(self, transcript_id: str, speaker: str) -> str:
        """"management" or "analyst" for a speaker on a given call.

        Reuses build_corpus_index.detect_analysts, which identifies analysts from
        the operator's own announcements ("our next question comes from X with Y")
        rather than guessing from the speaker list. Anyone not so announced --
        executives, and the operator -- counts as management-side for attribution.
        """
        if transcript_id not in self._analysts:
            self._analysts[transcript_id] = detect_analysts(self.records(transcript_id))
        return "analyst" if speaker in self._analysts[transcript_id] else "management"

    def document_frequency(self, anchor: str) -> int:
        """How many of the 128 transcripts contain this exact string."""
        return sum(1 for text in self.content.values() if anchor in text)

    def iter_sentences(self, transcript_id: str):
        """Every sentence in a transcript, with its identifiers."""
        for record in self.records(transcript_id):
            for start, end in split_sentence_spans(record["text"]):
                yield {
                    "transcript_id": transcript_id,
                    "turn_index": record["turn_index"],
                    "char_start": start,
                    "char_end": end,
                    "section": record["section"],
                    "speaker": record["speaker"],
                    "text": record["text"][start:end],
                }


# ---------------------------------------------------------------------------
# Anchor slicing and verification
# ---------------------------------------------------------------------------


def slice_anchor(sentence_text: str, word_start: int, word_end: int) -> tuple[str, int]:
    """Character-exact slice of words [word_start, word_end] inclusive.

    Returns (anchor, offset_within_sentence). Slicing rather than transcribing is
    what makes the anchor verbatim by construction.
    """
    words = list(_WORD_RE.finditer(sentence_text))
    if not 0 <= word_start <= word_end < len(words):
        raise ValueError(
            f"word range ({word_start}, {word_end}) out of bounds for {len(words)} words"
        )
    start, end = words[word_start].start(), words[word_end].end()
    return sentence_text[start:end], start


def verify_anchor(corpus: Corpus, spec: dict) -> tuple[dict | None, list[str]]:
    """Build one anchor's provenance, or explain why it must be dropped."""
    problems: list[str] = []
    transcript_id = spec["transcript_id"]

    try:
        sentence = corpus.sentence(transcript_id, spec["turn_index"], spec["sentence_char_start"])
    except (KeyError, ValueError) as exc:
        return None, [str(exc)]

    try:
        anchor, offset = slice_anchor(sentence["text"], *spec["words"])
    except ValueError as exc:
        return None, [f"{transcript_id}: {exc}"]

    n_words = len(_WORD_RE.findall(sentence["text"]))
    anchor_words = spec["words"][1] - spec["words"][0] + 1

    # (1) verbatim in the stated transcript
    if anchor not in corpus.content[transcript_id]:
        problems.append(f"{transcript_id}: anchor not found verbatim in transcript content")

    # (2) contained in a single chunk under both configs
    located = locate_chunks(anchor, corpus.locators(transcript_id), sentence["section"])
    chunk_ids = {size: located.get(f"chunk_ids@{size}", []) for size in CHUNK_SIZES}
    for size in CHUNK_SIZES:
        if len(chunk_ids[size]) != 1:
            problems.append(
                f"{transcript_id}: anchor spans {len(chunk_ids[size])} chunks at {size} tokens "
                "(must be exactly 1)"
            )

    # (3) clear of both sentence edges
    if spec["words"][0] < MIN_EDGE_MARGIN_WORDS:
        problems.append(
            f"{transcript_id}: anchor starts at word {spec['words'][0]}, "
            f"needs >= {MIN_EDGE_MARGIN_WORDS} words of margin"
        )
    if spec["words"][1] > n_words - 1 - MIN_EDGE_MARGIN_WORDS:
        problems.append(
            f"{transcript_id}: anchor ends at word {spec['words'][1]} of {n_words - 1}, "
            f"needs >= {MIN_EDGE_MARGIN_WORDS} words of margin"
        )

    # (Rule 3) neither edge may be a syntactic fragment
    anchor_tokens = _WORD_RE.findall(anchor)
    for position, token, stoplist in (
        ("starts", anchor_tokens[0], ANCHOR_HEAD_STOP),
        ("ends", anchor_tokens[-1], ANCHOR_TAIL_STOP),
    ):
        bare = token.strip(".,;:!?\"'()[]").lower()
        if bare in stoplist:
            problems.append(
                f"{transcript_id}: anchor {position} on {bare!r} (Rule 3: fragment edge)"
            )

    # length band -- wider for Q&A, see MAX_ANCHOR_WORDS_BY_SECTION
    max_words = MAX_ANCHOR_WORDS_BY_SECTION[sentence["section"]]
    if not MIN_ANCHOR_WORDS <= anchor_words <= max_words:
        problems.append(
            f"{transcript_id}: anchor is {anchor_words} words, "
            f"outside {MIN_ANCHOR_WORDS}-{max_words} for section {sentence['section']}"
        )

    # (4) document frequency, reported not enforced
    doc_frequency = corpus.document_frequency(anchor)

    # Chunk-size sensitivity. Retrieval matches whole chunks, not anchors, so
    # where the anchor boundary falls does not change what is findable. What DOES
    # is whether the anchor's surrounding sentence -- the context a query would
    # match on -- survives intact in one chunk. When the sentence is split at 200
    # tokens but whole at 500, the evidence and the words identifying it are
    # separately retrievable under one condition and jointly retrievable under the
    # other. Those candidates probe the chunk-size variable directly.
    sentence_chunks = locate_chunks(sentence["text"], corpus.locators(transcript_id), sentence["section"])
    sentence_span = {size: len(sentence_chunks.get(f"chunk_ids@{size}", [])) for size in CHUNK_SIZES}
    chunk_size_sensitive = sentence_span[200] > 1 and sentence_span[500] == 1

    provenance = {
        "anchor": anchor,
        "source_sentence": sentence["text"],
        "section": sentence["section"],
        "speaker": sentence["speaker"],
        "speaker_role": corpus.speaker_role(transcript_id, sentence["speaker"]),
        "turn_index": sentence["turn_index"],
        "anchor_char_offset_in_sentence": offset,
        "sentence_char_start": sentence["char_start"],
        "sentence_char_end": sentence["char_end"],
        "anchor_words": anchor_words,
        "sentence_words": n_words,
        "chunk_ids_200": chunk_ids[200],
        "chunk_ids_500": chunk_ids[500],
        "doc_frequency": doc_frequency,
        "transcript_id": transcript_id,
        "sentence_chunks_200": sentence_span[200],
        "sentence_chunks_500": sentence_span[500],
        "chunk_size_sensitive": chunk_size_sensitive,
    }
    return provenance, problems


# Framing verbs and company references a reference answer may use without them
# appearing in an anchor: they attribute the claim rather than assert new content.
ANSWER_FRAMING_ALLOWED = set("""
said says reported report described describe describes noted notes stated states
was were is are had has have been being be its it the a an and or but of to in for
with on at from that this these those which while whereas compared than as by
bank banks bancorp mellon express financial group corporation inc co company firm
blackrock jpmorgan morgan stanley citi citigroup goldman sachs wells fargo capital
one america pnc huntington fifth third state street york m&t us u.s bny bank's
quarter quarters year years first second third fourth half prior previous
million billion trillion basis points percent per share
its their his her they he she we our
expected expects expect guided guide guidance call calls
america's one's pnc's third's mellon's citi's jpmorgan's m&t's sachs's huntington's
bancorp's blackrock's stanley's fargo's bank's york's
booked recorded posted grew achieved generated came included reduced repeated
projected projects took saw ended stood reached later subsequently while and
"""
.split())

_CONTENT_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'&/.-]*")


def answer_support_warnings(candidate: dict) -> list[str]:
    """(Rule 2) Content words in the reference answer absent from every anchor.

    A heuristic flag for manual review, not a hard failure: an answer legitimately
    uses framing verbs and company names that no anchor contains. Anything else it
    asserts should be traceable to anchor text, so what surfaces here is either an
    attribution word to add to the allowlist or a genuine unsupported claim.
    """
    anchors = " ".join(p["anchor"] for p in candidate["provenance"]).lower()
    unsupported = []
    for word in _CONTENT_WORD_RE.findall(candidate["reference_answer"]):
        bare = word.strip(".,;:'\"").lower()
        if len(bare) < 3 or bare in ANSWER_FRAMING_ALLOWED:
            continue
        if bare not in anchors:
            unsupported.append(bare)
    return sorted(set(unsupported))


_ORDINAL_QUARTER = {"first": 1, "second": 2, "third": 3, "fourth": 4}
_Q_OF_YEAR = re.compile(r"(first|second|third|fourth)\s+quarter\s+of\s+(20\d{2})", re.I)
_Q_SHORT = re.compile(r"\bQ([1-4])\s*(20\d{2})\b", re.I)
_HALF_OF_YEAR = re.compile(r"(first|second)\s+half\s+of\s+(20\d{2})", re.I)
_BARE_YEAR = re.compile(r"\b(20\d{2})\b")


def question_period(question: str) -> tuple[set[tuple[int, int]] | None, set[int]]:
    """Fiscal periods a question commits to: (quarters, years).

    Returns (None, set()) when the question names no period at all, which is the
    correct shape for a thematic question and imposes no constraint.
    """
    quarters: set[tuple[int, int]] = set()
    for text, year in _Q_OF_YEAR.findall(question):
        quarters.add((int(year), _ORDINAL_QUARTER[text.lower()]))
    for quarter, year in _Q_SHORT.findall(question):
        quarters.add((int(year), int(quarter)))
    for half, year in _HALF_OF_YEAR.findall(question):
        quarters.update({(int(year), q) for q in ((1, 2) if half.lower() == "first" else (3, 4))})
    years = {int(y) for y in _BARE_YEAR.findall(question)}
    if quarters:
        # A question may name a quarter for one bank and a year for another; an
        # anchor satisfies the question if it matches EITHER, so both are returned
        # rather than letting a quarter phrase mask the years around it.
        return quarters, years
    return None, years


def check_period(spec: dict, provenances: list[dict]) -> list[str]:
    """(Rule 7) Every anchor must fall inside the period the question names."""
    quarters, years = question_period(spec["question"])
    problems = []
    for p in provenances:
        ticker, year, quarter = p["transcript_id"].split("_")
        year, quarter = int(year), int(quarter.lstrip("Q"))
        if quarters is not None and (year, quarter) not in quarters and year not in years:
            problems.append(
                f"[{spec['id']}] {p['transcript_id']} is outside the period the question names "
                f"({sorted(quarters)}) (Rule 7: reword the question period-neutrally or to the real span)"
            )
        elif quarters is None and years and year not in years:
            problems.append(
                f"[{spec['id']}] {p['transcript_id']} is outside the year(s) the question names "
                f"({sorted(years)}) (Rule 7)"
            )
    return problems


# Rule 10. A two-word reference answer makes semantic-similarity scoring
# meaningless -- a bare figure produces near-arbitrary BERTScore against any
# generated answer. Every reference answer must be a complete sentence naming the
# entity, the metric and the value.
MIN_ANSWER_WORDS = 10

# Rule 10 needs to know a company when it sees one. Short forms as they appear in
# questions and answers, not the legal names in the parquet.
COMPANY_ALIASES = {
    "AXP": ("American Express",), "BAC": ("Bank of America",),
    "BK": ("BNY Mellon", "BNY"), "BLK": ("BlackRock",),
    "C": ("Citigroup", "Citi"), "COF": ("Capital One",),
    "FITB": ("Fifth Third",), "GS": ("Goldman Sachs", "Goldman"),
    "HBAN": ("Huntington",), "JPM": ("JPMorgan", "JPMorgan Chase"),
    "MS": ("Morgan Stanley",), "MTB": ("M&T",), "PNC": ("PNC",),
    "STT": ("State Street",), "USB": ("U.S. Bancorp", "US Bancorp"),
    "WFC": ("Wells Fargo",),
}
_ALL_ALIASES = tuple(a for forms in COMPANY_ALIASES.values() for a in forms)

# Words that carry no metric meaning, so sharing them with the question does not
# show the answer names what was asked about.
_METRIC_STOP = set("""
bank banks firm firms company companies quarter quarters year years half
what how much many did does said say report reported describe described
their there this that with from into over under about during across between
each other were was have has been being they them the and for its
""".split())

# Rule 11. Light nouns that signal a clause was carried over from an anchor that
# ended mid-phrase: "driven by lower net interest revenue and changes" prompts
# "changes to what?" because the qualifier sat outside the anchor.
DANGLING_TAIL_NOUNS = set("""
changes change items factors things others ones adjustments impacts effects
matters areas aspects elements parts pieces
""".split())

_ANSWER_ASKS_VALUE = re.compile(r"how much|how large|how fast|what were|what was|what level|levels|"
                                r"what share|what proportion|what range|how did .* compare", re.I)


def check_answer(spec: dict, provenances: list[dict]) -> list[str]:
    """(Rule 8) The answer must be grammatically complete and actually answer.

    Rule 3 cleans the anchor edge; without this the fragmentation simply moves
    downstream into the answer, which then trails off mid-clause.
    """
    problems = []
    answer = spec["reference_answer"].strip()
    for clause in [c for c in re.split(r"[;.]", answer) if c.strip()]:
        last = _WORD_RE.findall(clause)[-1].strip(".,;:!?\"'()[]").lower()
        if last in ANCHOR_TAIL_STOP:
            problems.append(
                f"[{spec['id']}] reference answer clause ends on {last!r}: "
                f"...{clause.strip()[-60:]!r} (Rule 8: incomplete clause)"
            )
    if _ANSWER_ASKS_VALUE.search(spec["question"]):
        clauses = [c for c in re.split(r";", answer) if c.strip()]
        for clause in clauses:
            if not re.search(r"\d", clause):
                problems.append(
                    f"[{spec['id']}] the question asks for values but this clause carries none: "
                    f"{clause.strip()[:70]!r} (Rule 8: answer does not answer the question)"
                )
    return problems


def check_answer_quality(spec: dict, provenances: list[dict]) -> list[str]:
    """(Rules 10 and 11) The answer must be substantial and read as prose.

    Rule 11 is fundamentally a read-aloud judgement; what is automatable is the
    dangling-fragment case, where a clause ends on a light noun whose qualifier
    fell outside the anchor.
    """
    problems = []
    answer = spec["reference_answer"].strip()
    words = _WORD_RE.findall(answer)

    if len(words) < MIN_ANSWER_WORDS:
        problems.append(
            f"[{spec['id']}] reference answer is {len(words)} words ({answer!r}); "
            f"Rule 10 requires at least {MIN_ANSWER_WORDS} -- name the entity, the metric "
            "and the value, not a bare figure"
        )
    # (a) the answer must name a company
    if not any(alias.lower() in answer.lower() for alias in _ALL_ALIASES):
        problems.append(
            f"[{spec['id']}] reference answer names no company (Rule 10): {answer[:70]!r} -- "
            "an answer opening on a bare pronoun cannot stand alone"
        )
    # (b) it must name the period, which the question is required to state
    if not _BARE_YEAR.search(answer):
        problems.append(
            f"[{spec['id']}] reference answer names no period (Rule 10): {answer[:70]!r}"
        )
    # (c) it must name the metric -- shown by sharing a substantive word with the
    # question that is neither a company name nor a date
    q_words = {
        w.lower().strip(".,;:?'\"") for w in _WORD_RE.findall(spec["question"])
    }
    a_words = {
        w.lower().strip(".,;:?'\"") for w in _WORD_RE.findall(answer)
    }
    def _metric_terms(words):
        return {
            w[:5] for w in words
            if len(w) >= 4 and w not in _METRIC_STOP and not re.fullmatch(r"20\d\d", w)
            and not any(w in alias.lower() for alias in _ALL_ALIASES)
        }

    # compare on a 5-character stem so "expense"/"expenses" and "margin"/"margins"
    # count as the same metric rather than as a missing one
    shared = _metric_terms(q_words) & _metric_terms(a_words)
    if not shared:
        problems.append(
            f"[{spec['id']}] reference answer shares no metric term with the question (Rule 10)"
        )

    # A figure is required only where the question asks for one. Some candidates
    # are genuinely qualitative -- how a bank *characterised* a rule -- and their
    # anchors carry no numbers at all.
    if _ANSWER_ASKS_VALUE.search(spec["question"]) and not re.search(r"\d", answer):
        problems.append(
            f"[{spec['id']}] the question asks for a value but the answer carries no figure (Rule 10)"
        )

    for clause in [c for c in re.split(r"[;.]", answer) if c.strip()]:
        tokens = _WORD_RE.findall(clause)
        last = tokens[-1].strip(".,;:!?\"'()[]").lower()
        if last in DANGLING_TAIL_NOUNS:
            problems.append(
                f"[{spec['id']}] answer clause ends on the light noun {last!r}: "
                f"...{clause.strip()[-55:]!r} -- reads as a carried-over anchor fragment (Rule 11)"
            )
    return problems


_SPAN_OPENING = re.compile(r"^(In|Over|Across|During|Through)\s+(late\s+|early\s+)?20\d\d\s+and\b", re.I)
_HYPHEN_GAP = re.compile(r"\w-\s+\w|\w\s+-\w")


def check_answer_period_attribution(spec: dict, provenances: list[dict]) -> list[str]:
    """Each figure belongs to one quarter; the answer must not say otherwise.

    Rule 10 asked for a period in every answer. Satisfying that by prefixing the
    question's span to a multi-anchor answer turns a single-quarter figure into a
    multi-year claim -- a faithfulness error in a gold answer, which is the very
    thing the faithfulness metric measures. Where the anchors come from more than
    one quarter, each clause must carry its own period instead.
    """
    quarters = {p["transcript_id"].split("_", 1)[1] for p in provenances}
    if len(quarters) > 1 and _SPAN_OPENING.match(spec["reference_answer"].strip()):
        return [
            f"[{spec['id']}] answer opens with a multi-period span "
            f"({spec['reference_answer'][:45]!r}) but its anchors come from {sorted(quarters)}; "
            "attribute each clause to its own anchor's quarter (Rule 10)"
        ]
    return []


# Scope and basis qualifiers. Rule 2 catches an imported VALUE; it does not catch
# an imported CHARACTERISATION -- calling a segment figure "investment banking
# revenue" when the source said "gross", or a book-value figure "tangible" when
# the anchor says only "book value". Those change what the number means while
# leaving every digit correct.
SCOPE_QUALIFIERS = (
    "adjusted", "non-interest", "net operating", "core", "underlying", "reported",
    "total", "average", "period-end", "gross", "tangible", "annualized", "organic",
    "firmwide", "segment", "net", "cash", "operating", "retail", "pro forma",
)

# "reported" is a scope qualifier in "on a reported basis" and an ordinary
# attribution verb in "M&T reported". Only the modifier sense is worth flagging.
_REPORTED_AS_MODIFIER = re.compile(r"\b(?:a|on a)\s+reported\b|\breported\s+basis\b", re.I)


def _qualifier_present(term: str, text: str) -> bool:
    if term == "reported":
        return bool(_REPORTED_AS_MODIFIER.search(text))
    return bool(re.search(rf"\b{re.escape(term)}\b", text))


def check_scope_qualifiers(spec: dict, provenances: list[dict]) -> list[str]:
    """Flag scope words in the answer that no anchor supports. REVIEW ONLY.

    Deliberately not a hard failure and not fully automatable: whether a qualifier
    changes the meaning of a figure is a judgement. A word already present in the
    question is allowed, on the same footing as the entity and the period.
    """
    anchors = " ".join(p["anchor"] for p in provenances).lower()
    question = spec["question"].lower()
    answer = spec["reference_answer"].lower()
    flagged = [
        q for q in SCOPE_QUALIFIERS
        if _qualifier_present(q, answer)
        and not _qualifier_present(q, anchors)
        and not _qualifier_present(q, question)
    ]
    return [
        f"SCOPE REVIEW [{spec['id']}] answer uses {flagged} to describe a figure, but no anchor "
        "carries that qualifier -- confirm it does not change what the number means"
    ] if flagged else []


def check_dropped_qualifiers(spec: dict, provenances: list[dict]) -> list[str]:
    """Flag a metric named MORE BROADLY in the answer than in its anchor. REVIEW ONLY.

    The mirror of check_scope_qualifiers, and just as damaging. "Tangible book
    value per share" and "book value per share" are different metrics -- tangible
    excludes goodwill and intangibles, which is why banks report it separately.
    Dropping the qualifier to stay inside the anchor does not make the answer more
    conservative; it names a different figure.

    Where a qualifier is part of the metric's standard name it belongs in the
    answer, licensed by the question on the same footing as the entity and the
    period. Where it appears in neither anchor nor question, the QUESTION is what
    needs amending -- not the answer, and not by deletion.
    """
    anchors = " ".join(p["anchor"] for p in provenances).lower()
    answer = spec["reference_answer"].lower()
    problems = []
    for qualifier in SCOPE_QUALIFIERS:
        for match in re.finditer(rf"\b{re.escape(qualifier)}\s+(\w+)", anchors):
            noun = match.group(1)
            if len(noun) < 4:
                continue
            pair = f"{qualifier} {noun}"
            if re.search(rf"\b{re.escape(noun)}\b", answer) and pair not in answer:
                problems.append(
                    f"DROPPED-QUALIFIER REVIEW [{spec['id']}] the anchor says {pair!r} but the "
                    f"answer says {noun!r} without it -- confirm this is the same metric"
                )
    return sorted(set(problems))


# Prepositional carve-outs. These are not scope WORDS -- they are scope
# PHRASES -- so the qualifier lists miss them entirely, and omitting one does
# not weaken a claim, it reverses it. "a reserve release ... as certain troubled
# industries and credits outside of commercial real estate" describes an
# improvement everywhere EXCEPT commercial real estate; drop the carve-out and
# the same sentence reads as an improvement IN commercial real estate.
EXCLUSION_PATTERNS = (
    r"\boutside of\b", r"\bexcluding\b", r"\bother than\b", r"\bapart from\b",
    r"\bnet of\b", r"\bex-\w+", r"\bbefore (?:tax|taxes|provision|items)\b",
)


def check_exclusions(spec: dict, provenances: list[dict]) -> list[str]:
    """Flag a carve-out carried by the evidence but missing from the answer.

    REVIEW ONLY, like the qualifier checks, and for the same reason: whether an
    omitted exclusion changes the meaning is a judgement. Two directions are
    reported separately --
      * the ANCHOR carries the carve-out and the answer drops it: the answer may
        now assert the opposite of the source;
      * the SOURCE SENTENCE carries it but the anchor stops short: the anchor
        itself may be misleading in isolation, which is worth knowing even when
        the answer is written carefully around it.
    """
    answer = spec["reference_answer"].lower()
    problems = []
    for provenance in provenances:
        anchor = provenance["anchor"].lower()
        sentence = provenance["source_sentence"].lower()
        for pattern in EXCLUSION_PATTERNS:
            in_anchor = re.search(pattern, anchor)
            in_sentence = re.search(pattern, sentence)
            if in_anchor and not re.search(pattern, answer):
                problems.append(
                    f"EXCLUSION REVIEW [{spec['id']}] {provenance['transcript_id']}: the anchor "
                    f"carries {in_anchor.group(0)!r} but the answer omits it -- an omitted "
                    "carve-out can invert the claim"
                )
            elif in_sentence and not in_anchor:
                problems.append(
                    f"EXCLUSION REVIEW [{spec['id']}] {provenance['transcript_id']}: the source "
                    f"sentence carries {in_sentence.group(0)!r} but the anchor stops before it -- "
                    "confirm the anchor is not misleading in isolation"
                )
    return sorted(set(problems))


def check_whitespace(spec: dict) -> list[str]:
    """Line-wrap artefacts depress semantic similarity for no substantive reason."""
    problems = []
    for field in ("question", "reference_answer"):
        text = spec[field]
        if "  " in text:
            problems.append(f"[{spec['id']}] {field} contains a double space")
        if _HYPHEN_GAP.search(text):
            problems.append(
                f"[{spec['id']}] {field} has a stray space inside a hyphenated term: "
                f"{_HYPHEN_GAP.search(text).group(0)!r}"
            )
    return problems


# NOTE: the final coherence pass -- does the answer read as prose, is every
# demonstrative anchored, does a single-quarter figure sit under a single-quarter
# framing -- is a HUMAN judgement made by reading each answer with the question in
# view and the anchors hidden. It is deliberately not automated here; a regex that
# approximated it would give false assurance. The checks above cover only the
# mechanically decidable part.


def check_question_period(spec: dict) -> list[str]:
    """(Rule 12) A question with no time frame is not one an analyst would ask."""
    quarters, years = question_period(spec["question"])
    if quarters is None and not years:
        return [
            f"[{spec['id']}] question names no time period (Rule 12): "
            f"{spec['question']!r} -- state the span the anchors actually cover"
        ]
    return []


def check_metadata(spec: dict, provenances: list[dict]) -> list[str]:
    """(Rule 9) Difficulty label and notes must describe the CURRENT anchors."""
    problems = []
    notes = spec["notes"]
    difficulty = spec["difficulty"]
    sections = {p["section"] for p in provenances}
    if re.search(r"Q&A", notes) and SECTION_QA not in sections:
        problems.append(
            f"[{spec['id']}] notes mention Q&A but no anchor is Q&A-sourced (Rule 9: stale metadata)"
        )
    if re.search(r"Q&A", difficulty) and SECTION_QA not in sections:
        problems.append(f"[{spec['id']}] difficulty mentions Q&A but no anchor is Q&A-sourced (Rule 9)")
    for where, text in (("notes", notes), ("difficulty label", difficulty)):
        if re.search(r"spoken by an? analyst|analyst-sourced|analyst-spoken", text, re.I):
            problems.append(
                f"[{spec['id']}] {where} describes an analyst-spoken anchor, which Rule 1 no "
                "longer permits (Rule 9)"
            )
    # a claimed Q&A anchor count must match reality
    claimed = re.search(r"(one|two|three)\s+Q&A\s+anchors?", difficulty + " " + notes, re.I)
    if claimed:
        want = {"one": 1, "two": 2, "three": 3}[claimed.group(1).lower()]
        have = sum(1 for p in provenances if p["section"] == SECTION_QA)
        if want != have:
            problems.append(
                f"[{spec['id']}] metadata claims {want} Q&A anchor(s) but {have} are Q&A-sourced (Rule 9)"
            )
    # a claim that the question is period-neutral must still be true
    if re.search(r"period-neutral", notes, re.I):
        quarters, years = question_period(spec["question"])
        if quarters is not None or years:
            problems.append(
                f"[{spec['id']}] notes claim the question is period-neutral, but it names "
                f"{sorted(years) or sorted(quarters)} (Rule 9)"
            )
    # a claimed anchor count must match
    count_claim = re.search(r"\b(two|three)\s+(anchors|distinct|different)\b", notes + " " + difficulty, re.I)
    if count_claim:
        want = {"two": 2, "three": 3}[count_claim.group(1).lower()]
        if want != len(provenances):
            problems.append(
                f"[{spec['id']}] metadata claims {count_claim.group(0)!r} but the candidate has "
                f"{len(provenances)} anchor(s) (Rule 9)"
            )
    # any quarter named in the notes must be one the anchors actually come from
    have_quarters = {
        f"{p['transcript_id'].split('_')[1]} {p['transcript_id'].split('_')[2]}" for p in provenances
    }
    for claimed in re.findall(r"\b(20\d\d)\s*(Q[1-4])\b", notes):
        if f"{claimed[0]} {claimed[1]}" not in have_quarters:
            problems.append(
                f"[{spec['id']}] notes name {claimed[0]} {claimed[1]} but no anchor comes from it; "
                f"anchors are {sorted(have_quarters)} (Rule 9)"
            )

    hard_note = bool(re.search(r"\bHARD\b", notes))
    hard_label = difficulty.strip().upper().startswith("HARD")
    if hard_note and not hard_label:
        problems.append(
            f"[{spec['id']}] notes say HARD but the difficulty label is {difficulty.split(chr(8212))[0].strip()!r} (Rule 9)"
        )
    return problems


def build_candidate(corpus: Corpus, spec: dict) -> tuple[dict | None, list[str]]:
    """Verify every anchor of one candidate; drop the candidate if any fails."""
    provenances, problems = [], []
    for anchor_spec in spec["anchors"]:
        provenance, anchor_problems = verify_anchor(corpus, anchor_spec)
        problems.extend(f"[{spec['id']}] {p}" for p in anchor_problems)
        if provenance is not None:
            provenances.append(provenance)

    # (Rule 1) attribution must match the question. A question asking what a
    # company said or reported cannot rest on an analyst restating it back to
    # management -- that is evidence of what was discussed, not a disclosure.
    if spec.get("asks_company_statement", True):
        for provenance in provenances:
            if provenance["speaker_role"] == "analyst":
                problems.append(
                    f"[{spec['id']}] {provenance['transcript_id']}: anchor is spoken by "
                    f"{provenance['speaker']} (analyst), but the question asks what the company "
                    "said/reported (Rule 1: set asks_company_statement=False only if the question "
                    "is explicitly about what was discussed on the call)"
                )

    # (Rule 4) a thematic candidate synthesises across companies. One marked
    # subtype 'temporal' deliberately tests period discrimination within a single
    # company instead, and is labelled rather than silently mixed in.
    tickers = {p["transcript_id"].split("_")[0] for p in provenances}
    if spec["category"] == "thematic" and spec.get("subtype") != "temporal" and len(tickers) < 2:
        problems.append(
            f"[{spec['id']}] thematic spans only {sorted(tickers)} "
            "(Rule 4: needs >=2 companies, or subtype='temporal')"
        )

    problems += check_period(spec, provenances)
    problems += check_answer_quality(spec, provenances)
    problems += check_answer_period_attribution(spec, provenances)
    problems += check_whitespace(spec)
    for note in (check_scope_qualifiers(spec, provenances)
                 + check_dropped_qualifiers(spec, provenances)
                 + check_exclusions(spec, provenances)):
        print(note)
    problems += check_question_period(spec)
    problems += check_answer(spec, provenances)
    problems += check_metadata(spec, provenances)

    if problems or len(provenances) != len(spec["anchors"]):
        return None, problems

    transcript_ids = [p["transcript_id"] for p in provenances]
    candidate = {
        "id": spec["id"],
        "category": spec["category"],
        "question": spec["question"],
        "transcript_ids": list(dict.fromkeys(transcript_ids)),
        "gold_anchors": [p["anchor"] for p in provenances],
        "reference_answer": spec["reference_answer"],
        "provenance": [
            {
                "transcript_id": p["transcript_id"],
                "anchor": p["anchor"],
                "source_sentence": p["source_sentence"],
                "section": p["section"],
                "speaker": p["speaker"],
                "speaker_role": p["speaker_role"],
                "turn_index": p["turn_index"],
                "anchor_char_offset_in_sentence": p["anchor_char_offset_in_sentence"],
                "sentence_char_start": p["sentence_char_start"],
                "sentence_char_end": p["sentence_char_end"],
                "chunk_ids_200": p["chunk_ids_200"],
                "chunk_ids_500": p["chunk_ids_500"],
                "doc_frequency": p["doc_frequency"],
                "sentence_chunks_200": p["sentence_chunks_200"],
                "sentence_chunks_500": p["sentence_chunks_500"],
                "chunk_size_sensitive": p["chunk_size_sensitive"],
            }
            for p in provenances
        ],
        "difficulty": spec["difficulty"],
        "notes": spec["notes"],
        "batch": spec["batch"],
        "subtype": spec.get("subtype"),
        "asks_company_statement": spec.get("asks_company_statement", True),
        "chunk_size_sensitive": any(p["chunk_size_sensitive"] for p in provenances),
    }
    return candidate, []


# ---------------------------------------------------------------------------
# What the corpus does NOT contain (for authoring unanswerable questions)
# ---------------------------------------------------------------------------


def build_absence_report(corpus: Corpus, index: dict) -> dict:
    """Facts about corpus boundaries, so unanswerable questions can be grounded.

    Deliberately reports only what is checkable: the ticker list, the quarter
    range, and topics with a low document frequency in the mined vocabulary.
    Proving a topic is wholly absent across 128 transcripts is not something
    this can establish, so rare topics are reported WITH their frequency rather
    than claimed to be missing.
    """
    entries = index["transcripts"]
    quarters = sorted({f"{e['year']}Q{e['quarter']}" for e in entries})
    tickers = sorted({e["ticker"] for e in entries})
    companies = {e["ticker"]: e["company"] for e in entries}

    # Rank rare topics by how much they are discussed *where they do appear*, then
    # spread the selection across document frequencies 1-4. Sorting by topic name
    # instead would just return whatever is alphabetically first, which surfaces
    # mining fragments rather than genuine subject areas.
    frequency = index["aggregates"]["topic_frequency"]
    rare: list[dict] = []
    for doc_freq in (1, 2, 3, 4):
        at_frequency = sorted(
            (row for row in frequency if row["n_transcripts"] == doc_freq),
            key=lambda row: (-row["total_mentions"], row["topic"]),
        )
        rare.extend(at_frequency[:3])
    return {
        "tickers": [{"ticker": t, "company": companies[t]} for t in tickers],
        "n_tickers": len(tickers),
        "quarters": quarters,
        "quarter_range": f"{quarters[0]} through {quarters[-1]}",
        "n_transcripts": len(entries),
        "rare_topics": [
            {
                "topic": row["topic"],
                "n_transcripts": row["n_transcripts"],
                "tickers": row["tickers"],
                "total_mentions": row["total_mentions"],
            }
            for row in rare
        ],
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

CATEGORY_TITLES = {
    "unanswerable": "Unanswerable",
    "factual": "Factual",
    "thematic": "Thematic",
    "comparative": "Comparative",
}


def render_markdown(candidates: list[dict], absence: dict, dropped: list[str]) -> str:
    lines = [
        "# Reference candidate questions",
        "",
        "> **Reference material, not the benchmark.** `benchmark/questions.jsonl` is authored by",
        "> the researcher; nothing here is a gold label. These exist to calibrate against real",
        "> corpus material.",
        "",
        "> **`reference_candidates.json` is authoritative for exact text.** Anchors below are",
        "> reproduced in full — never truncated, escaped or normalised — but the JSON is the",
        "> copy source of record.",
        "",
        f"{len(candidates)} candidates — "
        f"{sum(1 for c in candidates if c['batch'] == 1)} in batch 1, "
        f"{sum(1 for c in candidates if c['batch'] == 2)} in batch 2. "
        "Batch 2 was built to fill batch 1's ticker, quarter and Q&A gaps, and its comparatives",
        "share no anchor with any thematic candidate in either batch.",
        "",
        "⚠ **CHUNK-SIZE SENSITIVE** marks a candidate whose source sentence is split across two",
        "chunks at 200 tokens but sits whole in one chunk at 500. Retrieval matches chunks, not",
        "anchors, so where an anchor boundary falls changes nothing — but a sentence that is",
        "divided under one condition and intact under the other genuinely probes the chunk-size",
        "variable, because the evidence and the words identifying it are only jointly retrievable",
        "at 500. These are the most informative candidates in the set.",
        "",
        f"Every anchor was sliced from the source by character",
        "offset rather than transcribed, then verified to (1) occur verbatim in its transcript,",
        "(2) sit inside a single chunk under both the 200- and 500-token configs, (3) stand at",
        f"least {MIN_EDGE_MARGIN_WORDS} words clear of both ends of its sentence, and (4) have its",
        "corpus-wide document frequency measured and reported.",
        "",
        "`df` = transcripts containing that exact anchor string. **`df 1` means the anchor is",
        "unique corpus-wide**; anything higher is flagged in the candidate's concerns.",
        "",
        "**How the reference answers are constrained.** Each answer restates only what its anchors say.",
        f"Because an anchor must stand {MIN_EDGE_MARGIN_WORDS} words clear of both sentence ends, it often",
        "excludes the subject that opens the sentence — several anchors carry the figure but not the metric",
        "name. Where that happens the metric is supplied by the *question*, never asserted independently by",
        "the answer, and the full source sentence is printed beneath each anchor so the gap is visible.",
        "Answers are deliberately narrower than their source sentences rather than inferring past them.",
        "",
    ]
    if dropped:
        lines += [f"{len(dropped)} candidate(s) were dropped in verification; see the report at the end.", ""]
    lines += ["---", ""]

    unanswerable = [c for c in candidates if c["category"] == UNANSWERABLE_CATEGORY]
    if unanswerable:
        lines += [
            f"## Unanswerable ({len(unanswerable)})",
            "",
            "No anchors and no transcript_ids: `evaluate.py` excludes these from anchor coverage@5",
            "and MRR@5 entirely and scores them only on an exact match against `generate.ABSTENTION`.",
            "Absence is re-proven at build time by counting every search term over all 128 raw",
            "transcripts; one occurrence anywhere fails the build.",
            "",
        ]
        for candidate in unanswerable:
            evidence = candidate["absence_evidence"]
            lines += [
                f"### {candidate['id']} · batch 3 · {candidate['absence_type']}",
                "",
                f"**Q.** {candidate['question']}",
                "",
                f"**Reference answer.** {candidate['reference_answer']}",
                "",
                f"**Absence proof.** {evidence['occurrences_found']} occurrences of "
                + ", ".join(f"`{t}`" for t in evidence["search_terms"])
                + f" across {evidence['transcripts_searched']} transcripts "
                f"({evidence['method']}).",
                "",
                f"**What retrieval actually returns.** {candidate['expected_retrieval']}",
                "",
                f"**Notes.** {candidate['notes']}",
                "",
                "---",
                "",
            ]

    for category in ("factual", "thematic", "comparative"):
        in_category = [c for c in candidates if c["category"] == category]
        lines += [f"## {CATEGORY_TITLES[category]} ({len(in_category)})", ""]
        for candidate in in_category:
            lines += [
                f"### {candidate['id']} · batch {candidate['batch']} · {candidate['difficulty']}"
                + ("  ⚠ CHUNK-SIZE SENSITIVE" if candidate["chunk_size_sensitive"] else ""),
                "",
                f"**Q.** {candidate['question']}",
                "",
                f"**Reference answer.** {candidate['reference_answer']}",
                "",
                f"**Transcripts.** {', '.join(candidate['transcript_ids'])}",
                "",
                "**Gold anchors.**",
                "",
            ]
            for provenance in candidate["provenance"]:
                section = "Q&A" if provenance["section"] == SECTION_QA else "prepared remarks"
                sensitive = (
                    "  — **source sentence splits across "
                    f"{provenance['sentence_chunks_200']} chunks at 200 tokens but is whole at 500**"
                    if provenance["chunk_size_sensitive"] else ""
                )
                lines += [
                    f"- `{provenance['transcript_id']}` · {section} · {provenance['speaker']} · "
                    f"turn {provenance['turn_index']} · df {provenance['doc_frequency']}{sensitive}",
                    f"  > {provenance['anchor']}",
                    "",
                    f"  Source sentence (offset {provenance['anchor_char_offset_in_sentence']} "
                    f"within it; chunks `{provenance['chunk_ids_200'][0]}` / "
                    f"`{provenance['chunk_ids_500'][0]}`):",
                    f"  > {provenance['source_sentence']}",
                    "",
                ]
            lines += [f"**Notes.** {candidate['notes']}", "", "---", ""]

    lines += [
        "## What the corpus does not contain",
        "",
        "For authoring unanswerable questions. **No unanswerable candidates are proposed here** —",
        "absence cannot be verified reliably across 128 transcripts, and a question that turned out",
        "to be partially answerable would be worse than none. These are the checkable boundaries.",
        "",
        f"### Tickers included ({absence['n_tickers']})",
        "",
        "Any bank outside this list is absent from the corpus by construction — Truist, Citizens,",
        "First Horizon, Zions, Comerica, Ally and Discover are all natural choices.",
        "",
    ]
    for row in absence["tickers"]:
        lines.append(f"- `{row['ticker']}` — {row['company']}")
    lines += [
        "",
        f"### Quarter range",
        "",
        f"**{absence['quarter_range']}** — {len(absence['quarters'])} consecutive quarters, "
        f"{absence['n_transcripts']} transcripts, every ticker present in every quarter.",
        "Anything in 2022 or earlier, or 2025 or later, is outside the corpus.",
        "",
        "### Rarely discussed topics",
        "",
        "Mined topics with a low document frequency, ranked by how much they are discussed where they",
        "do appear, across `df` 1 to 4. These are **rare, not absent** — a question grounded here needs",
        "the specific claim checked, not just the topic. They are also raw mined phrases, so a few are",
        "conversational artifacts rather than subject areas (`happy new` comes from a new-year greeting);",
        "read them as pointers into thin coverage, not as a curated list.",
        "",
    ]
    for row in absence["rare_topics"]:
        lines.append(
            f"- **{row['topic']}** — df {row['n_transcripts']}, "
            f"{row['total_mentions']} mentions in {', '.join(row['tickers'])}"
        )

    if dropped:
        lines += ["", "---", "", "## Dropped in verification", ""]
        for problem in dropped:
            lines.append(f"- {problem}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Candidate specifications
# ---------------------------------------------------------------------------

# Anchors are given as (transcript_id, turn_index, sentence_char_start, words).
# The word range is inclusive and indexes whitespace-separated tokens of the
# source sentence; the text itself is sliced out by slice_anchor().
def _a(transcript_id: str, turn_index: int, sentence_char_start: int, words: tuple[int, int]) -> dict:
    return {
        "transcript_id": transcript_id,
        "turn_index": turn_index,
        "sentence_char_start": sentence_char_start,
        "words": words,
    }


# Anchors rejected during construction, kept as a record of what was tried and
# why. Runtime failures from verify_anchor() are appended to this at build time.
KNOWN_DROPS: list[str] = [
    "[batch 1][ref_them_02/ref_comp_01] C_2024_Q1 turn 25 words (4,17) "
    "\"we are hearing kind of favorable things about how the Basel III endgame proposal\": "
    "spans 2 chunks at 200 tokens. The optimistic wording and the phrase 'Basel III endgame' "
    "fall either side of a 200-token boundary. Replaced with words (12,22), which keeps the "
    "topic phrase and loses the sentiment.",
    "[batch 1][ref_them_07/ref_comp_04] FITB_2024_Q3 turn 2 words (2,13) "
    "\"retail deposits nearly 16% year-over-year and gained meaningful market share in 14\": "
    "spans 2 chunks at 200 tokens. Shortened to (2,9).",
    "[batch 1][ref_them_05] AXP_2024_Q3 turn 3 words (8,20): spans 2 chunks at 200 tokens, and "
    "NO usable range exists in that sentence -- the 200-token boundary falls between '$1.9' and "
    "'billion', so no span carries a complete figure. Bank swapped out; candidate reduced to two "
    "anchors.",
    "[batch 1][ref_them_05] COF_2024_Q3 turn 2 words (9,19) "
    "\"by the impact of dividends, loan growth and $150 million of\": contained, but the words "
    "'share repurchases' fall outside the edge margin, so the anchor could not support the "
    "reference answer. Dropped rather than weaken the answer.",
    "[batch 1][ref_them_04] A third bank's operating-leverage sentence was rejected because the "
    "metric sat too close to the sentence edge to leave the required 2-word margin. Candidate "
    "kept at two anchors.",
    "[batch 2][planned MS-vs-BK trading comparative] Abandoned: a search of MS and BK for "
    "'markets revenue' returned no sentence anywhere in either bank's eight transcripts that "
    "yielded a 5-15 word range both edge-clear and contained under 200 AND 500 tokens. Replaced "
    "with the PNC/COF net interest margin pair (ref_comp_12).",
    "[batch 2][planned PNC-vs-USB capital markets comparative] Abandoned: 'capital markets' "
    "produced usable anchors for PNC but none for USB under the same constraints, so no "
    "same-quarter pair existed. Replaced with the PNC/USB expense-plan pair (ref_comp_07), which "
    "uses the same two banks in the same quarter on a different topic.",
    "[rules pass][ref_fact_01] BK_2023_Q1 turn 3 words (3,10) 'custody and/or administration of "
    "$46.6 trillion increased by': ends on 'by' (Rule 3), and NO span in that sentence carries both "
    "the figure and its 2% change within the edge margin. Replaced with a BK_2024_Q1 sentence that "
    "carries both.",
    "[rules pass][ref_them_09] BAC_2024_Q3 turn 25: anchor spoken by Matt O'Connor (analyst) while "
    "the question asks what banks reported (Rule 1). Replaced with a FITB_2024_Q2 management anchor "
    "on the same topic.",
    "[rules pass][ref_them_10] WFC_2024_Q2 turn 43: anchor spoken by Matt O'Connor (analyst) "
    "(Rule 1). Replaced with a WFC_2024_Q1 management anchor on the same topic.",
    "[rules pass][ref_them_12] MS_2023_Q2 turn 26: anchor spoken by Steven Chubak (analyst) "
    "(Rule 1). No management wealth-management alternative passed containment, so the anchor was "
    "DROPPED and the candidate reduced from three anchors to two.",
    "[rules pass][ref_them_11] MTB_2023_Q4 turn 9: anchor ends on 'not' (Rule 3) and no valid span "
    "carries the clause it qualifies, so the reference answer could not be supported by anchor text "
    "alone (Rule 2). DROPPED; candidate reduced to two anchors.",
    "[rules pass][Rule 5 re-sourcing] Five batch-1 thematics had anchors re-sourced so the "
    "comparatives they collided with stay independent: ref_them_02 (dropped GS_2023_Q4, moved Citi "
    "to 2024 Q3), ref_them_03 (BAC to 2023 Q3, HBAN to 2023 Q1), ref_them_05 (BAC to 2024 Q3), "
    "ref_them_06 (FITB to 2023 Q1, GS to 2024 Q1), ref_them_07 (HBAN to 2023 Q2, FITB to 2023 Q2). "
    "The comparatives kept their original anchors and notes.",
    "[batch 3][ref_unans_04] REMOVED. The 2029 expense-target question was mechanically sound -- "
    "'2029' occurs zero times across all 128 transcripts -- but its absence is an INTERIOR GAP "
    "rather than a structural property: 2028 occurs 9 times and 2030 occurs 6 times, so the year "
    "is empty by coincidence rather than because it lies outside the corpus window. Every other "
    "unanswerable candidate rests on a structural fact (a company outside the 16, a quarter "
    "outside 2023Q1-2024Q4, a topic never discussed). Removed when rebalancing to 15 thematics, "
    "since unanswerable questions are excluded from anchor_coverage_at_5 and MRR and so "
    "contribute nothing to the primary research question.",
    "[exclusion check][ref_them_03] BAC_2023_Q3 turn 3 words (3,17) 'a reserve release of $139 "
    "million as certain troubled industries and credits outside of commercial': DROPPED. The "
    "source sentence is about credits OUTSIDE commercial real estate having improved outlooks, so "
    "an answer omitting the carve-out inverted the meaning -- it read as a release relating to "
    "CRE. Extending to words (5,19) does carry 'outside of commercial real estate' and is "
    "contained under both configs with df 1, but drops 'reserve' from 'reserve release', trading "
    "an inverted claim for a renamed metric. The sentence is also off-topic for a question about "
    "CRE exposure, being about everything except it. Candidate reduced to two anchors; the "
    "chunk-size-sensitive flag is unaffected, since it comes from the Huntington anchor.",
    "[rules 7-9][ref_them_06] GS_2024_Q1 turn 2: the sentence states its efficiency ratio value "
    "(60.9%) at the last word, inside the edge margin, so no valid span carries it. An answer "
    "without a value fails Rule 8, and reaching outside the anchor fails Rule 2. Rules 2, 3 and 8 "
    "cannot all hold for this sentence -- anchor DROPPED, candidate reduced to two.",
    "[rules 7-9][ref_comp_05] REMOVED ENTIRELY. Neither Capital One buyback sentence "
    "(COF_2024_Q2 turn 2, COF_2024_Q3 turn 2) has any valid span carrying '$150 million of share "
    "repurchases' -- 'share repurchases' falls inside the edge margin in both. The answer could "
    "therefore say '$150 million' without saying of what, which fails Rule 8, and no alternative "
    "Capital One sentence on capital return passed containment. Comparatives reduced to 11.",
    "[rules 7-9][Rule 7 rewording] Four questions named a period their re-sourced anchors no longer "
    "matched: ref_them_03 and ref_them_06 made period-neutral, ref_them_07 restated to the real "
    "2023-2024 span, ref_comp_09 corrected from 'heading into 2025' to the late-2024 calls it cites.",
    "[batch 2] NOTE: batch 2 recorded no build-time verification failures because candidate word "
    "ranges were pre-checked for containment during selection rather than guessed and then tested. "
    "The two entries above are rejections that happened during that selection step; they are the "
    "batch 2 equivalent of batch 1's drops.",
]

BATCH1: list[dict] = [
    # ------------------------------------------------------------------ factual
    {
        "id": "ref_fact_01",
        "category": "factual",
        "difficulty": "easy — question vocabulary matches the passage almost word for word",
        "question": "What were BNY Mellon's assets under custody and administration in the first quarter of 2024, and how did they change?",
        "reference_answer": (
            "BNY Mellon's assets under custody and administration of $48.8 trillion were up 5% "
            "year-over-year in the first quarter of 2024."
        ),
        "anchors": [_a("BK_2024_Q1", 3, 473, (3, 17))],
        "notes": (
            "Assets under custody and administration is the headline scale metric for a custody bank. "
            "EASY: the question and the passage use the same words. NOTE: this anchor replaced an earlier "
            "Q1 sentence in which no valid span carried both the figure and its change, because the "
            "'2%' sat inside the edge margin; this 2024 Q1 sentence carries both. CHUNK-SIZE "
            "SENSITIVE: the source sentence splits across two chunks at 200 tokens but sits whole in "
            "one at 500."
        ),
    },
    {
        "id": "ref_fact_02",
        "category": "factual",
        "difficulty": "easy — distinctive guidance phrasing shared by question and passage",
        "question": (
            "What did American Express raise its full-year EPS guidance to in the third quarter of "
            "2024?"
        ),
        "reference_answer": (
            "American Express raised its full-year EPS guidance to $13.75 to $14.05 in the third "
            "quarter of 2024."
        ),
        "anchors": [_a("AXP_2024_Q3", 3, 8851, (3, 12))],
        "notes": (
            "Guidance revisions are among the most-asked-about disclosures on any call. EASY: 'full year "
            "EPS guidance' is a distinctive multi-word phrase carried verbatim in the anchor, which "
            "should favour BM25 as much as dense retrieval. CONCERN: AXP repeats this guidance range in "
            "the same call's prepared remarks, so another chunk may legitimately also contain the "
            "figures — check the anchor's document frequency below before treating a second hit as an error."
        ),
    },
    {
        "id": "ref_fact_03",
        "category": "factual",
        "difficulty": "medium — a formal question against a plainly-worded reporting sentence",
        "question": "How much did Morgan Stanley report in advisory revenues for the first quarter of 2023?",
        "reference_answer": (
            "Morgan Stanley's advisory revenues were $638 million in the first quarter of 2023."
        ),
        "anchors": [_a("MS_2023_Q1", 2, 1809, (3, 10))],
        "notes": (
            "Segment revenue lines are routine analyst questions. MEDIUM: the question asks about "
            "'advisory revenues' while the passage is a terse reporting sentence, so there is real "
            "but not extreme vocabulary distance. CONCERN: the anchor is generic apart from the "
            "figure, so it leans on '$638 million' carrying the identification — its document "
            "frequency of 1 confirms the string occurs in no other transcript."
        ),
    },
    {
        "id": "ref_fact_04",
        "category": "factual",
        "difficulty": "easy retrieval — metric name and value adjacent in the anchor",
        "question": "What were State Street's management fees in the first quarter of 2023, and how did they change year-on-year?",
        "reference_answer": (
            "State Street's management fees were $457 million in the first quarter of 2023, "
            "down 12% year-on-year."
        ),
        "anchors": [_a("STT_2023_Q1", 3, 3209, (2, 9))],
        "notes": (
            "Management fees are State Street's core fee line and the natural question for a quarter "
            "with falling markets. EASY: metric name, value and the year-on-year change all sit inside "
            "the anchor, so the reference answer is fully supported without reaching outside it. "
            "CONCERN: none material; the value is unique to this transcript in the index."
        ),
    },
    {
        "id": "ref_fact_05",
        "category": "factual",
        "difficulty": "medium — Q&A sourced, conversational phrasing",
        "question": "How large was the Walmart-related build that Capital One called out as an adjusting item in the second quarter of 2024?",
        "reference_answer": (
            "The Walmart-related build that Capital One called out as an adjusting item in the "
            "second quarter of 2024 was $826 million."
        ),
        "anchors": [_a("COF_2024_Q2", 7, 107, (3, 17))],
        "notes": (
            "Q&A-SOURCED. The Walmart partnership wind-down was a live analyst topic for Capital One, and "
            "the CFO quantifies it only in the Q&A, not the prepared remarks — so this candidate tests "
            "whether the retrievers reach into conversational text at all. MEDIUM: 'Walmart' is a strong, "
            "rare lexical hook, but the surrounding phrasing is loose spoken English ('the $826 million "
            "build that we spelled out') rather than reporting language. CONCERN: the question says "
            "'build' rather than 'reserve build' precisely because the source never says 'reserve' — "
            "do not tighten that wording without re-reading the source sentence."
        ),
    },
    {
        "id": "ref_fact_06",
        "category": "factual",
        "difficulty": "medium — multi-value answer, guidance framing",
        "question": (
            "What full-year expense range did Citi guide to on its fourth-quarter 2023 call, and what "
            "was the prior figure?"
        ),
        "reference_answer": (
            "On its fourth-quarter 2023 call, Citi guided to full-year expenses of approximately "
            "$53.5 billion to $53.8 billion, down from $54.3 billion."
        ),
        "anchors": [_a("C_2023_Q4", 3, 20996, (2, 14))],
        "notes": (
            "Citi's expense trajectory was the central controversy of its transformation programme, so "
            "this is exactly the number an analyst would chase. MEDIUM: the anchor carries three separate "
            "dollar figures, so an answer is only correct if all three are reproduced exactly and in the "
            "right roles — a good test of whether the generator copies faithfully rather than rounding. "
            "CONCERN: the sentence is guidance, so the question must be phrased as 'guided to', not "
            "'reported' — a candidate that blurs the two would be wrong even with the right figures."
        ),
    },
    {
        "id": "ref_fact_07",
        "category": "factual",
        "difficulty": "medium — requires both endpoints of a change",
        "question": "How did Bank of America's rate paid on deposits change between the third and fourth quarters of 2024?",
        "reference_answer": (
            "Bank of America's rate paid on deposits moved from 210 basis points in the third quarter "
            "of 2024 to 194 basis points in the fourth quarter."
        ),
        "anchors": [_a("BAC_2024_Q4", 2, 3608, (4, 17))],
        "notes": (
            "Deposit cost trajectory was the dominant question for large banks as rates began falling. "
            "MEDIUM: the anchor holds both endpoints, so a partial answer quoting only one number is "
            "detectably incomplete — useful for the faithfulness check rather than retrieval alone. "
            "CONCERN: 'rate paid' opens the source sentence and only 'on deposits' falls inside the "
            "anchor, so a retriever keying on the exact phrase 'rate paid on deposits' is matching the "
            "chunk, not the anchor."
        ),
    },
    # ----------------------------------------------------------------- thematic
    {
        "id": "ref_them_01",
        "category": "thematic",
        "difficulty": "easy — a rare fixed term the question and every passage share",
        "question": (
            "How did banks quantify the impact of the FDIC special assessment on their expenses in "
            "late 2023 and the first half of 2024?"
        ),
        "reference_answer": (
            "Capital One booked a $289 million accrual for its current estimate of the FDIC special "
            "assessment in the fourth quarter of 2023, and BNY Mellon's expenses were up 20% "
            "year-over-year on a reported basis in the same quarter, primarily reflecting the FDIC "
            "special assessment. On its second-quarter 2024 call, Bank of America noted that Q1 had "
            "included $700 million for the FDIC special assessment."
        ),
        "anchors": [
            _a("COF_2023_Q4", 2, 253, (9, 19)),
            _a("BAC_2024_Q2", 5, 3711, (8, 15)),
            _a("BK_2023_Q4", 3, 1225, (2, 12)),
        ],
        "notes": (
            "The FDIC special assessment hit nearly every large bank in the same quarter, making it the "
            "cleanest cross-bank theme in the corpus. EASY: 'FDIC special assessment' is a rare fixed "
            "phrase that BM25 should match almost perfectly, so this candidate is most useful as the "
            "control against which harder thematic items are compared. CONCERN: the three banks quantify "
            "different things — an accrual, a quarterly expense component, and a year-over-year expense "
            "move — so the answer must not imply they are like-for-like amounts."
        ),
    },
    {
        "id": "ref_them_02",
        "category": "thematic",
        "difficulty": "HARD — the question's vocabulary matches none of the passages closely",
        "question": (
            "How did banks characterise the uncertainty around the Basel III endgame proposal over "
            "2023 and 2024, and how did it affect their capital actions?"
        ),
        "reference_answer": (
            "On its third-quarter 2023 call, JPMorgan said the pace of buybacks would likely remain "
            "modest in light of Basel III. On its third-quarter 2024 call, Citi said that while "
            "uncertainty about the Basel III Endgame prevails, its capital position remains very "
            "robust."
        ),
        "anchors": [
            _a("C_2024_Q3", 2, 6420, (3, 17)),
            _a("JPM_2023_Q3", 2, 1837, (12, 24)),
        ],
        "notes": (
            "Regulatory capital uncertainty shaped buyback behaviour across the sector. HARD: the "
            "two passages register the same unresolved rule differently — Citi frames it as "
            "uncertainty against a robust capital position, JPMorgan as a concrete constraint on "
            "buybacks. CONCERN: the anchors are a year apart (2023 Q3 and 2024 Q3), so the answer "
            "describes an evolving stance rather than a single moment. A Goldman anchor was removed "
            "here to keep ref_comp_01 independent under Rule 5."
        ),
    },
    {
        "id": "ref_them_03",
        "category": "thematic",
        "difficulty": (
            "medium — the same exposure named two different ways across the passages"
        ),
        "question": "What did banks say about office and commercial real estate credit exposure during 2023?",
        "reference_answer": (
            "In the first quarter of 2023, Huntington said CRE comprises less than 2% of total loans, "
            "with the majority suburban, and in the fourth quarter of 2023 Capital One's allowance "
            "decreased by $37 million, primarily driven by the charge-offs of office real-estate "
            "loans."
        ),
        "anchors": [
            _a("COF_2023_Q4", 2, 2428, (2, 14)),
            _a("HBAN_2023_Q1", 3, 11826, (2, 14)),
        ],
        "notes": (
            "Office CRE was the sector's most-scrutinised credit risk in this window. MEDIUM: the two "
            "banks name the exposure differently -- a portfolio-share statement against an allowance "
            "movement -- so the passages share little vocabulary with each other or with a formal "
            "question. A Bank of America anchor was DROPPED here. Its sentence reads 'a reserve "
            "release of $139 million as certain troubled industries and credits outside of commercial "
            "real estate continue to have improved outlooks' -- it is a statement about everything "
            "EXCEPT commercial real estate. The answer had omitted the carve-out, which inverted the "
            "meaning: it read as though the release related to CRE. The phrase can be brought inside "
            "the anchor at words (5,19), which is contained under both configs, but only by losing "
            "'reserve' from 'reserve release' -- trading an inverted claim for a renamed metric. The "
            "sentence is off-topic for a CRE question in any case, so the anchor was removed rather "
            "than patched. CONCERN: Capital One's allowance DECREASING is driven by charge-offs, "
            "which is deterioration, not improvement; an answer framing it as good news would be "
            "unfaithful with the figure right."
        ),
    },
    {
        "id": "ref_them_04",
        "category": "thematic",
        "difficulty": "medium — same fixed term, different quantifications",
        "question": (
            "How did banks describe their progress on positive operating leverage in late 2023 and "
            "early 2024?"
        ),
        "reference_answer": (
            "Bank of America achieved 170 basis points of operating leverage in 2023, and Citi "
            "generated operating leverage in the first quarter of 2024 as its expenses decreased 4%."
        ),
        "anchors": [
            _a("BAC_2023_Q4", 2, 3750, (2, 16)),
            _a("C_2024_Q1", 4, 11534, (3, 17)),
        ],
        "notes": (
            "Operating leverage is the standard framing for whether revenue is outgrowing costs, and it "
            "recurs across 33 transcripts. MEDIUM: 'operating leverage' is a fixed phrase both anchors "
            "share, but the quantification differs (basis points of leverage versus a percentage expense "
            "decline), so the answer must not average or conflate them. Only two anchors here rather "
            "than three, because a third bank's phrasing put the metric too close to the sentence edge "
            "to anchor safely. CONCERN: 'operating leverage' appears in many chunks corpus-wide, so "
            "distractor retrievals are likely — that is a feature for testing precision, but it makes "
            "anchor coverage@5 less discriminating."
        ),
    },
    {
        "id": "ref_them_05",
        "category": "thematic",
        "difficulty": (
            "easy-medium — a shared term across two contemporaneous but differently-scoped "
            "disclosures"
        ),
        "question": (
            "How much did banks return through share repurchases in the third quarter of 2024, and "
            "how did the scale differ?"
        ),
        "reference_answer": (
            "In the third quarter of 2024, Bank of America's capital distributions included $2 "
            "billion in common dividends and the repurchase of $3.5 billion, while Citi returned $2.1 "
            "billion in the form of common dividends and share repurchases."
        ),
        "anchors": [
            _a("BAC_2024_Q3", 3, 1639, (3, 16)),
            _a("C_2024_Q3", 3, 7036, (2, 13)),
        ],
        "notes": (
            "Capital return pace is a routine cross-bank comparison and was unusually topical while "
            "Basel III endgame was unresolved. EASY-MEDIUM: 'share repurchases' appears in both "
            "passages. An American Express sentence was tried and rejected because the 200-token "
            "chunk boundary falls between '$1.9' and 'billion', leaving no span that carries a "
            "complete figure. CONCERN: both anchors are from the third quarter of 2024, so the two "
            "amounts are contemporaneous, but they are not like-for-like -- Bank of America's figure "
            "separates dividends from repurchases while Citi's combines them, and absolute amounts "
            "ignore very different balance-sheet sizes."
        ),
    },
    {
        "id": "ref_them_06",
        "category": "thematic",
        "difficulty": "medium — a shared metric name, but incomparable business models",
        "question": "What efficiency ratio levels and targets did banks discuss across 2023 and 2024?",
        "reference_answer": (
            "Fifth Third posted an adjusted efficiency ratio of 59% in a seasonally challenged first "
            "quarter of 2023, and in the third quarter of 2024 Capital One had guided its annual "
            "operating efficiency ratio, net of adjustments, to be modestly down compared to the "
            "43.5% it posted a year earlier."
        ),
        "anchors": [
            _a("FITB_2023_Q1", 2, 440, (2, 16)),
            _a("COF_2024_Q3", 3, 5089, (5, 19)),
        ],
        "notes": (
            "Efficiency ratio is the standard cost-discipline metric and every bank quotes it. "
            "MEDIUM: the phrase is shared by question and passages. CONCERN, the important one: "
            "these ratios are NOT comparable — a card issuer and a regional bank have structurally "
            "different cost bases, so ranking them would mislead even though each figure is "
            "correct. A Goldman anchor was dropped here: its sentence states the ratio value "
            "(60.9%) inside the edge margin, so no valid span carries it, and an answer without a "
            "value would not answer the question (Rules 2, 3 and 8 could not all hold)."
        ),
    },
    {
        "id": "ref_them_07",
        "category": "thematic",
        "difficulty": "medium — one metric reported on two different bases",
        "question": (
            "How did banks describe deposit growth in the second quarter of 2023?"
        ),
        "reference_answer": (
            "In the second quarter of 2023, Huntington's deposits increased by $2.7 billion or 1.9%, "
            "and Fifth Third's total period-end deposits increased 1% sequentially and 2% "
            "year-over-year."
        ),
        "anchors": [
            _a("HBAN_2023_Q2", 3, 277, (2, 10)),
            _a("FITB_2023_Q2", 2, 1749, (2, 16)),
        ],
        "notes": (
            "Deposit gathering was the competitive battleground of this period. MEDIUM: both banks "
            "report growth but on different bases -- an absolute sequential increase against "
            "period-end balances measured two ways -- so the passages share the topic without sharing "
            "vocabulary. A Capital One anchor was DROPPED here: it reads 'quarter at approximately "
            "$49 billion, up about $4 billion from the prior quarter' and never says what the figure "
            "is a balance OF. The source calls it a cash position, but that phrase falls outside the "
            "anchor, so any answer naming it would import a characterisation Rule 2 forbids, and "
            "leaving it unnamed fails the read-aloud test. With that anchor gone both remaining "
            "anchors are from 2023 Q2, so the question now names that quarter rather than the full "
            "two-year span. CONCERN: Huntington's anchor does not contain the word 'deposit' at all "
            "-- it opens the sentence, outside the anchor -- so the question supplies the metric."
        ),
    },
    # -------------------------------------------------------------- comparative
    {
        "id": "ref_comp_01",
        "category": "comparative",
        "difficulty": "HARD — the two passages describe one rule in opposite registers",
        "question": (
            "How did Goldman Sachs and Citi differ in how they characterised Basel III endgame "
            "uncertainty in late 2023 and early 2024?"
        ),
        "reference_answer": (
            "On its fourth-quarter 2023 call, Goldman Sachs said it was taking a more conservative "
            "posture given the uncertainty around Basel, while on its first-quarter 2024 call Citi "
            "pointed to how the Basel III endgame proposal could evolve, but that it hasn't."
        ),
        "anchors": [
            _a("GS_2023_Q4", 53, 879, (4, 18)),
            _a("C_2024_Q1", 25, 613, (12, 22)),
        ],
        "notes": (
            "THE DIFFERENCE: Goldman turns the unresolved rule into defensive action, constraining its "
            "own posture now, while Citi treats it as still open and pending — acting versus waiting on "
            "the same regulation. HARD: both anchors are Q&A and from adjacent quarters (2023 Q4 and "
            "2024 Q1), and only one of them contains the phrase 'Basel III endgame' — the Goldman anchor "
            "ends at 'Basel' — so lexical retrieval alone is unlikely to return both sides. Under "
            "fractional coverage that costs roughly half the score rather than all of it, which is "
            "exactly the discrimination the graded rule buys. CONCERN: the contrast is softer than it "
            "first looks. Citi's more clearly optimistic wording ('favorable things') sits in a different "
            "200-token chunk from 'Basel III endgame' and could not be anchored; and because the quarters "
            "differ, part of the difference may be timing rather than genuine disagreement."
        ),
    },
    {
        "id": "ref_comp_02",
        "category": "comparative",
        "difficulty": "medium — same quarter, one prepared-remarks and one Q&A anchor",
        "question": "How did Bank of America's and Huntington's positions on office real estate exposure differ in the first quarter of 2024?",
        "reference_answer": (
            "In the first quarter of 2024, Bank of America's charge-offs increased $191 million "
            "versus the fourth quarter, driven by commercial real estate losses, while Huntington cut "
            "the office portfolio by about $500 million over the course of the last four quarters."
        ),
        "anchors": [
            _a("BAC_2024_Q1", 3, 11086, (2, 15)),
            _a("HBAN_2024_Q1", 55, 37, (2, 14)),
        ],
        "notes": (
            "THE DIFFERENCE: Bank of America is absorbing realised losses from office exposure, whereas "
            "Huntington had been actively shrinking the portfolio ahead of the stress — a reactive versus "
            "pre-emptive posture on the same risk. MEDIUM: same quarter, so the comparison is clean, but "
            "one anchor is prepared remarks and the other Q&A, and they share no distinctive phrase "
            "beyond 'office'. CONCERN: the two are not strictly like-for-like — a charge-off figure "
            "versus a portfolio reduction — so an answer implying Huntington had lower losses would be "
            "unsupported; the anchors say nothing about Huntington's losses."
        ),
    },
    {
        "id": "ref_comp_03",
        "category": "comparative",
        "difficulty": "medium — same quarter, structurally incomparable ratios",
        "question": "How did Fifth Third's and Goldman Sachs's efficiency ratios compare in the second quarter of 2024?",
        "reference_answer": (
            "In the second quarter of 2024, Fifth Third still projects an efficiency ratio of around "
            "57%, while Goldman Sachs's year-to-date efficiency ratio at 63.8% is nearly 10 points "
            "better."
        ),
        "anchors": [
            _a("FITB_2024_Q2", 3, 11284, (2, 9)),
            _a("GS_2024_Q2", 26, 101, (2, 11)),
        ],
        "notes": (
            "THE DIFFERENCE: Fifth Third is guiding to a stable ratio, while Goldman is reporting a much "
            "higher one that is improving very fast — a level-versus-trajectory contrast. MEDIUM: same "
            "quarter, exact shared phrase 'efficiency ratio', one Q&A anchor. CONCERN, and it is the "
            "reason to watch this one: a regional bank and an investment bank have structurally different "
            "cost bases, so 57% versus 63.8% does not mean Fifth Third is better run. An answer drawing "
            "that conclusion would be unfaithful, which makes this a useful trap for the faithfulness "
            "check rather than a clean retrieval item."
        ),
    },
    {
        "id": "ref_comp_04",
        "category": "comparative",
        "difficulty": "HARD — same quarter, different denominators for 'deposit growth'",
        "question": (
            "How did Huntington's and Fifth Third's deposit growth differ in the third quarter of "
            "2024?"
        ),
        "reference_answer": (
            "In the third quarter of 2024, Huntington's growth continued at a robust pace, increasing "
            "by $8.3 billion or 5.6%, while Fifth Third grew retail deposits nearly 16% "
            "year-over-year."
        ),
        "anchors": [
            _a("HBAN_2024_Q3", 2, 1909, (2, 13)),
            _a("FITB_2024_Q3", 2, 2521, (2, 9)),
        ],
        "notes": (
            "THE DIFFERENCE: Huntington reports total average deposits growing 5.6%, while Fifth Third "
            "reports a much faster 16% but only in retail — the headline gap is largely a difference of "
            "denominator, not of performance. HARD: 'deposit' is one of the most common words in the "
            "corpus, so retrieval must discriminate two specific growth disclosures from hundreds of "
            "deposit mentions in the same quarter — and the Huntington anchor does not contain the word "
            "'deposit' at all, since it opens the sentence outside the anchor. CONCERN: the 5.6% versus "
            "16% contrast invites a conclusion the anchors do not support; a faithful answer must "
            "preserve 'retail' or the comparison is actively wrong."
        ),
    },
    {
        "id": "ref_comp_06",
        "category": "comparative",
        "difficulty": "medium — same quarter, same metric, different measurement basis",
        "question": "How did Bank of America and Fifth Third each describe their operating leverage in the first quarter of 2023?",
        "reference_answer": (
            "In the first quarter of 2023, Bank of America described its seventh straight quarter of "
            "operating leverage, led by 13% year-over-year revenue growth, while Fifth Third "
            "generated nine points of year-over-year positive operating leverage driven by an 18% "
            "increase in revenue."
        ),
        "anchors": [
            _a("BAC_2023_Q1", 2, 860, (2, 13)),
            _a("FITB_2023_Q1", 1, 959, (2, 13)),
        ],
        "notes": (
            "THE DIFFERENCE: Bank of America frames operating leverage as a streak — consistency over "
            "seven quarters — while Fifth Third quantifies the magnitude in a single period, nine points "
            "off 18% revenue growth. Same achievement, two different rhetorical strategies, which is "
            "itself informative about how banks present cost discipline. MEDIUM: same quarter, both "
            "prepared remarks, shared phrase 'operating leverage'. CONCERN: 'operating leverage' recurs "
            "in 33 transcripts, so distractors are plentiful; and a streak count is not comparable to a "
            "points figure, so an answer stating which bank did better would be unsupported."
        ),
    },
]

# Batch 2 deliberately fills batch 1's gaps: the five tickers absent from batch 1
# (BLK, MTB, PNC, USB, WFC), the under-used JPM/MS/BK, the 2023 Q2-Q3 and 2024 Q4
# quarters, and a much higher share of Q&A. Its comparatives are sourced
# independently -- no comparative anchor is shared with any thematic candidate in
# either batch, which build_candidate's caller asserts before writing output.
BATCH2: list[dict] = [
    # ------------------------------------------------------------------ factual
    {
        "id": "ref_fact_08",
        "category": "factual",
        "difficulty": "easy — question vocabulary matches the passage almost word for word",
        "question": "How much did BlackRock report in net inflows for the first half of 2023?",
        "reference_answer": (
            "BlackRock took in $190 billion of net inflows in the first half of 2023."
        ),
        "anchors": [_a("BLK_2023_Q2", 2, 732, (2, 14))],
        "notes": (
            "Net flows are the single number an asset manager is judged on, so this is the most "
            "predictable question anyone would ask BlackRock. EASY: 'net inflows' and 'first half' "
            "both appear verbatim, so lexical and dense retrieval should behave alike — useful as a "
            "control. CONCERN: BlackRock reports flows on several bases (total, long-term, active "
            "equity, cash), and ref_fact_14 anchors a different one from the next quarter; a "
            "retriever may surface the wrong basis, and an answer that drops the qualifier would be "
            "wrong rather than merely incomplete."
        ),
    },
    {
        "id": "ref_fact_09",
        "category": "factual",
        "difficulty": "medium — answer needs both the level and the change",
        "question": "What were M&T's average loans and leases in the second quarter of 2023, and how did they move?",
        "reference_answer": (
            "M&T's average loans and leases were $133.5 billion during the second quarter of 2023, up "
            "$1.5 billion."
        ),
        "anchors": [_a("MTB_2023_Q2", 2, 6312, (2, 16))],
        "notes": (
            "Loan balances are the core volume metric for a commercial bank. MEDIUM: the anchor "
            "carries both the level and the sequential change, so a partial answer is detectably "
            "incomplete. CONCERN: M&T restates average loans in almost identical wording every "
            "quarter — 'average loans and leases were $X billion during the Nth quarter' recurs "
            "across 2023 — so retrieval must discriminate on the figure and the quarter, not the "
            "phrasing. That makes it a good probe for whether the retriever respects quarter scoping."
        ),
    },
    {
        "id": "ref_fact_10",
        "category": "factual",
        "difficulty": "medium — two signed figures that must not be swapped",
        "question": "What was PNC's AOCI position at the end of the third quarter of 2023, and what had it been at the end of the prior quarter?",
        "reference_answer": (
            "PNC's AOCI was a negative $10.3 billion at the end of the third quarter of 2023, "
            "compared with a negative $9.5 billion at June 30."
        ),
        "anchors": [_a("PNC_2023_Q3", 2, 481, (2, 16))],
        "notes": (
            "Unrealised securities losses were the defining balance-sheet issue for regional banks "
            "in 2023, so AOCI is exactly what an analyst chases. MEDIUM: both figures are negative "
            "and close together, so an answer that swaps them or drops the sign is wrong in a way "
            "that is easy to miss — good material for the faithfulness check. CONCERN: AOCI moving "
            "from -$9.5bn to -$10.3bn is a deterioration; an answer describing it as an increase "
            "would be literally true of the magnitude and misleading about the direction."
        ),
    },
    {
        "id": "ref_fact_11",
        "category": "factual",
        "difficulty": "easy — distinctive phrasing, single figure",
        "question": "What proportion of U.S. Bancorp's total net revenue did fee income represent in the fourth quarter of 2024?",
        "reference_answer": (
            "U.S. Bancorp's fee income represented over 40% of total net revenue in the fourth "
            "quarter of 2024."
        ),
        "anchors": [_a("USB_2024_Q4", 2, 1640, (2, 12))],
        "notes": (
            "Fee-income mix is central to U.S. Bancorp's equity story as spread income compressed. "
            "EASY: 'fee income' and 'total net revenue' both appear in the anchor. CONCERN: the "
            "figure is 'over 40%', not a point estimate — an answer that reports exactly 40% would "
            "be a subtle misstatement, which is precisely the kind of slip worth catching."
        ),
    },
    {
        "id": "ref_fact_12",
        "category": "factual",
        "difficulty": "medium — the anchor stops before what the growth offset",
        "question": "How fast did Wells Fargo's fee-based revenue grow in 2024?",
        "reference_answer": (
            "In 2024, Wells Fargo's fee-based revenue growth was up 15% from a year ago."
        ),
        "anchors": [_a("WFC_2024_Q4", 2, 1475, (2, 14))],
        "notes": (
            "Wells Fargo's pivot toward fee income while NII fell was the year's central narrative "
            "for the bank. MEDIUM: 'fee-based revenue growth' is distinctive, but the question asks "
            "only about the growth rate because the anchor ends at 'largely offset' — what it "
            "offset (the expected decline in net interest income) is in the same sentence but "
            "outside the anchor. CONCERN: this is a candidate where a fuller and more useful "
            "question exists but cannot be anchored within the edge margin; the narrower question "
            "is the honest one."
        ),
    },
    {
        "id": "ref_fact_13",
        "category": "factual",
        "difficulty": "medium — two contradictory-looking growth rates in one answer",
        "question": "What was JPMorgan's investment banking revenue in the second quarter of 2023, and how did it change year-on-year?",
        "reference_answer": (
            "JPMorgan's investment banking revenue of $1.5 billion in the second quarter of 2023 was "
            "up 11% year-on-year, or down 7% excluding bridge book markdowns in the prior year."
        ),
        "anchors": [_a("JPM_2023_Q2", 1, 6976, (2, 16))],
        "notes": (
            "Investment banking revenue in a weak deal year, with a base-effect adjustment, is a "
            "standard analyst question. MEDIUM: the anchor holds a headline growth rate and an "
            "adjusted one that points the opposite way, so an answer quoting only '+11%' is "
            "materially misleading even though the number is right. CONCERN: this is the strongest "
            "faithfulness test in the factual set — the correct answer must carry both figures and "
            "the reason they differ."
        ),
    },
    {
        "id": "ref_fact_14",
        "category": "factual",
        "difficulty": "medium — Q&A sourced, narrower flow basis than the headline",
        "question": "How much did BlackRock report in active equity net inflows on its third-quarter 2023 call?",
        "reference_answer": (
            "BlackRock reported over $30 billion in active equity net inflows on its third-quarter "
            "2023 call."
        ),
        "anchors": [_a("BLK_2023_Q3", 24, 189, (2, 15))],
        "notes": (
            "Q&A-SOURCED. Active equity flows were a contested point for BlackRock given industry "
            "outflows from active management, and the figure surfaces only in the Q&A. MEDIUM: "
            "'active equity net inflows' is distinctive, but sits inside conversational text. "
            "CONCERN: BlackRock quotes several flow figures across 2023 on different bases — see "
            "ref_fact_08 — and this one is deliberately a narrower slice than the headline. An "
            "answer that reports it as total net inflows would be wrong."
        ),
    },
    # ----------------------------------------------------------------- thematic
    {
        "id": "ref_them_08",
        "category": "thematic",
        "difficulty": "medium — one Q&A anchor, three different measures of the same idea",
        "question": "How did firms describe client asset and net inflow momentum during 2023?",
        "reference_answer": (
            "BlackRock generated total net inflows of $110 billion in the first quarter of 2023, and "
            "by the second quarter of 2023 had seen an $830 billion increase over the first half of "
            "the year. In the third quarter of 2023, JPMorgan reported a 21% year-on-year increase "
            "driven by market performance and strong net inflows."
        ),
        "anchors": [
            _a("BLK_2023_Q1", 2, 3213, (2, 16)),
            _a("JPM_2023_Q3", 2, 7787, (5, 19)),
            _a("BLK_2023_Q2", 20, 913, (2, 16)),
        ],
        "notes": (
            "Asset gathering is the shared scoreboard for firms with wealth and asset management "
            "arms, and it is untouched by batch 1. MEDIUM: 'net inflows' is a fixed phrase in two "
            "of three anchors; the third is conversational Q&A. CONCERN — the important one: the "
            "three figures are NOT the same measure. $110 billion is a quarterly flow, $830 billion "
            "is a half-year change in AUM including market movement, and 21% is a year-on-year "
            "change in client assets. An answer that lists them as comparable inflow figures would "
            "be wrong; the question asks how firms described momentum, not who gathered most."
        ),
    },
    {
        "id": "ref_them_09",
        "category": "thematic",
        "difficulty": "easy to retrieve, hard to answer faithfully — incomparable margins",
        "question": (
            "What net interest margin levels did banks report in 2023 and 2024, on reported and "
            "adjusted bases, and which way were they moving?"
        ),
        "reference_answer": (
            "PNC's net interest margin was 2.84% in the first quarter of 2023, down 8 basis points "
            "reflecting increased funding costs; Capital One's net interest margin was 6.69% in the "
            "third quarter of 2023, 21 basis points higher than the prior quarter; and Fifth Third's "
            "adjusted net interest margin improved 3 basis points in the second quarter of 2024."
        ),
        "anchors": [
            _a("PNC_2023_Q1", 2, 2273, (2, 15)),
            _a("COF_2023_Q3", 2, 3454, (2, 16)),
            _a("FITB_2024_Q2", 3, 1441, (2, 9)),
        ],
        "notes": (
            "NIM is the most-quoted profitability metric in banking. EASY to retrieve -- the phrase "
            "is shared by question and passages -- but hard to answer faithfully. CONCERN, and the "
            "reason this candidate earns its place: a card issuer's 6.69% and a regional bank's 2.84% "
            "are not on the same scale, so an answer ranking or averaging them is unfaithful with "
            "every figure correct. A SECOND, subtler mismatch: Fifth Third's figure is an ADJUSTED "
            "margin while PNC's and Capital One's are reported. The word 'adjusted' opens the Fifth "
            "Third sentence at word index 1, inside the edge margin, so no valid span carries it; the "
            "question was widened to cover reported and adjusted bases so the clause can name its "
            "own. All three anchors are management-spoken prepared remarks."
        ),
    },
    {
        "id": "ref_them_10",
        "category": "thematic",
        "difficulty": "medium — a loosely-worded Q&A answer against a formal question",
        "question": (
            "What did banks say about credit card growth and card credit performance over 2023 and "
            "2024?"
        ),
        "reference_answer": (
            "Bank of America's card net charge-off rate rose 12 basis points to 2.72% in the third "
            "quarter of 2023. In the first quarter of 2024, Wells Fargo said its product offerings "
            "continue to drive strong credit card spend, up approximately $5 billion or 14%, and in "
            "the second quarter of 2024 U.S. Bancorp described a card growth rate of about 1%."
        ),
        "anchors": [
            _a("BAC_2023_Q3", 3, 12571, (4, 18)),
            _a("USB_2024_Q2", 80, 0, (2, 16)),
            _a("WFC_2024_Q1", 2, 4345, (2, 16)),
        ],
        "notes": (
            "Card credit normalisation was a running theme across issuers. MEDIUM: one anchor is a "
            "loosely-worded Q&A answer from the CFO ('the card growth rate was about 1% or so'), so "
            "the gap between a formal question and the passage is wide. CONCERN: the three cover "
            "different things — a loss rate, a growth rate and a spend figure — and cannot be "
            "compared to each other."
        ),
    },
    {
        "id": "ref_them_11",
        "category": "thematic",
        "difficulty": "medium — a realised level against a forward expectation",
        "question": (
            "How did banks characterise their net charge-off levels and direction in 2023 and 2024?"
        ),
        "reference_answer": (
            "M&T's net charge-offs were $127 million in the second quarter of 2023, compared to $70 "
            "million earlier that year. In the second quarter of 2024, Bank of America repeated its "
            "expectation that net charge-offs in the second half of 2024 would be lower than the "
            "first half, and U.S. Bancorp said it anticipated approaching 60 basis points in the back "
            "half of the year."
        ),
        "anchors": [
            _a("MTB_2023_Q2", 2, 12149, (3, 15)),
            _a("BAC_2024_Q2", 2, 11822, (4, 18)),
            _a("USB_2024_Q2", 29, 228, (2, 20)),
        ],
        "notes": (
            "Charge-off trajectory is the cleanest read on credit deterioration. MEDIUM: 'net "
            "charge-offs' is shared by question and passages, but the anchors are a realised level, a "
            "forward expectation and a Q&A guide, so the answer must not present them as one series. "
            "The U.S. Bancorp anchor is 19 words and exists only because Q&A anchors may now run to "
            "20 — the old 15-word ceiling admitted no valid span in that sentence. CONCERN: an "
            "earlier M&T anchor was dropped under Rule 2, having ended on the word 'not' with no "
            "valid span carrying the clause it qualified."
        ),
    },
    {
        "id": "ref_them_12",
        "category": "thematic",
        "difficulty": "HARD — one Q&A anchor carrying strategy language rather than metrics",
        "question": (
            "What did firms say during 2023 about their wealth management businesses and the "
            "investment behind them?"
        ),
        "reference_answer": (
            "In the third quarter of 2023, BNY Mellon's wealth management revenue decreased by 5%, "
            "driven by lower net interest revenue, while Morgan Stanley said it decided to keep "
            "investing through the cycle on the funnel and wealth."
        ),
        "anchors": [
            _a("BK_2023_Q3", 3, 9769, (2, 16)),
            _a("MS_2023_Q3", 7, 1530, (3, 12)),
        ],
        "notes": (
            "Wealth management is where BNY Mellon and Morgan Stanley genuinely compete. HARD: the "
            "Morgan Stanley anchor is Q&A strategy language rather than a reported metric, so a "
            "financially-worded question has little vocabulary overlap with it — one of the better "
            "dense-versus-sparse discriminators here, and it survives only because Q&A anchors may "
            "now run to 20 words. CONCERN: a revenue decline and an investment posture are different "
            "kinds of claim and should not be summarised as one trend. A third anchor was dropped "
            "under Rule 1 with no management alternative passing containment."
        ),
    },
    {
        "id": "ref_them_13",
        "category": "thematic",
        "subtype": "temporal",
        "difficulty": "easy retrieval — a multi-quarter trajectory in near-identical wording",
        "question": "How did BNY Mellon describe growth in its ETF servicing business through 2023 and 2024?",
        "reference_answer": (
            "BNY Mellon's ETF Assets Under Custody/Administration were up over 20% year-over-year in "
            "the third quarter of 2023. By the second quarter of 2024, ETF servicing AUC/A had "
            "reached over $2 trillion, up more than 50%, and in the third quarter of 2024 it stood at "
            "$2.7 trillion, up more than 70% year-on-year."
        ),
        "anchors": [
            _a("BK_2023_Q3", 3, 6161, (2, 16)),
            _a("BK_2024_Q2", 3, 3864, (4, 18)),
            _a("BK_2024_Q3", 3, 4298, (3, 16)),
        ],
        "notes": (
            "SUBTYPE: temporal. Unlike every other thematic, this one spans a single company "
            "across three quarters rather than several companies — kept deliberately and labelled "
            "rather than replaced, because near-identical wording recurs each quarter and this is "
            "the only candidate that tests whether retrieval discriminates on PERIOD rather than "
            "topic, which is the exact failure mode the corpus's quarter-scoping rule exists to "
            "prevent. Rule 4 allows it only because it carries this label. EASY to retrieve: "
            "'ETF' plus 'AUC/A' is a rare pairing. CONCERN: the 2023 anchor gives a growth rate "
            "with no level, so the three are not a clean series, and an answer implying continuous "
            "acceleration reads a trend into three points."
        ),
    },
    {
        "id": "ref_them_14",
        "category": "thematic",
        "difficulty": (
            "medium — one shared fee line, but a level in one period against percentage moves in "
            "another"
        ),
        "question": "What did banks report about investment banking revenue and fees across 2023 and 2024?",
        "reference_answer": (
            "Goldman Sachs's investment banking fees of $1.7 billion fell 12% year-over-year in the "
            "fourth quarter of 2023. In the third quarter of 2024, Citi's investment banking fees "
            "were up 44%, driven by investment-grade debt issuance, and Bank of America grew "
            "investment banking fees 18% year-over-year while sales and trading revenue increased 12% "
            "year-over-year."
        ),
        "anchors": [
            _a("GS_2023_Q4", 2, 837, (2, 16)),
            _a("C_2024_Q3", 2, 3829, (2, 16)),
            _a("BAC_2024_Q3", 2, 3264, (2, 16)),
        ],
        "notes": (
            "Investment banking fees are the standard cyclical read on capital markets activity. "
            "MEDIUM: the phrase is shared by the question and all three passages. REBUILT: this "
            "candidate previously used two JPMorgan anchors whose source sentences say GROSS "
            "investment banking revenue -- a segment-level figure -- while the word 'gross' sits at "
            "word index 1 and 0 of those sentences, inside the edge margin, so no valid span could "
            "carry it. The gold answer was therefore stating a segment figure as firmwide, the exact "
            "error the notes warned about. Both JPMorgan anchors were dropped and the candidate "
            "rebuilt on Goldman Sachs, Citi and Bank of America, all of which report a firmwide "
            "'investment banking fees' line with no scope qualifier outside the anchor. CONCERN: the "
            "three are still not directly comparable -- Goldman's is a level that FELL 12% in late "
            "2023, while Citi's and Bank of America's are percentage increases from 2024, so the "
            "answer must not read as one trend."
        ),
    },
    {
        "id": "ref_them_15",
        "category": "thematic",
        "difficulty": "medium — a distinctive shared term, but three incompatible spend measures",
        "question": (
            "How much did banks say they were spending on technology over 2023 and 2024, and how did "
            "that spend change?"
        ),
        "reference_answer": (
            "Citi's technology spend was $3 billion in the second quarter of 2023, up 13%. In the "
            "second quarter of 2024, Bank of America increased its technology initiatives and expects "
            "to spend nearly $4 billion on technology initiatives, while BlackRock's expenses were up "
            "7% year-over-year, primarily due to the timing of technology spend in the prior year."
        ),
        "anchors": [
            _a("C_2023_Q2", 3, 2727, (3, 17)),
            _a("BAC_2024_Q2", 2, 6412, (3, 16)),
            _a("BLK_2024_Q2", 3, 6766, (3, 17)),
        ],
        "notes": (
            "Technology and AI spending is a genuine cross-bank theme in this window and is untouched "
            "by every other thematic in the set. CHUNK-SIZE SENSITIVE: the BlackRock source sentence "
            "splits across two chunks at 200 tokens but sits whole in one at 500, so the spend "
            "attribution and the expense movement it explains are only jointly retrievable at the "
            "larger chunk size -- one of the few candidates that probes the independent variable "
            "directly. CONCERN, and it is the sharp one: the three figures are NOT comparable "
            "measures. Citi's $3 billion is a QUARTERLY spend, Bank of America's nearly $4 billion is "
            "a FULL-YEAR expectation, and BlackRock's 7% is a G&A expense movement attributed to "
            "timing rather than a spend level at all. An answer that ranks these would be confidently "
            "wrong with every figure copied correctly. The anchors run from 2023 Q2 to 2024 Q2, which "
            "is the span the question states."
        ),
    },
    # -------------------------------------------------------------- comparative
    {
        "id": "ref_comp_07",
        "category": "comparative",
        "difficulty": "medium — same quarter, action versus outcome",
        "question": "How did PNC and U.S. Bancorp each frame their 2024 expense plans on their third-quarter 2023 calls?",
        "reference_answer": (
            "On their third-quarter 2023 calls, PNC had begun executing on staff reductions which "
            "will reduce its 2024 expenses by $325 million, while U.S. Bancorp said that on a core "
            "basis it expected full year 2024 expenses to be flat."
        ),
        "anchors": [
            _a("PNC_2023_Q3", 1, 1758, (5, 19)),
            _a("USB_2023_Q3", 3, 4773, (2, 12)),
        ],
        "notes": (
            "THE DIFFERENCE: PNC names a specific action — headcount reduction — with a quantified "
            "saving attached, whereas U.S. Bancorp gives an outcome target with no mechanism. Same "
            "cost pressure, one answered with a lever and one with a promise. MEDIUM: same quarter, "
            "both prepared remarks, and 'expenses' is common enough that retrieval must find two "
            "specific forward statements among many mentions. CONCERN: $325 million of savings and "
            "'flat with 2023' are not comparable quantities — one is a delta, the other a level — "
            "so an answer concluding PNC was cutting harder is unsupported without knowing the "
            "bases. U.S. Bancorp's 'core basis' qualifier also matters and must survive into any "
            "answer."
        ),
    },
    {
        "id": "ref_comp_08",
        "category": "comparative",
        "difficulty": "HARD — same quarter, same metric, different basis and different period",
        "question": "How did M&T and Fifth Third each describe tangible book value per share in the third quarter of 2023?",
        "reference_answer": (
            "In the third quarter of 2023, M&T reported return on tangible common equity of 17.41% "
            "and tangible book value per share increased 3% compared to the end of June, while Fifth "
            "Third's tangible book value per share, excluding AOCI, increased 10% compared to the "
            "year ago quarter."
        ),
        "anchors": [
            _a("MTB_2023_Q3", 2, 3909, (2, 16)),
            _a("FITB_2023_Q3", 3, 7770, (2, 13)),
        ],
        "notes": (
            "THE DIFFERENCE: both banks report tangible book value per share growing, but on "
            "incompatible bases — M&T sequentially and including AOCI, Fifth Third year-over-year "
            "and *excluding* AOCI, which is precisely the line item that was destroying regional "
            "bank book value in 2023. Fifth Third's exclusion flatters the number by removing the "
            "problem. HARD: same quarter and a shared fixed phrase, so retrieval is tractable, but "
            "a faithful answer must carry both qualifiers. CONCERN — this is the sharpest trap in "
            "batch 2: 3% versus 10% invites the conclusion that Fifth Third grew book value faster, "
            "which the anchors do not support at all. Neither the periods nor the bases match."
        ),
    },
    {
        "id": "ref_comp_09",
        "category": "comparative",
        "difficulty": "medium — adjacent quarters, growth in different portfolios",
        "question": "How did M&T's and JPMorgan's loan growth expectations differ on their late-2024 calls?",
        "reference_answer": (
            "On its third-quarter 2024 call, M&T expected average total loans of approximately $136 "
            "billion with growth in C&I and consumer, while on its fourth-quarter 2024 call JPMorgan "
            "expected card loan growth again this year but below the 12% pace it saw in 2024."
        ),
        "anchors": [
            _a("MTB_2024_Q3", 2, 12160, (6, 20)),
            _a("JPM_2024_Q4", 1, 8167, (3, 17)),
        ],
        "notes": (
            "THE DIFFERENCE: M&T expects growth through a mix shift — C&I and consumer up, CRE down "
            "— while JPMorgan expects its card book to keep growing but decelerate. One is "
            "repositioning, the other is normalising after a fast year. MEDIUM: adjacent quarters "
            "(2024 Q3 and Q4), both prepared remarks, both use 'loan growth' verbatim. CONCERN: the "
            "two are about different portfolios, so this is not a like-for-like comparison of loan "
            "growth rates — an answer that contrasts '$136 billion' against '12%' as if they were "
            "the same kind of guidance would be meaningless. Both are also forward statements, so "
            "the question must be phrased as expectations, not results."
        ),
    },
    {
        "id": "ref_comp_10",
        "category": "comparative",
        "difficulty": "medium — adjacent quarters, the same exclusion for different purposes",
        "question": (
            "How did PNC and Fifth Third each treat AOCI when describing their capital and tangible "
            "book value per share during 2023?"
        ),
        "reference_answer": (
            "In the first quarter of 2023, PNC said that as a Category 3 institution it does not "
            "include AOCI in its CET1 ratio, while noting it understood the focus on that ratio with "
            "AOCI included. In the second quarter of 2023, Fifth Third reported tangible book value "
            "per share, excluding AOCI, increasing 11% compared to the year ago quarter."
        ),
        "anchors": [
            _a("PNC_2023_Q1", 2, 10488, (2, 16)),
            _a("FITB_2023_Q2", 3, 6155, (2, 13)),
        ],
        "notes": (
            "THE DIFFERENCE: both banks set AOCI aside, but for different reasons and in different "
            "measures -- PNC because regulation permits the exclusion from CET1 for its category, "
            "Fifth Third as a presentational choice in a tangible book value metric. PNC also "
            "acknowledges the scrutiny; Fifth Third simply presents the adjusted figure. MEDIUM: "
            "adjacent quarters, and 'AOCI' is a rare, highly distinctive token, so retrieval should "
            "be reliable. NOTE: the question names tangible book value per share explicitly. The "
            "Fifth Third anchor says only 'book value per share, excluding AOCI', but the source "
            "metric is the tangible one, and dropping the qualifier would name a different figure -- "
            "tangible book value excludes goodwill and intangibles. The question licenses the word. "
            "CONCERN: a regulatory exclusion and a presentational one are easy to conflate; an answer "
            "implying both banks were doing the same thing would misrepresent PNC's, which is a rule "
            "rather than a choice."
        ),
    },
    {
        "id": "ref_comp_11",
        "category": "comparative",
        "difficulty": "HARD — same quarter, same direction, completely different cause",
        "question": (
            "What drove the fall in BNY Mellon's reported expenses and M&T's non-interest expenses in "
            "the third quarter of 2023?"
        ),
        "reference_answer": (
            "In the third quarter of 2023, BNY Mellon's expense decline was on a reported basis, "
            "primarily reflecting the goodwill impairment associated with its investment management "
            "reporting unit, while M&T's non-interest expenses were $1.28 billion, down $15 million."
        ),
        "anchors": [
            _a("BK_2023_Q3", 3, 1082, (6, 20)),
            _a("MTB_2023_Q3", 2, 9021, (3, 14)),
        ],
        "notes": (
            "THE DIFFERENCE, and it is the whole point: BNY Mellon's decline is a base effect -- the "
            "prior-year quarter carried a goodwill impairment, so the comparison flatters it rather "
            "than reflecting cost discipline. M&T's $15 million decline is a genuine sequential "
            "reduction. Same headline direction, opposite substance. HARD: the question asks what "
            "drove each, so an answer must surface the impairment rather than reporting both as cost "
            "reductions. NOTE: 'Non-interest' opens the M&T sentence at word index 0, inside the edge "
            "margin, so the anchor cannot carry it; the question names the line explicitly instead, "
            "which is what licenses the word in the answer. CONCERN: this is the candidate most "
            "likely to produce a fluent, well-sourced, wrong answer."
        ),
    },
    {
        "id": "ref_comp_12",
        "category": "comparative",
        "difficulty": "medium — adjacent quarters, margins on incomparable scales",
        "question": "How did PNC's and Capital One's net interest margins compare and move in 2024?",
        "reference_answer": (
            "PNC's net interest income declined by $139 million or 4% in the first quarter of 2024 "
            "and its net interest margin was 2.57%, while Capital One's net interest margin was 6.7% "
            "in the second quarter of 2024, 1 basis point higher than the prior quarter."
        ),
        "anchors": [
            _a("PNC_2024_Q1", 3, 5616, (2, 15)),
            _a("COF_2024_Q2", 2, 3096, (2, 16)),
        ],
        "notes": (
            "THE DIFFERENCE: PNC's margin is compressing under funding costs while Capital One's is "
            "essentially flat at more than double the level — a spread-lending balance sheet against "
            "a card book. MEDIUM: adjacent quarters, 'net interest margin' verbatim in both. "
            "CONCERN: 2.57% and 6.7% are not comparable and never will be; a card issuer's margin "
            "reflects card yields against deposit funding. This shares a topic with ref_them_09 but "
            "no anchors with it — all four sentences are distinct, from four different transcripts "
            "— so the categories stay independent even though the subject recurs. If you would "
            "rather they not overlap at all, this is the candidate to swap."
        ),
    },
]

CANDIDATES: list[dict] = [{**spec, "batch": 1} for spec in BATCH1] + [
    {**spec, "batch": 2} for spec in BATCH2
]


# ---------------------------------------------------------------------------
# Batch 3: unanswerable candidates
#
# These were skipped in batches 1 and 2 because absence could not be asserted.
# They are included now because absence is PROVEN mechanically at build time:
# verify_absence() re-runs every search term over all 128 frozen transcripts and
# fails the build if any term occurs even once. A candidate that turned out to be
# partially answerable would make a correct abstention score as a failure, which
# is worse than having no unanswerable questions at all.
#
# They carry no anchors and no transcript_ids: evaluate.py excludes them from
# anchor_coverage_at_5 and MRR entirely (both return None) and scores them only
# on an exact match against generate.ABSTENTION.
#
# `expected_retrieval` records what a real dense retriever (bge-small over the
# 200-token chunking, top-5) actually returns for each question -- not a guess.
# A question whose distractors are irrelevant tests nothing, because abstaining
# is then trivial; one candidate was rejected on exactly that ground.
# ---------------------------------------------------------------------------

UNANSWERABLE: list[dict] = [
    {
        "id": "ref_unans_01",
        "absence_type": "out_of_corpus_company",
        "question": (
            "What were Northern Trust's assets under custody and administration, and how did they "
            "change year-over-year?"
        ),
        "reference_answer": (
            "ABSTAIN — Northern Trust is not one of the 16 banks in the frozen corpus, and it is "
            "never mentioned in any of the 128 transcripts, so no assets-under-custody figure for "
            "it exists to retrieve."
        ),
        "search_terms": ["Northern Trust", "NTRS", "Northern"],
        "expected_retrieval": (
            "Custody-bank AUC/A passages from the wrong company: BK_2023_Q1 carries the literal "
            "phrase 'Firm-wide assets under custody and/or administration', with further BK_2023_Q3 "
            "asset-servicing chunks and MS asset-management revenue alongside it."
        ),
        "notes": (
            "The most tempting shape of out-of-corpus question: Northern Trust is a direct custody "
            "peer of BNY Mellon and State Street, and AUC/A is the exact metric both report every "
            "quarter. Retrieval returns a chunk containing the metric name verbatim, so the "
            "generator must notice the COMPANY is wrong rather than that evidence is missing. "
            "VERIFIED: the bare token 'Northern' returns zero across all 128 transcripts, so there "
            "is no competitor mention, no acquisition reference and no analyst affiliation to leak "
            "a partial answer."
        ),
    },
    {
        "id": "ref_unans_02",
        "absence_type": "out_of_corpus_company",
        "question": (
            "How did Comerica's net interest margin move during the quarter, and what did management "
            "attribute the change to?"
        ),
        "reference_answer": (
            "ABSTAIN — Comerica is not among the 16 banks in the frozen corpus and appears nowhere "
            "in the 128 transcripts, so it has no reported net interest margin here."
        ),
        "search_terms": ["Comerica", "CMA"],
        "expected_retrieval": (
            "Confident NIM disclosures from the wrong banks: COF_2024_Q4 ('our fourth quarter net "
            "interest margin was 7.03%'), USB_2023_Q3 ('net interest margin declined 9 basis points "
            "to 2.81%'), plus HBAN and USB margin commentary."
        ),
        "notes": (
            "Comerica is a mid-cap commercial bank of the same type as M&T, Huntington and Fifth "
            "Third, and NIM is reported by all of them, so the retrieved chunks are the right metric "
            "at the wrong institution — several carry a precise percentage, which is exactly the "
            "material a generator is most likely to lift. VERIFIED: both 'Comerica' and the ticker "
            "'CMA' return zero. CONCERN: 'CMA' is a short token that could in principle appear as an "
            "acronym for something else; it does not appear at all, so the risk did not materialise."
        ),
    },
    {
        "id": "ref_unans_03",
        "absence_type": "out_of_range_period",
        "question": "What net interest margin did PNC report for the second quarter of 2021?",
        "reference_answer": (
            "ABSTAIN — the corpus covers calls from 2023 Q1 to 2024 Q4 only. PNC's second-quarter "
            "2021 results are never reported or referred to in any transcript."
        ),
        "search_terms": [
            "second quarter of 2021", "second quarter 2021", "Q2 2021", "2Q 2021", "2Q21", "1Q21",
        ],
        "expected_retrieval": (
            "PNC's own material from the wrong year, led by PNC_2023_Q2 whose text opens 'PNC "
            "reported a solid second quarter 2023', followed by PNC_2024_Q1 and PNC_2024_Q2 "
            "portfolio and fee-income chunks."
        ),
        "notes": (
            "The hardest candidate in the set, and the one that tests the adjacent-period trap "
            "directly. The COMPANY is in the corpus, the METRIC is reported every quarter, and the "
            "quarter-of-year matches — only the year is out of range. The top hit is PNC's own "
            "second-quarter call from 2023, so a generator that pattern-matches on 'PNC' plus "
            "'second quarter' will answer confidently with the wrong year's figure. VERIFIED: the "
            "bare token '2021' does occur 81 times corpus-wide as a backward comparative, which is "
            "precisely why the search terms are quarter-specific — every phrasing of 'Q2 2021' "
            "returns zero, so no backward reference reaches this specific period."
        ),
    },
    {
        "id": "ref_unans_05",
        "absence_type": "absent_topic",
        "question": (
            "What did banks report about the size and credit performance of their reverse mortgage "
            "portfolios?"
        ),
        "reference_answer": (
            "ABSTAIN — reverse mortgages are never discussed in any of the 128 transcripts. The "
            "corpus covers residential and commercial lending, but not this product."
        ),
        "search_terms": ["reverse mortgage"],
        "expected_retrieval": (
            "Loan-portfolio credit disclosures that are adjacent but about other products: "
            "WFC_2023_Q2 allowance for credit losses on the total portfolio, WFC_2023_Q3 office "
            "loans as a share of total loans, and GS_2023_Q2 total loan portfolio of $178 billion."
        ),
        "notes": (
            "Replaced an earlier stablecoin candidate that was REJECTED for being too easy: its "
            "top-5 returned operator transitions and travel commentary, nothing topically related, "
            "so abstaining would have been trivial. This one behaves as intended — retrieval "
            "returns real loan-portfolio size and credit-performance passages, so the generator has "
            "to notice the PRODUCT is absent while the surrounding vocabulary matches. CONCERN: "
            "mortgage lending broadly IS covered, so an answer that generalises from residential "
            "mortgage disclosures would look plausible; that is the failure this candidate is "
            "designed to catch."
        ),
    },
    {
        "id": "ref_unans_06",
        "absence_type": "absent_topic",
        "question": "How did banks describe the results of their climate risk stress testing?",
        "reference_answer": (
            "ABSTAIN — climate risk stress testing is not discussed anywhere in the corpus. The "
            "transcripts cover regulatory capital stress testing (CCAR), but not climate scenarios."
        ),
        "search_terms": [
            "climate stress test", "climate scenario", "climate risk", "climate-related",
            "physical risk", "net zero",
        ],
        "expected_retrieval": (
            "Regulatory stress-testing material of a different kind: JPM_2023_Q1 discussing the "
            "CCAR stress test directly, COF_2024_Q2 on the Federal Reserve releasing stress test "
            "results and its stress capital buffer, and GS_2024_Q2 on the Fed and returns."
        ),
        "notes": (
            "The near-miss is unusually tight: 'stress test' is heavily covered, so retrieval "
            "returns confident, on-vocabulary passages about CCAR — the generator must distinguish "
            "the TYPE of stress test rather than notice an empty result set. VERIFIED across six "
            "phrasings including 'climate risk' and 'net zero', all zero. CONCERN: a generator that "
            "treats 'stress testing' as the salient term and 'climate' as a modifier will answer "
            "from the CCAR chunks and look well-sourced doing it."
        ),
    },
]


def verify_absence(corpus: Corpus, spec: dict) -> tuple[dict | None, list[str]]:
    """Prove absence mechanically, then build the candidate.

    Every search term is re-counted over all 128 raw `content` fields at build
    time. One occurrence anywhere fails the build: a question that is even
    partially answerable would make correct abstention score as a failure.
    """
    problems = []
    for term in spec["search_terms"]:
        found = sum(text.lower().count(term.lower()) for text in corpus.content.values())
        if found:
            where = sorted(
                tid for tid, text in corpus.content.items() if term.lower() in text.lower()
            )
            problems.append(
                f"[{spec['id']}] search term {term!r} occurs {found} time(s) in "
                f"{len(where)} transcript(s) ({', '.join(where[:4])}...): the question is not "
                "unanswerable"
            )
    if problems:
        return None, problems

    return {
        "id": spec["id"],
        "category": UNANSWERABLE_CATEGORY,
        "question": spec["question"],
        "transcript_ids": [],
        "gold_anchors": [],
        "reference_answer": spec["reference_answer"],
        "absence_type": spec["absence_type"],
        "absence_evidence": {
            "search_terms": spec["search_terms"],
            "occurrences_found": 0,
            "transcripts_searched": len(corpus.content),
            "method": "case-insensitive substring search over raw content field",
        },
        "expected_retrieval": spec["expected_retrieval"],
        "notes": spec["notes"],
        "batch": 3,
        "provenance": [],
        "chunk_size_sensitive": False,
    }, []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verify-only", action="store_true", help="verify without writing outputs")
    parser.add_argument("--out-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    corpus = Corpus()
    index_path = OUTPUT_DIR / "corpus_index.json"
    if not index_path.exists():
        raise SystemExit(f"missing {index_path} -- run scripts/build_corpus_index.py first")
    index = json.loads(index_path.read_text(encoding="utf-8"))

    candidates, dropped = [], []
    for spec in CANDIDATES:
        candidate, problems = build_candidate(corpus, spec)
        if candidate is None:
            dropped.extend(problems)
        else:
            candidates.append(candidate)

    # (Rule 5) Comparative independence, enforced across BOTH batches: a
    # comparative must not re-test a passage a thematic already covers, or the two
    # categories are not independent and the same text is scored twice.
    thematic_anchors = {
        p["anchor"] for c in candidates if c["category"] == "thematic" for p in c["provenance"]
    }
    overlaps = [
        f"{c['id']} (batch {c['batch']}) shares an anchor with a thematic candidate: {p['anchor']!r}"
        for c in candidates
        if c["category"] == "comparative"
        for p in c["provenance"]
        if p["anchor"] in thematic_anchors
    ]
    if overlaps:
        raise SystemExit(
            "Rule 5 violated -- comparative/thematic anchor overlap:\n  "
            + "\n  ".join(overlaps)
        )
    print("Rule 5 OK: no comparative shares an anchor with any thematic candidate")

    # (Rule 2) heuristic support check, reported for manual review
    for candidate in candidates:
        unsupported = answer_support_warnings(candidate)
        if unsupported:
            print(f"RULE 2 REVIEW {candidate['id']}: answer words absent from every anchor: {unsupported}")

    dropped = KNOWN_DROPS + dropped
    unanswerable = []
    for spec in UNANSWERABLE:
        candidate, problems = verify_absence(corpus, spec)
        if candidate is None:
            dropped.extend(problems)
        else:
            unanswerable.append(candidate)
    print(f"absence proven for {len(unanswerable)} unanswerable candidates "
          f"over {len(corpus.content)} transcripts")
    candidates += unanswerable

    for problem in dropped:
        print(f"DROPPED: {problem}")

    counts = {c: sum(1 for x in candidates if x["category"] == c)
              for c in list(CATEGORY_TITLES) + [UNANSWERABLE_CATEGORY]}
    print(f"\nverified {len(candidates)} candidates: " + ", ".join(f"{v} {k}" for k, v in counts.items()))
    print(f"dropped {len(dropped)} anchor problem(s)")

    if args.verify_only:
        return

    absence = build_absence_report(corpus, index)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.out_dir / "reference_candidates.json"
    md_path = args.out_dir / "reference_candidates.md"
    json_path.write_text(
        json.dumps(
            {
                "note": (
                    "Reference material for calibration. NOT the benchmark -- "
                    "benchmark/questions.jsonl is authored by the researcher."
                ),
                "candidates": candidates,
                "corpus_boundaries": absence,
                "dropped_in_verification": dropped,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(candidates, absence, dropped), encoding="utf-8")
    print(f"Wrote {json_path} and {md_path}")


if __name__ == "__main__":
    main()
