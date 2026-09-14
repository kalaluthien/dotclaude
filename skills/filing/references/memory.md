# Memory

A pool is `projects/<slug>/memory/*.md` under `~/.claude`; the global pool,
`projects/-Users-hyungmokim--claude/memory/`, holds what is machine-wide and a
project's pool holds what is that project's. `MEMORY.md` in the pool is the
only index the harness loads by itself, so a file without its one line there
is never read. Git does not track a pool: nothing restores a bad write, and two
sessions editing one file is last-write-wins, so patch by exact-string
replacement over a fresh read.

## Name

Name it `<prefix>-<subject>`, the prefix one of
[`~/.claude/shared/memtype.md`](../../../shared/memtype.md)'s, with no date and no
project name. A file holds one *subject*, as `##` sections of one file, and
never repeats a fact another pool holds; link with `[[name]]` instead.

## Shape

`name` and `description` are the whole frontmatter. A `description` states the
file's role, never its contents. The harness's own memory instructions ask for
`metadata.type`; ignore that line, the hook below refuses it.

```markdown
---
name: topic-alloy
description: Running the Alloy Analyzer headless; read before invoking the jar.
---
```

The index line: `- [Title](file.md) — hook`, where the hook says when to read
it.

Once a rule is promoted into a tree the session loads, the memory keeps only
what the tree does not state -- the owner's words with their date, the concrete
case, a number's derivation -- and carries no pointer back to the tree, because
a pointer is a second reader that drifts and the tree is loaded anyway.

## What is refused

`~/.claude/hooks/check-memtype.py` runs on every `Write` or `Edit` into a pool
and refuses, with the reason on stderr, a name opening with none of the four
prefixes, a file with no line in its pool's `MEMORY.md`, and a `metadata.type`.
A Bash write
bypasses the hook; check it afterwards with
`check-memtype.py <absolute path>`.
