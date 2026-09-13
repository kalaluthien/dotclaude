---
name: grill-me
description: Interviews the user until a target document is filled - a campaign issue, a sub-issue, a proposal or a decision - each blank a question and each answer attacked before it is written. Use when the user wants an idea or plan stress-tested or a document drafted by interview - 검토해줘 이 아이디어, 둘 다 어찌하면 좋을까, grill me. Not for reviewing code (code-review) or explaining or comparing what the facts already settle (show-me).
---

# grill-me

The document to produce decides the questions: each blank in it is one. A
target the ask does not name is a proposal.

## The targets

| target | its blanks | the result |
| --- | --- | --- |
| a campaign issue, a sub-issue | the repository's own template, found through its `AGENTS.md` and read now, never copied | its markdown body |
| a proposal, a single idea being one weighed against leaving things as they are | a `comparison`'s parts, [doctype](../../types/doctype.md) § Doctypes | markdown |
| a decision | a numbered veto table: `#`, ruling, reason, one line each | markdown |

A repository's template or rule decides the rest of a document -- a title, a
first line, a ceiling -- and is read at run time, never restated here.

## The rounds

- Map the blanks as a tree: a blank waits while one it rests on is open, as a
  Definition of done waits on its Scope.
- Each round asks the whole frontier, every blank whose prerequisites are
  settled, and nothing downstream of an open one. Number each question `Q1`,
  `Q2`, and put `Recommended:` with your answer under it. Then wait.
- Finding facts is yours: look them up, by a subagent where it takes a
  search, and put only decisions to the user. A pending lookup holds back
  only the blanks under it.
- Attack each answer before writing it: a counterexample or an edge-case
  scenario, a check that can fail, a term the repository uses otherwise, or
  code that says otherwise. Write it once it survives, or once the user
  restates it knowing the attack.
- Done when every blank is filled and the user confirms the document; act on
  nothing before.

## Where a round is asked

| the round | where |
| --- | --- |
| four questions or fewer | `AskUserQuestion`, its limit |
| more, with the `Artifact` tool in the session | `assets/form.html` through that tool once it passes show-me's [probe](../show-me/references/probe.md): one fieldset per question, its recommendation prefilled |
| more, without it | numbered text in chat |

The form writes nowhere; it builds one block the user pastes back. Its first
line is `grill-me: <target>, round <n>`: read the block against that round, or
say it matches none. Each `Qn:` line opens that question's answer, the lines
under it indented two spaces are the answer verbatim, an answer equal to its
recommendation accepts it, and an empty one leaves the question open. The
attacks follow in chat.

## The ending

As show-me's [delivery](../show-me/references/delivery.md), with the filled
document as the result; an artifact is show-me's to render, invoked with it.
