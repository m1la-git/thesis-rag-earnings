"""Build a human-browsable index of the frozen transcript corpus.

Dev/analysis tool, NOT part of the experimental pipeline in src/. It exists so
the researcher can navigate 128 transcripts efficiently while manually
authoring benchmark questions, gold anchors, and reference answers.

SCOPE CONSTRAINT (methodological, not stylistic): this script extracts and
organizes material that already exists in the transcripts. It does not author
questions, propose gold anchors, or write reference answers -- those are the
researcher's work. No LLM is called; every
step is deterministic phrase statistics and regex, so the index is free to
re-run, reproducible, and explainable in a methodology chapter.

Outputs:
  analysis/benchmark_authoring/corpus_index.json  full structured data
  analysis/benchmark_authoring/corpus_index.md    skimmable Markdown, aggregates first

Filter invariance
-----------------
--ticker/--quarter change only WHICH transcripts are rendered, never what is
computed about them. The topic vocabulary, document frequencies, and figure
rarity counts are always mined over all 128 frozen transcripts. A filtered run
therefore produces per-transcript entries identical to the full run -- otherwise
regenerating a subset would silently relabel transcripts.

Verbatim guarantee
------------------
Sentences are extracted as (start, end) character offsets into the source turn
text and sliced out, never rebuilt from tokens. `assert_reconstructs` checks,
for every turn in the corpus, that the extracted spans plus the whitespace gaps
between them reproduce the turn text character-for-character. Every sentence in
the output can be located in the source by transcript_id + turn_index + offsets.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from transformers.utils import logging as hf_logging  # noqa: E402

from chunking import chunk_transcript  # noqa: E402
from ingest import diff_against_manifest, load_manifest  # noqa: E402
from preprocess import SECTION_PREPARED, SECTION_QA, preprocess_transcript  # noqa: E402

TRANSCRIPTS_PATH = REPO_ROOT / "data" / "processed" / "transcripts.parquet"
MANIFEST_PATH = REPO_ROOT / "data" / "corpus_manifest.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "analysis" / "benchmark_authoring"

CHUNK_SIZES = (200, 500)

# chunking.py tokenizes a whole section in one call and slices it into windows,
# which trips a benign "sequence length > 512" warning on every transcript.
hf_logging.set_verbosity_error()

# ---------------------------------------------------------------------------
# Topic mining parameters
# ---------------------------------------------------------------------------

NGRAM_MAX = 4              # longest candidate phrase, in tokens
VOCAB_MIN_DOC_FREQ = 3     # a phrase must occur in >= 3 transcripts to be a topic
VOCAB_MIN_TOTAL = 8        # ...and >= 8 times corpus-wide
ABSORB_RATIO = 0.6         # drop "net interest" if "net interest income" covers >=60% of it
MIN_TOPIC_COUNT = 3        # a topic must occur >= 3 times in a transcript to be listed
MAX_TOPICS = 12
MIN_DISTINCTIVE_COUNT = 2
MAX_DISTINCTIVE = 8
MIN_QA_THEME_COUNT = 2
MAX_QA_THEME_LABELS = 4

# ---------------------------------------------------------------------------
# Stoplists
#
# Two negative filters, applied at PHRASE BOUNDARIES only: a listed word may
# sit inside a phrase, it just cannot start or end one. Neither encodes a topic
# taxonomy. STOPWORDS is generic English function/discourse vocabulary;
# BOILERPLATE is earnings-call scaffolding read off the top ~150 mined phrases
# of this corpus, i.e. derived from output rather than imposed in advance.
# ---------------------------------------------------------------------------

STOPWORDS = set("""
a an the and or but if then than so as at by for of with about against between into through
during before after above below to from up down in out on off over under again further once
here there when where why how all any both each few more most other others some such no nor not
only own same too very s t can will just don should now i me my myself we our ours ourselves
you your yours yourself he him his she her hers it its they them their theirs what which who
whom whose this that these those am is are was were be been being have has had having do does
did doing would could shall may might must let lets ll re ve d m o y us whether either neither
im id ive ill youre youve youll weve were wed well theyre theyve thats its whats theres heres
i'm i'd i've i'll you're you've you'll we're we've we'll we'd they're they've it's that's
there's here's what's he's she's don't didn't doesn't isn't aren't wasn't weren't can't won't
couldn't wouldn't shouldn't haven't hasn't hadn't
going go goes went gone get gets got getting really much many well way ways said say says
saying know knows thing things little bit lot lots maybe probably actually basically obviously
certainly clearly definitely simply frankly honestly overall generally particularly especially
one two three four five six seven eight nine ten eleven twelve twenty hundred
first second third fourth fifth next last previous prior current
thank thanks yes yeah yep okay ok sure sorry hi hey hello
like want wants need needs make made makes making take takes taking
come comes came give gives given giving put puts keep keeps kept
see saw seen seeing look looks looking looked
think thinks thought feel feels felt believe believes believed
guy guys folks sir maam everybody everyone anybody anyone somebody someone nobody
kind sort couple several
""".split())

BOILERPLATE = set("""
slide slides page pages exhibit exhibits appendix chart charts table tables deck presentation
turn turning turned turns hand handing back
call calls conference webcast replay line lines open
question questions answer answers ask asked asking follow followup
remark remarks prepared operator ladies gentlemen participants
morning afternoon evening today tomorrow yesterday
quarter quarters year years month months week weeks day days time times period periods
billion billions million millions trillion thousand percent percentage basis point points bps
number numbers amount amounts level levels range ranges terms course result results
investor investors relations chief executive officer officers president chairman
statement statements forward looking release
begin begins beginning start starts started end ends ended ending
please ahead proceed welcome congratulations congrats appreciate joining
q1 q2 q3 q4
partially offset offsetting driven reflecting reflected primarily largely mainly
excluding including versus compared relative roughly approximately modestly slightly
across around throughout behind alongside
""".split())

BOUNDARY_STOP = STOPWORDS | BOILERPLATE

# Applied at the phrase-FINAL position only. These words modify a noun rather
# than being one, so a phrase ending on them is a truncated concept ("fx
# adjusted", "return on average", "capital ratios higher", "fee and total").
# The asymmetry is the point: every one of them is a perfectly good phrase
# *opening* ("total revenue", "average balances", "core deposits", "net
# charge-offs", "higher rates"), so banning them at both ends would delete real
# topics. Read off the 18 truncated labels in a full corpus run.
TAIL_STOP = set("""
total adjusted net gross average underlying core overall combined normalized
higher lower strong weak better worse positive negative flat stable similar elevated
additional further significant meaningful modest slight large small good great
full partial key major minor related reported essentially somewhat pretty still
expect expected based quarterly annually broad
""".split())

# Acronyms are admitted as single-token topics on a SURFACE-FORM rule (all caps
# in the source text), not a semantic whitelist. This deny-set removes acronyms
# that are structural or conversational rather than topical.
ACRONYM_DENY = set("""
CEO CFO COO CIO CRO CTO IR SEC GAAP FASB US USA UK EU AM PM ET EST PST GMT
Q1 Q2 Q3 Q4 FY YOY QOQ LLC INC LP LTD PDF FAQ OK TV CNBC IT HR PR AND THE FOR
""".split())

# ---------------------------------------------------------------------------
# Figure extraction
# ---------------------------------------------------------------------------

# ADMIT rule: currency amounts, percentages, and basis-point figures only.
# Bare integers, years, page/slide numbers and headcounts carry no $/%/bps and
# therefore never match at all.
FIGURE_RE = re.compile(
    r"""
    (?P<currency>\$\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:billion|million|trillion|bn|mm)\b)?)
  | (?P<percent>\d[\d,]*(?:\.\d+)?\s*(?:%|\bpercent\b|\bpercentage\s+points?\b))
  | (?P<bps>\d[\d,]*(?:\.\d+)?\s*(?:\bbasis\s+points?\b|\bbps\b|\bbp\b))
    """,
    re.VERBOSE | re.IGNORECASE,
)

# REJECT rule: the figure is a document locator, not a financial quantity.
# Deliberately narrow. Words like "note", "line", "item" and "question" read as
# locators on paper but are ordinary speech on an earnings call -- corpus-wide
# they rejected nothing genuine and wrongly dropped two real figures ("Of note,
# 87% of the nonaccrual loans..."). Because the ADMIT rule requires $, % or bps,
# a bare slide or page number cannot match the regex in the first place, so this
# list only needs to cover locators that could carry a unit.
FIGURE_REJECT_LEFT = {"page", "slide", "exhibit", "appendix", "footnote"}

# RANK rule: a figure is "salient" when its sentence carries a finance term.
# This ranks figures; it does not define topics, which are mined from the text.
FINANCE_KEYWORDS = set("""
revenue revenues income margin margins nii nim rotce roe roa cet1 rwa lcr tce
charge charge-off charge-offs chargeoffs charges provision provisions reserve reserves
allowance guidance guide outlook expense expenses efficiency deposit deposits loan loans
buyback buybacks repurchase repurchases dividend dividends capital ratio ratios
eps earnings profit profitability yield yields spread spreads fee fees
aum auc assets liabilities equity book payout npa nco delinquency delinquencies
growth decline inflows outflows originations balances funding liquidity
""".split())

_FIN_TOKEN_RE = re.compile(r"[a-z][a-z0-9'-]*")

# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------

ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "mt", "inc", "corp", "co",
    "ltd", "llc", "lp", "no", "nos", "vs", "etc", "approx", "est", "fig", "al",
    "u.s", "u.k", "e.g", "i.e", "a.m", "p.m", "dept", "gov", "sen", "rep",
}

# The closing quote/bracket after terminal punctuation belongs to the sentence,
# not to the gap, so it is captured separately and folded back into the span.
_SENTENCE_BREAK = re.compile(r"(?<=[.!?])(?P<close>[\"')\]]*)\s+")
_TRAILING_WORD = re.compile(r"[A-Za-z][A-Za-z.]*$")


def split_sentence_spans(text: str) -> list[tuple[int, int]]:
    """Return (start, end) char offsets of each sentence in `text`.

    Offsets index into `text` directly so callers slice rather than rebuild --
    sentences are verbatim by construction. Whitespace between sentences is
    left in the gaps, never inside a span.
    """
    spans: list[tuple[int, int]] = []
    start = 0
    for match in _SENTENCE_BREAK.finditer(text):
        end = match.start() + len(match.group("close"))
        if end <= start or _is_abbreviation_boundary(text, match.start()):
            continue
        spans.append((start, end))
        start = match.end()
    if start < len(text):
        spans.append((start, len(text)))
    return [(s, e) for s, e in spans if text[s:e].strip()]


def _is_abbreviation_boundary(text: str, end: int) -> bool:
    """True if the period ending at `end` closes an abbreviation or an initial."""
    if end == 0 or text[end - 1] != ".":
        return False
    word = _TRAILING_WORD.search(text[: end - 1])
    if word is None:
        return False
    token = word.group(0).lower()
    # Single-letter initials, e.g. "Ronald P. O'Hanley".
    return token in ABBREVIATIONS or len(token) == 1


def assert_reconstructs(text: str, spans: list[tuple[int, int]]) -> None:
    """Assert spans plus inter-span gaps reproduce `text` exactly, gaps blank.

    This is what makes "verbatim" a checked property rather than a claim: if
    any character were dropped, added, or altered, the rebuild would differ.
    """
    rebuilt: list[str] = []
    cursor = 0
    for start, end in spans:
        gap = text[cursor:start]
        assert gap.strip() == "", f"non-whitespace dropped between sentences: {gap!r}"
        rebuilt.append(gap)
        rebuilt.append(text[start:end])
        cursor = end
    tail = text[cursor:]
    assert tail.strip() == "", f"non-whitespace dropped after last sentence: {tail!r}"
    rebuilt.append(tail)
    assert "".join(rebuilt) == text, "sentence spans do not reconstruct the source text"


# ---------------------------------------------------------------------------
# Phrase tokenization
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-'][A-Za-z0-9]+)*|[^A-Za-z\s]+")
# This corpus spells the same acronym three ways -- "CET1", "CET 1" and "CET-1"
# all occur -- so a trailing number may be attached, spaced or hyphenated. The
# separator is folded out to keep one topic label instead of three.
_ACRONYM_RE = re.compile(r"\b[A-Z]{2,}(?:[\s\-]?[0-9]{1,2})?\b|\b[A-Z][0-9]+\b")
_NAME_PART_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]+")
_ACRONYM_SEPARATOR_RE = re.compile(r"[\s\-]+")


def phrase_runs(text: str, barrier_tokens: set[str]) -> list[list[str]]:
    """Split `text` into runs of lowercase word tokens.

    Punctuation, digits and `barrier_tokens` (speaker name parts) end a run, so
    a candidate phrase never spans a clause break or swallows a person's name.
    """
    runs: list[list[str]] = []
    current: list[str] = []
    for match in _TOKEN_RE.finditer(text):
        token = match.group(0)
        if not token[0].isalpha():
            if current:
                runs.append(current)
                current = []
            continue
        lowered = token.lower()
        if lowered in barrier_tokens:
            if current:
                runs.append(current)
                current = []
            continue
        current.append(lowered)
    if current:
        runs.append(current)
    return runs


def candidate_ngrams(runs: list[list[str]]) -> list[str]:
    """Enumerate 2..NGRAM_MAX-token phrases that neither start nor end on a
    stopword or boilerplate token.

    Unigrams are deliberately excluded: single common words ("quarter",
    "growth", "higher") dominate raw frequency without naming a topic. Single
    -token topics enter only through the acronym rule below.
    """
    out: list[str] = []
    for run in runs:
        length = len(run)
        for n in range(2, NGRAM_MAX + 1):
            for i in range(length - n + 1):
                gram = run[i:i + n]
                if gram[0] in BOUNDARY_STOP or gram[-1] in BOUNDARY_STOP:
                    continue
                if gram[-1] in TAIL_STOP:
                    continue
                if any(len(word) < 2 for word in gram):
                    continue
                # Two function words in a row means the phrase spans a clause
                # join ("merrill and the private"), not a single concept.
                if any(a in BOUNDARY_STOP and b in BOUNDARY_STOP for a, b in zip(gram, gram[1:])):
                    continue
                out.append(" ".join(gram))
    return out


def extract_acronyms(text: str) -> list[str]:
    """All-caps tokens in the source text, as single-token topic candidates."""
    acronyms = []
    for token in _ACRONYM_RE.findall(text):
        folded = _ACRONYM_SEPARATOR_RE.sub("", token)
        if folded not in ACRONYM_DENY:
            acronyms.append(folded.lower())
    return acronyms


def speaker_barrier_tokens(records: list[dict]) -> set[str]:
    """Name parts of every speaker in a transcript, lowercased.

    Without this, `jeremy barnum` outranks `net interest income`: names recur
    constantly inside spoken text ("Thanks, Jeremy", "Betsy, before I answer").
    """
    tokens: set[str] = set()
    for record in records:
        for part in _NAME_PART_RE.findall(record["speaker"]):
            if len(part) > 1:
                tokens.add(part.lower())
    return tokens


# ---------------------------------------------------------------------------
# Analyst detection
# ---------------------------------------------------------------------------

# Transcripts mix straight and curly apostrophes; both must be name characters
# or "Matt O'Connor" truncates to "Matt O" and the announcement fails to match.
_NAME = r"[A-Z][A-Za-z.'’\-]*(?:\s+[A-Z][A-Za-z.'’\-]*){0,3}"
_FIRM = r"[A-Z][A-Za-z.&'’\-]*(?:\s+(?:of|and|&)?\s*[A-Z][A-Za-z.&'’\-]*){0,4}"

# Two announcement shapes seen in this corpus:
#   "Our next question comes from the line of Moshe Orenbuch with TD Cowen."
#   "We'll go next to Michael Cyprys with Morgan Stanley."
# Both require "question" or "next", which excludes handovers such as
# "I will hand over the conference to Ron O'Hanley."
_ANNOUNCE_PATTERNS = (
    re.compile(
        rf"\bquestions?\b[^.?!]*?\bfrom\b(?:\s+the\s+line\s+of)?\s+(?P<name>{_NAME})"
        rf"(?:\s+(?:with|of|at|from)\s+(?P<firm>{_FIRM}))?"
    ),
    re.compile(
        rf"\bnext\b[^.?!]{{0,30}}?\bto\s+(?P<name>{_NAME})"
        rf"(?:\s+(?:with|of|at|from)\s+(?P<firm>{_FIRM}))?"
    ),
)

_ANNOUNCE_NAME_TAIL = re.compile(
    r"\s+(?:Please|Your|You|Go|Sir|Maam|Thank|Thanks|And|The|We|Our|Line|Now)\b.*$"
)


def _name_key(name: str) -> tuple[str, str] | None:
    """(last name, first initial), the join key between announcements and speakers.

    Tolerates nicknames and middle initials: "Mike Mayo" and "Michael Mayo"
    both key to ("mayo", "m"); "Ron O'Hanley" and "Ronald P. O'Hanley" both key
    to ("o'hanley", "r").
    """
    parts = [p for p in _NAME_PART_RE.findall(name) if len(p) > 1]
    if len(parts) < 2:
        return None
    return parts[-1].lower(), parts[0][0].lower()


def _clean_announced_name(raw: str) -> str:
    return _ANNOUNCE_NAME_TAIL.sub("", raw).strip(" .,")


def detect_analysts(records: list[dict]) -> dict[str, dict]:
    """Map speaker label -> {"firm": str|None, "matched": "name"|"next_turn"}.

    Primary gate is the operator's own announcement, matched to a real speaker
    label by (last name, first initial). The next-turn heuristic is a fallback
    used only when an announcement matches no speaker -- it disagrees with the
    announcement legitimately in a few transcripts (an executive interjects
    before the analyst speaks), so it must not be required to agree.
    """
    speakers_by_key: dict[tuple[str, str], str] = {}
    for record in records:
        key = _name_key(record["speaker"])
        if key is not None:
            speakers_by_key.setdefault(key, record["speaker"])

    analysts: dict[str, dict] = {}
    for i, record in enumerate(records):
        if record["section"] != SECTION_QA or record["speaker"] != "Operator":
            continue
        match = next(
            (m for pattern in _ANNOUNCE_PATTERNS if (m := pattern.search(record["text"]))),
            None,
        )
        if match is None:
            continue
        firm = _clean_announced_name(match.group("firm") or "") or None
        key = _name_key(_clean_announced_name(match.group("name")))
        speaker = speakers_by_key.get(key) if key else None
        how = "name"
        if speaker is None:
            nxt = records[i + 1] if i + 1 < len(records) else None
            if nxt is None or nxt["speaker"] == "Operator":
                continue
            speaker, how = nxt["speaker"], "next_turn"
        analysts.setdefault(speaker, {"firm": firm, "matched": how})
        if analysts[speaker]["firm"] is None and firm:
            analysts[speaker]["firm"] = firm
    return analysts


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

_SCALE_ALIASES = {"bn": "billion", "mm": "million", "": "unit"}
_PCT_SUFFIX = re.compile(r"^(\d+(?:\.\d+)?)(?:%|percent|percentagepoints?)$")
_BPS_SUFFIX = re.compile(r"^(\d+(?:\.\d+)?)(?:basispoints?|bps|bp)$")
_CCY_SUFFIX = re.compile(r"^\$(\d+(?:\.\d+)?)(billion|million|trillion|bn|mm)?$")


def _normalize_number(value: str) -> str:
    """'51.0' -> '51', '18.10' -> '18.1', so equal figures collapse together."""
    number = float(value)
    return str(int(number)) if number == int(number) else str(number)


def canonical_figure(raw: str) -> str:
    """Canonical key for rarity counting: '$51 billion' -> 'usd:51:billion'."""
    squashed = raw.lower().replace(",", "").replace(" ", "")
    if (m := _CCY_SUFFIX.match(squashed)) is not None:
        scale = m.group(2) or ""
        return f"usd:{_normalize_number(m.group(1))}:{_SCALE_ALIASES.get(scale, scale)}"
    if (m := _PCT_SUFFIX.match(squashed)) is not None:
        return f"pct:{_normalize_number(m.group(1))}"
    if (m := _BPS_SUFFIX.match(squashed)) is not None:
        return f"bps:{_normalize_number(m.group(1))}"
    return f"raw:{squashed}"


def _rejected_as_locator(sentence: str, figure_start: int) -> bool:
    """REJECT rule: the word immediately before the figure marks it as a locator."""
    preceding = _FIN_TOKEN_RE.findall(sentence[:figure_start].lower())
    return bool(preceding) and preceding[-1] in FIGURE_REJECT_LEFT


def is_salient(sentence: str) -> bool:
    """RANK rule: does the containing sentence carry any finance term?"""
    return any(t in FINANCE_KEYWORDS for t in _FIN_TOKEN_RE.findall(sentence.lower()))


def extract_figures(sentence: str, previous_sentence: str) -> list[dict]:
    """Figures stated in one sentence, with their offsets inside that sentence.

    Salience is judged over the sentence PLUS its predecessor in the same turn,
    never over the extracted text. Q&A phrasing routinely strands the number a
    sentence away from the term that gives it meaning ("So I'd anchor you to the
    $89 billion."), so a sentence-local test under-ranks exactly the
    conversational figures worth surfacing. Nothing incidental gets in either
    way: the ADMIT regex still requires a currency, percentage or bps unit.

    Only about a quarter of sentences contain a figure at all, so the salience
    scan is deferred until one matches rather than run over every sentence.
    """
    matches = [
        match
        for match in FIGURE_RE.finditer(sentence)
        if not _rejected_as_locator(sentence, match.start())
    ]
    if not matches:
        return []

    salient = is_salient(f"{previous_sentence} {sentence}" if previous_sentence else sentence)
    figures: list[dict] = []
    for match in matches:
        raw = match.group(0).strip()
        figures.append(
            {
                "figure": raw,
                "canonical": canonical_figure(raw),
                "kind": match.lastgroup,
                # Offset of the figure within its sentence; the sentence's own
                # offset within the turn is attached by the caller.
                "figure_char_start": match.start(),
                "figure_char_end": match.start() + len(raw),
                "salient": salient,
            }
        )
    return figures


# ---------------------------------------------------------------------------
# Corpus pass (always over all 128 transcripts -- see "Filter invariance")
# ---------------------------------------------------------------------------


def load_corpus() -> pd.DataFrame:
    """Load the frozen corpus and confirm its text still matches the manifest.

    The sentences in this index are what gold anchors get lifted from, so an
    index built over drifted text would hand out anchors that no longer exist in
    the corpus. `diff_against_manifest` re-hashes every transcript here (well
    under a second) and this refuses to build if anything moved.
    """
    if not TRANSCRIPTS_PATH.exists():
        raise SystemExit(f"missing {TRANSCRIPTS_PATH} -- run src/ingest.py first")
    frame = pd.read_parquet(TRANSCRIPTS_PATH)

    manifest = load_manifest()
    problems = diff_against_manifest(frame, manifest, "local parquet")
    if problems:
        for problem in problems:
            print(f"  {problem}")
        raise SystemExit(
            f"\n{len(problems)} corpus drift problem(s): the parquet no longer matches "
            f"{MANIFEST_PATH.name}. Refusing to build an index whose sentences may not "
            "exist in the frozen corpus. Run `python src/ingest.py --verify` to diagnose."
        )

    return frame.sort_values(["symbol", "year", "quarter"]).reset_index(drop=True)


def scan_transcript(row: pd.Series) -> dict:
    """Sentence-split, count phrases, and pull figures for one transcript.

    Returns the raw per-transcript material; topic *selection* happens later,
    once corpus-wide document frequencies are known.
    """
    records = preprocess_transcript(row)
    barriers = speaker_barrier_tokens(records)
    analysts = detect_analysts(records)

    phrase_counts: Counter[str] = Counter()
    analyst_phrase_counts: dict[str, Counter[str]] = defaultdict(Counter)
    sentences: list[dict] = []
    figures: list[dict] = []
    section_words: Counter[str] = Counter()
    section_turns: Counter[str] = Counter()
    questions: dict[str, list[dict]] = defaultdict(list)

    for record in records:
        text = record["text"]
        spans = split_sentence_spans(text)
        assert_reconstructs(text, spans)

        section_words[record["section"]] += len(text.split())
        section_turns[record["section"]] += 1

        grams = candidate_ngrams(phrase_runs(text, barriers)) + extract_acronyms(text)
        phrase_counts.update(grams)
        speaker = record["speaker"]
        if speaker in analysts and record["section"] == SECTION_QA:
            analyst_phrase_counts[speaker].update(grams)

        for span_index, (start, end) in enumerate(spans):
            sentence = text[start:end]
            # Salience looks one sentence back within the same turn; the stored
            # `sentence` field stays exactly the span sliced above.
            previous = text[spans[span_index - 1][0]:spans[span_index - 1][1]] if span_index else ""
            entry = {
                "turn_index": record["turn_index"],
                "speaker": speaker,
                "section": record["section"],
                "char_start": start,
                "char_end": end,
                "text": sentence,
            }
            sentences.append(entry)
            if speaker in analysts and record["section"] == SECTION_QA and sentence.rstrip().endswith("?"):
                questions[speaker].append(entry)
            for figure in extract_figures(sentence, previous):
                figures.append(
                    {
                        **figure,
                        "section": record["section"],
                        "speaker": speaker,
                        "turn_index": record["turn_index"],
                        "sentence": sentence,
                        "sentence_char_start": start,
                        "sentence_char_end": end,
                    }
                )

    return {
        "transcript_id": row["transcript_id"],
        "ticker": row["symbol"],
        "company": row["company_name"],
        "year": int(row["year"]),
        "quarter": int(row["quarter"]),
        "date": str(row["date"]),
        "records": records,
        "analysts": analysts,
        "phrase_counts": phrase_counts,
        "analyst_phrase_counts": analyst_phrase_counts,
        "questions": questions,
        "figures": figures,
        "n_sentences": len(sentences),
        "section_words": section_words,
        "section_turns": section_turns,
    }


_PLURAL_SAFE_SUFFIXES = ("ss", "us", "is", "as", "os")


def fold_phrase(phrase: str) -> str:
    """Group key merging a phrase with its plural and possessive forms
    ("servicing fee" / "servicing fees", "state street" / "state street's").

    Only a trailing possessive and then a plain trailing "s" on the final token
    are stripped, and the "s" never after ss/us/is/as/os, so no stem is mangled
    ("basis", "loss", "versus" are left alone). The key is internal: topics are
    always displayed using a surface form that actually occurs in the
    transcripts, so folding never invents a label.
    """
    words = phrase.split()
    last = words[-1]
    for possessive in ("'s", "’s"):
        if last.endswith(possessive):
            last = last[: -len(possessive)]
    if len(last) >= 4 and last.endswith("s") and not last.endswith(_PLURAL_SAFE_SUFFIXES):
        last = last[:-1]
    words[-1] = last
    return " ".join(words)


def fold_counts(counts: Counter[str]) -> Counter[str]:
    """Re-key a transcript's raw phrase counts onto folded group keys."""
    folded: Counter[str] = Counter()
    for phrase, count in counts.items():
        folded[fold_phrase(phrase)] += count
    return folded


def mine_vocabulary(scans: list[dict]) -> dict[str, dict]:
    """Corpus-wide phrase vocabulary keyed by folded phrase.

    Three passes: singular/plural folding, frequency pruning, then sub-phrase
    absorption -- "net interest" is dropped when "net interest income" accounts
    for >=ABSORB_RATIO of its occurrences, so the topic list carries the longest
    phrase actually used rather than its fragments.
    """
    total: Counter[str] = Counter()
    doc_freq: Counter[str] = Counter()
    surface: dict[str, Counter[str]] = defaultdict(Counter)
    for scan in scans:
        folded = fold_counts(scan["phrase_counts"])
        total.update(folded)
        doc_freq.update(folded.keys())
        for phrase, count in scan["phrase_counts"].items():
            surface[fold_phrase(phrase)][phrase] += count

    kept = {
        phrase
        for phrase, count in total.items()
        if count >= VOCAB_MIN_TOTAL and doc_freq[phrase] >= VOCAB_MIN_DOC_FREQ
    }

    best_extension: dict[str, int] = {}
    for phrase in kept:
        words = phrase.split()
        for n in range(1, len(words)):
            for i in range(len(words) - n + 1):
                sub = " ".join(words[i:i + n])
                if total[phrase] > best_extension.get(sub, 0):
                    best_extension[sub] = total[phrase]

    vocabulary = {}
    for phrase in kept:
        if best_extension.get(phrase, 0) >= ABSORB_RATIO * total[phrase]:
            continue
        label, _ = min(surface[phrase].items(), key=lambda kv: (-kv[1], len(kv[0]), kv[0]))
        vocabulary[phrase] = {
            "total": total[phrase],
            "doc_freq": doc_freq[phrase],
            "label": label,
        }
    return vocabulary


def company_name_phrases(company: str, ticker: str) -> set[str]:
    """Folded sub-phrases of a transcript's own company name.

    "state street" is not a topic of a State Street call, it is the speaker. The
    block is per-transcript and applies to sub-phrases of the full name only, so
    it never removes an ordinary word: "bank failures" survives on a Bank of
    America call because it is not part of that name. Another bank's name stays
    available as a topic, since a competitor mention is real content.
    """
    words = [w.lower() for w in _NAME_PART_RE.findall(company)]
    blocked = {ticker.lower()}
    for n in range(1, len(words) + 1):
        for i in range(len(words) - n + 1):
            blocked.add(fold_phrase(" ".join(words[i:i + n])))
    return blocked


def select_topics(
    counts: Counter[str],
    vocabulary: dict[str, dict],
    n_docs: int,
    blocked: set[str] = frozenset(),
) -> tuple[list[dict], list[dict]]:
    """Pick a transcript's main topics and its distinctive topics.

    `topics` ranks by within-transcript frequency -- what the call was mostly
    about, which is what makes thematic and comparative candidates findable.
    `distinctive` ranks by tf x log(1 + N/df) -- what sets this call apart from
    the other 127, which is where clean single-source factual candidates live;
    it excludes anything already in `topics` so the two lists never restate each
    other. Both are truncated by a minimum count rather than padded, so a thin
    section yields few topics instead of junk ones.
    """
    folded = fold_counts(counts)
    scored = [
        (phrase, folded[phrase])
        for phrase in vocabulary
        if folded.get(phrase) and phrase not in blocked
    ]

    main = sorted(
        ((p, c) for p, c in scored if c >= MIN_TOPIC_COUNT),
        key=lambda pc: (-pc[1], -len(pc[0]), pc[0]),
    )[:MAX_TOPICS]

    main_topics = {p for p, _ in main}
    distinctive = sorted(
        (
            (p, c, c * math.log(1 + n_docs / vocabulary[p]["doc_freq"]))
            for p, c in scored
            if c >= MIN_DISTINCTIVE_COUNT and p not in main_topics
        ),
        key=lambda pcs: (-pcs[2], -len(pcs[0]), pcs[0]),
    )[:MAX_DISTINCTIVE]

    return (
        [{"topic": vocabulary[p]["label"], "count": c} for p, c in main],
        [
            {
                "topic": vocabulary[p]["label"],
                "count": c,
                "score": round(s, 2),
                "doc_freq": vocabulary[p]["doc_freq"],
            }
            for p, c, s in distinctive
        ],
    )


# ---------------------------------------------------------------------------
# Per-transcript entry
# ---------------------------------------------------------------------------


_WHITESPACE_RE = re.compile(r"\s+")


def build_chunk_locator(chunks: list[dict]) -> tuple[str, list[tuple[int, int, str]]]:
    """Whitespace-stripped concatenation of one section's chunks, plus spans.

    Chunk texts are contiguous slices of the section text, but the whitespace
    between two token windows belongs to neither chunk, so a plain concatenation
    is not quite the section text. Stripping all whitespace from both sides of
    the comparison makes the search exact regardless of where a window landed.
    """
    pieces: list[str] = []
    spans: list[tuple[int, int, str]] = []
    cursor = 0
    for chunk in sorted(chunks, key=lambda c: c["chunk_index"]):
        stripped = _WHITESPACE_RE.sub("", chunk["text"])
        spans.append((cursor, cursor + len(stripped), chunk["chunk_id"]))
        pieces.append(stripped)
        cursor += len(stripped)
    return "".join(pieces), spans


def locate_chunks(
    sentence: str,
    locators: dict[tuple[int, str], tuple[str, list[tuple[int, int, str]]]],
    section: str,
) -> dict[str, list[str]]:
    """Chunk ids covering a sentence, per chunk size.

    Returns one id when the sentence sits inside a single chunk and two or more
    when it straddles a boundary -- the distinction that matters for anchor
    selection, since an anchor spanning a boundary fails the substring test
    under one chunk size while passing under the other.

    Searching the whole section rather than testing chunks individually is what
    makes a straddle resolvable: a short sentence lying across a boundary is
    contained in no chunk at all, so a per-chunk test can only report "not
    found".
    """
    needle = _WHITESPACE_RE.sub("", sentence)
    located: dict[str, list[str]] = {}
    for (size, locator_section), (haystack, spans) in locators.items():
        if locator_section != section:
            continue
        start = haystack.find(needle)
        if start < 0:
            located[f"chunk_ids@{size}"] = []
            continue
        end = start + len(needle)
        located[f"chunk_ids@{size}"] = [
            chunk_id for span_start, span_end, chunk_id in spans
            if span_start < end and span_end > start
        ]
    return located


def build_entry(
    scan: dict,
    vocabulary: dict[str, dict],
    n_docs: int,
    figure_doc_freq: Counter[str],
    with_chunk_stats: bool,
) -> dict:
    """Assemble one transcript's index entry."""
    blocked = company_name_phrases(scan["company"], scan["ticker"])
    topics, distinctive = select_topics(scan["phrase_counts"], vocabulary, n_docs, blocked)

    pools: dict[tuple[int, str], list[dict]] = {}
    locators: dict[tuple[int, str], tuple[str, list[tuple[int, int, str]]]] = {}
    if with_chunk_stats:
        for size in CHUNK_SIZES:
            chunks = chunk_transcript(scan["records"], size)
            for section in (SECTION_PREPARED, SECTION_QA):
                in_section = [c for c in chunks if c["section"] == section]
                pools[(size, section)] = in_section
                locators[(size, section)] = build_chunk_locator(in_section)

    sections = {}
    for section in (SECTION_PREPARED, SECTION_QA):
        stats = {
            "turns": scan["section_turns"].get(section, 0),
            "words": scan["section_words"].get(section, 0),
        }
        if with_chunk_stats:
            # Chunks partition the section exactly, so any chunk size sums to the
            # same total: one token count per section, not one per size.
            first = CHUNK_SIZES[0]
            stats["tokens"] = sum(c["n_tokens"] for c in pools[(first, section)])
            for size in CHUNK_SIZES:
                stats[f"chunks@{size}"] = len(pools[(size, section)])
        sections[section] = stats

    figures = []
    for figure in scan["figures"]:
        located = (
            locate_chunks(figure["sentence"], locators, figure["section"])
            if with_chunk_stats
            else {}
        )
        figures.append(
            {
                **figure,
                "corpus_doc_freq": figure_doc_freq[figure["canonical"]],
                **located,
            }
        )
    figures.sort(key=lambda f: (not f["salient"], f["turn_index"], f["figure_char_start"]))

    qa_themes = []
    for speaker, info in scan["analysts"].items():
        counts = fold_counts(scan["analyst_phrase_counts"].get(speaker, Counter()))
        # An analyst who asks one short question repeats nothing; fall back to
        # single mentions rather than leaving their row unlabelled.
        labels: list[tuple[str, int]] = []
        for threshold in (MIN_QA_THEME_COUNT, 1):
            labels = sorted(
                (
                    (p, c)
                    for p, c in counts.items()
                    if p in vocabulary and p not in blocked and c >= threshold
                ),
                key=lambda pc: (-pc[1], -len(pc[0]), pc[0]),
            )[:MAX_QA_THEME_LABELS]
            if labels:
                break
        qa_themes.append(
            {
                "analyst": speaker,
                "firm": info["firm"],
                "matched_by": info["matched"],
                "themes": [vocabulary[p]["label"] for p, _ in labels],
                "questions": [
                    {
                        "turn_index": q["turn_index"],
                        "char_start": q["char_start"],
                        "char_end": q["char_end"],
                        "text": q["text"],
                    }
                    for q in scan["questions"].get(speaker, [])
                ],
            }
        )

    return {
        "transcript_id": scan["transcript_id"],
        "ticker": scan["ticker"],
        "company": scan["company"],
        "year": scan["year"],
        "quarter": scan["quarter"],
        "date": scan["date"],
        "sections": sections,
        "n_sentences": scan["n_sentences"],
        "topics": topics,
        "distinctive_topics": distinctive,
        "qa_themes": qa_themes,
        "figures": figures,
    }


# ---------------------------------------------------------------------------
# Cross-corpus aggregates (always computed over all 128 transcripts)
# ---------------------------------------------------------------------------

MAX_RARE_PER_TRANSCRIPT = 3


def build_aggregates(entries: list[dict], figure_doc_freq: Counter[str]) -> dict:
    """Topic frequency, topic-by-company, rare figures, and coverage gaps."""
    tickers_all = sorted({e["ticker"] for e in entries})
    quarters_all = sorted({f"{e['year']}Q{e['quarter']}" for e in entries})

    topic_docs: dict[str, list[str]] = defaultdict(list)
    topic_tickers: dict[str, set[str]] = defaultdict(set)
    topic_quarters: dict[str, set[str]] = defaultdict(set)
    topic_total: Counter[str] = Counter()
    for entry in entries:
        quarter = f"{entry['year']}Q{entry['quarter']}"
        for item in entry["topics"]:
            topic = item["topic"]
            topic_docs[topic].append(entry["transcript_id"])
            topic_tickers[topic].add(entry["ticker"])
            topic_quarters[topic].add(quarter)
            topic_total[topic] += item["count"]

    topic_frequency = sorted(
        (
            {
                "topic": topic,
                "n_transcripts": len(docs),
                "n_tickers": len(topic_tickers[topic]),
                "total_mentions": topic_total[topic],
                "tickers": sorted(topic_tickers[topic]),
                "quarters": sorted(topic_quarters[topic]),
                "transcript_ids": sorted(docs),
            }
            for topic, docs in topic_docs.items()
        ),
        key=lambda row: (-row["n_transcripts"], -row["total_mentions"], row["topic"]),
    )

    comparative = sorted(
        (row for row in topic_frequency if row["n_tickers"] >= 2),
        key=lambda row: (-row["n_tickers"], -row["n_transcripts"], row["topic"]),
    )

    coverage_gaps = sorted(
        (
            {
                "topic": row["topic"],
                "n_transcripts": row["n_transcripts"],
                "present_tickers": row["tickers"],
                "absent_tickers": [t for t in tickers_all if t not in set(row["tickers"])],
                "absent_quarters": [q for q in quarters_all if q not in set(row["quarters"])],
            }
            for row in topic_frequency
            if 1 <= row["n_transcripts"] < len(entries)
        ),
        key=lambda row: (-row["n_transcripts"], row["topic"]),
    )

    rare: list[dict] = []
    for entry in entries:
        picks = [
            f for f in entry["figures"]
            if f["salient"] and figure_doc_freq[f["canonical"]] == 1
        ]
        picks.sort(key=lambda f: (f["kind"] != "currency", f["turn_index"], f["figure_char_start"]))
        # One row per distinct value: a figure restated later in the same call
        # would otherwise use up the per-transcript budget on a duplicate.
        seen: set[str] = set()
        picks = [f for f in picks if not (f["canonical"] in seen or seen.add(f["canonical"]))]
        for figure in picks[:MAX_RARE_PER_TRANSCRIPT]:
            rare.append(
                {
                    "figure": figure["figure"],
                    "canonical": figure["canonical"],
                    "transcript_id": entry["transcript_id"],
                    "ticker": entry["ticker"],
                    "quarter": f"{entry['year']}Q{entry['quarter']}",
                    "section": figure["section"],
                    "speaker": figure["speaker"],
                    "turn_index": figure["turn_index"],
                    "sentence": figure["sentence"],
                    **{k: v for k, v in figure.items() if k.startswith("chunk_ids@")},
                }
            )

    return {
        "topic_frequency": topic_frequency,
        "topics_by_company": comparative,
        "coverage_gaps": coverage_gaps,
        "rare_figures": rare,
        "tickers": tickers_all,
        "quarters": quarters_all,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

MD_TOPIC_ROWS = 60
MD_COMPARATIVE_ROWS = 50
MD_GAP_ROWS = 40
MD_FIGURES_PER_TRANSCRIPT = 18
MD_QUESTION_CHARS = 220


def _cell(text: str) -> str:
    """Make a string safe for a Markdown table cell without altering wording."""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _truncate(text: str, limit: int) -> str:
    text = _cell(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "\u2026"


def _quarter_cell(quarters: list[str], all_quarters: list[str]) -> str:
    """'8/8' when a topic spans every quarter, the explicit list when it does not."""
    if len(quarters) == len(all_quarters):
        return f"all {len(all_quarters)}"
    return f"{len(quarters)}/{len(all_quarters)}: " + ", ".join(quarters)


def _chunk_cell(chunk_ids: list[str]) -> str:
    """Show only the chunk index; the full id is transcript_section_size_index."""
    return ", ".join(cid.rsplit("_", 1)[-1] for cid in chunk_ids) or "–"


def _select_display_figures(figures: list[dict], limit: int) -> list[dict]:
    """Up to `limit` figures with both sections represented.

    `figures` is already ordered salient-first, so taking the head alone fills
    the table from prepared remarks and never reaches Q&A -- where the
    analyst-driven material is.
    """
    per_section = max(1, limit // 2)
    picked: list[int] = []
    for section in (SECTION_PREPARED, SECTION_QA):
        picked += [i for i, f in enumerate(figures) if f["section"] == section][:per_section]
    if len(picked) < limit:
        taken = set(picked)
        picked += [i for i in range(len(figures)) if i not in taken][: limit - len(picked)]
    return [figures[i] for i in sorted(picked)]


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["_none_", ""]
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    out += ["| " + " | ".join(row) + " |" for row in rows]
    out.append("")
    return out


def render_markdown(entries: list[dict], aggregates: dict, meta: dict) -> str:
    lines: list[str] = [
        "# Corpus index",
        "",
        f"Generated by `scripts/build_corpus_index.py` \u00b7 "
        f"{meta['n_rendered']} of {meta['n_corpus']} transcripts rendered.",
        "",
        "> Extraction and organisation only. Nothing here is an authored question, a proposed",
        "> gold anchor, or a reference answer \u2014 those are the researcher's.",
        "",
        "**Scope.** Topic vocabulary, document frequencies and figure-rarity counts are always",
        f"computed over all {meta['n_corpus']} frozen transcripts, so a filtered run labels",
        "transcripts identically to a full run. Filters change only what is rendered below.",
        "",
        f"**Filters.** ticker: `{meta['ticker_filter'] or 'all'}` \u00b7 "
        f"quarter: `{meta['quarter_filter'] or 'all'}`",
        "",
        "**Contents.** "
        + " \u00b7 ".join(
            f"{ticker} ({count})"
            for ticker, count in sorted(Counter(e["ticker"] for e in entries).items())
        ),
        "",
        "Search a transcript id to jump straight to it, e.g. `#### "
        + (entries[0]["transcript_id"] if entries else "JPM_2024_Q1")
        + "`.",
        "",
        "**Method.** Topics are 2\u20134-token phrases mined from the transcript text itself",
        "(no imposed taxonomy), pruned by a generic-English + earnings-call-boilerplate",
        "stoplist applied at phrase boundaries, with sub-phrases absorbed into the longer",
        "phrase that contains them; plus all-caps acronyms found in the source. *Main* topics",
        "rank by within-transcript frequency; *distinctive* topics rank by tf \u00b7 log(1 + N/df),",
        "i.e. what sets this call apart from the other 127. Figures are currency, percentage",
        "and basis-point expressions only; a figure is marked salient when its sentence carries",
        "a finance term. Every sentence is sliced verbatim from the source by character offset.",
        "",
        "> **Take gold-anchor text from `corpus_index.json`, not from this file.** Sentences in",
        "> the JSON are exact character-for-character slices of the source. The tables below are",
        "> a browsing view: a long sentence is cut short and marked with `…`, and any literal `|`",
        "> is backslash-escaped so it does not break the table. Copying a truncated sentence from",
        "> here would silently fail to substring-match against chunk text. The JSON carries the",
        "> full sentence plus `turn_index` and `sentence_char_start`/`_end` to locate it.",
        "",
        "---",
        "",
        "## Aggregates",
        "",
        f"### Topic frequency (top {MD_TOPIC_ROWS} of {len(aggregates['topic_frequency'])})",
        "",
        "How widely each topic is discussed \u2014 high `transcripts` suggests a thematic candidate.",
        "",
    ]

    lines += _table(
        ["topic", "transcripts", "tickers", "mentions", "quarters"],
        [
            [
                _cell(row["topic"]),
                str(row["n_transcripts"]),
                f"{row['n_tickers']} ({_truncate(', '.join(row['tickers']), 100)})",
                str(row["total_mentions"]),
                _quarter_cell(row["quarters"], aggregates["quarters"]),
            ]
            for row in aggregates["topic_frequency"][:MD_TOPIC_ROWS]
        ],
    )

    lines += [
        f"### Topics by company (top {MD_COMPARATIVE_ROWS} of {len(aggregates['topics_by_company'])})",
        "",
        "Topics discussed by two or more banks \u2014 the pool for comparative candidates.",
        "",
    ]
    lines += _table(
        ["topic", "# tickers", "tickers"],
        [
            [_cell(row["topic"]), str(row["n_tickers"]), _truncate(", ".join(row["tickers"]), 110)]
            for row in aggregates["topics_by_company"][:MD_COMPARATIVE_ROWS]
        ],
    )

    lines += [
        f"### Coverage gaps (top {MD_GAP_ROWS} of {len(aggregates['coverage_gaps'])})",
        "",
        "Topics present in some transcripts and absent from others \u2014 the absent side is where",
        "an unanswerable candidate can be grounded.",
        "",
    ]
    lines += _table(
        ["topic", "transcripts", "absent tickers", "absent quarters"],
        [
            [
                _cell(row["topic"]),
                str(row["n_transcripts"]),
                _truncate(", ".join(row["absent_tickers"]) or "\u2014", 90),
                _truncate(", ".join(row["absent_quarters"]) or "\u2014", 50),
            ]
            for row in aggregates["coverage_gaps"][:MD_GAP_ROWS]
        ],
    )

    lines += [
        f"### Rare figures ({len(aggregates['rare_figures'])} shown, "
        f"max {MAX_RARE_PER_TRANSCRIPT} per transcript)",
        "",
        "Salient figures whose value occurs in exactly one transcript corpus-wide \u2014 candidates",
        "with a clean single-source answer. Sentences are verbatim. This table spans the whole",
        "corpus, so `c@200`/`c@500` are filled in only for the transcripts rendered below.",
        "",
    ]
    lines += _table(
        ["figure", "transcript", "sec", "c@200", "c@500", "sentence (verbatim)"],
        [
            [
                _cell(row["figure"]),
                _cell(row["transcript_id"]),
                "prep" if row["section"] == SECTION_PREPARED else "Q&A",
                _chunk_cell(row.get("chunk_ids@200", [])),
                _chunk_cell(row.get("chunk_ids@500", [])),
                _truncate(row["sentence"], 260),
            ]
            for row in aggregates["rare_figures"]
        ],
    )

    lines += ["---", "", "## Transcripts", ""]

    current_ticker = None
    for entry in entries:
        if entry["ticker"] != current_ticker:
            current_ticker = entry["ticker"]
            lines += [f"### {entry['ticker']} \u2014 {entry['company']}", ""]

        prep, qa = entry["sections"][SECTION_PREPARED], entry["sections"][SECTION_QA]
        lines += [
            f"#### {entry['transcript_id']} \u2014 {entry['year']} Q{entry['quarter']} "
            f"({entry['date'][:10]})",
            "",
            "| section | turns | words | tokens | chunks@200 | chunks@500 |",
            "|---|---|---|---|---|---|",
            f"| prepared remarks | {prep['turns']} | {prep['words']} | {prep.get('tokens', '\u2013')} | "
            f"{prep.get('chunks@200', '\u2013')} | {prep.get('chunks@500', '\u2013')} |",
            f"| Q&A | {qa['turns']} | {qa['words']} | {qa.get('tokens', '\u2013')} | "
            f"{qa.get('chunks@200', '\u2013')} | {qa.get('chunks@500', '\u2013')} |",
            "",
            "**Main topics.** "
            + (" \u00b7 ".join(f"{t['topic']} ({t['count']})" for t in entry["topics"]) or "_none above threshold_"),
            "",
            "**Distinctive.** "
            + (
                " \u00b7 ".join(
                    f"{t['topic']} ({t['count']}\u00d7, df {t['doc_freq']})"
                    for t in entry["distinctive_topics"]
                )
                or "_none_"
            ),
            "",
            "**Q&A themes.**",
            "",
        ]
        lines += _table(
            ["analyst", "firm", "themes", "a question (verbatim)"],
            [
                [
                    _cell(theme["analyst"]),
                    _cell(theme["firm"] or "\u2014"),
                    _cell(" \u00b7 ".join(theme["themes"]) or "\u2014"),
                    _truncate(theme["questions"][0]["text"], MD_QUESTION_CHARS)
                    if theme["questions"]
                    else "\u2014",
                ]
                for theme in entry["qa_themes"]
            ],
        )

        shown = _select_display_figures(entry["figures"], MD_FIGURES_PER_TRANSCRIPT)
        lines += [
            f"**Notable figures** ({len(shown)} of {len(entry['figures'])}, salient first, both "
            "sections represented). `df` = transcripts corpus-wide stating this value; `c@200` / "
            "`c@500` = index of the containing chunk, whose full id is "
            "`{transcript}_{section}_{size}_{index}`.",
            "",
        ]
        lines += _table(
            ["figure", "sec", "df", "c@200", "c@500", "sentence (verbatim)"],
            [
                [
                    _cell(figure["figure"]),
                    "prep" if figure["section"] == SECTION_PREPARED else "Q&A",
                    str(figure["corpus_doc_freq"]),
                    _chunk_cell(figure.get("chunk_ids@200", [])),
                    _chunk_cell(figure.get("chunk_ids@500", [])),
                    _truncate(figure["sentence"], 300),
                ]
                for figure in shown
            ],
        )

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_QUARTER_TOKEN = re.compile(r"^(?:(?P<year>\d{4}))?-?(?:Q(?P<quarter>[1-4]))?$", re.IGNORECASE)


def _display(path: Path) -> str:
    """Repo-relative path when possible, absolute otherwise (--out-dir may be anywhere)."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_quarter_filter(raw: str | None) -> list[tuple[int | None, int | None]]:
    """Accept '2024Q1', '2024-Q1', 'Q1', '2024', comma-separated."""
    if not raw:
        return []
    parsed = []
    for token in (t.strip() for t in raw.split(",") if t.strip()):
        match = _QUARTER_TOKEN.match(token)
        if match is None or not (match.group("year") or match.group("quarter")):
            raise SystemExit(f"unrecognised --quarter value: {token!r} (use 2024Q1, Q1, or 2024)")
        year = int(match.group("year")) if match.group("year") else None
        quarter = int(match.group("quarter")) if match.group("quarter") else None
        parsed.append((year, quarter))
    return parsed


def keep_entry(entry: dict, tickers: set[str], quarters: list[tuple[int | None, int | None]]) -> bool:
    if tickers and entry["ticker"].upper() not in tickers:
        return False
    if quarters and not any(
        (year is None or entry["year"] == year) and (quarter is None or entry["quarter"] == quarter)
        for year, quarter in quarters
    ):
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ticker", help="comma-separated tickers to render, e.g. JPM,BAC")
    parser.add_argument("--quarter", help="comma-separated quarters, e.g. 2024Q1,Q3,2023")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--no-chunk-stats",
        action="store_true",
        help="skip chunking (drops token counts, chunk counts and figure->chunk_id mapping)",
    )
    args = parser.parse_args()

    tickers = {t.strip().upper() for t in args.ticker.split(",")} if args.ticker else set()
    quarters = parse_quarter_filter(args.quarter)

    frame = load_corpus()
    print(f"Scanning {len(frame)} frozen transcripts (corpus-wide pass)...")
    scans = [scan_transcript(row) for _, row in frame.iterrows()]
    print(f"  sentence spans verified verbatim for all {sum(s['n_sentences'] for s in scans)} sentences")

    vocabulary = mine_vocabulary(scans)
    print(f"  mined {len(vocabulary)} topic phrases (df>={VOCAB_MIN_DOC_FREQ}, total>={VOCAB_MIN_TOTAL})")

    figure_doc_freq: Counter[str] = Counter()
    for scan in scans:
        figure_doc_freq.update({f["canonical"] for f in scan["figures"]})

    selected = [
        scan for scan in scans
        if keep_entry(
            {"ticker": scan["ticker"], "year": scan["year"], "quarter": scan["quarter"]},
            tickers,
            quarters,
        )
    ]
    if not selected:
        raise SystemExit("no transcripts matched --ticker/--quarter")

    if not args.no_chunk_stats:
        print(f"  chunking {len(selected)} rendered transcripts at {CHUNK_SIZES} tokens...")

    # Aggregates need every transcript's topic list, so entries are built for the
    # whole corpus; only the rendered subset pays for chunking.
    selected_ids = {scan["transcript_id"] for scan in selected}
    all_entries = [
        build_entry(
            scan,
            vocabulary,
            len(scans),
            figure_doc_freq,
            with_chunk_stats=not args.no_chunk_stats and scan["transcript_id"] in selected_ids,
        )
        for scan in scans
    ]
    aggregates = build_aggregates(all_entries, figure_doc_freq)
    entries = [e for e in all_entries if e["transcript_id"] in selected_ids]

    meta = {
        "n_corpus": len(scans),
        "n_rendered": len(entries),
        "ticker_filter": args.ticker,
        "quarter_filter": args.quarter,
        "chunk_sizes": list(CHUNK_SIZES) if not args.no_chunk_stats else [],
        "offsets": (
            "sentence_char_start/end index into the source turn text "
            "(preprocess_transcript(row)[turn_index]['text']); "
            "figure_char_start/end index into the sentence"
        ),
        "parameters": {
            "ngram_max": NGRAM_MAX,
            "vocab_min_doc_freq": VOCAB_MIN_DOC_FREQ,
            "vocab_min_total": VOCAB_MIN_TOTAL,
            "absorb_ratio": ABSORB_RATIO,
            "min_topic_count": MIN_TOPIC_COUNT,
            "max_topics": MAX_TOPICS,
        },
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.out_dir / "corpus_index.json"
    md_path = args.out_dir / "corpus_index.md"
    json_path.write_text(
        json.dumps({"meta": meta, "aggregates": aggregates, "transcripts": entries}, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(entries, aggregates, meta), encoding="utf-8")

    n_figures = sum(len(e["figures"]) for e in entries)
    n_salient = sum(1 for e in entries for f in e["figures"] if f["salient"])
    n_topics = sum(len(e["topics"]) for e in entries)
    print(
        f"\nRendered {len(entries)} transcripts \u00b7 "
        f"{n_topics} topic labels ({len({t['topic'] for e in entries for t in e['topics']})} distinct) \u00b7 "
        f"{n_figures} figures ({n_salient} salient) \u00b7 "
        f"{len(aggregates['rare_figures'])} rare figures corpus-wide"
    )
    print(f"Wrote {_display(json_path)} and {_display(md_path)}")


if __name__ == "__main__":
    main()
