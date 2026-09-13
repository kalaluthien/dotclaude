---
name: show-me
description: Explains a structure, concept, repository, PR, scenario or a difference the facts settle as a diagram, a narrative or a comparison. Use when the user asks to have a model, lifecycle, flow, repository, PR or measured result explained, shown or set side by side - 설명해줘, 보여줘, 그림으로, 구조화해서, 시각화, 비교해줘 - or types /show-me. Not for rewording the last reply, a status list, or a decision the user still has to make (grill-me).
---

# show-me

Show the topic instead of describing it: the one named, else whatever the
conversation is about. Its sentences beside code, a figure or a spec follow
[prose](references/prose.md) in either medium. A new rule on drawing is filed
in `~/.claude/types/doctype.md`, one on writing in `references/`.

## The steps

1. **Doctype**: the question the ask puts picks a `diagram`, a `narrative`
   or a `comparison`, [doctype](../../types/doctype.md) § Doctypes; build its
   parts in that order.
2. **Medium**: doctype.md § Media picks it. Markdown takes the chat forms
   below; an artifact starts from `assets/<doctype>.html`.
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
