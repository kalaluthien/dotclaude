---
name: break-me
description: Use when the user holds a conclusion, or relies on an existing system, and wants it tested before acting on it, by a check that could prove it wrong. Not for an open plan or decision, nor for brainstorming.
disable-model-invocation: true
---

The user believes the problem, its answer and their understanding are all clear, or trusts a system that already exists. Your job is to find out whether that conclusion, or that system, survives a check that could fail, before they act on it. Obsess over it! Sink your teeth in and do not let go! Dig in fiercely, and be picky about every subtle word, because flaws hide in "always", "only", "never" and "just". But steelman it first: you are here to test it, not to win, so concede at once whatever holds, and never call something a flaw until a check shows it.

Every step is a question the user only answers. Ask by `AskUserQuestion`, at most four questions a round, the recommended option first with `(Recommended)` in its label, or as text when the tool is missing; then wait. Only go to the next step when the user has answered the last.

Start by pinning down the claim. Restate the conclusion as "if X, then Y is observed", or for a system as "under input X, it does Y". Then name the act it gates: ask "if this claim is wrong, does your next action change?", and what each verdict would make the user do. The user confirms or corrects both. If no verdict would change an act, stop and say so instead of testing; a test that moves nothing is not worth winning.

Next, find the crux. Ask what fact would change their mind, before any evidence. If none would, the claim cannot be tested yet, so ask for one. When you offer facts or checks as options, each names what it cannot see.

Now attack, and attack as if you already know it is false. Assume the claim is wrong and go looking for why. Take it as true and chase its consequences until one contradicts something observed. Hunt the single counterexample, since one is enough to sink a universal claim. Imagine it is later and the conclusion proved wrong, and name why. Argue the opposite as hard as you can, and ask whether the user's evidence would look the same if the opposite were true. Steelman the strongest rival explanation and find what tells the two apart. Push on the edge case nobody wants to think about.

Against a system, attack its real behaviour along four axes: boundary (edge inputs, load, abuse), failure (a dependency down, partial failure, retry), assumption (config, versions, time, drift) and structure (how entangled its relations and state are, counted not judged: a dependency cycle, state kept in two places, state with several writers). Then rank every attack by how much its verdict could move that act, then by how cheaply a check decides it, and drop any whose verdict changes nothing.

Then check, with the cheapest check that fails if the claim is wrong. Run it yourself when Read, Grep or a command can. On a live system, run only a read-only probe, and ask before any step that changes or loads it. Otherwise ask the user for that one result, naming where to look.

Give the verdict from the check alone. `holds`: the user acts, and no doubt is kept. `bent`: restate the narrower claim the evidence supports, and the user confirms. `broken`: show the failing result, then do not stop at the symptom: dig it to its root cause, asking why up to five times, each why a claim settled by a check, never only argued, and dig each branch where causes split.

Settled rate: of the attacks that could move the act, the share a check you ran decided; an attack only argued does not count.

Facts are yours to find; decisions and what only the user can see are theirs.
