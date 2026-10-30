---
name: surprise-me
description: Use when the user names an area or question to research in depth and wants a structured explanation back. Not for a single fact, a document, deck or textbook, or a plan to stress-test, which grill-me takes.
disable-model-invocation: true
---

Research what the user names, round by round. Each round chases the findings that broke the current picture. Stop when Convergence, a count no one can talk up, says little is left to find. Return the answer a domain expert would have given had the user asked them, as a structured explanation in chat; build no document unless asked.

Surprise here means compression progress (https://arxiv.org/html/0812.4360v2): a finding is surprising only when it reveals a regularity you had not seen, so the explanation gets shorter or more unified with respect to the user's direction. An unlikely finding triggers a step, but noise is unlikely and explains nothing, and the fully predictable teaches nothing, so neither keeps a lead.

Work in one folder: a temporary folder by default, or the folder the user names or a project instruction sets, which takes precedence. Give each task its own subagent when you can, else run them one after another, with one report file each:

| File | Holds |
|---|---|
| `brief.md` | direction, checklist, constraints, axes, routes |
| `rivals.md` | rivals, with evidence for and against each |
| `claims.md` | all claim rows, merged, kept whole |
| `abstract.md` | the claims shrunk by age, which you and each task read |
| `round-N-*.md` | one report per task |
| `probe-N.md` | the blind probe's findings, marked by the audit |
| `diff-N.md` | what each round changed, and its Convergence |

## 1. Brief

Start with a short scoping search for the one or two most recent reviews or meta-analyses. Every account they name becomes a rival candidate and an entry on the coverage list. Then write `brief.md`, and re-read it before every round and before writing, since dropped constraints are how research drifts.

- **Direction**: what the user will decide or wants to know. If it is unclear and a wrong guess would waste the run, ask once by one `AskUserQuestion` call, the recommended option first with `(Recommended)` in its label; else infer it and state it in your first message.
- **Checklist**: 5-15 items the explanation must answer, implied ones included, each tagged must-answer or useful. Freeze it; gaps found later go to open questions.
- **Constraints**: scope, depth, source types, time window, language.
- **Axes**: one per task, none overlapping, each with an out-of-scope line: 1-2 for a narrow question, 3-4 for a comparison, 5 for a broad area.
- **Rivals**: per axis, two or more hypotheses plus "none of these", each with what it predicts that the others do not. Keep them in `rivals.md` as evidence lists, not scores; add more later with their predictions.
- **Anchors**: 5-10 sources or cases from different authors, places and years.
- **Routes**: 4-6 ways into the area that share no index, such as another source type, language, database or citing network. Freeze them with the checklist and show both to the user in your first message, since a probe down a route you chose late measures your choice.

## 2. Rounds

Give each task its objective, its rivals and their predictions, the out-of-scope line, and a search budget of about 10 for a first-round axis, fewer later. Sources go in this order: the primary source, then the author's or preprint copy, then a mirror of the same document. Mark a secondary source as secondary; when sources conflict, search further.

Each report holds:

1. **Claims**: one row each, with the snippet (marked verbatim or tool paraphrase), URL, qualifiers (population, conditions, limits), read depth (abstract, full or secondary) and grade (high, moderate, low or very low).
2. **Refutation**: per rival, what it predicts, the search aimed at exactly that, and the result, nothing found included.
3. **Anomalies**: findings that fit no rival; no mere curiosities.
4. **Threads**: what a source names that no one followed, such as a cited original, dataset, author, term or exception, with the source that names it.
5. **Unused sources**, and why each was not used.
6. **Next questions**: 3-5, each naming the checklist item or anomaly it serves.

Round 1 maps the area with one task per axis, in parallel. After each round, do these steps yourself, never trusting a task's own rating of its yield, since agents rate it too high:

1. **Diff**: merge the claims and update `rivals.md`. In `diff-N.md`, record which checklist items gained or lost support, how the rivals' ranking moved, and which anomalies stay unexplained. Merging two rivals is progress only when the merged account predicts something neither did and the evidence bears it out.
2. **Measure**: count Convergence as below and show the user `diff-N.md` in at most 12 lines, a diff of the explanation, never of the search:

   ```diff
   round 3  Convergence 0.6  Settled 6/10  Recapture 7/10  next: repeat
   + item 4 settled: <the answer>
   - rival B: <the finding that killed it>
   ~ rival A passes C: <why>
   ? open anomaly: <what it is>
   ```

3. **Abstract**: rewrite `abstract.md` so old material costs less to read. Keep this round's claims as full rows, turn last round's into one line per group, and turn anything older into one clause per checklist item or rival. Each line says what its rows show together and cites their row numbers. A contradiction, an open anomaly or a qualifier that flips a conclusion stays at full size at any age, and a new finding that touches a line brings its rows back. Keep everything older than this round under 20 lines.
4. **Dive**, since a wide search stops at what the first page shows: run each thread that touches an unsettled item or open anomaly as one small depth-first task. Each hop starts from what the last source names, never from a fresh topic search. At the origin, or after two hops that add no claim, it backs up to the last fork. It reports the chain as `A → B → C` with what each hop added.
5. **Jump**, from round 2 on, since agents stay near the obvious framing unless pushed off it:
   - for the top two or three anomalies, write abductive hypotheses: if A were true, the anomaly would be expected;
   - for each axis that only refined last round, pick one domain at moderate distance that shares its purpose and relations but not its surface, and ask what transfers; very distant domains seldom do;
   - before a jump runs, write the item or anomaly it serves, its prediction and the test that would kill it; run each as one small task.
6. **Pick leads**: pool the next questions, anomalies, jumps, threads, unused sources and cross-axis combinations. Park any lead that touches no checklist item or anomaly. Order the rest by three tests in turn, never by how unlikely or new a lead looks, only by the surprise it can be expected to yield:
   - does it serve an unanswered must-answer item?
   - would it settle more claims or anomalies than the exceptions it could add?
   - how cheap is it?

   Between two questions, prefer the one whose possible answers would each eliminate a different rival.
7. **Narrow**: phrase each next task as "which of these rivals does this search eliminate?". Use fewer tasks with sharper targets each round.

Agents stop too early, so the stop is counted, by tasks that never see your reasoning:

- **Probe**: one task sees only the direction and the checklist, never the claims, rivals or queries. It takes the next unused route and returns ten atomic findings that bear on the direction, at most two per source and three per checklist item. Every probe counts, so never rerun one. Under five findings gives no reading: take the next route. After a Repeat round, skip the probe and carry the last reading, since routes run out.
- **Audit**: one task sees only `claims.md`, `probe-N.md` and the cited sources. It marks a finding `known` only by quoting the row that states it, with the same population and conditions, else `new`. It marks a must-answer item settled only by quoting the sentence of a source that answers it, or that says no one knows, and not while rows conflict or the support is graded low. Merge the `new` findings into `claims.md` after the count.
- **Settled**: settled must-answer items over all must-answer items. An item listed as open counts 0.
- **Recapture**: `known` findings over all the probe's findings.
- **Convergence**: the lower of the two, so neither can make up for the other.

| Reading | Next round |
|---|---|
| Below 0.9, Recapture the lower | **Widen**: one task per group of `new` findings, plus the jumps |
| Below 0.9, Settled the lower or equal | **Repeat**: one dive per unsettled must-answer item; two failed reformulations close an item as open |
| Convergence 0.9 or more once | **Confirm**: only the next probe and audit |
| Convergence 0.9 or more on two probes in a row | **Stop**, once a dive has run, the last diff left the top rival in place and one small final task, aimed where the explanation is most likely wrong, only refined it; else Repeat |

One clean probe proves little: ten of ten known still leaves about a quarter unseen. Set no maximum round count. The user's budget or running out of routes also ends the run, and so does a Repeat with only closed items left. When you stop before converging, say so, give the last Convergence and name what the next round would target.

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

One writer drafts the whole explanation in one pass from `claims.md`, as the expert the user would have asked. An answer that changes nothing the user believed is a good answer, so never hunt for a twist. Every claim needs a cited snippet, and a synthesis across sources is labelled as yours. A familiar example that bridges to what the user knows may go uncited when it reads as an illustration. Define each technical term and model name at first use. In this order:

1. **Answer**: one to three sentences per must-answer item.
2. **Main claims**: non-overlapping, each with the likely alternative view and the evidence that favours this one. Show key mechanisms step by step; when several causes act, give their relative strength or say it is unknown.
3. **Rivals**: a table of evidence for and against, a verdict and the settling test for each, noting which common views the evidence overturned.
4. **Open questions**: what is unknown, which assumption would flip which conclusion, and, if the run stopped early, the next target.
5. **Sources**.

Explain the subject, never the search. The user's language and style rules override this skill's wording. Keep the explanation in chat unless a file was asked for, and offer in one line to save it if it runs long.
