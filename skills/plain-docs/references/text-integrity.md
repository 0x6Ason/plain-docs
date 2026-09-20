# Text integrity

## Diagnose before repairing

| Symptom | Plausible cause | Check and repair |
| --- | --- | --- |
| Empty boxes, bullets, or black squares in place of letters | Missing glyph, unintended Symbol/Dingbats fallback, or font substitution | Compare source code points, the selected font's cmap, embedded fonts, and page render; select a covering font |
| Sequences such as `Ã©` or `â€™` | A wrong encoding conversion | Compare with the original bytes/text; fix the known decoding boundary, not every occurrence of `Ã` |
| Replacement character U+FFFD | An earlier lossy decode or a deliberate literal example | Recover from the original source if available; replacing the visible marker does not recover lost text |
| Looks right, copies incorrectly | Incorrect or missing Unicode mapping, unusual encoding, or ordering | Compare extraction and copy/paste with source; repair export settings or regenerate from good source |
| Chinese missing only in headings | A bold face or fallback differs from the body | Check each face and actual run; register the correct bold font |
| Leaked `turn...search...`, tool citation syntax, or raw markup | Formatting artifacts entered the document source | Replace citations with human-readable references and escape/parse markup correctly |
| Correct letters in the wrong place | Reading order, shaping, bidi, or line-break problem | Use a suitable layout engine and inspect the final output; cmap coverage is insufficient |

These are diagnostic possibilities, not a claim about an unseen PDF.

## Font and encoding choices

1. Preserve the original input and read with the known encoding. Prefer explicit UTF-8 for newly authored files. Never use `errors="ignore"` or ASCII filtering as a repair.
2. Keep a copy of the text as sent to the layout engine. After templating, scan that text too: source markup and final display text differ.
3. For each font face/run, check the actual code points, including punctuation, nonbreaking spaces, units, mathematical operators, Chinese characters, and localized UI labels. Inspect CJK punctuation at line starts and ends.
4. Configure explicit fallback for missing code points. Noto CJK and Source Han provide useful regional families, but verify the particular font file and license. Never assume a font covers all of Unicode.
5. Check bold, italic, and monospace separately. If a true Chinese italic is unavailable, use a deliberate supported emphasis treatment rather than silently falling back to a Latin font.
6. Embed or subset the fonts if permitted. A non-embedded built-in CJK font can depend on the reader's font installation; it is unsuitable as an untested portability shortcut.
7. Verify the final PDF independently through page rendering and text extraction. A cmap check proves code-point coverage only; it does not prove shaping, font routing, visual appearance, or extraction correctness.

Use collection indices for TTC/OTC files. Fonts may carry embedding restrictions; an OS/2 fsType check is a useful flag, not a substitute for the license. Some engines cannot consume certain CFF, variable, or collection formats even when those fonts contain the characters. Convert only when permitted, or choose a supported font.

Do not replace a minus sign, micro sign, multiplication sign, degree symbol, or scientific unit merely because it is not ASCII. Preserve the correct character or use an explicitly approved equivalent. Normalize only with a known purpose; compatibility normalization can change technical identifiers and distinctions.

## Source of text

Use native text for headings, body copy, labels, and commands. Bitmap text can look correct while becoming inaccessible to search, copy/paste, and assistive technology. OCR may be appropriate when recovering a scan, but it needs proofreading, particularly for numbers, punctuation, Chinese characters, and units.

Leaked markup and suspected mojibake need context. A troubleshooting manual may intentionally display those exact strings. The checker is read-only and intentionally reports candidates rather than altering source content.
