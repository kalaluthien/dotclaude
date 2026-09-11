# Scripts and hooks

A script is a mechanism a caller trusts without reading. Everything below
exists because a mechanised rule fails silently where a written one fails
loudly.

## Name and place

Carry the language in the extension, `.py` or `.sh`: the interpreter is a fact
about the file, and a glob that must select by language cannot otherwise
select at all. Name by who calls it: a script a flow asks a question is
`<subject>-<question>`, one git or the harness runs unasked is
`<verb>-<object>`. Name it generic against change, with no state, verdict or
measurement in the name.

Default to the owning skill's `scripts/`, so the script is deleted with the
procedure that reaches it. A top-level `scripts/` is for what has no owning
skill: one small enough to need no procedure, one a hook or CI runs, one two
skills call.

## The contract a caller reads

The line under the shebang states the purpose, so a derived inventory can
announce the script with no second edit. Usage goes in the file for anything
called by hand. Handle your own errors and assume no tool is installed: a
script that dies on a missing binary reports a stack trace where it owed a
reading.

One script answers one question. A sequence with judgement in it is a skill; a
sequence with no judgement is a script; a judgement with no sequence is a
sentence. Do not write a second reader of a rule another script owns. Prefer
parsing formal syntax over prose: a claim extracted from a declaration cannot
be forged by editing a comment.

## Exit status

A guard takes the convention its caller reads.

- **A harness hook**: 0 allows, 2 refuses with the reason on stderr, and no
  other code blocks. A hook needing more than allow-or-refuse exits 0 and
  prints JSON under `hookSpecificOutput`; exit 2 overrides that JSON, so never
  write both.
- **A git hook**: git blocks on any non-zero, so the script numbers its own
  findings and says which codes it uses in its docstring.
- **A script that answers a question** prints the answer as a word on stdout
  and exits 0; the caller reads the word, never the status. Non-zero means *I
  could not look*.

Keep a guard's own crash apart from its refusal where the caller can act on
the difference: a guard that could not run has permitted nothing. Its
last-resort handler permits, so a bug in the check costs one unjudged call
that names itself rather than a wall across everything it guards.

Three harness facts, each of which makes a hook enforce nothing when missed:

- Exit 2 blocks only on events that can block. On `PostToolUse`,
  `PermissionRequest`, `SessionStart`, `Notification` and their kind it prints
  and execution continues.
- On `SessionStart`, `UserPromptSubmit` and their kind stdout is injected into
  the model's context, and only on exit 0. A script that announces something
  always exits 0.
- A `PreToolUse` matcher lists tool names; a call to a tool it does not name
  is never seen.

## Absence

The inputs a script reads about a running system go stale on their own, and
each stale input arrives as an absence indistinguishable from a pass.

- Distinguish *I looked and found nothing* from *I could not look*. A
  directory that does not exist is a refusal, not an empty result.
- Print what was read, from where, and which branch was taken, and name only
  the conditions the code actually read.
- Give a polling loop a terminal branch: for a finished subject, absence is
  the steady state.
- Scope a dedupe or idempotency check to unsettled records only, so a failed
  record stays repeatable.

## Verifying one

A guard you did not watch refuse is not verified. Break the thing it guards,
watch the named check fail, restore by undoing that one edit. Break each
branch separately and assert on what the break changes, never on a neighbour
it leaves alone, and never on an exit status alone: a crash and a refusal
share one.
