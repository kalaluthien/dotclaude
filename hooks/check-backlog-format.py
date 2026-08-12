#!/usr/bin/env python3
"""Validate the backlog item grammar in a memory pool's board file.

The grammar is not this file's. It is declared once, in the "Filing" section
of ~/.claude/CLAUDE.md, as the fenced `json contract=pool` block; this hook
parses that block and compiles what it says. Every other reader of a pool —
the board service among them — compiles the same declaration, which is the
whole point: two encodings of one rule is how a hook and a reader come to
disagree about the same file, and they did.

What the block declares and this file compiles:

    item.bullet        the list marker an item opens with, at column 0
    item.markers       the bracketed status characters
    item.date          the date form
    item.tags          the declared #tag kinds, sitting between the date and
                       the title (position: after-date); with scope_required,
                       every item must carry at least one kind declaring
                       scope: true — the scope kinds. Not "every kind that
                       waits on nobody": a priority kind waits on nobody as
                       well, and a row tagged only #urgent would otherwise
                       pass a requirement it says nothing about.
    item.tags.reason   where an item's own reason for wearing a tag goes,
                       in-parentheses right after the token. The key is the
                       whole permission: without it the parenthesis belongs to
                       no token and a row carrying one is refused.
    item.title_style   bold-lead-required — the text opens with a bold run
    item.body          max_chars, the budget for the text after that bold run.
                       The body is the whole card: every indented line under
                       the item is folded in with one space before the count,
                       so wrapping a row over more lines buys it no room. The
                       budget is the checkable half of the writing rule; the
                       three-sentence half stays author discipline, so a row
                       under budget can still break the rule. A contract
                       without the key declares no budget and none is checked.
    sections.match     word-prefix — a prose heading is a listed name, alone
                       or followed by a space or a colon
    pool.pattern       where a pool lives, which is how a path is recognised
    pool.board_file    the one file in it that carries items

A prose section keeps plain bullets and an indented bullet is item body, so
neither is checked.

Two entry points:
  - as a Claude Code PostToolUse hook: reads the tool payload on stdin, checks
    the touched file, exits 2 with the offending line on stderr.
  - as a CLI: `check-backlog-format.py FILE...`, exits 1 on any violation.

A contract that cannot be read is a refusal, never a pass: this hook has no
grammar of its own to fall back to, and accepting a write it could not check
would be the silent half of a rule that only looks enforced.
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

DATE_PATTERNS = {"YYYY-MM-DD": r"\d{4}-\d{2}-\d{2}"}
TITLE_PATTERNS = {"bold-lead-required": r"\*\*\S"}
# Where an item's own reason for a tag may sit. The empty key is a contract
# silent on the subject, and it admits none: the parenthesis is then part of no
# token, so a row carrying one fails the expression like any other stray text.
REASON_PATTERNS = {"": "", "in-parentheses": r"(?:\([^()]*\))?"}

BULLET = re.compile(r"^(?:[-*+] |\d+[.)] )")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
FENCE = re.compile(r"^\s*(?:```|~~~)")


class ContractError(Exception):
    """The declaration could not be read, with the reason a reader can act on."""


def contract(path=CONTRACT_DOCUMENT):
    """The pool contract, parsed and compiled out of the document that owns it."""
    try:
        with open(path, encoding="utf-8") as handle:
            document = handle.read()
    except OSError as exc:
        raise ContractError("%s: cannot be read: %s" % (path, exc))

    found = BLOCK.search(document)
    if not found:
        raise ContractError(
            "%s: no ```json contract=pool block — the grammar is declared there" % path
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

    item = data.get("item") or {}
    pool = data.get("pool") or {}
    sections = data.get("sections") or {}
    markers = [row.get("marker", "") for row in item.get("markers") or []]
    tags_decl = item.get("tags") or {}
    kinds = tags_decl.get("kinds") or []
    tags = [str(row.get("tag", "")) for row in kinds]
    scope_tags = [str(row.get("tag", "")) for row in kinds if row.get("scope")]
    scope_required = bool(tags_decl.get("scope_required"))
    if scope_required and not scope_tags:
        raise ContractError(
            "%s: item.tags.scope_required is set but no kind declares scope" % path
        )
    body = item.get("body") or {}
    budget = body.get("max_chars")
    if body and not (isinstance(budget, int) and not isinstance(budget, bool) and budget > 0):
        raise ContractError(
            "%s: item.body.max_chars %r is not a positive whole number of characters"
            % (path, budget)
        )
    date = DATE_PATTERNS.get(item.get("date"))
    title = TITLE_PATTERNS.get(item.get("title_style"))
    match = sections.get("match")
    pattern = pool.get("pattern") or ""

    if not markers or any(len(m) != 1 for m in markers):
        raise ContractError("%s: item.markers must be single characters" % path)
    if tags_decl and tags_decl.get("position") != "after-date":
        raise ContractError(
            "%s: item.tags.position %r is a rule this hook cannot compile"
            % (path, tags_decl.get("position"))
        )
    if tags_decl and (not tags or any(not t for t in tags)):
        raise ContractError("%s: item.tags.kinds must name non-empty tags" % path)
    if date is None:
        raise ContractError(
            "%s: item.date %r is a form this hook cannot compile"
            % (path, item.get("date"))
        )
    if title is None:
        raise ContractError(
            "%s: item.title_style %r is a rule this hook cannot compile"
            % (path, item.get("title_style"))
        )
    if match != "word-prefix":
        raise ContractError(
            "%s: sections.match %r is a rule this hook cannot compile" % (path, match)
        )
    if not pool.get("board_file") or len(pattern.split("/")) < 2:
        raise ContractError("%s: pool.board_file and pool.pattern are required" % path)

    bullet = item.get("bullet", "-")
    reason = tags_decl.get("reason", "")
    if reason and reason not in REASON_PATTERNS:
        raise ContractError(
            "%s: item.tags.reason %r is a place this hook cannot compile" % (path, reason)
        )
    tag_run = (
        r"((?:#(?:%s)%s )*)" % ("|".join(re.escape(t) for t in tags), REASON_PATTERNS[reason])
        if tags
        else "()"
    )
    return {
        "item": re.compile(
            r"^%s \[[%s]\] %s %s%s"
            % (
                re.escape(bullet),
                "".join(re.escape(m) for m in markers),
                date,
                tag_run,
                title,
            )
        ),
        "token": re.compile(
            r"#(%s)%s" % ("|".join(re.escape(t) for t in tags), REASON_PATTERNS[reason])
            if tags
            else r"(?!)"
        ),
        "scope_tags": scope_tags,
        "scope_required": scope_required,
        "body_max": budget if body else None,
        "form": "`%s [<m>] %s%s **Title.** body`"
        % (bullet, item.get("date"), " [#tag …]" if tags else ""),
        "markers": markers,
        "tags": tags,
        "prose": [str(p).lower() for p in sections.get("prose_prefixes") or []],
        "board_file": pool["board_file"],
        # A pool's own directory is the pattern's last directory segment:
        # `projects/*/memory/*.md` puts a board file in a `memory` directory.
        "pool_dir": pattern.split("/")[-2],
    }


def is_prose(heading, rule):
    """A heading names a prose section under the contract's word-prefix rule.

    The opening words carry the section's role; a trailing gloss such as
    "Horizon (dots noted, not scheduled)" only annotates it.
    """
    text = heading.strip().lower()
    return any(
        text == name or text.startswith(name + " ") or text.startswith(name + ":")
        for name in rule["prose"]
    )


def rows(lines, rule):
    """Every candidate item line, paired with the indented lines that continue it.

    A candidate is a bullet at column 0 outside the front matter, a fence and a
    prose section. Its continuation is every indented non-empty line that
    follows — an indented bullet among them, which the contract calls the body
    of the item above it.
    """
    found = []
    in_front_matter = lines and lines[0].strip() == "---"
    in_fence = False
    prose = False
    current = None

    for number, line in enumerate(lines, start=1):
        if in_front_matter:
            if number > 1 and line.strip() == "---":
                in_front_matter = False
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            current = None
            continue
        if in_fence:
            continue
        heading = HEADING.match(line)
        if heading:
            prose = is_prose(heading.group(1), rule)
            current = None
            continue
        if prose:
            continue
        if BULLET.match(line):
            current = (number, line, [])
            found.append(current)
            continue
        if current is not None and line[:1].isspace() and line.strip():
            current[2].append(line.strip())
            continue
        current = None
    return found


def body(line, matched):
    """The item line's text after the bold title.

    Empty when the bold run never closes: the whole line is then the title, and
    an unterminated run is the title style's business, not the budget's.
    """
    rest = line[matched.end(1):]
    closed = rest.find("**", len("**"))
    return "" if closed < 0 else rest[closed + len("**"):]


def violations(path, rule):
    """Return a list of (line_number, line, reason) for one board file."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")

    found = []
    for number, line, continuation in rows(lines, rule):
        matched = rule["item"].match(line)
        if not matched:
            found.append((number, line, "expected %s" % rule["form"]))
            continue
        # Named off the token rather than split on whitespace: a reason holds
        # spaces, so splitting the run would read "#code(the request named the"
        # as a tag and lose the one that is there.
        carried = set(rule["token"].findall(matched.group(1)))
        if rule["scope_required"] and not carried & set(rule["scope_tags"]):
            found.append(
                (
                    number,
                    line,
                    "needs at least one scope tag: %s"
                    % ", ".join("'#%s'" % tag for tag in rule["scope_tags"]),
                )
            )
        if rule["body_max"]:
            text = " ".join([body(line, matched)] + continuation)
            length = len(" ".join(text.split()))
            if length > rule["body_max"]:
                found.append(
                    (
                        number,
                        line,
                        "the text after the title runs %d characters, over the "
                        "%d-character budget (indented lines folded in)"
                        % (length, rule["body_max"]),
                    )
                )
    return found


def report(path, found, rule):
    # Counted over distinct lines: one item can break two rules at once.
    lines = [
        "%s: %d backlog item(s) break the grammar."
        % (path, len({number for number, _, _ in found}))
    ]
    markers = ", ".join("'%s'" % marker for marker in rule["markers"])
    for number, line, reason in found:
        lines.append("  line %d: %s" % (number, line.rstrip()))
        if reason.startswith("expected"):
            lines.append("    %s — <m> is one of %s." % (reason, markers))
        else:
            lines.append("    %s." % reason)
    if rule["tags"]:
        lines.append(
            "  (a tag is one of %s, between the date and the title)"
            % ", ".join("'#%s'" % tag for tag in rule["tags"])
        )
    lines.append("  (the grammar is declared in %s, section Filing)" % CONTRACT_DOCUMENT)
    return "\n".join(lines)


def is_board_file(path, rule):
    return (
        os.path.basename(path) == rule["board_file"]
        and os.path.basename(os.path.dirname(path)) == rule["pool_dir"]
    )


def main():
    try:
        rule = contract()
    except ContractError as exc:
        print("check-backlog-format: %s" % exc, file=sys.stderr)
        # A write this hook could not check is refused, not waved through.
        return 1 if len(sys.argv) > 1 else 2

    if len(sys.argv) > 1:
        failed = False
        for path in sys.argv[1:]:
            found = violations(path, rule)
            if found:
                failed = True
                print(report(path, found, rule), file=sys.stderr)
            else:
                print("%s: ok" % path)
        return 1 if failed else 0

    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path or not is_board_file(path, rule) or not os.path.exists(path):
        return 0
    found = violations(path, rule)
    if not found:
        return 0
    print(report(path, found, rule), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
