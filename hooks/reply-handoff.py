#!/usr/bin/env python3
"""Stop hook: block a final reply that hands the owner a command to run (a `! <command>` line, or "run `x`" beside a
code span) when no tool call of the turn was refused, since a tool the session holds can run it. The block repeats once
at most: a second stop (`stop_hook_active`), a refusal earlier in the turn, or any error passes. A match passes when its own
sentence only reports a run, done or not done: it ends in a past tense or a copula and
holds no request or question word, since another sentence that hands a command over has its own match. A sentence
naming a code span beside a run, type or paste verb is a hand-off when it is no such report and holds a request word
or ends in an imperative."""
import json
import re
import sys

CODE = r"```.*?```|`[^`\n]+`"
BANG = re.compile(r"^[ \t]*(?:`+[ \t]*)?!\s+[\w./~$-]", re.M)
ASK = re.compile(
    r"(?:실행|입력|붙여\s*넣|돌려)\s*(?:해|하)\s*(?:주|보|시|세|십|줄|달)|붙여\s*넣(?:(?:으|어)?\s*(?:세|시|십|주)|어(?=\s*[.!]|\s*$)|기\s*바)|직접\s*(?:실행|입력)|돌려\s*(?:보|봐)|실행하면\s*됩"
    r"|\b(?:please\s+run|you\s+(?:can|could|need\s+to|must|should)\s+run|run\s+(?:this|the\s+following|it)\s+(?:yourself|command))\b"
    r"|\b(?:run|execute)\s+(?:this|that|these|the\s+following)\b|^[ \t]*run:[ \t]*$|\b(?:run|execute|paste|type)\s+`",
    re.I | re.M,
)
VERB = re.compile(r"실행|입력|붙여\s*넣|돌려|돌리|타이핑|쳐")
ASKING = re.compile(
    r"주세|주시|주십|줘|드립|드려|부탁|바랍|세요|셔요|십시|시기|하시|하셔|셔야|보시|해\s*주|면\s*됩|야\s*합니|시겠|나요|까요|권장|권합|추천|볼\s*것|할\s*것|하는\s*것을|[?？]"
    r"|\b(?:please|you|your)\b",
    re.I,
)
LABEL = re.compile(r"(?:실행|입력|붙여\s*넣기)\s*[:!]")
IMPERATIVE = re.compile(r"(?:어|아|려|라|줘|봐|해|요|시다|바람)[\s.!]*$")
CLOSED = re.compile(r"([가-힣])(습니|니)?다[\s.!:;,)]*$")
REFUSED = re.compile(r"denied|blocked|refused|not allowed|hook error|disabled|no such tool|requires approval|rejected|doesn't want to proceed|not permitted", re.I)
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


def closed(line):
    """True when the line ends as a statement of something done: a past tense or a copula."""
    end = CLOSED.search(line)
    if not end:
        return False
    last, polite = end.groups()
    if polite == "니":
        return last == "입"
    return last in "이없" or (ord(last) - 0xAC00) % 28 == 20


def sentence(reply, at, code):
    """The sentence of the reply holding position `at`: a stop counts only outside a code span and before a space or
    the end, so `a.py` or v0.20.1 splits nothing."""
    masked = code.sub(lambda span: "x" * len(span.group()), reply)
    stops = [stop.end() for stop in re.finditer(r"[.!?？](?=\s|$)|\n", masked)]
    start = max([end for end in stops if end <= at], default=0)
    end = min([end for end in stops if end > at], default=len(reply))
    return reply[start:end]


def reports(text, code):
    """Whether a sentence only reports: closed in a past tense or a copula, with no request or question word; 직접
    there says who ran it, since the closed ending already rules out a request."""
    prose = code.sub("", text)
    return closed(prose.strip(" \t-*>:;,()")) and not ASKING.search(prose)


def handoff(reply):
    """The first span of the reply that hands over a command, else None."""
    code = re.compile(CODE, re.S)
    found = BANG.search(reply)
    if found:
        return reply[found.start():].strip().splitlines()[0][:80]
    for m in ASK.finditer(reply):
        if reports(sentence(reply, m.start(), code), code):
            continue
        if code.search(reply[max(0, m.start() - 200):m.end() + 200]):
            return reply[max(0, m.start() - 20):m.end() + 40].strip().replace("\n", " ")
    for m in VERB.finditer(reply):
        text = sentence(reply, m.start(), code)
        if not code.search(text) or reports(text, code):
            continue
        prose = code.sub("", text).strip(" \t-*>:;,()")
        if ASKING.search(prose) or IMPERATIVE.search(prose) or LABEL.search(text):
            return text.strip().replace("\n", " ")[:120]
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
