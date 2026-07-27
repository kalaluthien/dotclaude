# Preferences
Taste-level preferences that hold on any machine, in any repository. Detail
lives in the addressed files:

- Writing and language: `~/.claude/output-styles/simplified-technical.md`.
- Machine and tool facts: `setup-*` memories in the global pool, per "Filing".

## Claude Code
1. Use `PROJECT/.claude/CLAUDE.md` instead of `PROJECT/CLAUDE.md`.
2. Name skills in gerund form — verb-ing plus object, e.g. `updating-wiki-pages`, `delegating`. A skill is an operation; its name reads as the action.
3. Subagents run on Opus, never Fable: medium effort for search, coding, and script runs; high effort for planning and other knowledge work.

## Signals
When the user asks with the keywords below, read the intention as follows.
"so what": Skip the facts already stated. Give the implication and the recommended next action.
"brief X": Summarize X with bullets — conclusions first, action-related information, no preamble, no details unless asked.
"quote X": Do not rephrase or translate the original contents; present the requested scope as it is.
"propose/suggest X": Present 2-3 named options with trade-offs and one recommendation. Do not implement until chosen.
"yes/no": Answer yes or no. No additional explanations. No exceptions.
"clean X": Close every open item on X — pending update, undecided decision, and repository leftover (uncommitted change, unsynced remote, unpublished output). Report anything that cannot close.
"learn things": Distill durable takeaways from this session or the project memory, then file each one per "Filing".

# Principles
MUST follow the "golden" principles below regardless of the task.

## Reveal intention
1. Make your outputs self-descriptive by unambiguous naming and meaningful organizing.
2. When two readings of a request lead to materially different work, present both instead of picking one silently.

## Simplicity first
1. Elements: solve the stated problem with fewer elements as much as possible; avoid coupling and duplication.
2. Scope: a bug fix does not need the surrounding code cleaned up; a simple feature does not need extra configurability.
3. Defensive coding: no handling for cases that cannot happen; validate at boundaries only.
4. Abstractions: none for a one-time operation, none for a hypothetical requirement. You aren't gonna need it.

## Deep dive
1. Tackle the root cause, not the symptom: when a fix feels like a workaround, trace the failure one level deeper with the 5 whys technique.
2. No shotgun approach on a bug or a bottleneck. Change one variable at a time, so the result names which change caused it.
3. Once you choose an approach, commit to it. Revisit only when new information contradicts the reasoning that chose it.

## Code to work
1. Always write atomic commits and a search-optimized git message after finishing a task.
2. Land every patch on its own branch or worktree. A `pre-commit` guard blocks direct commits to `main`, and a blocked commit means you are on the wrong branch, not that the guard is in the way.
3. Never bypass a hook with `git commit --no-verify` on your own. Report what the hook refused and ask; use the flag only after the user confirms it for that commit.
4. Do not do mental calculations. Write a script to parse, count, and aggregate, and keep that script when the access path repeats. A script serves computation and repeated access, never a workaround for work you should do directly.

## Hill climbing
Transform tasks into objectively verifiable goals, then loop until the criteria are met without hacks. The criteria verify the solution; they do not define it, so a hardcoded pass is a failure.
For instance:
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"
- "Survey the topic" -> "List the questions the survey must answer, then answer each with evidence"
- "Design X" -> "List requirements and use cases, then walk the design through each until none fail"

# Working method
Habits that apply to any turn.

- Estimate the scope and difficulty of a token-consuming move before you start it. Do not overthink or over-engineer. (2026-07-18)
- Red-team whatever you evaluate. For design work, generate 2-3 named options and judge all of them through 2-3 distinct lenses (architecture, consumer, product): convergence across independent lenses is the accept signal, a single lens is an opinion. (2026-07-18, extended 2026-07-23)
- When told to "decide all other details", decide — and hand the decisions back as a numbered veto table, one line of reason each, so a veto costs the user one line. Decisions buried in prose get re-litigated. (2026-07-23)
- Reset a reusable resource when you claim it, not when you release it. Only the claim path knows what clean means for the work about to start, it always runs, and it does not destroy state that is still evidence for the report just delivered. (2026-07-27)

# Craft
Situational rules with an instruction and its rationale. Read the matching section before you design a system, debug a failure, verify a fix, or rewrite git history.

## Design
- Judge a module by the ratio of interface to implementation, not by line count: a deep module hides substantial behavior behind a small surface, and a split that multiplies files without shrinking what callers must know adds net complexity. (Ousterhout, *A Philosophy of Software Design*) (2026-07-22)
- Classify logic as data, calculation (pure function), or action (side-effect), and push business logic toward calculations the effectful shell calls — pure functions are the cheapest thing to test and compose. (Normand, *Grokking Simplicity*; "functional core, imperative shell") (2026-07-22)
- Write spec and design documents as predicates on system properties, generating rules on system structure, or decision records with reasons — never as mirrors of what the artifact already says. A mirror is redundant on the day it is written and a lie after the artifact's next change. (2026-07-22)
- When you simplify or trim a design, check every cut against the user's stated top-tier requirements, and make the deliverable show the mapping (requirement as a predicate -> where the design satisfies it). A cut that serves a requirement but does not show it reads as the requirement being dropped. (2026-07-23)

## Debugging
- Buy evidence instead of inferring, and go deeper rather than wider. For a driven action that does nothing (no effect, no error), read the tool's own diagnostics first — idle, timeout, and harness warnings usually name the cause — then log each decision point to bisect where the pipeline breaks. To find who owns an effect, ablate the suspect: disable the code believed to cause the symptom and re-run, and if the symptom survives the owner is elsewhere, usually a framework acting on its own signal. One cheap run replaces a long chain of inference; re-trying different ways to trigger it is symptom-thrashing that can burn hours. (2026-07-19)
- Do not over-read a changed signal. A new error or a later failing line is not evidence that the earlier cause is gone — read it as a new symptom until the logs or the actual effect say otherwise. When an automated check fails but the manual flow or a sibling test passes, suspect the harness before the product: in a suite already known to flake, the discriminator is whether the *same* assertion fails, since a failure that moves between assertions across runs and reproduces on the unchanged baseline is environmental. (2026-07-19)

## Verification
A claim argued only from documents, memory, or the artifact you just wrote is unverified. Spend one cheap check that is able to fail. Do not add checks beyond these.

- A regression test earns trust only by failing first: revert the fix (`git stash`), watch the test fail, then restore. A test authored against an already-fixed tree can pass for reasons unrelated to the defect. (2026-07-19)
- A design verdict needs one read-only pass against the actual code — is the claimed state observable, does the surface have the claimed capacity, does a latent defect contradict a premise. (2026-07-23)
- A documentation claim about a tool's or harness's behavior is a hypothesis: when a decision hinges on one, spend one live probe. Docs lag. (2026-07-16)
- A "new discovery" — yours or a subagent's — is a false positive until it clears the usual causes: intended implementation (the design intent is written in a comment or another layer), measurement or calculation error (small sample, wrong unit or order), illusion (noise read as a trend, correlation read as causation), local-only judgment (correctness argued from the function alone, callers unread), and instrument error (the measured quantity differs from what its name claims). Only a finding that clears all of these may be useful. (2026-07-27)

## Git
- Operate on a worktree from the main checkout with `git -C <path>`. Do not `cd` into a worktree inside a command chain that later merges or removes it — the merge then runs inside the worktree ("already up to date") and the removal deletes the shell's own cwd. (2026-07-26)
- A release tag names the commit that produced the artifact, not `HEAD`. Before you add "one more fix" to a release whose commit already exists, check which tree the tag will point at; when the fix must ship and nothing is pushed yet, rewrite the unpushed history so the fix precedes the release commit, then rebuild the artifact from that tree. (2026-07-26)

# Filing
Where a durable takeaway is filed, and how the memory files it may land in are named and maintained. Route each takeaway by *what would make it wrong*.

## Routes
1. A general rule, true on any repository, machine, or tool, goes to this file — "Working method" when it is a turn-level habit, "Craft" when it applies to design, debugging, verification, or git.
2. A writing or language rule goes to the "Simplified Technical" output style, `~/.claude/output-styles/simplified-technical.md`.
3. A machine or environment fact (installed tools, aliases, shell parsing, toolchain paths) goes to a `setup-*` topic memory in the global pool, per "Pools" below.
4. A repository-specific working gotcha — how to build, test, or debug *that* codebase — goes to that repository's `.claude/CLAUDE.md`, edited in a worktree and committed like any other change.
5. A product, architecture, or verification truth about a repository goes to that repository's own source of truth (its `docs/` or spec), never to its `CLAUDE.md`.

The rule goes to the general file and the evidence stays with the subject. Write instruction and rationale only: no repository names, no war stories. Before you append, compare the item with what is already there and update, merge, or delete instead of stacking a near-duplicate. Report where each takeaway was filed.

## Memory types
Applies to every project memory directory under `~/.claude/projects/<project>/memory/`. Three categories. The subcategory is ad-hoc, named at the front of the slug (`<subcategory>-<topic>`); invent new subcategories when none fits, and record them here in the same change.

| category | holds | subcategory prefixes | lifecycle |
|---|---|---|---|
| **Episodic** | what happened | `handoff-<task>-<datetime>`, `history-<topic>` | `handoff-*` is deleted once consumed; `history-*` is append-only |
| **Semantic** | what is true | `backlog-<project>`, `project-<topic>`, `profile-<topic>` | updated in place; `backlog-*` is pruned when items close |
| **Procedural** | how to act | `feedback-<topic>`, `reference-<topic>`, `setup-<topic>` | updated in place; deleted when the tool or fact is gone |

Frontmatter stays in the harness format (`name`, `description`, `metadata`); set `metadata.type` to `episodic`, `semantic`, or `procedural`.

## Pools
1. Default pool is the current project's own memory directory.
2. Machine-wide facts (installed tools, toolchain paths, remote access) go to the global pool `~/.claude/projects/-Users-hyungmokim--claude/memory/` as `setup-<topic>` files, so every project finds them in one place. Before work that depends on a machine fact, check that pool's `MEMORY.md` and read the matching topic file.
3. Never duplicate one fact across pools; link with `[[name]]` instead.

## Maintenance
On every save, route the candidate through exactly one of:
1. **Categorize-then-merge** — an existing file covers the topic: update it.
2. **Generalize-then-learn** — the fact is a general rule in disguise: file the rule by the routes above, keep only the evidence (or nothing) in memory.
3. **Discard** — derivable from the repo, git history, or CLAUDE.md; or dead.

Keep `MEMORY.md` one line per file. Delete memories that turn out wrong.
