---
name: asking-jev
description: Use when code needs a fast typed judgment on text or application state - a yes/no probability, one option of a set, a graded score - from TypeSafe's Jev model, or when an LLM prompt-and-parse step could become one; not when the output is generated text or multi-step reasoning (claude-api).
---

# Asking Jev

Jev is TypeSafe's System One model: one call takes a `state` and a map of
typed questions and returns a number or an option per question, with
probabilities, in well under a second. It writes no text and explains nothing.
Code owns the workflow, the known rules and the exact lookups; Jev answers only
what needs reading comprehension.

`POST https://api.typesafe.ai/v1/systemone` with `state` (string, object or
array), `model` (`jev-latest`; required over HTTP, defaulted by the SDKs) and
`questions`. The key is `TYPESAFE_API_KEY` in `~/.env`, which no shell exports:
run with `uv run --env-file ~/.env --with typesafe-sdk`. The package is
`typesafe-sdk`, imported as `typesafe_sdk`; `typesafe` on PyPI is unrelated.
`TypeSafeClient` is sync only and `AsyncTypeSafeClient` is its async twin.
Keep the key server-side in a web app.

## The question types

| the need | `type` | `criteria` | the answer |
| --- | --- | --- | --- |
| whether a condition holds; one per label when several may apply | `noul` | optional `{"true": …, "false": …}` | `noul`, the probability of yes; no `confidence` |
| one of a defined set | `choice` | `{option: description or null}` | `choice`, `probabilities`, `confidence` |
| a degree along one dimension; comparable per-item scores rank | `score` | ordered level descriptions, each a concrete situation | `score` between level indexes, `probabilities`, `confidence` |

Put the judgment in `instructions` and the meaning of each answer in
`criteria`; both take a string or JSON structure. The question id never reaches
the model, so the instructions carry the whole meaning. Name several-part state
as JSON fields and point at one with a backticked path,
`ticket.messages[0].text`. One narrow judgment per question, and every
independent question over the same state in one call: forty cost the latency
of one and cannot see each other's answers. A second call is for an answer
that must fetch evidence or build the next options.

## Silent failures

- A `choice` with no fitting option still picks one with high `confidence`:
  an off-topic message scored 0.96. Add a no-match option; `confidence`
  measures how concentrated the distribution is, not whether the set fits.
- A `noul` near 0.5 means yes and no are equally likely, not a medium degree.
  Degree is a `score`.
- The same request returns probabilities a few hundredths apart. Assert a band
  in tests, never a float, and keep a threshold off the values observed.
- A `score` with one level returns 200 and `confidence` 1.0, though two is the
  documented minimum.
- `jev-latest` moves on release. The response's `model` names the version that
  answered; pin that once thresholds are tuned.
- A missing key is 403, a wrong key 401. 429 and 529 are retried by the SDKs;
  over raw HTTP back off.
- Typed output guarantees the shape, not the truth. Thresholds come from a run
  over the user's own cases, including one that fits no option, gated by the
  cost of acting wrongly; a cookbook's numbers are examples.

## The live docs

The docs hold the contracts and move faster than this file. Read the index,
<https://docs.typesafe.ai/llms.txt>, then only the pages the task needs; any
page path plus `.md` is Markdown. Read the SDK page before writing the
integration, and the nearest cookbook before designing a new workflow, since
it often decomposes better than a single classifier.

| the task | the page under `https://docs.typesafe.ai/` |
| --- | --- |
| call shape, errors | `api.md`, `sdk/python.md`, `sdk/javascript.md` |
| writing questions and state | `primitives.md`, `primitives/advanced.md`, `concepts/state.md` |
| thresholds | `confidence.md`, `patterns/confidence-routing.md` |
| route a request and fill its arguments | `cookbooks/function_calling.md`, `patterns/fan-out.md` |
| pick a value out of source text | `cookbooks/pre_parsed_value_extraction_cookbook.md` |
| rank or rerank candidates | `cookbooks/rerank_typesafe.md`, `patterns/composite-scoring.md` |
| check a claim against its evidence | `cookbooks/citation_check.md`, `cookbooks/sde_cascade.md` |
| price, limits, versions | `models.md` |
