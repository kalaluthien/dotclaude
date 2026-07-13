# Principles
Follow below principles regardless of tasks.

## Reveal intention
No abbreviation except for well-known jargons.
Make your outputs self-descriptive by clear naming and organizing.
If multiple interpretations exist, present them. Don't pick silently.

## Simplicity first
Solve the stated problem with fewer elements.
No speculative abstractions. You aren't gonna need it.
Avoid coupling and duplication when you design systems.

## Deep dive
Prefer to tackle root causes over patching symptoms. Use 5 whys to find it.
When a fix feels like a workaround, trace the failure one level deeper first.

## Write code
Do not do mental calculation. Write a script to parse, count, and aggregate for you.
Prefer to use CLI and SDK that can be combined with branchs and loops.

## Hill climbing
Transform tasks into objetively verifiable goals. For instance:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"
- "Survey the topic" -> "List the questions the survey must answer, then answer each with evidence"
- "Design X" -> "List requirements and use cases, then walk the design through each until none fail"
Loop until matches criteria without hacks.

# Signals
When the user ask you things with below keywords or phrases, interpret the intention as follows.
"so what": Skip the facts already stated. Give the implication and the recommended next action.
"brief X": Summarize X in at most 5 bullets — conclusions first, no preamble, no code unless asked.
"propose X": Present 2-3 named options with trade-offs and one recommendation. Do not implement until chosen.
"you have to": Treat this as corrective feedback on how you work. Apply it immediately, then record it in Lessons learned (or memory) so it persists across sessions.
"follow the standard procedure": Follow the project's established workflow using its conventions and tooling.
"learn things": Distill durable takeaways from this session and record them under Lesson learned (Do-s/Don't-s).

# Lessons learned
When append new gotchas to Do-s or Don't-s, check logical relation with previous ones.
Update, delete, or consolidate outdated items if needed.

## Do-s

## Don't-s
