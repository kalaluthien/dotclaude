#!/usr/bin/env python3
"""PostToolUseFailure hook on Bash: when a failed call's error holds a line of a known failure, add the known fix as
context, so the next call takes it instead of a guess. It owns every such reminder: to teach a new repeat failure, add a
row to HINTS, a regex anchored at a line start, so a quote of the error inside other output never matches, and the fix
in one sentence. Any error, or no match, prints nothing."""
import json
import re
import sys

HINTS = [
    (re.compile(r"^KeyError: ", re.M),
     "A KeyError from reading a tool's JSON: read it by key, each by `.get(...)` or `jq '.k // empty'`, and print the "
     "reply when one is missing, since the shape varies by call and a failed call returns an error body."),
    (re.compile(r"^\(eval\):\d+: diff: function definition file not found", re.M),
     "The tool shell's `diff` is a broken zsh autoload stub: call `/usr/bin/diff` instead."),
    (re.compile(r"^\(eval\):\d+: parse error near `\(\)'", re.M),
     "zsh refuses `name() { … }` when `name` is an alias: define the function as `function name { … }`."),
]


def hints(error):
    """The fix of each row whose pattern the error text matches."""
    return [fix for pattern, fix in HINTS if pattern.search(error)]


def main():
    try:
        found = hints(str(json.load(sys.stdin).get("error") or ""))
    except Exception:
        return
    if found:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUseFailure",
                                                 "additionalContext": "\n".join(["Known failure, known fix:", *found])}}))


if __name__ == "__main__":
    main()
