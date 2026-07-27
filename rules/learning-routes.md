# Learning routes
Where a durable takeaway is filed. Route each one by *what would make it wrong*.

1. A general rule, true on any repository, machine, or tool, goes to
   `~/.claude/CLAUDE.md` when it is a turn-level habit, or to
   `~/.claude/rules/craft.md` when it applies to design, debugging,
   verification, or git.
2. A writing or language rule goes to the "Simplified Technical" output style,
   `~/.claude/output-styles/simplified-technical.md`.
3. A machine or environment fact (installed tools, aliases, shell parsing,
   toolchain paths) goes to a `setup-*` topic memory in the global pool, per
   `~/.claude/rules/memory-types.md`.
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
