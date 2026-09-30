---
name: show-me
description: Use when the user asks to see something rather than read about it - show, draw, map, walk through, compare or offer options, or when you are about to describe a layout, plan or design in prose; not when the answer is still the user's to make (grill-me).
---

# show-me

**A render they have not seen does not exist.** Describing a picture in prose is not showing it, and a file path is not showing it.

Show the topic, the one named or else the conversation's. Skip the preamble, and pick the smallest form that makes the point. A blank is not shown: hand it to `grill-me`.

## When it fires

When the answer is visual and you are about to type it out instead:

- a plan, a structure, a roadmap, a set of steps
- a comparison between two or more things
- a layout, a page, a design, a wireframe
- a report, a review, a dashboard, a summary of where you got to
- any moment the user has to choose between options

If they would have to read it twice, draw it once.

## SHOW

One thing, or a stack of versions: render it, then say anything about it.

## PICK

Two or more directions the user must choose between.

- Offer at least three options: two is a yes-or-no in disguise, and three is where someone sees what they want.
- Give each a short label and a one-line description of its argument, not its decoration.
- Never ask for a choice between visual options described in words, since a description is your model of the thing; render first, ask second.

The one-sentence test, before you render: describe each direction in one sentence. If one sentence fits two of them, you restyled one idea instead of designing two: go back.

## HTML versus plain text

- HTML for what they look at or share: plans, reviews, comparisons, reports, dashboards, option grids.
- Plain text for what they paste elsewhere: posts, docs, config and instruction files, since HTML breaks the paste target and costs tokens in every later session.
- Chat widgets, below, for an answer that needs no page.

State which one you are producing before you build it.

## Render step

- Load `paperwork:rendering` when the paperwork plugin is loaded, since it holds the page design.
- Read `references/html.md` for the page rules and the PICK board.
- Publish every page with the `Artifact` tool and give the link; never open a local file in a browser, since the owner's browser is theirs.

## What you say around it

The render does the explaining, so say almost nothing.

- Lead with the verdict, not the process: what they are looking at and what you think of it, failures included.
- End with one next thing, doable now, on its own line; if there is none, say the work is done and stop.

## Do not guess

If you do not know a filename, a number, a status, a path or what a link points to, check it: read the file, run the query, open the page. If you cannot check, write "not verified" and name what is missing; never fill a gap with what merely sounds right, and never report a check you did not run.

## The check before you speak

Have they seen this, with their eyes, in this session? If not, you are not finished.

The answer goes to chat by default, and into a document as well when one is asked for.

## Widgets

Every widget is plain markdown: a table or a fenced `text`, `diff` or source
block. Nothing needs HTML or a renderer, so use one when the answer needs no page.

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
| cache  | 1 file, 20 lines | stale reads | use |

## Guidance

- Place each widget next to the one or two sentences it supports.
- Keep only the calls, files, props, states and boundaries the current
  question needs.
- Use one widget, sometimes several, never all of them.
