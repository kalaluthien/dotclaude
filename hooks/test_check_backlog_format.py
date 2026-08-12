#!/usr/bin/env python3
"""Tests for check-backlog-format.py, the pool board file guard.

Run: python3 ~/.claude/hooks/test_check_backlog_format.py

Every fixture contract is the live one from ~/.claude/CLAUDE.md with one key
patched, so a test cannot pass against a grammar the pools do not use. Each
refusal test reads the reason the checker gave, not the exit code alone, and
each is paired with a row the same rule must allow.
"""

import copy
import importlib.util
import json
import os
import re
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "check-backlog-format.py")
CONTRACT_DOCUMENT = os.path.join(os.path.dirname(HERE), "CLAUDE.md")

_spec = importlib.util.spec_from_file_location("check_backlog_format", HOOK)
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)

BLOCK = re.compile(
    r"^```json[ \t]+contract=pool[ \t]*\n(.*?)\n```[ \t]*$", re.MULTILINE | re.DOTALL
)

FRONT_MATTER = """---
name: backlog
description: "A pool board file."
metadata:
  type: semantic
---

## Work

"""


def live_contract():
    with open(CONTRACT_DOCUMENT, encoding="utf-8") as handle:
        return json.loads(BLOCK.search(handle.read()).group(1))


class Fixtures(unittest.TestCase):
    """A temporary contract document and board file per test."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

    def rule(self, patch=None):
        """The live contract, optionally patched, compiled by the hook."""
        data = copy.deepcopy(live_contract())
        if patch is not None:
            patch(data)
        path = os.path.join(self.directory.name, "CLAUDE.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("```json contract=pool\n%s\n```\n" % json.dumps(data, indent=2))
        return hook.contract(path)

    def board(self, body):
        path = os.path.join(self.directory.name, "backlog.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(FRONT_MATTER + body)
        return path

    def reasons(self, body, patch=None):
        return [reason for _, _, reason in hook.violations(self.board(body), self.rule(patch))]


def item(text, marker=" ", tags="#code", title="**A short title.**"):
    return "- [%s] 2026-08-12 %s %s %s\n" % (marker, tags, title, text)


class TheLiveContract(Fixtures):
    def test_declares_the_budget_the_writing_rule_names(self):
        self.assertEqual(hook.contract(CONTRACT_DOCUMENT)["body_max"], 300)


class TheBudget(Fixtures):
    def test_a_body_within_budget_passes(self):
        self.assertEqual(self.reasons(item("A" * 300)), [])

    def test_a_body_over_budget_is_refused_by_the_budget_check(self):
        found = self.reasons(item("A" * 301))
        self.assertEqual(len(found), 1)
        self.assertIn("301 characters, over the 300-character budget", found[0])

    def test_wrapping_a_row_buys_it_no_room(self):
        """Continuation lines are the same body, so the count folds them in."""
        wrapped = item("A" * 100) + "  " + "B" * 100 + "\n  " + "C" * 100 + "\n"
        found = self.reasons(wrapped)
        self.assertEqual(len(found), 1)
        self.assertIn("302 characters", found[0])

    def test_the_same_text_split_under_the_budget_passes(self):
        wrapped = item("A" * 100) + "  " + "B" * 100 + "\n  " + "C" * 97 + "\n"
        self.assertEqual(self.reasons(wrapped), [])

    def test_the_title_itself_is_not_counted(self):
        long_title = "**%s.**" % ("T" * 400)
        self.assertEqual(self.reasons(item("A" * 200, title=long_title)), [])

    def test_a_prose_section_bullet_is_not_measured(self):
        body = "## Horizon (dots noted)\n\n- " + "A" * 500 + "\n"
        self.assertEqual(self.reasons(body), [])

    def test_a_fenced_specimen_is_not_measured(self):
        body = "```\n" + item("A" * 500) + "```\n"
        self.assertEqual(self.reasons(body), [])

    def test_a_contract_without_the_key_measures_nothing(self):
        def drop(data):
            del data["item"]["body"]

        self.assertEqual(self.reasons(item("A" * 900), drop), [])

    def test_a_budget_that_is_not_a_positive_number_is_a_contract_error(self):
        for bad in ("300", 0, -1, True, None):
            def patch(data, bad=bad):
                data["item"]["body"] = {"max_chars": bad}

            with self.assertRaises(hook.ContractError) as caught:
                self.rule(patch)
            self.assertIn("item.body.max_chars", str(caught.exception))


class TheGrammar(Fixtures):
    """The rules that stood before the budget, over the rewritten row reader."""

    def test_a_well_formed_row_passes(self):
        self.assertEqual(self.reasons(item("Short body.")), [])

    def test_a_row_without_a_scope_tag_is_refused(self):
        found = self.reasons(item("Short body.", tags="#need-you"))
        self.assertEqual(len(found), 1)
        self.assertIn("needs at least one scope tag", found[0])

    def test_a_row_without_a_bold_title_is_refused(self):
        found = self.reasons(item("Short body.", title="A plain title."))
        self.assertEqual(len(found), 1)
        self.assertIn("expected", found[0])

    def test_one_row_can_break_two_rules_at_once(self):
        found = self.reasons(item("A" * 400, tags="#need-you"))
        self.assertEqual(len(found), 2)


class TheEntryPoints(Fixtures):
    def test_the_report_counts_items_not_reasons(self):
        rule = self.rule()
        path = self.board(item("A" * 400, tags="#need-you"))
        found = hook.violations(path, rule)
        self.assertIn("1 backlog item(s)", hook.report(path, found, rule))


if __name__ == "__main__":
    unittest.main(verbosity=2)
