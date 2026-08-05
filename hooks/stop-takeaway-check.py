#!/usr/bin/env python3
"""Stop hook: ask for a durable-takeaway check, but only after a working turn.

Reads the hook input on stdin. Blocks with the takeaway reminder only when
the just-finished turn — everything after the last real user prompt — made
at least one tool call. A turn that only answered in text has nothing worth
filing, and the reminder on it is noise.

A real user prompt is a main-chain user entry whose content is text; a user
entry carrying tool_result blocks is a tool answer, not a prompt. Sidechain
(subagent) and meta entries are ignored.
"""

import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    if payload.get("stop_hook_active"):
        return 0

    path = payload.get("transcript_path")
    if not path:
        return 0

    tool_call_seen = False
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return 0

    for line in reversed(lines):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("isSidechain") or entry.get("isMeta"):
            continue
        kind = entry.get("type")
        content = (entry.get("message") or {}).get("content")
        if kind == "assistant" and isinstance(content, list):
            if any(b.get("type") == "tool_use" for b in content if isinstance(b, dict)):
                tool_call_seen = True
                break
        if kind == "user":
            if isinstance(content, str):
                break
            if isinstance(content, list) and not any(
                b.get("type") == "tool_result" for b in content if isinstance(b, dict)
            ):
                break

    if tool_call_seen:
        json.dump(
            {
                "decision": "block",
                "reason": (
                    "Before you finish: check this turn for a durable takeaway - "
                    "a rule, a tool or machine fact, feedback, or a decision whose "
                    "evidence would vanish. If one exists, file it per the Filing "
                    "rules in ~/.claude/CLAUDE.md, then finish. If none exists, "
                    "finish now without extra commentary."
                ),
            },
            sys.stdout,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
