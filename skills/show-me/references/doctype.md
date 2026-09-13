# Doctypes, and what each owes its reader

A review fails a page on a bullet, cited as `doctype.md § <section>: <name>`.
`~/.claude/CLAUDE.md` § Visual encoding binds every HTML page as well.

## Doctypes

| doctype | the reader | form |
| --- | --- | --- |
| `doc` | follows an argument, or looks a thing up | markdown |
| `view` | reads one relationship or structure off a figure | a form in chat, or one HTML page |
| `dashboard` | monitors, to decide | one HTML page |
| `ui` | acts, and the page changes | one HTML page |

- **The doctype test**: what the reader does with it. A `ui` offers an action
  that changes state; a `dashboard` only reads. What keeps its value with every
  behaviour removed is a `doc` or a `view` (Balkan).
- **Agent reader**: an agent gets the same content as markdown, never HTML.

## Markdown

What a `doc` owes, and the text a `view` sits in.

- **Conclusion first**: the answer opens; a heading says what is under it; one
  idea per paragraph (Nielsen).
- **One form**: a tutorial, a how-to, a reference or an explanation, never a
  mix (Procida).
- **Portable syntax**: CommonMark and GFM; a callout as `> [!NOTE]`; a
  `mermaid` fence only where the host renders it.

## HTML

- **Settled first**: the reader's task, the data, then audience, register,
  fidelity and interaction, before any code (Munzner).
- **One file**: CSS and JS inline; opens from `file://`; a library inlined or
  pinned from a CDN the artifact allows; under 16 MiB.
- **Data first**: content drafted as JSON or markdown, HTML built from it.
- **The product's look**: its colours, type, spacing and components; real labels
  and real data.
- **Themes**: colour tokens on `:root`, redefined under
  `prefers-color-scheme: dark` and `[data-theme]`.
- **Phone width**: a viewport meta without `user-scalable=no`; no sideways page
  scroll at 320 px; a 16 px gutter; only a table, a diagram or code scrolls, in
  its own box.
- **Semantic markup**: `main`, `nav`, `section`, `figure`, headings in order;
  native elements before ARIA.
- **Accessible**: contrast 4.5:1, visible focus, every control operable by
  keyboard (WCAG 2.2).
- **Works without JS**: content reads with scripts off; JS enhances, never
  gates; a `ui`'s next actions are controls on the page (Fielding).
- **Priority order**: reading order is priority order; secondary work
  collapsed; two disclosure levels at most (Nielsen).
- **Sourced**: every claim one click from its source.
- **SVG first**: inline SVG or CSS before a library; an artifact renders
  `<pre class="mermaid">` with none.
- **Motion**: a subtler animation under `prefers-reduced-motion: reduce`.
- **Used, not viewed**: a `ui` is checked by using each action it offers, never
  from a screenshot.

## Visualisation

- **Overview first**: the whole set, then zoom and filter, then details on
  demand (Shneiderman).
- **Status**: what is shown, and as of when; an error names the way out
  (Nielsen).
- **Lie factor**: shown effect over data effect within 0.95–1.05, so a bar axis
  starts at zero (Tufte).
- **Channel**: the compared quantity on the highest free channel: position,
  length, angle, area, hue; no pie where a bar would do (Cleveland & McGill).
- **Colour**: hue for category, one hue's intensity for quantity, colour only
  for meaning, never red against green (Few).
- **Ink**: no decoration; non-data ink just visible (Tufte).
- **Shared axes**: compared series side by side on shared axes (Tufte).
- **Table or graph**: a table to look a value up, a graph to see a pattern
  (Few).
- **Dashboard**: one screen, no scrolling; every number beside its target or
  prior; a page of links is not one (Few).
- **Title and key**: a title naming type and scope; a key for every colour,
  shape and line style; every element named and typed; every line one-way,
  labelled with intent (C4).
- **Nothing hidden**: every boundary partner, dependency direction, protocol,
  box level and source; one concern per diagram (arc42, Kruchten).
- **Symbols**: one symbol per concept, few symbol types, each looking like what
  it means (Moody).
- **Locality**: a diagram only where adjacency shows the relation; else a list
  (Larkin & Simon).
