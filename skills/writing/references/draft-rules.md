# Draft rules

Read at step 5. The draft passes all fifteen. A to I are nine prohibitions,
so a writer who obeys them writes boxes, arrows, and nothing else. J to O are
the positive half, and they are what puts something on the page.

| | prohibition | | positive |
|---|---|---|---|
| A | No prologue and no colophon | J | The glyph, not its name |
| B | One block per set | K | Group a long enumeration |
| C | Bare noun phrase for a section name | L | The fewest components |
| D | One number set | M | One example per claim |
| E | Plain English | N | The figure leads, the prose follows |
| F | Exact scope in every name | O | A chip or a badge where one is owed |
| G | One component, one mission | | |
| H | No sentence that expires | | |
| I | No sentence about the document | | |

## A · No prologue and no colophon

The title and the provenance block are followed by the first section. Six
shapes carry the same fault: a subtitle, a scope note, a metadata table, a
source pin block, a summary paragraph, and a footer. A metadata table is a
prologue with a border, and a footer is a prologue at the other end. A commit
a reader needs belongs on the citation it pins, inline.

- Rejected: a kicker line above the title, a sentence under it saying what
  the page covers, a `Commit` field, and a Sources footer.
- Accepted: `<h1>`, `dl.provenance`, then section 1. Every commit sits on its
  own citation.

## B · One block per set

Show a set as one block: a file map for files, one figure plus a grouped
table for items. Never one card per member.

- Rejected: three bordered cards, one per doctype.
- Accepted: one grouped table, three rows, two group headers.

## C · Bare noun phrase for a section name

No article, no verb, no claim of importance.

- The loop → Run sequence. The article, and "loop" is the writer's metaphor.
- What it does not do → Run triggers. A sentence, and a negative framing.
- Parts → File map. Vague scope.
- Steps → merged into the figure legend. A second heading for one thing.

Banned words in a heading: `core`, `key`, `powerful`, `deep dive`,
`under the hood`, `magic`, `the real`, `essential`.

## D · One number set

The figure and the step list share one number set.

- Rejected: a figure keyed 1 to 4 above a legend numbered 1 to 6.
- Accepted: the same numerals in the drawing and in the legend.

## E · Plain English

One idea, active voice, no compound sentence. The caps, the twelve writing
rules, and the word lists are in `plain-writing.md`, which step 5 reads
beside this file.

## F · Exact scope in every name

Name the object and the property.

- Lifecycle → Notification state of a task record
- Events and States → Frontmatter change to Slack action
- Message sequence → Message sequence, one task from creation to report
- Frontmatter fields → Frontmatter fields of a task record

The test: read the heading alone, with no page around it. When it does not
say what object it is about, it fails.

## G · One component, one mission

Events go to a step chain, states to a state machine, actor order to a
sequence diagram. The caption states the mission as a fact about the system,
never as a fact about the drawing. It runs to at most two sentences and it
carries no key, because the legend under it already names every part.

- Rejected: "Figure 2 shows the lifecycle of a task."
- Rejected: "Keyed step chain. Key: circled numeral — one stage; dashed box —
  an artifact nobody has built; dashed arrow — a proposed link."
- Accepted: "`diffing` compares the old status value against the new one. It
  does not check the order, so a record can move from announced straight to
  done."

## H · No sentence that expires

Cut every sentence addressed to the person who asked, and every count or
state true only on the day of the read.

- Rejected: "Two failure modes are worth remembering, because both look like
  the service being broken. Four records are held right now."
- Accepted: the two mechanisms, stated as facts, inside the table that
  already covers that behaviour.

The test: when a code change or a new run can make it false while the
mechanism stays the same, it belongs in the return message.

## I · No sentence about the document

Cut the read path, the read date, the item count, the tool, and the re-pin
note. A source citation is not text about the document.

- Rejected: "This page was built by reading the three modules listed above."
- Accepted: the citation on each claim.

## J · The glyph, not its name

Show the glyph a reader sees. ✅ reaches the reader, and `white_check_mark`
is its name.

- `white_check_mark` → ✅
- `hourglass_flowing_sand` → ⏳
- `question` → ❓

Show the shortcode beside the glyph when a reader must type it or search for
it. Show the glyph alone when the reader only has to recognise it.

## K · Group a long enumeration

Group an enumeration of 6 or more rows, and name each group with a noun
phrase.

- Rejected: one table, nine rows, the yes rows and the no rows interleaved by
  no principle.
- Accepted: the same nine rows under three group headers.

The threshold is 6 rows, or 3 items where one grouping is the point. A group
of one is not a group: fold it into its neighbour, or drop the grouping.

## L · The fewest components

Use the fewest components that cover the subject. Five clauses:

1. One component per reader question. A section with two figures has two
   questions in it, or one redundant figure.
2. Reuse a kind before you add a kind. A new visual grammar for the same job
   makes the reader learn a second symbol set for nothing.
3. Merge a code sample plus a field table into one specimen anatomy.
4. Cut a component whose facts the neighbouring component already carries.
5. Prefer a table when the shape carries no information. A list of trigger
   inputs does not have a shape.

Rule L never trims the negative-space section.

## M · One example per claim

Every definition, every rule, and every mechanism is shown with one concrete
instance: a real file snippet, a real command with its output, a real record,
a real path. The instance comes from a file the run read, at the pinned
commit. The prose then connects the instances and adds nothing a reader
cannot check against one of them.

A section that states a concept and shows no instance is a defect, however
clear the sentence reads. A reader who does not already know the concept
cannot tell a correct statement from a wrong one, and a reader who does know
it learns nothing.

- Rejected: "A runner never edits the tree it checks."
- Accepted: the same sentence, then
  `scripts/check-figures <view.html>` with its two output lines, showing a
  run that reads and reports and writes nothing.

Two instances beat one where a term has an edge: show what the term covers,
then show the nearest thing it does not. Where a proposal owes a Domain
section at all, each definition in it carries both, per `doctypes.md`.

## N · The figure leads, the prose follows

A section opens with its figure, its file map, or its keyed panels. The prose
comes after, as keyed items tied to the numerals in the drawing, one item per
numeral.

Beyond the figure, its caption, its legend, and its keyed items, a section
carries at most two connective paragraphs. A third paragraph means the
section holds a second subject, or holds prose that a component should be
carrying.

- Rejected: four paragraphs describing a flow, then a drawing of the flow.
- Accepted: the drawing, its caption, one keyed item per stage, and one
  sentence connecting the section to the next.

## O · A chip or a badge where one is owed

A component no rule selects is never drawn, so three marks have a rule that
selects them.

- **A count chip** wherever the page states how many of something exist —
  every group in a file map, every side of a mapping, every set a reader
  might think is longer. Write `<span class="ct">4&times; entrypoint</span>`,
  not "there are four entrypoints".
- **A value chip** on every state name, status, mode, and doctype that sits
  inside a sentence. The test is one question: could the reader run, open, or
  paste this? A path, a command, an identifier, and a field name are things a
  reader copies, so they stay code spans. A command stays one only while it
  fits the source line: wrapped inside a span it pastes as two broken
  commands, so one that does not fit takes a block of its own. A value drawn from a set the page
  names elsewhere is a thing a reader scans for, so it takes the chip:
  `<span class="chip">Open</span>`, not `<code>Open</code>`.
- **A human badge** on the one transition no code performs. A page with no
  such transition carries none.

A page that states a number in words, or a state name in plain text, has
skipped a mark a reader scans for.

## P · A closed list states why it closes

An enumeration offered as complete carries the partition it came from, not a
count. A count is a tally, and a tally invites the next reader to add one more
without being able to say whether another remains.

- Rejected: "Two cases produce no check", then "Three cases produce no check".
  Each survived a review and each was one case short, because neither said what
  made the list end.
- Accepted: "Three cases, and they partition by *why* the run is absent" —
  followed by the three reasons, which between them admit no fourth.

The test is one question: could a reader add a fourth item without
contradicting anything the passage says? If yes, the passage is counting rather
than closing. A list that genuinely has no partition says "at least", and then
it is honest instead of wrong.

This applies where the list is normative and a reader acts on its
completeness. A list of examples closes nothing and needs none of this.

## Correct a sentence in place; do not write a truer one after it

A wrong sentence is not repaired by a better sentence three lines down. The
passage then carries both, and a reader who stops early — or who greps for the
old phrasing — gets the retired claim with nothing marking it retired. Worse,
each correction lengthens the passage that is already failing to be read.

Observed across five review rounds on one document: the model rule said "the
same model as the session launching it", was corrected by adding "so the
launcher's model is a floor", and then by adding a paragraph arguing the
absolute rule — three statements, two of them retired, none of them deleted.
The reviewer's summary is the rule: *the last two rounds each corrected a false
sentence by writing a truer one after it.*

Delete the wrong clause and write the right one in its place. If the wrong
version is worth preserving because being wrong is itself the lesson — a claim
that has now failed in two opposite directions — say so explicitly and mark it
as history, which is a different act from leaving it standing as current.

The symptom to grep for after any correction: the retired phrasing still
present. If it is, the correction was an addition.


## A rules document's bulk is usually its own changelog

**Before cutting a long document of rules, measure how much of it is history
rather than instruction.** Measured on one 1585-line instruction file: 416 lines
— 26% — were a paragraph saying what a rule replaced, when it was measured, or
which issue retired it. None of it changed a reader's next action, and version
control already held every word.

That share is invisible while you read, because each such paragraph *earned its
place* when it was written: somebody had just been burned and wrote down why.
The tell is the tense. A rule is in the present and addresses the reader; a
changelog entry is in the past and addresses whoever is about to re-open a
settled argument. Route it to the commit message that makes the change, and the
next reader who needs it will find it there with the diff attached.

The two other reliable sources of bulk in the same file: a rule restated beside
the tool that already decides it, and a section that summarises rules stated
elsewhere for the reader's convenience. Both are hand-kept copies, and both
drift. Cutting all three took the file to a third with no rule lost.


## Verifying a prose cut: only a meaning-reader finds a lost rule

**A keyword sweep cannot tell you whether a deletion lost a rule.** Cutting a
1585-line instruction file to 528, I checked my work by extracting every bolded
claim from the old file and testing each one's keywords against the new text. It
reported 38 unmatched, of which 37 were false positives, and it found **one** of
the twenty rules that were actually gone. A reviewer reading the two files for
meaning found the other nineteen in one pass.

The reason is structural, not a matter of a better regex. A rule survives the cut
in *reworded* form, so its keywords are present; a rule that is genuinely gone
often shares vocabulary with the paragraph that replaced it. The signal a sweep
reads and the property you care about are nearly uncorrelated.

So budget for a reading. Two things make that reading cheap enough to get: give
the reader the old file, the new file, and **the claim that each deleted rule is
now carried by a named mechanism** — a claim is falsifiable where "I cut
carefully" is not. And ask the single question ("was a live rule lost?") rather
than a list of angles, so the whole of the attention lands on the one failure a
deletion actually has.

The corollary for the writer: **state where every deleted rule went, in a table,
before anyone asks.** Building that table is itself the reading, and the rules
with no cell to go in are exactly the ones about to be lost.
