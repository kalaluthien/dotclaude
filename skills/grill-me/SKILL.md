---
name: grill-me
description: Use when the answer is still the user's to make - a decision, a proposal or a plan with open choices to settle by asking them; not when the facts settle it (show-me) or code is under review.
---

# grill-me

Settle a document with the user: each blank in it is one question.

- A question waits while one it rests on is open; each round asks every
  question whose prerequisites are settled, numbered `Q1`, `Q2`, each with
  `Recommended:` and your answer under it, through `AskUserQuestion` when it
  holds four or fewer, else as numbered text; then wait.
- Facts are yours to find, not the user's to answer.
- Attack each answer once before writing it: a counterexample, an edge case,
  or a check that can fail.
- Done when every blank is filled and the user confirms the document; act on
  nothing before that. Then hand it to `show-me` to deliver.
