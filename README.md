# dotclaude

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-donate-yellow)](https://buymeacoffee.com/kalaluthien)

The author's Claude Code setup for `~/.claude`: four skills you call by name, six hooks that run by themselves, a settings template and a global `CLAUDE.md` of preferences. Take one part or all of it.

## Skills

A skill is a command you type in a session, such as `/grill-me`, followed by your topic. None of these four starts on its own.

| Skill | What it does | Use it when |
| --- | --- | --- |
| `/grill-me` | Asks you about a plan, one open choice at a time, each with options, their cost and a recommended pick, until every choice is settled. | You have a plan or an idea and decisions are still open. |
| `/show-me` | Draws a system, change, status, data or choice as a diagram, table, chart or HTML page. | A wall of text would hide the shape of the answer. |
| `/surprise-me` | Researches an area or question in depth and brings back an explanation with a clear structure. | You want an answer deeper than your own question reaches. |
| `/teach-me` | Teaches a topic by questions, or walks you through a paper, document or book quote by quote. | You want to explain or use an idea on your own, not just hear it once. |

`/show-me` and `/surprise-me` run in a separate subagent that sees none of your earlier chat, so put the whole ask, with its subject and source, after the command.

## Hooks

A hook is a script Claude Code runs at a set moment; you never call it. Each one runs once its entry from `settings.json.example` is in your `settings.json`, as [Steal it](#steal-it) shows. The template also holds one inline entry with no file, an `echo` on each message that asks for replies in Korean.

| Hook | Runs when | What it does |
| --- | --- | --- |
| `kill-guard.py` | Before each shell command | Refuses a process kill by a broad name, such as `pkill -f cat`, which could stop every app; a kill by process number or exact name runs. |
| `refuse-downloads.py` | Before Claude uses any tool (reads a file, runs a command), and when you send a message | Keeps the session out of `~/Downloads`, `~/Documents` and any other protected folder, by any spelling of the path; [Protected folders](#protected-folders) lists what it misses. |
| `failure-hint.py` | After a shell command fails | Adds the known fix for that error, so the next try is not a guess. |
| `reply-language.py` | When a reply ends | Asks for a rewrite when a reply to a Korean message has no Korean or uses a banned word; the author's habit, so drop it if you do not write Korean. |
| `reply-handoff.py` | When a reply ends | Sends the reply back when it asks you to run a command yourself that Claude could have run, so Claude runs it instead. |
| `herdr-agent-state.sh` | When a session starts, and again after `/resume`, `/clear`, `/compact` or a fork | Tells herdr, a terminal workspace app that runs several sessions side by side, which session runs in which of its panels; does nothing outside herdr. |

## Other parts

| Part | What it does | When it runs |
| --- | --- | --- |
| `settings.json.example` | The settings template: permissions, hooks, output style and memory folder. | Once, merged into your `settings.json` by the script below. |
| `scripts/merge-settings.py` | Merges `settings.json.example` into your `settings.json`, keeping your local-only keys. | When you install, and after a pull that changes the template. |
| `scripts/protect-folders.zsh` | Refuses to start `claude` in a protected folder, or with one added, before its project files load. | Each time you type `claude` in zsh, once sourced from `~/.zshenv`. |
| `CLAUDE.md` | The author's global preferences, which every session reads. | At every session start; replace it with yours. |

## How the author uses each skill

Each row is a request the author typed, restated in plain words, and what they wanted from it.

### How the author uses `/grill-me`

| The author typed | What they wanted |
| --- | --- |
| `/grill-me` and the link to a plan written up in a shared document | Every open choice in a long plan settled, one at a time. |
| `/grill-me` and a one-line backlog wish: one lead per plugin, where today one lead covers a whole repository | A goal and tasks out of a wish that named a problem but no design. |
| `/grill-me` and their own proposal for a decision-tree diagram skill, asking to push it further and make it concrete | A sharper proposal, each loose part questioned. |
| `/grill-me` a new command-line tool that searches markdown notes; language, index or not, where notes live and output form are open | Decisions that hang on each other settled in the right order. |
| `/grill-me` a household budget command-line tool, with nothing decided yet: language, storage, commands, categories, currencies, backup, reports | A whole design from a blank page. |

One run: on the shared-document plan, three rounds of questions settled how to split and order the work, then a table of every decision came back for a final yes.

### How the author uses `/show-me`

| The author typed | What they wanted |
| --- | --- |
| `/show-me` every task still open, briefed as one table | Each task's state at a glance. |
| `/show-me` how each subsystem is built, as a zoom diagram | One level at a time, opened on demand. |
| `/show-me` a tutorial page of what users see change in a new version, with mock screens and technical notes behind toggles | A change shown as screens, not as a list of commits. |
| `/show-me` a full report of the models a service runs: quoted preprocessing and call code, and a catalog of each model's inputs and outputs, as a temporary page | Code quotes and a catalog side by side on one page. |

### How the author uses `/surprise-me`

| The author typed | What they wanted |
| --- | --- |
| `/surprise-me` take a grading feature further: how it sets metrics, how it scores, and how it shows results to people | The strongest options for an open question, found by research. |
| `/surprise-me` how HTTP caching headers decide when a browser reuses a stored response | A structure for a broad topic before its details. |
| `/surprise-me` one narrow question: ETag or Last-Modified, which makes a browser check a cached response again, and which to set | A short answer on one axis, tied to a decision. |

One run: on the ETag question, the answer opened with the verdict in bold, then a table, the reasons in order, a recommendation, its caveats and the sources.

### How the author uses `/teach-me`

| The author typed | What they wanted |
| --- | --- |
| `/teach-me` compound interest, to compare two loan offers alone | To do the sums without help. |
| `/teach-me` a paper abstract, pasted in, before presenting it at a journal club the next day | To present it with confidence. |
| `/teach-me` why the seasons happen, to explain it to a child | An explanation simple enough to pass on. |
| `/teach-me` Bayes' rule, to tell a patient what a positive test result really means | To read a test result right, base rates included. |
| `/teach-me` the first chapter of a book on fast and slow thinking | The chapter's ideas, with the book's own words beside them. |

One run: on the book chapter, the first message asked what the learner wanted from it, with lettered options, and asked for the text to quote.

## Steal it

### One part

Clone to a scratch folder, so nothing in `~/.claude` changes until you copy.

1. `git clone --depth 1 https://github.com/kalaluthien/dotclaude /tmp/dotclaude`
2. A skill: `mkdir -p ~/.claude/skills && cp -r /tmp/dotclaude/skills/grill-me ~/.claude/skills/`
3. A hook: `mkdir -p ~/.claude/hooks && cp /tmp/dotclaude/hooks/kill-guard.py ~/.claude/hooks/`, then copy its entry from `settings.json.example` (the command that names it, under its event) into your `settings.json`.
4. Edit what you copied; the skills and hooks hold the author's habits, such as Korean replies.

### Everything

Claude Code creates files in `~/.claude` first, so a plain `git clone` fails; install in place.

1. `cd ~/.claude && git init -b main`; if a file this repository tracks, such as `CLAUDE.md`, already exists there, step 3 stops rather than overwrite it, so move that file aside first.
2. `git remote add origin https://github.com/kalaluthien/dotclaude`
3. `git fetch origin && git checkout -t origin/main`
4. `python3 scripts/merge-settings.py` writes `settings.json` from `settings.json.example`; it keeps local-only keys and `theme` and `feedbackDrafts`, and backs the old file up to `backups/`. A hook only this machine runs survives a merge when `settings.machine-hooks`, an untracked file, holds a substring of its command, one per line.
5. Add `[[ -r ~/.claude/scripts/protect-folders.zsh ]] && source ~/.claude/scripts/protect-folders.zsh` to `~/.zshenv`, so `claude` refuses to start in a protected folder.
6. Write a note that must be known before its situation arises in `~/.claude/rules/<topic>.md`, such as `machine.md` for one that holds only on this machine; write any other note in `~/.claude/memory/`.
7. After a `git pull` that changes `settings.json.example`, run step 4 again.

## Use it

1. Type a skill's name in a session, then your topic, as the [Skills](#skills) table shows.
2. Read `settings.json.example` once: `permissions`, `hooks`, `outputStyle` and `autoMemoryDirectory` are the keys most worth changing.
3. Hooks need no action; they run each time Claude uses a tool, you send a message, a reply ends or a session starts.
4. To change a part, edit it under `~/.claude`, then open a pull request against your own fork, not this repository.

## Protected folders

Sessions stay out of `~/Downloads` and `~/Documents`, since downloaded instruction files can inject a prompt and both hold personal and payment records. Each folder is one `Read(~/<dir>/**)` deny rule, with its `Edit` twin, in `settings.json.example`; add a pair to protect another.

| Layer | Stops |
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
