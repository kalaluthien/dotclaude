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
- Make each question answerable without reading a file: its text says the
  current state, why the choice matters, and what it decides downstream; each
  option's description gives its trade-off. Your recommended answer is the
  first option, labelled `(Recommended)`.

## Settling

- Finding facts is your job, never the user's. When a frontier question needs a
  fact from the environment, dispatch a sub-agent to find it; only the
  questions downstream of it wait. The decisions are the user's.
- Attack each answer once before settling it: a counterexample, an edge case,
  or a check that can fail. Put the objection in the next round.
- Done when the frontier is empty: every branch visited, nothing silently
  assumed. Act on nothing until the user confirms the shared understanding.

## Output

The settled answers only: each decision and its answer, no transcript of the
rounds and no document. Hand them back to the caller as they are.
