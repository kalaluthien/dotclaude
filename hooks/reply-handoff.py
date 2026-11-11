#!/usr/bin/env python3
"""Stop hook: block a final reply that hands the owner a command to run (a `! <command>` line, or "run `x`" beside a
code span) when no tool call of the turn was refused, since a tool the session holds can run it. The block repeats once
at most: a second stop (`stop_hook_active`), a refusal earlier in the turn, or any error passes."""
import json
import re
import sys

CODE = r"```.*?```|`[^`\n]+`"
BANG = re.compile(r"^[ \t]*(?:`+[ \t]*)?!\s+\S", re.M)
ASK = re.compile(
    r"(?:실행|입력|붙여\s*넣|돌려)\s*(?:해|하)\s*(?:주|보|시|세|십|줄|달)|직접\s*(?:실행|입력)"
    r"|\b(?:please\s+run|you\s+(?:can|could|need\s+to|must|should)\s+run|run\s+(?:this|the\s+following|it)\s+(?:yourself|command))\b"
    r"|\brun\s+`|\btype\s+`",
    re.I,
)
REFUSED = re.compile(r"denied|blocked|refused|not allowed|hook error|disabled|no such tool", re.I)
INJECTED = re.compile(r"<(system-reminder|command-[\w-]+|task-notification|local-command-[\w-]+)>.*?</\1>", re.S)
REASON = (
    "Your reply hands the owner a command to run, but no tool call this turn was refused: {shown}. "
    "Run the step now with a tool you hold, then report the result; hand over a command only after a tool refuses it, "
    "naming the refusal."
)


def blocks(content):
    return content if isinstance(content, list) else [{"type": "text", "text": content or ""}]


def refused_this_turn(lines):
    """True when a tool result after the latest typed user message is an error that reads as a refusal."""
    refused = False
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        content = blocks((entry.get("message") or {}).get("content")) if isinstance(entry, dict) else []
        if entry.get("type") != "user":
            continue
        results = [b for b in content if isinstance(b, dict) and b.get("type") == "tool_result"]
        if results:
            for b in results:
                text = json.dumps(b.get("content"), ensure_ascii=False)
                refused = refused or bool(b.get("is_error") and REFUSED.search(text))
            continue
        typed = INJECTED.sub("", "".join(b.get("text", "") for b in content if isinstance(b, dict))).strip()
        if typed and not entry.get("isMeta") and not typed.startswith("[Request interrupted"):
            refused = False
    return refused


def handoff(reply):
    """The first span of the reply that hands over a command, else None."""
    code = re.compile(CODE, re.S)
    found = BANG.search(reply)
    if found:
        return reply[found.start():].strip().splitlines()[0][:80]
    for m in ASK.finditer(reply):
        if code.search(reply[max(0, m.start() - 200):m.end() + 200]):
            return reply[max(0, m.start() - 20):m.end() + 40].strip().replace("\n", " ")
    return None


def main():
    try:
        event = json.load(sys.stdin)
        if event.get("stop_hook_active"):
            return
        shown = handoff(event.get("last_assistant_message") or "")
        if not shown:
            return
        with open(event["transcript_path"], encoding="utf-8") as transcript:
            if refused_this_turn(transcript):
                return
    except Exception:
        return
    print(json.dumps({"decision": "block", "reason": REASON.format(shown=f"“{shown}”")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
