#!/usr/bin/env python3
"""Refuse a malformed decision page, and a link into one that resolves to nothing.

`spec/decision-pages.md` is the contract; this enforces the machine-decidable
half of it and nothing else. The provenance block, the doctype and the prose
were the `writing` skill's `render-check.py`'s, and a second reader of one rule
drifts from the first, so none of them is read here. That skill was retired in
`f94ce33` and nothing enforces those three today: they are contract without a
checker until one is written.

Two entry points, one judgement, and one exit code for it: 0 allows, 2 refuses,
anything else is this script's own failure and refuses nothing.

  * with arguments, a file checker -- one line per path;
  * with none, a `PostToolUse` hook reading the payload on stdin.

`PostToolUse` fires after the write has landed, so a 2 there does not undo it;
what it does is put the reason in front of the model that wrote it, which is the
only correction available once the bytes are on disk. The rule this enforces is
therefore loud, not preventive, and `spec/decision-pages.md` says so too.

A page declares itself a decision page with `class="decision-page"` on its
`<body>`, and only a declared page is held to the entry rules. `docs/` holds
views of every kind, and an ordinary explanation's `<h2>First section</h2>` is
not a malformed decision -- judging every page here would refuse an ordinary
view on every write.

Every path outside this checkout's `docs/` and its links is skipped, and the
skip says so: a hook registered machine-wide sees every write on the machine,
and a silent skip and a pass look identical from the outside.
"""

import json
import os
import re
import sys

# The checkout this script ships in, so a copy under test judges its own tree
# rather than the live one. `check-memtype.py` resolves its contract the same
# way and for the same reason.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# The one markdown `docs/` holds: the page list a repository's file naming is
# read from. Every other markdown file under `docs/` is misfiled.
INDEX = "INDEX.md"

# An attribute value may hold a `>` (`title="a > b"`), so the attribute run is
# scanned quote by quote rather than up to the first `>`; the naive form read
# the rest of the tag as the entry's title.
ATTRS = r"""((?:[^>"']|"[^"]*"|'[^']*')*)"""
H2 = re.compile(r"<h2\b" + ATTRS + r">(.*?)</h2>", re.DOTALL | re.IGNORECASE)
BODY = re.compile(r"<body\b" + ATTRS + r">", re.IGNORECASE)
ID = re.compile(r"""\bid\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
CLASS = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
TAG = re.compile(r"<[^>]*>")
DATE = re.compile(r"\s*(\d{4}-\d{2}-\d{2})\b")

# Commented-out markup is not in the page. Both the entries and the links are
# read from the text with comments removed, so a draft entry parked in a comment
# is neither counted nor refused.
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

# The class that declares a decision page.
MARK = "decision-page"

# A link that unambiguously addresses THIS docs root: spelled from the home
# directory. A bare `docs/x.html#y` is not one -- every repository on the
# machine has a `docs/`, and a memory citing another one is not this hook's
# business. Page-to-page links inside `docs/` are resolved separately, where
# the relative form is unambiguous because the file itself sits there.
#
# An anchor never ends in a dot, so a link closing a sentence keeps its full
# stop out of the id -- the first version of this pattern refused every link
# written at the end of a sentence.
PAGE_RE = r"([A-Za-z0-9._-]+\.html)"
ANCHOR_RE = r"([A-Za-z0-9_-]+(?:[.][A-Za-z0-9_-]+)*)"
HOME_LINK = re.compile(
    r"(?:~|\$HOME|/Users/[^/\s]+)/\.claude/docs/" + PAGE_RE + "#" + ANCHOR_RE)
# The local form has to START a path, or `https://docs.python.org/3/library/
# re.html#re.DOTALL` reads as a sibling page named `re.html`. The lookbehind
# refuses a match that continues someone else's path, host, or word.
LOCAL_LINK = re.compile(
    r"(?<![\w/.:-])(?:\./|\.\./docs/|docs/)?" + PAGE_RE + "#" + ANCHOR_RE)


def under(path, directory):
    """Whether `path` sits inside `directory`, both resolved."""
    path = os.path.abspath(path)
    directory = os.path.abspath(directory)
    return path == directory or path.startswith(directory + os.sep)


def read(path):
    """The file's text, or None when it cannot be read as text at all."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError):
        return None


def visible(text):
    """The page with its comments removed."""
    return COMMENT.sub("", text)


def declared(text):
    """Whether the page declares itself a decision page on its `<body>`."""
    match = BODY.search(visible(text))
    if not match:
        return False
    attrs = CLASS.search(match.group(1))
    return bool(attrs) and MARK in attrs.group(1).split()


def entries(text):
    """Every `<h2>` in the page, as (id, visible text) in document order."""
    found = []
    for attrs, inner in H2.findall(visible(text)):
        match = ID.search(attrs)
        anchor = match.group(1) if match else None
        found.append((anchor, TAG.sub("", inner).strip()))
    return found


def anchors(path):
    """The set of `<h2>` ids in a page, empty when the page cannot be read."""
    text = read(path)
    return {a for a, _ in entries(text) if a} if text is not None else set()


def page_faults(text):
    """What is wrong with a decision page's entries, as a list of sentences."""
    faults = []
    seen = {}
    for index, (anchor, title) in enumerate(entries(text), start=1):
        shown = title[:60] or "(empty)"
        if not anchor:
            faults.append(
                "entry %d, '%s', carries no id. The id is the address a memory "
                "or a commit links to, so an entry without one cannot be cited."
                % (index, shown)
            )
        elif anchor in seen:
            faults.append(
                "entry %d, '%s', repeats the id '%s' already used by entry %d. "
                "A link to it resolves to whichever the browser reaches first."
                % (index, shown, anchor, seen[anchor])
            )
        else:
            seen[anchor] = index
        if not DATE.match(title):
            faults.append(
                "entry %d, '%s', does not open with a YYYY-MM-DD date. Undated, "
                "it cannot be ordered, and a later entry cannot supersede it."
                % (index, shown)
            )
    return faults


def link_faults(path, text):
    """Links into this checkout's `docs/` that resolve to nothing."""
    text = visible(text)
    wanted = set(HOME_LINK.findall(text))
    if under(path, DOCS):
        # Inside `docs/` the relative form is unambiguous: it can only mean a
        # sibling page. Outside it, the same string means some other repository.
        wanted |= set(LOCAL_LINK.findall(text))
    faults = []
    for page, anchor in sorted(wanted):
        target = os.path.join(DOCS, page)
        if not os.path.exists(target):
            faults.append(
                "links to '%s#%s', and %s holds no such page." % (page, anchor, DOCS)
            )
        elif anchor not in anchors(target):
            faults.append(
                "links to '%s#%s', and that page carries no entry with that id. "
                "An id is permanent precisely so this link keeps working."
                % (page, anchor)
            )
    return faults


def verdict(path):
    """(ok, message). `ok` false means the write is refused."""
    if not os.path.exists(path):
        return True, "%s: skipped, no such file" % path

    base = os.path.basename(path)
    # By name, before the file is read: the misfiling is the extension, and a
    # `.md` that is not valid UTF-8 is misfiled just the same. Reading first
    # let a binary file under `docs/` skip a check it had already failed.
    if under(path, DOCS) and base.endswith(".md") and base != INDEX:
        return False, (
            "%s is markdown under %s, and only `%s` may be. A view is HTML and "
            "`spec/` is where normative markdown lives, so this is misfiled, "
            "not temporary." % (path, DOCS, INDEX)
        )

    text = read(path)
    if text is None:
        return True, "%s: skipped, not readable as UTF-8 text" % path

    if under(path, DOCS):
        if base == INDEX:
            return True, "%s: ok, the docs index" % path
        if not base.endswith(".html"):
            # A stylesheet, a font, a rendered PNG. `docs/` holds what a view
            # needs, and only its markdown is misfiled.
            return True, "%s: skipped, not a view" % path
        faults = link_faults(path, text)
        if not declared(text):
            # A `docs/` tree holds views of every kind. Without the marker
            # the entry rules do not apply, and only the links are read.
            if faults:
                return False, "%s %s" % (path, "; also ".join(faults))
            return True, ("%s: ok, a view, not declared a decision page; links only"
                          % path)
        faults = page_faults(text) + faults
        if faults:
            return False, "%s is a decision page and %s" % (path, "; also ".join(faults))
        return True, "%s: ok, decision page, %d entries" % (path, len(entries(text)))

    if not under(path, ROOT):
        return True, "%s: skipped, outside %s" % (path, ROOT)

    faults = link_faults(path, text)
    if faults:
        return False, "%s %s" % (path, "; also ".join(faults))
    return True, "%s: ok, no unresolved link into %s" % (path, DOCS)


def main():
    if not os.path.isdir(DOCS):
        # Nothing to enforce yet, and saying so beats a silent zero: this is
        # what a checkout before the first decision page looks like.
        if len(sys.argv) > 1:
            print("check-decision-page: %s does not exist; nothing checked" % DOCS)
        return 0

    if len(sys.argv) > 1:
        failed = False
        for path in sys.argv[1:]:
            ok, message = verdict(path)
            if ok:
                print(message)
            else:
                failed = True
                print("check-decision-page: %s" % message, file=sys.stderr)
        return 2 if failed else 0

    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path:
        return 0
    ok, message = verdict(path)
    if ok:
        return 0
    print("check-decision-page: %s" % message, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
