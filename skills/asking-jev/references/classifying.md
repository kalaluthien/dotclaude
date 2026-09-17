# Sorting items into classes

For a pile of items, each to get one class or several: sources into patterns,
findings into kinds, tickets into queues. Read [questions](questions.md)
first. The worked case is 385 projects sorted into nine patterns in 446 calls
(cb#471 NOTEs 5716405562, 5716409117; `cb` is `kalaluthien/campaign-base`).

## The shape

| the classes | ask |
| --- | --- |
| an item may hold several | one `noul` per class, all in one call |
| exactly one of a closed set | a `choice`, a no-match guard beside it ([questions](questions.md) § Nothing fits), and a `noul` "does the picked class fit" that can veto it; the veto has no published numbers, so measure it |
| an order or a degree | a `score` per item, compared across items |

- One item is one state and one call: every class question and both wordings
  in it. Items are never batched into one state.
- A `choice` over a property the text rarely states is degenerate: 21 of 22
  true answers were `not_stated`. Ask it only where the text can show it.
- Option order is a variable: reversing it flipped 32 of 200 picks elsewhere,
  the flipped ones at confidence 0.42 against 0.81. Ask both orders on a
  sample, and read a flip as `uncertain` (blakestone-x/jev-mcp, read
  first-hand; not measured here).

## Before the run

1. Write the class list from a hand-read sample, not from Jev's answers. Fold
   a class with fewer than eight items, or list it apart.
2. Lint first. Where a keyword names the class outright the item is code's,
   Jev only tied it at 0.94 each, and an item code settles is never sent.
3. Hand-label at least eight per class, and split by hash into a half the
   criteria are written from and a half held out.
4. Write the bar down before any call: held-out agreement on what lint left,
   against the label and chance, and what happens to a class that misses. A
   class under the bar is sorted by hand, and the report says so.

## Reading the result

- Report recall beside agreement. With 3 to 12 positives in 68, one class
  agreed 0.88 and 0.93 under two wordings while recall was 4 of 10 and 7 of
  10.
- Two wordings in one call are free instrumentation: they agreed on 363-377
  of 385, and the class where they split was the one worth reading.
- Repeat a sample, not the pile: three byte-identical runs changed 8 of 570
  answers, the raw spread at most 0.12.
- A person's own earlier label is weak truth: a reviewer's word agreed with
  the written definition on 21 of 32, so a keyword rule "won" by matching the
  labeller's habits. Label a sample against the definition (cb#458 NOTE
  5715409487).
- Jev sorts; whoever owns the decision judges. What a class means for the
  system stays with the reader of the sorted pile.
