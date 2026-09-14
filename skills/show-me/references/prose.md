# Prose beside code, a figure, or a spec

Rules for the sentences a reader trusts because they sit next to the thing they
describe.

## Never state a count of things you can name — name them

A count is a derived value with no reader: nothing recomputes it, so it goes
stale on the next edit and stays wrong until somebody counts by hand. The names
are checkable by a grep, and adding a member moves a name instead of an
arithmetic.

Bad: "Four sentences, and two of them are also problems."
Good: "Only absence is a reading; the other three are problems."

Bad: "three sources are read and two are absent on an ordinary checkout."
Good: "of the three sources read, `.claude/settings.json` is tracked and the
machine's is written by install-hooks, so the one absent on an ordinary
checkout is `.claude/settings.local.json`."

The tell that you are about to write one: a numeral for something the same
paragraph then enumerates. Delete the numeral, keep the enumeration.

Where a count genuinely is the point — a measurement, a budget, a limit — put
it where something consumes it (a constant a check reads, a test's expected
value) and let the prose point at that, so the number has exactly one home.

## A heading on a change says what is true only after it

A heading that could have been true before the change names the subject, not
the change: the reader learns nothing from it they did not know.

Bad: "The session guard"
Good: "The guard reads the session's role before a write"

## Write for a smart twelve-year-old

Short words, one idea per sentence. A term the reader has not met is defined
where it first appears, or cut. Intelligence is assumed, context is not.

Bad: "The claim is atomic via create-ref semantics."
Good: "Two sessions cannot take one sub-issue: GitHub refuses the second
branch."
