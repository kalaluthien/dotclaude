#!/usr/bin/env python3
"""Test for reply-language.py: writes transcripts, feeds the hook its Stop JSON and checks it blocks or passes.
Run: python3 hooks/reply-language_test.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reply-language.py")


def user(content, **extra):
    return {"type": "user", "message": {"role": "user", "content": content}, **extra}


def said(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def tool_use():
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}}]}}


def tool_result(text):
    return user([{"type": "tool_result", "tool_use_id": "t1", "content": text}])


class ReplyLanguage(unittest.TestCase):
    def run_hook(self, entries=None, raw=None, **event):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "t.jsonl")
            with open(path, "w", encoding="utf-8") as f:
                f.write(raw if raw is not None else "".join(json.dumps(e) + "\n" for e in entries))
            stdin = json.dumps({"transcript_path": path, "stop_hook_active": False, **event})
            done = subprocess.run([sys.executable, SCRIPT], input=stdin, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def assert_blocks(self, out):
        verdict = json.loads(out)
        self.assertEqual(verdict["decision"], "block")
        self.assertIn("Rewrite", verdict["reason"])
        self.assertIn("Korean", verdict["reason"])

    def test_korean_message_english_reply_blocks(self):
        self.assert_blocks(self.run_hook([user("상태를 알려주세요"), said("All tasks are done.")]))

    def test_english_final_after_korean_before_tools_blocks(self):
        entries = [user("상태를 알려주세요"), said("확인하겠습니다."), tool_use(), tool_result("ok"), said("All done.")]
        self.assert_blocks(self.run_hook(entries))

    def test_korean_reply_passes(self):
        self.assertEqual(self.run_hook([user("상태를 알려주세요"), said("모두 끝났습니다. PR #5 merged.")]), "")

    def test_english_message_english_reply_passes(self):
        self.assertEqual(self.run_hook([user("What is the status?"), said("All tasks are done.")]), "")

    def test_stop_hook_active_passes(self):
        entries = [user("상태를 알려주세요"), said("All tasks are done.")]
        self.assertEqual(self.run_hook(entries, stop_hook_active=True), "")

    def test_tool_results_are_not_the_user_message(self):
        entries = [user("What is the status?"), tool_use(), tool_result("한국어 출력"), said("All done.")]
        self.assertEqual(self.run_hook(entries), "")

    def test_injected_user_entries_are_not_the_user_message(self):
        for injected in [
            "<system-reminder>한국어로 답하세요</system-reminder>",
            "<command-name>/foo</command-name>\n<command-message>한국어</command-message>",
            "<task-notification>\n<summary>작업 완료</summary>\n</task-notification>",
        ]:
            with self.subTest(injected=injected[:20]):
                entries = [user("What is the status?"), said("Checking."), user(injected), said("All done.")]
                self.assertEqual(self.run_hook(entries), "")
                entries = [user("상태를 알려주세요"), user([{"type": "text", "text": injected}]), said("All done.")]
                self.assert_blocks(self.run_hook(entries))

    def test_meta_entries_are_not_the_user_message(self):
        entries = [user("What is the status?"), user("Stop hook feedback: 한국어", isMeta=True), said("Done.")]
        self.assertEqual(self.run_hook(entries), "")

    def test_last_assistant_message_is_preferred(self):
        entries = [user("상태를 알려주세요"), said("모두 끝났습니다.")]
        self.assert_blocks(self.run_hook(entries, last_assistant_message="All tasks are done."))

    def test_missing_or_malformed_transcript_passes(self):
        done = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True,
                              input=json.dumps({"transcript_path": "/nonexistent/t.jsonl", "stop_hook_active": False}))
        self.assertEqual((done.returncode, done.stdout), (0, ""))
        for stdin in ["not json", "{}", "[]"]:
            done = subprocess.run([sys.executable, SCRIPT], input=stdin, capture_output=True, text=True)
            self.assertEqual((done.returncode, done.stdout), (0, ""))
        self.assertEqual(self.run_hook(raw="{broken\n[1,2]\n\"x\"\n"), "")


if __name__ == "__main__":
    unittest.main()
