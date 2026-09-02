---
name: writing
description: Writes one human-facing view document as a single self-contained HTML page under a repository's docs/ directory. Use when the request asks to explain how something works with diagrams (도식과 함께 설명해줘), to draw it like an IKEA manual (IKEA 매뉴얼처럼), to make it an HTML page and open it (html로 만들어서 열어줘), to write up how X works, or to lay a change out as a proposal page (제안서로 정리해줘). Not for a chart of measured data, a diagnosis, or a Markdown spec or report.
context: fork
agent: general-purpose
model: opus
background: false
effort: high
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Writing

One run writes one view. A view is a human-facing HTML page under a
repository's `docs/` directory. It is derived from the tree at a pinned
commit, and it goes stale. Staleness is its normal state, not a defect. A
specification (`.md`) is normative and this skill never writes one. The
fields a machine reads off a view are declared in `references/doctypes.md`.

The run is finished when all four hold:

- one `.html` file exists at the output path
- every section whose subject is a relation carries one component
- `scripts/render-check.py <output>` exits 0
- nothing else in any repository changed

## Fork contract

This skill runs in a fork. The fork holds no conversation history. No user
answers a question. The working directory is inherited.

1. Read the paths in the brief. They are readable.
2. Every claim comes from a file you read. Memory is not a source.
3. A brief with no readable source ends the run: return
   `STATUS: INSUFFICIENT-INPUT`, name what is missing, and write no HTML. The
   `proposal` doctype takes one exemption. Its TO-BE half may stand on the
   brief alone. Its AS-IS half still needs a readable source, so a proposal
   brief with no readable source ends the run too.

## The brief

| field | what it carries | which step consumes it |
|---|---|---|
| doctype | `explanation`, `guide`, or `proposal` | 0 |
| subject | what the view is about | 0, 2 |
| sources | the paths to read | 1 |
| target | a repository root; the view lands in its `docs/` | 0, 1, 6 |
| reader | who reads the page | 2, 5 |

## Steps

**0 · Fix the doctype and the output path.** Default to `explanation` when
the brief names no doctype. A request that belongs to another skill exits
here: write no HTML and return `STATUS: INSUFFICIENT-INPUT` naming the route.
Doctypes, the exits, and the provenance fields: `references/doctypes.md`.

The output path is `<target>/docs/<slice>.html`. The brief may name the
slice; otherwise derive it from the subject per the naming rule in
`references/doctypes.md`. Then resolve it against what the store already
holds:

- Read `<target>/docs/INDEX.md` and list `<target>/docs/*.html`.
- A document already covering this subject is the output path, and the run
  is a rewrite. One subject is one file, so a rewrite replaces it in place
  and `INDEX.md` keeps the one line it has.
- When the derived path holds a document whose `Question` or `Goal` names a
  different subject, stop. Return `STATUS: INSUFFICIENT-INPUT`, name both
  subjects, and write nothing. Overwriting would destroy an unrelated view.

**1 · Read the source.** Read the subject's entry point, every module it
calls, its configuration, and the definition of what starts it. Where the
subject writes a log, read the newest lines. A behaviour a document claims
and the code denies is not a fact.

Pin each source to its own repository: run
`git -C <that repository> rev-parse --short HEAD` once per repository a
source comes from, and give each citation the commit of the repository the
file sits in. Run `date +%F` for the `Updated` field. On a rewrite, read the
document at the output path: its content is a source, its structure is not.

**2 · Partition the subject.** Split it into 4 to 7 sections that neither
overlap nor leave a gap. Every fact gets exactly one home. A fact that fits
two sections means the split is wrong. The reader field sets the depth: a
section the named reader cannot use is one section too deep, and a
non-engineer reader collapses two mechanism sections into one.

An explanation and a proposal each hold negative space: what does not start
the subject, and what the subject does not change. Nothing on the page may
let a reader infer a trigger or an effect the code does not have. Rule L
never trims it. An explanation gives it its own section. A proposal carries
it in the "what this does not do" section its section order already requires,
and a guide walks one procedure and owes none.

A proposal takes its whole section order from `references/doctypes.md`, which
fixes what comes first and what comes last.

**3 · Route each question.** Each section question routes to one component
from the vocabulary in `references/components.md`. Never draw two components
of one kind for one content.

**4 · Draw before you write.** Draw each figure before drafting its prose.
Each drawing carries its numbered circles and its legend inside the same
`<figure>`. A label inside a drawing stops at five words. The text budget is
one paragraph per legend key. Markers, geometry, and label placement:
`references/svg-rules.md`.

**5 · Draft the prose.** The draft passes rules A to O, one worked example
per rule: `references/draft-rules.md`. The section leads with its figure, the
prose follows as keyed items, and every definition, rule, and mechanism shows
one concrete instance from a file the run read. Every sentence obeys the caps and the
word lists in `references/plain-writing.md`. The reader field sets the
register: explain in plain words every term the named reader does not already
use.

**6 · Build one file.** One HTML file, white ground, black text, no external
asset, no script, no build step, and inline SVG for every figure. The page
opens from `file://` complete and prints to paper without a change. The head
skeleton, the CSS baseline, the table rules, and the citation form:
`references/page-html.md`. Write the file at the output path fixed in step 0.

**7 · Render and look.** The script sits in the skill directory, not in the
working directory the fork inherited, so call it by its installed path. Send
the images to the session scratchpad directory named in your environment;
without `--out` they land in a temporary directory, which the script prints.

```bash
~/.claude/skills/writing/scripts/render-check.py <output> --out <scratchpad>
```

It renders the page twice, at the desktop measure and at the narrow measure
the owner reads on a phone, crops each image to the drawn page, and checks
the page opening, the SVG markup, and the figure geometry. It prints the two
PNG paths, the layout width it measured, and one verdict line.

Read both PNGs back. This is the one check that is able to fail. Count five
things:

1. components against sections
2. paragraphs outside a figure
3. each caption and each label against what it labels
4. each sentence against the caps and the word lists read at step 5
5. every table row and every glyph against the set it claims to be complete

Then fix and re-run. Three failures share one loop and one bound: a label
that touches another mark, a `check-figures` finding, and a marker used but
not defined. The loop runs at most three passes. After the third pass, stop
and return `STATUS: PARTIAL` naming the figure that still fails and the
finding it still carries.

**8 · Open it.** Run `open <output>` when the brief asks for it. A brief that
does not ask gets no `open` call.

## Return message

Only this message reaches the main session. Every file read and all tool
output die with this context.

```
STATUS: <one value>

## Output
the absolute output path, then the section list

## Findings the reader needs
3 to 6 facts, each with the file it came from

## Grounding
every file the run read

## Residual uncertainty
the highest-risk claim on the page, and what would settle it

## Next action
one action for the main session
```

| status | when it applies |
|---|---|
| `COMPLETE` | every section whose subject is a relation carries one component, and `render-check.py` exited 0 |
| `PARTIAL` | the file stands, and one figure still fails after three passes |
| `INSUFFICIENT-INPUT` | no readable source, a path collision, or a request that routes elsewhere. No HTML written. |

`## Grounding` is a superset of every file this message names elsewhere.
`## Next action` names the caller's work, which the run never does: the
`INDEX.md` line for a new document, and the commit that lands both.

## Gotchas

- A view carries no script, so a request that needs one moving part is the
  wrong deliverable. Say so instead of writing a page that cannot do it.
- A decision the sources do not record is reported back, never written into
  the page. A view decides nothing.
- Headless Chrome does not lay out below 500 CSS units. `render-check.py`
  measures the width it got and prints it, so a narrow render that reads as
  text cut off at the right edge is the instrument, not the page.
- `render-check.py` captures at most 16000 pixels of height, so a long page fails
  at phone width with nothing wrong with it. Re-shoot taller and read the tail
  before believing the failure.
