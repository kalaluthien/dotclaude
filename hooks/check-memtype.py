#!/usr/bin/env python3
"""Check that a memory file's declared memtype matches the name it carries.

A pool file's `metadata.type` is written once, by whoever created the file, and
nothing re-reads it afterwards; four workspace-pool files had drifted to the
harness default before anyone counted. This hook is that second reader.

The mapping is not this file's. It is declared once, in the "Filing" section of
~/.claude/CLAUDE.md, as the memtype table — the subcategory prefix a file's name
opens with, paired with the `type` its row names. This hook parses that table
out of the document and compiles what it says; a copy kept here would drift
exactly the way the files did. Where a pool lives, which file is its index, and
which frontmatter key carries the declaration all come from the same document's
fenced `json contract=pool` block.

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
SUPPORTED_MAJOR = 1

BLOCK = re.compile(
    r"^```json[ \t]+contract=pool[ \t]*\n(.*?)\n```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)
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
    `backlog` names exactly one file. The angle bracket is what separates them.
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


def contract(text, path):
    """The pool shape: where a pool lives, its index file, the frontmatter key."""
    found = BLOCK.search(text)
    if not found:
        raise ContractError(
            "%s: no ```json contract=pool block — the pool shape is declared there"
            % path
        )
    try:
        data = json.loads(found.group(1))
    except ValueError as exc:
        raise ContractError("%s: the pool contract block is not JSON: %s" % (path, exc))

    version = data.get("version")
    if version != SUPPORTED_MAJOR:
        raise ContractError(
            "%s: pool contract version %r; this hook reads major %d"
            % (path, version, SUPPORTED_MAJOR)
        )
    pool = data.get("pool") or {}
    pattern = pool.get("pattern") or ""
    key = (data.get("frontmatter") or {}).get("type")
    if len(pattern.split("/")) < 2 or not pool.get("index_file"):
        raise ContractError("%s: pool.pattern and pool.index_file are required" % path)
    if not key:
        raise ContractError("%s: frontmatter.type is required" % path)
    return {
        # A pool's own directory is the pattern's last directory segment:
        # `projects/*/memory/*.md` puts its files in a `memory` directory.
        "pool_dir": pattern.split("/")[-2],
        "suffix": os.path.splitext(pattern.split("/")[-1])[1],
        "index_file": pool["index_file"],
        "type_key": key,
    }


def rule(path=CONTRACT_DOCUMENT):
    text = document(path)
    compiled = contract(text, path)
    compiled["memtypes"] = memtypes(text, path)
    return compiled


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


def violation(path, compiled):
    """The one reason this file fails, or None."""
    name = os.path.splitext(os.path.basename(path))[0]
    want = expected(name, compiled["memtypes"])
    if want is None:
        listed = sorted(
            set(
                "%s*" % n if is_prefix else n
                for (n, is_prefix) in compiled["memtypes"]
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
            "'%s' the type '%s'." % (compiled["type_key"], name, want)
        )
    got = declared(block, compiled["type_key"])
    if got is None:
        return (
            "the frontmatter declares no %s; the table gives '%s' the type '%s'."
            % (compiled["type_key"], name, want)
        )
    if got != want:
        return (
            "%s is '%s'; the table gives '%s' the type '%s'."
            % (compiled["type_key"], got, name, want)
        )
    return None


def is_pool_file(path, compiled):
    base = os.path.basename(path)
    return (
        base.endswith(compiled["suffix"])
        and base != compiled["index_file"]
        and os.path.basename(os.path.dirname(path)) == compiled["pool_dir"]
    )


def report(path, reason):
    return "%s: %s\n  (the memtype table is declared in %s, section Filing)" % (
        path,
        reason,
        CONTRACT_DOCUMENT,
    )


def main():
    try:
        compiled = rule()
    except ContractError as exc:
        print("check-memtype: %s" % exc, file=sys.stderr)
        # A write this hook could not check is refused, not waved through.
        return 1 if len(sys.argv) > 1 else 2

    if len(sys.argv) > 1:
        failed = False
        for path in sys.argv[1:]:
            if not is_pool_file(path, compiled):
                print("%s: skipped, not a pool file the table covers" % path)
                continue
            reason = violation(path, compiled)
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
    if not path or not is_pool_file(path, compiled) or not os.path.exists(path):
        return 0
    reason = violation(path, compiled)
    if not reason:
        return 0
    print(report(path, reason), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
