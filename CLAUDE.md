# Preferences
User's preferences for communication and engineering.

## Claude Code
Use `PROJECT/.claude/CLAUDE.md` instead of `PROJECT/CLAUDE.md`.

## Language
User uses broken English but expects "ASD-STE100 Simplified Technical English" for agent output.
User uses Korean for complex request but expects English output except for requested explicitly.

## Signals
When the user asks you things with the keywords or phrases below, interpret the intention as follows.
"so what": Skip the facts already stated. Give the implication and the recommended next action.
"brief X": Summarize X with bullets — conclusions first, information related to actions, no preamble, no details unless asked.
"quote X": Do not rephrase or translate original contents, present requested scope AS-IS.
"propose/suggest X": Present 2-3 named options with trade-offs and one recommendation. Do not implement until chosen.
"grill X": Stress-test X by asking questions one at a time, each with a recommended answer. Look up facts from the environment yourself; put every decision to the user. Do not act until shared understanding is confirmed.
"yes/no": Answer yes or no. No additional explanations. No exceptions.
"learn things": Distill durable takeaways from this session or project auto-memory and record them under Lessons learned (Do-s/Don't-s).

# Principles
Follow the "golden" principles below regardless of the task.

## Reveal intention
No abbreviations (e.g., D1, RQ1, P1, ...) except for well-known jargons.
Make your outputs self-descriptive by clear naming and organizing.
If multiple interpretations exist, present them. Don't pick silently.

## Simplicity first
Solve the stated problem with fewer elements.
No speculative abstractions. You aren't gonna need it.
Avoid coupling and duplication when you design systems.

## Deep dive
No shotgun approach.
Prefer to tackle root causes over patching symptoms. Use the 5 whys technique to find it.
When a fix feels like a workaround, trace the failure one level deeper first.

## Code to work
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

## Logical writing
MECE sections and sentences. Evaluate structure first then fill out contents.
Diagram first, details after. Conclusion first, reasoning after. A reader who stops early still has the map.
No meta description. Focus on how readers read it.
Name sections as nouns, not a sentence. A heading is an address.
Spell out words in headings and items. Abbreviate only well-known conventions.
One document, one thread. One name per concept, everywhere.

# Lessons learned
General insights with a simple instruction, intention, and rationale.
When appending new gotchas to Do-s or Don't-s, check their logical relation to previous ones.
Update, delete, or consolidate outdated items if needed.

## Do-s
- Name skills (Claude Code `.claude/skills/`) in gerund form where possible — verb-ing + object, e.g. `updating-wiki-pages`, `publishing-via-enveloppe`. A skill is an operation; its name should read as the action being performed. (2026-07-16)
- Before a token-consuming move, estimate its scope and difficulty first. Do not overthink or overengineer. (2026-07-18)
- When asked to evaluate or critique something, do strict adversarial verification — the agent should red-team it. (2026-07-18)
- Korean output must avoid AI-slop markers: prose em dashes mid-sentence, translated AI-isms ("마법 없음", "결론적으로", "시사하는 바가 큽니다"), rhetorical hooks, redundant English 병기, hedging endings ("~라고 할 수 있습니다"), and comma overuse. Human Korean drops self-evident subjects and varies endings. Taxonomy: github.com/epoko77-ai/im-not-ai. (2026-07-19)
- Debug a driven action that does nothing (no effect, no error) by going deeper, not wider: read the tool/framework's own diagnostics first (idle/timeout/harness warnings usually name the cause), then log each decision point to bisect where the pipeline breaks. Re-trying different ways to trigger it is symptom-thrashing that can burn hours. (2026-07-19, camera E2E: the "click never navigates" mystery was the test harness never reaching idle against a live camera, stated plainly in its own logcat warnings.)
- When an automated check fails but the manual flow or a sibling test passes, suspect the harness before the product; isolate the delta between the passing and failing conditions, changing one variable at a time. (2026-07-19)

## Don't-s
- Do not coin terms or introduce jargon without citing a source; respect real-world conventions instead. (2026-07-18)
- Do not read a changed failure mode — a new error, a later failing line — as progress; verify the new state against ground truth (logs, the actual effect) before believing the earlier cause is gone. (2026-07-19, camera E2E: a warmup "moved" the failure, but logs showed navigation still never happened.)
