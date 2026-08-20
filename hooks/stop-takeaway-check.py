#!/usr/bin/env python3
"""Stop hook: ask for a durable-takeaway check, but only after real work.

Reads the hook input on stdin. Blocks the stop only when the session has
changed at least WORK_THRESHOLD things since this hook last fired.

Two properties of that condition matter, and each fixes an observed failure:

  The window starts at this hook's own previous fire, not at the last user
  prompt. The hook fires again a few seconds after it blocks, and a window
  anchored on the prompt still holds every tool call of the turn, so the same
  lesson arrives twice with nothing new between the two. Anchored on the last
  fire, the second window is empty and the hook stays quiet.

  The work counted is what changed something - a file write or edit, or a
  shell command that writes, commits, or calls a service door. Reads, probes,
  searches, and worker launches are not counted. An orchestration turn that
  reads a ticket, launches a worker and arms a watch runs many tools and
  settles nothing, so counting raw tool calls asks it to harvest a takeaway
  from work that has not happened yet.

A subagent's work does not count either: it is on the sidechain, and a
subagent files its own takeaways.

The threshold of three is the smallest window that holds a landed piece of
work - one edit, one commit, one push. Replaying the 2021 recorded firings of
this hook over 500 sessions (2026-08-04 to 2026-08-19) with
`~/workspace/scripts/stop-hook-survey --counterfactual`, three is also the
last step whose marginal cost is worth paying: each step up to three drops
more than five barren blocks per block that produced a filing, and the next
step drops three.
"""

import json
import re
import sys

# Change either of these two and the numbers in `stop-hook-survey
# --counterfactual` are the measurement to redo, not a claim to restate.
WORK_THRESHOLD = 3
CHANGING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
CHANGING_COMMAND = re.compile(
    r">>|(^|\s)>\s|\btee\b|sed -i"
    r"|\bgit (commit|push|merge|tag|revert|rebase)\b"
    r"|-X\s+(POST|PATCH|PUT|DELETE)"
    r"|\b(mv|rm|cp|mkdir|touch|install)\b"
)

HOOK_NAME = "stop-takeaway-check.py"
REASON = (
    "Before you finish: check the work since the last check for a durable "
    "takeaway - a rule, a tool or machine fact, feedback, or a decision whose "
    "evidence would vanish. If one exists, file it per the Filing rules in "
    "~/.claude/CLAUDE.md, then finish. If none exists, finish now without "
    "extra commentary."
)
REASON_MARK = "durable takeaway"


def changes_something(block):
    """True when this tool call changed something outside the session."""
    name = block.get("name")
    if name in CHANGING_TOOLS:
        return True
    if name != "Bash":
        return False
    return bool(CHANGING_COMMAND.search((block.get("input") or {}).get("command") or ""))


def is_previous_fire(entry):
    """True for the summary entry the harness wrote when this hook last ran."""
    if entry.get("type") != "system" or entry.get("subtype") != "stop_hook_summary":
        return False
    commands = " ".join(i.get("command", "") for i in (entry.get("hookInfos") or []))
    if HOOK_NAME in commands:
        return True
    return REASON_MARK in " ".join(entry.get("hookErrors") or [])


def work_done(entries):
    """Count the changing tool calls made since this hook last fired."""
    count = 0
    for entry in reversed(entries):
        if entry.get("isSidechain") or entry.get("isMeta"):
            continue
        if is_previous_fire(entry):
            break
        if entry.get("type") != "assistant":
            continue
        content = (entry.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use" \
                    and changes_something(block):
                count += 1
    return count


def should_block(entries):
    """The hook's whole decision, replayable over a recorded transcript."""
    return work_done(entries) >= WORK_THRESHOLD


def entries_of(path):
    """Every JSON line of a transcript, in order; unreadable lines are skipped."""
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError:
        return None
    parsed = []
    for line in lines:
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return parsed


def main() -> int:
    payload = json.load(sys.stdin)
    if payload.get("stop_hook_active"):
        return 0

    path = payload.get("transcript_path")
    if not path:
        return 0
    entries = entries_of(path)
    if entries is None:
        return 0

    if should_block(entries):
        json.dump({"decision": "block", "reason": REASON}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
