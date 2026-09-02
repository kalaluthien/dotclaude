# Page HTML

Read at step 6, when the file is built. Fixes the page skeleton, the CSS
baseline, the table rules, and every component that is markup rather than
drawing.

- [Skeleton](#skeleton)
- [CSS baseline](#css-baseline)
- [Tables](#tables)
- [Do and do-not pair](#do-and-do-not-pair)
- [Chips and badges](#chips-and-badges)
- [Typed record](#typed-record)
- [Icon callout](#icon-callout)
- [Source citation](#source-citation)
- [Toggle](#toggle)
- [Keyed legend](#keyed-legend)

## Skeleton

Copy this whole shape. Three head lines are load-bearing and silently break
the page when dropped: `charset` keeps the box-drawing characters, the Korean
in a subject, and a quoted glyph from turning into replacement characters;
`viewport` stops a phone from laying the page out at 980 px, which throws
away the 42rem measure and every stacking rule below; `lang` tells a screen
reader which language to speak.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Run sequence</title>
<style>
  …the CSS baseline…
</style>
</head>
<body>
<article>

  <h1>Run sequence</h1>
  <dl class="provenance">
    <dt>Doctype</dt>  <dd>explanation</dd>
    <dt>Question</dt> <dd>one sentence, the question the page answers</dd>
    <dt>Updated</dt>  <dd>2026-08-15</dd>
  </dl>

  <h2>First section</h2>
  …

</article>
</body>
</html>
```

The page carries one `<style>` element, no external asset, and no script. A
figure whose subject is Korean keeps `lang="en"` on `<html>` and takes
`lang="ko"` on the element that holds the Korean.

## CSS baseline

```css
:root { --ink:#111; --mute:#555; --hair:#e4e4e4; --wash:#f4f4f4; }
html { font-size: 16px; }
body { max-width: 42rem; margin: 0 auto; padding: 4rem 1.5rem 8rem;
       background: #ffffff; color: var(--ink);
       font-family: system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
       line-height: 1.55; overflow-wrap: break-word; }
h1 { font-size: 2rem; line-height: 1.15; margin: 0 0 .9rem; font-weight: 700; letter-spacing: -.01em; }
h2 { font-size: 1.25rem; margin: 3rem 0 .5rem; font-weight: 700; }
h3 { font-size: 1rem; margin: 2rem 0 .3rem; font-weight: 700; }
h4 { font-size: .95rem; margin: 0 0 .4rem; font-weight: 700; }
p, li { margin: .6rem 0; }
ul, ol { padding-left: 1.2rem; }
ol.steps { padding-left: 1.6rem; }
ol.steps > li { margin: 1.3rem 0; }
ol.steps > li::marker { font-weight: 700; }
ol.keys { list-style: none; padding-left: 0; margin: 1rem 0; }
ol.keys > li { display: grid; grid-template-columns: 1.6rem 1fr; gap: .6rem; margin: .8rem 0; }
/* A grid track sizes to its longest unbreakable token unless it may shrink,
   so a legend item holding a path would push the page sideways. The <div> is
   the wrapper a legend item takes when it separates its statements: two
   children of the <li> would land the second one in the numeral column. */
ol.keys > li > p, ol.keys > li > div { min-width: 0; }
ol.keys > li > p, ol.keys > li > div > p { margin: 0; }
ol.keys ul { margin: .3rem 0 0; padding-left: 1.05rem; }
ol.keys ul li { margin: .2rem 0; }
.k { display: inline-flex; align-items: center; justify-content: center; width: 1.45rem; height: 1.45rem;
  border: 1px solid var(--ink); border-radius: 50%; font-size: .72rem; font-weight: 700; }
a { color: #14459b; text-decoration-color: #9bb0d8; }
code, pre, .provenance dd, .src { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .85em; }
pre { overflow-x: auto; background: var(--wash); padding: 1rem; line-height: 1.45; margin: 1.4rem 0; }
.src { color: var(--mute); }
table { border-collapse: collapse; width: 100%; margin: 1.4rem 0; font-size: .9rem; }
th, td { text-align: left; vertical-align: top; padding: .45rem .8rem .45rem 0; border-bottom: 1px solid var(--hair); }
th { font-weight: 700; }
tr.grp td { background: var(--wash); font-weight: 700; font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; }
/* Three columns of short values fit the narrow measure, so no table stacks
   into label-value rows and none pans out of view. A table that would need
   either is the wrong component. */
@media (max-width: 42rem) {
  table { font-size: .85rem; }
  th, td { padding-right: .5rem; }
}
.provenance { display: grid; grid-template-columns: max-content 1fr; gap: .15rem 1rem;
  margin: 0 0 2.4rem; font-size: .85rem; color: var(--mute); }
.provenance dt { font-variant: small-caps; letter-spacing: .04em; }
.provenance dd { margin: 0; }
figure { margin: 2.2rem 0; }
figure svg { display: block; width: 100%; height: auto; }
figure pre { margin: 0; }
figure.pan { overflow-x: auto; }
figcaption { margin-top: .7rem; font-size: .85rem; color: var(--mute); line-height: 1.5; }
.figure-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: 1.2rem; margin: 2.2rem 0; }
.figure-row figure { margin: 0; }
table.filemap td { border-bottom: none; padding: .12rem .8rem .12rem 0; }
table.filemap td:first-child { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: .85em; white-space: pre; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; margin: 1.4rem 0; }
.do, .dont { border: 2px solid var(--ink); padding: .8rem 1rem; }
.dont { border-style: dashed; }
.do h4::before { content: "\2713\00a0"; }
.dont h4::before { content: "\2715\00a0"; }
/* One typed record per term: a name bar, then a fixed field set. The field
   column is the record's type, so every record of one kind repeats it. */
.recs { display: grid; gap: .9rem; margin: 1.4rem 0; }
.rec { border: 1px solid var(--ink); }
.rec-n { margin: 0; padding: .35rem .75rem; background: var(--wash);
  border-bottom: 1px solid var(--ink); font-weight: 700; font-size: .92rem; }
.rec-t { font-weight: 400; color: var(--mute); font-size: .78rem; }
.rec dl { display: grid; grid-template-columns: max-content 1fr; gap: .25rem .8rem;
  margin: 0; padding: .55rem .75rem .65rem; font-size: .9rem; }
.rec dt { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .74rem;
  color: var(--mute); padding-top: .22rem; white-space: nowrap; }
.rec dd { margin: 0; min-width: 0; overflow-wrap: anywhere; }
.rec dd ul { margin: .1rem 0 0; padding-left: 1.05rem; }
.rec dd li { margin: .15rem 0; }
.ct { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .72rem;
  border: 1px solid var(--ink); border-radius: 3px; padding: 1px 4px; white-space: nowrap; }
.hum { display: inline-flex; align-items: center; gap: .3rem; font-size: .8rem;
  border: 1px solid var(--ink); border-radius: 11px; padding: 1px 8px; }
/* No nowrap here, unlike the count chip: a count is a numeral and one noun,
   while a value long enough to wrap must wrap rather than push the page
   sideways. */
.chip { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .72rem;
  background: var(--wash); border-radius: 3px; padding: 1px 5px; }
.callout { display: grid; grid-template-columns: 1.5rem 1fr; gap: .7rem; align-items: start;
  background: var(--wash); border-left: 3px solid var(--hair); padding: .8rem 1rem; margin: 1.4rem 0; }
.callout .g { font-size: 1.05rem; line-height: 1.35; }
.callout p { margin: 0; font-size: .92rem; }
.callout strong { font-weight: 700; }
details { border: 1px solid var(--hair); border-radius: 3px; padding: .45rem .9rem;
  margin: 1.2rem 0; font-size: .92rem; }
details summary { cursor: pointer; font-weight: 600; font-size: .92rem; list-style: none; }
details summary::-webkit-details-marker { display: none; }
details summary::before { content: "\25B8\00a0\00a0"; color: var(--mute); }
details[open] summary::before { content: "\25BE\00a0\00a0"; }
details[open] summary { margin-bottom: .5rem; }
/* Last, so it wins over the two-column .pair declared above. */
@media (max-width: 42rem) { .pair { grid-template-columns: 1fr; } }
```

The type split carries a signal a reader learns once: monospace text is
copyable, and sans text is not. `--ink` takes the body text, every box
border, and every solid arrow. `--mute` takes a caption, a role comment, and
an axis label. `--hair` takes a table cell border, and `--wash` takes the
ground under code and under a group header row.

## Tables

**A table carries at most three columns, and every cell is a short value.**
Three short columns fit the narrow measure as a table, so nothing stacks and
nothing pans. There is no `class="stack"` and no `data-label`: a stacked row
prints one label above each value, and repeating that per item is the
label-value form `components.md` rules out. Content that wants a fourth
column, or a cell holding a sentence, is not a table — route it to keyed
option panels or a figure.

A group header row replaces a yes-or-no column. Nine flat rows with a
yes-or-no column make a reader sort them; three groups of three state the
sorting as the answer.

```html
<tr class="grp"><td colspan="3">Settled by the repository</td></tr>
<tr><td>explanation</td><td>how does it work</td><td>Question</td></tr>
```

## Do and do-not pair

Two panels, once per page. The dashed border carries the same meaning it
carries in a drawing, so a reader who learned it in a figure does not learn
it again.

```html
<div class="pair">
  <div class="do"><h4>Brief that names the paths</h4><p>…</p></div>
  <div class="dont"><h4>Brief that names no readable source</h4><p>…</p></div>
</div>
```

## Chips and badges

Three inline marks, each with its own job. Rule O in `draft-rules.md` says
where each one is owed.

```html
<span class="ct">4&times; entrypoint</span>
<span class="chip">spec/</span> <span class="chip">Open</span>
<span class="hum">a person writes the brief</span>
```

- **Count chip**, bordered. A number and the noun it counts. It states the
  size of a complete set, so a reader knows what a full set looks like before
  reading the members.
- **Value chip**, tinted and unbordered. One state, status, mode, or doctype,
  inline in a sentence. Rule O gives the test that keeps a copyable token in a
  code span instead. The border is what separates a quantity from a value at a
  glance, so the two never trade styles.
- **Human badge**, rounded. The one transition no code performs, and nothing
  else.

## Typed record

One `div.recs` holds every member of one kind, stacked down the page. Each
member is a `div.rec`: a name bar, then a `<dl>` of the kind's fields in a
fixed order. `components.md` says when this component is the right one.

```html
<div class="recs">
  <div class="rec">
    <p class="rec-n"><code>tm-&lt;kebab-name&gt;</code> <span class="rec-t">term</span></p>
    <dl>
      <dt>half</dt>      <dd>domain</dd>
      <dt>is</dt>        <dd>a word the program is about</dd>
      <dt>instance</dt>  <dd>“balance”, how much water a plant still holds</dd>
      <dt>settled by</dt><dd>a code identifier, <code>PlantStatus.balance</code></dd>
      <dt>not</dt>       <dd>the code identifier that settles it</dd>
    </dl>
  </div>
</div>
```

A field label is a short lowercase word, in monospace, and it is a label
rather than a sentence. A `<dd>` holding more than one statement carries a
`<ul>`, which is what keeps a definition, an example, and a non-example from
collapsing into one paragraph. The name bar carries the term or its identifier
grammar, with the kind beside it in `.rec-t`.

## Icon callout

One glyph, one short paragraph, on the wash ground. It carries a warning, a
tip, or a definition aside that a reader must not skim past.

```html
<div class="callout">
  <span class="g" aria-hidden="true">⚠️</span>
  <p><strong>A pinned commit goes stale.</strong> A view describes the tree it
  was read from, never the tree the reader has.</p>
</div>
```

The block opens with a bold lead naming the point, then one sentence. The
glyph is the one place a page shows colour, under the same exception a
quoted system glyph takes: the emoji renders as the reader's system draws it.
The ground stays `--wash` and the rule `--hair`, so the block survives a
black-and-white print. A callout longer than three sentences is a section.

## Source citation

A citation is the file, the line, and the commit the claim was read from. The
commit pins the bytes forever, which is what makes a citation checkable. A
page standing on two repositories carries each file's own commit.

```html
<span class="src">scripts/campaign-tracker.py:101 @ 8fd13c1</span>
```

**A citation sits on a prose claim, a callout, or evidence inside a toggle,
and never inside a definition list or a figure legend.** A reader of a
definition is reading for the term, and a `path:12-34 @ 9e2a365` tail at the
end of that definition is a token nobody reads and everybody steps over. Where
the file itself is the example, name the readable path alone, with no line
range and no commit; the section's own prose carries the pinned citation for
the same claim.

A citation takes an `<a href>` only when the reader can open the target
without a login. These repositories are private, so a file citation stays
plain text. An `<a>` carries an anchor inside the page, or a sibling view in
the same `docs/` directory.

## Toggle

`<details>` is the one carrier for evidence a reader may want and does not
need: a raw command, a long enumeration, a transcript.

```html
<details>
  <summary>The tool lost twice on maintenance, which is why no option keeps a model</summary>
  <ul>…</ul>
</details>
```

**The summary line reads as a claim, never as a label.** "Evidence" and
"Details" name a genre and say nothing; the sentence above says what a reader
learns by opening it, so a reader who never opens it still gets the finding. A
page with nothing to collapse writes none.

## Keyed legend

A figure's legend is `ol.keys`, whose circled numerals repeat the numerals
drawn in the figure. A guide's procedure keeps `ol.steps`, whose plain
numerals count actions a reader performs.

```html
<ol class="keys">
  <li><span class="k">1</span><p><strong>Read the source</strong> — stage. One sentence.</p></li>
</ol>
```
