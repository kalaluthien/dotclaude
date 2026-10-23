#!/usr/bin/env python3
"""Merge settings.json.example into settings.json: the example wins on shared keys, local-only keys stay, hooks are
concatenated per event, permission lists are unioned, and the old file is backed up first. A local hook group the
previous example held is dropped, so an edited example hook replaces its old copy. Rerun after every pull that
touches the example."""
import json
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE, EXAMPLE = ROOT / "settings.json", ROOT / "settings.json.example"
LAST = ROOT / "backups" / "settings.json.example.last"
PER_MACHINE = ("theme", "feedbackDrafts")


def same(a, b):
    """True when two hook groups differ only by `$HOME` against its expansion or by the quote style of a path."""
    def flat(group):
        text = json.dumps(group, sort_keys=True).replace(str(Path.home()), "$HOME")
        return text.replace('\\"', "").replace("'", "")
    return flat(a) == flat(b)


def merge(example, local, last):
    merged = json.loads(json.dumps(example))
    for key, value in local.items():
        if key == "hooks":
            for event, groups in value.items():
                target = merged.setdefault("hooks", {}).setdefault(event, [])
                old = last.get("hooks", {}).get(event, [])
                target.extend(g for g in groups if not any(same(g, t) for t in target + old))
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
    LIVE.write_text(json.dumps(merge(json.loads(EXAMPLE.read_text()), local, last), indent=2, ensure_ascii=False) + "\n")
    LAST.parent.mkdir(exist_ok=True)
    shutil.copy2(EXAMPLE, LAST)


if __name__ == "__main__":
    main()
