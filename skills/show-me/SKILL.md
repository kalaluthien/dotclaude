---
name: show-me
description: Explains a structure, concept, repository, PR or scenario as a diagram or a narrative. Use when the user asks to have a model, lifecycle, flow, repository or PR explained or shown - 설명해줘, 보여줘, 그림으로, 구조화해서, 시각화 - or types /show-me. Not for rewording the last reply, a status list, or weighing options (grill-me).
---

# show-me

Show the topic instead of describing it. If no topic is named, show whatever
the conversation is currently about. Before drafting prose beside a figure,
read `references/prose.md`; a new rule on writing or drawing is filed in
`references/`.

## The steps

1. **Doctype**: a `diagram` for one structure or concept, a `narrative` for a
   repository, a PR or a scenario, as [doctype](references/doctype.md)
   § Doctypes defines them; build its parts in that order.
2. **Medium**: `markdown`, in the chat forms below, unless the figure needs a
   page -- a layout, a state comparison, a map too dense for text. An
   artifact starts from `assets/diagram.html` or `assets/narrative.html` and
   is held to doctype.md § Media.
3. **Ending**: [delivery](references/delivery.md).

## The chat forms

Pick the smallest form that makes the point, place it next to the short text
it supports, and keep only the calls, files, props, states and boundaries the
current question needs. Use one form, sometimes several, never all of them.
No Mermaid in chat: it renders there as source.

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

Topic: $ARGUMENTS
