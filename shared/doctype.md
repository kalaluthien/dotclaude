# Doctypes and media

The doctype is how a document explains, the medium where it is read.
`~/.claude/CLAUDE.md` § Visual encoding binds every artifact.

## Doctypes

| doctype | explains | for | its parts, in order |
| --- | --- | --- | --- |
| `diagram` | in one picture | what it is made of, how its parts connect | the title; the one thing to read off it; the figure; its key; the source |
| `narrative` | in the order understanding builds | how it works, why it is so | a one-line thesis; a map of the whole; chapters, one question each with its evidence, never in file or commit order; a reason the source omits, called absent; the source at a sha |
| `comparison` | under one yardstick | which one, or what differs | the question; the verdict and what would change it; the yardstick, fixed before any option; each option against it, differences in bold and keyed, ties plain |

- **The question picks, not the subject**: a repository's structure is a
  diagram, what a PR changed a comparison, why a design is so a narrative.
- **Two questions**: a narrative, the diagram its map, the comparison a
  chapter.
- **Markdown**: the parts are headings.

## Media

- **`markdown`**: GitHub, chat, and always an agent. Mermaid only in a GitHub body: an artifact would fetch its library.
- **`artifact`**: one HTML page for a person, where a layout, a wide table or
  a dense map outgrows markdown; held to [page](doctype-page.md) and
  [figures](doctype-figures.md), or to the page bullets its header names.
