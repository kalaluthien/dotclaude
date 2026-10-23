---
name: break-me
description: Use when the user holds a conclusion and wants it tested before acting on it, by a check that could prove it wrong. Not for an open plan or decision, which grill-me takes, nor for brainstorming.
disable-model-invocation: true
---

The user believes the problem, its answer and their understanding are all clear. Your job is to find out whether that conclusion survives a check that could fail, before they act on it. Steelman it first: the aim is to test it, not to argue against it, and you concede at once whatever holds.

Every step is a question the user only answers: ask by `AskUserQuestion`, at most four questions a round, the recommended option first with `(Recommended)` in its label, or as text when the tool is missing; then wait. Only go to the next step when the user has answered the last.

- **Claim**: restate the conclusion as "if X, then Y is observed"; the user confirms or corrects it.
- **Crux**: ask what fact would change their mind, before any evidence. If none would, the claim cannot be tested yet; ask for one.
- **Attack**: imagine it is later and the conclusion proved wrong; name why. Add the strongest rival explanation and the edge case. Keep only attacks a check could decide.
- **Check**: the cheapest check that fails if the claim is wrong. Run it yourself when Read, Grep or a command can; else ask the user for that one result, naming where to look.
- **Verdict** from the check alone: `holds` (the user acts; no doubt kept), `bent` (restate the narrower claim the evidence supports; the user confirms), or `broken` (show the failing result; offer `/grill-me` to rework the plan).

Facts are yours to find; decisions and what only the user can see are theirs.
