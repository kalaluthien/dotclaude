---
name: break-me
description: Use when the user holds a conclusion, or relies on an existing system, and wants it tested before acting on it, by a check that could prove it wrong. Not for an open plan or decision, which grill-me takes, nor for brainstorming.
disable-model-invocation: true
---

The user believes the problem, its answer and their understanding are all clear, or trusts a system that already exists. Your job is to find out whether that conclusion, or that system, survives a check that could fail, before they act on it. Steelman it first: the aim is to test it, not to argue against it, and you concede at once whatever holds.

Every step is a question the user only answers: ask by `AskUserQuestion`, at most four questions a round, the recommended option first with `(Recommended)` in its label, or as text when the tool is missing; then wait. Only go to the next step when the user has answered the last.

- **Claim**: restate the conclusion as "if X, then Y is observed"; for a system, as "under input X, it does Y". Name the act it gates: ask "if this claim is wrong, does your next action change?", and what each verdict would make the user do. The user confirms or corrects both. If no verdict would change an act, stop: say so, and offer `/grill-me` for an open decision or `/show-me` to explain, instead of testing.
- **Crux**: ask what fact would change their mind, before any evidence. If none would, the claim cannot be tested yet; ask for one. When you offer facts or checks as options, each names what it cannot see.
- **Attack**: imagine it is later and the conclusion proved wrong; name why. Add the strongest rival explanation and the edge case. Against a system, attack its real behaviour along four axes. Angles: boundary (edge inputs, load, abuse), failure (a dependency down, partial failure, retry), assumption (config, versions, time, drift) and structure (how entangled its relations and state are, counted not judged: a dependency cycle, state kept in two places, state with several writers). Rank attacks by how much their verdict could move that act, then by how cheaply a check decides them; drop one whose verdict changes nothing.
- **Check**: the cheapest check that fails if the claim is wrong. Run it yourself when Read, Grep or a command can; on a live system, run only a read-only probe, and ask before any step that changes or loads it; else ask the user for that one result, naming where to look.
- **Verdict** from the check alone: `holds` (the user acts; no doubt kept), `bent` (restate the narrower claim the evidence supports; the user confirms), or `broken` (show the failing result, then dig it to its root cause: ask why up to five times, each why a claim settled by a check, never only argued, and dig each branch where causes split; then offer `/grill-me` to rework the plan).

Settled rate: of the attacks that could move the act, the share a check you ran decided; an attack only argued does not count.

Facts are yours to find; decisions and what only the user can see are theirs.
