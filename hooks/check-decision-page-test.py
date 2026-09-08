#!/usr/bin/env python3
"""Cases for `check-decision-page.py`, allow side first.

The allow cases come first on purpose. This hook is registered machine-wide, so
a missed refusal is caught at the next write and a false refusal stops every
session on the machine at once; the ordinary shapes it could wrongly catch are
the half that has to hold.

The script under test is COPIED into a temp tree and run there, because it
resolves `docs/` from its own location -- a suite that pointed it at the live
checkout would be reading the real pages and would pass while the shipped copy
was broken.

Run: python3 hooks/check-decision-page-test.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check-decision-page.py")

PAGE = """<!doctype html><html><head><title>Pool shape</title></head>
<body class="decision-page">
<h1>Pool shape</h1>
<dl class="provenance">
  <dt>Doctype</dt>  <dd>explanation</dd>
  <dt>Question</dt> <dd>what has the pool's layout been, and why</dd>
  <dt>Updated</dt>  <dd>2026-09-06</dd>
</dl>
<h2 id="grouped-by-subject">2026-08-18 — setup topics grouped by subject</h2>
<p>Sixteen files became six.</p>
<h2 id="renamed-by-reader">2026-09-06 — the pool renamed by reader</h2>
<p>The memtype axis went.</p>
</body></html>
"""


def decision(inner):
    """A minimal page that declares itself a decision page."""
    return '<html><body class="decision-page"><h1>T</h1>%s</body></html>' % inner


def view(inner):
    """A page under `docs/` that is some other doctype."""
    return '<html><body><h1>T</h1>%s</body></html>' % inner


class Tree(object):
    """A temp checkout holding the script, a `docs/`, and a memory pool."""

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="decision-page-")
        os.makedirs(os.path.join(self.root, "hooks"))
        os.makedirs(os.path.join(self.root, "docs"))
        self.pool = os.path.join(self.root, "projects", "-tmp-p", "memory")
        os.makedirs(self.pool)
        self.script = os.path.join(self.root, "hooks", "check-decision-page.py")
        shutil.copy(SCRIPT, self.script)

    def write(self, relative, text, binary=False):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mode, payload = ("wb", text) if binary else ("w", text)
        with open(path, mode) as handle:
            handle.write(payload)
        return path

    def run(self, *paths):
        done = subprocess.run(
            [sys.executable, self.script] + list(paths),
            capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    def hook(self, path):
        payload = json.dumps({"tool_input": {"file_path": path}})
        done = subprocess.run(
            [sys.executable, self.script],
            input=payload, capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    def drop(self):
        shutil.rmtree(self.root, ignore_errors=True)


RESULTS = []


def case(name, ok, detail=""):
    RESULTS.append((name, ok, detail))


def expect(name, got_code, got_text, code, says=(), absent=()):
    """One case: the exit status AND what the run said.

    A status alone is satisfied by every other cause that shares it, so every
    case names a phrase the message must carry, and refusals also name the
    phrase that must be ABSENT -- the wrong diagnosis is how a check that
    silently stopped enforcing still reads green.
    """
    problems = []
    if got_code != code:
        problems.append("exit %d, wanted %d" % (got_code, code))
    for phrase in says:
        if phrase not in got_text:
            problems.append("said nothing about %r" % phrase)
    for phrase in absent:
        if phrase in got_text:
            problems.append("wrongly diagnosed %r" % phrase)
    case(name, not problems, "; ".join(problems) + (" || " + got_text.strip()[:200] if problems else ""))


def allow_cases(t):
    t.write("docs/pool-shape.html", PAGE)

    code, out = t.run(os.path.join(t.root, "docs", "pool-shape.html"))
    expect("a well-formed decision page is accepted", code, out, 0,
           says=["ok, decision page, 2 entries"])

    t.write("docs/INDEX.md", "- [Pool shape](pool-shape.html) - the pool's layout decisions\n")
    code, out = t.run(os.path.join(t.root, "docs", "INDEX.md"))
    expect("INDEX.md is the one markdown docs/ may hold", code, out, 0,
           says=["ok, the docs index"], absent=["misfiled"])

    p = t.write("projects/-tmp-p/memory/topic-x.md",
                "See ~/.claude/docs/pool-shape.html#renamed-by-reader for why.\n")
    code, out = t.run(p)
    expect("a memory link that resolves is accepted", code, out, 0, says=["ok, no unresolved link"])

    p = t.write("projects/-tmp-p/memory/topic-home.md",
                "See $HOME/.claude/docs/pool-shape.html#grouped-by-subject.\n")
    # The full stop closes the sentence and is not part of the id.
    code, out = t.run(p)
    expect("the $HOME spelling resolves too", code, out, 0, says=["ok, no unresolved link"])

    p = t.write("projects/-tmp-p/memory/topic-other.md",
                "Repointed docs/agent-config-scopes.html#scopes in the workspace repo.\n")
    code, out = t.run(p)
    expect("a bare docs/ link means ANOTHER repository and is left alone",
           code, out, 0, says=["ok, no unresolved link"], absent=["holds no such page"])

    p = t.write("projects/-tmp-p/memory/topic-plain.md", "No links here at all.\n")
    code, out = t.run(p)
    expect("an ordinary memory with no links is accepted", code, out, 0)

    outside = tempfile.mkdtemp(prefix="decision-page-outside-")
    stray = os.path.join(outside, "docs-notes.md")
    with open(stray, "w") as handle:
        handle.write("~/.claude/docs/missing.html#nope\n")
    code, out = t.run(stray)
    expect("a file outside the checkout is skipped, and says so", code, out, 0,
           says=["skipped, outside"], absent=["holds no such page"])
    shutil.rmtree(outside, ignore_errors=True)

    code, out = t.run(os.path.join(t.root, "docs", "never-written.html"))
    expect("a path that does not exist is skipped, not refused", code, out, 0,
           says=["skipped, no such file"])

    p = t.write("projects/-tmp-p/memory/blob.bin", b"\xff\xfe\x00binary", binary=True)
    code, out = t.run(p)
    expect("a file that is not UTF-8 text is skipped, not refused", code, out, 0,
           says=["not readable as UTF-8"])

    t.write("docs/subheads.html",
            decision('<h2 id="a">2026-01-01 one</h2><h3>a subhead with no id</h3>'))
    code, out = t.run(os.path.join(t.root, "docs", "subheads.html"))
    expect("only h2 is an entry; an h3 needs no id", code, out, 0, says=["1 entries"])

    t.write("docs/rich.html",
            decision('<h2 id="b">2026-02-03 the <code>setup-</code> row</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "rich.html"))
    expect("an entry title may carry markup around its words", code, out, 0,
           says=["ok, decision page"])

    t.write("docs/extra-fields.html",
            decision('<dl><dt>Doctype</dt><dd>guide</dd><dt>Commit</dt><dd>abc</dd></dl>'
                     '<h2 id="c">2026-02-04 a decision</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "extra-fields.html"))
    expect("the provenance block is not this hook's to judge", code, out, 0,
           says=["ok, decision page"], absent=["Doctype", "provenance"])

    t.write("docs/empty.html", decision("<p>Nothing decided yet.</p>"))
    code, out = t.run(os.path.join(t.root, "docs", "empty.html"))
    expect("a page with no entries yet is accepted", code, out, 0, says=["0 entries"])

    code, out = t.hook(os.path.join(t.root, "docs", "pool-shape.html"))
    expect("the stdin hook lets a good page through", code, out, 0)

    done = subprocess.run([sys.executable, t.script], input="{}",
                          capture_output=True, text=True)
    expect("a payload with no file_path is not an error", done.returncode,
           done.stdout + done.stderr, 0)

    done = subprocess.run([sys.executable, t.script], input="not json",
                          capture_output=True, text=True)
    expect("an unparseable payload is not an error", done.returncode,
           done.stdout + done.stderr, 0)

    t.write("docs/explainer.html", view('<h2>First section</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "explainer.html"))
    expect("an undeclared view keeps its own h2 rules", code, out, 0,
           says=["not declared a decision page"],
           absent=["carries no id", "does not open with a YYYY-MM-DD date"])

    t.write("docs/nearly.html", '<html><body class="my-decision-page">'
                                '<h1>T</h1><h2>First section</h2></body></html>')
    code, out = t.run(os.path.join(t.root, "docs", "nearly.html"))
    expect("the marker is a whole class, not a substring of one", code, out, 0,
           says=["not declared a decision page"], absent=["carries no id"])

    t.write("docs/external.html",
            decision('<h2 id="x">2026-04-01 a decision</h2><p>see '
                     '<a href="https://docs.python.org/3/library/re.html#re.DOTALL">re</a></p>'))
    code, out = t.run(os.path.join(t.root, "docs", "external.html"))
    expect("a URL ending in a page and a fragment is not a sibling page",
           code, out, 0, says=["ok, decision page"], absent=["holds no such page"])

    t.write("docs/style.css", "body { margin: 0 }")
    code, out = t.run(os.path.join(t.root, "docs", "style.css"))
    expect("a stylesheet under docs/ is not markdown and is not refused",
           code, out, 0, says=["skipped, not a view"], absent=["misfiled"])

    t.write("docs/diagram.png", b"\x89PNG\r\n\x1a\n\xff", binary=True)
    code, out = t.run(os.path.join(t.root, "docs", "diagram.png"))
    expect("a rendered PNG under docs/ is not refused", code, out, 0,
           absent=["misfiled"])

    t.write("docs/commented.html",
            decision('<h2 id="live">2026-04-02 a decision</h2>'
                     '<!-- <h2>a draft</h2> and <a href="gone.html#nope">a dead link</a> -->'))
    code, out = t.run(os.path.join(t.root, "docs", "commented.html"))
    expect("commented-out markup is not in the page", code, out, 0,
           says=["ok, decision page, 1 entries"],
           absent=["carries no id", "holds no such page"])

    t.write("docs/attr.html",
            decision('<h2 id="k" title="a > b">2026-04-03 a decision</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "attr.html"))
    expect("a `>` inside an attribute value does not end the tag", code, out, 0,
           says=["ok, decision page, 1 entries"],
           absent=["does not open with a YYYY-MM-DD date"])

    bare = Tree()
    os.rmdir(os.path.join(bare.root, "docs"))
    code, out = bare.run(bare.write("projects/-tmp-p/memory/topic-y.md", "hi\n"))
    expect("a checkout with no docs/ yet checks nothing and says so", code, out, 0,
           says=["does not exist"])
    bare.drop()


def refuse_cases(t):
    p = t.write("docs/stray.md", "# a decision, in markdown\n")
    code, out = t.run(p)
    expect("markdown under docs/ that is not INDEX.md is refused", code, out, 2,
           says=["misfiled"])

    t.write("docs/no-id.html", decision('<h2>2026-03-01 a decision with no id</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "no-id.html"))
    expect("an entry with no id is refused", code, out, 2,
           says=["carries no id"], absent=["YYYY-MM-DD date"])

    t.write("docs/no-date.html", decision('<h2 id="d">a decision with no date</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "no-date.html"))
    expect("an entry that does not open with a date is refused", code, out, 2,
           says=["does not open with a YYYY-MM-DD date"], absent=["carries no id"])

    t.write("docs/late-date.html",
            decision('<h2 id="f">a decision taken on 2026-03-05</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "late-date.html"))
    expect("a date anywhere but the opening is not an opening date", code, out, 2,
           says=["does not open with a YYYY-MM-DD date"])

    t.write("docs/dupes.html",
            decision('<h2 id="same">2026-03-02 first</h2>'
                     '<h2 id="same">2026-03-03 second</h2>'))
    code, out = t.run(os.path.join(t.root, "docs", "dupes.html"))
    expect("two entries sharing an id are refused", code, out, 2,
           says=["repeats the id 'same'"])

    p = t.write("projects/-tmp-p/memory/topic-bad-page.md",
                "See ~/.claude/docs/no-such-page.html#anything.\n")
    code, out = t.run(p)
    expect("a link to a page that does not exist is refused", code, out, 2,
           says=["holds no such page"])

    p = t.write("projects/-tmp-p/memory/topic-bad-anchor.md",
                "See ~/.claude/docs/pool-shape.html#never-decided.\n")
    code, out = t.run(p)
    expect("a link to a missing anchor in a real page is refused", code, out, 2,
           says=["carries no entry with that id"], absent=["holds no such page"])

    t.write("docs/sibling.html",
            decision('<h2 id="e">2026-03-04 a decision</h2>'
                     '<p>as in <a href="pool-shape.html#never-decided">the other page</a></p>'))
    code, out = t.run(os.path.join(t.root, "docs", "sibling.html"))
    expect("inside docs/, a relative link to a missing anchor is refused", code, out, 2,
           says=["carries no entry with that id"])

    t.write("docs/binary-note.md", b"\xff\xfe\x00# a decision", binary=True)
    code, out = t.run(os.path.join(t.root, "docs", "binary-note.md"))
    expect("markdown under docs/ is refused by name, before it is read",
           code, out, 2, says=["misfiled"], absent=["not readable as UTF-8"])

    t.write("docs/many-classes.html",
            '<html><body class="note decision-page wide"><h1>T</h1>'
            '<h2>2026-04-04 a decision with no id</h2></body></html>')
    code, out = t.run(os.path.join(t.root, "docs", "many-classes.html"))
    expect("the marker is found among other classes", code, out, 2,
           says=["carries no id"])

    t.write("docs/plain-view.html",
            view('<h2>First section</h2><p><a href="gone.html#nope">x</a></p>'))
    code, out = t.run(os.path.join(t.root, "docs", "plain-view.html"))
    expect("an undeclared view still has its links checked", code, out, 2,
           says=["holds no such page"], absent=["carries no id"])

    code, out = t.hook(os.path.join(t.root, "docs", "no-id.html"))
    expect("the stdin hook refuses with 2 and gives the reason", code, out, 2,
           says=["carries no id"])

    code, out = t.run(os.path.join(t.root, "docs", "pool-shape.html"),
                      os.path.join(t.root, "docs", "no-id.html"))
    expect("one bad file among good ones fails the whole run", code, out, 2,
           says=["ok, decision page", "carries no id"])


def main():
    t = Tree()
    try:
        allow_cases(t)
        refuse_cases(t)
    finally:
        t.drop()

    failed = [(n, d) for n, ok, d in RESULTS if not ok]
    for name, detail in failed:
        print("FAIL  %s\n      %s" % (name, detail))
    print("%d/%d cases pass" % (len(RESULTS) - len(failed), len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
