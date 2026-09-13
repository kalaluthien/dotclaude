---
name: grill-me
description: Interviews the user until a target document is filled - a campaign issue, a sub-issue, a proposal or a decision - each blank a question and each answer attacked before it is written. Use when the user wants an idea or plan stress-tested or a document drafted by interview - 검토해줘 이 아이디어, 둘 다 어찌하면 좋을까, grill me. Not for reviewing code (code-review) or explaining a topic (show-me).
---

# grill-me

The document to produce decides the questions: each blank in it is one. With
no target named, ask which, once.

## The targets

| target | its blanks | the result |
| --- | --- | --- |
| a campaign issue, a sub-issue | the repository's own template, found through its `AGENTS.md` and read now, never copied | its markdown body |
| a proposal | a `comparison`'s parts, [doctype](../show-me/references/doctype.md) § Doctypes | markdown, or `assets/comparison.html` |
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

- In chat by default: `AskUserQuestion` for a round of four questions or
  fewer, its limit; numbered text otherwise.
- As a form when the `Artifact` tool is in the session and a round holds more
  than four: one fieldset per question in `assets/form.html`, recommendations
  prefilled, held to doctype.md § Media. The page writes nowhere; it builds
  one block the user pastes back, and the attacks follow in chat.
- At the end, unless the ask already says, ask once where the document goes:
  a GitHub issue, an artifact, or chat. When it is obvious, do not ask. A
  GitHub issue is filed by the repository's own procedure where it has one,
  else `gh issue create`; an artifact is held to doctype.md § Media, its
  probe included.
