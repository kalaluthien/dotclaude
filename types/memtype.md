# Memory types

A memory is named after its reader, because the type it used to be named after
predicted nothing about whether a file was ever read and the prefix did.
`~/.claude/hooks/check-memtype.py` reads the list below at run time, so this is
its one home. The four memory prefixes are:

- `topic-<subject>` — a fact looked up. States the current truth of one subject, updated in place.
- `pitfall-<subject>` — a trap read when stuck. Deleted when the tool or the fact is gone.
- `feedback-<subject>` — a rule the owner gave. Losing one repeats the failure or re-asks them.
- `archive-<subject>` — what a deleted thing knew, read when one is rebuilt. Names the commit that deleted it, its upstream if it had one, and the essence worth reusing.
