---
name: show-me
description: Explains a structure, concept, repository, PR, scenario or set of options as a diagram, a narrative or a comparison. Use when the user asks to have a model, lifecycle, flow, repository, PR or result explained, shown or compared - 설명해줘, 보여줘, 그림으로, 구조화해서, 시각화, 비교해줘 - or types /show-me. Not for rewording the last reply, a status list, or reaching a decision by interview (grill-me).
---

# show-me

Show the topic instead of describing it: the one named, else whatever the
conversation is about. A new rule on writing or drawing is filed in
`references/`.

## The steps

1. **Doctype**: the question the ask puts picks a `diagram`, a `narrative`
   or a `comparison`, [doctype](references/doctype.md) § Doctypes; build its
   parts in that order.
2. **Medium**: `markdown`, in the chat forms below, unless the figure needs a
   page -- a layout, a table too wide for chat, a map too dense for text. An
   artifact starts from `assets/<doctype>.html`. Either medium is held to
   doctype.md § Media.
3. **Ending**: [delivery](references/delivery.md).

## The chat forms

Pick the smallest form that makes the point, place it next to the short text
it supports, and keep only the calls, files, props, states and boundaries the
current question needs. Use one form, sometimes several, never all of them.

**Pseudocode** for logic or an algorithm:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
```

**A call tree** for runtime control flow:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

**A component tree** for UI structure, carrying the state and module
boundaries that matter:

```tsx
<SessionPage> (apps/web/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

**A shallow file tree** for file responsibility or a broad refactor:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

**A table** for a comparison: a row per option, a column per criterion,
bold on the cells that differ, and a line under it saying so.

**A diff** when the point is what changes and the surrounding shape already
exists. The diff takes the shape of whichever form above fits the topic:

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the slash command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

**The whole block** when most of it is new, when omitted context would hide
ownership or order, or when the user needs a copyable target shape.
