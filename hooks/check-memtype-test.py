#!/usr/bin/env python3
"""Prove the widened pool check refuses what Filing refuses and allows the rest,
through the script settings.json actually runs.

Every case copies the shipped `check-memtype.py` and the shipped `CLAUDE.md`
into a temporary tree and runs the copy, so what is under test is the file that
gets installed and the table a reader would actually read. The allow half is
the load-bearing one: this hook is registered machine-wide on every `Write` and
`Edit`, so a false refusal stops every session at once, while a missed one is
caught by the next sweep. The last case replays every real pool file on this
machine for that reason.

Both entry points are exercised. The harness calls this hook with a JSON
payload on stdin and reads its exit code, so the cases that matter run that way
rather than through argv alone.

Usage: hooks/check-memtype-test.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOK = HERE / "check-memtype.py"
DOCUMENT = HERE.parent / "CLAUDE.md"

ran, fails = [], []


def check(name, ok, detail=""):
    ran.append(name)
    if not ok:
        fails.append("%s\n      %s" % (name, detail))


def tree(root, table=None):
    """A temporary copy of the shipped hook, its document, and an empty pool."""
    root = Path(root)
    (root / "hooks").mkdir()
    shutil.copy(HOOK, root / "hooks" / "check-memtype.py")
    (root / "CLAUDE.md").write_text(
        DOCUMENT.read_text(encoding="utf-8") if table is None else table,
        encoding="utf-8",
    )
    pool = root / "project" / "memory"
    pool.mkdir(parents=True)
    return root / "hooks" / "check-memtype.py", pool


def memory(pool, name, body="", type_=None, index=True, title=None):
    """One pool file, and its index line unless the case is about its absence."""
    lines = ["---", "name: %s" % name, "description: a fixture."]
    if type_ is not None:
        lines += ["metadata:", "  type: %s" % type_]
    lines += ["---", "", body or "Body."]
    path = pool / ("%s.md" % name)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if index:
        with open(pool / "MEMORY.md", "a", encoding="utf-8") as handle:
            handle.write("- [%s](%s.md) - a fixture.\n" % (title or name, name))
    return path


def cli(hook, *paths):
    return subprocess.run(
        [sys.executable, str(hook)] + [str(p) for p in paths],
        capture_output=True, text=True)


def posttooluse(hook, path):
    """The hook as the harness runs it: the tool payload on stdin."""
    return subprocess.run(
        [sys.executable, str(hook)], input=json.dumps(
            {"tool_name": "Write", "tool_input": {"file_path": str(path)}}),
        capture_output=True, text=True)


def said(result):
    return (result.stdout or "") + (result.stderr or "")


def main():
    # ---- allow: every name the table carries today still passes, and so does
    # the one the rename adds. A widening that dropped one would strand a pool.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        today = {
            "history-shape": "episodic",
            "topic-layout": "semantic",
            "feedback-sizing": "procedural",
            "setup-herdr": "procedural",
            "pitfalls": "procedural",
            "pitfall-alloy": "procedural",
        }
        for name, kind in today.items():
            path = memory(pool, name, type_=kind)
            r = posttooluse(hook, path)
            check("allowed: '%s' declaring '%s'" % (name, kind),
                  r.returncode == 0 and not said(r).strip(),
                  "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow: the widening proper. The target frontmatter is `name` and
    # `description` alone, so a file declaring no type is the new shape, not a
    # drift; a file with no frontmatter at all is the same absence.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        for name, note in (("topic-alloy", "no metadata.type"),
                           ("pitfall-alloy", "no metadata.type"),
                           ("feedback-sizing", "no metadata.type")):
            path = memory(pool, name)
            r = posttooluse(hook, path)
            check("allowed: '%s' with %s" % (name, note), r.returncode == 0,
                  "exit %d: %s" % (r.returncode, said(r)[:300]))
        bare = pool / "topic-bare.md"
        bare.write_text("No frontmatter at all.\n", encoding="utf-8")
        (pool / "MEMORY.md").write_text(
            (pool / "MEMORY.md").read_text() + "- [bare](topic-bare.md) - x.\n")
        r = posttooluse(hook, bare)
        check("allowed: a file with no frontmatter block at all",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow: what is not a memory. The index is not one of its own
    # entries, and a Markdown file outside a pool is nobody's business here.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        memory(pool, "topic-alloy", type_="semantic")
        r = posttooluse(hook, pool / "MEMORY.md")
        check("allowed: MEMORY.md itself, which no line indexes",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))
        outside = Path(d) / "notes.md"
        outside.write_text("Not a pool file.\n")
        r = posttooluse(hook, outside)
        check("allowed: a Markdown file outside any pool",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow: the index line is a person's sentence, so only its link is
    # read. A title unlike the name and space inside the parentheses pass.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        path = memory(pool, "topic-alloy", type_="semantic", index=False)
        (pool / "MEMORY.md").write_text(
            "# Memory index\n\n- [Alloy, and its module system]( topic-alloy.md )"
            " — read before writing a model.\n", encoding="utf-8")
        r = posttooluse(hook, path)
        check("allowed: an index line whose title differs and whose link is spaced",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: no index line. The harness loads the index and never a
    # memory, so this is the file nobody can reach.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        memory(pool, "topic-alloy", type_="semantic")
        orphan = memory(pool, "topic-lost", type_="semantic", index=False)
        r = posttooluse(hook, orphan)
        check("refused: a pool file the index does not link to",
              r.returncode == 2 and "topic-lost.md" in said(r)
              and "carries no line linking" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: the file is named in the index only by a neighbour's prose,
    # which is what a split leaves behind. Only the link is a reader's route,
    # so a mention passes a substring test and must not pass this one.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        memory(pool, "topic-alloy-modules", type_="semantic", index=False)
        short = memory(pool, "topic-alloy", type_="semantic", index=False)
        (pool / "MEMORY.md").write_text(
            "- [Alloy modules](topic-alloy-modules.md) — split out of "
            "topic-alloy.md, which the index no longer links.\n",
            encoding="utf-8")
        r = posttooluse(hook, short)
        check("refused: a file the index only mentions in another line's prose",
              r.returncode == 2 and "carries no line linking" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        r = posttooluse(hook, pool / "topic-alloy-modules.md")
        check("allowed: the neighbour that line actually links to",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: the pool has no index at all. Distinguished in words from
    # the case above, because one is a pool nobody indexed and the other is one
    # file that was never added.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        path = memory(pool, "topic-alloy", type_="semantic", index=False)
        r = posttooluse(hook, path)
        check("refused: a pool with no MEMORY.md, said as 'no readable'",
              r.returncode == 2 and "no readable MEMORY.md" in said(r)
              and "carries no line linking" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: the checks the widening keeps. A name outside the table, and
    # a declared type contradicting its row.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        stray = memory(pool, "notes-alloy", type_="semantic")
        r = posttooluse(hook, stray)
        check("refused: a name matching no row of the table",
              r.returncode == 2 and "matches no row" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        drifted = memory(pool, "topic-drift", type_="procedural")
        r = posttooluse(hook, drifted)
        check("refused: metadata.type contradicting its row",
              r.returncode == 2 and "metadata.type is 'procedural'" in said(r)
              and "semantic" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: a document with no table. This hook has no fallback copy, so
    # an unreadable declaration is a refusal and says which document it read.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d, table="# CLAUDE\n\nNo table here.\n")
        path = memory(pool, "topic-alloy", type_="semantic")
        r = posttooluse(hook, path)
        check("refused: a document carrying no memtype table",
              r.returncode == 2 and "no memtype table" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow, replayed: every real pool file on this machine, against the
    # shipped document. A widening that refuses one of these stops every
    # session that writes a memory.
    corpus = sorted(
        p for pool in Path.home().glob(".claude/projects/*/memory")
        for p in pool.glob("*.md") if p.name != "MEMORY.md")
    r = cli(HOOK, *corpus) if corpus else None
    check("allowed: every real pool file on this machine (%d)" % len(corpus),
          bool(corpus) and r.returncode == 0
          and r.stdout.count(": ok") == len(corpus),
          "no pool files found" if not corpus else
          "exit %d, %d of %d ok: %s" % (
              r.returncode, r.stdout.count(": ok"), len(corpus),
              (r.stderr or r.stdout)[:400]))

    if not ran:
        print("FAIL  the suite ran no case at all")
        return 1
    for x in fails:
        print("FAIL  %s" % x)
    print("%d/%d cases pass" % (len(ran) - len(fails), len(ran)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
