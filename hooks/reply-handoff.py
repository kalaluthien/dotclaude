#!/usr/bin/env python3
"""Stop hook: block a final reply that hands the owner a command to run (a `! <command>` line, or "run `x`" beside a
code span) when no tool call of the turn was refused, since a tool the session holds can run it. The block repeats once
at most: a second stop (`stop_hook_active`), a refusal earlier in the turn, or any error passes. A reply whose `돌려 보`
match only reports a run, done or not done, passes: that match's own sentence ends in a past tense or a copula and
holds no request or question word, since another sentence that hands a command over has its own match."""
import json
import re
import sys

CODE = r"```.*?```|`[^`\n]+`"
BANG = re.compile(r"^[ \t]*(?:`+[ \t]*)?!\s+[\w./~$-]", re.M)
ASK = re.compile(
    r"(?:실행|입력|붙여\s*넣|돌려)\s*(?:해|하)\s*(?:주|보|시|세|십|줄|달)|붙여\s*넣(?:으|어)?\s*(?:세|시|십|주)|직접\s*(?:실행|입력)|돌려\s*(?:보|봐)|실행하면\s*됩"
    r"|\b(?:please\s+run|you\s+(?:can|could|need\s+to|must|should)\s+run|run\s+(?:this|the\s+following|it)\s+(?:yourself|command))\b"
    r"|\b(?:run|execute)\s+(?:this|that|these|the\s+following)\b|^[ \t]*run:[ \t]*$|\b(?:run|execute|paste|type)\s+`",
    re.I | re.M,
)
REPORT = re.compile(r"돌려\s*보(?:니|고|았(?:습|더니|는데|고|던)|지\s*(?:는|도)?\s*(?:못|않))")
REQUEST = re.compile(
    r"주세|주시|주십|주셔|주실|줄래|줄\s*수|달라|드립|드려|부탁|바랍|바라|원합|원하|알려|세요|셔요|십시|시겠|실래|셔야|셔도|해야|어야|아야"
    r"|바란|권하|권합|권한|하실|하셔|하라|해라|할\s*일|할\s*것|다음|이제|단계|좋|추천|권장|낫|나을|수\s*있|남아|기대|몫|맡|요청|요구|원한|두면|일(?:입|이)|라고|명령|사용자|소유자|터미널|owner|user"
    r"|면(?![가-힣])|게\s*좋|당신|직접|남았|남은|남는|하자|보자|합시|봅시|차례|필요|나요|까요|가요|던가|습니까|니까|겠어|래요|[?？]"
    r"|\b(?:please|try|you|your|should|need)\b",
    re.I,
)
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
    prose = re.sub(r"직접", "", code.sub("", text))
    return closed(prose.strip(" \t-*>:;,()")) and not REQUEST.search(prose)


def handoff(reply):
    """The first span of the reply that hands over a command, else None."""
    code = re.compile(CODE, re.S)
    found = BANG.search(reply)
    if found:
        return reply[found.start():].strip().splitlines()[0][:80]
    for m in ASK.finditer(reply):
        if REPORT.match(reply, m.start()) and reports(sentence(reply, m.start(), code), code):
            continue
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
