#!/usr/bin/env python3
"""Cases for `check-document-kind.py`, allow side first.

The script under test and the live `spec/document-kinds.md` are COPIED into a
temp tree and run there, because the script resolves `docs/` and its spec from
its own location: a suite pointed at the live checkout would read the real
pages. Copying the real spec, not a fixture, keeps the kind words the suite
sees the ones that ship.

Run: python3 hooks/check-document-kind-test.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check-document-kind.py")
SPEC = os.path.join(os.path.dirname(HERE), "spec", "document-kinds.md")


def page(body_attrs):
    return "<!doctype html><html><head><title>T</title></head><body%s><h1>T</h1></body></html>" % body_attrs


class Tree(object):
    """A temp checkout holding the script, its spec, and a `docs/`."""

    def __init__(self, spec=True):
        self.root = tempfile.mkdtemp(prefix="document-kind-")
        for d in ("hooks", "docs", "spec"):
            os.makedirs(os.path.join(self.root, d))
        self.script = os.path.join(self.root, "hooks", "check-document-kind.py")
        shutil.copy(SCRIPT, self.script)
        if spec:
            shutil.copy(SPEC, os.path.join(self.root, "spec", "document-kinds.md"))

    def write(self, relative, text, binary=False):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb" if binary else "w") as handle:
            handle.write(text)
        return path

    def run(self, *paths):
        done = subprocess.run([sys.executable, self.script] + list(paths),
                              capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    def hook(self, path):
        done = subprocess.run([sys.executable, self.script],
                              input=json.dumps({"tool_input": {"file_path": path}}),
                              capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    def drop(self):
        shutil.rmtree(self.root, ignore_errors=True)


RESULTS = []


def expect(name, got_code, got_text, code, says=(), absent=()):
    """One case: the exit status AND what the run said, since a crash and a
    refusal can share a status."""
    problems = []
    if got_code != code:
        problems.append("exit %d, wanted %d" % (got_code, code))
    problems += ["said nothing about %r" % p for p in says if p not in got_text]
    problems += ["wrongly diagnosed %r" % p for p in absent if p in got_text]
    RESULTS.append((name, not problems,
                    "; ".join(problems) + (" || " + got_text.strip()[:200] if problems else "")))


def allow_cases(t):
    for kind in ("doc", "view", "dashboard", "ui"):
        p = t.write("docs/%s.html" % kind, page(' class="%s"' % kind))
        code, out = t.run(p)
        expect("a page declaring %s is accepted" % kind, code, out, 0, says=["ok, kind %s" % kind])

    p = t.write("docs/decision.html", page(' class="doc decision-page"'))
    code, out = t.run(p)
    expect("a decision page declaring doc is accepted", code, out, 0, says=["ok, kind doc"])

    p = t.write("docs/attr.html", page(' data-x="a > b" class="wide view"'))
    code, out = t.run(p)
    expect("a `>` inside another attribute does not end the tag", code, out, 0,
           says=["ok, kind view"])

    p = t.write("docs/INDEX.md", "- a page\n")
    code, out = t.run(p)
    expect("markdown under docs/ is not this hook's", code, out, 0, says=["skipped, not an .html"])

    outside = tempfile.mkdtemp(prefix="document-kind-outside-")
    stray = os.path.join(outside, "page.html")
    with open(stray, "w") as handle:
        handle.write(page(""))
    code, out = t.run(stray)
    expect("an .html outside docs/ is skipped, and says so", code, out, 0,
           says=["skipped, not an .html under"], absent=["no kind word"])
    shutil.rmtree(outside, ignore_errors=True)

    code, out = t.run(os.path.join(t.root, "docs", "never-written.html"))
    expect("a path that does not exist is skipped", code, out, 0, says=["skipped, no such file"])

    p = t.write("docs/blob.html", b"\xff\xfe\x00", binary=True)
    code, out = t.run(p)
    expect("a page that is not UTF-8 is skipped", code, out, 0, says=["not readable as UTF-8"])

    code, out = t.hook(os.path.join(t.root, "docs", "view.html"))
    expect("the stdin hook lets a declared page through", code, out, 0)

    done = subprocess.run([sys.executable, t.script], input="not json",
                          capture_output=True, text=True)
    expect("an unparseable payload is not an error", done.returncode,
           done.stdout + done.stderr, 0)

    bare = Tree(spec=False)
    code, out = bare.run(bare.write("notes.md", "hi\n"))
    expect("with no spec, a path out of scope is still just skipped", code, out, 0,
           says=["skipped"], absent=["could not read"])
    bare.drop()


def refuse_cases(t):
    p = t.write("docs/bare.html", page(""))
    code, out = t.run(p)
    expect("a page with no class is refused", code, out, 2,
           says=["carries no kind word", "doc", "dashboard"], absent=["more than one"])

    p = t.write("docs/other.html", page(' class="decision-page"'))
    code, out = t.run(p)
    expect("a class that is no kind word is refused", code, out, 2,
           says=["carries no kind word", "'decision-page'"])

    p = t.write("docs/near.html", page(' class="my-view"'))
    code, out = t.run(p)
    expect("a kind word must be a whole class, not a substring", code, out, 2,
           says=["carries no kind word"])

    p = t.write("docs/two.html", page(' class="view dashboard"'))
    code, out = t.run(p)
    expect("a page declaring two kinds is refused", code, out, 2,
           says=["more than one kind", "view and dashboard"], absent=["no kind word"])

    p = t.write("docs/commented.html",
                '<html><!-- <body class="view"> --><body><h1>T</h1></body></html>')
    code, out = t.run(p)
    expect("a kind in commented-out markup is not declared", code, out, 2,
           says=["carries no kind word"])

    p = t.write("docs/nobody.html", "<html><h1>T</h1></html>")
    code, out = t.run(p)
    expect("a page with no <body> is refused and says so", code, out, 2, says=["no <body>"])

    code, out = t.hook(os.path.join(t.root, "docs", "two.html"))
    expect("the stdin hook refuses with 2 and gives the reason", code, out, 2,
           says=["more than one kind"])

    code, out = t.run(os.path.join(t.root, "docs", "view.html"),
                      os.path.join(t.root, "docs", "bare.html"))
    expect("one bad page among good ones fails the run", code, out, 2,
           says=["ok, kind view", "carries no kind word"])

    wider = Tree()
    with open(os.path.join(wider.root, "spec", "document-kinds.md"), "a") as handle:
        handle.write("\n## Other\n\n| word | x |\n| --- | --- |\n| `chart` | not a kind |\n")
    p = wider.write("docs/chart.html", page(' class="chart"'))
    code, out = wider.run(p)
    expect("only the § Kinds table declares kind words", code, out, 2,
           says=["carries no kind word"], absent=["ok, kind chart"])
    wider.drop()

    bare = Tree(spec=False)
    p = bare.write("docs/view.html", page(' class="view"'))
    code, out = bare.run(p)
    expect("with no spec, a page in scope is not judged, and says why", code, out, 1,
           says=["could not read the kind words"], absent=["carries no kind word"])
    bare.drop()


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
