# Verification

A PDF that compiled is not a finished document. Run the checks, then look.

## 1. Source lint

```sh
python3 scripts/lint.py document.tex chapters/*.tex
```

Errors (exit 1): placeholders, chatbot residue, emoji, raw colours, packages
that override the class. Warnings: padding words, Title Case or colon
headings, manual spacing, size commands, straight quotes, three dots, spaced
hyphens, units typed by hand, half-width punctuation in CJK text, internal
files and repository paths, commit hashes, claims of no hazard, and in
manuals, dated history and test status. Fix each
warning or be able to say why it stands (a quoted UI string, a literal
example).

## 2. Build and automatic checks

```sh
python3 scripts/build.py document.tex --render out/ [--expect strings.txt]
```

Runs `latexmk -lualatex` (twice or more, until references settle) and then
`check.py` on the log and the PDF:

| Finding | Level | Meaning |
| --- | --- | --- |
| `tex-error` | error | Compilation failed or recovered from an error |
| `missing-glyph` | error | A character has no glyph in its font: it prints as nothing |
| `overfull` | error | A line or box sticks into the margin by more than 0.5 pt |
| `undefined-ref`, `undefined-cite` | error | A cross-reference or citation prints as ?? |
| `not-embedded` | error | A font is not embedded in the PDF |
| `missing-text` | error | A string from `--expect` is not in the extracted text |
| `font-fallback` | warning | A fixed font was missing; the user must be told |
| `no-label` | warning | A signal word or label is untranslated for a language |
| `underfull` | warning | A very loose line (badness 10000) |
| `no-tounicode`, `type3` | warning | Text may copy wrongly; a bitmap font slipped in |

Use `--expect` for facts that must survive exactly: model numbers, ratings,
limits, part numbers, translated safety wording. One string per line.

## 3. Look at every page

Open `out/contact.png` for the sequence, then each `out/page-NN.png` at
reading size. Check:

**Grid and type**
- Text, numbers and labels sit on the grid: hanging numbers align, body text
  starts on one edge, wide figures span the full measure.
- No widow lines, no heading or step number alone at a page foot, no table
  head without rows below it.
- Line breaks inside names, numbers, units and model numbers (IEC 61010-1,
  12.5 V) do not happen; use `\mbox` or `~` where they do.
- Titles do not leave one word on the last line.

**Figures**
- Every callout number has a legend entry and every legend entry a callout.
- Leaders end on the right feature, do not cross each other or text.
- Labels in drawings are legible (at least 5 pt printed) and spelled as on
  the product.
- Charts: axes labelled with quantity and unit, series distinguishable in
  greyscale.

**Colour**
- Only role colours appear. Render one page with `pdftoppm -gray` and check
  that nothing depends on hue.

**Language**
- Each language uses its fixed fonts (the `Fonts` line of `check.py`).
- CJK: punctuation is full-width and regional; no half-width commas in
  Chinese text; no stray spaces typed between CJK and Latin text.
- RTL: numbers, units and model names read left to right.
- Thai: line breaks fall between words.

**Content**
- Every value matches the source. Every safety message has hazard,
  consequence and avoidance, at the right level.
- The hazard check in `writing.md` has been run; anything the sources do not
  cover is in the delivery note, not written as "no hazard".
- No full safety box appears more than twice; later occurrences are
  embedded messages.
- The document has one reader: no commit hashes, repository paths, agent
  files, incident dates, test status or review notes in a manual.
- Callout numbers run in order on one side or two opposite sides.
- No placeholder, no "TBD", no invented contact or standard.

Fix, rebuild, and look again at the pages that changed and the pages after
them (pagination moves).

## 4. Delivery note

Tell the user, briefly: what was produced; any font fallback or user font;
untranslated or unverified items; facts that were missing from the sources;
contradictions between sources; hazards the sources do not cover; material
left out because it belongs in another document. Do not paste the check
output, and do not put any of this inside the document itself.

## Accessibility (tagged PDF)

Tagged PDF output from LaTeX needs LuaLaTeX with TeX Live 2025 or newer, and
the tagging code must be enabled before the class:

```latex
\DocumentMetadata{lang=en-GB, pdfversion=2.0, pdfstandard=ua-2, tagging=on}
\documentclass{plaindoc}
```

This skill has not been validated for PDF/UA. If accessibility is a
requirement, validate the result with a PDF/UA checker (for example veraPDF)
and report the result; never claim conformance without it. Not every package
the class loads supports tagging yet; see the LaTeX Project's tagging status
page.
