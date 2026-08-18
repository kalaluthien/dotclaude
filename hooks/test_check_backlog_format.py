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


def item(marker=" ", tags="#code", title="**[PARSER] A short title.**", fields=None):
    """One row in the live labeled-fields form: a head line and field bullets."""
    if fields is None:
        fields = {"what": "The work.", "why": "The reason.", "how": "The next step."}
    head = "- [%s] 2026-08-12 %s %s\n" % (marker, tags, title)
    return head + "".join("  - %s: %s\n" % (label, text) for label, text in fields.items())


def prose_item(text, marker=" ", tags="#code", title="**[PARSER] A short title.**"):
    """One row in the older whole-body form, for a contract that declares it."""
    return "- [%s] 2026-08-12 %s %s %s\n" % (marker, tags, title, text)


def prose_body(max_chars=300):
    """A patch putting the contract back on a single folded body budget."""

    def patch(data):
        data["item"]["body"] = {"max_chars": max_chars}

    return patch


class TheLiveContract(Fixtures):
    def test_declares_the_field_bound_the_writing_rule_names(self):
        self.assertEqual(hook.contract(CONTRACT_DOCUMENT)["field_max"], 160)

    def test_requires_the_group_label(self):
        self.assertTrue(hook.contract(CONTRACT_DOCUMENT)["label"]["required"])

    def test_moves_that_bound_with_the_rows_difficulty(self):
        """The numbers the writing rule names, read off the kinds that carry
        them rather than off a list kept here."""
        self.assertEqual(
            hook.contract(CONTRACT_DOCUMENT)["field_max_by_tag"],
            {"easy": 120, "hard": 200},
        )


class TheBudget(Fixtures):
    """The folded whole-body budget, for a contract that declares one."""

    def test_a_body_within_budget_passes(self):
        self.assertEqual(self.reasons(prose_item("A" * 300), prose_body()), [])

    def test_a_body_over_budget_is_refused_by_the_budget_check(self):
        found = self.reasons(prose_item("A" * 301), prose_body())
        self.assertEqual(len(found), 1)
        self.assertIn("301 characters, over the 300-character budget", found[0])

    def test_wrapping_a_row_buys_it_no_room(self):
        """Continuation lines are the same body, so the count folds them in."""
        wrapped = prose_item("A" * 100) + "  " + "B" * 100 + "\n  " + "C" * 100 + "\n"
        found = self.reasons(wrapped, prose_body())
        self.assertEqual(len(found), 1)
        self.assertIn("302 characters", found[0])

    def test_the_same_text_split_under_the_budget_passes(self):
        wrapped = prose_item("A" * 100) + "  " + "B" * 100 + "\n  " + "C" * 97 + "\n"
        self.assertEqual(self.reasons(wrapped, prose_body()), [])

    def test_the_title_itself_is_not_counted(self):
        long_title = "**[PARSER] %s.**" % ("T" * 400)
        self.assertEqual(
            self.reasons(prose_item("A" * 200, title=long_title), prose_body()), []
        )

    def test_a_prose_section_bullet_is_not_measured(self):
        body = "## Horizon (dots noted)\n\n- " + "A" * 500 + "\n"
        self.assertEqual(self.reasons(body, prose_body()), [])

    def test_a_fenced_specimen_is_not_measured(self):
        body = "```\n" + prose_item("A" * 500) + "```\n"
        self.assertEqual(self.reasons(body, prose_body()), [])

    def test_a_contract_without_the_key_measures_nothing(self):
        def drop(data):
            del data["item"]["body"]

        self.assertEqual(self.reasons(prose_item("A" * 900), drop), [])

    def test_a_budget_that_is_not_a_positive_number_is_a_contract_error(self):
        for bad in ("300", 0, -1, True, None):
            with self.assertRaises(hook.ContractError) as caught:
                self.rule(prose_body(bad))
            self.assertIn("item.body.max_chars", str(caught.exception))


class TheFields(Fixtures):
    """The labeled-fields body the live contract declares."""

    def test_a_row_with_the_required_fields_passes(self):
        self.assertEqual(self.reasons(item()), [])

    def test_a_row_missing_a_required_field_is_refused(self):
        found = self.reasons(item(fields={"what": "The work."}))
        self.assertEqual(len(found), 1)
        self.assertIn("missing required field(s): 'why:', 'how:'", found[0])

    def test_a_field_over_its_bound_is_refused(self):
        found = self.reasons(
            item(fields={"what": "A" * 161, "why": "The reason.", "how": "The step."})
        )
        self.assertEqual(len(found), 1)
        self.assertIn("161 characters, over the 160-character bound", found[0])


def graded(easy=120, hard=200):
    """A patch giving the two difficulty kinds their own field bounds.

    Written as a patch on the live contract, like every fixture here, so the
    numbers under test are the shape the pools use and not a second copy.
    """

    def patch(data):
        for kind in data["item"]["tags"]["kinds"]:
            if kind["tag"] == "easy":
                kind["field_max_chars"] = easy
            elif kind["tag"] == "hard":
                kind["field_max_chars"] = hard

    return patch


class TheFieldBoundPerRow(Fixtures):
    """The bound a row is measured against, which its own tags may move."""

    def field(self, length, tags):
        return item(
            tags=tags,
            fields={"what": "A" * length, "why": "The reason.", "how": "The step."},
        )

    def test_a_hard_row_may_be_written_wider_than_the_body_wide_bound(self):
        self.assertEqual(self.reasons(self.field(200, "#hard #code"), graded()), [])

    def test_the_same_row_without_the_hard_tag_is_refused(self):
        """The pair that proves the tag is what moved the bound."""
        found = self.reasons(self.field(200, "#code"), graded())
        self.assertEqual(len(found), 1)
        self.assertIn("200 characters, over the 160-character bound", found[0])

    def test_a_hard_row_past_its_own_wider_bound_is_still_refused(self):
        found = self.reasons(self.field(201, "#hard #code"), graded())
        self.assertEqual(len(found), 1)
        self.assertIn("201 characters, over the 200-character bound", found[0])

    def test_an_easy_row_is_held_to_less_than_the_body_wide_bound(self):
        found = self.reasons(self.field(121, "#easy #code"), graded())
        self.assertEqual(len(found), 1)
        self.assertIn("121 characters, over the 120-character bound", found[0])
        self.assertEqual(self.reasons(self.field(120, "#easy #code"), graded()), [])

    def test_two_difficulty_claims_on_one_row_resolve_to_the_widest(self):
        """The tie-break the effort rule already makes, for the same reason:
        the bounds move with difficulty, so the widest is what the hardest
        claim on the row asked for."""
        self.assertEqual(
            self.reasons(self.field(200, "#easy #hard #code"), graded()), []
        )

    def test_a_row_wearing_no_difficulty_falls_to_the_body_wide_bound(self):
        self.assertEqual(self.reasons(self.field(160, "#code"), graded()), [])
        found = self.reasons(self.field(161, "#code"), graded())
        self.assertIn("over the 160-character bound", found[0])

    def test_a_contract_whose_kinds_bound_nothing_measures_every_row_alike(self):
        """The shape the pools had before the key, and the one a pool that
        never declares it keeps."""

        def drop(data):
            for kind in data["item"]["tags"]["kinds"]:
                kind.pop("field_max_chars", None)

        self.assertEqual(self.reasons(self.field(160, "#hard #code"), drop), [])
        found = self.reasons(self.field(161, "#hard #code"), drop)
        self.assertIn("over the 160-character bound", found[0])

    def test_a_kinds_bound_that_is_not_a_positive_number_is_a_contract_error(self):
        for bad in ("200", 0, -1, True, None):
            with self.assertRaises(hook.ContractError) as caught:
                self.rule(graded(hard=bad))
            self.assertIn("field_max_chars", str(caught.exception))


class TheLabel(Fixtures):
    """The bracketed label leading the bold title, which is what groups rows."""

    def test_a_labelled_row_passes(self):
        self.assertEqual(self.reasons(item(title="**[PARSER] A short title.**")), [])

    def test_a_run_of_leading_labels_passes(self):
        """A row may lead with more than one; the first is the group it joins."""
        self.assertEqual(
            self.reasons(item(title="**[PARSER] [HOOKS] A short title.**")), []
        )

    def test_a_row_without_a_label_is_refused_by_the_label_check(self):
        found = self.reasons(item(title="**A short title.**"))
        self.assertEqual(len(found), 1)
        self.assertIn("must open with a bracketed label", found[0])

    def test_a_bracket_later_in_the_title_is_refused_by_the_label_check(self):
        found = self.reasons(item(title="**[PARSER] A [plus] bullet is swallowed.**"))
        self.assertEqual(len(found), 1)
        self.assertIn("only the run leading the title is a label", found[0])

    def test_a_bracket_in_the_body_is_left_alone(self):
        """The rule is about the title; a field may quote whatever it needs."""
        self.assertEqual(
            self.reasons(
                item(
                    fields={
                        "what": "Fix [x] input.",
                        "why": "It breaks.",
                        "how": "Patch it.",
                    }
                )
            ),
            [],
        )

    def test_a_contract_that_does_not_require_one_allows_an_unlabelled_row(self):
        def optional(data):
            data["item"]["label"]["required"] = False

        self.assertEqual(self.reasons(item(title="**A short title.**"), optional), [])

    def test_a_contract_without_the_key_asks_for_no_label(self):
        def drop(data):
            del data["item"]["label"]

        self.assertEqual(self.reasons(item(title="**A [short] title.**"), drop), [])

    def test_a_label_rule_this_hook_cannot_compile_is_a_contract_error(self):
        for key, bad in (("position", "anywhere"), ("spelling", "in-braces")):
            def patch(data, key=key, bad=bad):
                data["item"]["label"][key] = bad

            with self.assertRaises(hook.ContractError) as caught:
                self.rule(patch)
            self.assertIn("item.label.%s" % key, str(caught.exception))

    def test_the_refusal_names_the_form_the_label_belongs_to(self):
        self.assertIn("**[LABEL] Title.**", self.rule()["form"])


class TheGrammar(Fixtures):
    """The rules that stood before the label, over the same row reader."""

    def test_a_well_formed_row_passes(self):
        self.assertEqual(self.reasons(item()), [])

    def test_a_row_without_a_scope_tag_is_refused(self):
        found = self.reasons(item(tags="#need-you"))
        self.assertEqual(len(found), 1)
        self.assertIn("needs at least one scope tag", found[0])

    def test_a_row_without_a_bold_title_is_refused(self):
        found = self.reasons(item(title="[PARSER] A plain title."))
        self.assertEqual(len(found), 1)
        self.assertIn("expected", found[0])

    def test_one_row_can_break_two_rules_at_once(self):
        found = self.reasons(item(tags="#need-you", title="**A short title.**"))
        self.assertEqual(len(found), 2)


class TheEntryPoints(Fixtures):
    def test_the_report_counts_items_not_reasons(self):
        rule = self.rule()
        path = self.board(item(tags="#need-you", title="**A short title.**"))
        found = hook.violations(path, rule)
        self.assertIn("1 backlog item(s)", hook.report(path, found, rule))


if __name__ == "__main__":
    unittest.main(verbosity=2)
