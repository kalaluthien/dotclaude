# Components

Read at step 3. Routes one section question to one component, and fixes what
each component must show.

- [The vocabulary](#the-vocabulary)
- [Choosing a form](#choosing-a-form)
- [The elements carrier](#the-elements-carrier)
- [File map](#file-map)
- [Specimen anatomy](#specimen-anatomy)
- [Typed record](#typed-record)
- [Keyed option panels](#keyed-option-panels)
- [Not in this vocabulary](#not-in-this-vocabulary)

## The vocabulary

Route each section question to exactly one component. Never draw two
components of one kind for one content.

| the reader's question | component | its mission | its form |
|---|---|---|---|
| **Page-level figures, 7** | | | |
| Which parts exist, and where? | File map | Locate each part, and state its role in six words | below |
| Which option wins, and why? | Keyed option panels | One panel per option, and the verdict in the prose | below |
| What happens in one run? | Keyed step chain | The order, and the two ends | `svg-rules.md` |
| Which states exist, and how does it move? | State machine | The legal transitions, and their writers | `svg-rules.md` |
| Which input produces which output? | Three-column mapping | The count on each side | `svg-rules.md` |
| Who acts, in which order? | Sequence diagram | The channel between the actors | `svg-rules.md` |
| Which items share a fault, and where do they sit? | Location map | The count per group, and the position of each item | `svg-rules.md` |
| **Components below the figure level, 9** | | | |
| What triggers it, and what does not? | Grouped table | Coverage, sorted into named groups | `page-html.md` |
| Which of two paths is right here? | Do and do-not pair | The path that looks legal and is not. Once per page | `page-html.md` |
| Which fields does one record hold, and from where? | Specimen anatomy | Replaces a code sample plus a field table | below |
| What must the reader not skim past? | Icon callout | One warning, tip, or aside, in one glyph and one sentence | `page-html.md` |
| Which step does no code perform? | Human-action badge | That transition, and nothing else | `page-html.md` |
| How many parts are in this set? | Count chip | The complete set | `page-html.md` |
| Which state or mode is this? | Value chip | One member of a named set, inline in a sentence | `page-html.md` |
| What is this term, field by field? | Typed record | One fixed field set, repeated across every member of the kind | below |
| What backs this, for a reader who wants it? | Toggle | The evidence, under a summary that already states the finding | `page-html.md` |
| Where did this claim come from? | Source citation | The file, the line, and the pinned commit | `page-html.md` |

## Choosing a form

The form follows the data and the reader's task, never the domain noun. State
the item count and the task first.

- A relation that is not genuinely two-dimensional is a table or a list, and
  the section owes no drawing. A list drawn as boxes is worse than a list.
- Three or more parallel facts are a table, never prose. A table carries at
  most three columns, and every cell is a short value a reader compares at a
  glance. A fourth column, or a cell holding a sentence, a rationale, or a
  verdict, means the content is not a table: route it to keyed option panels
  or to a figure.
- A straight-line sequence with no branch and no loop is `<ol class="steps">`.
- Text with no shape at all still does not stay as running paragraphs. A
  point a reader must not skim past is an icon callout, evidence a reader may
  want is a toggle, and every count, path, state, and field value inside a
  sentence is a chip. Prose then carries the connections between them and
  nothing else.
- One figure carries one relation and at most seven elements. A denser
  subject becomes a row of small panels in a `div.figure-row`, each panel
  with its own caption, read left to right, sharing one elements table under
  the row.
- Prose that describes a shape a figure could draw is a defect.

## The elements carrier

Every figure names its parts in one of two ways, and never in both.

- A table under the drawing, with a row per element: the name, the type, and
  a one-line description.
- A numbered legend keyed to the figure's numerals, same three parts per
  entry. Order is the legend's extra claim over the table.

Four components name their own parts in place and take no key: the file map
names them in its role column, the do-and-do-not pair in its two headings,
the grouped table in its group header rows, and the specimen anatomy on its
leader lines. The five SVG figures all take numbered circles and a legend.

**The caption is one or two plain sentences saying what the figure shows, and
it never carries the key.** A caption that spells out "circled numeral — one
stage; dashed box — an artifact nobody has built" restates the carrier
directly under it, and the reader pays for the same list twice. Write the
caption a paper writes: what the drawing shows, then at most one sentence for
a convention the drawing alone cannot state, such as what a dashed mark means.
Rule G in `draft-rules.md` fixes the rest. A figure may carry invented
illustrative values only when its caption says so. A file map and a specimen
never invent.

## File map

A directory whose nesting is part of the answer. Use it at depth two or more,
where a child's role depends on its parent. A flat directory is a plain
table.

```html
<figure id="fig-map">
  <table class="filemap">
    <tbody>
      <tr><td>writing/</td><td>the skill directory</td></tr>
      <tr><td>├── SKILL.md</td><td>entry point, steps 0 to 8</td></tr>
      <tr><td>└── references/</td><td>one file per step that needs one</td></tr>
    </tbody>
  </table>
  <figcaption>The skill directory at the pinned commit: one entry point and
    five references, with each part's role beside it.</figcaption>
</figure>
```

The table aligns the two columns, so no hand-counted spaces drift, and the
role column is the map's own elements carrier. Transcribe every path from the
tree at the pinned commit. Counts go in the caption as a sentence.

## Specimen anatomy

A text artifact whose field order is the grammar: a filename pattern, a log
line, a message format, a flag string. Put one real instance from the pinned
commit in a `<pre>`, rule each field with box-drawing characters on the lines
below, and end each leader at the field's name alone. Every ruler character
sits under a character of the field it spans. The meaning lives in the
elements carrier under the figure.

```
agent-config-scopes.html
└─┬─┘ └─────┬─────┘ └─┬┘
  │         │         └── extension
  │         └── slice
  └── plane
```

An artifact whose fields name themselves, such as JSON or `key=value`, is a
table and not a specimen.

## Typed record

A term of art whose parts a reader must hold at once: what it is, what it
holds, one instance, one non-instance. One record per member of the kind, each
with a name bar and the same field set under it. The markup and the CSS are in
`page-html.md`.

The field set is the record's type, so every member repeats it in the same
order, and a member with nothing for a field still shows the field. A reader
who has learned one record can then read the next by position. Two kinds on
one page take two field sets: the members of a kind share theirs, and nothing
forces one set across kinds.

This is the one place a repeated label set is right, and `page-html.md` keeps
the shape out of tables. A definition is not a comparison, so the labels are
what the reader navigates by rather than a column they were denied. Use it for
a proposal's Domain section on the runs that owe one — `doctypes.md` makes it
conditional, and demands a definition, an example, and a counter-example per
term. Do not use it for options, whose component is keyed option panels.

## Keyed option panels

A comparison across options is a drawing plus numbered prose, never a matrix.
One `div.figure-row` holds one small panel per option, each panel keyed with
a circled numeral and carrying the shape of that option. Under the row, an
`ol.keys` legend carries one item per key: the option's name in bold, what
the option gives up, and its verdict.

The numerals in the panels and the numerals in the prose are one set, per
rule D. Four options are four panels and four paragraphs. An option killed by
an earlier decision keeps its panel, drawn dashed, and its paragraph carries
the reason it lost.

A reader on a phone reads a paragraph. The same content as a matrix becomes
one stacked block of repeated labels per option, which is the shape this
component exists to replace.

## Not in this vocabulary

Two shapes look like components and are not. Neither has a question in the
table above, so neither has a mission.

**A labelled summary box.** A bordered block may open a section. It carries
no genre label above its content — no `CONCLUSION`, no `SUMMARY`, no `NOTE`,
in any case or size. The section heading already says what the block is, so
the label states the genre twice and states the content zero times. The
bordered blocks this skill does draw, the do-and-do-not panels, take headings
naming their own content.

**Label-value rows carrying a comparison.** A row that repeats one label set
under every item compares nothing, because the values never sit side by side:
`Refutes / Maintenance / Verdict` under option one, then again under option
two, then again. Route a comparison to keyed option panels above, or to a
grouped table when the values really are short and flat. The typed record uses
the same shape for the opposite job — a reader who wants one term's fields, not
two terms ranked — so the fault is the comparison, never the repeated labels.

The second shape has one entrance left, and `page-html.md` closes it: a wide
table that turns itself into label-value rows at the narrow measure. There is
no stacking mechanism to reach, and a table caps at three short columns, so a
comparison cannot arrive at that shape by being wide.
