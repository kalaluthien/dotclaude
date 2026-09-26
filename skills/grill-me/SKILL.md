---
name: grill-me
description: Use when the answer is still the user's to make - a decision, a proposal or a plan with open choices to settle by asking them; not when the facts settle it or code is under review.
---

# grill-me

Follows upstream `grill-me`, which calls `grilling`:
https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grilling/SKILL.md

Interview the user relentlessly until you reach a shared understanding. Map
this as a **design tree**: every decision branches into the decisions that hang
off it. A blank another skill hands you is one decision in it.

Work the tree in **rounds**. The **frontier** is every decision whose
prerequisites are already settled. A question whose answer depends on another
question still open in this round belongs to a later round.

## Asking a round

- Every round is one `AskUserQuestion` call of at most four questions, and
  nothing else: no numbered text, no pasted-back block. Then wait.
- Pick the four from the frontier by impact first - the answer that changes
  the most of the tree - then by conceptual order, a concept before the
  choices built on it. The rest of the frontier waits.
- Choose each next round from the answers so far: recompute the frontier,
  drop questions an answer made moot, and ask the next four the same way.
- Before each round after the first, write one line of what the last round
  settled, wholly in the user's language, its label included (`Settled: …`,
  `정한 것: …`).
- A free-text answer is not settled as typed: restate it as a concrete
  proposal in the next round ("I read your last answer as: …") and settle it
  when the user confirms that.
- An objection to a settled answer - yours, after attacking it once with a
  counterexample, an edge case or a check that can fail - is its own question
  in the next round, its header tagged `[objection]` in the user's language.
- An answer that is itself a question is answered with facts in the next
  round, and never recorded as a decision.
- Finding facts is your job, never the user's: check each fact a round needs
  before asking that round, by a sub-agent when the search is wide. The
  decisions are the user's.

## Question shape

Each question is answerable without opening a file. Its body carries:

- the current state, quoting the rule and its `path:line`;
- why it matters: the failure the choice causes or prevents, with a real case
  where one exists;
- the recommended model, as bullets.

Each option's description names its downside. The recommended option is the
first, labelled `(Recommended)`.

Example (the user wrote in Korean; this is its English):

> **How should a reopened issue's branch be named?**
> Current: `repo.md:14` names a branch `<topic>-<n>`. A reopened issue keeps
> its number, so its new branch takes the name of the merged pull request's
> branch, and `stop.py` then reads "this branch's pull request is merged" and
> ends the worker at once. The worker, tab and worktree names follow the
> branch name.
> Recommended:
> - `<topic>-<n>-<k>`, `k` counting openings, for every issue
>
> Options:
> 1. `<topic>-<n>-<k>` (Recommended) - one shape for every name; downside: a
>    little longer
> 2. `<topic>-<n>` first, `-r2` only when reopened - downside: two shapes
> 3. keep the name, change the check - downside: `gh pr view <branch>` may
>    pick the old pull request

## Settling

Done when every branch of the tree is visited, nothing silently assumed, and
the user confirms a summary of the settled answers. Act on nothing before that.

## Output

The settled answers only: each decision and its answer, no transcript of the
rounds and no document. Hand them back to the caller as they are.
