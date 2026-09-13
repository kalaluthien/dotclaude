# Document kinds

Normative. What a page or a document is, named by what its reader does with
it, and the rules a page of each kind is failed on.

## Kinds

A page's kind is its reader's primary job. Test the rows in order; the first
match is the kind. `hooks/check-document-kind.py` reads the kind words from
this table's first column.

| kind | the reader | default form |
| --- | --- | --- |
| `ui` | supplies input the page did not hold, and the page answers or acts on it | HTML |
| `dashboard` | returns to the same page to read numbers against a target or a prior, then decides | HTML |
| `view` | reads one structure or relationship off a figure; no decision owed | HTML, or a `mermaid` fence where the host renders it |
| `doc` | reads top to bottom or by heading; nothing changes while they read | markdown; HTML where the host renders no markdown (`docs/`) or a figure needs it |

- A control that re-reads or re-shows what the page already holds -- refresh,
  filter, disclosure, zoom -- changes no kind.
- A page is one kind; a part of another kind inside it is a figure or a
  control.
- Fidelity -- wireframe, prototype, final -- is an attribute, not a kind.
- One example of each kind is listed in `docs/INDEX.md`.

## Reading a rule

Each rule ends with what it can fail -- `all`, a kind, or `chart` and
`diagram` for a page of any kind holding one -- and the html-doc#382 NOTEs it
rests on: `2.1` is step 2, group 1, and `c1` to `c3` are its closing NOTE's
parts, which § Kinds, §§ Composition and Markdown, and § Visualisation rest on
in that order. The issue is
<https://github.com/kalaluthien/campaign-base/issues/382>, its NOTEs in order.

## Composition

An HTML page.

- **C1** One local file: CSS, JS and SVG inline, nothing fetched, so it opens
  from `file://` with no connection; a library only for what SVG or CSS
  cannot draw, and then inlined. A Claude artifact follows the `Artifact`
  tool's own rules instead. `all` · 1.1, 2.1, 2.4
- **C2** Its facts read with script not run, from the markup or from one
  `<script type="application/json">` block. `all` · 1.1, 1.3
- **C3** One kind word from § Kinds on `<body class>`; a decision page is
  `<body class="doc decision-page">`. `all` · 1.1
- **C4** `main`, `nav`, `article`, `section`, `figure` and `time` for what
  they name; headings in order; a native element before an ARIA role; every
  control worked from the keyboard, focus visible; text contrast 4.5:1; motion
  stops under `prefers-reduced-motion`. `all` · 2.1, 3.4
- **C5** With script off, a `doc`, `view` or `dashboard` reads whole, and a
  `ui` shows its current state and names the actions that need script.
  `all` · 3.4
- **C6** Honours `prefers-color-scheme`, and `body` paints its own
  background. `all` · 2.1
- **C7** `<meta name="viewport" content="width=device-width">`; reflows at
  320 px with no sideways page scroll; only a table, a diagram or a code block
  overflows, inside its own scroll box. `all` · 1.2, 2.1
- **C8** Reading order is priority order, conclusion first; secondary
  material sits behind a labelled control, two disclosure levels at most.
  `all` · 1.1, 3.1
- **C9** Every claim is one click from its source. `all` · 1.1, 1.4

## Markdown

A `doc` in markdown.

- **M1** CommonMark plus GFM tables, task lists, strikethrough and autolinks;
  a callout is `> [!NOTE]`, a diagram a `mermaid` fence; C8 and C9 hold here
  too. `doc` · 2.2

## Visualisation

`CLAUDE.md` § Visual encoding comes first, for every page and every reply.

- **V1** Overview first, then zoom and filter, then details on demand.
  `all` · 3.1
- **V2** Status shows: what is shown, as of when, whether it is loading; an
  error names the way out. `dashboard` · 3.1
- **V3** One screen with no scroll at desktop width, its tiles stacking on a
  phone (C7); every number beside its target or prior; a page of links is not
  a dashboard. `dashboard` · 1.2, 3.2
- **V4** Lie factor within 0.95-1.05: a bar's axis starts at zero.
  `chart` · 3.2
- **V5** The compared quantity takes the strongest channel free -- position,
  then length, angle, area, hue -- so no pie where a bar would do; no
  decoration, and non-data ink only just visible. `chart` · 3.2
- **V6** Hue for a category, one hue's lightness for a quantity; colour only
  where it means something; never a red-green pair. `chart` · 3.2
- **V7** Compared series share axes, side by side. `chart` · 3.2
- **V8** A table to look a value up, a graph to see a pattern. `chart` · 3.2
- **V9** A title naming the diagram's type and scope; a key; every element
  named and typed; every line one-way and labelled. `diagram` · 3.3
- **V10** No boundary partner, direction, protocol, level, second concern or
  source left out. `diagram` · 3.3
- **V11** One symbol per concept, few symbol kinds, and a symbol's look
  suggests its meaning. `diagram` · 3.3
- **V12** A diagram only where position carries meaning; a sequence with no
  spatial relation is a list. `diagram` · 3.3

## What the check refuses

`hooks/check-document-kind.py`, a `PostToolUse` hook: an `.html` under
`docs/` whose `<body class>` carries no kind word, or two. It allows with 0
and refuses with 2; any other code is its own failure and refuses nothing.
Every other rule here is a reviewer's.
