---
paths:
  - "**/scripts/*.py"
  - "**/scripts/*.sh"
  - "**/hooks/*.py"
  - "**/hooks/*.sh"
---

# Script authoring

A script is a mechanism a caller trusts without reading. Everything below exists
because a mechanised rule fails silently where a written one fails loudly.

## Name and extension

Carry the language in the extension — `.py`, `.sh`. The interpreter is a fact
about the file, and hiding it costs every reader a `head -1`; a glob that must
select by language cannot select at all.

Name by who calls it. A script a flow asks a question is `<subject>-<question>`;
a script git or the harness runs unasked is `<verb>-<object>`. The two forms
separate on the call, not on the topic, and a listing that groups them is
readable for that reason.

A name is the only part a reader always sees, so name it generic against change:
no state, verdict, or measurement in the name, since updating the thing in place
makes any of those false.

## The contract a caller reads

- **State the purpose on the line under the shebang.** A derived inventory can
  then announce the script with no second edit, and a hand-kept list of scripts
  drifts the way every second copy drifts.
- **Carry usage in the file.** A reader should not need a project's instructions
  to call one.

## Exit status

Any script may end up on a hook, so use the hook meanings from the start:
**0 succeeded, 2 refuses, any other non-zero is the script's own failure and
refuses nothing.** Under `~/.claude/rules/`, `2` is the only code that blocks.

Which of the two a script uses depends on what it is:

- **A script that answers a question** prints the answer as a word on stdout and
  exits 0. The caller reads the word, never the status. Non-zero means *I could
  not look* — `2` when that must stop the caller, another code when it must not.
- **A script that guards** exits 0 to allow and 2 to refuse, with the reason on
  stderr, where the model reads it. Its own crash is a different code, because a
  guard that cannot run has not permitted anything.

Two facts the hook spec adds, and both bite:

- **Exit 2 blocks only on events that can block.** On `PostToolUse`,
  `PermissionRequest`, `SessionStart`, `Notification` and their kind it prints
  and execution continues. A guard installed on a non-blocking event enforces
  nothing, whatever it exits.
- **On `SessionStart`, `UserPromptSubmit` and their kind, stdout is injected
  into the model's context, and only on exit 0.** A script that announces
  something must always exit 0, or the announcement silently disappears.

A hook that needs more than allow-or-refuse exits 0 and prints JSON under
`hookSpecificOutput`, which then decides. Exit 2 overrides that JSON, so do not
write both.

## Absence

The inputs a script reads about a running system go stale on their own — a pid
or session id changes under a restart, a name changes under a rename, a file it
expects was never written. Each arrives as an absence, and an absence is
indistinguishable from a pass unless the code separates them.

- **Distinguish "I looked and found nothing" from "I could not look."** The
  second denies the verdict; it never quietly grants it. A directory that does
  not exist cannot be enumerated, and that is a refusal, not an empty result.
- **Print what was read, from where, and which branch was taken** — enough that
  a person meeting a refusal knows which cause it was without re-running
  anything. A bare exit code, or a verdict word with no evidence, is the shape
  that gets trusted for months while enforcing nothing.
- **Name only the conditions the code actually read.** A message listing a
  signal no branch inspects sends the next reader to rule out an absence nobody
  observed.
- **Give a polling loop a terminal branch.** For a finished subject, absence is
  the steady state, so mapping unknown to keep-waiting waits forever.

## Where it lives

Default to `skills/<skill>/scripts/`. A script is reached through the procedure
that needs it, and one that lives beside its skill is deleted with it.

A top-level `scripts/` is for the three cases that have no owning skill: the
script is small enough to need no procedure around it, a hook runs it, or CI
runs it. A script two skills call belongs there too — the alternative is a copy.

## Scope

One script answers one question. A sequence with judgement in it is a skill, not
a script; a sequence with no judgement is a script; a judgement with no sequence
is a sentence.

Do not write a second reader of a rule another script owns. Two of them drift,
and the copy that drifts is the one nobody re-runs.

Prefer parsing formal syntax over prose. A claim extracted from a declaration
cannot be forged by editing a comment, and something deleted disappears from the
extraction on its own.

## Failure

Handle your own errors and assume no tool is installed. A script that dies on a
missing binary reports a stack trace where it owed the caller a reading.

Reset a reusable resource when you claim it, not when you release it: only the
claim path knows what clean means for the work about to start.

## Verifying one

A guard you did not watch refuse is not verified. Break the thing it guards,
watch the named check fail, then restore by undoing that one edit — and put the
assertion on what the break changes, never on a neighbour it leaves alone.

Break each branch separately. A case several branches satisfy pins none of them
and passes while any one is deleted.
