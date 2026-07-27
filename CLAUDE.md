# Preferences
Taste-level preferences that hold on any machine, in any repository.
Writing and language rules live in the "Simplified Technical" output style
(`~/.claude/output-styles/simplified-technical.md`), not here. Machine and
tool facts live as `setup-*` topic memories (see `~/.claude/rules/memory-types.md`).

## Claude Code
1. Use `PROJECT/.claude/CLAUDE.md` instead of `PROJECT/CLAUDE.md`.
2. Name skills in gerund form — verb-ing + object, e.g. `updating-wiki-pages`,
   `delegating`. A skill is an operation; its name reads as the action.
3. Subagents run on Opus, never Fable: medium effort for search, coding, and
   script runs; high effort for planning and other knowledge work.

## Signals
When the user asks you things with the keywords or phrases below, interpret the intention as follows.
"so what": Skip the facts already stated. Give the implication and the recommended next action.
"brief X": Summarize X with bullets — conclusions first, information related to actions, no preamble, no details unless asked.
"quote X": Do not rephrase or translate original contents, present requested scope AS-IS.
"propose/suggest X": Present 2-3 named options with trade-offs and one recommendation. Do not implement until chosen.
"grill X": Stress-test X by asking questions one at a time, each with a recommended answer. Look up facts from the environment yourself; put every decision to the user. Do not act until shared understanding is confirmed.
"yes/no": Answer yes or no. No additional explanations. No exceptions.
"clean X": Close every open item on X — pending update, undecided decision, and repository leftover (uncommitted change, unsynced remote, unpublished output). Report anything that cannot close.
"learn things": Distill durable takeaways from this session or project auto-memory and record them under Lessons learned (Do-s/Don't-s). Route each one by *what would make it wrong* — where it goes:
- **General rule**, true regardless of repo, machine, or tool -> this file. Instruction and rationale only; no repo names, no war stories.
- **Writing or language rule** -> the Simplified Technical output style.
- **Machine or environment fact** (installed tools, aliases, shell parsing, toolchain paths) -> a `setup-*` topic memory per `~/.claude/rules/memory-types.md`.
- **Repo-specific working gotcha** — how to build, test, or debug *this* codebase -> that repo's `.claude/CLAUDE.md`, in a worktree and committed like any other change.
- **Product, architecture, or verification truth about a repo** -> that repo's own source of truth (its `docs/` or spec), never its CLAUDE.md.
The rule goes to the general file and the evidence stays with the subject. Say where each takeaway was filed.

# Principles
MUST follow the "golden" principles below regardless of the task.

## Reveal intention
1. No abbreviations (e.g., D1, RQ1, P1, ...) except for well-known jargon.
2. Make your outputs self-descriptive by unambiguous naming and meaningful organizing.
3. If multiple interpretations exist, present them. Don't pick silently.

## Simplicity first
1. Solve the stated problem with fewer elements as much as possible.
2. No predictive and speculative abstractions. You aren't gonna need it.
3. Avoid coupling and duplication when you design any kind of systems.

## Deep dive
1. No shotgun approach when fixing bug or bottleneck.
2. When a fix feels like a workaround, trace the failure one level deeper first.
3. Prefer to tackle root causes over patching symptoms. Use the 5 whys technique to find it.

## Code to work
1. Always write atomic commits and a search-optimized git message after finishing a task.
2. Do not do mental calculations. Write a script to parse, count, and aggregate for you.
3. Write scripts for repeated complex access to external dependencies. Do not write same script again and again.

## Hill climbing
Transform tasks into objectively verifiable goals. Loop until the criteria are met without hacks.
For instance:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"
- "Survey the topic" -> "List the questions the survey must answer, then answer each with evidence"
- "Design X" -> "List requirements and use cases, then walk the design through each until none fail"

# Lessons learned
General insights with a simple instruction, intention, and rationale.
When appending a new gotcha, check its logical relation to previous ones.
Update, delete, or consolidate outdated items if needed.

## working-method
- Before a token-consuming move, estimate its scope and difficulty first. Do not overthink or over-engineer. (2026-07-18)
- When asked to evaluate or critique something, do strict adversarial verification — the agent should red-team it. For design work, extend this to generation: develop 2-3 named options and set 2-3 critics with distinct lenses (e.g. architecture, consumer/programmability, product) on all of them. A synthesis that converges across independent lenses is the strongest accept signal; a single-lens verdict is an opinion. (2026-07-18, extended 2026-07-23)
- When told to "decide all other details", decide — and hand the decisions back as a numbered veto table (decision + one-line reason each). The user reviews instead of re-deriving, and a veto costs them one line. Silent decisions buried in prose get re-litigated. (2026-07-23)
- Reset a reusable resource when you claim it, not when you release it. The claim path always runs and is the only point that knows what clean means for the work about to start; the release path is skipped by every interruption, escalation, and timeout, and it destroys state that is still evidence for the report just delivered. (2026-07-27)

## design
- Judge a module by the ratio of interface to implementation, not by line count: a deep module hides substantial behavior behind a small surface, and a split that multiplies files without shrinking what callers must know adds net complexity. (Ousterhout, *A Philosophy of Software Design*) (2026-07-22)
- Classify logic as data, calculation (pure function), or action (side-effect), and push business logic toward calculations the effectful shell calls — pure functions are the cheapest thing to test and compose. (Normand, *Grokking Simplicity*; the "functional core, imperative shell" pattern) (2026-07-22)
- Write spec and design documents as predicates on system properties, generating rules on system structure, or decision records with reasons — never as mirrors of what the artifact already says. A mirror is redundant on the day it is written and a lie after the artifact's next change. (2026-07-22)
- When simplifying or trimming a design, check every cut against the user's stated top-tier requirements, and make the deliverable show the mapping (requirement as a predicate -> where the design satisfies it). A cut that serves a requirement but does not show it reads as the requirement being dropped, and costs a rework round. (2026-07-23)

## debugging
- Debug a driven action that does nothing (no effect, no error) by going deeper, not wider: read the tool/framework's own diagnostics first (idle/timeout/harness warnings usually name the cause), then log each decision point to bisect where the pipeline breaks. Re-trying different ways to trigger it is symptom-thrashing that can burn hours. (2026-07-19)
- To find who owns an effect, ablate the suspect instead of reasoning about it: disable the code believed to cause the symptom and re-run. If the symptom survives, the owner is elsewhere — usually a framework acting on its own signal rather than your call site. One cheap run replaces a long chain of inference, and it is the sharp instrument for the deeper-not-wider rule above. (2026-07-19)

## verification
- A regression test earns trust only by failing first. Before believing a new test covers the bug, revert the fix (`git stash`), watch the test fail, then restore. A test authored against an already-fixed tree can pass for reasons unrelated to the defect, and a green suite then certifies nothing. (2026-07-19)
- When an automated check fails but the manual flow or a sibling test passes, suspect the harness before the product; isolate the delta between the passing and failing conditions, changing one variable at a time. In a suite already known to flake, the discriminator is whether the *same* assertion fails: a failure that moves between assertions across runs — and reproduces on the unchanged baseline under the same conditions — is environmental, not caused by the change under test. (2026-07-19)
- A design verdict argued only against documents is unverified. Before shipping it, run one read-only pass that checks its feasibility claims against the actual code: is the claimed state observable, does the surface have the claimed capacity, does a latent defect contradict a premise. A document-grounded debate can be unanimous and still wrong about the code. (2026-07-23)
- Do not read a changed failure mode — a new error, a later failing line — as progress; verify the new state against ground truth (logs, the actual effect) before believing the earlier cause is gone. (2026-07-19)
- Treat documentation claims about a tool's or harness's behavior as hypotheses; when a design decision hinges on one, verify with a cheap live probe before building on it. Docs lag, and a probe costs one run. (2026-07-16, promoted from project memory 2026-07-27)
