# Verification

Use the installed environment's equivalent tools when available. The helper is optional; the checks are the workflow. Paths below are relative to the skill folder.

## Helper

Python 3.10+ is required. The source scan uses the standard library. Font checks additionally use `fonttools`; PDF checks use `pypdf` and `pdfplumber`.

```sh
python scripts/preflight.py source final-text.txt
python scripts/preflight.py source heading-text.txt --font /path/to/bold.ttf
python scripts/preflight.py source chinese-body.txt --font /path/to/regular.ttc --font-index 0
python scripts/preflight.py pdf document.pdf --expect critical-strings.txt
python scripts/preflight.py pdf document.pdf --json work/preflight.json
```

For font coverage, provide the actual display text assigned to that face, not a Markdown file whose markup uses other fonts. Check fallback runs separately. The font option checks one selected font, not whether a renderer actually uses it. Expected strings are UTF-8 text with one non-empty string per line; whitespace is ignored for comparison, but punctuation, case, signs, and digits are retained. Use strings such as exact product labels, Chinese headings, and values; this is not a full semantic or translation comparison.

Exit status: 0 means no configured errors were detected; 1 means detected errors; 2 means an input, dependency, or parsing failure. Review warnings even when the exit status is zero. `--warnings-as-errors` makes reviewed warning categories enforceable in a build. JSON reports use `clear`, `review`, or `errors` and always state that visual review is still required. They do not certify the document.

The helper detects invalid UTF-8, replacement/control characters, some leaked citation syntax, missing font glyphs, common mojibake candidates, unextractable PDF pages, missing expected strings, and extracted characters outside the visible page. It reports font embedding, Unicode-map, and document-structure signals. It does not alter files, run OCR, prove all fonts were embedded correctly, detect every overlap, validate scientific meaning, or establish accessibility compliance. Font-resource inventory can include unused resources; an unembedded unused font should be reviewed rather than assumed to have broken the output.

## Render and inspect

For PDF, use a renderer such as Poppler:

```sh
pdftoppm -r 150 -png document.pdf work/page
pdffonts document.pdf
pdftotext -layout document.pdf work/extracted.txt
```

For DOCX, render/export through an available office engine. Inspect the exported pages and the editable file's styles and lists. A ZIP/XML check alone does not verify Word layout.

Inspect every final page at readable scale:

- All text visible; no tofu boxes, corrupt punctuation, accidental symbols, raw citations, or markup.
- No overlap, clipping, content outside margins, or footer collisions.
- Headings with their following content; procedures in a clear order; reasonable page breaks.
- Table widths and wrapping work; continuation headers repeat; no tiny type to force a fit.
- Symbols and numbers match the source, including signs, decimal places, and units.
- Chinese font forms and punctuation suit the selected locale; line breaks do not strand closing punctuation.
- Images and labels are sharp; captions and referents agree; links and page references work where applicable.
- No empty packaging sections or decoration that has no reader-facing function.
- Page composition suits the task: overview drawings, connection figures, procedure pairs, and reference tables use consistent grids and typography.
- Callout numbers match their legends; leaders identify the intended feature; captions, links, bookmarks, and printed page references agree.
- Diagrams and screenshots are large enough to use, not merely decorative thumbnails. Authoritative product details are preserved.

For a request for publication-quality manual design, also run the design acceptance review in [manual-design.md](manual-design.md). A zero-error preflight report does not establish a professional layout.

Keep the source, check report, and page images in a working directory until review is done. After a correction, regenerate from the source and inspect the final file again. If the exporter cannot meet a required quality check, explain that limitation instead of silently weakening the requirement.

## Review record

Record internally: artifact name, source revision or hash, exporter and fonts, pages inspected, text checks, reviewed warnings, and unresolved issues. Only tell the user what they need to assess the deliverable. Do not insert a ceremonial QA checklist into every manual.
