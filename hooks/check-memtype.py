#!/usr/bin/env python3
"""Check a memory pool file against what the "Filing" section says about it.

A file is refused when its name opens with none of the memory prefixes, when
its pool's `MEMORY.md` carries no line linking to it, or when it still declares
`metadata.type`.

The index line is the load-bearing check. The harness injects a pool's
`MEMORY.md` and never a memory file, so an unindexed memory has no way of being
read at all, and one written without its line is indistinguishable from one
nobody needed.

The name is the second. A memory is named after its reader -- `topic-` for a
fact looked up, `pitfall-` for a trap read when stuck, `feedback-` for a rule
the owner gave -- because the type it used to be named after predicted nothing
about whether the file was ever read and the prefix did. `setup-`, `pitfalls`,
`backlog` and `history-` are the names that scheme retired; the refusal names
each one's successor, and `history-`'s is a decision page under `docs/` rather
than anything in the pool (`spec/decision-pages.md`).

`metadata.type` is the third and the smallest edit: nothing re-read it after it
was written, four files in one pool had drifted to the harness default before
anyone counted, and the prefix now carries what it claimed. `name` and
`description` are the whole frontmatter.

The prefix list is not this file's. It is declared once, in the "Filing"
section of ~/.claude/CLAUDE.md, as the bullets under "memory prefixes are:".
This hook parses them out of the document; a copy kept here would drift exactly
the way the files did, and a document that declares none refuses every write
rather than falling back on one.

Where a pool lives, what its files are named, which file is its index, and
which frontmatter key carries the retired declaration are the four constants
below. They were a fenced `json contract=pool` block in the same document while
a second program parsed it; that program is gone, so the values live with their
one remaining reader. A constant no second reader consumes is a constant, not a
contract.

What this hook does not cover: settings.json matches it on `Write` and `Edit`
only, so a memory written by `sed` or a heredoc is never checked. And a new
memory's first write is always refused, its index line not existing yet -- one
round-trip per new file, which is the nudge, not a defect.

Two entry points:
  - as a Claude Code PostToolUse hook: reads the tool payload on stdin, checks
    the touched file, exits 2 with the reason on stderr.
  - as a CLI: `check-memtype.py FILE...`, exits 1 on any violation.

A declaration that cannot be read is a refusal, never a pass: this hook has no
list of its own to fall back to. So is an index, in one of three wordings a
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

FENCE = re.compile(r"^\s*(?:```|~~~)")
# The prefix list as the document writes it: a line that ends by announcing it,
# then one bullet per prefix opening with the prefix in backticks. The count is
# not in the anchor, so adding a fourth prefix is one bullet and no edit here.
PREFIX_LEAD = re.compile(r"memory prefixes are:\s*$")
PREFIX_ITEM = re.compile(r"^[ \t]*[-*+][ \t]+`([A-Za-z0-9]+)-<[^`]*>`")


class ContractError(Exception):
    """The declaration could not be read, with the reason a reader can act on."""


def document(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise ContractError("%s: cannot be read: %s" % (path, exc))


def prefixes(text, path):
    """The memory prefixes the document declares, in the order it lists them.

    One home for the rule: the hook does not carry a list of its own, so a
    prefix added to the document is accepted the moment it is written and a
    document that stops declaring them refuses every write rather than falling
    back on a stale copy.
    """
    lines, found, reading, done = text.split("\n"), [], False, False
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if reading:
            item = PREFIX_ITEM.match(line)
            if item:
                found.append(item.group(1) + "-")
                continue
            if not line.strip():
                continue
            # Any other non-empty line ends the list. It is still tested for a
            # lead below, because a line that both ends one list and announces
            # another is the contradiction, not a terminator.
            reading, done = False, True
        if PREFIX_LEAD.search(line):
            # A second announcement is a document that declares the set twice.
            # Taking the union would let a list of the names being RETIRED
            # widen what is accepted, and the widening would be silent.
            if done or found:
                raise ContractError(
                    "%s: line %d announces the memory prefixes a second time. "
                    "One list is the declaration; two contradict, and a reader "
                    "cannot tell which is meant." % (path, number)
                )
            reading = True
    if not found:
        raise ContractError(
            "%s: no memory prefixes -- a line ending 'memory prefixes are:' "
            "followed by one bullet per prefix, each opening with "
            "`<prefix>-<subject>` in backticks" % path
        )
    return found


def rule(path=CONTRACT_DOCUMENT):
    return prefixes(document(path), path)


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


def violation(path, names):
    """The one reason this file fails, or None.

    Three checks, in the order a reader fixes them: the name says who reads the
    file, the index line is what makes it readable at all, and the retired
    declaration is last because removing it is the smallest edit of the three.
    """
    name = os.path.splitext(os.path.basename(path))[0]
    if not any(name.startswith(prefix) for prefix in names):
        return (
            "'%s' opens with none of the memory prefixes (%s). A memory is "
            "named after its reader, so `setup-` is `topic-`, `pitfalls` is one "
            "`pitfall-<subject>` per subject, and `history-` is a decision page "
            "under `docs/` -- see `spec/decision-pages.md`. A genuinely new "
            "prefix is added to the list in the same change that first uses it."
            % (name, ", ".join("'%s'" % prefix for prefix in names))
        )
    reason = indexed(path)
    if reason:
        return reason
    block = frontmatter(path)
    got = declared(block, TYPE_KEY) if block is not None else None
    # The declaration is retired outright, not checked against a row: the type
    # predicted nothing about whether the file was read, and nothing re-read it
    # after it was written. `name` and `description` are the whole frontmatter.
    if got is not None:
        return (
            "%s is declared ('%s'), and that key is retired. `name` and "
            "`description` are the whole frontmatter; the prefix carries what "
            "the type used to claim." % (TYPE_KEY, got)
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
