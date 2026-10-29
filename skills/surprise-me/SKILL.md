---
name: surprise-me
description: Use when the user names an area or question to research in depth and wants a structured explanation back. Not for a single fact, a document, deck or textbook, or a plan to stress-test, which grill-me takes.
disable-model-invocation: true
---

Research what the user names, round by round. Each round chases the findings that broke the current picture. Stop when another round no longer changes the explanation. Return a structured explanation in chat; build no document unless asked.

A surprise triggers a step; it does not justify keeping a lead. Keep a lead when it makes the explanation shorter or more unified with respect to the user's direction. Noise surprises without explaining anything.

Work in one folder, one task per subagent when you can, else one after another with one report file each:

| File | Holds |
|---|---|
| `brief.md` | direction, checklist, constraints, axes |
| `rivals.md` | rivals, with evidence for and against each |
| `claims.md` | all claim rows, merged |
| `round-N-*.md` | one report per task |
| `diff-N.md` | what each round changed |

## 1. Brief

Start with a short scoping search for the one or two most recent reviews or meta-analyses. Every account they name becomes a rival candidate and an entry on the coverage list. Then write `brief.md`, and re-read it before every round and before writing, since dropped constraints are how research drifts.

- **Direction**: what the user will decide or understand differently. If it is unclear and a wrong guess would waste the run, ask once by one `AskUserQuestion` call, the recommended option first with `(Recommended)` in its label; else infer it and state it in your first message.
- **Checklist**: 5-15 items the explanation must answer, implied ones included, each tagged must-answer or useful. Freeze it; gaps found later go to open questions.
- **Constraints**: scope, depth, source types, time window, language.
- **Axes**: one per task, none overlapping, each with an out-of-scope line: 1-2 for a narrow question, 3-4 for a comparison, 5 for a broad area.
- **Rivals**: per axis, two or more hypotheses plus "none of these", each with what it predicts that the others do not. Keep them in `rivals.md` as evidence lists, not scores; add more later with their predictions.
- **Anchors**: 5-10 sources or cases from different authors, places and years.

## 2. Rounds

Give each task its objective, its rivals and their predictions, the out-of-scope line, and a search budget of about 10 for a first-round axis, fewer later. Sources go in this order: the primary source, then the author's or preprint copy, then a mirror of the same document. Mark a secondary source as secondary; when sources conflict, search further.

Each report holds:

1. **Claims**: one row each, with the snippet (marked verbatim or tool paraphrase), URL, qualifiers (population, conditions, limits), read depth (abstract, full or secondary) and grade (high, moderate, low or very low).
2. **Refutation**: per rival, what it predicts, the search aimed at exactly that, and the result, nothing found included.
3. **Anomalies**: findings that fit no rival; no mere curiosities.
4. **Unused sources**, and why each was not used.
5. **Next questions**: 3-5, each naming the checklist item or anomaly it serves.

Round 1 maps the area with one task per axis, in parallel. After each round, do these four steps yourself, never trusting a task's own rating of its yield, since agents rate it too high:

1. **Diff**: merge the claims and update `rivals.md`. In `diff-N.md`, record which checklist items gained or lost support, how the rivals' ranking moved, and which anomalies stay unexplained. Merging two rivals is progress only when the merged account predicts something neither did and the evidence bears it out.
2. **Jump**, from round 2 on, since agents stay near the obvious framing unless pushed off it:
   - for the top two or three anomalies, write abductive hypotheses: if A were true, the anomaly would be expected;
   - for each axis that only refined last round, pick one domain at moderate distance that shares its purpose and relations but not its surface, and ask what transfers; very distant domains seldom do;
   - before a jump runs, write the item or anomaly it serves, its prediction and the test that would kill it; run each as one small task.
3. **Pick leads**: pool the next questions, anomalies, jumps, unused sources and cross-axis combinations. Park any lead that touches no checklist item or anomaly. Order the rest by three tests in turn, never by surprise or novelty:
   - does it serve an unanswered must-answer item?
   - would it settle more claims or anomalies than the exceptions it could add?
   - how cheap is it?

   Between two questions, prefer the one whose possible answers would each eliminate a different rival.
4. **Narrow**: phrase each next task as "which of these rivals does this search eliminate?". Use fewer tasks with sharper targets each round.

Stop when all three hold:

- every must-answer item is supported or listed as open;
- the last diff added no top-level element, left the rivals' ranking unchanged and explained no new anomaly;
- one small final task, aimed where the explanation is most likely wrong, only refined it.

Agents stop too early, so when in doubt run one more round on uncovered items. The user's budget, or two failed reformulations of the same hunt, also ends the run. When you stop before converging, say so and name what the next round would target.

## 3. Verify

Write the key claims as atomic statements in `verify.md`. Check them with a task that sees only that file and the cited sources, never your draft or reasoning; batch the claims by source, one fetch per source. Look for:

- the source does not state the claim, credits it to an aggregator, or says something different about a term, formula or mechanism;
- a qualifier the source states (age, task, design, sample size, moderator) is missing;
- sources set against each other that measured different things, or a synthesis of several sources under one source's citation;
- a grade that should drop because the evidence is indirect to the question, observational only, inconsistent, single-source or secondhand;
- overclaiming: causation from correlation, humans from animals or lab studies, a null read as "no effect", a subgroup made the headline, or a figure taken from news instead of the paper.

For claims that carry a must-answer item, also search for later work that contradicts the source, and for who is behind it. Keep a downgraded claim at its new grade; move a claim that cannot be supported at all to open questions.

Then run a separate recall pass, item by item against the checklist and the coverage list. After each correction, restore anything dropped without being found wrong.

## 4. Write

Run a pre-mortem first: assume the explanation turned out wrong, name the three likeliest reasons, and check each against the sources.

One writer drafts the whole explanation in one pass from `claims.md`. Every claim needs a cited snippet, and a synthesis across sources is labelled as yours. A familiar example that bridges to what the user knows may go uncited when it reads as an illustration. Define each technical term and model name at first use. In this order:

1. **Answer**: one to three sentences per must-answer item.
2. **Main claims**: non-overlapping, each with the likely alternative view and the evidence that favours this one. Show key mechanisms step by step; when several causes act, give their relative strength or say it is unknown.
3. **Rivals**: a table of evidence for and against, a verdict and the settling test for each, noting which common views the evidence overturned.
4. **Open questions**: what is unknown, which assumption would flip which conclusion, and, if the run stopped early, the next target.
5. **Sources**.

Explain the subject, never the search. The user's language and style rules override this skill's wording. Keep the explanation in chat unless a file was asked for, and offer in one line to save it if it runs long.
