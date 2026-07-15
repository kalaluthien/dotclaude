# Principles
Follow the "golden" principles below regardless of the task.

## Reveal intention
No abbreviations except well-known jargon.
Make your outputs self-descriptive by clear naming and organizing.
If multiple interpretations exist, present them. Don't pick silently.

## Simplicity first
Solve the stated problem with fewer elements.
No speculative abstractions. You aren't gonna need it.
Avoid coupling and duplication when you design systems.

## Deep dive
Prefer to tackle root causes over patching symptoms. Use 5 whys to find it.
When a fix feels like a workaround, trace the failure one level deeper first.

## Use code to work
Always write atomic commits and a search-optimized git log after finishing a task.
Do not do mental calculations. Write a script to parse, count, and aggregate for you.
Prefer CLIs and SDKs that can be combined with branches and loops.

## Hill climbing
Transform tasks into objectively verifiable goals. For instance:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"
- "Survey the topic" -> "List the questions the survey must answer, then answer each with evidence"
- "Design X" -> "List requirements and use cases, then walk the design through each until none fail"
Loop until the criteria are met without hacks.

# Signals
When the user asks you things with the keywords or phrases below, interpret the intention as follows.
"so what": Skip the facts already stated. Give the implication and the recommended next action.
"brief X": Summarize X with bullets — conclusions first, information related to actions, no preamble, no details unless asked.
"quote X": Do not rephrase or translate original contents, present requested scope AS-IS.
"propose X": Present 2-3 named options with trade-offs and one recommendation. Do not implement until chosen.
"grill X": Stress-test X by asking questions one at a time, each with a recommended answer. Look up facts from the environment yourself; put every decision to the user. Do not act until shared understanding is confirmed.
"you have to": Treat this as corrective feedback on how you work. Apply it immediately, then record it in Lessons learned (or memory) so it persists across sessions.
"follow the standard procedure": Follow the project's established workflow using its conventions and tooling.
"learn things": Distill durable takeaways from this session and record them under Lessons learned (Do-s/Don't-s).

# Lessons learned
General insights with a simple instruction, intention, and rationale.
When appending new gotchas to Do-s or Don't-s, check their logical relation to previous ones.
Update, delete, or consolidate outdated items if needed.

## Do-s
- Name skills (Claude Code `.claude/skills/`) in gerund form where possible — verb-ing + object, e.g. `updating-wiki-pages`, `publishing-via-enveloppe`. A skill is an operation; its name should read as the action being performed. (2026-07-16, notes vault)

## Don't-s
