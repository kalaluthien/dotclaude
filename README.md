# dotclaude

Shared Claude Code setup for `~/.claude`: four skills, four hooks, a settings template and a global `CLAUDE.md` of preferences.

| Part | What it does |
| --- | --- |
| `skills/grill-me` | Interviews you on a plan until every open choice is settled. |
| `skills/break-me` | Tests a conclusion you hold with a check that could prove it wrong. |
| `skills/show-me` | Shows a system, change or choice as a diagram, table or HTML page. |
| `skills/surprise-me` | Researches an area in depth and explains it in a structure. |
| `hooks/kill-guard.py` | Refuses a broad process kill such as `pkill -f cat`. |
| `hooks/failure-hint.py` | After a failed Bash call, adds the known fix for that failure. |
| `hooks/reply-language.py` | Asks for a rewrite when a reply to a Korean message has no Korean. |
| `hooks/herdr-agent-state.sh` | Reports session state to herdr; does nothing outside herdr. |
| `scripts/merge-settings.py` | Merges `settings.json.example` into your `settings.json`. |
| `CLAUDE.md` | The author's global preferences; replace them with yours. |

## Steal it

### One part

Clone to a scratch folder, so nothing in `~/.claude` changes until you copy.

1. `git clone --depth 1 https://github.com/kalaluthien/dotclaude /tmp/dotclaude`
2. A skill: `cp -r /tmp/dotclaude/skills/grill-me ~/.claude/skills/`
3. A hook: `cp /tmp/dotclaude/hooks/kill-guard.py ~/.claude/hooks/`, then copy its entry from `settings.json.example` (the command that names it, under its event) into your `settings.json`.
4. Edit what you copied; the skills and hooks hold the author's habits, such as Korean replies.

### Everything

Claude Code creates files in `~/.claude` first, so a plain `git clone` fails; install in place.

1. `cd ~/.claude && git init -b main`
2. `git remote add origin https://github.com/kalaluthien/dotclaude`
3. `git fetch origin && git checkout -t origin/main`
4. `python3 scripts/merge-settings.py` writes `settings.json` from `settings.json.example`; it keeps local-only keys and `theme` and `feedbackDrafts`, and backs the old file up to `backups/`. On a machine with an older `settings.json`, the first run keeps its old `PreToolUse` Bash group (the one ending `exec rtk hook claude`); delete that group by hand once.
5. Install `rtk`. Without it the Bash hook skips it.
6. Write notes that hold only on this machine in `~/.claude/rules/machine.md`.
7. After a `git pull` that changes `settings.json.example`, run step 4 again.

## Use it

1. Type `/grill-me`, `/break-me`, `/show-me` or `/surprise-me` in a session, then your topic; the four skills run only when you type them.
2. Read `settings.json.example` once: `permissions`, `hooks` and `outputStyle` are the keys most worth changing.
3. Hooks need no action; they run on each Bash call or reply.
4. To change a part, edit it under `~/.claude`, then open a pull request against your own fork.
