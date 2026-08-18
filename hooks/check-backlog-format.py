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
                       well, and a row tagged only #optional would otherwise
                       pass a requirement it says nothing about.
    item.tags.reason   where an item's own reason for wearing a tag goes,
                       in-parentheses right after the token. The key is the
                       whole permission: without it the parenthesis belongs to
                       no token and a row carrying one is refused.
    item.title_style   bold-lead-required — the text opens with a bold run
    item.label         where the item's group label sits and how it is spelled:
                       position title-lead, spelling in-brackets — one or more
                       bracketed labels at the head of the bold run, which is
                       the only place anything groups on. With required set, a
                       row carrying none is refused, and so is a bracket
                       further into the title: it reads as a label to every
                       reader that looks for one, and it would group nothing.
                       The label's words are the author's own — the contract
                       declares free-text and no vocabulary anywhere does
                       otherwise.
    item.body          the body shape. style: labeled-fields — the body is
                       indented `- label: text` bullets drawn from body.fields
                       in declared order, each label at most once, required
                       ones present, no others, and nothing after the title
                       on the head line; field_max_chars bounds each field's
                       folded text. Without a style, max_chars is the folded
                       whole-body budget. Bounds are ceilings the hook counts;
                       plainness stays author discipline, so a row inside
                       every bound can still break the writing rule.
    item.tags.kinds[].field_max_chars
                       one kind's own field bound, which replaces the body-wide
                       one for a row carrying it — a hard row needs room to say
                       what it is and an easy one does not. Absent says nothing
                       and leaves the body-wide bound answering. Where a row
                       carries more than one, the widest wins: the bounds move
                       with difficulty, so the widest is what the hardest claim
                       on the row asked for.
    item.tags.reason_max_chars
                       the bound on one tag's parenthesised reason.
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
# Where the group label sits, and how it is spelled. The leading run is what a
# grouping reader matches; the opener is what may not appear after it, since a
# second bracket looks like a label and groups nothing.
LABEL_POSITIONS = {"title-lead"}
LABEL_SPELLINGS = {"in-brackets": (r"^(?:\[[^\[\]\n]+\]\s*)+", "[")}

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
    field_max_by_tag = {}
    for row in kinds:
        if "field_max_chars" not in row:
            continue
        declared = row["field_max_chars"]
        if not (
            isinstance(declared, int)
            and not isinstance(declared, bool)
            and declared > 0
        ):
            raise ContractError(
                "%s: item.tags.kinds %r field_max_chars %r is not a positive whole "
                "number of characters" % (path, str(row.get("tag", "")), declared)
            )
        field_max_by_tag[str(row.get("tag", ""))] = declared
    scope_required = bool(tags_decl.get("scope_required"))
    if scope_required and not scope_tags:
        raise ContractError(
            "%s: item.tags.scope_required is set but no kind declares scope" % path
        )
    body_decl = item.get("body") or {}
    budget = None
    fields = None
    field_max = None
    if body_decl.get("style") == "labeled-fields":
        fields = [
            (str(row.get("label", "")), bool(row.get("required")))
            for row in body_decl.get("fields") or []
        ]
        if not fields or any(not label for label, _ in fields):
            raise ContractError("%s: item.body.fields must name non-empty labels" % path)
        field_max = body_decl.get("field_max_chars")
        if not (
            isinstance(field_max, int)
            and not isinstance(field_max, bool)
            and field_max > 0
        ):
            raise ContractError(
                "%s: item.body.field_max_chars %r is not a positive whole number of "
                "characters" % (path, field_max)
            )
    elif body_decl:
        budget = body_decl.get("max_chars")
        if not (isinstance(budget, int) and not isinstance(budget, bool) and budget > 0):
            raise ContractError(
                "%s: item.body.max_chars %r is not a positive whole number of characters"
                % (path, budget)
            )
    label_decl = item.get("label") or {}
    label = None
    if label_decl:
        position = label_decl.get("position")
        spelling = label_decl.get("spelling")
        if position not in LABEL_POSITIONS:
            raise ContractError(
                "%s: item.label.position %r is a place this hook cannot compile"
                % (path, position)
            )
        if spelling not in LABEL_SPELLINGS:
            raise ContractError(
                "%s: item.label.spelling %r is a form this hook cannot compile"
                % (path, spelling)
            )
        lead, opener = LABEL_SPELLINGS[spelling]
        label = {
            "lead": re.compile(lead),
            "opener": opener,
            "required": bool(label_decl.get("required")),
        }
    reason_max = tags_decl.get("reason_max_chars")
    if reason_max is not None and not (
        isinstance(reason_max, int) and not isinstance(reason_max, bool) and reason_max > 0
    ):
        raise ContractError(
            "%s: item.tags.reason_max_chars %r is not a positive whole number of "
            "characters" % (path, reason_max)
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
    title_form = "**[LABEL] Title.**" if label else "**Title.**"
    if fields:
        form = "`%s [<m>] %s%s %s` + indented %s field bullets" % (
            bullet,
            item.get("date"),
            " [#tag …]" if tags else "",
            title_form,
            "/".join("`- %s:`" % name for name, required in fields if required),
        )
    else:
        form = "`%s [<m>] %s%s %s body`" % (
            bullet,
            item.get("date"),
            " [#tag …]" if tags else "",
            title_form,
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
        "reason_body": re.compile(
            r"#(?:%s)\(([^()]*)\)" % "|".join(re.escape(t) for t in tags)
            if tags
            else r"(?!)"
        ),
        "label": label,
        "scope_tags": scope_tags,
        "scope_required": scope_required,
        "body_max": budget,
        "fields": fields,
        "field_max": field_max,
        "field_max_by_tag": field_max_by_tag,
        "reason_max": reason_max,
        "form": form,
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


def title(line, matched):
    """The text inside the item's bold run, or all that follows an unclosed one.

    An unterminated run is the title style's business; the label rule still
    reads the head of it, which is where a label sits either way.
    """
    rest = line[matched.end(1):][len("**"):]
    closed = rest.find("**")
    return rest if closed < 0 else rest[:closed]


def label_violations(text, rule):
    """Every way one item's group label breaks the declaration.

    The label is what a reader groups rows by, so a title carrying a bracket
    anywhere but the head is refused rather than read: nothing downstream can
    tell that one from a label, and it would put the row in a group of one.
    """
    lead = rule["label"]["lead"].match(text)
    if lead is None:
        if rule["label"]["required"]:
            return [
                "the bold title must open with a bracketed label naming which rows "
                "this one belongs with, as in '**[PARSER] A plus bullet is "
                "swallowed.**'"
            ]
        return []
    if rule["label"]["opener"] in text[lead.end():]:
        return [
            "a bracket sits inside the title text; only the run leading the title "
            "is a label"
        ]
    return []


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
        if rule["reason_max"] is not None:
            for reason_text in rule["reason_body"].findall(matched.group(1)):
                if len(reason_text) > rule["reason_max"]:
                    found.append(
                        (
                            number,
                            line,
                            "a tag reason runs %d characters, over the %d-character "
                            "bound" % (len(reason_text), rule["reason_max"]),
                        )
                    )
        if rule["label"]:
            found.extend(
                (number, line, reason)
                for reason in label_violations(title(line, matched), rule)
            )
        if rule["fields"]:
            # The widest the row's own tags ask for, and the body-wide bound
            # when they ask for nothing — the same tie-break the effort rule
            # makes, because the bounds move with the same claim.
            bound = max(
                (rule["field_max_by_tag"][tag] for tag in carried if tag in rule["field_max_by_tag"]),
                default=rule["field_max"],
            )
            found.extend(
                (number, line, reason)
                for reason in field_violations(
                    body(line, matched), continuation, rule, bound
                )
            )
        elif rule["body_max"]:
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


FIELD = re.compile(r"^- ([A-Za-z]+):\s*(.*)$")


def field_violations(head_rest, continuation, rule, bound):
    """Every way one item's labeled-fields body breaks the declaration.

    `bound` is this row's own field ceiling, resolved from the tags it
    carries, so a row is measured against what its own difficulty asks for.
    """
    reasons = []
    if head_rest.strip():
        reasons.append(
            "text after the title belongs in the field bullets, not on the item line"
        )
    declared = [label for label, _ in rule["fields"]]
    required = [label for label, req in rule["fields"] if req]
    parsed = []
    current = None
    for text in continuation:
        matched = FIELD.match(text)
        if matched:
            label = matched.group(1)
            if label not in declared:
                reasons.append(
                    "field '%s:' is not declared; the fields are %s"
                    % (label, ", ".join("'%s:'" % l for l in declared))
                )
                current = None
                continue
            current = [label, matched.group(2)]
            parsed.append(current)
        elif current is not None:
            current[1] += " " + text
        else:
            reasons.append("body text sits outside any field bullet: %r" % text)
    labels = [label for label, _ in parsed]
    if len(set(labels)) != len(labels):
        reasons.append("a field appears more than once")
    elif labels != [label for label in declared if label in labels]:
        reasons.append(
            "fields out of declared order; the order is %s"
            % ", ".join("'%s:'" % l for l in declared)
        )
    missing = [label for label in required if label not in labels]
    if missing:
        reasons.append(
            "missing required field(s): %s" % ", ".join("'%s:'" % l for l in missing)
        )
    for label, text in parsed:
        length = len(" ".join(text.split()))
        if length > bound:
            reasons.append(
                "field '%s:' runs %d characters, over the %d-character bound"
                % (label, length, bound)
            )
    return reasons


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
