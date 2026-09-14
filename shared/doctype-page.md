# Page

What an `artifact` page must be, [doctype](doctype.md) § Media.

- **One file**: its own JS, SVG, CSS, fonts and images inline, nothing
  fetched; opens from `file://`; under 16 MiB (bencho).
- **Themes**: `prefers-color-scheme` and `[data-theme]` both followed, by
  the tokens of `doctype-skin.css`, which every page carries verbatim.
- **Phone width**: no sideways scroll at 320 px; a 16 px gutter; only tables,
  diagrams and code scroll, in their own focusable, labelled box.
- **Legible**: no text under 11 px at 320 px, Apple's smallest, and no Hangul
  or Han under 12 px (diagram-design); an SVG keeps its viewBox width and
  scrolls.
- **Semantic markup**: `main`, `nav`, `section`, `figure`, headings in order;
  native elements before ARIA.
- **Accessible**: contrast 4.5:1, visible focus, every control
  keyboard-operable (WCAG 2.2).
- **Actions on the page**: next actions are the page's own controls, never a
  fixed URI or an out-of-band instruction (Fielding).
- **One batch**: collected input goes back as one batch, each item keyed to
  what it answers, never to a line number (human-review).
- **Priority order**: reading order is priority order; secondary work
  collapsed; two disclosure levels at most (Nielsen).
- **SVG first**: inline SVG or CSS before a library.
- **Motion**: none on its own; a transition answers a reader's action, only
  under `prefers-reduced-motion: no-preference`; the end state alone carries
  every fact; change over time as small multiples, never played (Robertson,
  Tversky).
- **Used, not viewed**: every control clicked, never judged from a
  screenshot.
- **Footer sha**: a page inside the repository it describes pins the
  source's last commit before the page, since no commit names itself.
