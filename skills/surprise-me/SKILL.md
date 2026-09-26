---
name: surprise-me
description: Use when the owner wants a result well above ordinary - rival plans compete in rounds, scored by a hostile judge on a rubric fixed first, until one scores 80 of 100; not when one plain answer will do.
disable-model-invocation: true
---

# surprise-me

Beat the ordinary answer on the topic, the one named or else the conversation's:
rival plans, a hostile judge, and rounds until the result scores 80 of 100.

## Before any plan

- Read the owner's words as meant: a figure of speech is its sense, not a tool
  or term of the same name. Where readings lead to different work, write each
  with the answer it implies, and keep the one the owner's other words support.
- An undefined term or an open choice is yours to settle, never handed back.
- Fix the rubric in a file: 3-6 weighted lenses, each anchored in one line on
  what scores 50 (the ordinary or current result) and 100 (the ideal expert's).
- Fit to the reading is a gate, not a lens: a plan that misses it is out.

## A round

- Brief 3 read-only planner subagents alike: the reading, the context files,
  the open questions, a 60-line cap. Each builds a different mechanism, not
  just a different stance, and ends with the 3 strongest attacks on its plan.
- Planners never see the rubric, so they solve the problem, not the test.
- Write the plans into one file with a file tool, labelled in shuffled order,
  and hand the judge its path.
- The judge is one more subagent, neither a planner nor you, and hostile. It
  checks every claim against the files, citing `path:line`, and uses the
  planners' attacks as its red team. A wrong claim costs points, and so does a
  criterion that cannot fail or that the honest empty outcome cannot pass;
  length earns nothing. It applies the gate, then scores each lens with a
  one-line reason. It never sees an earlier round's scores.
- It grafts at most 3 ideas from the losers that lower none of the winner's
  heaviest lenses, each credited by name, and writes the grafted plan as
  answers to the same questions.
- Recompute the weighted totals with a script, never the judge's arithmetic.

## Rounds

- A grafted plan is unjudged: it competes in the next round against the 3
  planners' new plans, their briefs now carrying the judge's findings.
- Stop when the winner's weighted total is at least 80. Stop earlier when the scores across
  rounds have flattened with little gain and no new way out, and say so with
  the best score reached. There is no fixed round cap.

## Output

- Spend one cheap check on the judge's key findings first.
- Give the winning plan, its score per lens, the reading it answers and the
  credited grafts, in your own message, never left in a subagent's scratch.
- Post any artifact from a file written with a file tool (`--body-file
  <path>`), never a shell heredoc, which a guard may refuse whole.
- The answer goes to chat by default, and into a document as well when one is
  asked for.
