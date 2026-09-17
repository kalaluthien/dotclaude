# Putting Jev into a system

What holds for any reading, learned by replacing an agent's judgments with
Jev calls. How a question and its state are written is
[questions](questions.md); sorting a pile is [classifying](classifying.md). A lesson true of one reading alone stays with that reading's data
and cases, never here. Each line ends with where its evidence is; `cb` is
`kalaluthien/campaign-base`.

## Where things live

| what | where | form |
| --- | --- | --- |
| a lesson true of any reading | this file | prose, once |
| one reading: question, `criteria`, state fields, prefilter, thresholds, tier | one data entry its reader asks by name | fields only, no advice |
| what is true of one reading: its cases, a change with before and after numbers | beside its case file | names and values |

No script writes a question inline: a question written twice is tuned once.

## Measuring

- Code is the lint and Jev the judge, in series and never rivals: code
  settles what a rule can see, and Jev is scored only on what is left,
  against the label and against chance (owner, html-doc#462 DECISION
  5716755047). A code rule's score on the same pile is not Jev's bar.
- Score a reading by what it clears over what can be cleared at the cut that
  misses no real negative. A share of all cases hid a reading that cleared
  most of what it could (cb#471 NOTE 5716875903).
- What code can rank it ranks first: token overlap sat near chance (AUC
  0.48-0.69) and plain size ordered one pile better than Jev, so that pile
  was lint's (cb#460, cb#458 NOTE 5713231532).
- Mask the judged name before trusting a band: AUC 0.94 fell to 0.34-0.58
  masked, because the score read the spelling (cb#458 NOTE 5713150753).
- A negative differs only in the thing judged: the same artifact before and
  after, or one inverting edit. A random swap is weak truth, and a swap of
  order in time reads weakest (cb#458 NOTEs 5713213485, 5713581245).
- Report a cut on cases it was not set on: set on half, it missed a real
  negative in the other half in four readings of four. Use a round cut under
  the lowest real negative, not that minimum (cb#460 NOTE 5713910475).
- State the ceiling the class balance allows: one reading could save 8 of 20
  whatever Jev did (cb#460 A).
- When the judged text states its own class, a regex finds it and Jev adds
  little; a prefilter or condition fitted on the reported cases is a
  hypothesis until refit on unseen ones (cb#460 E, F).
- Two wordings, three runs, one flip, one no-match, eight real cases with a
  truth. Fewer than eight is `unmeasurable`, never padded.
- `unmeasurable` names a missing record, not a bad question: add the write
  that records what then happened, and collect cases at `shadow` meanwhile.
- A band from one run is luck: a declared yes floor of 0.80 became 0.55 over
  four runs. Set a cut after three, off any value observed, and prefer a band
  with an `uncertain` middle to one cut (cb pr#465).
- Compare the lowest positive with the highest negative before calling a band
  separate: a pooled AUC hid an overlap that was the same two cases in four
  runs of four (cb#458).
- When history lacks negatives, make them by one meaning-flipping edit, marked
  as made: they read `contradicts` 0.88-1.00 against 0.00-0.07 (cb#458 NOTE
  5713581245).
- Write the bar and what a miss means before the first call, and with it the
  rule that names the headline design. Picked after the run, the headline was
  not the design that missed none and cleared 15 of 26 (cb#471 NOTE
  5716842004).
- A cut read on all cases overstates: two readings "kept" that way went back
  to `shadow` on a held-out split (cb#471 DECISION 5716742190).
- A reject needs two designs tried, another state slice and another split,
  with both sets of numbers, and names what would reopen it.

## Spending calls

Count calls against distinct states in the log. Four logs here ran 3.5 to 9.5
calls a state, 14.8k calls in all, by asking one claim, one wording or one run
at a time (cb logs, 2026-09-17). Where a line below does not fit, skip it.

- One call a state holds every claim, both wordings, the reversed option
  order and any mirror question. Questions cannot see each other, the price is
  per input token, and 13 in one call gave the same answers 12x cheaper (the
  `parallel_questions` cookbook). This is not batching cases, which stays out.
  The reversed order asked in the same call read as well as a second request,
  and one call ran 4 to 8 times faster (cb#471 DECISION 5716742190).
- Only a repeat run needs a second call. Repeat a sample, plus the rows that
  land inside or near the band; a row far from both edges does not flip on a
  few hundredths of noise.
- Keep the raw probabilities and replay them: moving a cut, a band or a
  combiner asks nothing. Key a stored answer by state hash, wording hash and
  pinned `model`; a hit is not a call, and a changed wording misses by itself.
- What the prefilter settles is never sent.
- A second call is right when it needs the first one's answer, to fetch
  evidence or build options. A reader already at one call a state is done.

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
- Code decides first and last: a deterministic layer settles what it can, and
  a flag fires only where a Jev answer and a code fact agree. Jev reads
  "claims it is done"; a script says whether a check ran after the last edit
  (pi-quiet-ask and pi-jev-auto-mode, read first-hand; cb#471 NOTE
  5716409117).
- A test that stubs the endpoint stubs the log too, and joined cases are
  counted by distinct state before they are committed: one suite wrote 70
  copies of a stub title into a corpus (cb pr#472).
- Pin the answering `model` and hash the wording, so drift and a rewording
  are told apart.
