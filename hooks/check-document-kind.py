#!/usr/bin/env python3
"""Refuse a page under `docs/` whose `<body class>` carries no kind word, or two.

`spec/document-kinds.md` is the contract, and its § Kinds table is the one
declaration of the kind words: they are read from that table's first column at
run time, so the list lives there once. Every other rule of that spec is a
reviewer's, not this script's.

Two entry points, one judgement, and one exit code for it: 0 allows, 2 refuses,
anything else is this script's own failure and refuses nothing.

  * with arguments, a file checker -- one line per path;
  * with none, a `PostToolUse` hook reading the payload on stdin.

`PostToolUse` fires after the write has landed, so a 2 does not undo it; it
puts the reason in front of the model that wrote it.

Every path that is not an `.html` under this checkout's `docs/` is skipped,
and the skip says so: the hook is registered machine-wide, and a silent skip
and a pass look identical from the outside.
"""

import json
import os
import re
import sys

# The checkout this script ships in, so a copy under test judges its own tree
# and reads its own spec. `check-decision-page.py` resolves `docs/` the same way.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SPEC = os.path.join(ROOT, "spec", "document-kinds.md")

ATTRS = r"""((?:[^>"']|"[^"]*"|'[^']*')*)"""
BODY = re.compile(r"<body\b" + ATTRS + r">", re.IGNORECASE)
CLASS = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
ROW = re.compile(r"^\|\s*`([a-z]+)`\s*\|")


def kinds():
    """The kind words, from the first column of the spec's § Kinds table.

    None when the spec cannot be read or holds no such table: a caller told
    "no kinds" would refuse every page, which is a missing contract, not a
    finding.
    """
    try:
        with open(SPEC, "r", encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    found, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == "## Kinds"
            continue
        match = ROW.match(line) if inside else None
        if match:
            found.append(match.group(1))
    return found or None


def under(path, directory):
    """Whether `path` sits inside `directory`, both resolved."""
    path = os.path.abspath(path)
    directory = os.path.abspath(directory)
    return path == directory or path.startswith(directory + os.sep)


def verdict(path):
    """(code, message): 0 allows, 2 refuses, 1 could not judge.

    The spec is read only for a page in scope, so a missing spec costs the
    pages it governs and not every write on the machine.
    """
    if not (under(path, DOCS) and path.endswith(".html")):
        return 0, "%s: skipped, not an .html under %s" % (path, DOCS)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = COMMENT.sub("", handle.read())
    except FileNotFoundError:
        return 0, "%s: skipped, no such file" % path
    except (OSError, UnicodeDecodeError):
        return 0, "%s: skipped, not readable as UTF-8 text" % path
    words = kinds()
    if words is None:
        return 1, ("could not read the kind words from %s; %s not checked"
                   % (SPEC, path))

    body = BODY.search(text)
    attrs = CLASS.search(body.group(1)) if body else None
    classes = attrs.group(1).split() if attrs else []
    held = [c for c in classes if c in words]
    if len(held) == 1:
        return 0, "%s: ok, kind %s" % (path, held[0])
    if held:
        return 2, (
            "%s declares more than one kind, %s. A page is one kind, the reader's "
            "primary job; a part of another kind is a figure or a control "
            "(%s § Kinds)." % (path, " and ".join(held), SPEC))
    return 2, (
        "%s carries no kind word on its <body class> (read: %s). Add one of "
        "%s, tested in that order, first match wins (%s § Kinds)."
        % (path, "no <body>" if not body else repr(" ".join(classes)),
           ", ".join(words), SPEC))


def main():
    if len(sys.argv) > 1:
        worst = 0
        for path in sys.argv[1:]:
            code, message = verdict(path)
            if code == 0:
                print(message)
            else:
                print("check-document-kind: %s" % message, file=sys.stderr)
            worst = max(worst, code)
        return worst

    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path:
        return 0
    code, message = verdict(path)
    if code:
        print("check-document-kind: %s" % message, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
