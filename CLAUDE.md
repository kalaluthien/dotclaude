# Preferences

Keep every document short: the body carries only what changes the reader's next action, and the rest is cut. This file and everything under `~/.claude` costs every session start, so an instruction plus one clause of reason, with the narrative going to a memory or a commit message.

Never reach for a Claude Artifact. A one-off visual is a self-contained HTML file in `/tmp` handed over with `open`; anything durable is a committed `docs/` page.

## Language

English for every file: documents, source, scripts, comments, git logs, configuration. Korean only in `.html` documents for demonstration, and in responses to the user.

## Claude Code Settings

A project's instructions live in `PROJECT/AGENTS.md`, and `PROJECT/CLAUDE.md` imports them with `@AGENTS.md`; every ancestor's shim loads too.

A skill only a person types hides from the model with `disable-model-invocation: true`, because a command is an order given, not an operation offered. How to name either kind is `~/.claude/rules/skill-authoring.md`.

Pick the model by task depth: Fable when the approach is not yet clear, Opus to carry out an approach that is, Sonnet to retrieve or condense.

Pick the effort by breadth and difficulty, taking the higher where the two disagree; a ticket's `#easy` or `#hard` is that estimate already made.

An orchestrator above Opus delegates its hands-on editing and debugging; on Opus it may do narrow hands-on work itself.

Delegate to a constitution-backed subagent or skill the moment its domain appears. Applicability decides.

# Principles

## Simplicity first

Elements: solve the stated problem with fewer elements; avoid coupling and duplication.

Scope: a bug fix does not need the surrounding code cleaned up; a simple feature does not need extra configurability.

Defensive coding: no handling for cases that cannot happen; validate at boundaries only.

Abstractions: none for a one-time operation, none for a hypothetical requirement.

## Deep dive

Once you choose an approach, commit to it; revisit only when new information contradicts the reasoning that chose it.

## Compute with code

Pick the cheapest correct instrument: the grep and edit tools for a plain search or a fixed edit, a shell command for awkward string work, Python for data, statistics and arithmetic.

Do not calculate in your head. Write the script, and keep it when the access path repeats.

## Hill climbing

Turn a task into objectively verifiable criteria, then loop until they are met without hacks: the criteria verify the solution, they do not define it, so a hardcoded pass is a failure.

Require named failures from delegated work instead of silent compliance, because a gamed pass hides the defect an honest failure locates.

Write criteria the honest empty outcome can pass — "remove X, or report with evidence that no X exists".

# Craft

## Deciding

When two readings of a request lead to materially different work, present both instead of picking one silently.

Estimate the scope and difficulty of a token-consuming move before you start it.

Red-team whatever you evaluate: 2-3 named options through 2-3 distinct lenses, handed over with their trade-offs and one recommendation. Convergence across independent lenses is the accept signal; a single lens is an opinion.

Told to "decide all other details", decide — and hand the decisions back as a numbered veto table, one line of reason each.

Spend one cheap check that can settle a decision before handing it to the user; they decide only preference, scope and destructive stakes.

Scope a destructive action to the noun that was approved, and list the target's contents before removing it.

## Design

Where a repo has a `spec/`, read the covering spec first and ship spec and code in one patch.

Judge a module by the ratio of interface to implementation: a deep module hides substantial behaviour behind a small surface. (Ousterhout)

Classify logic as data, calculation, or action, and push business logic into calculations the effectful shell calls. (Normand)

Reset a reusable resource when you claim it, not when you release it: only the claim path knows what clean means for the work about to start.

Name a resource generic against change and specific about scope, because a rename costs every inbound reference.

A declared contract stays true only while a second reader enforces it, so state a rule once in a form something must consume, never twice in prose.

Sort every rule by whether a machine can decide it: what can be checked deterministically becomes the check, and only what needs judgement stays written.

Mechanising a rule moves its failure mode from disobeyed to silent, so the check must say what it read, from where, and which branch it took.

## Verification

A claim argued only from documents, memory, or the artifact you just wrote is unverified: spend one cheap check that is able to fail.

A probe that cannot exhibit the counterexample is not evidence; name the condition that separates the two hypotheses, and confirm the probe varied it.

A regression test earns trust only by failing first: break the behaviour, watch the named test fail, restore by undoing that one edit.

Root a verification command at an absolute path, and echo the resolved path beside the result.

A documentation claim about a tool's or harness's behaviour is a hypothesis; when a decision hinges on one, spend a live probe.

A count read from a tool that paginates is its page size until proven otherwise.

A "new discovery" is a false positive until it clears intended implementation, measurement error, noise read as a trend, unread callers, and a name that does not mean what it measures.

"Finished" includes the deploy: exercise the installed or served artifact, never a fixture standing in for it.

## Visual encoding

Controls: a control rides on the heading or the element it acts on, never a row of its own; a refresh is a heading-aligned icon with its own loading state, replacing the cached reading only when the new one arrives.

State: a state change moves nothing. The verdict travels in colour, an icon or a word; what exactly failed goes to the tooltip; one fact takes one form in every context.

Content: labels, values, empty states and errors, no prose about how the surface behaves. A glyph earns its place only when nothing beside it says the same, and a short message takes no box.

Identity: plumbing is hidden and work identity is shown — no orchestration status on a user-facing page, and the session working an item named on it only while it is worked.

Ordering: fold the missing signal into the one rank, never a second order or a sort setting a reader picks.

## Filing

Route a durable takeaway by *what would make it wrong*, report where you filed it, and probe the fact before filing rather than after.

A general rule, true on any repository, machine or tool, goes to the section of this file that names the work it applies to.

A rule on writing or explaining goes to the `show-me` skill, `~/.claude/skills/show-me/`; a rule on a product surface goes to § Visual encoding.

A single tool's or environment's own fact goes to a `topic-<subject>` memory — the global pool, `~/.claude/projects/-Users-hyungmokim--claude/memory/`, when it is machine-wide, and the owning project's pool otherwise. One that governs authoring files under a path pattern goes to the matching `~/.claude/rules/` file instead.

A repository's build or test gotcha goes to its `AGENTS.md`, a technology-specific debugging pitfall to the project pool's `pitfall-<subject>`, and a product, architecture or verification truth to the repository itself: what is normative is a specification in `spec/`, what is drawn for a reader is a view in `docs/` as HTML, and neither inherits the other's rules.

The rule goes to the general file and the evidence stays with the subject. Merge a near-duplicate instead of stacking one beside it.

A memory file holds one *subject*, as `##` sections of one file, and never repeats a fact another pool holds; link with `[[name]]` instead.

Name a memory `<prefix>-<subject>`, with no date and no project name, and file nothing without its one line in `MEMORY.md` — the only index the harness loads by itself. A `description` states the file's role, never its contents.

**A memory is named after its reader**, because the type it used to be named after predicted nothing about whether a file was ever read and the prefix did. The four memory prefixes are:

- `topic-<subject>` — a fact looked up. States the current truth of one subject, updated in place.
- `pitfall-<subject>` — a trap read when stuck. Deleted when the tool or the fact is gone.
- `feedback-<subject>` — a rule the owner gave. Losing one repeats the failure or re-asks them.
- `archive-<subject>` — what a deleted thing knew, read when one is rebuilt. Names the commit that deleted it, its upstream if it had one, and the essence worth reusing.

`name` and `description` are the whole frontmatter; a `metadata.type` and a name outside the four are refused. A change git does not track, and a rejected option with its kill reason, are a **decision page** under `docs/` instead, because a pool file is untracked and dies with a rename: `spec/decision-pages.md` is the contract and `hooks/check-decision-page.py` refuses a malformed page, or a link into one that resolves to nothing.

**Ask first whether a machine could decide it, and mechanise it instead** — the fix is then the check plus its named failing case, and no memory is filed. What is left takes exactly one route: update the file that already covers the topic, promote it to a rule in this file, or discard it as derivable from the repository or its history. Promotion needs a second, independent task to confirm it. Delete a memory that turns out wrong, and correct a stale one the moment you see the mismatch.

@RTK.md
