# dotclaude

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-donate-yellow)](https://buymeacoffee.com/kalaluthien)

Shared Claude Code setup for `~/.claude`: three skills, six hooks, a settings template and a global `CLAUDE.md` of preferences.

| Part | What it does |
| --- | --- |
| `skills/grill-me` | Interviews you on a plan until every open choice is settled. |
| `skills/show-me` | Shows a system, change or choice as a diagram, table or HTML page, made in a forked subagent. |
| `skills/surprise-me` | Researches an area in depth and explains it in a structure, in a forked subagent. |
| `hooks/kill-guard.py` | Refuses a broad process kill such as `pkill -f cat`. |
| `hooks/failure-hint.py` | After a failed Bash call, adds the known fix for that failure. |
| `hooks/reply-language.py` | Asks for a rewrite when a reply to a Korean message has no Korean or uses a banned word. |
| `hooks/reply-handoff.py` | Asks for a rerun when a final reply hands you a command to run and no tool call of the turn was refused. |
| `hooks/refuse-downloads.py` | Keeps sessions out of each folder a `Read(~/<dir>/**)` deny rule names (`~/Downloads`, `~/Documents`): refuses a session working there and a tool call naming a path inside, by any spelling, or scanning a folder above; passes only a plain `cp` of named regular files out of a folder. |
| `hooks/herdr-agent-state.sh` | Reports session state to herdr; does nothing outside herdr. |
| `scripts/protect-folders.zsh` | Refuses to start `claude` in a protected folder or with one added, before its project files load. |
| `scripts/merge-settings.py` | Merges `settings.json.example` into your `settings.json`. |
| `CLAUDE.md` | The author's global preferences; replace them with yours. |

## Steal it

### One part

Clone to a scratch folder, so nothing in `~/.claude` changes until you copy.

1. `git clone --depth 1 https://github.com/kalaluthien/dotclaude /tmp/dotclaude`
2. A skill: `mkdir -p ~/.claude/skills && cp -r /tmp/dotclaude/skills/grill-me ~/.claude/skills/`
3. A hook: `mkdir -p ~/.claude/hooks && cp /tmp/dotclaude/hooks/kill-guard.py ~/.claude/hooks/`, then copy its entry from `settings.json.example` (the command that names it, under its event) into your `settings.json`.
4. Edit what you copied; the skills and hooks hold the author's habits, such as Korean replies.

### Everything

Claude Code creates files in `~/.claude` first, so a plain `git clone` fails; install in place.

1. `cd ~/.claude && git init -b main`
2. `git remote add origin https://github.com/kalaluthien/dotclaude`
3. `git fetch origin && git checkout -t origin/main`
4. `python3 scripts/merge-settings.py` writes `settings.json` from `settings.json.example`; it keeps local-only keys and `theme` and `feedbackDrafts`, and backs the old file up to `backups/`. On a machine with an older `settings.json`, the first run keeps its old `PreToolUse` Bash group (the one ending `exec rtk hook claude`); delete that group by hand once. A hook only this machine runs survives a merge when `settings.machine-hooks`, an untracked file, holds a substring of its command, one per line.
5. Install `rtk`. Without it the Bash hook skips it.
6. Add `[[ -r ~/.claude/scripts/protect-folders.zsh ]] && source ~/.claude/scripts/protect-folders.zsh` to `~/.zshenv`, so `claude` refuses to start in a protected folder.
7. Write a note that must be known before its situation arises in `~/.claude/rules/<topic>.md`, such as `machine.md` for one that holds only on this machine; write any other note in `~/.claude/memory/`.
8. After a `git pull` that changes `settings.json.example`, run step 4 again.

## Use it

1. Type `/grill-me`, `/show-me` or `/surprise-me` in a session, then your topic; the three skills run only when you type them. `/show-me` and `/surprise-me` run in a forked subagent that sees no earlier chat, so give the full ask up front, as their argument hint shows.
2. Read `settings.json.example` once: `permissions`, `hooks`, `outputStyle` and `autoMemoryDirectory` are the keys most worth changing.
3. Hooks need no action; they run on each Bash call, reply or session start.
4. To change a part, edit it under `~/.claude`, then open a pull request against your own fork.

## Protected folders

Sessions stay out of `~/Downloads` and `~/Documents`, since downloaded instruction files can inject a prompt and both hold personal and payment records. Each folder is one `Read(~/<dir>/**)` deny rule, with its `Edit` twin, in `settings.json.example`; add a pair to protect another.

| layer | stops |
| --- | --- |
| deny rules | Claude Code's file tools, `cat`-like commands and redirections, and the folder's `CLAUDE.md`, `AGENTS.md` and rules loading |
| `hooks/refuse-downloads.py` | the spellings deny rules miss: `$HOME`, `cd`, relative paths, `..`, symlinks, globs, inline code, scans of a folder above (`find ~`) |
| `scripts/protect-folders.zsh` | a start in the folder or with it added, which would load its project skills, agents, hooks and MCP servers |

Not covered: a script that opens a protected file without naming it, a path the shell computes at run time (`eval` of a built string, an encoded path), and a launcher that runs the `claude` binary without zsh. The sandbox (`sandbox.filesystem.denyRead`) closes the first at the OS level; it is off here, since it also cut SSH in a probe.

## Contributions

- [CONTRIBUTING.md](CONTRIBUTING.md) says how to report a problem or ask a question; pull requests from outside are not accepted.
- [CLAUDE.md](CLAUDE.md) holds the preferences every change follows.

## License

[Apache-2.0](LICENSE); works it took from are named in [NOTICE](NOTICE). This project is not affiliated with Anthropic.
