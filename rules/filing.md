# Filing
Where a durable takeaway is filed, and how the memory files it may land in are
named and maintained. Route each takeaway by *what would make it wrong*.

## Routes
1. A general rule, true on any repository, machine, or tool, goes to
   `~/.claude/CLAUDE.md` when it is a turn-level habit, or to
   `~/.claude/rules/craft.md` when it applies to design, debugging,
   verification, or git.
2. A writing or language rule goes to the "Simplified Technical" output style,
   `~/.claude/output-styles/simplified-technical.md`.
3. A machine or environment fact (installed tools, aliases, shell parsing,
   toolchain paths) goes to a `setup-*` topic memory in the global pool, per
   "Pools" below.
4. A repository-specific working gotcha — how to build, test, or debug *that*
   codebase — goes to that repository's `.claude/CLAUDE.md`, edited in a
   worktree and committed like any other change.
5. A product, architecture, or verification truth about a repository goes to
   that repository's own source of truth (its `docs/` or spec), never to its
   `CLAUDE.md`.

The rule goes to the general file and the evidence stays with the subject.
Write instruction and rationale only: no repository names, no war stories.
Before you append, compare the item with what is already there and update,
merge, or delete instead of stacking a near-duplicate. Report where each
takeaway was filed.

## Memory types
Applies to every project memory directory under
`~/.claude/projects/<project>/memory/`. Three categories. The subcategory is
ad-hoc, named at the front of the slug (`<subcategory>-<topic>`); invent new
subcategories when none fits, and record them here in the same change.

| category | holds | subcategory prefixes | lifecycle |
|---|---|---|---|
| **Episodic** | what happened | `handoff-<task>-<datetime>`, `history-<topic>` | `handoff-*` is deleted once consumed; `history-*` is append-only |
| **Semantic** | what is true | `backlog-<project>`, `project-<topic>`, `profile-<topic>` | updated in place; `backlog-*` is pruned when items close |
| **Procedural** | how to act | `feedback-<topic>`, `reference-<topic>`, `setup-<topic>` | updated in place; deleted when the tool or fact is gone |

Frontmatter stays in the harness format (`name`, `description`, `metadata`);
set `metadata.type` to `episodic`, `semantic`, or `procedural`.

## Pools
1. Default pool is the current project's own memory directory.
2. Machine-wide facts (installed tools, toolchain paths, remote access) go to
   the global pool `~/.claude/projects/-Users-hyungmokim--claude/memory/` as
   `setup-<topic>` files, so every project finds them in one place. Before work
   that depends on a machine fact, check that pool's `MEMORY.md` and read the
   matching topic file.
3. Never duplicate one fact across pools; link with `[[name]]` instead.

## Maintenance
On every save, route the candidate through exactly one of:
1. **Categorize-then-merge** — an existing file covers the topic: update it.
2. **Generalize-then-learn** — the fact is a general rule in disguise: file the
   rule by the routes above, keep only the evidence (or nothing) in memory.
3. **Discard** — derivable from the repo, git history, or CLAUDE.md; or dead.

Keep `MEMORY.md` one line per file. Delete memories that turn out wrong.
