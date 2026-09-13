# Doctypes and media

The doctype is how a document explains, the medium where it is read.
[prose.md](prose.md) binds the sentences in both, `~/.claude/CLAUDE.md`
§ Visual encoding every artifact.

## Doctypes

| doctype | explains | for | its parts, in order |
| --- | --- | --- | --- |
| `diagram` | in one picture | what it is made of, how its parts connect | the title; the figure; its key; the one thing to read off it; the source |
| `narrative` | in the order understanding builds | how it works, why it is so | a one-line thesis; a map of the whole; chapters, one question each with its evidence, never in file or commit order; a reason the source omits, called absent; the source at a sha |
| `comparison` | under one yardstick | which one, or what differs | the question; the yardstick, fixed first; each option against it, differences marked and keyed, ties plain; the verdict and what would change it |

- **The question picks, not the subject**: a repository's structure is a
  diagram, what a PR changed a comparison, why a design is so a narrative.
- **Two questions**: a narrative, the diagram its map, the comparison a
  chapter.
- **Template**: show-me's `assets/<doctype>.html`; in markdown the parts are
  headings.

## Media

- **`markdown`**: GitHub, chat, and always an agent; drawn in show-me's chat
  forms. Mermaid only in a GitHub body: an artifact's breaks Works without JS.
- **`artifact`**: one HTML page for a person, where a layout, a wide table or
  a dense map outgrows markdown; held to § Figures and to § Page, or to the
  § Page bullets its header names.

### Page

- **One file**: CSS, JS, images and icons inline; opens from `file://`;
  libraries pinned from a CDN the artifact allows; under 16 MiB (bencho).
- **Themes**: `prefers-color-scheme` and `[data-theme]` both followed, by
  tokens on `:root` redefined under each or by system colours.
- **Phone width**: no sideways scroll at 320 px; a 16 px gutter; only tables,
  diagrams and code scroll, in their own box.
- **Legible**: no text under 11 px at 320 px, Apple's smallest, read here by
  the probe; an SVG keeps its viewBox width and scrolls.
- **Semantic markup**: `main`, `nav`, `section`, `figure`, headings in order;
  native elements before ARIA.
- **Accessible**: contrast 4.5:1, visible focus, every control
  keyboard-operable (WCAG 2.2).
- **Works without JS**: content reads with scripts off; JS never gates.
- **Actions on the page**: next actions are the page's own controls, never a
  fixed URI or an out-of-band instruction (Fielding).
- **One batch**: collected input goes back as one batch, each item keyed to
  what it answers, never to a line number (human-review).
- **Priority order**: reading order is priority order; secondary work
  collapsed; two disclosure levels at most (Nielsen).
- **SVG first**: inline SVG or CSS before a library.
- **Motion**: subtler under `prefers-reduced-motion: reduce`.
- **Used, not viewed**: [probe.md](probe.md) clicks every control and checks
  width and legibility; a screenshot shows none of them.

### Figures

- **Earns its place**: drawn only where it teaches more than a paragraph, one
  judgment each, cut if removing it loses nothing; non-data ink just visible
  (diagram-design, Ian, Tufte).
- **Lie factor**: shown effect over data effect within 0.95–1.05; a bar axis
  starts at zero (Tufte).
- **Channel**: a compared quantity on the highest channel: position, length,
  angle, area, hue; no pie where a bar would do (Cleveland & McGill).
- **Colour**: hue for category, one hue's intensity for quantity, colour only
  for meaning, no red–green pair; on a change, only new, changed, gone
  (Few, pr-lens).
- **Shared axes**: compared series side by side, one scale (Tufte).
- **Title and key**: a title naming type and scope; a key for every colour,
  mark, shape and line style; every element named and typed; every line
  one-way, labelled with intent (C4).
- **Nothing hidden**: boundary partners, dependency directions, protocols and
  box levels shown; the source named; one concern (arc42, Kruchten).
- **Symbols**: one per concept, few types, each suggesting its meaning
  (Moody).
- **Locality**: a relational diagram only where adjacency shows the relation,
  else a list (Larkin & Simon).
