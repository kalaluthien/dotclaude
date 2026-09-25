---
name: show-me
description: Use when the answer is settled and must be shown in chat - explain, draw, map, walk through or compare something as a markdown answer; not when the answer is still the user's to make (grill-me), nor for a page, Artifact, HTML, issue body, PR body or repository doc (mumu-document:writing-documents).
---

# show-me

Show the topic, the one named or else the conversation's, in chat. Skip the
preamble, keep prose brief, and pick the smallest widget that makes the point.
A blank is not shown: hand it to `grill-me`.

Answer in chat only, as markdown that reads the same in a terminal and in web
chat. An ask for a page, Artifact, HTML, issue body, PR body or repository doc
is not this skill's: hand it to `mumu-document:writing-documents` by that name,
and when that skill is not available, answer in chat and say so.

## Widgets

Every widget is plain markdown: a table or a fenced `text`, `diff` or source
block. Nothing needs HTML or a renderer.

**Pseudocode**, for logic or an algorithm:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

**Call tree**, for runtime control flow:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

**Component tree**, for UI structure, with the state and module boundaries
that matter:

```text
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

**File tree**, shallow, for file responsibility or a broad refactor:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

**Sequence**, for who calls whom and in what order, one message per line:

```text
User    ──choose command──▶  UI
UI      ──expanded prompt─▶  Daemon
UI      ◀─stream result──  Daemon
```

**Flow**, for data flow or a state machine, one arrow per edge:

```text
draft ──submit──▶ review ──approve──▶ merged
                    │
                    └──request changes──▶ draft
```

**Diff**, when the point is what changes and the shape around it exists;
match the diff to the shape it changes (a tree, a file layout, a call tree,
a state):

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
```

**Whole block**, when most of it is new, when omitted context would hide
ownership or order, or when the reader needs a copyable target:

```ts
function expandSkill(command: string): string {
  return `use the ${command.slice(1)} skill`
}
```

**Table**, for options or items compared on the same attributes: one row per
item, one column per attribute, the verdict last.

| option | cost | risk | verdict |
| --- | --- | --- | --- |
| cache  | low  | stale reads | use |

## Guidance

- Place each widget next to the one or two sentences it supports.
- Keep only the calls, files, props, states and boundaries the current
  question needs.
- Use one widget, sometimes several, never all of them.
