#!/bin/bash
# Claude Code UserPromptSubmit hook: rename the herdr tab and pane this
# session runs in, using the first user prompt of the session as the source.
# A one-shot `claude -p` writes a short English title; on any failure the
# slug of the prompt (the old behavior) is the fallback, so a tab is never
# left numbered. One attempt per session, marker-gated, so later prompts
# never rename again. The yield to a delegating orchestrator is pane-only:
# the pane keeps the role-task name the orchestrator gave it, the tab still
# gets the title.

[ -n "$HERDR_TAB_ID" ] || [ -n "$HERDR_PANE_ID" ] || exit 0
command -v herdr >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)

session_id=$(jq -r '.session_id // empty' <<<"$input")
[ -n "$session_id" ] || exit 0

marker="${TMPDIR:-/tmp}/herdr-named-$session_id"
[ -e "$marker" ] && exit 0
touch "$marker"

# Yield to the delegating layer, pane only: a pane whose agent claim carries
# a *name* was named role-task by the orchestrator, and that name is the
# pane's one name. Herdr auto-claims any claude pane with name null, so the
# name — not the claim — is the predicate. The tab is a different level of
# the naming strategy (workspace = where, agent = purpose, tab = current
# work), so a named pane's tab still gets the title; yielding it too is what
# left a delegated session's tab on its default numeric label.
named=
if [ -n "$HERDR_PANE_ID" ]; then
  named=$(herdr agent list 2>/dev/null | jq -r --arg p "$HERDR_PANE_ID" \
    '.result.agents[] | select(.pane_id == $p) | .name // empty')
fi
# Nothing left to rename: the pane has yielded and there is no tab.
[ -n "$named" ] && [ -z "$HERDR_TAB_ID" ] && exit 0

# Fallback slug: lowercase, non-alphanumeric runs become one hyphen.
# Oniguruma's [[:alnum:]] matches Unicode letters, and jq slices by
# codepoint, so multibyte (Korean) prompts slug and truncate cleanly.
slug=$(jq -r '.prompt // ""
  | ascii_downcase
  | gsub("[^[:alnum:]]+"; "-")
  | sub("^-"; "") | sub("-$"; "")
  | .[0:32]
  | sub("-+$"; "")' <<<"$input")

prompt_head=$(jq -r '.prompt // "" | .[0:1000]' <<<"$input")
[ -n "$slug" ] || exit 0

# Title in a detached fork: the one-shot call takes seconds, and the hook
# must return before the prompt is processed. --safe-mode keeps the call
# free of this machine's settings and hooks, so no Stop hook rewrites its
# output and no hook recurses into this one.
(
  title=""
  if command -v claude >/dev/null 2>&1 && [ -n "$prompt_head" ]; then
    title=$(claude -p --safe-mode --model claude-sonnet-5 --effort low \
      "Generate a short tab title (3-6 words, English, Title Case, no quotes, no trailing period) summarizing this coding-session request. Output the title only. Request: $prompt_head" \
      2>/dev/null | head -n 1)
    title=$(printf '%s' "$title" \
      | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | cut -c 1-60)
  fi
  [ -n "$title" ] || title="$slug"
  [ -n "$HERDR_TAB_ID" ] && herdr tab rename "$HERDR_TAB_ID" "$title" >/dev/null 2>&1
  [ -z "$named" ] && [ -n "$HERDR_PANE_ID" ] &&
    herdr pane rename "$HERDR_PANE_ID" "$title" >/dev/null 2>&1
) >/dev/null 2>&1 &

exit 0
