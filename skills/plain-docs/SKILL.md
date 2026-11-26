---
name: plain-docs
description: Typeset professional PDF documents in LaTeX (LuaLaTeX and the bundled plaindoc class) - user manuals, equipment and software guides, reports, memos - in 25 languages, with a fixed font for each language, a role-based colour system and build checks. Use when someone asks for a manual, report, memo, specification or other formal document to publication standard, or to fix one that looks generated.
---

# Plain Docs

Produce documents that look and read like a careful publisher made them: a
grid, one type system, colour only where it carries meaning, text that states
facts. Everything is LaTeX, compiled with LuaLaTeX through the `plaindoc`
class in `latex/plaindoc.cls`. The class holds the design decisions; your job
is the content, the structure and the checks.

## Non-negotiables

1. **LaTeX only, through `plaindoc`.** No Word, HTML or ReportLab output, and no
   restyling the class from the document (no `geometry`, `xcolor` colours,
   `titlesec`, `tcolorbox`, font packages). If the user supplies their own
   template or house style, theirs wins: follow it, and apply the rest of this
   skill (fonts, writing, checks) where it does not conflict.
2. **Fixed fonts per language** (`references/fonts.md`). Use them unless the user
   names another font or the named font cannot be used (missing characters,
   cannot be installed, licence). Any substitution is reported to the user.
3. **Colour by role only** (`references/color.md`). Text is black. One accent at
   most, for navigation and figure callouts. Safety colours only in safety
   messages. Data colours only in charts.
4. **No invented facts, no false all-clears.** Do not make up
   specifications, ratings, warnings, certifications, contacts or version
   numbers to make a document feel complete, and never write that a product
   has no hazards: run the hazard check in `references/writing.md` and ask
   about what the sources do not cover. Missing facts are listed back to the
   user.
5. **One reader per document.** A manual is for operating the product. Test
   status, development history (commit hashes, repository paths, incident
   dates), agent files such as `CLAUDE.md` and notes made while writing go
   in a report or in the delivery note, never in the manual.
6. **Verified build.** `scripts/lint.py` and `scripts/build.py` report zero
   errors, and you have looked at every rendered page before delivering.

## Workflow

1. **Brief.** From the request and sources, settle: reader and their task,
   document type (`manual`, `report`, `memo`), language and region (`zh-HK` is
   not `zh-TW`), paper (A4 unless the user is in North America or says Letter),
   and the source of every fact. If the sources mix operating instructions
   with test status or development history, plan separate documents (see
   "One reader per document" in `references/writing.md`). Ask only for facts
   that would change the content.
2. **Plan.** List the chapters or sections and, for a manual, the figures each
   task needs (overview drawing with callouts, connection diagram, screen).
   Manuals are organised by task; reports lead with the finding.
3. **Start from a template** in `templates/` (`manual.tex`, `report.tex`,
   `memo.tex`). Read `references/layout.md` for the components: `steps`,
   `\result`, `safety`, `\pdhazard`, `note`, `description`, `\pdwide`,
   `widetable`, `\pdcallout`, `pdlegend`, `\key`, `\ui`, `\menu`, `\qty`,
   `\hd`, `\pdgroup`, `lang`. Manuals keep the asymmetric grid: numbers,
   terms and labels in the index column, wide tables and figures across both
   columns.
4. **Write** following `references/writing.md`. For any language other than
   English, also follow its entry in `references/languages.md` (conventions
   drawn from Microsoft's localization style guides and national standards).
5. **Draw** technical figures in TikZ with the `pd/*` styles: live text labels,
   leaders that never cross each other or text, a legend that matches every
   number. Never use AI-generated images of the product.
6. **Build and check.**
   ```sh
   python3 scripts/lint.py document.tex
   python3 scripts/build.py document.tex --render out/
   ```
   Fix every error. Read every warning and fix it or know why it stands.
   Then open `out/contact.png` and every `out/page-*.png` and review them
   against `references/verification.md`. Rebuild after each fix.
7. **Deliver** the PDF and its sources (`.tex`, figure files, `plaindoc.cls`).
   In a few lines, tell the user anything they must act on: a font fallback,
   an untranslated label, facts you could not confirm, contradictions between
   sources, hazards the sources do not cover, material left for another
   document. These go in your message, not in the document.

## Setup

Requires TeX Live 2023 or newer (or MiKTeX) with LuaLaTeX, latexmk, Poppler
(`pdftoppm`, `pdffonts`, `pdftotext`) and Python 3.8+. Font installation per
platform is in `references/fonts.md`. `build.py` puts the class on
`TEXINPUTS`; to compile by hand, copy `latex/plaindoc.cls` next to the
document and run `latexmk -lualatex document.tex`.

## When something does not fit

- A component the class lacks: build it from class colours, fonts and the
  `pd/*` TikZ styles, and keep it consistent with the rest of the page.
- Tagged PDF (PDF/UA) is required: see the accessibility section in
  `references/verification.md`; do not claim compliance without a validator.
- Language not in the table: add a row to the language table in
  `plaindoc.cls` (babel name, script, decimal marker, group separator), pick a
  Noto face for its script, check every character with `build.py`, and tell
  the user the language is outside the tested set.
