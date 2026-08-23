"""Canonical, dependency-free model-scoped result paths.

Why this is its own module
--------------------------
The generation cache and the published tables are both scoped by generator
model, and six analysis scripts need to resolve those paths. `run_generation`
owns the writing side, but importing it pulls in faiss, sentence-transformers
and the whole retrieval stack -- far too heavy for a script that only wants to
read a CSV. Duplicating the slug rule in each reader is the alternative, and
that is exactly the kind of second implementation that drifts.

So the rule lives here, imports nothing beyond the standard library, and
`run_generation` re-exports `model_slug` for its existing callers.

Layout, for one generator `M` with slug `S = model_slug(M)`:

    results/generation/S/{condition_id}/{question_id}.json   generations
    results/tables/S/generation_outcomes.csv                 scored table
    results/tables/S/case_outcome_breakdown.csv              breakdown
    results/tables/S/generation_coverage.json                coverage record
    results/tables/S/subset/{condition_ids}/...              partial-grid runs

Not model-scoped, deliberately:

    results/tables/retrieval_metrics.csv   retrieval only, no generator
    results/tables/prefix/                 frozen pre-fix q4 tables; historical,
                                           nothing writes there; the evidence for
                                           the documented scorer fix
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
GENERATION_DIR = RESULTS_DIR / "generation"
ANALYSIS_DIR = REPO_ROOT / "analysis"
EXPECTATIONS_DIR = ANALYSIS_DIR / "expectations"

DEFAULT_MODEL = "qwen3.8-27b@q4_k_xl"

_SLUG_UNSAFE = re.compile(r"[^a-z0-9._-]+")


def model_slug(model_name: str) -> str:
    """Filesystem-safe directory name for a generator model identifier."""
    return _SLUG_UNSAFE.sub("_", model_name.strip().lower())


def model_tables_dir(model_name: str) -> Path:
    """Published tables for one generator."""
    return TABLES_DIR / model_slug(model_name)


def generation_outcomes_path(model_name: str) -> Path:
    return model_tables_dir(model_name) / "generation_outcomes.csv"


def case_outcome_breakdown_path(model_name: str) -> Path:
    return model_tables_dir(model_name) / "case_outcome_breakdown.csv"


def generation_coverage_path(model_name: str) -> Path:
    return model_tables_dir(model_name) / "generation_coverage.json"


def prefix_generation_outcomes_path() -> Path:
    """The frozen PRE-fix table. q4-only and historical; not model-scoped."""
    return TABLES_DIR / "prefix" / "generation_outcomes.csv"


# ---------------------------------------------------------------------------
# analysis/ documents -- the same Option C scoping, applied to the second surface
# ---------------------------------------------------------------------------
#
# results/ was scoped by generator; analysis/ was not, and every document,
# validation target and pinned expectation there silently assumed q4. Running an
# analysis under another generator therefore either validated q8 rows against a
# q4 reference or overwrote a q4 document with q8 content.
#
# Every generator's documents live under `analysis/<slug>/`, DEFAULT_MODEL
# included. Generator-INDEPENDENT documents (Stage 1, corpus) live under
# `analysis/stage1/` via stage1_path() and belong to no model.
# The historical note below is kept because it explains why the q4
# documents were once at the top of analysis/:
# DEFAULT_MODEL formerly kept the BARE `analysis/<name>` paths rather than moving to
# `analysis/<slug>/<name>`. That asymmetry is deliberate and is the whole reason
# this migration needs no file to move: the q4 documents are committed and are the reference the q4 regression check reproduces. Relocating
# them to satisfy a naming symmetry would break every citation and force a
# regeneration of exactly the artifacts whose byte-identity is the evidence.
# Every non-default generator gets its own subdirectory, so no two generators can
# ever write the same document.


STAGE1_ANALYSIS_DIR = ANALYSIS_DIR / "stage1"


def stage1_path(filename: str) -> Path:
    """A generator-INDEPENDENT analysis document.

    Stage 1 is retrieval-only and the corpus diagnostics never call a generator,
    so these documents serve every arm at once. Filing them under a model slug
    would assert a dependency that does not exist -- the same reason
    `results/retrieval/` is not model-scoped.
    """
    return STAGE1_ANALYSIS_DIR / filename


def analysis_dir(model_name: str) -> Path:
    """Directory holding one generator's analysis documents.

    Every generator gets `analysis/<slug>/`, DEFAULT_MODEL included. The earlier
    asymmetry (q4 resolving to bare `analysis/`) made the directory listing read
    as though the q4 documents were unowned, and mixed them with the Stage 1
    documents that genuinely belong to no generator.
    """
    return ANALYSIS_DIR / model_slug(model_name)


def analysis_path(model_name: str, filename: str) -> Path:
    """One analysis document, scoped to a generator."""
    return analysis_dir(model_name) / filename


def ensure_analysis_dir(model_name: str) -> Path:
    """analysis_dir(), created if missing. Call before writing a document."""
    d = analysis_dir(model_name)
    d.mkdir(parents=True, exist_ok=True)
    return d


def expectations_path(model_name: str) -> Path:
    """The pinned-figure set for one generator.

    Expectations are per-model DATA, not literals in the scripts, so that a
    second generator cannot inherit the first one's pins by default -- the
    absence of a file is what makes a first run announce itself instead of
    silently comparing against numbers from another model.
    """
    return EXPECTATIONS_DIR / f"{model_slug(model_name)}.json"


def load_expectations(model_name: str) -> dict | None:
    """Pinned figures for one generator, or None when no set exists.

    None means FIRST RUN: the caller must say so loudly and must NOT report a
    pass. It must never be treated as "nothing to check, therefore fine".
    """
    path = expectations_path(model_name)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
