#!/usr/bin/env python3
"""Check that a memory file's declared memtype matches the name it carries.

A pool file's `metadata.type` is written once, by whoever created the file, and
nothing re-reads it afterwards; four files in one pool had drifted to the
harness default before anyone counted. This hook is that second reader.

The mapping is not this file's. It is declared once, in the "Filing" section of
~/.claude/CLAUDE.md, as the memtype table — the subcategory prefix a file's name
opens with, paired with the `type` its row names. This hook parses that table
out of the document and compiles what it says; a copy kept here would drift
exactly the way the files did.

Where a pool lives, what its files are named, which file is its index, and
which frontmatter key carries the declaration are the four constants below. They were a fenced
`json contract=pool` block in the same document while a second program parsed
it; that program is gone, so the values live with their one remaining reader.
A constant no second reader consumes is a constant, not a contract.

A name matching no row of the table is a refusal too, not a pass: the Filing
prose says a new memtype is invented by adding it to the table in the same
change, so an unlisted prefix is a table that was never updated.

Two entry points:
  - as a Claude Code PostToolUse hook: reads the tool payload on stdin, checks
    the touched file, exits 2 with the reason on stderr.
  - as a CLI: `check-memtype.py FILE...`, exits 1 on any violation.

A declaration that cannot be read is a refusal, never a pass: this hook has no
table of its own to fall back to.
"""

import json
import os
import re
import sys

CONTRACT_DOCUMENT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CLAUDE.md"
)
# The pool shape. A pool is `projects/*/memory/*.md`, so its files sit in a
# `memory` directory and end in `.md`; `MEMORY.md` is the index, not a memory.
POOL_DIR = "memory"
POOL_SUFFIX = ".md"
INDEX_FILE = "MEMORY.md"
TYPE_KEY = "metadata.type"

ROW = re.compile(r"^\|(.+)\|\s*$")
RULE_ROW = re.compile(r"^[\s:|-]+$")
FENCE = re.compile(r"^\s*(?:```|~~~)")
# The header names the two columns this hook needs; their order is the table's
# to choose, so it is read rather than assumed.
TYPE_COLUMN = "type"
PREFIX_COLUMN = "subcategory prefixes"


class ContractError(Exception):
    """The declaration could not be read, with the reason a reader can act on."""


def document(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        raise ContractError("%s: cannot be read: %s" % (path, exc))


def cells(line):
    return [cell.strip() for cell in ROW.match(line).group(1).split("|")]


def names(cell):
    """The names one table cell lists, as (name, is_prefix) pairs.

    `history-<topic>` names every file whose name opens with `history-`;
    `pitfalls` names exactly one file. The angle bracket is what separates
    them.
    """
    found = []
    for token in re.findall(r"`([^`]+)`", cell):
        placeholder = token.find("<")
        if placeholder >= 0:
            found.append((token[:placeholder], True))
        else:
            found.append((token, False))
    return found


def memtypes(text, path):
    """The memtype table, compiled to (name, is_prefix) -> type.

    The table is the one whose header row names both columns this hook reads;
    a document holding several tables therefore needs no positional guess.
    """
    lines = text.split("\n")
    in_fence = False
    mapping = {}
    header = None
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not ROW.match(line):
            header = None
            continue
        row = cells(line)
        if header is None:
            plain = [re.sub(r"[*`]", "", cell).strip().lower() for cell in row]
            if TYPE_COLUMN in plain and PREFIX_COLUMN in plain:
                header = (plain.index(TYPE_COLUMN), plain.index(PREFIX_COLUMN))
            continue
        if RULE_ROW.match(line.replace("|", "")):
            continue
        type_at, prefix_at = header
        if max(type_at, prefix_at) >= len(row):
            continue
        kind = re.sub(r"[*`]", "", row[type_at]).strip()
        for name, is_prefix in names(row[prefix_at]):
            # One name in two rows is a table that contradicts itself; taking
            # the row that happens to be last would answer with half of it.
            if mapping.get((name, is_prefix), kind) != kind:
                raise ContractError(
                    "%s: the memtype table gives '%s' both '%s' and '%s'"
                    % (path, name, mapping[(name, is_prefix)], kind)
                )
            mapping[(name, is_prefix)] = kind
    if not mapping:
        raise ContractError(
            "%s: no memtype table — a row names a `type` and its "
            "`subcategory prefixes`" % path
        )
    return mapping


def rule(path=CONTRACT_DOCUMENT):
    return memtypes(document(path), path)


def frontmatter(path):
    """The file's YAML frontmatter block, or None when it carries none."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for number, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:number]
    return None


def declared(block, dotted):
    """The scalar at a dotted key path in a frontmatter block, or None.

    Indentation is the nesting: a child of `metadata:` is any following line
    indented past it, up to the first line that dedents back.
    """
    lines, parent_indent, value = block, -1, None
    for key in dotted.split("."):
        pattern = re.compile(r"^\s*%s:\s*(.*?)\s*$" % re.escape(key))
        child_indent, rest = None, None
        for number, line in enumerate(lines):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            if indent <= parent_indent:
                break
            if child_indent is None:
                child_indent = indent
            if indent != child_indent:
                continue
            found = pattern.match(line)
            if found:
                rest = (lines[number + 1 :], indent, found.group(1))
                break
        if rest is None:
            return None
        lines, parent_indent, value = rest
    return value.strip("\"'") or None


def expected(name, mapping):
    """The type the table gives a file's name, or None when no row names it.

    An exact row wins over a prefix row, and the longest prefix wins among
    prefixes, so a table that later adds `setup-android-` still reads.
    """
    if (name, False) in mapping:
        return mapping[(name, False)]
    best = None
    for (candidate, is_prefix), kind in mapping.items():
        if is_prefix and name.startswith(candidate):
            if best is None or len(candidate) > len(best[0]):
                best = (candidate, kind)
    return best[1] if best else None


def violation(path, table):
    """The one reason this file fails, or None."""
    name = os.path.splitext(os.path.basename(path))[0]
    want = expected(name, table)
    if want is None:
        listed = sorted(
            set(
                "%s*" % n if is_prefix else n
                for (n, is_prefix) in table
            )
        )
        return (
            "'%s' matches no row of the memtype table. A new memtype is added to "
            "the table in the same change that first uses it; the table names %s."
            % (name, ", ".join("'%s'" % row for row in listed))
        )
    block = frontmatter(path)
    if block is None:
        return (
            "no '---' frontmatter block, so nothing declares %s; the table gives "
            "'%s' the type '%s'." % (TYPE_KEY, name, want)
        )
    got = declared(block, TYPE_KEY)
    if got is None:
        return (
            "the frontmatter declares no %s; the table gives '%s' the type '%s'."
            % (TYPE_KEY, name, want)
        )
    if got != want:
        return (
            "%s is '%s'; the table gives '%s' the type '%s'."
            % (TYPE_KEY, got, name, want)
        )
    return None


def is_pool_file(path):
    base = os.path.basename(path)
    return (
        base.endswith(POOL_SUFFIX)
        and base != INDEX_FILE
        and os.path.basename(os.path.dirname(path)) == POOL_DIR
    )


def report(path, reason):
    return "%s: %s\n  (the memtype table is declared in %s, section Filing)" % (
        path,
        reason,
        CONTRACT_DOCUMENT,
    )


def main():
    try:
        table = rule()
    except ContractError as exc:
        print("check-memtype: %s" % exc, file=sys.stderr)
        # A write this hook could not check is refused, not waved through.
        return 1 if len(sys.argv) > 1 else 2

    if len(sys.argv) > 1:
        failed = False
        for path in sys.argv[1:]:
            if not is_pool_file(path):
                print("%s: skipped, not a pool file the table covers" % path)
                continue
            reason = violation(path, table)
            if reason:
                failed = True
                print(report(path, reason), file=sys.stderr)
            else:
                print("%s: ok" % path)
        return 1 if failed else 0

    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path or not is_pool_file(path) or not os.path.exists(path):
        return 0
    reason = violation(path, table)
    if not reason:
        return 0
    print(report(path, reason), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
