"""Refuse a Claude Code prompt or tool call whose session works in ~/Downloads or moves there.

usage: refuse-downloads.py < hook-input.json
"""
import json, os, re, sys

DOWNLOADS = os.path.realpath(os.path.expanduser("~/Downloads"))
MOVE = re.compile(r"(^|[;&|(\s])(cd|pushd)\s+[\"']?(~|\$HOME|/Users/[^/\s]+)/Downloads(/|[\"'\s;&|)]|$)")


def main(args):
    event = json.load(sys.stdin)
    cwd = os.path.realpath(event.get("cwd") or ".")
    command = (event.get("tool_input") or {}).get("command", "")
    if cwd == DOWNLOADS or cwd.startswith(DOWNLOADS + os.sep) or MOVE.search(command):
        print("A Claude session never works in ~/Downloads: start it elsewhere, and do not cd there.", file=sys.stderr)
        return 2
    return 0


sys.exit(main(sys.argv[1:]))
