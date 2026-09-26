#!/usr/bin/env python3
"""PreToolUse hook on Bash: deny a process kill that matches by a broad name, so a stray `pkill -f cat` cannot SIGTERM
every app; a kill by numeric PID or by exact name (`pkill -x`, plain `killall <name>`) runs."""
import json
import os
import re
import shlex
import sys

KILLERS = {"kill", "pkill", "killall"}
SUBST = "\0subst\0"  # stands for a `$(...)` or backtick substitution; NUL never survives in a real command
SEPARATORS = set(";&|()\n")
DESCRIPTOR = re.compile(r"(^|[\s;&|()])(?:\d+|\{\w+\})(?=[<>])")  # the `2` of `2>&1`, so it is not read as an argument
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
# wrappers that run the rest of their words as a command, with the options of each that take a value
WRAPPERS = {
    "sudo": set("ugpChDrtUT"), "doas": set("uC"), "env": set("uSCP"), "nice": set("n"), "nohup": set(),
    "time": set(), "exec": set("a"), "command": set(), "xargs": set("IJLnPRSsEda"), "timeout": set("sk"),
}
ALTERNATIVE = "look up the PID with `pgrep -fl <pattern>` in its own call, read the list, then `kill <pid>` with the number written out"


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": f"kill-guard: {reason}; {ALTERNATIVE}",
    }}))
    sys.exit(0)


def unheredoc(text):
    """Drop each heredoc's body, which is text fed to a command, not a command."""
    lines, kept, ends = text.split("\n"), [], []
    for line in lines:
        if ends:
            if line.strip() == ends[0]:
                ends.pop(0)
            continue
        kept.append(line)
        ends = [m[1] for m in HEREDOC.findall(line.replace("<<<", ""))]
    return "\n".join(kept)


def substitutions(text):
    """Return text with each `$(...)` and backtick substitution replaced by SUBST, and the inner texts."""
    out, inner, i, quote = [], [], 0, None
    while i < len(text):
        c = text[i]
        if quote == "'":
            if c == "'":
                quote = None
        elif c == "\\":
            out.append(text[i:i + 2])
            i += 2
            continue
        elif c == "'" and not quote:
            quote = "'"
        elif c == '"':
            quote = None if quote else '"'
        elif c == "`" or text.startswith("$(", i):
            end = closing(text, i)
            body = text[i + 1:end] if c == "`" else text[i + 2:end]
            inner.append(body)
            out.append(SUBST)
            i = end + 1
            continue
        out.append(c)
        i += 1
    return "".join(out), inner


def closing(text, start):
    """Index of the character closing the substitution at start; past the end when it never closes."""
    if text[start] == "`":
        i = start + 1
        while i < len(text) and text[i] != "`":
            i += 2 if text[i] == "\\" else 1
        return i
    depth, i, quote = 0, start + 1, None
    while i < len(text):
        c = text[i]
        if quote == "'":
            quote = None if c == "'" else quote
        elif c == "\\":
            i += 1
        elif c in "'\"" and (not quote or quote == c):
            quote = None if quote else c
        elif not quote and c == "(":
            depth += 1
        elif not quote and c == ")":
            depth -= 1
            if depth == 0:
                return i
        elif c == "`" or text.startswith("$(", i):
            i = closing(text, i)
        i += 1
    return i


def segments(text):
    """Split text into the word lists of its commands, as a shell would split it."""
    text = DESCRIPTOR.sub(r"\1", text.replace("\\\n", ""))
    lexer = shlex.shlex(text, posix=True, punctuation_chars=";&|()<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    segment, redirect = [], False
    for word in list(lexer) + [";"]:
        if word and set(word) <= SEPARATORS:
            if segment:
                yield segment
            segment, redirect = [], False
        elif word and set(word) <= set("<>&"):
            redirect = True
        elif redirect:
            redirect = False  # a redirect's target is no argument
        else:
            segment.append(word)


def unwrap(words, piped=False):
    """The command words after leading assignments and wrappers such as `sudo` or `xargs`, and whether an `xargs` feeds it."""
    while words:
        while words and ASSIGNMENT.match(words[0]):
            words = words[1:]
        if not words or os.path.basename(words[0]) not in WRAPPERS:
            return words, piped
        name, rest = os.path.basename(words[0]), words[1:]
        piped = piped or name == "xargs"
        while rest and rest[0].startswith("-") and rest[0] != "-":
            flag = rest.pop(0)
            if flag == "--":
                break
            if not flag.startswith("--") and flag[-1] in WRAPPERS[name] and len(flag) == 2:
                rest = rest[1:]  # the option's value
        if name == "env":
            while rest and ASSIGNMENT.match(rest[0]):
                rest = rest[1:]
        if name == "timeout" and rest:
            rest = rest[1:]  # the duration
        if name == "command" and words[1:2] and words[1] in ("-v", "-V"):
            return [], piped  # a lookup only
        words = rest
    return words, piped


def broad(words, piped):
    """Why the words kill by a broad match, or None."""
    words, piped = unwrap(words, piped)
    if not words:
        return None
    name = os.path.basename(words[0])
    if name in SHELLS:
        for i, word in enumerate(words[1:-1], 1):
            if re.fullmatch(r"-[a-z]*c[a-z]*", word):
                return check(words[i + 1])
        return None
    if name not in KILLERS:
        return None
    args = words[1:]
    if any(SUBST in arg for arg in args):
        return f"`{name}` with an argument built by a command substitution, which changes meaning when it comes back empty"
    if piped:
        return f"`xargs {name}` takes its targets from another command's output, which changes meaning when it comes back empty"
    if name == "pkill":
        if not any(arg == "--exact" or re.fullmatch(r"-[a-zA-Z]*x[a-zA-Z]*", arg) for arg in args):
            return "`pkill` without `-x` matches every process whose name contains the pattern"
    elif name == "killall":
        if any(arg == "--regexp" or re.fullmatch(r"-[a-z]*[mr][a-z]*", arg) for arg in args):
            return "`killall -m` matches process names by a regular expression"
    elif "-1" in targets(args):
        return "`kill -1` signals every process you own"
    return None


def targets(args):
    """The PIDs `kill` would signal: its words after the signal option."""
    if args and args[0] in ("-s", "-n"):
        args = args[2:]
    elif args and args[0].startswith("-") and args[0] != "--":
        args = args[1:]  # `-9`, `-KILL`, `-l`
    if args and args[0] == "--":
        args = args[1:]
    return args


def check(command):
    """Why command kills by a broad match, or None."""
    command = unheredoc(command)
    text, inner = substitutions(command)
    for body in inner:
        reason = check(body)
        if reason:
            return reason
    try:
        lists = list(segments(text))
    except ValueError:  # an unclosed quote: read each line that lexes
        return next(filter(None, (check(line) for line in command.split("\n") if line != command)), None)
    return next(filter(None, (broad(words, False) for words in lists)), None)


def main():
    try:
        command = json.load(sys.stdin)["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        sys.exit(0)  # no Bash command to judge
    if not isinstance(command, str) or "kill" not in command:
        sys.exit(0)
    try:
        reason = check(command)
    except Exception as err:  # a crash would let the command run
        deny(f"could not read a command naming a kill ({type(err).__name__})")
    if reason:
        deny(reason)


if __name__ == "__main__":
    main()
