---
name: grill-me
description: Use when the answer is still the user's to make; not when the facts settle it (show-me) or the code is under review (code-review).
---

# grill-me

The document to produce decides the questions: each blank in it is one. A
target the ask does not name is a proposal.

## The targets

| target | its blanks | the result |
| --- | --- | --- |
| a campaign issue, a sub-issue | the repository's own template, found through its `AGENTS.md` and read now, never copied | its markdown body |
| a proposal, a single idea being one weighed against leaving things as they are | a `comparison`'s parts, [doctype](../../shared/doctype.md) § Doctypes | markdown |
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
- Attack each answer before writing it: a counterexample or an edge case, a
  check that can fail, a term the repository uses otherwise, or
  code that says otherwise. Write it once it survives, or once the user
  restates it knowing the attack.
- Done when every blank is filled and the user confirms the document; act on
  nothing before.

## Where a round is asked

| the round | where |
| --- | --- |
| four questions or fewer | `AskUserQuestion`, its limit |
| more, with the `Artifact` tool in the session | `assets/form.html` through that tool: one fieldset per question, its recommendation prefilled |
| more, without it | numbered text in chat |

The form writes nowhere; it builds one block the user pastes back, whose first
line is `grill-me: <target>, round <n>`: read it against that round, or say it
matches none. Under each `Qn:` line, indented two spaces, is that answer
verbatim; one equal to its recommendation accepts it, an empty one leaves the
question open. The attacks follow in chat.

Before publishing, it passes the [probe](../../shared/doctype-probe.md), whose
controls count includes the button.

## The ending

[delivery](../../shared/doctype-delivery.md); an artifact or a repository
page is show-me's, invoked with the document.
