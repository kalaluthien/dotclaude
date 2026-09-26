#!/usr/bin/env python3
"""Table test for kill-guard.py: feeds it hook JSON and checks each command is denied or passed. Run: python3 hooks/kill-guard_test.py"""
import json
import os
import subprocess
import sys
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kill-guard.py")

BROAD = [
    "pkill -f cat",
    "pkill cat",
    "pkill -9 -f 'scratch data'",
    'pkill -f "cat" -P $(pgrep -f "scratch_data" | head -1)',
    "pkill -P $(pgrep -f x)",
    "pkill -x -P $(pgrep -f x) cat",
    "kill $(pgrep -f x)",
    "kill -9 `pidof node`",
    "kill \"$(ps -ax | awk '/x/ {print $1}')\"",
    "killall -x $(pgrep x)",
    "killall -m 'Saf.*'",
    "killall -r 'Saf.*'",
    "kill -9 -1",
    "kill -- -1",
    "kill -s KILL -1",
    "echo $(pkill -f cat)",
    "bash -c 'pkill -f cat'",
]
WRAPS = ["true && {}", "true; {}", "echo x | {}", "sudo {}", "sudo -u root {}", "xargs {}", "FOO=1 nohup {} &", "{} 2>/dev/null"]
REFUSE = [wrap.format(cmd) for cmd in BROAD for wrap in ["{}"] + WRAPS] + [
    "pgrep -f x | xargs kill",
    "pgrep -f x | xargs -n1 kill -9",
    "pgrep x | xargs pkill -x",
    "true\npkill -f cat",
    "cat <<EOF > note.md\nhi\nEOF\npkill -f cat",
]
ALLOW = [
    "kill 1234",
    "kill -9 1234 5678",
    "kill %1",
    "kill -- -1234",
    "kill $PID",
    "pkill -x Safari",
    "pkill -9 -x Safari",
    "sudo pkill -x Safari",
    "killall Safari",
    "killall -9 Safari",
    "pgrep -f cat",
    "echo pkill",
    "grep -r pkill .",
    'git commit -m "pkill note"',
    "git commit -m 'pkill -f cat is dangerous'",
    "ps aux | grep cat",
    "command -v pkill",
    "man killall",
    "ls",
    "cat <<EOF > note.md\npkill -f cat\nEOF",
    "gh pr create --body \"$(cat <<'EOF'\nit's about pkill -f cat\nEOF\n)\"",
    "cat <<-'X'\n\tkillall -m y\n\tX\necho done",
]


def run(command):
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
    return subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload), capture_output=True, text=True)


class KillGuard(unittest.TestCase):
    def test_refuse(self):
        for command in REFUSE:
            with self.subTest(command=command):
                result = run(command)
                self.assertEqual(result.returncode, 0, result.stderr)
                out = json.loads(result.stdout)["hookSpecificOutput"]
                self.assertEqual(out["permissionDecision"], "deny")
                self.assertIn("kill <pid>", out["permissionDecisionReason"])

    def test_allow(self):
        for command in ALLOW:
            with self.subTest(command=command):
                result = run(command)
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))


if __name__ == "__main__":
    unittest.main()
