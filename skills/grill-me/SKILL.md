---
name: grill-me
description: Use when the answer is still the user's to make - a decision, a proposal or a plan with open choices to settle by asking them; not when the facts settle it (show-me) or code is under review.
---

# grill-me

Follows upstream `grill-me`, which calls `grilling`:
https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grilling/SKILL.md

Interview the user relentlessly until you reach a shared understanding. Map
this as a **design tree**: every decision branches into the decisions that hang
off it. A blank another skill hands you is one decision in it.

Work the tree in **rounds**. The **frontier** is every decision whose
prerequisites are already settled. Ask the whole frontier in one round: number
each question `Q1`, `Q2`, and give your recommended answer. Then wait. A
question whose answer depends on another question still open in this round
belongs to a later round.

## Asking a round

- **Four questions or fewer:** `AskUserQuestion`, one question each, your
  recommended answer as the first option, labelled `(Recommended)`.
- **More than four:** publish a plain page with the Artifact tool. Plain means
  plain: no design system, no stylesheet, no `style` attribute, only browser
  defaults, so skip the design pass. The page holds the target and round
  number, then per question its `Qn` title and body and one `textarea`
  prefilled with your recommended answer, and one button. The button builds
  this block into a read-only `textarea` and copies it to the clipboard:

  ```text
  grill-me: <target>, round <n>
  Q1:
    <answer, every line indented two spaces>
  Q2:
    <answer>
  ```

  Give the user the page url and ask them to paste the block back. Read a
  pasted block as the answers of that round: each `Qn:` takes the indented
  lines under it.

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
rounds. Hand them by name to `mumu-document:writing-documents` when that skill
is available, else to `show-me`.
