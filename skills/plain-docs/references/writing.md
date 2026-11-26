# Writing

A professional document states facts in the order the reader needs them, in
words the reader already uses. It does not sell, reassure, summarise itself
or fill space. These rules apply in every language; `languages.md` adds the
conventions of each one.

## One reader per document

Before writing, name the reader and what they will do with the document.
Sources for a product usually mix three kinds of material: how to use it,
how well it has been proven, and how it came to be. Each has a different
reader and goes in a different document.

| Material | Example | Where it goes |
| --- | --- | --- |
| How to operate, set up, fix | steps, limits, indicators, specifications | the manual |
| What has been verified | "never tried", test dates, pass/fail per function | a test or status report (`type=report`) |
| How it was developed | commit hashes, branch names, repository paths, incident dates, bench notes | release notes, or nowhere |
| Problems found while writing | contradictions between sources, missing facts | the delivery note to the requester; a review memo if it is long |
| Plans for one occasion | a particular event, shoot or visit | a separate checklist or memo |

In a manual, therefore:

- Identify the version once, by release numbers the reader can check (app
  version, firmware version, hardware revision), on the cover or in *About
  this manual*. No commit hashes, build timestamps or file paths.
- Never refer the reader to files they cannot open: `CLAUDE.md`, `AGENTS.md`,
  repository paths, issue numbers, private notes. Never say where secrets are
  kept.
- State behaviour, not its history. Not "three link drops on 2026-11-24 came
  during full-speed moves; why is not known", but "During full-speed moves the
  link can drop for up to 5 s. Autofocus resumes when the board answers."
- Describe only what exists. A planned or unbuilt feature gets at most one
  line marked as not available, or nothing.
- An internal engineering manual is the exception the user must ask for.
  Even then, keep status in a clearly labelled appendix.

If the sources mix these, write the manual from the first row and tell the
user which other documents the remaining material could become.

## Hazards

A manual never claims that a product has no hazards. Before writing the
safety chapter, check each category below against the product and its
sources:

- electrical: mains, exposed conductors, high voltage, capacitors;
- batteries: lithium cells (fire, swelling, deep discharge, charging,
  transport), wrong chemistry or cell count;
- moving parts: gears, belts, motors that start or move unexpectedly,
  pinch and entanglement points;
- heat: hot surfaces, loads, wires;
- stability and weight: rigs on stands, falling equipment, mounting;
- emissions: lasers, RF, UV, noise;
- misuse that is foreseeable from the product's purpose.

For each category that applies, write a safety message only from facts in
the sources (limits, ratings, the manufacturer's instructions). Where the
product plainly has a hazard the sources do not cover, do not invent the
details and do not write "no hazard": list it in the delivery note and ask
the owner. Choose the signal word from the actual consequence: a lithium pack
that can catch fire is a WARNING, not a NOTICE.

## Repeated safety messages

ANSI Z535.6 distinguishes *grouped* messages (a safety chapter), *section*
messages (a whole section or procedure) and *embedded* messages (one step or
sentence). Use them that way:

- the full message once in the safety chapter;
- a section message (`safety` environment) at the start of the first section
  or procedure where the hazard applies;
- after that, an embedded message (`\pdhazard{level}{one sentence}`) at the
  step it concerns.

The same full box more than twice in a document is noise; readers learn to
skip it, and then skip the one that differs.

## Manuals

IEC/IEEE 82079-1 (*Preparation of information for use*) is the international
standard for instructions. The parts that shape the text:

- **Organise by task.** Chapters follow what the reader does: set up, operate,
  maintain, fix. A reader should be able to open any task and complete it.
- **One term per thing.** Use the name printed on the product or shown on
  screen, exactly, every time. If the panel says OUTPUT, never write "output
  button", "On key" or "enable switch".
- **Mark every string the product shows**: buttons, menu items, dialog
  titles, state words. `\ui{Home the motor?}` in a result line, not plain
  text that reads as part of the sentence.
- **Conditions before actions, results after.** "If OUT is lit, press
  OUTPUT." Then `\result{...}` with what the reader sees.
- **Safety information at the point of use**, before the step it concerns, as
  a safety message with hazard, consequence and avoidance. A general safety
  chapter does not replace it.
- **State limits as numbers** with units: "at least 1.0 mm² wire", not
  "suitable wire".
- **Say what the product is not for** in an intended-use section, only from
  the manufacturer's facts.

Procedures, following the Microsoft Writing Style Guide: a complete sentence
per step with an imperative verb, one action per step, UI names in bold
(`\ui`), no more than seven steps (split longer tasks into sub-tasks). No
"please", "simply" or "you will now".

## Reports

- The title says what was found or decided, not just the topic.
- The summary comes first and contains the numbers and the recommendation.
- Methods are specific enough to repeat. Results state values with units and
  uncertainty. Discussion separates measurement from interpretation and
  states limits once, concretely ("one unit was tested"), not as general
  hedging on every sentence.
- Recommendations are numbered actions with an owner or a condition.
- Every figure and table is referred to in the text before it appears.

## Memos

First paragraph: the decision or request and why, in three sentences or
fewer. Then only what the reader needs to act: what changes, dates, owners.
No greeting, no sign-off paragraph, no "I hope".

## Sentences

- Prefer short sentences with the subject and verb early.
- Use the active voice when the actor matters: "Over-temperature protection
  switches the output off", not "The output is switched off".
- Write numbers as digits with units (`\qty`). Spell out a number only at the
  start of a sentence, or rewrite the sentence.
- Headings in sentence case. A task heading starts with a verb ("Connect a
  load"); a reference heading is a noun phrase ("Specifications").
- Define an abbreviation at first use, unless every reader knows it (USB, AC).
- Write for translation (Microsoft *Global communications*): no idioms, no
  humour, no culture-bound examples, no phrasal verbs where a single verb
  exists ("connect", not "hook up").

## Slop: remove on sight

These patterns make a document read as generated. `scripts/lint.py` flags
many of them; the rest need a reader's eye. The fix is always to say the
specific thing instead.

| Pattern | Example | Instead |
| --- | --- | --- |
| Promotional adjectives | seamless, robust, powerful, intuitive, cutting-edge, state-of-the-art | the measured property: "settles within 50 µs" |
| Inflated verbs | leverage, empower, unlock, elevate, streamline, delve | use, let, open, raise, shorten, examine |
| Throat-clearing | "It is important to note that", "Please note", "In today's world" | delete; state the fact |
| Significance claims | "plays a crucial role", "a testament to" | what it does, with numbers |
| Signposting | "In this section we will explore", "Let's dive in" | the section heading already says it |
| Recaps | "In conclusion", "Key takeaways", a summary of a one-page section | delete, or a real summary at the start |
| Triads and parallel padding | "fast, reliable and secure" without evidence for each | the one claim you can support |
| Reassurance | "Don't worry", "Rest assured", "easily", "simply", "just" | delete; if a step is hard, help instead |
| Hedging everywhere | "may potentially", "could possibly", "generally tends to" | state the limit once, specifically |
| Chat residue | "Certainly!", "I hope this helps", "As an AI" | delete |
| Bold sprinkled in prose | three bold phrases in a paragraph | bold for UI labels and run-in lead words only |
| Lists for prose | every paragraph turned into bullets | bullets only for parallel items |
| Em dashes as all-purpose glue | "The supply—which is robust—works" | a comma, a full stop or parentheses |
| Colon headings | "Safety: What You Need to Know" | "Safety" |
| Invented specifics | made-up ratings, standards, contacts, quotes | ask; mark as missing |
| Provenance in the text | "at commit 744e70d", "kept in CLAUDE.md", "seen on 2026-11-16" | the release version once; history elsewhere |
| Review notes shipped | a chapter of problems found while writing | the delivery note |

Signs of AI writing are signs of a problem, not the problem: the underlying
fault is text that does not carry information. Rewriting to dodge a word list
without adding facts does not fix it.
