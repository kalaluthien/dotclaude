---
name: show-me
description: Use when the user asks to see, show, explain, map, brief, compare or draw something - a system, structure, change, status, data, process or choice - as a diagram, table, chart, map, mockup, page, html or artifact. Not for a single fact, a yes/no or capability question, or a command to run.
disable-model-invocation: true
---

## Steps

1. **Name the core question.** Before anything else, write in one line what the user really wants to understand and what it is about, as one of the question types below. An ask with several questions gets one line each.
2. **Name what the answer is for.** The real point is what the user wants to get from the answer, not the question alone. Write one line for it: they want to **understand**, to **review** or to **decide**, or another aim in its own words. The aim sets what the page leads with: for understand, the idea built up from what the reader already knows; for review, the thing itself with each point to check; for decide, the options, their trade-offs and a recommendation.
3. **Assume a reader new to the subject.** That the user asked at all means they may lack deep expertise here, may not remember the specifics, and may not know its terms. Say what each term means where it first appears, and spell out what an expert would skip.
4. **Read the original.** Open the source itself: the file, log, diff, data, page or transcript. Never a summary of it, a memory, or an earlier answer. Quote what you show with its `path:line` or URL.
5. **Pick by matching.** Find the case below whose question and data shape match, and use its representation; the smallest that answers wins. One representation per question.
6. **Make the page.** Put the result in one HTML file, in this order: the answer in one sentence, the representation, what the reader can do next. Chat holds only that sentence, the file's full path and the next step: no table, tree, diagram, PNG or ASCII drawing, since the owner asked for HTML only.

## The page

- **Make it polished**: the owner asked for a page that is visually well considered, so load `artifact-design` (and `artifact-diagramming` for a drawing) when listed, else apply the same care yourself, and follow them for type, spacing, colour and both themes.
- **Style it for the field**: draw it the way an expert of the subject's field expects to see it, such as a circuit as a schematic or a proof as numbered steps, and arrange it by UX/UI principles: a clear hierarchy, related things grouped, one thing to look at first.
- **Make it responsive**: the reader may open it on a desktop or on a mobile, so the layout adapts to the width; a wide diagram or table reflows or scrolls inside its own box.
- **One file**: inline CSS and SVG, no external fetch, no build step, a few lines of script only for a live control. Draw each diagram as inline SVG, never Mermaid or an image.
- **Write it** to a new file under the scratchpad, or `~/Documents/show-me/` when no scratchpad exists, named for its subject (`retry-rule.html`). Print its full path in the reply, since a terminal tab shows no `SendUserFile` file, and never run `open`; send it by `SendUserFile` too for a remote viewer (phone, Remote Control, desktop app).
- **Check it**: read the file back and confirm it holds each quoted `path:line`; where a headless browser of your own runs (never the owner's Chrome), screenshot it at a desktop and a mobile width and look for overflow or a broken layout, and fix what you see before you report it.

## Question types and data shapes

- Questions: **what is it** (identity, value, meaning), **how is it built** (parts and how they connect), **how does it behave over time** (steps, states, messages, events), **how do parts compare** (size, rank, position, overlap), **what changed** (before and after, cause), **what if** (a value or choice varied), **why does it hold** (a concept or a line of reasoning).
- Data shapes: **single value**, **category** (items with attributes), **sequence** (ordered in time or position), **network** (nodes and links), **hierarchy** (nesting), **space** (positions on axes or a layout), **flow** (quantities or work moving between nodes), **argument** (claims and the reasons that support them).

## Representations

Each entry: when to pick it, then a tiny example. Every pick is drawn on the page, and a pele.run link only shows its shape, to be redrawn as inline SVG.

### What is it

- **Plain answer**: one value, name or yes/no, with its source. *"Timeout is 30 s (`config.yaml:12`)."*
- **Worked example**: a concept or rule shown on one real instance, input to output. *A retry rule shown as: request 1 fails at 0 s, retry at 2 s, retry at 6 s, give up.*
- **Status board**: where many items stand now, when status is the one attribute that matters, shown as one column per status. *Open tasks in columns To do / Doing / Done* ([kanban](https://pele.run/examples/kanban)).

### How is it built

- **Tree**: nesting with no cross-links, such as folders, a config or an outline. *`skills/` with its folders, one level each* ([treeview](https://pele.run/examples/treeview), [mindmap](https://pele.run/examples/mindmap)); sized by value: [treemap](https://pele.run/examples/treemap).
- **Box-and-arrow diagram**: parts and their links, such as services, modules or people and systems. *Browser → API → queue → worker → database* ([architecture](https://pele.run/examples/architecture), [c4](https://pele.run/examples/c4), [block](https://pele.run/examples/block)).
- **Data model**: entities or classes with fields and relations. *User 1-n Order n-1 Product* ([er](https://pele.run/examples/er), [class](https://pele.run/examples/class)).
- **Goal map**: who wants what from a system, and which requirement serves it. *Owner → "approve PR" → judge check* ([usecase](https://pele.run/examples/usecase), [requirement](https://pele.run/examples/requirement)).
- **Format diagram**: the fields or grammar of a message, file or command line. *Header 2 bytes, length 2 bytes, body* ([packet](https://pele.run/examples/packet), [railroad](https://pele.run/examples/railroad)).
- **Mockup**: what a screen or page looks like and where things sit on it. *A settings screen sketched with the new toggle marked.*

### How does it behave over time

- **Flowchart**: steps and decisions of one process. *Push → tests pass? → yes: merge / no: fix* ([flowchart](https://pele.run/examples/flowchart)); split by who does each step: [swimlane](https://pele.run/examples/swimlane); work passed between agents: [agentflow](https://pele.run/examples/agentflow); how each step feels to a user: [journey](https://pele.run/examples/journey).
- **Sequence diagram**: messages between participants, in order. *Client → server: login; server → client: token* ([sequence](https://pele.run/examples/sequence)); commands and events changing views: [eventmodeling](https://pele.run/examples/eventmodeling).
- **State diagram**: the states one thing moves through and what moves it. *Issue: open → held → blocked → closed* ([state](https://pele.run/examples/state)).
- **Timeline**: events or tasks placed in time. *What happened in an incident, minute by minute* ([timeline](https://pele.run/examples/timeline)); planned tasks with durations: [gantt](https://pele.run/examples/gantt); branches and merges: [git](https://pele.run/examples/git).
- **Line chart**: one or a few quantities over time. *Daily token use across a week* ([xychart](https://pele.run/examples/xychart)).

### How do parts compare

- **Table**: fixed items against the same several attributes, when the reader needs each exact value, such as a catalogue, or options to choose between. *Three libraries by size, licence and last release.*
- **Bar chart**: one quantity across categories. *Lines changed per folder* ([xychart](https://pele.run/examples/xychart)); parts of one whole, five or fewer: [pie](https://pele.run/examples/pie).
- **Distribution chart**: how many values of one quantity spread, with their middle and tails. *Request latency: median 120 ms, p95 900 ms* (histogram, box plot).
- **Heatmap**: one value across two categories, or across days. *Test failures by module and weekday.*
- **Profile chart**: a few items scored by number on the same several axes, when the shape of each profile matters more than its exact values. *Two designs on speed, cost, risk, effort* ([radar](https://pele.run/examples/radar)).
- **Position map**: items placed on two axes. *Tasks by impact and effort* ([quadrant](https://pele.run/examples/quadrant)); by user visibility and maturity: [wardley](https://pele.run/examples/wardley); by kind of problem: [cynefin](https://pele.run/examples/cynefin).
- **Geographic map**: values or links placed on real places. *Users per country, shaded.*
- **Overlap diagram**: which items share which members. *Skills each of three plugins ships, and the shared ones* ([venn](https://pele.run/examples/venn)).
- **Flow diagram**: how much moves from where to where. *Tokens by source → tool → model* ([sankey](https://pele.run/examples/sankey)).

### What changed

- **Diff**: before and after of text, code or a value, the changed lines quoted. *`- timeout: 30` / `+ timeout: 60` at `config.yaml:12`.*
- **Before-and-after diagram**: two of the same diagram from above, the changed parts marked. *The service map before and after the split.*
- **Guided tour**: the steps a reader follows to see each change themselves, each with where to go and what they should see. *Open Settings → the new Sync toggle is on by default.*
- **Cause map**: the causes behind one result, grouped. *Slow build ← cache miss, large image, cold runner* ([ishikawa](https://pele.run/examples/ishikawa)).

### What if

- **Scenario table**: one choice or value varied, each setting against what it causes. *Retries 1 / 3 / 5 → success rate and wait time.*
- **Live control page**: a value judged by seeing or feeling it, such as a colour, a timing or a layout, or a large graph or data set the reader explores by filtering, hovering and selecting; a small script on the page. *A slider for the animation easing, with the box moving.*
- **Decision tree**: a choice that depends on several conditions, each answer leading to the next question and the leaves naming the outcome. *Over 1 GB? → yes: needs random access? → yes: database / no: object store; no: flat file.*

### Why does it hold

- **Proof walkthrough**: a claim reached from what is given, one numbered step per line, each naming the rule that allows it. *Given a > b and b > c; 1. a > c by transitivity.* Draw the givens in a box on top, then a numbered ladder of steps down the left, each with its rule as a right-aligned tag, and the claim in a filled box at the end; a step that uses an earlier one shows its number.
- **5 Whys**: one symptom followed down a single chain of causes, each answer the next "why?", ending at the root cause. *Deploy failed ← disk full ← logs never rotated ← the cron job was removed.* Draw a vertical chain of five boxes joined by arrows, each box headed "Why 1" to "Why 5" and sized the same, the symptom at the top in a neutral colour and the root cause at the bottom in the accent colour, with the evidence for each step in small text under it.
- **MECE pyramid**: a conclusion on top, held up by groups of reasons that do not overlap and together leave nothing out, each group by its own evidence. *Revenue fell ← fewer buyers / fewer orders per buyer / lower price per order.* Draw the conclusion as a wide box on top, two or three group boxes in one row below it, and the evidence as small boxes under each group, joined by straight lines; the group boxes share one width, and a note under the row says what splits them (one axis only).
- **Venn diagram**: how concepts relate as sets, to show where one includes, overlaps or excludes another. *Every square is a rectangle, and rectangles and rhombuses overlap in the squares* ([venn](https://pele.run/examples/venn)). Draw translucent circles (nested for inclusion, apart for exclusion), each labelled outside its edge, with the overlap shaded darker and carrying an example item; use at most three sets, and a legend line states what each region means.
- **Causal loop diagram**: quantities that drive each other in a circle, each link marked + or −, each loop marked reinforcing or balancing. *More users → more load → slower pages → fewer users (balancing).* Draw the quantities as words (no boxes) round a circle, joined by curved arrows with a + or − at each head, and the loop's name in its centre with a circular arrow, R for reinforcing or B for balancing; a line below says how to read the loop.
