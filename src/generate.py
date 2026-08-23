"""Generate an answer from retrieved chunks, via a local LM Studio model.

The model, temperature, and prompt template are held constant across every
condition in the grid -- only the retrieved chunks passed in vary. Uses
temperature 0 so answer differences trace back to retrieval quality, not
sampling noise. See src/index.py and configs/base.json for
the sibling convention on the retrieval side (query prefix).

Generation goes through a local LM Studio server (OpenAI-compatible endpoint
on the Mac Studio), and that is the only backend there is. The generator held
constant across all 12 conditions is qwen3.8-27b@q8_k_xl, served locally, and
every reported record came from this path. `LM_STUDIO_MODEL_NAME` names the
model LM Studio has loaded.

Abstention detection, settled 2026-09-03 and measured 2026-09-09.
`evaluate.classify_outcome` does NOT test `answer == ABSTENTION`. It calls
`evaluate.contains_abstention_sentence` (Fix 3), true when the canonical
sentence appears anywhere in the response as a complete sentence;
`evaluate.abstained` keeps exact equality as a separate diagnostic. Measured
across all 540 records of the reported arm: 285 carry the `abstained`
outcome, 284 of those state the sentence alone, and one is caught by the
contains-rule only.

The match is byte-exact, hence case-sensitive, and that misses exactly one
further record. It is recorded in README.md, "Scorer fixes and known defects",
and disclosed in the thesis. The original rule is
unchanged and still binding: a divergence found after results exist is
reported and signed off, never repaired by loosening the match
mid-experiment.

`LMSTUDIO_API_KEY` must be set in the environment; no key is read or passed
in code. The client is not constructed until first use.
"""

import os
import sys
import time

import openai
from dotenv import load_dotenv

load_dotenv()

TEMPERATURE = 0

# The LM Studio server's address. It is host configuration, not an experimental
# parameter: the runs reported in the thesis reached the server over the local
# network, and where the server listens changes nothing about what it returns.
LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")


ABSTENTION = "The provided context does not contain enough information to answer this question."

SYSTEM_PROMPT = f"""You are answering questions about earnings call transcripts using ONLY the context chunks provided below.

Rules:
- Base your answer strictly on the provided context. Do not use any outside knowledge about the companies, markets, or events involved.
- If the context does not contain enough information to answer the question, respond with exactly this sentence and nothing else: "{ABSTENTION}"
- Give a direct, concise answer. Do not show your reasoning or chain of thought, and do not cite or reference chunk IDs in your answer."""

_local_client: openai.OpenAI | None = None


def get_local_client() -> openai.OpenAI:
    """Lazily construct and cache the LM Studio (OpenAI-compatible) client."""
    global _local_client
    if _local_client is None:
        _local_client = openai.OpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key=os.environ["LMSTUDIO_API_KEY"],
            timeout=600.0,  # queued requests block under LM Studio's concurrency cap; a short timeout looks like a hang
            max_retries=0,  # retries deepen the queue, they never fix a timeout
        )
    return _local_client


def format_context(retrieved_chunks: list[dict]) -> str:
    """Format retrieved chunks into the context block, prefixed by chunk_id
    for the audit trail.
    """
    return "\n\n---\n\n".join(f"[{chunk['chunk_id']}]\n{chunk['text']}" for chunk in retrieved_chunks)


def _generate_local(query: str, retrieved_chunks: list[dict]) -> dict:
    model_name = os.environ["LM_STUDIO_MODEL_NAME"]
    context = format_context(retrieved_chunks)
    user_message = f"Context:\n\n{context}\n\nQuestion: {query}"

    start = time.monotonic()
    response = get_local_client().chat.completions.create(
        model=model_name,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        extra_body={"reasoning_effort": "none"},  # both loaded models default reasoning on; "none" avoids hundreds of wasted reasoning tokens per call (server rejects "off" -- valid values are none/minimal/low/medium/high/xhigh)
    )
    latency = time.monotonic() - start

    # LM Studio returns HTTP 200 even for unrecognized endpoints -- validate response shape, not status.
    if not response.choices or not response.choices[0].message.content:
        raise RuntimeError(f"LM Studio returned an unexpected response shape for model={model_name!r}: {response!r}")
    answer = response.choices[0].message.content.strip()

    prompt_tokens = getattr(response.usage, "prompt_tokens", "n/a")
    print(
        f"[local generate] model={model_name} reasoning_effort=none temperature={TEMPERATURE} "
        f"prompt_tokens={prompt_tokens} latency={latency:.2f}s",
        file=sys.stderr,
    )

    return {
        "answer": answer,
        "model": model_name,
        "chunk_ids": [chunk["chunk_id"] for chunk in retrieved_chunks],
        "abstained": answer == ABSTENTION,
    }


def generate(query: str, retrieved_chunks: list[dict]) -> dict:
    """Generate an answer to `query` grounded only in `retrieved_chunks`.

    Calls the local LM Studio server (see module docstring). Returns a dict
    with the generated answer, the model actually used, the chunk_ids fed
    in, and whether the model abstained (answer matches ABSTENTION exactly)
    -- enough to audit both what went in and what came out.
    """
    return _generate_local(query, retrieved_chunks)


LOCAL_MAX_CONCURRENCY = 4

_local_async_client: openai.AsyncOpenAI | None = None


def get_local_async_client() -> openai.AsyncOpenAI:
    """Lazily construct and cache the async LM Studio client.

    Same settings as the sync client: a long timeout because requests queue
    behind LM Studio's concurrency cap, and no retries because a retry only
    deepens that queue.
    """
    global _local_async_client
    if _local_async_client is None:
        _local_async_client = openai.AsyncOpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key=os.environ["LMSTUDIO_API_KEY"],
            timeout=600.0,
            max_retries=0,
        )
    return _local_async_client


async def _generate_local_async(query: str, retrieved_chunks: list[dict], semaphore) -> dict:
    """One local-backend call, gated by `semaphore`. Mirrors _generate_local."""
    model_name = os.environ["LM_STUDIO_MODEL_NAME"]
    context = format_context(retrieved_chunks)
    user_message = f"Context:\n\n{context}\n\nQuestion: {query}"

    async with semaphore:
        response = await get_local_async_client().chat.completions.create(
            model=model_name,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            extra_body={"reasoning_effort": "none"},
        )

    if not response.choices or not response.choices[0].message.content:
        raise RuntimeError(f"LM Studio returned an unexpected response shape for model={model_name!r}: {response!r}")
    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "model": model_name,
        "chunk_ids": [chunk["chunk_id"] for chunk in retrieved_chunks],
        "abstained": answer == ABSTENTION,
    }


def generate_many(jobs: list[tuple[str, list[dict]]]) -> list[dict]:
    """Generate answers for many (query, retrieved_chunks) pairs, in order.

    Bounded concurrency of 4, because the server is configured for max concurrency 4. Do NOT
    expect a 4x speedup -- measured ~27% over sequential (29.4s vs 40.3s for
    4 calls), because the four slots share compute rather than running as
    independent workers.

    Returns results in the SAME ORDER as `jobs` regardless of completion
    order, so a per-question log can be zipped back against its questions.
    Temperature is 0, so concurrency changes throughput only, never the
    answers.
    """
    import asyncio

    async def run_all() -> list[dict]:
        semaphore = asyncio.Semaphore(LOCAL_MAX_CONCURRENCY)
        return await asyncio.gather(*(_generate_local_async(q, c, semaphore) for q, c in jobs))

    start = time.monotonic()
    results = asyncio.run(run_all())
    elapsed = time.monotonic() - start
    print(
        f"[local generate_many] {len(jobs)} calls at concurrency={LOCAL_MAX_CONCURRENCY} "
        f"in {elapsed:.1f}s ({elapsed / max(len(jobs), 1):.2f}s/call)",
        file=sys.stderr,
    )
    return results
