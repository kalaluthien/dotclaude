# <Title>

<!--
  Specification — the normative record: what must stay true and why. Copy
  to docs/<name>.md and fill in. Delete every comment, including this one;
  the document must read as if written directly. The .md extension is the
  kind — a spec carries no Doctype field.

  When a spec and the artifact disagree, one of them is wrong — fix
  whichever lost, in the same change. A spec sentence is a predicate on
  system properties, a generating rule on system structure, or a decision
  record with reasons — never a mirror of what the artifact already says.
  A numeric or enum value carries either the reason and date that make it
  a decision, or a note that the artifact's own constant owns it.

  One template, several section shapes. Purpose is required; after it, use
  the shape the content has, and only that shape:
  - decision:   "## Decision: <the decision> (<YYYY-MM-DD>, <who asked>)" —
                the body carries the alternative that lost and why, so a
                future reader can tell whether the reason expired.
  - rule:       one section per generating rule or predicate, applicable
                to code the reader has never seen.
  - procedure:  numbered full-sentence steps; a branch exit is a labelled
                sub-item under its step; a step names the script that runs
                it rather than restating the script. An operational
                procedure states its trigger (the observable signals that
                select it), its verification (the observable resolved
                state), and its rollback (or why none exists).
  - capability: "## Behavior" (predicates, naming the owner of every piece
                of state read), "## Configuration" (the control surface
                and persistence; "None — <why>" is a valid answer),
                "## Acceptance" (observable checks, naming the test that
                automates each).
  - ledger:     "## Non-goals and deferred work" — reason and date per
                row; never re-litigate an entry without reading its
                reason; delete the section when empty.

  required-fields: Status, Scope, Last verified
  required-sections: Purpose

  rubric:
  - [ ] GROUND RULE: the spec is short — every sentence is a predicate,
        rule, step, or decision; background and evidence are cut or moved
        to a view.
  - [ ] Purpose states what the reader gets and why this exists, before
        any mechanism.
  - [ ] No sentence mirrors the artifact.
  - [ ] Every decision heading carries the decision; its body carries the
        losing alternative and why it lost.
  - [ ] Every value carries a reason and date, or names the constant that
        owns it.
  - [ ] Each section uses exactly one shape from the list above.
-->

- **Status**: Active <!-- or: Superseded by <file> -->
- **Scope**: <!-- one sentence: what questions this document answers -->
- **Last verified**: <!-- YYYY-MM-DD — checked against the artifact -->

## Purpose

<!-- What the reader gets and why this exists, before any mechanism. -->

## <The first decision, rule, procedure, or capability>
