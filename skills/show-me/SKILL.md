---
name: show-me
description: Use when the user asks to see, show, explain, map, brief, compare or draw something - a system, structure, change, status, data, process or choice - as a diagram, table, chart, map, mockup, page, html or artifact. Invoke it first, before reading any file, since it says how to read the source and pick the representation. Not for a single fact, a yes/no or capability question, or a command to run.
---

# show-me

Show the user what they want to understand, built from the thing itself.

## Steps

1. **Name the core question.** Before anything else, write in one line what the user really wants to understand and what it is about, as one of the question types below. An ask with several questions gets one line each.
2. **Read the original.** Open the source itself: the file, log, diff, data, page or transcript. Never a summary of it, a memory, or an earlier answer. Quote what you show with its `path:line` or URL.
3. **Pick by matching.** Find the case below whose question and data shape match, and use its representation; the smallest that answers wins. One representation per question.
4. **Show it.** Open with the one-sentence answer, then the representation, then what the reader can do next. Something that fits one screen goes in chat: a table, a tree, a short list, a fenced diagram. A rich page (several parts, controls, styling) is an Artifact prompt's job: hand it the picked representations, the facts and their sources, and let it build the page.

Draw each diagram, never paste Mermaid, since chat shows it as raw text: where `mmdc` is on `PATH` or `npx -y @mermaid-js/mermaid-cli` runs, render each to PNG, print its full path in the reply, since a terminal tab shows no `SendUserFile` file, and never run `open`; send it by `SendUserFile` too for a remote viewer (phone, Remote Control, desktop app); where neither runs, use a table, a tree list or an ASCII drawing, and hand the user `! npx -y @mermaid-js/mermaid-cli --version`. The links below are example drawings.

## Question types and data shapes

- Questions: **what is it** (identity, value, meaning), **how is it built** (parts and how they connect), **how does it behave over time** (steps, states, messages, events), **how do parts compare** (size, rank, position, overlap), **what changed** (before and after, cause), **what if** (a value or choice varied).
- Data shapes: **single value**, **category** (items with attributes), **sequence** (ordered in time or position), **network** (nodes and links), **hierarchy** (nesting), **space** (positions on axes or a layout), **flow** (quantities or work moving between nodes).

## Representations

Each entry: when to pick it, then a tiny example.

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
- **Live control page**: a value judged by seeing or feeling it, such as a colour, a timing or a layout, or a large graph or data set the reader explores by filtering, hovering and selecting; a rich page, so an Artifact prompt. *A slider for the animation easing, with the box moving.*
