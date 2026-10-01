#!/usr/bin/env python3
"""PreToolUse hook on Bash: deny a plain `>` onto an existing regular file, since zsh's `noclobber` makes it fail with
"file exists" and leave the old file in place; `>|`, `>>`, a descriptor copy such as `2>&1`, and a new file run."""
import json
import os
import re
import sys

SUBST = "\0subst\0"  # stands for a `$(...)` or backtick substitution; NUL never survives in a real command
METACHARS = set(" \t\n;&|()<>")
ASSIGN = re.compile(r"(?:^|[;&|(\n{]|\b(?:export|local|typeset)\s)\s*([A-Za-z_]\w*)=")
VAR = re.compile(r"\$(?:([A-Za-z_]\w*)|\{([A-Za-z_]\w*)\})")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
kill_guard = __import__("kill-guard")  # the heredoc and substitution readers are shared, not copied


def deny(target):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": f"redirect-guard: `>` onto the existing file `{target}` fails under zsh's noclobber "
                                    f"and leaves it unchanged; write `>|` to overwrite it, or `>>` to append",
    }}))
    sys.exit(0)


def word(text, i):
    """The shell word starting at i with its quotes removed, and the index after it."""
    out, quote = [], None
    while i < len(text):
        c = text[i]
        if quote:
            if c == quote:
                quote = None
            elif c == "\\" and quote == '"' and i + 1 < len(text):
                i += 1
                out.append(text[i])
            else:
                out.append(c)
        elif c in "'\"":
            quote = c
        elif c == "\\" and i + 1 < len(text):
            i += 1
            out.append(text[i])
        elif c in METACHARS:
            break
        else:
            out.append(c)
        i += 1
    return "".join(out), i


def targets(text):
    """Yield the target word and its index of each plain `>` or `&>` redirect outside quotes and comments."""
    i, quote = 0, None
    while i < len(text):
        c = text[i]
        if quote:
            if c == quote:
                quote = None
            elif c == "\\" and quote == '"':
                i += 1
        elif c in "'\"":
            quote = c
        elif c == "\\":
            i += 1
        elif c == "#" and (i == 0 or text[i - 1] in METACHARS):
            while i < len(text) and text[i] != "\n":
                i += 1
        elif c == ">" and not (i and text[i - 1] == "<"):  # `<>` opens read-write without truncating
            nxt = text[i + 1:i + 2]
            if nxt in (">", "|", "!", "("):  # append, forced clobber, process substitution
                i += 2
                continue
            j = i + 1
            if nxt == "&":
                j += 1
                if text[j:j + 1].isdigit() or text[j:j + 1] == "-":  # `>&2` copies a descriptor
                    i = j + 1
                    continue
            while j < len(text) and text[j] in " \t":
                j += 1
            target, i = word(text, j)
            if target:
                yield target, j
            continue
        i += 1


def expand(target, at, text):
    """target with each `$NAME` or `${NAME}` replaced by its last assignment before index at in text, else the
    environment's; None when a name stays unset or its value is not plain text."""
    values = {}
    for m in ASSIGN.finditer(text, 0, at):
        value, _ = word(text, m.end())
        values[m.group(1)] = value
    bad = False

    def sub(m):
        nonlocal bad
        name = m.group(1) or m.group(2)
        value = values.get(name, os.environ.get(name))
        if value is None or "$" in value or SUBST in value:
            bad = True
            return ""
        return value
    out = VAR.sub(sub, target)
    return None if bad or "$" in out else out


def clobbers(command, cwd):
    """The first redirect target in command that is an existing regular file, or None."""
    text, inner = kill_guard.substitutions(kill_guard.unheredoc(command))
    for body in inner:
        found = clobbers(body, cwd)
        if found:
            return found
    for target, at in targets(text):
        if SUBST in target:
            continue  # its value is unknown until the shell expands it
        shown = target
        if "$" in target:
            target = expand(target, at, text)
            if target is None:
                continue  # unset, or not plain text: the shell decides
        path = os.path.join(cwd, os.path.expanduser(target))
        if os.path.isfile(path):  # noclobber spares devices such as /dev/null
            return shown
    return None


def main():
    try:
        data = json.load(sys.stdin)
        command, cwd = data["tool_input"]["command"], data.get("cwd") or os.getcwd()
    except (ValueError, KeyError, TypeError, AttributeError):
        sys.exit(0)  # no Bash command to judge
    if not isinstance(command, str) or ">" not in command:
        sys.exit(0)
    try:
        target = clobbers(command, cwd)
    except Exception:  # a misread lets the command run: zsh itself still refuses the overwrite
        sys.exit(0)
    if target:
        deny(target)


if __name__ == "__main__":
    main()
