# dotclaude

Shared Claude Code setup for `~/.claude`. Claude Code creates files there first, so a plain `git clone` fails; install in place.

1. `cd ~/.claude && git init -b main`
2. `git remote add origin https://github.com/kalaluthien/dotclaude`
3. `git fetch origin && git checkout -t origin/main`
4. `python3 scripts/merge-settings.py` writes `settings.json` from `settings.json.example`; it keeps local-only keys and `theme` and `feedbackDrafts`, and backs the old file up to `backups/`. On a machine with an older `settings.json`, the first run keeps its old `PreToolUse` Bash group (the one ending `exec rtk hook claude`); delete that group by hand once.
5. Install `rtk`. Without it the Bash hook skips it.
6. Write notes that hold only on this machine in `~/.claude/rules/machine.md`.
7. After a `git pull` that changes `settings.json.example`, run step 4 again.
