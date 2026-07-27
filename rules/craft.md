# Craft lessons
Situational rules with an instruction and its rationale. Read this file before
you design a system, debug a failure, verify a fix, or rewrite git history.
Turn-level habits stay in `~/.claude/CLAUDE.md`; append here per
`~/.claude/rules/learning-routes.md`.

## Design
- Judge a module by the ratio of interface to implementation, not by line count:
  a deep module hides substantial behavior behind a small surface, and a split
  that multiplies files without shrinking what callers must know adds net
  complexity. (Ousterhout, *A Philosophy of Software Design*) (2026-07-22)
- Classify logic as data, calculation (pure function), or action (side-effect),
  and push business logic toward calculations the effectful shell calls — pure
  functions are the cheapest thing to test and compose. (Normand, *Grokking
  Simplicity*; "functional core, imperative shell") (2026-07-22)
- Write spec and design documents as predicates on system properties, generating
  rules on system structure, or decision records with reasons — never as mirrors
  of what the artifact already says. A mirror is redundant on the day it is
  written and a lie after the artifact's next change. (2026-07-22)
- When you simplify or trim a design, check every cut against the user's stated
  top-tier requirements, and make the deliverable show the mapping (requirement
  as a predicate -> where the design satisfies it). A cut that serves a
  requirement but does not show it reads as the requirement being dropped.
  (2026-07-23)

## Debugging
- Debug a driven action that does nothing (no effect, no error) by going deeper,
  not wider: read the tool or framework's own diagnostics first (idle, timeout,
  and harness warnings usually name the cause), then log each decision point to
  bisect where the pipeline breaks. Re-trying different ways to trigger it is
  symptom-thrashing that can burn hours. (2026-07-19)
- To find who owns an effect, ablate the suspect instead of reasoning about it:
  disable the code believed to cause the symptom and re-run. If the symptom
  survives, the owner is elsewhere — usually a framework acting on its own
  signal rather than your call site. One cheap run replaces a long chain of
  inference. (2026-07-19)

## Verification
- A regression test earns trust only by failing first. Before you believe a new
  test covers the bug, revert the fix (`git stash`), watch the test fail, then
  restore. A test authored against an already-fixed tree can pass for reasons
  unrelated to the defect. (2026-07-19)
- When an automated check fails but the manual flow or a sibling test passes,
  suspect the harness before the product; isolate the delta, changing one
  variable at a time. In a suite already known to flake, the discriminator is
  whether the *same* assertion fails: a failure that moves between assertions
  across runs, and reproduces on the unchanged baseline, is environmental.
  (2026-07-19)
- A design verdict argued only against documents is unverified. Before you ship
  it, run one read-only pass against the actual code: is the claimed state
  observable, does the surface have the claimed capacity, does a latent defect
  contradict a premise. (2026-07-23)
- Do not read a changed failure mode — a new error, a later failing line — as
  progress; verify the new state against ground truth (logs, the actual effect)
  before you believe the earlier cause is gone. (2026-07-19)
- Treat documentation claims about a tool's or harness's behavior as hypotheses;
  when a decision hinges on one, verify with a cheap live probe. Docs lag, and a
  probe costs one run. (2026-07-16)

## Git
- Operate on a worktree from the main checkout with `git -C <path>`. Do not `cd`
  into a worktree inside a command chain that later merges or removes it — the
  merge then runs inside the worktree ("already up to date") and the removal
  deletes the shell's own cwd. (2026-07-26)
- A release tag names the commit that produced the artifact, not `HEAD`. Before
  you add "one more fix" to a release whose commit already exists, check which
  tree the tag will point at; when the fix must ship and nothing is pushed yet,
  rewrite the unpushed history so the fix precedes the release commit, then
  rebuild the artifact from that tree. (2026-07-26)
