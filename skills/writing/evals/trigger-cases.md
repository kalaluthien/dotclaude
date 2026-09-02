# Trigger cases

Twelve requests that reach the skill, and twenty-two rubric lines for a
delivered run. Six requests start a run, and six do not. Every subject is a
repository or a tool this machine holds.

- [Must fire](#must-fire-6)
- [Must not fire](#must-not-fire-6)
- [Rubric](#rubric-22-lines)

## Must fire, 6

| the request | what the run then owes |
|---|---|
| campaign tracker가 서브이슈를 어떻게 읽어서 정산하는지 도식과 함께 설명해줘 · explain with diagrams how the campaign tracker reads sub-issues and settles them | An explanation. A sequence diagram for the read, and a specimen anatomy of one claim record. |
| opening-campaign 스킬의 세션 수명주기를 IKEA 매뉴얼처럼 한 페이지로 · the opening-campaign session lifecycle, on one page like an IKEA manual | An explanation. A keyed step chain for the order, and a state machine for the states, sharing one numeral set. |
| garden 릴리스 APK 설치 절차 html로 만들어서 열어줘 · make the garden release APK install procedure an HTML page and open it | A guide. `Goal` replaces `Question`, the steps are `ol.steps`, and step 8 runs `open`. |
| pre-commit 훅들이 뭘 막고 뭘 안 막는지 정리해줘 · write up what the pre-commit hooks block and what they do not | An explanation. A grouped table, and the negative-space section carries the request itself. |
| camera 프리뷰가 느린 원인은 아는데, 어떻게 바꿀지 제안서로 정리해줘 · the camera preview is slow for a known reason; lay the change out as a proposal | A proposal in the fixed section order. The options become keyed panels with numbered prose, and the decisions sit after the recommendation. |
| 새 herdr 세션 목록 화면이 어떻게 생기면 좋을지 그려서 보여줘 · draw what a new herdr session list screen could look like | A proposal. The drawing is the TO-BE half, and the AS-IS half still needs a readable source. |

## Must not fire, 6

| the request | why the run does not start |
|---|---|
| 세션당 토큰 사용량 차트 그려줘 · draw the token-usage-per-session chart | A chart of measured data. Route to the `dataviz` skill. |
| herdr 스포너가 왜 팬 이름을 안 붙였는지 찾아줘 · find out why the herdr spawner did not name the pane | A diagnosis. Route to the `debugger` subagent. |
| camera 릴리스 노트 md로 써줘 · write the camera release notes as markdown | A Markdown document. The working agent writes it. |
| 캠페인 규칙 스펙 업데이트해줘 · update the campaign rules spec | A `.md` specification, which is normative. This skill never authors one. |
| herdr 세션 이름 규칙 바꿔줘 · change the herdr session naming rule | A change to the system. Perform the change, do not document it. |
| 이거 어떻게 하는 게 나을지 제안해줘 · suggest what would be better | No artifact was asked for. `~/.claude/CLAUDE.md` "Deciding" answers it in chat, as named options with one recommendation. |

Two neighbours split on one word. A request to **find** a cause is a
diagnosis and goes to the `debugger`. A request to lay out a change whose
cause is already established is a proposal and starts a run. When the brief
carries no established cause, it is the first one.

A request that must not fire and still reaches the skill ends the run: return
`STATUS: INSUFFICIENT-INPUT`, name the route, and write no HTML.

## Rubric, 22 lines

**Structure**

1. The page opens with `<h1>` and then `dl.provenance`. Nothing else opens
   it: no kicker, no sentence under the title, no summary paragraph, no
   footer.
2. The head carries `<!doctype html>`, `lang`, `charset`, the viewport meta,
   and a `<title>` holding the same words as the `<h1>`.
3. The provenance block carries `Doctype`, one of `Question` or `Goal`, and
   `Updated`, spelled as `references/doctypes.md` spells them, and no
   `Reviewed`.
4. The title is a noun phrase of one to three words. A rewrite keeps the
   title and the path the document already had, and a derived path that holds
   a different subject ended the run instead.
5. The subject is split into 4 to 7 sections. An explanation gives the
   negative space its own section, and a proposal carries it in "what this
   does not do".
6. A proposal runs its sections in the fixed order: the change in one plain
   sentence of at most 50 words, the AS-IS problem, the options, the
   recommendation, what this does not do, what it costs, and the decisions
   last. No decision or veto row appears before the recommendation.
6a. A proposal carries a Domain section only when the change is a change to
   the vocabulary itself. On any other subject a Domain section is a defect,
   and the terms are defined at first use instead.
6b. Every field of "what it costs" is answered, and a field with no cost says
   so in one sentence rather than being left out.
6c. Every losing option is its own named entry stating what it would have
   bought and what it cost. No entry reads "rejected because X".

**Figures**

7. Every section whose subject is a relation carries one component, and no
   section carries two components of one kind. No page carries a summary box
   labelled with its genre, or a comparison drawn as repeated label-value
   rows.
8. Every `<svg>` inside a `<figure>` is at most 620 viewBox units wide, and
   every one over 360 units carries `class="pan"` plus an inline `min-width`
   equal to its viewBox width.
9. Every annotation is at least 10 viewBox units of font size.
10. Every marker id is suffixed per figure and defined inside the same `<svg>`
    that points at it.
11. No table carries more than three columns, no cell holds a sentence, and
    no page carries `class="stack"` or a `data-label`.
12. Every section opens with its figure, file map, or keyed panels, and
    carries at most two connective paragraphs beyond the caption, the legend,
    and the keyed items.
13. Every definition, rule, and mechanism shows one concrete instance from a
    file the run read, and where a proposal owes a Domain section, every entry
    in it shows an example and a counter-example.
14. Every stated count is a count chip, every state, status, mode, and
    doctype inside a sentence is a value chip, every token the reader would
    run or open stays a code span, and the one transition no code performs
    carries the human badge.
15. `scripts/render-check.py <output>` exits 0.

**Language**

16. No sentence carries a contraction, an idiom, or a word from the drop
    lists in `references/plain-writing.md`.
17. Every section heading is a bare noun phrase that names its object.
18. Every caption states a fact about the system, not a fact about the
    drawing.
19. No sentence addresses the person who asked, and no count true only on the
    day of the read appears on the page.

**Grounding**

20. Every claim is observable in a file the run read, and each citation
    carries the commit of the repository its file sits in.
21. The page carries no external asset, no script, and no build step, and it
    opens from `file://` complete.
22. The run wrote exactly one file, at the output path, and changed nothing
    else: no spec, no `INDEX.md` line, no commit. The return message carries
    the status line and the five sections, and `## Grounding` is a superset
    of every file the message names.
