---
name: grill-me
description: Use when the user wants to stress-test a plan, decision, or idea by being grilled on its open choices. Not when the facts settle it or code is under review.
disable-model-invocation: true
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask a round as one `AskUserQuestion` call of at most four questions from the frontier, picked by impact first (the answer that changes the most of the tree), then by concept order (a concept before the choices built on it); the rest of the frontier waits. Then wait for the user's answers before the next round.

Shape each question so it is answerable without opening a file:

- its body gives the current state, quoted with its `path:line`, and why it matters: the failure the choice causes or prevents, with a real case where one exists;
- each option's description names its cost as a number and its downside;
- the recommended option comes first, its label ending in `(Recommended)`.

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Before each round after the first, write one line of what the last round settled, wholly in the user's language, its label included (`Settled: …`, `정한 것: …`). Then, in that round:

- a free-text answer is restated as a concrete proposal ("I read your last answer as: …") and settled once the user confirms it;
- an objection to a settled answer, yours after attacking it once with a counterexample, an edge case or a check that can fail, is its own question, its header tagged `[objection]` in the user's language;
- an answer that is itself a question is answered with facts, never recorded as a decision.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms a summary of the settled answers: each decision and its answer, no transcript of the rounds. When no one can answer (a non-interactive run), take each recommended option and say so in the summary.

Then judge from the context where the settled answers should live, such as the project's `README.md`, an issue, or a spec file, and ask the user where to keep them, the likeliest first; never pick one destination yourself. In a non-interactive run, this question is the run's last text.
