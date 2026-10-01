#!/usr/bin/env python3
"""Table test for redirect-guard.py: feeds it hook JSON with a cwd holding `old.txt` and checks each command is denied
or passed. Run: python3 hooks/redirect-guard_test.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redirect-guard.py")

REFUSE = [
    "echo hi > old.txt",
    "echo hi >old.txt",
    "git show origin/main:old.txt > old.txt",
    "cat > old.txt <<'EOF'\nhi\nEOF",
    "cat <<EOF > old.txt\nhi\nEOF",
    "echo hi 1> old.txt",
    "ls 2> old.txt",
    "ls &> old.txt",
    "echo hi > 'old.txt'",
    "echo hi > \"old.txt\"",
    "echo hi > ./sub/../old.txt",
    "true && echo hi > old.txt",
    "echo $(echo hi > old.txt)",
    "echo \"$(echo hi > old.txt)\"",
    "(echo hi > old.txt)",
    "echo '>' x; echo hi > old.txt",
    "L=old.txt; echo hi > $L",
    "L=old.txt; echo hi > \"$L\"",
    "L=old.txt; echo hi > ${L}",
    "L=old.txt; while true; do ls > $L 2>&1; c=$?; [ $c -ne 75 ] && break; sleep 30; done",
    "echo hi > $OLDFILE",
]
ALLOW = [
    "echo hi >| old.txt",
    "echo hi >! old.txt",
    "echo hi >> old.txt",
    "ls 2>&1",
    "ls > new.txt 2>&1",
    "ls &> /dev/null",
    "ls > /dev/null",
    "ls 2> /dev/null",
    "echo hi >&2",
    "echo hi > new.txt",
    "echo hi > sub/new.txt",
    "echo 'a > old.txt'",
    "echo \"a > old.txt\"",
    "echo a \\> old.txt",
    "git commit -m 'x > old.txt'",
    "cat > new.txt <<'EOF'\necho hi > old.txt\nEOF",
    "cat <<EOF\nls > old.txt\nEOF",
    "gh pr create --body \"$(cat <<'EOF'\nrun ls > old.txt\nEOF\n)\"",
    "echo hi # > old.txt",
    "cat < old.txt",
    "diff <(ls) old.txt",
    "tee >(cat) < old.txt",
    "echo hi > $FILE",
    "L=new.txt; echo hi > $L",
    "echo hi > $UNSET_VAR_X",
    "L=old.txt; echo hi >| $L",
    "ls",
]


def run(command, cwd, env=None):
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": cwd, "tool_input": {"command": command}}
    # the hook runs from elsewhere, so only the input's cwd can make old.txt resolve
    return subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload), capture_output=True, text=True, cwd="/", env=env)


class RedirectGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.cwd = cls.tmp.name
        os.mkdir(os.path.join(cls.cwd, "sub"))
        with open(os.path.join(cls.cwd, "old.txt"), "w") as f:
            f.write("old\n")
        cls.env = {**os.environ, "OLDFILE": os.path.join(cls.cwd, "old.txt")}
        cls.env.pop("UNSET_VAR_X", None)
        cls.env.pop("FILE", None)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_refuse(self):
        for command in REFUSE:
            with self.subTest(command=command):
                result = run(command, self.cwd, self.env)
                self.assertEqual(result.returncode, 0, result.stderr)
                out = json.loads(result.stdout)["hookSpecificOutput"]
                self.assertEqual(out["permissionDecision"], "deny")
                self.assertIn(">|", out["permissionDecisionReason"])

    def test_allow(self):
        for command in ALLOW:
            with self.subTest(command=command):
                result = run(command, self.cwd, self.env)
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))


if __name__ == "__main__":
    unittest.main()
