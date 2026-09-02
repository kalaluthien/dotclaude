# Doctypes

Read at step 0. Fixes the doctype, the provenance fields, the title, the
proposal additions, and the exits.

- [Three doctypes](#three-doctypes)
- [The page opening](#the-page-opening) — [the machine copy](#the-machine-copy)
- [Title and file name](#title-and-file-name)
- [Proposal mode](#proposal-mode) — [section order](#section-order), [Domain](#domain-only-when-the-proposal-moves-the-words), [a losing option](#how-a-losing-option-is-written)
- [Requests this skill does not serve](#requests-this-skill-does-not-serve)
- [What the run never writes](#what-the-run-never-writes)

## Three doctypes

| doctype | the reader's question | what it stands on | field it adds |
|---|---|---|---|
| `explanation` | how does it work, why is it this way, what shape does it have, what did the run measure | the tree at the pinned commit, a recorded decision, or a protocol another reader can re-run to the same numbers | Question |
| `guide` | how do I do it | one walk through the procedure at a known commit | Goal |
| `proposal` | what should change, and to what | grounded facts for the problem, and options for everything after | Status, Question |

An explanation and a guide are claims the repository can settle. A claim it
cannot settle is a defect in them. A proposal is the one doctype allowed to
describe what does not exist, and a drawing of a surface nobody has built
belongs to it.

Write the doctype value exactly as the machine copy below spells it.

## The page opening

The page opens with the title as `<h1>`, then the provenance block, then the
first section. Nothing else opens it: no kicker, no subtitle, no scope note,
no summary paragraph, and no footer. The `<h1>` and the `<title>` in the head
carry the same words, and a machine reads the title from the head.

```html
<h1>Run sequence</h1>
<dl class="provenance">
  <dt>Doctype</dt>  <dd>explanation</dd>
  <dt>Question</dt> <dd>one sentence, the question the page answers</dd>
  <dt>Updated</dt>  <dd>2026-08-15</dd>
</dl>
```

- A guide writes `Goal` in place of `Question`. Every doctype carries one of
  the two, because the docs surfaces draw it as the line under the title, and
  a view without one lists with a blank line.
- A proposal adds `Status` above `Question`, with one of three values:
  - `Open` — no decision is recorded yet.
  - `Accepted YYYY-MM-DD → <file>.md` — the acceptance is recorded in a spec,
    and the field points at it.
  - `Rejected YYYY-MM-DD, <reason>` — the reason travels with the rejection.
- `Updated` is today's date, from `date +%F`.
- `Reviewed` is a field this skill never writes. It says when somebody last read the document against the tree and found
  it still true. A re-render replaces the prose, so a review of the old prose
  vouches for nothing, and the page reads as never reviewed again. Never
  carry the field over from the document being rewritten.
- No `Commit` field. A commit a reader needs sits on the citation it pins, so
  a page standing on two repositories pins each one where it is used.

### The machine copy

The block below is the machine copy of the fields above. An entry's docs
checker parses it to decide what a view of each doctype must carry, so a
change to the fields is made here, in the same commit as the prose it
follows. It replaces the per-doctype template files this skill retired: an
entry that resolves a template path instead finds nothing and refuses every
view it is handed.

Required fields only. A view carrying more than the block names is left
alone, because a page that pins a commit or a build in its provenance is
answering its own reader, and the block cannot know which.

```json contract=doctype
{
  "contract": "doctype",
  "version": 1,
  "updated": "2026-08-20",

  "doctypes": {
    "explanation": { "fields": ["Doctype", "Question", "Updated"] },
    "guide":       { "fields": ["Doctype", "Goal", "Updated"] },
    "proposal":    { "fields": ["Doctype", "Status", "Question", "Updated"] }
  }
}
```

## Title and file name

The title is a noun phrase of one to three words. It carries no state, no
verdict, and no measurement, because updating the page in place would make
any of those false. It names the slice the page owns, never the genre, which
the directory already carries. It stays the same across re-renders, and a
rewrite never renames a document on its own.

The file name is that same slice in kebab-case, with `.html`. A repository's
file follows that repository's own naming, read from its `docs/INDEX.md`.

## Proposal mode

Two cultures have written proposals against a standing template for over a
decade: Python's PEPs and Swift Evolution. What they enforce is which slots
must be filled, and what a slot must say when the honest answer is "nothing".
They enforce no sentence rules at all — `plain-writing.md` is already stricter
than either. The full survey is `wiki/proposal-document-conventions.md` in
the `notes` repository.

### Section order

A proposal runs its sections in one fixed order. The reader meets the change
first, then the facts, then the argument, then the limits, and the decisions
last.

| # | section | what it holds |
|---|---|---|
| 1 | the change, named | one plain sentence stating what is proposed |
| 2 | the problem, AS-IS | today's facts, each backed by a file |
| 3 | the options, TO-BE | the candidates, each named, and what each gives up |
| 4 | the recommendation, TO-BE | the one option taken, and why it wins |
| 5 | what this does not do | the exclusions, one line each |
| 6 | what it costs | the impact answers, including every "nothing" |
| 7 | the decisions | rows the proposal settled on its own |

Sections 1 to 4 take names from the subject, not from this table. Rule C in
`draft-rules.md` holds: a section name is a bare noun phrase, so the first
section is named after the change and never "Answer", "Summary", or
"Proposal". Sections 5 and 6 may keep the names above.

**Options come before the recommendation, and that order is settled.** Both
outside cultures put the proposed solution first and file the losers in an
appendix, because a PEP or a Swift proposal is advocacy: its author already
decided and is arguing for one thing. A page in this repository is read by an
owner who has not decided yet, so the options they are choosing between come
before the one this page picks. Take the record shape from those cultures and
leave the stance.

**The first section states the change in one sentence a reader can repeat.**
It sits inside that section, under its heading, and never above the first
heading, which the page opening rule keeps clear. Hold it to 50 words, and
write it to be read away from the page — in a ticket, in a chat message, in a
list of open proposals. Repeating a fact the page states again later is
correct here, not redundant. A reader who stops after that sentence can still
say what the proposal wants.

**Section 5 is what this does not do.** One bulleted list, one exclusion per
line, each naming a thing a reader could reasonably expect and would otherwise
guess about. It carries the page's negative space, so a proposal owes no
separate negative-space section. Write each line as a bare exclusion with the
boundary drawn where it is genuinely fuzzy — "this does not change how a card
is coloured, though which chip a card carries is in scope". No line of it
argues, and none of it says the proposal *will* do the thing later; an
affirmative future sentence reads as something the reader is being asked to
approve.

**Section 6 is what it costs, and every field is answered even when the answer
is nothing.** This is the one convention worth importing whole. A reader has
to tell *the writer considered this and there is no cost* from *the writer did
not think about it*, and an omitted section cannot carry that difference. A
one-line denial can, and it costs one sentence.

| field | what it holds |
|---|---|
| `who relearns` | what a person who knows today's system has to unlearn |
| `what migrates` | what already-stored records or files need doing to them |
| `what undoing costs` | what reversing this costs once it has shipped |

"No record changes shape." is a complete and correct answer to the second
field. Leaving it out is not.

**The decisions come last.** A decision list placed before the argument asks
the reader to accept rulings on a change nobody has explained yet, and it
reads as a page of verdicts. Each decision names its consequence and points
at the section that argues it. Six decisions after a recommendation are six
things to veto; the same six before it are six things to distrust.

### Domain, only when the proposal moves the words

A Domain section defines every term of art the proposal manipulates: what each
one is, and what each one is not. It is **not** a standing section, and a
proposal that opens with one is usually wrong. Neither outside culture has
such a section at all.

Write one only when the change *is* a change to the vocabulary — a rename, a
record being split or merged, two words a reader currently uses for one thing.
There the definitions are the argument. Everywhere else, define each term at
its first use, in the sentence that needs it, with its one example beside it
per rule M.

The test is one question: would deleting the Domain section leave a sentence
the reader cannot parse? If not, the section is an inventory of parts, and an
inventory in front of the argument is the reliable way to lose a reader before
they reach the question.

When a Domain section is owed, the terms of one kind are drawn as typed
records, never as a bullet each. Four statements per term pack into one
unreadable paragraph when a bullet carries them. The record gives each
statement its own field, and the shared field set lets a reader read the
second term by position. The component is in `components.md`, its markup in
`page-html.md`.

| field | what it holds |
|---|---|
| `is` | the definition, in one line |
| `holds` | what the thing is made of, where that is part of the term |
| `instance` | one real example, from a file the run read |
| `not` | the nearest things it is not, one per line |

Add a field the proposal's own argument turns on, such as `verdict` for a
stage that gates or informs, and give it to every member of the kind.

### How a losing option is written

The strongest convention in either outside corpus, and one no template asks
for: a losing option is its own named entry with its reason underneath, never
a paragraph in a list of also-rans. The shape is fixed — **name the option,
say what it would have bought, then say what it cost**. Do not write "rejected
because X"; write the two halves and let the verdict follow them.

A losing option stays in the document forever. The reason it lost is the only
thing standing between it and being proposed again.

When a proposal is revised and its own earlier version is what changed, that
earlier version becomes an entry in the options section with its own kill
reason. The page then carries its history instead of losing it in a diff.

### Four more rules the two cultures earn

1. **One idea per proposal.** A page that argues two changes gets both
   rejected on the weaker one. When a page will not fit, split it by document
   role — the facts in one, the argument in another — and never by feature.
   The same rule is the repair when a reader calls a proposal hard to read:
   count the decisions on the page before cutting any words. A page carrying
   a settled decision beside an open one reads as neither, and the fix is to
   name the one live question in the provenance block, keep only what serves
   it, and push the settled half into an appendix. Trimming sentences on a
   two-decision page leaves it exactly as hard to answer.
2. **Rationale sits beside the change, never after it.** Each proposed change
   carries the AS-IS fact it answers. A change with no fact above it is a
   preference. Both cultures have tried and abandoned a separate rationale
   section, which is the same finding from the other side.
3. **Two halves, marked in the section names.** AS-IS states the problem, and
   a file backs every claim in it. TO-BE states the change, and it is the one
   half allowed to describe what does not exist. A reader must never guess
   which half a figure belongs to.
4. **No unevidenced claim of support.** Do not write that a person, a ticket,
   or another document backs the change without citing where they say so.

### Where the drawing goes

The house style is figure-first, and the outside cultures place their examples
on the *why* side: show how a reader gets a similar effect today and what is
wrong with it, before the change is named. Follow that. The AS-IS section
carries the anatomy figure and the worked example; the TO-BE section carries
the comparison of candidates.

These conventions come from plain-text documents read top to bottom, and the
parts that assume that do not survive a page. Do not number sections by hand,
do not write "the section above", do not keep a change history inside a file
git already versions, and do not carry a footnote list — a citation is inline,
beside the claim it backs.

## Requests this skill does not serve

| the request | what it is | where it goes |
|---|---|---|
| 학습 곡선 차트 그려줘 · draw the learning-curve chart | a chart of measured data | the `dataviz` skill |
| 왜 알림이 안 갔는지 봐줘 · find out why it sent nothing | a diagnosis | the `debugger` subagent |
| 결과 리포트 써서 reports/ 에 올려줘 · put the result report under reports/ | a Markdown report under a repository convention | the working agent writes it |
| 이 스펙 문서 업데이트해줘 · update this spec | a `.md` specification | the working agent writes it |
| 알림 채널 바꿔줘 · change the notification channel | a change to the system | perform the change, do not document it |
| 이거 어떻게 하는 게 나을지 제안해줘 · suggest what would be better | no artifact was asked for | chat: named options with trade-offs and one recommendation, per `~/.claude/CLAUDE.md` "Deciding" |

When the brief is one of these, write no HTML. Return
`STATUS: INSUFFICIENT-INPUT` and name the route.

## What the run never writes

- a `.md` file of any kind
- an edit to the system the page explains
- a line in `INDEX.md`, which the caller adds
- a git commit, because the caller owns git
- a decision. Report an unrecorded decision instead of writing it into the
  page.
