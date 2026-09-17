---
name: delegating-to-aside
description: Use when a task reads or acts on a web page only the signed-in owner can reach and no CLI or API here covers - account settings, mail, chat, a bank, a cloud console - or needs what Aside remembers about them; not for a localhost or development page, its console, network or pixels (claude-in-chrome).
---

# Delegating to Aside

Aside is the owner's AI browser, holding their sign-ins, history and a memory
of who they are. Its own agent carries a task out; hand it the goal and the
finished state, as to a subagent. `aside guide` holds the commands and moves
with the CLI, so read it before the first call of a session, and
`aside guide repl` before `aside repl`.

## The modes

| the need | the call | what comes back |
| --- | --- | --- |
| a task on the owner's sites | `aside exec "<task>"` | blocks until done: the session id on the first line, a tool trace, the answer on the last line, in ANSI colour |
| a follow-up, a redirect, a halt | `aside session resume`, `steer`, `stop` with that id | `steer` prints `ok` and returns |
| what the owner prefers, who a person is, which account a site uses | `aside memory search "<query>" --json` | Markdown hits; ask the owner only after this finds nothing |
| the DOM or a screenshot, step by step | `aside repl` | a Playwright-style session |

Run a long `exec` in the background and report from its output, not from a
guess about how far it is.

## The limits

- An `exec` acts as the owner. One that sends, posts, pays, deletes or
  changes a setting is confirmed first, scoped to the thing named; a read is
  not.
- `--permission full-access` only on the owner's word. The default asks
  before leaving the working folder.
- Aside's memory is read only from here. What Aside should remember goes
  through `aside exec`.
- An update downloads and runs an installer, so report a stale CLI instead of
  running `aside --update` unasked.
- The Aside app rewrites `aside-browser/SKILL.md` in any skills directory that
  holds one, on every CLI update. This skill has another name so its text
  survives; `aside skills install` would bring the duplicate back.
