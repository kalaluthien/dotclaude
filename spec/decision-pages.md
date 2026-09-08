# Decision pages

Normative. A decision page is where a decision about an unversioned thing is
recorded, and where a rejected option keeps its kill reason. Git holds neither:
history cannot be rewritten to carry a decision taken before it, and a pool
memory is untracked and dies with a rename.

## What a decision page is

A view under `docs/`, one page per **subject**, holding that subject's decisions
in dated entries. It is an explanation page: the provenance block, the title and
the prose rules were the `writing` skill's, retired in `f94ce33`, and this spec
adds nothing to them and restates none of them.

The page records only what version control cannot:

- a change to something git does not track,
- an option that was rejected, with what it would have bought and what it cost,
- the evidence a later reader would otherwise have to re-derive.

Anything the tree already states belongs in the tree.

## Where it lives, and how it is addressed

- `docs/<slug>.html`, the slug being the subject in kebab-case, and its
  `<body>` carries `class="decision-page"`. `docs/` holds views of every kind,
  and only a page that declares itself is held to the
  rules below — an ordinary explanation's `<h2>First section</h2>` is not a
  malformed decision. A page that omits the marker is checked for nothing but
  its links, which is the cost of the declaration and is why it is one word.
- `docs/INDEX.md` carries one line per page. It is the only markdown `docs/`
  holds, and it is what a repository's file naming is read from.
- Every decision is an `<h2 id="...">` whose text opens with its ISO date. That
  `id` is the address: a memory, a commit message, or another page links to
  `docs/<slug>.html#<id>`, never to the page alone.

An `id` is permanent. Renaming one breaks every inbound link, and the links are
the only thing that makes the record reachable.

## Append-only

A recorded decision is never rewritten and never deleted. What changes it is a
later dated entry that names the earlier one and says what it supersedes — in
whole or, more usually, in one clause. A page that edits its own past cannot be
told from a page that never held the fact.

## What the check refuses

`hooks/check-decision-page.py`, registered as a `PostToolUse` hook. It allows
with 0 and refuses with 2; any other code is the script's own failure and
refuses nothing. `PostToolUse` fires after the write has landed, so the refusal
does not undo it — it puts the reason in front of the model that wrote it, which
is the only correction left once the bytes are on disk.

A link is checked when it can only mean this `docs/` **and** sits in a file
inside this checkout: spelled from the home directory (`~/.claude/docs/...`,
`$HOME/...`, `/Users/<user>/...`) anywhere under it — a pool memory included,
since the pools live here — or written relative inside `docs/` itself. A file
outside the checkout is skipped and says so; a scratch note in `/tmp` is
nobody's contract.

A bare `docs/x.html#y` elsewhere names some other repository's `docs/` and is
left alone, and so does a URL that merely ends in a page and a fragment
(`https://docs.python.org/3/library/re.html#re.DOTALL`).

The three entry rows below hold on a **declared** decision page only, and every
rule is read from the page with its HTML comments removed: commented-out markup
is not in the page.

| refused | why |
|---|---|
| markdown under `docs/` other than `INDEX.md` | a view is HTML, and `spec/` is where normative markdown lives. Judged by the name, before the file is read, so a `.md` that is not even text is caught. A stylesheet, a font or a rendered PNG is what a view needs and is not refused |
| an `<h2>` with no `id` | an entry with no address cannot be linked, so it cannot be cited |
| an `<h2>` whose text does not open with `YYYY-MM-DD` | undated, the entry cannot be ordered or superseded |
| two `<h2>` elements sharing an `id` | the link resolves to whichever the browser reaches first |
| a link into this `docs/` that names no existing page or `id` | this is the failure the record exists to prevent. Checked on every page under `docs/`, declared or not |

The provenance block, the doctype and the prose are **not** checked here. They
were the `writing` skill's `render-check.py`'s, and a second reader of one rule
drifts from the first. That skill was retired in `f94ce33`, so those three are
contract with no checker until one is written.

## The option that lost

**One page per decision, as a `proposal` view.** It would have bought the
strongest fit with the `writing` skill's own conventions: `Status: Accepted
YYYY-MM-DD` is already a decision record, and "one idea per proposal" is already
the rule. It cost the move itself — the two live `history-*` files hold roughly
a dozen decisions between them, and a dozen HTML pages each needing a render and
a read-back is a price the record does not repay. A dated `<h2>` inside one
subject's page carries the same date, evidence and kill reason at a fraction of
it, and the subject is the unit a reader actually looks things up by.
