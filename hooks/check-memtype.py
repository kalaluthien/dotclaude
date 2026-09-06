#!/usr/bin/env python3
"""Check a memory pool file against what the "Filing" section says about it.

A file is refused when its name matches no row of the memtype table, when its
pool's `MEMORY.md` carries no line linking to it, or when a `metadata.type` it
does declare contradicts its row.

The index line is the load-bearing check. The harness injects a pool's
`MEMORY.md` and never a memory file, so an unindexed memory has no way of being
read at all, and one written without its line is indistinguishable from one
nobody needed. `metadata.type` is the retiring check: nothing re-read it after
it was written and four files in one pool had drifted to the harness default
before anyone counted, so a declaration is still compared against its row — but
the subcategory is being renamed after its reader (`topic-`, `pitfall-`,
`feedback-`), and a file declaring no type is the target shape rather than a
drift.

The name mapping is not this file's. It is declared once, in the "Filing"
section of ~/.claude/CLAUDE.md, as the memtype table — the subcategory prefix a file's name
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

What this hook does not cover: settings.json matches it on `Write` and `Edit`
only, so a memory written by `sed` or a heredoc is never checked. And a new
memory's first write is always refused, its index line not existing yet -- one
round-trip per new file, which is the nudge, not a defect.

Two entry points:
  - as a Claude Code PostToolUse hook: reads the tool payload on stdin, checks
    the touched file, exits 2 with the reason on stderr.
  - as a CLI: `check-memtype.py FILE...`, exits 1 on any violation.

A declaration that cannot be read is a refusal, never a pass: this hook has no
table of its own to fall back to. So is an index, in one of three wordings a
reader acts on differently: it could not be read at all, an unclosed fence ate
the entry, or it was read and simply does not carry one.
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
# The index line as the document prescribes it: a list item whose first element
# is a Markdown link to the file. Anchored to the bullet, because a link further
# along the line is a neighbour's prose naming the file -- what a split leaves
# behind -- and prose is not a route to anything. A `./` prefix and an `#anchor`
# are tolerated; the title and the trailing hook are a person's and unread.
LINK = (
    r"(?m)^[ \t]*(?:[-*+]|\d+[.)])[ \t]+"
    r"\[[^\]]*\]\([ \t]*\.?/?%s(?:#[^)\s]*)?[ \t]*\)"
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
    except (OSError, UnicodeDecodeError) as exc:
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
    """The file's YAML frontmatter block, or None when it carries none.

    A file that cannot be decoded carries no readable block; the index check
    has already run by here, so the caller reports the absence rather than
    dying on it, which on PostToolUse would exit 1 and enforce nothing.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except UnicodeDecodeError:
        return None
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


def unfenced(text):
    """The text with its fenced blocks dropped, and the tail an open fence ate.

    A fence in an index holds an example of an index line -- the shape a reader
    is being shown how to write -- and an example is not an entry. An
    unterminated fence swallows every line below it, which is fail-closed and
    right, but it is a different defect from a missing entry and is fixed by a
    different edit, so the caller gets the swallowed tail itself and can say
    which of the two it observed. A closed fence is not in that tail: its
    contents are examples on purpose, and blaming them on the last unclosed
    fence somewhere else would be the same misdiagnosis one step along.

    This is a fence model, not a Markdown parser, and the differences it admits
    are written down rather than left silent. It pairs any fence line with any
    other, so `~~~` opened and ``` closed reads as one block; it does not know
    the 4-space indented code block, so an entry indented that far still counts
    as one; and neither it nor `LINK` knows CommonMark's nine-digit cap on an
    ordered marker. Each is fail-open on a shape no pool index contains -- none
    of the six holds a fence at all -- and closing them means a second Markdown
    parser inside a hook.
    """
    kept, swallowed, in_fence = [], [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            if in_fence:
                # Only the LAST opener can be the unmatched one.
                swallowed = []
            continue
        (swallowed if in_fence else kept).append(line)
    return "\n".join(kept), "\n".join(swallowed) if in_fence else ''


def indexed(path):
    """Why the pool's index does not name this file, or None when it does.

    A pool with no readable index, an index whose unclosed fence swallowed the
    entry, and an index that was read and simply omits the file are three
    different failures fixed by three different edits, so each reason says
    which of them was observed.

    An HTML comment is not read, so a commented-out entry still counts as one.
    Accepted, and written down rather than left silent: nobody comments an
    entry out, and reading them would put a second Markdown parser in a hook.
    """
    index = os.path.join(os.path.dirname(path), INDEX_FILE)
    base = os.path.basename(path)
    try:
        with open(index, encoding="utf-8") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        return "the pool has no readable %s (%s), so nothing can index '%s'." % (
            INDEX_FILE,
            exc,
            base,
        )
    body, swallowed = unfenced(text)
    if not re.search(LINK % re.escape(base), body):
        # The fence is the diagnosis only when the unclosed fence ate THIS
        # entry. Gated on "a fence is open" it rewrote the reason for every
        # miss in the file, so a wrongly shaped entry was answered "close the
        # fence"; gated on the raw text it did the same for an entry sitting in
        # a fence that was closed on purpose. Both would name a condition no
        # branch had read.
        if swallowed and re.search(LINK % re.escape(base), swallowed):
            return (
                "%s has a fence that is never closed, so every line below it "
                "was read as an example and not as an entry, '%s' among them. "
                "Close the fence; the entry may well be there."
                % (INDEX_FILE, base)
            )
        return (
            "%s was read and carries no line linking to '%s'. An entry is a "
            "list item whose FIRST element is the link -- "
            "`- [<name>](%s) - <what a reader would come for>` -- so a link "
            "wrapped in bold, in a table cell, or inside another entry's prose "
            "is not one, and a second line for the same file is not the fix. "
            "The harness loads the index and never a memory, so an unindexed "
            "file has no reader." % (INDEX_FILE, base, base)
        )
    return None


def violation(path, table):
    """The one reason this file fails, or None.

    Ordered by what outlives the rename: the name and the index line are the
    whole of the target scheme's check, and the type is read last because it is
    the one being retired.
    """
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
    reason = indexed(path)
    if reason:
        return reason
    block = frontmatter(path)
    got = declared(block, TYPE_KEY) if block is not None else None
    # A file that declares no type is the target scheme's shape, where the
    # frontmatter is `name` and `description` alone; only a declaration that
    # contradicts its row is the drift this check was written for.
    if got is not None and got != want:
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
    return "%s: %s\n  (what a pool file is checked against is declared in %s, section Filing)" % (
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
                print("%s: skipped, not a pool file" % path)
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
