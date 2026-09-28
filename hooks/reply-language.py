#!/usr/bin/env python3
"""Stop hook: block a reply with no Hangul to a user message written in Korean, asking for a rewrite in Korean, since
the per-prompt instruction alone was ignored. Any error, or a second stop (`stop_hook_active`), passes."""
import json
import re
import sys

HANGUL = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
# a user entry whose text only carries these blocks was written by the harness, not typed by the user
INJECTED = re.compile(
    r"<(system-reminder|command-name|command-message|command-args|task-notification|local-command-[\w-]+)>.*?</\1>",
    re.S,
)
REASON = ("Your reply has no Korean, but the user's latest message is in Korean. "
          "Rewrite the whole reply in Korean, in the formal polite register (-습니다/-ㅂ니다 endings).")


def texts(content, kind):
    """The text blocks of a message's content, a string or a list of blocks."""
    if isinstance(content, str):
        return [content]
    return [b.get("text", "") for b in content or [] if isinstance(b, dict) and b.get("type") == kind]


def user_message(entry):
    """The text the user typed in a transcript entry, or None for a tool result, a meta or harness-injected entry."""
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isCompactSummary"):
        return None
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        return None
    text = INJECTED.sub("", "\n".join(texts(content, "text"))).strip()
    if not text or text.startswith("[Request interrupted"):
        return None
    return text


def last_exchange(lines):
    """The latest user message and the final run of assistant text after it, read from transcript lines."""
    message, reply = None, []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if not isinstance(entry, dict):
            continue
        typed = user_message(entry)
        if typed is not None:
            message, reply = typed, []
        elif entry.get("type") == "assistant":
            content = (entry.get("message") or {}).get("content")
            said = [t for t in texts(content, "text") if t.strip()]
            if said:
                reply += said
            elif isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_use" for b in content):
                reply = []  # text before a tool call is not the final answer
    return message, "\n".join(reply)


def verdict(message, reply):
    """The block decision for a Korean message answered with no Hangul, else None."""
    if message and reply and HANGUL.search(message) and not HANGUL.search(reply):
        return {"decision": "block", "reason": REASON}
    return None


def main():
    try:
        event = json.load(sys.stdin)
        if event.get("stop_hook_active"):
            return
        with open(event["transcript_path"], encoding="utf-8") as transcript:
            message, reply = last_exchange(transcript)
        reply = event.get("last_assistant_message") or reply
        decision = verdict(message, reply)
    except Exception:
        return
    if decision:
        print(json.dumps(decision, ensure_ascii=False))


if __name__ == "__main__":
    main()
