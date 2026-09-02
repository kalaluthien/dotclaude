# Plain writing

Read at step 5, beside `draft-rules.md`, whose rule E points here. Step 7
checks every sentence on the rendered page against it a second time.

The rule set is Simple English Wikipedia, with three replacements. The word
lists give way to the plainest common word for everything that is not an
identifier. The imperative is allowed, and `you` and `we` are not, because an
imperative step already gives the instruction without the pronoun. A domain
noun is defined once, and then reused.

## Caps

| what | cap |
|---|---|
| a step or an instruction | 20 words |
| a description | 25 words |
| a noun cluster | 3 words |
| a paragraph, on one topic | 6 sentences |
| subordinate clauses per sentence | 1 |
| a sequence of 3 or more items | becomes a vertical list |

## Twelve rules

1. **One idea per sentence.** Every cap above comes from this rule.
2. **Simple sentence order.** Subject, verb, object. A subordinate clause
   comes after the object.
3. **No compound sentence.** An embedded `and`, `or`, `but`, or `however`
   joins two ideas that belong in two sentences.
4. **Active voice.** The passive is allowed in a description only, and only
   when the actor is genuinely unknown.
5. **Past or present only.** An `-ing` form is allowed inside a technical
   noun only.
6. **One word, one meaning.** Do not rotate `check`, `verify`, and `confirm`
   for one action.
7. **One part of speech per word.** Write "apply oil to the valve", not "oil
   the valve".
8. **No contraction.** Write `does not`, never `doesn't`.
9. **No idiom and no metaphor.** "Under the hood" names nothing in the
   system.
10. **No ellipsis.** "Files not backed up will be lost" hides which files.
11. **A safety condition or an exception opens the sentence.**
12. **Precision beats brevity.** Keep the longer sentence when a shorter one
    drops a number, a scope, or a condition.

## Words to drop

| group | words |
|---|---|
| intensifiers | simply, just, easily, of course, obviously, actually |
| value words | powerful, elegant, robust, clean, smart, seamless, the whole, the single, the only, the purest, core, key |
| hedges that stack | may possibly, could potentially, seems to |
| reader address | note that, keep in mind, worth remembering, as you can see, we will now |

One word carries an exception. `only` is allowed when it states a restriction
the code enforces, such as "the reader parses `docs/` only". It is not
allowed as emphasis.

## The read-back test

Read every sentence back and ask one question: would a smart reader with no
context follow it on the first pass? Rewrite until the answer is yes.
