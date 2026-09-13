# Delivery by kind

Where a show-me result is built and how it reaches the reader, once its kind
is named. What the result must be is `~/.claude/spec/document-kinds.md`'s,
cited here by rule ID and never restated.

| kind | built at | reaches desktop and phone | asked |
| --- | --- | --- | --- |
| `ui` | `/tmp/show-me-<slug>.html`, or an artifact | `open` on desktop; the artifact on a phone | file or artifact |
| `dashboard` | one path named by its subject and rebuilt in place, carrying V2's status: the repository's `docs/<slug>.html` when the numbers are that repository's, else an artifact republished from one file so its URL holds | `open`, then PNG slices; the artifact | file or artifact, when both fit |
| `view` | in chat, one of the forms in `SKILL.md`; or `/tmp/show-me-<slug>.html`; or an artifact | the chat; `open`, then PNG slices ([to-png](to-png.md)); the artifact | which of the three |
| `doc` | markdown, in chat or in a `.md` file the reader keeps (M1) | the chat, or the file's path | nothing |

- Ask with `AskUserQuestion`, and build only the delivery chosen.
- A `ui` never goes out as PNG: an image takes no input, so a phone reaches it
  only through an artifact.
- A `dashboard` is never built at a run-named or `/tmp` path; § Kinds says
  why.
- Every HTML page passes the 320 px probe ([to-png](to-png.md)) before it is
  delivered, which checks C7's no-sideways-scroll clause and no other; a
  `dashboard` also passes its desktop-width run (V3).
- Reading the `.html` back is not a delivery: it renders as source text.
- Tell the user the one-sentence version in chat, whatever the delivery.

An artifact is the page handed to the `Artifact` tool, and C1 defers to that
tool's rules. When the tool is absent from the session, say so and offer
`SendUserFile` with `display: render` instead. `SendUserFile` is not
available in every harness either, so check with ToolSearch before naming it,
and never build a delivery on it.
