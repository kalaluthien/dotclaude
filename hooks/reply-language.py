#!/usr/bin/env python3
"""Stop hook: block a reply to a user message written in Korean when it has no Hangul or uses a banned word
(ledger, 장부), naming each offending sentence and its fix, since the per-prompt instruction alone was ignored.
Code, quotes and a message not in Korean pass. Any error, or a second stop (`stop_hook_active`), passes."""
import json
import re
import sys

HANGUL = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
# a user entry whose text only carries these blocks was written by the harness, not typed by the user
INJECTED = re.compile(
    r"<(system-reminder|command-name|command-message|command-args|task-notification|local-command-[\w-]+)>.*?</\1>",
    re.S,
)
# text the rules do not govern: code, a blockquote, quoted words
SKIP = re.compile(r"```.*?```|`[^`\n]*`|^>[^\n]*|\"[^\"\n]*\"|“[^”\n]*”|「[^」\n]*」", re.S | re.M)
BANNED = re.compile(r"\bledger|(?<!대)장부(?!터)", re.I)
SENTENCE = re.compile(r"[^\n]+?(?:[.!?](?=\s|$)|$)", re.M)
SHOWN = 3
HEADER = "Your reply to a Korean message breaks the Korean reply rules:"
FOOTER = "Rewrite the whole reply in Korean, in the formal polite register (-습니다/-ㅂ니다 endings), with no banned word."


def mask(text):
    """The text with each skipped span blanked to spaces, so offsets still point into the original."""
    return SKIP.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), text)


def sentence(text, start, end):
    """The sentence of text around [start, end), cut to a window of about 100 characters."""
    for m in SENTENCE.finditer(text):
        if m.start() <= start < m.end():
            found, offset = m.group().strip(), start - m.start() - (len(m.group()) - len(m.group().lstrip()))
            break
    else:
        found, offset = text[start:end], 0
    if len(found) > 100:
        left = max(0, offset - 50)
        found = ("…" if left else "") + found[left:offset + (end - start) + 30] + "…"
    return found


def problems(reply):
    """One line per break of the reply rules in a reply to a Korean message, each naming the sentence and the fix."""
    found = []
    if not HANGUL.search(reply):
        found.append(f"No Korean in the reply, which begins “{reply.strip()[:60]}”: write it in Korean.")
    seen = mask(reply)
    for m in list(BANNED.finditer(seen))[:SHOWN]:
        found.append(f"Banned word “{m.group()}” in “{sentence(reply, m.start(), m.end())}”: "
                     "name the record by what it holds, such as 기록 or 목록.")
    return found


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
    """The block decision for a reply that breaks the reply rules in answering a Korean message, else None."""
    if message and reply and HANGUL.search(message):
        found = problems(reply)
        if found:
            return {"decision": "block", "reason": "\n".join([HEADER, *(f"- {line}" for line in found), FOOTER])}
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
