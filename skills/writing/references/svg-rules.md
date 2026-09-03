# SVG rules

Read at step 4, when the figures are drawn. Fixes the width limits, the
markup rules, the geometry, and the five SVG construction recipes.

- [Width and legibility](#width-and-legibility)
- [Five markup rules](#five-markup-rules)
- [Geometry](#geometry)
- [Label placement](#label-placement)
- [Figure skeleton](#figure-skeleton)
- [Construction recipes](#construction-recipes)

## Width and legibility

The page measure is 42rem, and a phone shows about 312 px of it. Three limits
follow. `scripts/check-figures` enforces all three, and
`scripts/render-check.py` runs it.

1. **Annotation floor, 10 viewBox units.** A 10-unit label in a shrinking
   360-unit figure renders at 8.6 px, which clears the 8 px floor. A 9-unit
   label renders at 7.8 px and no reader can read it. The floor is the font
   size, never the label width, so it holds at any viewBox.
2. **Pan threshold, 360 viewBox units.** A figure of 360 units or less
   shrinks to the measure and needs nothing more. A wider figure carries
   `class="pan"` on the `<figure>` and an inline `min-width` on the `<svg>`
   equal to the viewBox width in px, so it draws at full size instead of
   shrinking.
3. **Maximum drawn width, 620 viewBox units.** This is the desktop measure.
   Split the figure or draw it down the page instead of going wider.

Draw a figure down the page rather than across it. The viewBox height has no
limit. Pick the narrowest viewBox that holds the drawing.

```html
<figure class="pan">
  <svg viewBox="0 0 480 300" style="min-width:480px" role="img" aria-labelledby="f2t">
```

## Five markup rules

1. **One marker set inside every `<svg>`, with an id suffixed per figure.**
   Inline SVG shares one id namespace with the whole page, so a second figure
   that reuses `arrow` points at the first figure's marker, and the
   arrowheads vanish with no error. Write `arrow-stages`, never `arrow`.
   `orient="auto-start-reverse"` lets one marker serve a left-pointing and a
   right-pointing arrow.

   ```html
   <marker id="arrow-stages" viewBox="0 0 8 8" refX="7" refY="4"
           markerWidth="7" markerHeight="7" orient="auto-start-reverse">
     <path d="M0,0 L8,4 L0,8 z" fill="currentColor"/>
   </marker>
   ```

2. **`viewBox` only, no `width` and no `height`.** The CSS scales it. The
   inline `min-width` of a panning figure is the one exception.
3. **Solid for a normal transition, dashed for a secondary path.** A
   secondary path is a return after a human action, a side effect that
   re-enters the flow, or an element a proposal has not built yet. Dashed
   keeps that one meaning in every figure of the page.
4. **A non-text stroke needs 3:1 contrast.** `#111` on `#ffffff` passes.
   Never draw a line lighter than `#767676`.
5. **A keyed circle sits on a box corner.** Draw the box, then the circle
   with a white fill, then the numeral, so the border does not cross the
   digit. The circle reads as a badge and costs no space inside the box.

   ```html
   <circle cx="54" cy="20" r="11" fill="#ffffff" stroke="currentColor" stroke-width="1.2"/>
   <text x="54" y="20" dy=".35em" text-anchor="middle" font-size="11" font-weight="bold">1</text>
   ```

Text and solid strokes use `currentColor`, so the ink follows the body
colour. A muted detail line inside a box is `currentColor` at
`opacity=".65"`. A secondary line is `stroke="#767676"`. Use no other colour
unless the brief asks for one, because a page that carries meaning in colour
loses that meaning in a black-and-white print. One exception: a glyph the
system itself renders is not a colour choice. ✅ is green because Slack draws
it green, and the page quotes it.

## Geometry

| what | value |
|---|---|
| box or arrow stroke width | 1.4 |
| keyed circle stroke width | 1.2 |
| lifeline or leader stroke width | 1 |
| secondary path dash array | `5 4` |
| lifeline dash array | `4 4` |
| in-box title baseline | about 30 units below the box top |
| in-box line pitch | 18 units |
| in-box text | at most 3 lines, each under 22 characters |
| keyed circle radius | 11 units |
| label clearance | at least 8 units from every other mark |
| label width estimate | 0.6 × font size per character, 0.66 when bold |
| lifeline pitch | at least 180 units |
| arrow pitch | at least 34 units |
| actor header box | 34 units tall |

**No text touches another mark.** Estimate a label's span with the width
estimate above, then check that span against every neighbouring box, line,
and text. When the band is too narrow, stack the label, shorten it to its
noun, or replace it with a keyed numeral. Never shrink the font to force a
fit, because the 10-unit floor holds first.

## Label placement

1. In-box text is a bold title, then at most two monospace lines.
2. An arrow label centres on the arrow with `text-anchor="middle"`, or
   anchors to the near end with `text-anchor="end"`. A label started at the
   arrow tail runs past the far element.
3. Both lines of a two-line label sit on the same side of the line, 14 units
   apart. Never one line above and one below.
4. An edge label sits beside the line, not on it: `text-anchor="end"` to the
   left, the default anchor to the right, 8 units clear.

## Figure skeleton

The `<figcaption>` is a direct child of `<figure>`; a wrapper `<div>` breaks
the association. The legend sits inside the `<figure>` too, which keeps the
drawing and its key one unit. A visible legend serves a reader with a
cognitive disability, which a hidden `sr-only` description does not.

```html
<figure id="fig-run">
  <svg viewBox="0 0 320 235" role="img" aria-labelledby="f1t">
    <title id="f1t">Three stages of one run, from the source read to the render check</title>
    …
  </svg>
  <figcaption>One run at the pinned commit, from the source read to the
    render check.</figcaption>
  <ol class="keys">
    <li><span class="k">1</span><p><strong>Read the source</strong> — stage. One sentence.</p></li>
  </ol>
</figure>
```

Every line in a drawing is unidirectional and labelled with its intent, never
a bare "uses". A line between two deployable things names the protocol. A
frame is a thin box labelled with what the set is, and one edge at the frame
stands for that edge to every member; the frame takes its own elements row.

## Construction recipes

**Keyed step chain.** At most four stages, drawn down the page where that
keeps the figure under 360 units. Each box carries a circled numeral on its
border, a bold title of at most three words, and at most two monospace detail
lines. The forward edge is solid. A feedback edge is solid and labelled with
its intent. An exit outcome is bare text outside any box.

**State machine.** A double border marks a final state, in every figure of
the page, and nothing else takes a double border. Mark every final state, not
the one that feels special.

**Three-column mapping.** The columns are input, agent, and result. State the
count on each side. A reader sees "four changes, two calls" at a glance and
cannot see it in a table.

**Sequence diagram.** One header box per actor at `y=16..50`, centred on its
lifeline x. A dashed lifeline from `y=50` to the last arrow plus 20. One
horizontal arrow per step, with the keyed circle 22 units after the tail. A
self-call is a three-segment path: out to `x+30`, down 16, back to the
lifeline.

**Location map.** One vertical bar per artifact at `x=40`, width 26, height
scaled to the line count. Axis labels every 200 lines, `text-anchor="end"` at
`x=34`. One tick per item on the bar, 10 units wide, at
`y = top + line / total × height`. Group by fault kind, and give each group
one fill: solid, hatched, open. A leader from each tick to a keyed circle in
the right column, rows 26 units apart. A count badge per group in the legend
row under the bar. Two ticks closer than 6 units merge into one tick with a
`2×` badge, and the grouped table keeps both rows.
