# Preferences
Taste-level preferences that hold on any machine, in any repository. Detail
lives in the addressed files:

- Writing and language: `~/workspace/.claude/output-styles/simplified-technical.md`.
  **Ground rule for every document: keep it short, and separate the
  crucial from the detail — obsessively. The body carries only what
  changes the reader's next action; details collapse or get cut.**
- Machine and tool facts: `setup-*` memories in the global pool, per "Filing".
- This file and everything under `~/.claude`: short and clean. Trim an addition in the same change — instruction plus one-clause rationale; narrative goes to a memory or the commit message. Every session loads this file, so each sentence costs every start. (Owner, 2026-08-15.)

## Claude Code
1. Use `PROJECT/.claude/CLAUDE.md` instead of `PROJECT/CLAUDE.md`.
2. Name skills in gerund form — verb-ing plus object, e.g. `updating-wiki-pages`, `delegating`. A skill is an operation; its name reads as the action.
3. Pick the model by task depth and the effort by task breadth. Work whose approach is not yet clear — an extremely hard problem, a request that reads two ways, a design with no obvious shape, a failure nothing has explained — runs Fable; work that decides against an approach already clear (ideation, planning, implementation, review) runs Opus; work that retrieves or condenses knowledge (search, classification, summarization) runs Sonnet. Effort is a thinking budget that both breadth and difficulty spend: high or xhigh for many exceptional cases, a large state space, or one genuinely hard case; low or medium for work both narrow and well understood. Where the two disagree, take the higher — a session started too low meets the hard part with nothing left. A ticket's `#easy` or `#hard` tag is that estimate already made, so read it instead of guessing again. Fable is chosen by the task and never by position. An orchestrator on a tier dearer than Opus delegates its own hands-on editing and debugging, since hands-on work multiplies turns; on Opus it may do narrow hands-on work itself and still delegates anything wide enough to need its own context.
4. Delegate to a constitution-backed subagent or skill the moment its domain appears — the `writing` skill (workspace) when a document view is ordered, `debugger` when anything needs debugging. Applicability decides; do not judge not to use it.

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

## Compute with code
Pick the instrument by the work: the grep and edit tools for a plain search or a fixed edit, a shell command for awkward string work or gluing CLIs together, and Python for data processing, statistics, and arithmetic. Each is the cheapest correct tool for its own kind of work, and reaching past it spends turns.
Do not do mental calculations. Write a script to parse, count, and aggregate, and keep that script when the access path repeats. A script serves computation and repeated access, never a workaround for work you should do directly.

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

Write goal criteria so the honest empty outcome can pass: "remove X, commit,
deploy" becomes "remove X, or report with evidence that no X exists". A
criterion that presumes the work exists leaves a goal-judged session no
passing move when the true answer is "nothing to do" — the judge loops it
until a hook cap kills the turn.

# Craft
Rules with an instruction and its rationale, grouped by the work they apply to. Read the matching section before you commit to a decision, design a system, read a signal, write a document, draw a readout, verify a fix, rewrite git history, or file a takeaway. Debugging method and its filing live in the debugger constitution, `~/.claude/agents/debugger.md`; no `CLAUDE.md` and no `docs/` holds a debugging procedure.

## Deciding
- Estimate the scope and difficulty of a token-consuming move before you start it. Do not overthink or over-engineer.
- Red-team whatever you evaluate: generate 2-3 named options and judge all of them through 2-3 distinct lenses (architecture, consumer, product). Convergence across independent lenses is the accept signal; a single lens is an opinion.
- When told to "decide all other details", decide — and hand the decisions back as a numbered veto table, one line of reason each, so a veto costs the user one line. Decisions buried in prose get re-litigated.
- Before you hand a decision to the user, spend one cheap check that can settle it — read the target, probe the tool, dry-run the move — and act on what the check shows. A question a check can answer costs the user a round-trip for nothing; the user decides only what no check can settle: preference, scope, and destructive stakes.
- Scope a destructive action to the noun that was approved. List the target's contents before removing it, and when the container holds more than the named thing, remove only the named thing or ask again — approval of the part is not approval of the directory around it.

## Design
- Judge a module by the ratio of interface to implementation, not by line count: a deep module hides substantial behavior behind a small surface, and a split that shrinks nothing a caller must know adds net complexity. (Ousterhout, *A Philosophy of Software Design*)
- Classify logic as data, calculation (pure function), or action (side-effect), and push business logic into calculations the effectful shell calls — pure functions are the cheapest thing to test and compose. (Normand, *Grokking Simplicity*; "functional core, imperative shell")
- Reset a reusable resource when you claim it, not when you release it: only the claim path knows what clean means for the work about to start, it always runs, and it does not destroy state the report just delivered still rests on.
- Name a resource, a document, or an artifact generic against change and specific about scope. Generic: no state, verdict, measurement, or candidate label, because updating the thing in place makes any of those false. Specific: the slice of the system it owns, never the genre its directory already carries. Name by role, so one documented mapping carries every setting the role implies. A rename costs every inbound reference, so a name that meets both is left alone.
- A declared contract stays true only while a second reader enforces it — a validator or hook on the authoring side, beside the consumer that reads it. With the consumer as its only reader, the contract drifts exactly like the hardcoded copy it replaced, in a file that looks more authoritative.

## State and events
A signal means less than its name promises. Before you act on one, enumerate everything that produces it and everything that reads it.

- Anchor a wait on a run's own marker, or write the run to a fresh file. A log that is appended to holds every previous run's success line, so a grep over the whole file matches the last run and returns before this one has started — and the failure looks exactly like success.

- Scope a dedupe or idempotency check to unsettled records only. A key naming *what was asked for* rather than *which attempt* repeats whenever the subject returns to a state it has held, so matching it against the whole history answers a fresh request with a settled one — accepted, nothing spawned, no error to read. A failed record must stay repeatable.
- Before you trigger on "this record just came into existence", ask what the store's own maintenance does to that signal. Compaction, repacking and reindexing announce a rewrite exactly as a creation, so a trigger reading the committed event alone fires once per record the store has ever held. The distinguishing evidence sits in the phase before the event lands, where a true creation's subject does not yet exist — sample there.
- Derive a retention window from the longest-lived reader, and enumerate the readers before accepting any premise about who they are. The reader a discussion names is the interesting one, not the durable one: an undo expires in minutes while a drawn card waiting on a human tap outlives it by orders of magnitude. Take the maximum.
- When a list stops being its own enumeration and becomes derived from a mapping, enumerate everything the new source names and add the predicate the list's own use requires. The mapping was built to answer another question, so it carries members the list cannot serve, and admitting them trades a visible gap for an entry that fails at use.
- Let a failure message name only the conditions the code actually read. A message listing a signal no branch inspects sends the next debugger to rule out an absence nobody observed, while the signal it denies may sit in plain view. Re-read the message whenever a settlement or timeout gate is widened.
- Renaming a value a store already holds needs its own migration table, applied unconditionally after the existing one. The existing table is gated on a field's *absence*, so rows added there never fire on records the current build wrote; removing that guard is worse, because the old keys then rewrite records that were already correct. Check the rename against the deployed store, not a fixture.
- Give a polling loop's no-evidence verdict a terminal branch. For a finished subject, absence is the steady state, so mapping "unknown" to "keep waiting" waits forever. Count the quiet polls and exit reporting what was observed; recover the true outcome from a durable source, never by reading the lossy surface harder.

## Documenting
- Write spec and design documents as predicates on system properties, generating rules on system structure, or decision records with reasons — never as mirrors of what the artifact already says. A mirror is redundant on the day it is written and a lie after the artifact's next change.
- Update a document that records history by *adding* to it, never by refreshing what it recorded. A superseded decision keeps its own text under a pointer to what replaced it, and a rejected option keeps the kill reason it was judged on, because a reason rewritten against a rule that did not exist yet claims a judgment nobody made. Name which half of a stale reason the reversal retires, then re-verify the half that still stands.
- Keep a document's commit pin unless the whole document is re-verified: the pin dates every implicit citation, so bumping it during a targeted edit re-points old claims onto a tree they were never read on. Anchor each new claim to its own commit inline.
- When you trim a design, check every cut against the user's stated top-tier requirements and make the deliverable show the mapping (requirement as a predicate -> where the design satisfies it). A cut that serves a requirement but does not show it reads as the requirement being dropped.

## Visual encoding
- Choose a visual form from the data abstraction and the reader's task, never from the domain noun ("it is a knowledge base, so it gets a graph"). State the span and the item count first: node-link legibility collapses past ~50 nodes, a calendar heatmap needs ~90 days of span to beat a bar strip, a swimlane degrades by lane count rather than bar count, and a faceted list is bounded by page size and so never expires.
- Encode a readout's *verdict* only in a channel that carries direction — colour, an icon, a word. Weight and size carry salience, which says "worth reading" and never says "wrong", and the loud state looks self-evident only to whoever already knows which end is bad. Ask whether a reader who does not know the metric could name the good end from the pixels alone; hold the healthy state at the quietest value, and give a bare quantity the shortest label naming what was counted.
- A label earns a control in a browsing surface only when it is not derivable from something already on screen and its values actually divide the set. A taxonomy that routes well at writing time can still be worthless at reading time, so check the label against the filename, the path, and the value distribution before it becomes a facet.
- A control on a view rides on something already drawn — the heading of the thing it acts on, or the element itself — and never takes a full-width row of its own. A row per control spends the screen the control was meant to serve, and a heading that has to grow to hold one is still cheaper than a second line to read past.
- A glyph earns its place only when nothing beside it already says what it says. The owner has struck a caret whose fold the motion showed and an arrow whose direction the verb spelled: a mark that repeats its neighbour still costs the reader the convention it needs, and returns nothing for it.
- A page's single content block takes no section heading, and no heading stands over an empty block while a filled one above it has none. The page title already names a lone block, and a heading over nothing reads as the page's real subject. Before deleting a heading, find what leaned on it: a fact only the heading carried moves onto the items, and its writer can sit in another codebase.
- A UI surface carries labels, values, empty states and errors, and no prose explaining how it behaves. The value beside a label already says what the row is set to, so a sentence under each heading only pushes the rows off the phone; the explanation belongs in the project's `docs/`.

## Verification
A claim argued only from documents, memory, or the artifact you just wrote is unverified. Spend one cheap check that is able to fail. Do not add checks beyond these.

- A regression test earns trust only by failing first: break the behaviour in the source, watch the named test fail, then restore. A test authored against an already-fixed tree can pass for reasons unrelated to the defect. Restore by undoing the one edit you made — `git stash`, `git checkout --` and their kin restore the whole file to its last commit and silently discard any other uncommitted work, invisibly, because the suite goes green either way. Commit first where you can; otherwise unmutate by exact string and re-read the line.
- Before adopting a word for a renamed value, grep the tree *and* `git log -S` it. A word absent from the tree may have been retired deliberately, usually pinned by an assertion that it is *not* present, which a grep for current usage never surfaces; re-adopting one reverses that decision and breaks the pin. A word the tree does hold is the other half of the check: a spec names a field for its new meaning, unaware the key already carries a different one, so read every existing reader before reusing a key.
- Root a verification command at an absolute path. A shell's cwd is state an earlier command set, so a relative search resolves against whichever tree that was, and among several checkouts of one repository the wrong tree answers in the right shape — a confident finding about work you never inspected. Echo the resolved path beside the result whenever the answer decides whether the work is done.
- A delegate killed mid-task is not proof its work is lost: diff its target artifacts before re-running it. A writer often finishes the file before the harness kills the report.
- A liveness verdict on a running agent needs a delta, never a snapshot: read its screen or counters twice and diff its target artifacts between the reads. One read shows a state that can be an hour stale, and answers "alive" and "wedged" with equal confidence.
- A design verdict needs one read-only pass against the actual code — is the claimed state observable, does the surface have the claimed capacity, does a latent defect contradict a premise.
- A documentation claim about a tool's or harness's behavior is a hypothesis: when a decision hinges on one, spend one live probe. Docs lag.
- A command written into a document is copied from a shell where it just succeeded, never retyped to fit the prose. Nothing executes it until a reader does, and a CLI that answers a malformed invocation with a usage message and a non-zero exit reads as a no-op — worst in a recovery step, where the reader arrives with something already broken. When the runnable form holds a machine-specific value, write the general form and probe that one.
- A "new discovery" — yours or a subagent's — is a false positive until it clears the usual causes: intended implementation (the intent is written in a comment or another layer), measurement error (small sample, wrong unit), illusion (noise read as a trend, correlation as causation), local-only judgment (correctness argued from the function alone, callers unread), and instrument error (the measured quantity differs from what its name claims).
- For a change the user sees through a running service, "finished" includes the deploy: rebuild or restart the service and verify the served artifact shows the change. A landed commit leaves the user watching the old build, and a dev-server check does not cover the deployed one.

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
- A task is finished when it is committed, merged, and pushed. Write atomic commits with a search-optimized message, then land and push them without waiting to be asked — this overrides any harness default that says to commit or push only on request. Ask first only when the push is destructive: a force-push, a history rewrite, or a branch you do not own.
- Land every patch on its own branch or worktree. A `pre-commit` guard blocks direct commits to `main`, and a blocked commit means you are on the wrong branch, not that the guard is in the way.
- Never bypass a hook with `git commit --no-verify` on your own. Report what the hook refused and ask; use the flag only after the user confirms it for that commit.
- Removing a stale branch is everybody's responsibility, not its author's. Delete any local branch whose commits already sit on `main` or the remote, whoever created it — a branch left for its owner is how a checkout collects dead refs. Confirm the commits exist elsewhere before you delete. A branch that holds the only copy of its work is not stale: report it and leave it standing.
- Operate on a worktree from the main checkout with `git -C <path>`. Do not `cd` into a worktree inside a command chain that later merges or removes it — the merge then runs inside the worktree ("already up to date") and the removal deletes the shell's own cwd. Edit through the worktree's own absolute paths: a file tool addresses the path it is given, so a shell `cd` does not redirect it, and a main-checkout path keeps writing to the main checkout while the branch you are building stays untouched. Read the working tree's status, not the shell's prompt, to see where an edit landed.
- Merge the protected branch *into* your topic branch, resolve there, then fast-forward the protected branch. A clean merge skips `pre-commit`, but a conflicted one needs a resolution commit, and the no-direct-commits guard blocks it — leaving a half-merged protected branch that another agent can check out.
- Do not assume the shared checkout stays on your branch — and do not move it yourself. `HEAD` is shared state: a peer's switch strands your next commit, and your `git checkout -b` strands theirs onto your branch, where a later fast-forward publishes work you never read. Read `git branch --show-current` before each commit, do branch work in a worktree driven with `git -C`, and before fast-forwarding any branch, read its log for commits you did not author.
- A release tag names the commit that produced the artifact, not `HEAD`. Before you add "one more fix" to a release whose commit already exists, check which tree the tag will point at; when the fix must ship and nothing is pushed yet, rewrite the unpushed history so the fix precedes the release commit, then rebuild the artifact from that tree.

## Filing
Route a durable takeaway by *what would make it wrong*, and report where you filed it.

1. A general rule, true on any repository, machine, or tool, goes to the section of this file that names the work it applies to.
2. A writing or language rule goes to the "Simplified Technical" output style, `~/workspace/.claude/output-styles/simplified-technical.md`.
3. A single tool's or environment's own fact — installed tools, aliases, shell parsing, toolchain paths, a tool's observed behavior, where a resource lives — goes to a `setup-<topic>` memory. It lands in the global pool, `~/.claude/projects/-Users-hyungmokim--claude/memory/`, when the fact holds machine-wide, so every project finds it in one place; it stays in the owning project's pool when only that project touches the tool. Read the global pool's `MEMORY.md` before work that depends on a machine fact. A fact that governs authoring files under a recognizable path pattern goes instead to the matching path-scoped rule in `~/.claude/rules/`, which loads itself when a matching file is read; `setup-*` keeps the facts with no path signature (owner redirect, 2026-08-15, dotclaude 98af604).
4. A procedure that coordinates several projects or third-party services — deploying more than one service, driving one project's output into another, anything whose subject is the combination rather than any one member — goes to the workspace pool, `~/.claude/projects/-Users-hyungmokim-workspace/memory/`. The global pool holds a tool's own facts for visibility; a coordination procedure that lands there hides behind a tool name that names only one of its parts.
5. A repository-specific working gotcha — how to build or test *that* codebase — goes to that repository's `.claude/CLAUDE.md`, edited in a worktree and committed like any other change. A debugging pitfall specific to a project's technology or conventions goes instead to that project pool's `pitfalls.md`, per the debugger constitution's own filing rule (`~/.claude/agents/debugger.md`) — never to a `CLAUDE.md` or `docs/`.
6. A product, architecture, or verification truth about a repository goes to that repository's own source of truth (its `docs/` or spec), never to its `CLAUDE.md`.

The rule goes to the general file and the evidence stays with the subject. Write instruction and rationale only: no repository names, no war stories. Before you append, update or merge a near-duplicate instead of stacking one beside it.

A memory file holds one *subject* — the facts a reader asks for in one go, as `##` sections of one file — and never repeats a fact another pool already holds; link with `[[name]]` instead. Merge a new fact into the file whose subject covers it rather than opening a sibling: every extra file is a line every session loads and one more place to look (owner, 2026-08-18). It lives in the pool of the project it serves; a fact that serves several projects lives in the workspace pool, whose subject is the combination, and only a single tool's own fact goes to the global pool, where every project can see it. Name it `<subcategory>-<topic>`, keep `MEMORY.md` at one line per file, and set `metadata.type` from the memtype table. A **memtype** is the kind a memory file declares: the subcategory prefix in its name, paired with the `type` row the prefix maps to. A memtype fixes the file's lifecycle and never its pool — the routes above pick the pool by scope. Invent a memtype when none fits, and add it to the table in the same change.

| type | holds | subcategory prefixes | lifecycle |
|---|---|---|---|
| **episodic** | what happened | `history-<topic>` | `history-*` is append-only |
| **semantic** | what is true | `backlog`, `topic-<topic>` | updated in place; a `backlog` item is deleted when it closes |
| **procedural** | how to act | `feedback-<topic>`, `setup-<topic>`, `pitfalls` | updated in place; deleted when the tool or fact is gone |

The memtypes divide by what would make the file wrong. Nothing falsifies `history-`, so it only grows, and it records what version control cannot: changes to unversioned things, and rejected options with their kill reasons. A `backlog` item dies when its work closes. A `topic-` file states the current truth of one subject and is updated in place; the events that made it true stay in the paired `history-` file. It splits from `setup-` by recovery cost: a `setup-` fact is one probe away, a `topic-` truth was bought by analysis no probe re-derives. Neither holds external technical knowledge, which belongs to the notes wiki, nor a repository's own truth, which belongs to that repository's `docs/`. A `feedback-` rule was given by the owner — a correction bought with an observed failure, or a standing fact about what they prefer — so losing one repeats the failure or re-asks the owner. A decision is not a memtype: the choice goes to `history-` when its evidence would otherwise vanish, and the chosen rule lives where rules of its kind live. A file's frontmatter `description` and its `MEMORY.md` line state the file's role, never its contents, because a content list goes stale on the file's next edit.

A file name carries no date and no project name: the pool directory already names the project, so a pool holds at most one `pitfalls.md`. A date in a name forces a rename on every update, and a second write then lands beside the first instead of on it.

On every save, take exactly one route: update the file that already covers the topic, promote the item to a rule in this file when it is a general rule in disguise and keep only the evidence, or discard it as derivable from the repository, git history, or a `CLAUDE.md`. Promotion has a threshold: a takeaway observed once — however general it sounds — files as a `feedback-*` or `pitfalls` entry with its evidence, and moves into this file only when a later, independent task confirms it. One observation cannot tell a rule from a coincidence, and a premature rule costs every future session that obeys it. Delete memories that turn out wrong, and correct a clearly stale memory or setup fact the moment you observe the mismatch, in the same task — the next session reads the file before it probes the world, so a stale fact left standing misroutes it.

### Tickets

A ticket is one filed piece of work. Tickets live in the board server's own store, not in files (owner decision 2026-08-19; board `docs/data-ticket-store.html`). File, change, and close a ticket by calling the server at `localhost:8300` — never by writing a file. The five doors, and the dry run:

- `POST /api/tickets` — file a ticket into a pool; with `?validate=1` it runs every check and writes nothing (the dry run).
- `PATCH /api/tickets/{id}/head` — the marker, tags, labels, and title.
- `PATCH /api/tickets/{id}/body` — the body fields and the prose, replaced whole.
- `POST /api/tickets/{id}/claim` — take the working marker; the store refuses a row another session holds.
- `DELETE /api/tickets/{id}` — close. Closing deletes the row, and the event log keeps its words.

Read tickets from `GET /api/snapshot` on the same server: it carries every pool's cards, from the store and from any pool file still standing.

The ticket grammar — markers, tag kinds, labels, body fields, bounds, and the reasons behind them — is board's spec, `~/workspace/board/docs/data-ticket-contract.md`; the request shapes are the server's `/openapi.json`. The door checks a request against the grammar before the write, and a refusal is typed: fix what it names and call again. A working example, run 2026-08-19:

    curl -s -X POST 'http://localhost:8300/api/tickets?validate=1' -H 'Content-Type: application/json' -d '{"pool":"workspace","title":"Probe the filing door.","labels":["PROBE"],"tags":["docs"],"fields":{"what":"Check the dry run answers.","why":"A documented command must have run once.","how":"Discard the answer."}}'

Work owed to the owner is a `#need-you` ticket in the owning pool, never a file or a second list. A `#need-you` ticket holds its own next transition: never start an open one and never close a working one on your own initiative. A prompt saying the owner confirmed the row carries the owner's decision, so it starts the row and drops the tag. Before closing any ticket, lift an owed action still buried in it into its own `#need-you` ticket: a shipped row can still carry unshipped debt.

Two shapes coexist until the last pool file goes. A **migrated pool** (today: garden, mabinogi-mobile-automation) has no `backlog.md`; every one of its tickets is in the store. A pool whose **`backlog.md` still stands** (today: camera, notes, workspace, board) is still read as before, and a row already in that file is changed or closed by editing that file — one row at a time, with the Edit tool — until the pool migrates. A new ticket goes through the door for every pool, migrated or not, and nothing ever creates a `backlog.md`: a deleted one stays deleted.

### The pool contract

The block below is the machine copy of the memory-pool half: where a pool lives, how its directory name encodes a project, the index file, the prose-section rule, and the frontmatter keys. Every program that reads a pool parses it instead of keeping its own copy — the board service and the `check-memtype.py` hook both do — so a change to any of those shapes is made here, in the same commit as the prose it follows. A value the deployed board cannot compile empties its surfaces, so a widening ships in board first (the workspace pool's `topic-pool-contract-rollout`).

The block's `item` half is the ticket grammar of the pool files that still stand, kept only for them: the deployed board still compiles it to read those files. The grammar's home is now board's `contract=ticket` block in `data-ticket-contract.md`; the two copies must agree while both exist, so edit this one only together with board's, and this copy retires with the last `backlog.md`.

```json contract=pool
{
  "contract": "pool",
  "version": 1,
  "updated": "2026-08-19",

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
    "label": {
      "position": "title-lead",
      "spelling": "in-brackets",
      "vocabulary": "free-text",
      "required": true,
      "means": "which rows of the file this one belongs with"
    },
    "body": {
      "style": "labeled-fields",
      "field_max_chars": 160,
      "fields": [
        { "label": "what", "required": true, "reader": "both",
          "means": "the work in one plain sentence" },
        { "label": "why", "required": true, "reader": "reviewer",
          "means": "why the item exists, and why this way of solving it was chosen — in simple sentences" },
        { "label": "how", "required": true, "reader": "reviewer",
          "means": "the next step and who takes it" },
        { "label": "where", "required": false, "reader": "worker",
          "means": "what the worker touches" },
        { "label": "when", "required": false, "reader": "both",
          "means": "dependencies in and out — rows in other backlogs this item waits on, and rows there that wait on it" },
        { "label": "context", "required": false, "reader": "worker",
          "means": "the detailed context — paths, commits, dates, and everything the other fields do not carry" }
      ]
    },
    "markers": [
      { "marker": " ", "status": "open" },
      { "marker": "/", "status": "working" }
    ],
    "tags": {
      "position": "after-date",
      "reason": "in-parentheses",
      "reason_max_chars": 40,
      "scope_required": true,
      "effort_default": "medium",
      "kinds": [
        { "tag": "need-you", "waits_on": "owner", "emphasis": "accent", "rank": "first",
          "means": "the next step is the owner's" },
        { "tag": "easy", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "effort": "low",
          "field_max_chars": 120,
          "means": "the work is well understood and narrow, so a session needs little thinking to finish it" },
        { "tag": "hard", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "effort": "high",
          "field_max_chars": 200,
          "means": "the work is difficult or reads more than one way, so a session needs room to think" },
        { "tag": "optional", "waits_on": "nobody", "emphasis": "muted", "rank": "last",
          "means": "the item is worth reading after its untagged neighbours" },
        { "tag": "agent", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "scope": true,
          "means": "the change is to how an agent is instructed or configured — an instruction file, a constitution, a skill, a prompt" },
        { "tag": "code", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "scope": true,
          "means": "the change is to a program a machine runs — source, a script, a configuration it reads" },
        { "tag": "docs", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "scope": true,
          "means": "the change is to a document a person reads — a view, a wiki page, a report" },
        { "tag": "spec", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "scope": true,
          "means": "the change is to a spec — a contract or rule document that programs and agents obey" },
        { "tag": "eval", "waits_on": "nobody", "emphasis": "muted", "rank": "none", "scope": true,
          "means": "the change is to an eval — a graded scenario or benchmark that measures an agent's output quality" },
        { "tag": "test", "waits_on": "nobody", "emphasis": "muted", "rank": "early", "scope": true,
          "means": "the change is to what checks the work — a test, a fixture, a hook or guard that enforces a rule" }
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
