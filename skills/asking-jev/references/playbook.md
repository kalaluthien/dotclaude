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
  combines. `max` suits one decisive condition: over five it inverted a
  reading (AUC 0.34), and it hides which answer moved, so the combiner prints
  that (cb#460 NOTE 5713910475).
- Claims graded one at a time mostly pass: four kinds read `supports` at
  0.71-0.96 on one body. Compare the answers and use the margin (cb#460 F).
- Fix the state before the wording: a body added for empty sections moved
  AUC 0.73 to 0.85, where rewording moved 0.00 (cb#460 D).
- A claim against evidence is a `choice` of supports, contradicts,
  says_nothing, the `citation_check` cookbook; flag `1 - P(supports)`.
- The state must hold the evidence. When it lives elsewhere, code makes the
  hop first; a claim against a formal definition needs the declarations of
  the fields it reads (cb#458 NOTEs 5713548995, 5713595497).
- Every question a state could need goes in the one call, used or not.
- A no-match option does not fire: ask a `noul`, "does this ask or claim
  anything", and let code drop the case. `confidence` cannot gate a no-match
  either, which scored 0.93 on a bread recipe (cb#460 groups B, E, F).

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
- Report a cut on cases it was not set on: set on half, it missed a real
  negative in the other half in four readings of four. Use a round cut under
  the lowest real negative, not that minimum (cb#460 NOTE 5713910475).
- State the ceiling the class balance allows and the best code rule beside
  Jev: one reading could save 8 of 20 whatever Jev did (cb#460 A).
- When the judged text states its own class, a regex finds it and Jev adds
  little; a prefilter or condition fitted on the reported cases is a
  hypothesis until refit on unseen ones (cb#460 E, F).
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
