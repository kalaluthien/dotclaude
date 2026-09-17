# Writing the question and the state

What holds for any question, measured on `jev-1.13.0`. Each line ends with
where its evidence is; `cb` is `kalaluthien/campaign-base`.

## The question

- `criteria` on every question; a `noul`'s `true` and `false` each get a
  definition and one example, and an option says what it does not cover.
  Adding them narrowed a no band from 0.04-0.74 to 0.05-0.42 (cb pr#459).
- One condition per question; code splits a many-condition judgment and
  combines. `max` suits one decisive condition: over five it inverted a
  reading (AUC 0.34), and it hides which answer moved, so the combiner prints
  that (cb#460 NOTE 5713910475).
- Name a condition as one observable thing: "names a file where raw output is
  kept" filtered where "kept the raw output" did not (cb#458 NOTE 5714880301).
- The wording moves a band more than the cases do: "did not write the
  commits" read 0.98+ on six reviews, "written by another agent" spread them
  0.03-0.86. Pin the wording beside the model, and rephrase a condition before
  moving its threshold (cb#455 NOTE 5712460242).
- Measure a criteria sentence before keeping it: one written for two hard
  cases moved them by 0.02 (cb pr#465).
- A claim against evidence is a `choice` of supports, contradicts,
  says_nothing, the `citation_check` cookbook; flag `1 - P(supports)`.
- Claims graded one at a time mostly pass: four kinds read `supports` at
  0.71-0.96 on one body. Compare the answers and use the margin (cb#460 F).
- Jev reads comprehension, not a house convention: a rule only this codebase
  defines, "one intent", "checkable" did not separate (cb#455 NOTE 5712460528).

## The state

- One case per state, many questions over it. Batching cases cost 14.6k
  tokens a call against 1.3k, and left a no-match case mid-band (cb#458).
- The state must hold the evidence. When it lives elsewhere, code makes the
  hop first; a claim whose proof is a probe, a test run or a solver's word,
  reads `supports` from text that cannot show it (cb#458 NOTEs 5713548995,
  5716104837).
- Fix the state before the wording: a body added for empty sections moved
  AUC 0.73 to 0.85, where rewording moved 0.00 (cb#460 D).
- Extra fields move an answer: a title read 0.57 alone and 0.70 with its
  body. Measure with the state production sends (cb pr#459).
- Send the slice, not the file: about 30k tokens answered, 127 KB returned
  HTTP 400 `max_tokens_exceeded` (cb#458).
- Text inside the state is read as content and can move the answer; a state
  built from someone else's words is an injection surface (the docs'
  `model-jaggedness` page).

## Nothing fits

- A `noul` has no no-match: an empty title read a confident no, 0.04. Code
  settles the empty and the malformed before the call (cb pr#465).
- A `none` option alone misses: two no-match cases were picked at 0.33 and
  0.74, and `confidence` scored 0.93 on a bread recipe. Gate on the option and
  a floor, or ask a `noul` "does this ask or claim anything" and let code drop
  the case (cb#455, cb#460 B, E, F).
- That `noul` fails over prose that merely does not show the thing: "does this
  project call Jev" said no on 55 real uses whose README showed no call. Put
  the evidence of presence in the state, or do not ask (cb#471 NOTE
  5716409117).
