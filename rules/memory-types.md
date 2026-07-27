# Memory types
How auto-memory files are named, categorized, and maintained. Applies to every
project memory directory under `~/.claude/projects/<project>/memory/`.

## Taxonomy
Three categories. The subcategory is ad-hoc, named at the front of the slug
(`<subcategory>-<topic>`); invent new subcategories when none fits, and record
them here in the same change.

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
   `setup-<topic>` files, so every project finds them in one place. Before
   JVM/Android, Python, shell-automation, remote-access, or herdr-install work,
   check that pool's `MEMORY.md` and read the matching topic file.
3. Never duplicate one fact across pools; link with `[[name]]` instead.

## Maintenance
On every save, route the candidate through exactly one of:
1. **Categorize-then-merge** — an existing file covers the topic: update it.
2. **Generalize-then-learn** — the fact is a general rule in disguise: file the
   rule per `~/.claude/rules/learning-routes.md`, keep only the evidence (or
   nothing) in memory.
3. **Discard** — derivable from the repo, git history, or CLAUDE.md; or dead.

Keep `MEMORY.md` one line per file. Delete memories that turn out wrong.
