#!/usr/bin/env python3
"""Prove the narrowed pool check refuses what Filing refuses and allows the rest,
through the script settings.json actually runs.

Every case copies the shipped `check-memtype.py` and the shipped `CLAUDE.md`
into a temporary tree and runs the copy, so what is under test is the file that
gets installed and the prefix list a reader would actually read. The allow half is
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
import re
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


def tree(root, document=None):
    """A temporary copy of the shipped hook, its document, and an empty pool."""
    root = Path(root)
    (root / "hooks").mkdir()
    shutil.copy(HOOK, root / "hooks" / "check-memtype.py")
    (root / "CLAUDE.md").write_text(
        DOCUMENT.read_text(encoding="utf-8") if document is None else document,
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


def target_prefixes():
    """The prefixes § Filing declares, read out of the document independently.

    Deliberately not the hook's own parser: this reads the bullets the way a
    person does, so a hook that quietly stopped seeing one of them, or saw one
    the document does not list, fails here rather than passing itself.
    """
    text = DOCUMENT.read_text(encoding="utf-8")
    after = text.split("memory prefixes are:", 1)
    if len(after) < 2:
        return []
    found = []
    for line in after[1].split("\n"):
        item = re.match(r"^[-*+][ \t]+`([a-z]+-)<subject>`", line)
        if item:
            found.append(item.group(1))
        elif found and line.strip():
            break
    return found


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
    # ---- allow: a memory under each prefix the document declares, in the
    # target shape -- `name` and `description` and no declaration at all. The
    # bullets are the only statement of the rule, so this is their second
    # reader: a hook that stopped seeing one of them strands a whole prefix.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        prefixes = target_prefixes()
        check("the document declares 4 memory prefixes (raise this count when "
              "the scheme gains one)", len(prefixes) == 4,
              "read %r from the bullets after 'memory prefixes are:'" % (prefixes,))
        check("the four are topic-, pitfall-, feedback- and archive-",
              sorted(prefixes) == ["archive-", "feedback-", "pitfall-", "topic-"],
              "read %r" % (prefixes,))
        for prefix in prefixes:
            path = memory(pool, "%sprobe" % prefix)
            r = posttooluse(hook, path)
            check("allowed: '%sprobe', a prefix the document declares" % prefix,
                  r.returncode == 0 and not said(r).strip(),
                  "exit %d: %s" % (r.returncode, said(r)[:300]))
        # `archive-` is the fourth, added when the writing skill and the
        # debugger agent were retired: what a deleted thing knew has to land
        # where a rebuild will read it. Named on its own, because the loop
        # above is generated FROM the list -- delete the bullet and that loop
        # quietly runs one case fewer, while this one fails and says which.
        r = posttooluse(hook, memory(pool, "archive-writing-skill"))
        check("allowed: 'archive-writing-skill' -- § Filing declares "
              "`archive-<subject>` and the hook honours it",
              "archive-" in prefixes and r.returncode == 0
              and not said(r).strip(),
              "read %r; exit %d: %s" % (prefixes, r.returncode, said(r)[:300]))

    # ---- refuse: every name the scheme retired. Each is a real file shape
    # that lived in a pool, and each gets the same reason naming its successor.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        for name in ("history-shape", "setup-herdr", "pitfalls", "backlog"):
            path = memory(pool, name)
            r = posttooluse(hook, path)
            check("refused: '%s', a retired name" % name,
                  r.returncode == 2
                  and "opens with none of the memory prefixes" in said(r)
                  and "named after its reader" in said(r),
                  "exit %d: %s" % (r.returncode, said(r)[:300]))
        # `history-` is the one with nowhere in the pool to go, so its reason
        # has to name where it went instead.
        r = posttooluse(hook, pool / "history-shape.md")
        check("the refusal sends a `history-` file to the decision page",
              "decision page" in said(r) and "spec/decision-pages.md" in said(r),
              said(r)[:300])

    # ---- refuse: any `metadata.type`, not merely a contradicting one. Nothing
    # re-read the key after it was written, and the prefix now carries what it
    # claimed, so a declaration is a file that has not been migrated.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        for kind in ("semantic", "procedural", "episodic"):
            path = memory(pool, "topic-declares-%s" % kind, type_=kind)
            r = posttooluse(hook, path)
            check("refused: metadata.type '%s' on a well-named file" % kind,
                  r.returncode == 2 and "that key is retired" in said(r)
                  and "opens with none" not in said(r),
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
        memory(pool, "topic-alloy")
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
        path = memory(pool, "topic-alloy", index=False)
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
        memory(pool, "topic-alloy")
        orphan = memory(pool, "topic-lost", index=False)
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
        memory(pool, "topic-alloy-modules", index=False)
        short = memory(pool, "topic-alloy", index=False)
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
        path = memory(pool, "topic-alloy", index=False)
        r = posttooluse(hook, path)
        check("refused: a pool with no MEMORY.md, said as 'no readable'",
              r.returncode == 2 and "no readable MEMORY.md" in said(r)
              and "carries no line linking" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- the list has a start and an end, and neither is decorative. A
    # document holding a bullet of the same shape somewhere else must not
    # widen the set: read with no anchor, or with no terminator, the hook
    # accepts whatever that other bullet names, and nothing on the shipped
    # document would show it.
    with tempfile.TemporaryDirectory() as d:
        decoy = (
            "# CLAUDE\n\n"
            "Somewhere above:\n\n"
            "- `above-<subject>` — a bullet that is not the list.\n\n"
            "The three memory prefixes are:\n\n"
            "- `topic-<subject>` — a fact looked up.\n"
            "- `pitfall-<subject>` — a trap read when stuck.\n"
            "- `feedback-<subject>` — a rule the owner gave.\n\n"
            "Somewhere below:\n\n"
            "- `below-<subject>` — another bullet that is not the list.\n"
        )
        hook, pool = tree(d, document=decoy)
        r = posttooluse(hook, memory(pool, "topic-inside"))
        check("allowed: a prefix from the list itself, with decoys around it",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))
        for name, where in (("above-thing", "before the list"),
                            ("below-thing", "after the list")):
            r = posttooluse(hook, memory(pool, name))
            check("refused: a bullet of the same shape %s is not in the list"
                  % where,
                  r.returncode == 2
                  and "opens with none of the memory prefixes" in said(r),
                  "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: a document that announces the set twice. Taking the union
    # is how a list of the names being RETIRED widens what is accepted, and
    # the shipped document already names them in prose one edit away from
    # this shape. Two declarations is a contradiction, not a longer list.
    with tempfile.TemporaryDirectory() as d:
        twice = (
            "# CLAUDE\n\nThe three memory prefixes are:\n\n"
            "- `topic-<subject>` — a fact looked up.\n"
            "- `pitfall-<subject>` — a trap read when stuck.\n"
            "- `feedback-<subject>` — a rule the owner gave.\n\n"
            "That list is the whole rule.\n\n"
            "For the record, the retired memory prefixes are:\n\n"
            "- `setup-<subject>` — was `topic-` under its old name.\n"
            "- `history-<subject>` — has left the pool.\n"
        )
        hook, pool = tree(d, document=twice)
        r = posttooluse(hook, memory(pool, "setup-herdr"))
        check("refused: a second list does not widen the set",
              r.returncode == 2 and "a second time" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        r = posttooluse(hook, memory(pool, "topic-still-fine"))
        check("and the contradiction refuses a well-named file too, rather "
              "than answering from half the document",
              r.returncode == 2 and "a second time" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # The second announcement can be the very line that ends the first list,
    # with no prose between them. That line is a terminator AND a lead, and
    # reading it as only the first hides the contradiction entirely.
    with tempfile.TemporaryDirectory() as d:
        adjacent = (
            "# CLAUDE\n\nThe three memory prefixes are:\n\n"
            "- `topic-<subject>` — a fact looked up.\n"
            "- `pitfall-<subject>` — a trap read when stuck.\n"
            "- `feedback-<subject>` — a rule the owner gave.\n"
            "The retired memory prefixes are:\n\n"
            "- `setup-<subject>` — was `topic-` under its old name.\n"
        )
        hook, pool = tree(d, document=adjacent)
        r = posttooluse(hook, memory(pool, "topic-real"))
        check("refused: a line that both ends the list and announces a second",
              r.returncode == 2 and "a second time" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow: a FENCED declaration is an example being shown, not a second
    # one. Without the fence skip the mutant reads five prefixes here.
    with tempfile.TemporaryDirectory() as d:
        fenced = (
            "# CLAUDE\n\nThe three memory prefixes are:\n\n"
            "- `topic-<subject>` — a fact looked up.\n"
            "- `pitfall-<subject>` — a trap read when stuck.\n"
            "- `feedback-<subject>` — a rule the owner gave.\n\n"
            "How the list is written:\n\n```\n"
            "The three memory prefixes are:\n\n"
            "- `example-<subject>` — a sample.\n"
            "- `sample-<subject>` — another.\n"
            "```\n"
        )
        hook, pool = tree(d, document=fenced)
        r = posttooluse(hook, memory(pool, "topic-real"))
        check("allowed: a fenced example of the declaration is not a second one",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))
        r = posttooluse(hook, memory(pool, "example-thing"))
        check("refused: a prefix that appears only inside the fenced example",
              r.returncode == 2
              and "opens with none of the memory prefixes" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- the list is CONTIGUOUS. A later bullet of the same shape must not
    # join it, and none of these shapes announces itself, so the second-list
    # refusal above cannot be what catches them. The document names the
    # RETIRED prefixes a few lines below the real list, so every one of these
    # is one edit away on the shipped file.
    #
    # A bullet written straight into the list with no blank line is NOT here:
    # that is an edit to the declaration itself, and the document is what
    # declares. The hook is not the place to argue with it.
    LIST = ("# CLAUDE\n\nThe three memory prefixes are:\n\n"
            "- `topic-<subject>` — a fact looked up.\n"
            "- `pitfall-<subject>` — a trap read when stuck.\n"
            "- `feedback-<subject>` — a rule the owner gave.\n")
    for tail, note in (
            ("\n- `setup-<subject>` — retired.\n", "after a blank line"),
            # Glued to the list on both sides ON PURPOSE. With a blank line
            # before the fence the blank-line terminator has already closed
            # the list, and this case passes with the fence branch deleted.
            ("```\nan example\n```\n- `setup-<subject>` — retired.\n",
             "across a fence glued to the list"),
            ("  - `setup-<subject>` — retired.\n", "indented, with no blank line")):
        with tempfile.TemporaryDirectory() as d:
            hook, pool = tree(d, document=LIST + tail)
            r = posttooluse(hook, memory(pool, "setup-herdr"))
            check("refused: a stray bullet %s does not join the list" % note,
                  r.returncode == 2
                  and "opens with none of the memory prefixes" in said(r),
                  "exit %d: %s" % (r.returncode, said(r)[:300]))
            r = posttooluse(hook, memory(pool, "topic-fine"))
            check("and the list is still read, with a stray bullet %s" % note,
                  r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- the fence terminator has two effects and a firing condition, and a
    # case pins one each. It closes the list, which the stray-bullet case
    # above pins; it also marks the list CLOSED, so a second announcement past
    # the fence contradicts rather than reopening; and it waits for the list to
    # have a bullet, which the case after this one pins. Without the second
    # effect a retired list past the fence is collected, silently.
    with tempfile.TemporaryDirectory() as d:
        past_fence = (LIST + "```\nan example\n```\n"
                      "The retired memory prefixes are:\n"
                      "- `setup-<subject>` — retired.\n")
        hook, pool = tree(d, document=past_fence)
        r = posttooluse(hook, memory(pool, "topic-fine"))
        check("refused: a second announcement past a fence contradicts the "
              "first", r.returncode == 2
              and "announces the memory prefixes a second time" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- and the terminator only fires once the list HAS a bullet. A fence
    # between the lead and the first bullet is the document showing how the
    # list is written; ending the list there declares no prefix at all and
    # refuses every memory write on the machine.
    with tempfile.TemporaryDirectory() as d:
        fence_first = ("# CLAUDE\n\nThe three memory prefixes are:\n"
                       "```\n- `setup-<subject>` — how a bullet is written.\n```\n"
                       "- `topic-<subject>` — a fact looked up.\n"
                       "- `pitfall-<subject>` — a trap read when stuck.\n")
        hook, pool = tree(d, document=fence_first)
        r = posttooluse(hook, memory(pool, "pitfall-fine"))
        check("allowed: a fence before the first bullet does not end the list",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))
        r = posttooluse(hook, memory(pool, "setup-herdr"))
        check("refused: a prefix inside a fence before the first bullet",
              r.returncode == 2
              and "opens with none of the memory prefixes" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- the lead is anchored at END OF LINE, and that is what keeps the
    # phrase usable mid-sentence. The shipped document does not carry the
    # phrase mid-sentence today -- measured: the line naming the retired
    # prefixes in prose holds no `memory prefixes are:` at all -- so this
    # fixture's sentence is invented, and the hazard is one prose edit away
    # rather than present. Unanchored, that edit refuses every memory write.
    with tempfile.TemporaryDirectory() as d:
        inline = (LIST + "\nThe retired memory prefixes are: `setup-`, "
                  "`history-` and `pitfalls`.\n")
        hook, pool = tree(d, document=inline)
        r = posttooluse(hook, memory(pool, "topic-fine"))
        check("allowed: the lead phrase mid-sentence announces nothing",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow: prose that merely ENDS in those words declares nothing, so it
    # is not a second declaration either. Read as one, it refuses every memory
    # write on the machine -- the widest possible false refusal.
    with tempfile.TemporaryDirectory() as d:
        empty_lead = ("# CLAUDE\n\nA note on what the memory prefixes are:\n\n"
                      "they are named after their readers.\n\n" + LIST[len("# CLAUDE\n\n"):])
        hook, pool = tree(d, document=empty_lead)
        r = posttooluse(hook, memory(pool, "topic-fine"))
        check("allowed: an announcement that yields no bullets is not a "
              "declaration", r.returncode == 0,
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: a prefix nobody declared. Inventing one is a document that
    # was never updated, so the reason names the list rather than the file.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        stray = memory(pool, "notes-alloy")
        r = posttooluse(hook, stray)
        check("refused: a prefix the document does not declare",
              r.returncode == 2
              and "opens with none of the memory prefixes" in said(r)
              and "'topic-'" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: a link that is not the line's first element. A neighbour's
    # prose naming the file is what a split leaves behind, and it is not a
    # route to the file; a fenced example is being shown, not filed.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        buried = memory(pool, "topic-old", index=False)
        (pool / "MEMORY.md").write_text(
            "- [New](topic-new.md) - split out of [old](topic-old.md).\n",
            encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused: linked only from the middle of another entry's line",
              r.returncode == 2 and "carries no line linking" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        (pool / "MEMORY.md").write_text(
            "How to write one:\n\n```\n- [Old](topic-old.md) - a hook.\n```\n",
            encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused: linked only from inside a fenced example",
              r.returncode == 2 and "carries no line linking" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        # A fence nobody closed swallows the entry below it. Fail-closed is
        # right; calling it a missing entry sends the reader to the wrong edit.
        (pool / "MEMORY.md").write_text(
            "How to write one:\n\n```\n- [Old](topic-old.md)\n\n"
            "- [Old](topic-old.md) - a hook.\n", encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused: an unterminated fence, named as the fence and not as a "
              "missing entry", r.returncode == 2
              and "fence that is never closed" in said(r)
              and "carries no line linking" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        # The fence is the diagnosis only when the fence is what hid the entry.
        # Gated on the fence alone, it rewrites the reason for every miss in the
        # file -- so these two pin the branch's scope, where the case above pins
        # only its wording.
        (pool / "MEMORY.md").write_text(
            "- [Other](topic-other.md) - a hook.\n\n```\nan example\n",
            encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused as a missing entry, not as the fence, when a stray fence "
              "is open but did not hide it", r.returncode == 2
              and "carries no line linking" in said(r)
              and "fence that is never closed" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        (pool / "MEMORY.md").write_text(
            "- **[Old](topic-old.md)** - a hook.\n\n```\nan example\n",
            encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused with the shape named, not as the fence, when a stray "
              "fence is open", r.returncode == 2
              and "FIRST element is the link" in said(r)
              and "fence that is never closed" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        # The entry sits in a fence that was CLOSED on purpose, and an unrelated
        # fence is left open. Blaming the closed one on the open one is the same
        # misdiagnosis one step along, so only the tail the open fence ate counts.
        (pool / "MEMORY.md").write_text(
            "```\n- [Old](topic-old.md) - a hook.\n```\n\n"
            "- [Other](topic-other.md) - a hook.\n\n```\nan example\n",
            encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused as a missing entry when the entry sits in a fence that "
              "was closed and a different fence is open", r.returncode == 2
              and "carries no line linking" in said(r)
              and "fence that is never closed" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        # Closed, then reopened: the tail after the LAST opener is what was
        # eaten, so this one is the fence's fault.
        (pool / "MEMORY.md").write_text(
            "```\nan example\n```\n\n```\n- [Old](topic-old.md) - a hook.\n",
            encoding="utf-8")
        r = posttooluse(hook, buried)
        check("refused as the fence when a closed fence is reopened above the "
              "entry", r.returncode == 2
              and "fence that is never closed" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: the shapes the bullet anchor newly rejects. The message has
    # to name the shape, or a session reads "the line is missing" and appends a
    # second entry for a file the index already names.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        path = memory(pool, "topic-alloy", index=False)
        for line, note in (
                ("- **[Alloy](topic-alloy.md)** - a hook.", "the link inside bold"),
                ("| [Alloy](topic-alloy.md) | a hook |", "the link in a table cell"),
                ):
            (pool / "MEMORY.md").write_text(line + "\n", encoding="utf-8")
            r = posttooluse(hook, path)
            check("refused with the shape named: %s" % note,
                  r.returncode == 2 and "FIRST element is the link" in said(r)
                  and "a second line for the same file is not the fix" in said(r),
                  "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allowed, and accepted rather than left silent: an HTML comment is not
    # read, so a commented-out entry still counts. Reading them would put a
    # second Markdown parser in a hook, and nobody comments an entry out.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        path = memory(pool, "topic-alloy", index=False)
        (pool / "MEMORY.md").write_text(
            "<!--\n- [Alloy](topic-alloy.md) - retired.\n-->\n", encoding="utf-8")
        r = posttooluse(hook, path)
        check("allowed, accepted difference: an entry inside an HTML comment",
              r.returncode == 0, "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- allow: the link shapes a writer plausibly reaches for. A refusal
    # here stops a session that did nothing wrong.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        path = memory(pool, "topic-alloy", index=False)
        for line, note in (
                ("- [Alloy](./topic-alloy.md) - a hook.", "a './' prefix"),
                ("1. [Alloy](topic-alloy.md) - a hook.", "a numbered list"),
                ("1) [Alloy](topic-alloy.md) - a hook.", "a '1)' marker"),
                ("+ [Alloy](topic-alloy.md) - a hook.", "a '+' bullet"),
                ("- [Alloy](topic-alloy.md#modules) - a hook.", "an '#anchor'"),
                ("* [Alloy](topic-alloy.md) - a hook.", "a '*' bullet"),
                ("  - [Alloy]( topic-alloy.md ) - a hook.", "indented and spaced")):
            (pool / "MEMORY.md").write_text(line + "\n", encoding="utf-8")
            r = posttooluse(hook, path)
            check("allowed: an index line with %s" % note, r.returncode == 0,
                  "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: an index that cannot be decoded. PostToolUse treats exit 1
    # as non-blocking and shows it to the person, not to Claude, so a traceback
    # here is a pool that silently stops being checked.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        path = memory(pool, "topic-alloy", index=False)
        (pool / "MEMORY.md").write_bytes(
            b"- [Alloy](topic-alloy.md) - \xff\xfe not utf-8.\n")
        r = posttooluse(hook, path)
        check("refused: an index that is not valid UTF-8, with exit 2",
              r.returncode == 2 and "no readable MEMORY.md" in said(r)
              and "Traceback" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
        bad = pool / "topic-bytes.md"
        bad.write_bytes(b"---\nname: topic-bytes\n\xff\xfe\n---\n")
        (pool / "MEMORY.md").write_text(
            "- [Alloy](topic-alloy.md) - h.\n- [B](topic-bytes.md) - h.\n",
            encoding="utf-8")
        r = posttooluse(hook, bad)
        check("allowed: a memory that is not valid UTF-8, read as no frontmatter",
              r.returncode == 0 and "Traceback" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- refuse: a document this hook cannot compile. It keeps no fallback
    # copy of the table, so an unreadable declaration refuses with exit 2 and
    # says which document it read -- never a traceback, which exits 1 and is
    # non-blocking.
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d, document="# CLAUDE\n\nNo prefixes here.\n")
        path = memory(pool, "topic-alloy")
        r = posttooluse(hook, path)
        check("refused: a document declaring no memory prefixes",
              r.returncode == 2 and "no memory prefixes" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
    with tempfile.TemporaryDirectory() as d:
        hook, pool = tree(d)
        (Path(d) / "CLAUDE.md").write_bytes(b"# CLAUDE\n\n\xff\xfe\n")
        path = memory(pool, "topic-alloy")
        r = posttooluse(hook, path)
        check("refused: a document that is not valid UTF-8, with exit 2",
              r.returncode == 2 and "cannot be read" in said(r)
              and "Traceback" not in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))

    # ---- replayed: every real pool file on this machine, against the shipped
    # document. This is the load-bearing half -- a false refusal here stops
    # every session that writes a memory.
    #
    # A file still carrying a retired name is refused on purpose, so the case
    # cannot be "everything passes": it is every file with a target name
    # passing, and every file with a retired one refused FOR THAT REASON.
    # Written the other way round it would go green the day the last retired
    # file is migrated and also on the day the check stopped refusing.
    prefixes = tuple(target_prefixes())
    corpus = sorted(
        p for pool in Path.home().glob(".claude/projects/*/memory")
        for p in pool.glob("*.md") if p.name != "MEMORY.md")
    migrated = [p for p in corpus if p.stem.startswith(prefixes)]
    retired = [p for p in corpus if not p.stem.startswith(prefixes)]
    check("the machine holds pool files to replay", bool(corpus),
          "no pool files found under ~/.claude/projects/*/memory")
    if migrated:
        r = cli(HOOK, *migrated)
        check("allowed: every migrated pool file on this machine (%d of %d)"
              % (len(migrated), len(corpus)),
              r.returncode == 0 and r.stdout.count(": ok") == len(migrated),
              "exit %d, %d of %d ok: %s" % (
                  r.returncode, r.stdout.count(": ok"), len(migrated),
                  (r.stderr or r.stdout)[:400]))
    for path in retired:
        r = cli(HOOK, path)
        check("refused, and named as a retired name: %s/%s"
              % (path.parent.parent.name, path.name),
              r.returncode == 1
              and "opens with none of the memory prefixes" in said(r),
              "exit %d: %s" % (r.returncode, said(r)[:300]))
    check("the replay states its two sets (%d migrated, %d still retired)"
          % (len(migrated), len(retired)),
          len(migrated) + len(retired) == len(corpus),
          "%d + %d != %d" % (len(migrated), len(retired), len(corpus)))

    if not ran:
        print("FAIL  the suite ran no case at all")
        return 1
    for x in fails:
        print("FAIL  %s" % x)
    print("%d/%d cases pass" % (len(ran) - len(fails), len(ran)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
