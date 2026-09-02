---
paths:
  - "**/skills/*/SKILL.md"
  - "**/skills/*/references/*.md"
---

# Skill authoring

A skill is procedural knowledge loaded on demand: the conventions and the
hard-won steps that spare a reader the trial and error, not a workflow to march
through. The reader knows the tools, the language, and the domain. Write only
what it cannot derive.

## Frontmatter

- `name` — lowercase, hyphens only, identical to the directory name. A skill
  the model loads takes the gerund form, verb plus object
  (`updating-wiki-pages`). A user-typed skill takes the voice of its pool: a
  bare verb phrase under a project, the utterance that provokes it under
  `~/.claude/skills` (`so-what`, `you-sure`). `writing` is fixed by
  owner order and stays as it is, though it is model-loaded and no gerund.
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

Optional. Omit each one unless the skill needs it.

- `context: fork` runs the skill in an isolated subagent with no conversation
  history. `agent` picks the subagent type: `general-purpose` when omitted,
  `Explore`, `Plan`, or a name from `.claude/agents/`.
- `background: false` makes the invoking turn wait for the fork's result.
- `allowed-tools` lists tools usable without a permission prompt during the
  invoking turn only. The grant clears on the next message, and it never
  restricts baseline permissions.
- `disable-model-invocation: true` keeps the description out of context; only
  the user can invoke the skill.

## Body sections

Zero to three sections, whichever the skill's own subject needs, titled with
noun phrases. Order them so the reader meets each one when it applies.

Shape each section to its material:

| the material | the shape |
| --- | --- |
| a subject that reduces to a small rule | the rule, from first principles |
| a subject thick with exceptions | a few worked examples that carry the shape |
| a term the skill encapsulates | its definition |
| distinct situations | a catalogue: the situation in one column, the action it selects in the next |

A catalogue row that selects a whole mode links a file in `references/` holding
that mode; the row keeps the selector, the reference keeps the body.

Put the reason in the clause after the rule it defends. State a finished state
as a predicate the agent can check ("every index entry resolves to a file"),
never an adjective ("the index is correct"). Name the failure modes that raise
no error. Match specificity to the cost of a wrong step: a narrow path with real
hazards gets exact instructions, open work gets direction and the criteria that
judge it.

## Content and register

- Include only what the agent cannot derive: house conventions, defaults that
  surprise, values that must match another file, failures with no error message.
- Cut a rule before you shorten it. Compliance falls with the number of rules
  held at once, and two rules that can contradict each other cost more than two
  that cannot.
- Give the reason only where the rule looks arbitrary without it. A rule the
  agent can already justify is stated bare.
- Write plain imperative sentences. Do not escalate to capitals or to `MUST`;
  emphasis buys over-triggering, not compliance.
- Keep a prohibition as a prohibition. Restate it positively only when the
  positive form specifies more.
- One term per concept. No dates, versions, or "currently". No constant without
  the reason for its value.
- An example that repeats the instruction anchors the agent to the sample
  instead of the rule.

## Directory layout

| directory | what happens to the file | what reaches context |
| --- | --- | --- |
| `scripts/` | executed | its output only |
| `references/` | read on demand | the file, when read |
| `assets/` | copied into the deliverable | nothing |

Code to run goes to `scripts/` and is called from the body. A template copied
verbatim goes to `assets/`; a template read and adapted goes to `references/`.

References are one level deep. Name one for the situation that selects it and
link it from the row that selects it — a reference no row names is never read. A
reference over 100 lines opens with its own table of contents, because an
unsummarized file gets previewed instead of read.

## Gotchas

- The body loads once and stays for the session. Write standing instructions,
  not one-time steps.
- Compaction keeps only the opening of a re-attached body, so a rule that must
  survive a long session belongs near the top.
- An unused skill still costs its description on every turn. A fact belongs in
  `CLAUDE.md`; only a procedure earns a skill.
- A script must handle its own errors and must not assume a tool is installed.
