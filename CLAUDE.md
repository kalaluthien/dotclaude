# Preferences
Taste-level preferences that hold on any machine, in any repository. Detail
lives in the addressed files:

- Writing and language: `~/workspace/.claude/output-styles/simplified-technical.md`.
  **Ground rule for every document: keep it short, and separate the
  crucial from the detail — obsessively. The body carries only what
  changes the reader's next action; details collapse or get cut.**
- Machine and tool facts: `setup-*` memories in the global pool, per "Filing".

## Claude Code
1. Use `PROJECT/.claude/CLAUDE.md` instead of `PROJECT/CLAUDE.md`.
2. Name skills in gerund form — verb-ing plus object, e.g. `updating-wiki-pages`, `delegating`. A skill is an operation; its name reads as the action.
3. Pick the model by task depth and the effort by task breadth. Fable runs only the top-level orchestrating session, never a subagent or a delegated session. Below it, work that decides — ideation, planning, implementation, review — runs Opus; work that retrieves or condenses knowledge — search, classification, summarization — runs Sonnet. Effort measures scope, not difficulty: high or xhigh for a task that spans many exceptional cases or a large state space, low or medium for a narrow one.
4. Delegate to a constitution-backed subagent the moment its domain appears — `document-writer` when a document view is ordered, `debugger` when anything needs debugging. Applicability decides; do not judge not to use it.

## Signals
When the user asks with the keywords below, read the intention as follows.
"so what": Skip the facts already stated. Give the implication and the recommended next action.
"brief X": Summarize X with bullets — conclusions first, action-related information, no preamble, no details unless asked. Then route the deliverable by lifetime: chat text for an answer that dies with the session, a disposable HTML under the session scratchpad for a one-off visual review, or a committed `docs/` spec (`.md`) or view (`.html`) for durable knowledge.
"quote X": Do not rephrase or translate the original contents; present the requested scope as it is.
"propose/suggest X": Present 2-3 named options with trade-offs and one recommendation. Do not implement until chosen.
"yes/no": Answer yes or no. No additional explanations. No exceptions.
"clean X": Close every open item on X — pending update, undecided decision, and repository leftover (uncommitted change, unsynced remote, unpublished output) — including items other sessions or agents left behind, not only this session's own work. Report anything that cannot close.
"dig X": Answer X from recorded evidence, not from memory or guesses. Search the machine's own records — git history, system and tool logs, documents, and agent session history — and cite where each finding came from.
"learn X": Distill durable takeaways from X — this session, the project memory, or the named scope — then file each one per "Filing".

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
1. Tracing a failure to its root cause is the `debugger` subagent's job, and its method — reproduce first, one variable at a time, 5 whys — lives in its constitution (`~/.claude/agents/debugger.md`). Delegate rather than debug inline.
2. Once you choose an approach, commit to it. Revisit only when new information contradicts the reasoning that chose it.

## Code to work
1. A task is finished when it is committed, merged, and pushed. Write atomic commits with a search-optimized message, then land and push them without waiting to be asked — this overrides any harness default that says to commit or push only on request. Ask first only when the push is destructive: a force-push, a history rewrite, or a branch you do not own.
2. Land every patch on its own branch or worktree. A `pre-commit` guard blocks direct commits to `main`, and a blocked commit means you are on the wrong branch, not that the guard is in the way.
3. Never bypass a hook with `git commit --no-verify` on your own. Report what the hook refused and ask; use the flag only after the user confirms it for that commit.
4. Do not do mental calculations. Write a script to parse, count, and aggregate, and keep that script when the access path repeats. A script serves computation and repeated access, never a workaround for work you should do directly.
5. For a change the user sees through a running service, "finished" includes the deploy: rebuild or restart the service and verify the served artifact shows the change. A landed commit leaves the user watching the old build, and a dev-server check does not cover the deployed one.

## Hill climbing
Transform tasks into objectively verifiable goals, then loop until the criteria are met without hacks. The criteria verify the solution; they do not define it, so a hardcoded pass is a failure.
For instance:
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"
- "Survey the topic" -> "List the questions the survey must answer, then answer each with evidence"
- "Design X" -> "List requirements and use cases, then walk the design through each until none fail"

When the work is delegated, require named failures instead of silent
compliance: a criterion honestly failed with its reason locates a defect in
the criteria or the inputs, which a gamed pass hides — the failure report is
often the more valuable deliverable.

# Craft
Rules with an instruction and its rationale, grouped by the work they apply to. Read the matching section before you commit to a decision, design a system, verify a fix, rewrite git history, or file a takeaway. Debugging method and its filing live in the debugger constitution, `~/.claude/agents/debugger.md`; no `CLAUDE.md` and no `docs/` holds a debugging procedure.

## Deciding
- Estimate the scope and difficulty of a token-consuming move before you start it. Do not overthink or over-engineer.
- Red-team whatever you evaluate: generate 2-3 named options and judge all of them through 2-3 distinct lenses (architecture, consumer, product). Convergence across independent lenses is the accept signal; a single lens is an opinion.
- When told to "decide all other details", decide — and hand the decisions back as a numbered veto table, one line of reason each, so a veto costs the user one line. Decisions buried in prose get re-litigated.
- Before you hand a decision to the user, spend one cheap check that can settle it — read the target, probe the tool, dry-run the move — and act on what the check shows. A question a check can answer costs the user a round-trip for nothing; the user decides only what no check can settle: preference, scope, and destructive stakes.
- Scope a destructive action to the noun that was approved. List the target's contents before removing it, and when the container holds more than the named thing, remove only the named thing or ask again — approval of the part is not approval of the directory around it.

## Design
- Judge a module by the ratio of interface to implementation, not by line count: a deep module hides substantial behavior behind a small surface, and a split that multiplies files without shrinking what callers must know adds net complexity. (Ousterhout, *A Philosophy of Software Design*)
- Classify logic as data, calculation (pure function), or action (side-effect), and push business logic toward calculations the effectful shell calls — pure functions are the cheapest thing to test and compose. (Normand, *Grokking Simplicity*; "functional core, imperative shell")
- Write spec and design documents as predicates on system properties, generating rules on system structure, or decision records with reasons — never as mirrors of what the artifact already says. A mirror is redundant on the day it is written and a lie after the artifact's next change.
- When you simplify or trim a design, check every cut against the user's stated top-tier requirements, and make the deliverable show the mapping (requirement as a predicate -> where the design satisfies it). A cut that serves a requirement but does not show it reads as the requirement being dropped.
- Update a document that records history by *adding* to it, never by refreshing what it recorded. A superseded decision keeps its own text under a pointer to what replaced it, and a rejected option keeps the kill reason it was actually judged on — a reason rewritten against a rule that did not exist yet claims a judgment nobody made, and it hides that the option may now lose for a different reason or not at all. Name which half of a stale reason the reversal retires, then re-verify the half that still stands. A document's commit pin follows the same rule: it dates every implicit citation in the document, so bumping it during a targeted edit silently re-points claims onto a tree they were never read on. Keep the pin and anchor each new claim to its own commit inline; re-pin only when the whole document is re-verified.
- Reset a reusable resource when you claim it, not when you release it. Only the claim path knows what clean means for the work about to start, it always runs, and it does not destroy state that is still evidence for the report just delivered.
- Scope a dedupe or idempotency check to the window it was written for, and derive that window from the key's own vocabulary. A key that names *what was asked for* rather than *which attempt* repeats every time the subject returns to a state it has held, so matching it against the whole history answers a fresh request with a settled one — accepted, nothing spawned, no error to read. Match it against unsettled records only; a settled record answered an earlier request, and a failed one must stay repeatable.
- Derive a retention window from the longest-lived reader of the thing kept, and enumerate the readers before you accept any premise about who they are. The reader a discussion names is the interesting one, not the durable one — an undo or a revert is talked about most and usually expires within minutes, while a plain drawn card that waits on a human tap outlives it by orders of magnitude. Enumerate first, then take the maximum; a window set from the named reader deletes what someone is still looking at.
- When a list stops being its own enumeration and starts being derived from a mapping, enumerate everything the new source names, not only the member that motivated the change. A mapping was built to answer a different question, so it carries members the list cannot serve, and admitting them silently trades an entry missing from the list for one that fails at use — the worse of the two, because a gap is visible on sight and a broken entry is not. Add the predicate the list's own use requires, in the same change that widens the source.
- Let a failure message name only the conditions the code actually read. A message listing a signal no branch ever inspects reports a check that never ran, and it reads as evidence to the next debugger: it sends them to rule out an absence that was never observed, while the signal it denies may be sitting in plain view. When a settlement or timeout gate is widened, re-read its message against the branches it now has.
- Name a resource, a document, or an artifact so it is generic against change and specific about scope at once. Generic: the name carries no state, verdict, measurement, setting, or candidate label, because updating the thing in place makes any of those false. Specific: it names the slice of the system the thing owns, never the genre, which the surrounding catalogue or directory already carries — a name that could sit under three categories divides nothing. A name is read to route work, not to run it, so a name that states the role lets one documented mapping carry every setting the role implies. The two halves are traded against each other only by renaming, and a rename costs every inbound reference, so a name that meets both is left alone.
- A label earns a control in a browsing surface only when it is not derivable from something already on screen, and only when its values actually divide the set. A taxonomy that routes well at writing time — where it forces "what would make this wrong?" — can still be worthless at reading time, so check the label against the filename, the path, and the value distribution before it becomes a facet.
- A declared contract stays true only while a second reader enforces it — a validator or hook on the authoring side, beside the consumer that reads it. With the consumer as its only reader, the contract drifts exactly like the hardcoded copy it replaced, in a file that looks more authoritative.
- Renaming a value that a store already holds needs its own migration table, applied unconditionally, never rows added to the one already there. An existing table is usually gated on the *absence* of a field — it upgrades records written before that field existed — so rows added to it never fire on records the current build wrote, and the rename silently does not happen. Removing the guard is worse: the old table's keys then match the new field's values and rewrite records that were already correct. Write the second table, apply it after the first, and check the rename against the deployed store rather than a fixture.
- Choose a visual form from the data abstraction and the reader's task, never from the domain noun ("it is a knowledge base, so it gets a graph"). Each form has a measured size range: node-link legibility collapses past ~50 nodes, a calendar heatmap needs ~90 days of span to beat a bar strip, a swimlane degrades by lane count rather than bar count, and a faceted list is bounded by page size and so never expires. State the span and the item count first; the form follows.

## Verification
A claim argued only from documents, memory, or the artifact you just wrote is unverified. Spend one cheap check that is able to fail. Do not add checks beyond these.

- A regression test earns trust only by failing first: revert the fix (`git stash`), watch the test fail, then restore. A test authored against an already-fixed tree can pass for reasons unrelated to the defect.
- Before adopting a word for a renamed value, grep the tree *and* `git log -S` it. A word absent from the working tree is not free: it may have been retired deliberately, and a retirement is usually pinned by an assertion that the word is *not* present, which a plain grep for current usage never surfaces. Re-adopting one silently reverses the decision that removed it and breaks its pin. Prefer a word nothing has held; when history shows the word was retired, either take another or override the retirement out loud, citing the commit.
- A delegate killed mid-task is not proof its work is lost: diff its target artifacts before re-running it. A writer often finishes the file before the harness kills the report, and one status check costs less than a re-run.
- A design verdict needs one read-only pass against the actual code — is the claimed state observable, does the surface have the claimed capacity, does a latent defect contradict a premise.
- A documentation claim about a tool's or harness's behavior is a hypothesis: when a decision hinges on one, spend one live probe. Docs lag.
- A command written into a document is copied from a shell where it just succeeded, never retyped or adapted to fit the prose around it. Nothing executes a documented command until a reader does, so a form its author never ran is unverified text sitting in the one place that looks authoritative. A CLI that answers a malformed invocation with a usage message and a non-zero exit reads as a no-op to whoever follows it, and the exposure is worst in a recovery step or a symptom table, where the reader arrives with something already broken and the least attention to spare. When the runnable form holds a machine-specific value, write the general form and probe that one.
- A "new discovery" — yours or a subagent's — is a false positive until it clears the usual causes: intended implementation (the design intent is written in a comment or another layer), measurement or calculation error (small sample, wrong unit or order), illusion (noise read as a trend, correlation read as causation), local-only judgment (correctness argued from the function alone, callers unread), and instrument error (the measured quantity differs from what its name claims). Only a finding that clears all of these may be useful.

## Reporting
- Own what you discover. An issue found mid-task is never the user's to
  triage: fix it in the same task when it is in scope, delegate or file it
  to the owning backlog when it is not, and name it to the user only when
  it blocks the task or the decision is theirs. An "awareness" or
  "follow-ups" list outsources triage to the reader — the fix for wanting
  to write one is to go do the work.
- Report outcomes, not operations. The reader learns what changed and the
  artifact that proves it (path, commit, URL); the journey — sessions,
  phases, retries, waits, verification mechanics — appears only when the
  user asks how. Wording rules: the "Simplified Technical" output style,
  "Reporting".

## Git
- Removing a stale branch is everybody's responsibility, not its author's. Delete any local branch whose commits already sit on `main` or the remote, whoever created it — a branch left for its owner is how a checkout collects dead refs. Confirm the commits exist elsewhere before you delete. A branch that holds the only copy of its work is not stale: report it and leave it standing.
- Operate on a worktree from the main checkout with `git -C <path>`. Do not `cd` into a worktree inside a command chain that later merges or removes it — the merge then runs inside the worktree ("already up to date") and the removal deletes the shell's own cwd. Edit through the worktree's own absolute paths: a file tool addresses the path it is given, so a shell `cd` does not redirect it, and a main-checkout path keeps writing to the main checkout while the branch you are building stays untouched. Read the working tree's status, not the shell's prompt, to see where an edit landed.
- Merge the protected branch *into* your topic branch, resolve there, then fast-forward the protected branch. A clean merge skips `pre-commit`, but a conflicted one needs a resolution commit, and the no-direct-commits guard blocks it — leaving a half-merged protected branch that another agent can check out.
- Do not assume the shared checkout stays on your branch — and do not move it yourself. `HEAD` is shared state: a peer's switch strands your next commit, and your `git checkout -b` strands theirs onto your branch, where a later fast-forward publishes work you never read. Read `git branch --show-current` before each commit, do branch work in a worktree driven with `git -C`, and before fast-forwarding any branch, read its log for commits you did not author.
- A release tag names the commit that produced the artifact, not `HEAD`. Before you add "one more fix" to a release whose commit already exists, check which tree the tag will point at; when the fix must ship and nothing is pushed yet, rewrite the unpushed history so the fix precedes the release commit, then rebuild the artifact from that tree.

## Filing
Route a durable takeaway by *what would make it wrong*, and report where you filed it.

1. A general rule, true on any repository, machine, or tool, goes to the section of this file that names the work it applies to.
2. A writing or language rule goes to the "Simplified Technical" output style, `~/workspace/.claude/output-styles/simplified-technical.md`.
3. A single tool's or environment's own fact — installed tools, aliases, shell parsing, toolchain paths, a tool's observed behavior, where a resource lives — goes to a `setup-<topic>` memory. It lands in the global pool, `~/.claude/projects/-Users-hyungmokim--claude/memory/`, when the fact holds machine-wide, so every project finds it in one place; it stays in the owning project's pool when only that project touches the tool. Read the global pool's `MEMORY.md` before work that depends on a machine fact.
4. A procedure that coordinates several projects or third-party services — deploying more than one service, driving one project's output into another, anything whose subject is the combination rather than any one member — goes to the workspace pool, `~/.claude/projects/-Users-hyungmokim-workspace/memory/`. The global pool holds a tool's own facts for visibility; a coordination procedure that lands there hides behind a tool name that names only one of its parts.
5. A repository-specific working gotcha — how to build or test *that* codebase — goes to that repository's `.claude/CLAUDE.md`, edited in a worktree and committed like any other change. A debugging pitfall specific to a project's technology or conventions goes instead to that project pool's `pitfalls.md`, per the debugger constitution's own filing rule (`~/.claude/agents/debugger.md`) — never to a `CLAUDE.md` or `docs/`.
6. A product, architecture, or verification truth about a repository goes to that repository's own source of truth (its `docs/` or spec), never to its `CLAUDE.md`.

The rule goes to the general file and the evidence stays with the subject. Write instruction and rationale only: no repository names, no war stories. Before you append, update or merge a near-duplicate instead of stacking one beside it.

A memory file holds one fact and never repeats a fact another pool already holds — link with `[[name]]` instead. It lives in the pool of the project it serves; a fact that serves several projects lives in the workspace pool, whose subject is the combination, and only a single tool's own fact goes to the global pool, where every project can see it. Name it `<subcategory>-<topic>`, keep `MEMORY.md` at one line per file, and set `metadata.type` from the memtype table. A **memtype** is the kind a memory file declares: the subcategory prefix in its name, paired with the `type` row the prefix maps to. A memtype fixes the file's lifecycle and never its pool — the routes above pick the pool by scope. Invent a memtype when none fits, and add it to the table in the same change.

| type | holds | subcategory prefixes | lifecycle |
|---|---|---|---|
| **episodic** | what happened | `history-<topic>` | `history-*` is append-only |
| **semantic** | what is true | `backlog`, `profile-<topic>` | updated in place; a `backlog` item is deleted when it closes |
| **procedural** | how to act | `feedback-<topic>`, `setup-<topic>`, `pitfalls` | updated in place; deleted when the tool or fact is gone |

The memtypes divide by what would make the file wrong. Nothing falsifies `history-`, so it only grows, and it records what version control cannot: changes to unversioned things, and rejected options with their kill reasons. A `backlog` item dies when its work closes; `profile-` states who the owner is. A `setup-` fact is re-derivable by probing the tool, so losing one costs a probe; a `feedback-` rule was bought with an observed failure and is not re-derivable, so losing one repeats the failure. A decision is not a memtype: the choice goes to `history-` when its evidence would otherwise vanish, and the chosen rule lives where rules of its kind live. A file's frontmatter `description` and its `MEMORY.md` line state the file's role, never its contents: an enumerated content list is a mirror that goes stale on the file's next edit.

A file name carries no date and no project name: the pool directory already names the project, so a pool holds exactly one `backlog.md` and at most one `pitfalls.md`. A date in a name forces a rename on every update, and a second write then lands beside the first instead of on it.

Write every item in a `backlog.md` task-bearing section as `- [<m>] YYYY-MM-DD #tag … **Title.** body`, where `<m>` is one of ` ` (open) or `/` (working), the date is the day the item was created, never the day it moved, and each optional `#tag` sits between the date and the title. The marker is the item's state; a tag is an orthogonal annotation that combines with either state. A tag names who the item waits on — `#need-you` waits on the owner — and no tag means the item is workable now. A prose section — Why, How to apply, Horizon, Preliminary research — keeps plain bullets. One fixed grammar lets a reader and a tool read the same file, the tag separates what is waiting from what is merely open, and the creation date makes an item's age visible without a session log. A `PostToolUse` hook, `~/.claude/hooks/check-backlog-format.py`, rejects a write that breaks the grammar.

Work owed to the owner is a `#need-you` item in the pool's `backlog.md`, never a file of its own. The tag already names who the work waits on, and a separate file splits one list into two lists that drift apart.

Done is deletion: an item leaves the file the moment it closes, and no done marker exists. Git history and the repository's own documents hold the evidence of shipped work, so the backlog stays a list of live work. Before you delete a closing item, lift any owed action still buried in it into its own `#need-you` item: a shipped row can still carry unshipped debt.

On every save, take exactly one route: update the file that already covers the topic, promote the item to a rule in this file when it is a general rule in disguise and keep only the evidence, or discard it as derivable from the repository, git history, or a `CLAUDE.md`. Delete memories that turn out wrong, and correct a clearly stale memory or setup fact the moment you observe the mismatch, in the same task — the next session reads the file before it probes the world, so a stale fact left standing misroutes it.

### The pool contract

The block below is this section's machine copy: where a pool lives, how its directory name encodes a project, which two filenames carry the cards and the index, the item grammar, the prose sections, and the frontmatter keys. Every program that reads a pool parses it instead of keeping its own copy of the rule — the `check-backlog-format.py` hook and the board service both do — so a change to any of those shapes is made here, in the same commit as the prose it follows. Two encodings of one rule is how a hook and a reader come to disagree about the same file.

Three values name a rule rather than spell it, and every reader compiles them the same way. `title_style: bold-lead-required` means the text after the date opens with a bold run, so a bullet without one is prose and yields no card. `match: word-prefix` means a heading names a prose section when it equals a listed name, or opens with that name followed by a space or a colon — "Horizon (noted)" is prose, "Whys and wherefores" is not. `column: 0` means an item starts at column 0; an indented bullet is the body of the item above it. The tag values name display rules the same way: `rank: first` lifts a tagged item to the top of its state group, and `emphasis` names the visual weight a surface gives the tag's chip — `accent` or `muted` — never a specific color, which each surface picks from its own palette.

```json contract=pool
{
  "contract": "pool",
  "version": 1,
  "updated": "2026-08-06",

  "pool": {
    "pattern": "projects/*/memory/*.md",
    "board_file": "backlog.md",
    "index_file": "MEMORY.md",
    "encoding": { "replace": ["/", "."], "with": "-" },
    "suffixes": [
      { "match": "-workspace-<repo>", "project": "<repo>" },
      { "match": "-workspace", "project": "workspace", "role": "workspace" },
      { "match": "--claude", "project": "user", "role": "user" }
    ]
  },

  "item": {
    "bullet": "-",
    "column": 0,
    "date": "YYYY-MM-DD",
    "title_style": "bold-lead-required",
    "markers": [
      { "marker": " ", "status": "open" },
      { "marker": "/", "status": "working" }
    ],
    "tags": {
      "position": "after-date",
      "kinds": [
        { "tag": "need-you", "waits_on": "owner", "emphasis": "accent", "rank": "first" }
      ]
    }
  },

  "sections": {
    "prose_prefixes": ["why", "how to apply", "horizon", "preliminary research"],
    "match": "word-prefix"
  },

  "frontmatter": {
    "title": "name",
    "description": "description",
    "type": "metadata.type",
    "conditional_paths": "paths",
    "modified": "metadata.modified"
  }
}
```

@RTK.md
