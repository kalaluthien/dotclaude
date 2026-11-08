# Refuse to start Claude Code in a protected folder or with one added (`--add-dir`), before that folder's project
# skills, agents, hooks and MCP servers load. A protected folder is a `Read(~/<dir>/**)` deny rule of the user settings.
# Install: add to ~/.zshenv
#   [[ -r ~/.claude/scripts/protect-folders.zsh ]] && source ~/.claude/scripts/protect-folders.zsh
claude() {
  local hook="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/refuse-downloads.py"
  if [[ -r $hook ]]; then
    python3 "$hook" start "$@" || return
  fi
  command claude "$@"
}
