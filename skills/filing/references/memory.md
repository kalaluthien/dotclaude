# Memory

A pool is `projects/<slug>/memory/*.md` under `~/.claude`; the global pool,
`projects/-Users-hyungmokim--claude/memory/`, holds what is machine-wide and a
project's pool holds what is that project's. `MEMORY.md` in the pool is the
only index the harness loads by itself, so a file without its one line there
is never read. Git does not track a pool: nothing restores a bad write, and two
sessions editing one file is last-write-wins, so patch by exact-string
replacement over a fresh read.

## Name

A memory is named after its reader, because the type it used to be named after
predicted nothing about whether a file was ever read and the prefix did. The
four memory prefixes are:

- `topic-<subject>` — a fact looked up. States the current truth of one subject, updated in place.
- `pitfall-<subject>` — a trap read when stuck. Deleted when the tool or the fact is gone.
- `feedback-<subject>` — a rule the owner gave. Losing one repeats the failure or re-asks them.
- `archive-<subject>` — what a deleted thing knew, read when one is rebuilt. Names the commit that deleted it, its upstream if it had one, and the essence worth reusing.

Name it `<prefix>-<subject>`, with no date and no project name. A file holds one
*subject*, as `##` sections of one file, and never repeats a fact another pool
holds; link with `[[name]]` instead.

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

## What is refused

`~/.claude/hooks/check-memtype.py` runs on every `Write` or `Edit` into a pool
and refuses, with the reason on stderr, a name opening with none of the four
prefixes, a file with no line in its pool's `MEMORY.md`, and a `metadata.type`.
It reads the prefixes from the bullet list above at run time, so that list is
the declaration and this file is the only place it may appear. A Bash write
bypasses the hook; check it afterwards with
`check-memtype.py <absolute path>`.
