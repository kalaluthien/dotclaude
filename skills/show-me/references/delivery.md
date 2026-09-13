# The ending

Where a show-me result goes once its doctype and medium are settled.

- Unless the ask already says, ask once with `AskUserQuestion`: a GitHub
  issue, an artifact, or chat. When it is obvious, do not ask. Build only the
  one chosen.
- **Chat**: markdown, in the chat forms of `SKILL.md`.
- **GitHub issue**: markdown as an issue body or comment, filed by the
  repository's own procedure where it has one, else `gh issue create`.
- **Artifact**: the page is written to `show-me-<slug>.html` in the session's
  scratchpad directory, `/tmp` where none is named, passes the
  [probe](probe.md), then goes to the `Artifact` tool and follows that tool's
  rules. When the tool is absent from the session, say so and `open` the file.
- Reading the `.html` back is not a delivery: it renders as source text.
- Tell the user the one-sentence version in chat, whatever the ending.
