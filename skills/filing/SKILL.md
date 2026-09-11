---
name: filing
description: Files a durable takeaway where it belongs and shapes what it lands in - a memory, a rule in CLAUDE.md or AGENTS.md, a skill, a script or hook, an agent, a spec, a doc, a decision page. Use when the stop check asks for a takeaway, when something learned must outlive the session, or when writing or editing a SKILL.md, a file under scripts/ or hooks/, a PreToolUse or PostToolUse hook, or a file under agents/. Not for settings.json permissions or env (update-config), and not for explaining a topic (show-me).
---

# Filing

Route a durable takeaway by *what would make it wrong*, report where you filed
it, and probe the fact before filing rather than after.

**Ask first whether a machine could decide it, and mechanise it instead**: the
fix is then the check plus its named failing case, and nothing is filed. What
is left takes exactly one route below: update the file that already covers the
topic, promote it, or discard it as derivable from the repository or its
history. Promotion needs a second, independent task to confirm it. Delete a
memory that turns out wrong, and correct a stale one the moment you see the
mismatch.

| what would make it wrong | where it goes | how to shape it |
| --- | --- | --- |
| a tool, machine or environment changes | `topic-<subject>` or `pitfall-<subject>` memory, in the pool that owns the subject | [memory](references/memory.md) |
| the owner changes their mind | `feedback-<subject>` memory | [memory](references/memory.md) |
| a deleted thing is rebuilt | `archive-<subject>` memory | [memory](references/memory.md) |
| the practice changes, on any repository | `~/.claude/CLAUDE.md`, the section naming the work | one instruction plus one clause of reason |
| a repository's build or test changes | its `AGENTS.md` | same |
| a procedure changes | a skill | [skills](references/skills.md) |
| a machine can decide it | a script or hook, with its failing case | [scripts](references/scripts.md) |
| a delegate's role changes | `agents/<name>.md` | frontmatter as a skill's, [skills](references/skills.md) |
| a product's norm changes | `spec/` markdown | the repository's own spec rules |
| a reader needs a picture of it | `docs/` HTML | same, and neither inherits the other's rules |
| git does not track the change, or an option lost | a decision page under `docs/` | `~/.claude/spec/decision-pages.md` |
| how to write or explain changes | the `show-me` skill | its own body |

The rule goes to the general file and the evidence stays with the subject:
instruction and rationale only, no repository names and no war stories. Merge a
near-duplicate instead of stacking one beside it.
