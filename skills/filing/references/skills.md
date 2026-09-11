# Skills and agents

A skill is procedural knowledge loaded on demand: the conventions and the
hard-won steps that spare a reader the trial and error, not a workflow to march
through. The reader knows the tools, the language and the domain. Write only
what it cannot derive. An agent file under `agents/` takes the same
frontmatter rules; its body is the system prompt of the delegate.

## Frontmatter

- `name`: lowercase, hyphens, identical to the directory name. A model-loaded
  skill takes the gerund form, verb plus object (`updating-wiki-pages`); a
  user-typed one takes the voice of its pool.
- `description`: one sentence of what the skill does, then a `Use when …`
  clause naming the situations and the words a person would actually type,
  third person, no angle brackets. Put the routing words in the first line:
  the listing truncates long entries and drops the least-used first. Add a
  `Not for …` clause when a sibling can claim the same request; negative scope
  stops over-triggering, more positive description does not.
- `disable-model-invocation: true` hides a skill only a person types, because
  a command is an order given, not an operation offered.
- `context: fork` runs the skill in a subagent with no conversation history;
  `agent` picks its type. `allowed-tools` grants tools for the invoking turn
  only.

## Body

Zero to three sections, noun phrases, ordered so the reader meets each when it
applies, shaped to their material:

| the material | the shape |
| --- | --- |
| a subject that reduces to a small rule | the rule, from first principles |
| a subject thick with exceptions | a few worked examples that carry the shape |
| a term the skill encapsulates | its definition |
| distinct situations | a catalogue: the situation in one column, the action it selects in the next |

A catalogue row that selects a whole mode links a file in `references/`
holding that mode; the row keeps the selector, the reference keeps the body. A
reference no row names is never read, and one over 100 lines opens with a
summary.

State a finished state as a predicate the agent can check, never an
adjective. Name the failure modes that raise no error. Match specificity to
the cost of a wrong step.

## Register

Include only what the agent cannot derive: house conventions, defaults that
surprise, values that must match another file. Cut a rule before you shorten
it, since compliance falls with the number of rules held at once. Plain
imperative sentences, no capitals and no `MUST`. Keep a prohibition as a
prohibition. One term per concept, no dates or versions, no constant without
the reason for its value. An example that repeats its instruction anchors the
agent to the sample instead of the rule.

## Layout and cost

| directory | what happens to the file | what reaches context |
| --- | --- | --- |
| `scripts/` | executed | its output only |
| `references/` | read on demand | the file, when read |
| `assets/` | copied into the deliverable | nothing |

The body loads once and stays for the session, so it holds standing
instructions, not one-time steps; compaction keeps only its opening, so a rule
that must survive a long session sits near the top. An unused skill still
costs its description every session: a fact belongs in `CLAUDE.md`, and only a
procedure earns a skill.

A vendored skill is a byte-identical copy of its upstream, named on the first
line of its body; an upgrade replaces the whole file and any edit breaks that
identity.
