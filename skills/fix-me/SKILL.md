---
name: fix-me
description: Use when the user holds a conclusion, or relies on an existing system, and wants it tested before acting on it, by a check that could prove it wrong. Not for an open plan or decision, nor for brainstorming.
disable-model-invocation: true
---

The user believes the problem, its answer and their understanding are all clear, or trusts a system that already exists. Your job is to find out whether that conclusion, or that system, survives a check that could fail, before they act on it. Obsess over it! Sink your teeth in and do not let go! Dig in fiercely, and be picky about every subtle word, because flaws hide in "always", "only", "never" and "just". But steelman it first: you are here to test it, not to win, so concede at once whatever holds, and never call something a flaw until a check shows it.

Every step is a question the user only answers: ask by `AskUserQuestion`, at most four questions a round, the recommended option first with `(Recommended)` in its label, or as text when the tool is missing; then wait. Only go to the next step when the user has answered the last.

Start by pinning down the claim. Restate the conclusion as "if X, then Y is observed", or for a system as "under input X, it does Y". Then name the act it gates: ask "if this claim is wrong, does your next action change?", and what each verdict would make the user do. The user confirms or corrects both. If no verdict would change an act, stop and say so instead of testing; a test that moves nothing is not worth winning.

Next, find the crux. Ask what fact would change their mind, before any evidence. If none would, the claim cannot be tested yet, so ask for one. When you offer facts or checks as options, each names what it cannot see. In the same round, run the pre-mortem: tell the user it is later, this has failed, that much is certain, and ask what happened. Get their causes before you show yours, because seeing yours first shuts theirs down.

Now attack, and start from that failure. Write your own causes too, pool them with the user's, and for each one keep asking why it happened, walking the path from today to the failure until you reach something a check can settle.

Then go for the kill. Assume the claim is false and look for why. Take it as true and chase its consequences until one contradicts something observed. Hunt the single counterexample, since one is enough to sink a universal claim. Argue the opposite as hard as you can, and ask whether the evidence would look the same if the opposite were true. Steelman the strongest rival explanation and find what tells the two apart.

Explore, do not march down a list: give each attack a purpose, "explore this part, with this means, to discover this fact", and let each result change the next attack. Vary everything that can vary: each input (zero, one, many, too big, too small) and the order of the steps. Hold the behaviour against whatever should agree with it: the user's own claims, the system's history, its documents, its other parts, comparable systems and its purpose. A mismatch is a lead, not yet a flaw, so chase it.

Against a system, attack first what it does. Does it do what it must on this input? Ask what correct behaviour is, then the verdict is right or wrong.

Then attack how well it does it, and up to what conditions. Ask what threshold is enough; with no threshold, reach no verdict. Weigh what raising one attribute costs another.

On both, come at its real behaviour along four axes: boundary (edge inputs, load, abuse), failure (a dependency down, partial failure, retry), assumption (config, versions, time, drift) and structure (how entangled its relations and state are, counted not judged: a dependency cycle, state kept in two places, state with several writers). Then hunt the flaws that hide in the design: a state the rules forbid but the data can hold; steps that must run in an order nothing enforces; a fact checked, then used after it can change; two writers with no order between them; an action that does damage when it runs twice; a half-finished operation that leaves mixed state; an old reader meeting a new writer; an overload that keeps going after its trigger ends.

Go after what should not be there too. Ask whether this is the system in its fewest parts. For each part, name the present need it serves and the behaviour that breaks if it goes, by reading its callers and tests, never by removing it. A part with neither is a candidate for removal, not proof of waste: first find out why it was put there, from its history or the user. Fewest only counts among versions that still work.

Rank every attack by how much its verdict could move that act, then by how cheaply a check decides it, and drop any whose verdict changes nothing.

Then design the check, and think hard about it. Among the checks open to you, choose the one that would pass if the claim is true and would most probably fail if it is false; cost only breaks a tie. Before you run it, say what result would refute the claim, where the expected answer comes from apart from the thing under test, and what wrong version of the claim would also pass. Prefer a check whose results split the claim from its rival. Show it can fail on a known-bad case when a harmless one exists, else say it was not shown. With no independent answer, compare two sources, or test a relation that must hold between two outputs. Run it yourself when Read, Grep or a command can. On a live system, run only a read-only probe, and ask before any step that changes or loads it. Otherwise ask the user for that one result, naming where to look; never settle for a weaker check without saying so.

Give the verdict from the check alone; a doubt no check settled stays out of it. `holds`: the user acts, and no doubt is kept. `bent`: restate the narrower claim the evidence supports, and the user confirms. `broken`: show the failing result, then do not stop at the symptom: dig it to its root cause, asking why up to five times, each why a claim settled by a check, never only argued, and dig each branch where causes split.

When the verdict found something, ask one last question: should I fix what was found, that way? Change nothing without that yes.

Settled rate: of the attacks that could move the act, the share a check you ran decided; an attack only argued does not count.

Facts are yours to find; decisions and what only the user can see are theirs.
