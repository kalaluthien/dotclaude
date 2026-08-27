---
paths:
  - "**/skills/*/SKILL.md"
  - "**/skills/*/references/*.md"
---

# Skill authoring

A skill is a procedure loaded on demand, not a document about a procedure. The
reader knows the tools, the language, and the domain. Write only what it cannot
derive.

## Frontmatter

Two keys carry the whole routing decision. Add a third key only when the harness
needs it.

- `name` — lowercase, hyphens only, identical to the directory name. A skill
  the model loads takes the gerund form, verb plus object
  (`updating-wiki-pages`). A user-typed skill takes the voice of its pool: a
  verb phrase under a project (`clean`, `verify`), the utterance that provokes
  it under `~/.claude/skills` (`so-what`, `you-sure`).
- `description` — one sentence of what the skill does, then a `Use when …`
  clause naming the situations and the words a user would actually type. Third
  person, no angle brackets. The harness truncates it at 1,536 characters,
  shared with `when_to_use`.
- Put the routing words in the first line of the description. The listing
  truncates long entries and drops the least-used ones first, so a trigger
  buried at the end can disappear before the skill is ever considered.
- Add a `Not for …` clause when a sibling skill can claim the same request.
  Negative scope stops over-triggering; more positive description does not.

## Execution keys

Optional keys that change how the body runs. Omit each one unless the skill
needs it.

- `context: fork` runs the skill in an isolated subagent with no conversation
  history. `agent` picks the subagent type: `general-purpose` when omitted,
  `Explore`, `Plan`, or a name from `.claude/agents/`. The body must state the
  whole task, because a fork cannot ask the user or read the conversation.
- Pin `model` on every fork skill. An unpinned fork inherits the invoking
  session's model, which is whatever the owner selected and says nothing about
  the fork's work. Deciding work pins `opus`, retrieval pins `sonnet`.
- `background: false` makes the invoking turn wait for the fork's result.
- `effort` overrides reasoning effort while the skill is active, `low` through
  `max`.
- On a plain skill too, `model` and `effort` beat the flags the session was
  launched with, in both directions. So a command skill declares the tier its
  own procedure is worth and gets it however it was started — typed, or spawned
  by a service that knows only its own default (probed 2026-08-21,
  claude-code 2.1.238).
- `allowed-tools` lists tools usable without a permission prompt during the
  invoking turn only. The grant clears on the next message, and it never
  restricts baseline permissions.
- `disable-model-invocation: true` keeps the description out of context; only
  the user can invoke the skill.

## Body slots and their order

Four slots, always in this order. Skip a slot with no content, never reorder
them.

| slot | holds | position |
| --- | --- | --- |
| purpose | what the skill is for, and the finished state as a predicate the agent can check | first |
| procedure | the catalogue, or the sequence when order is load-bearing | after purpose |
| examples | one worked shape per example | after procedure |
| gotchas | failure modes that raise no error | last |

Rationale is not a slot. It rides in the clause after the rule it defends.

State the finished state as a checkable predicate ("every index entry resolves
to a file"), not as an adjective ("the index is correct"). A run that deviates
from the procedure still knows what it was for.

## Body shape

Default to a catalogue: situations in one column, the action each selects in the
next. Write a numbered sequence only where the steps cannot be permuted without
breaking the result.

Match specificity to the cost of a wrong step. A narrow path with real hazards
gets exact instructions. Open work gets direction and the criteria that judge
it.

## Content and register

- Include only what the agent cannot derive: house conventions, defaults that
  surprise, values that must match another file, failures with no error message.
- Cut a rule before you shorten it. Compliance falls with the number of rules
  held at once, and two rules that can contradict each other cost more than two
  that cannot.
- Give the reason only where the rule looks arbitrary without it: a convention, a
  house choice, a workaround for something the agent cannot observe. A rule the
  agent can already justify is stated bare.
- Write plain imperative sentences. Do not escalate to capitals or to `MUST`;
  emphasis buys over-triggering, not compliance.
- Keep a prohibition as a prohibition. Restate it positively only when the
  positive form specifies more.
- One term per concept. No dates, versions, or "currently". No constant without
  the reason for its value.
- Add an example only for a shape that prose specifies poorly, such as a format,
  a naming pattern, or a call signature. One is usually enough. An example that
  repeats the instruction anchors the agent to the sample instead of the rule.

## Directory layout

| directory | what happens to the file | what reaches context |
| --- | --- | --- |
| `scripts/` | executed | its output only |
| `references/` | read on demand | the file, when read |
| `assets/` | copied into the deliverable | nothing |

Keep everything in `SKILL.md` until one of three triggers fires.

1. The content is code to run. Move it to `scripts/` and call it from the body.
2. Two bodies of content are mutually exclusive, so no single run reads both.
   Give each its own file in `references/`. This covers per-mode instructions,
   per-format procedures, and long templates.
3. `SKILL.md` approaches 500 lines. The file has already grown wrong: cut rules
   first, and split only what survives the cut.

References are one level deep. A reference over 100 lines opens with its own
table of contents, because a nested or unsummarized file gets previewed instead
of read.

Name a reference for the situation that selects it, and link it from the
catalogue row that selects it. A reference no row names is never read.

Keep the selector in `SKILL.md` and the branch body in the reference. A template
copied verbatim belongs in `assets/`; a template read and adapted belongs in
`references/`.

## Gotchas

- The body loads once and stays for the session. Write standing instructions,
  not one-time steps.
- Compaction keeps only the opening of a re-attached body, so a rule that must
  survive a long session belongs near the top.
- An unused skill still costs its description on every turn. A fact belongs in
  `CLAUDE.md`; only a procedure earns a skill.
- A script must handle its own errors and must not assume a tool is installed.
