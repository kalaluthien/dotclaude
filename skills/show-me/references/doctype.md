# Doctypes and media

The doctype is what a document explains, the medium where it is read; any
skill may cite either. A review fails a page on a bullet, cited as
`doctype.md § <section>: <name>`. `~/.claude/CLAUDE.md` § Visual encoding
binds every artifact too.

## Doctypes

| doctype | explains | its parts, in order |
| --- | --- | --- |
| `diagram` | one structure or concept | the title; the figure; its key; the one thing to read off it; the source |
| `narrative` | a repository, a PR or a scenario | a one-line thesis; a map of the whole; chapters, one question each with its evidence, in the order understanding builds, never file or commit order; a reason the source omits, called absent; the source at a sha |
| `comparison` | options, measurements or a change | the question; the yardstick, fixed first; each option against it, differences marked, ties plain; the pick and what would change it |

- **Template**: one HTML file per doctype, owned by its emitting skill;
  in markdown, the parts become headings.

## Media

- **`markdown`**: GitHub, chat, and always an agent; no rules.
- **`artifact`**: one HTML page for a person, JS allowed; § Page, § Figures.
- **Mermaid**: only where it renders: an artifact's `<pre class="mermaid">`
  or a GitHub body; never in chat.

### Page

Settle task and data, then audience, register, fidelity and
interaction, before code (Munzner).

- **One file**: CSS and JS inline, opens from `file://`, libraries inlined or
  pinned from a CDN the artifact allows, under 16 MiB.
- **Data first**: content drafted as JSON or markdown, HTML built from it.
- **The product's look**: its colours, type, spacing, components, real labels
  and data.
- **Themes**: colour tokens on `:root`, redefined under
  `prefers-color-scheme: dark` and `[data-theme]`.
- **Phone width**: a viewport meta without `user-scalable=no`; no sideways
  scroll at 320 px; a 16 px gutter; only tables, diagrams and code scroll, in
  their own box; [probe.md](probe.md) checks it.
- **Semantic markup**: `main`, `nav`, `section`, `figure`, headings in order;
  native elements before ARIA.
- **Accessible**: contrast 4.5:1, visible focus, every control keyboard-operable
  (WCAG 2.2).
- **Works without JS**: content reads with scripts off; JS enhances, never
  gates.
- **Actions on the page**: a page's next actions are its own controls, never a
  fixed URI or an out-of-band instruction (Fielding).
- **Priority order**: reading order is priority order; secondary work
  collapsed; two disclosure levels at most (Nielsen).
- **Sourced**: every claim one click from its source.
- **SVG first**: inline SVG or CSS before a library.
- **Motion**: a subtler animation under `prefers-reduced-motion: reduce`.
- **Used, not viewed**: a page's controls are checked by using each, never
  from a screenshot.

### Figures

- **Earns its place**: drawn only where it teaches more than a paragraph, one
  judgment each, cut if removing it loses nothing; no decoration, non-data
  ink just visible (diagram-design, Ian, Tufte).
- **Overview first**: the whole first, then zoom and filter, then details on
  demand (Shneiderman).
- **Status**: what is shown, as of when, whether loading; an error names the
  way out (Nielsen).
- **Lie factor**: shown effect over data effect within 0.95–1.05; a bar axis
  starts at zero (Tufte).
- **Channel**: a compared quantity on the highest channel: position, length,
  angle, area, hue; no pie where a bar would do (Cleveland & McGill).
- **Colour**: hue for category, one hue's intensity for quantity, colour only
  for meaning, no red–green pair; on a change, colour marks only new, changed,
  gone (Few, pr-lens).
- **Shared axes**: compared series side by side, one scale (Tufte).
- **Table or graph**: a table to look a value up, a graph to see a pattern
  (Few).
- **Title and key**: a title naming type and scope; a key for every colour,
  shape and line style; every element named and typed; every line one-way,
  labelled with intent (C4).
- **Nothing hidden**: every boundary partner, dependency direction, protocol
  and box level shown; its source named; one concern (arc42, Kruchten).
- **Symbols**: one symbol per concept, few types, each suggesting its
  meaning (Moody).
- **Locality**: a relational diagram only where adjacency shows the relation,
  else a list (Larkin & Simon).
