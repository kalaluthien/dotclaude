# Putting Jev into a system

What holds for any reading, learned by replacing an agent's judgments with
Jev calls. A lesson true of one reading alone stays with that reading's data
and cases, never here. Each line ends with where its evidence is; `cb` is
`kalaluthien/campaign-base`.

## Where things live

| what | where | form |
| --- | --- | --- |
| a lesson true of any reading | this file | prose, once |
| one reading: question, `criteria`, state fields, prefilter, thresholds, tier | one data entry its reader asks by name | fields only, no advice |
| what is true of one reading: its cases, a change with before and after numbers | beside its case file | names and values |

No script writes a question inline: a question written twice is tuned once.

## Asking

- `criteria` on every question; a `noul`'s `true` and `false` each get a
  definition and one example, and an option says what it does not cover.
  Adding them narrowed a no band from 0.04-0.74 to 0.05-0.42 (cb pr#459).
- One case per state, many questions over it. Batching cases cost 14.6k
  tokens a call against 1.3k, and left a no-match case mid-band (cb#458).
- One condition per question; code splits a many-condition judgment and
  combines. Let the combiner say which answer moved: a bare `max` inverted
  one reading and hid the moving answer in another (cb#460 NOTE 5713828913).
- A claim against evidence is a `choice` of supports, contradicts,
  says_nothing, the `citation_check` cookbook; flag `1 - P(supports)`.
- The state must hold the evidence. When it lives elsewhere, code makes the
  hop first; a claim against a formal definition needs the declarations of
  the fields it reads (cb#458 NOTEs 5713548995, 5713595497).
- Every question a state could need goes in the one call, used or not.
- A no-match option is not enough: it never fired where a separate
  `no_question` `noul` did, and `confidence` cannot gate a no-match, which
  scored up to 0.93 on a bread recipe (cb#460 groups B, E).

## Measuring

- Jev is a filter, not the judge. Score a reading by the share of cases no
  agent has to read at the cut that misses no real negative.
- Code first: a prefilter settles what it can, and a cheap code ranker runs
  beside token overlap as the baseline. Overlap sat near chance (AUC
  0.48-0.69), and plain size once beat Jev (cb#460, cb#458 NOTE 5713231532).
- Mask the judged name before trusting a band: AUC 0.94 fell to 0.34-0.58
  masked, because the score read the spelling (cb#458 NOTE 5713150753).
- A negative differs only in the thing judged: the same artifact before and
  after, or one inverting edit. A random swap is weak truth, and a swap of
  order in time reads weakest (cb#458 NOTEs 5713213485, 5713581245).
- Hold cases out. A cut set on half the cases missed a real negative in the
  other half in four readings of four (cb#460 NOTE 5713828913).
- Distrust a label the judged text wrote itself, and a prefilter fitted on
  the cases that score it (cb#460 group E).
- Two wordings, three runs, one flip, one no-match, eight real cases with a
  truth. Fewer than eight is `unmeasurable`, never padded.
- `unmeasurable` names a missing record, not a bad question: add the write
  that records what then happened, and collect cases at `shadow` meanwhile.
- A reject needs two designs tried, another state slice and another split,
  with both sets of numbers, and names what would reopen it.

## Adopting

- The aim is replacement: Jev makes the decision at its moment and the agent
  reads only what Jev escalates. Count decisions Jev makes, not agreements.
- A reading enters at a tier. `shadow` logs only; `advise` prints to the
  agent; `act` does a reversible thing at high confidence, asks at medium,
  does nothing at low. A refusal, a merge and a delete stay with code or a
  person. A tier moves on logged agreement, by a recorded decision.
- The corpus grows by itself: every logged call keeps its state, a join
  named by the reading labels it later from what then happened, and the case
  becomes a regression case and the threshold's source. A reading with no
  join cannot compound; say so before building it.
- Something must show what is waiting without being asked: rows unjoined,
  cases unlabelled, readings short of evidence, drift outside a declared band.
- Pin the answering `model` and hash the wording, so drift and a rewording
  are told apart.
