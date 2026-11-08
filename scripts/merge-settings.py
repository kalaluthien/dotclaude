#!/usr/bin/env python3
"""Merge settings.json.example into settings.json: the example wins on shared keys, local-only keys stay, hooks are
concatenated per event, permission lists are unioned, and the old file is backed up first. A local hook group any
earlier example held is dropped, so an edited example hook replaces its old copy, unless one of its commands holds a
line of `settings.machine-hooks`, an untracked file of substrings, one per line, for a hook only this machine runs.
Rerun after every pull that touches the example."""
import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE, EXAMPLE = ROOT / "settings.json", ROOT / "settings.json.example"
LAST = ROOT / "backups" / "settings.json.example.last"
MACHINE_HOOKS = ROOT / "settings.machine-hooks"
PER_MACHINE = ("theme", "feedbackDrafts")


def same(a, b):
    """True when two hook groups differ only by `$HOME` against its expansion or by the quote style of a path."""
    def flat(group):
        text = json.dumps(group, sort_keys=True).replace(str(Path.home()), "$HOME")
        return text.replace('\\"', "").replace("'", "")
    return flat(a) == flat(b)


def past_examples():
    """Every committed version of the example, so a missing or already-updated record of the last one still drops old groups."""
    git = ["git", "-C", str(ROOT)]
    shas = subprocess.run(git + ["log", "--format=%H", "--", EXAMPLE.name], capture_output=True, text=True).stdout.split()
    found = []
    for sha in shas:
        shown = subprocess.run(git + ["show", f"{sha}:{EXAMPLE.name}"], capture_output=True, text=True)
        try:
            found.append(json.loads(shown.stdout))
        except ValueError:
            pass
    return found


def machine_only(group, marks):
    return any(m in h.get("command", "") for h in group.get("hooks", []) for m in marks)


def merge(example, local, past, marks=()):
    merged = json.loads(json.dumps(example))
    for key, value in local.items():
        if key == "hooks":
            for event, groups in value.items():
                target = merged.setdefault("hooks", {}).setdefault(event, [])
                old = [g for version in past for g in version.get("hooks", {}).get(event, [])]
                target.extend(g for g in groups if not any(same(g, t) for t in target)
                              and (machine_only(g, marks) or not any(same(g, o) for o in old)))
        elif key == "permissions":
            for sub, sub_value in value.items():
                have = merged.setdefault("permissions", {}).setdefault(sub, sub_value)
                if isinstance(have, list) and isinstance(sub_value, list):
                    have.extend(v for v in sub_value if v not in have)
        elif key in PER_MACHINE:
            merged[key] = value
        else:
            merged.setdefault(key, value)
    return merged


def main():
    local = json.loads(LIVE.read_text()) if LIVE.exists() else {}
    if LIVE.exists():
        backup = ROOT / "backups" / f"settings.json.{time.strftime('%Y%m%d%H%M%S')}"
        backup.parent.mkdir(exist_ok=True)
        shutil.copy2(LIVE, backup)
    last = json.loads(LAST.read_text()) if LAST.exists() else {}
    marks = [m for m in MACHINE_HOOKS.read_text().splitlines() if m.strip()] if MACHINE_HOOKS.exists() else []
    LIVE.write_text(json.dumps(merge(json.loads(EXAMPLE.read_text()), local, [last] + past_examples(), marks), indent=2, ensure_ascii=False) + "\n")
    LAST.parent.mkdir(exist_ok=True)
    shutil.copy2(EXAMPLE, LAST)


if __name__ == "__main__":
    main()
