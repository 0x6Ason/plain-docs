# Why generated documents go wrong

Investigation date: 20 September 2026.

Design revision: the user's review established that clean typography alone did not meet the requested standard. The skill now includes a professional manual design workflow and a new eight-page technical example. See the [manufacturer study](DESIGN-REFERENCES.md) for the rendered-page observations that informed this change. References to the original three-page specimen below describe the initial text-integrity example.

The reported symptoms are broken or meaningless characters, unnecessary design, and generic writing in generated PDFs. No failing user PDF was supplied, so this is an investigation of plausible failure mechanisms and a tested prevention workflow, not a diagnosis of a particular earlier file. It does not establish how often any model causes these problems.

## Four different problems

| Problem | What it looks like | Useful prevention |
| --- | --- | --- |
| Text corruption | Replacement symbols, garbled punctuation, empty boxes | Preserve encoding; check font coverage and embedding; compare source, extraction, and render |
| Export artifacts | Raw Markdown, internal citation tokens, clipped text | Clean the actual display text; use a flow layout; inspect the final pages |
| Overdesign | Giant cover, repeated cards, irrelevant icons, excessive color | Use a restrained default and require a reader-facing reason for each added element |
| Generic content | Promotional language, repetition, invented details, vague instructions | Ground claims in the source; organize around reader tasks; edit for precision |

The first two are often engineering or workflow defects. The latter two are editorial and design judgments. A single instruction such as “make it professional” leaves all four underspecified. That is a design inference from the mechanisms below, not a published measurement of model behavior.

## What the sources establish

Unicode distinguishes missing-glyph/display failures from incorrect encoding conversions. A replacement character may represent text already lost during a prior decode. Deleting the marker cannot recover the original. This supports preserving source bytes and diagnosing the conversion boundary. [Unicode display problems](https://www.unicode.org/help/display_problems.html).

ReportLab accepts Unicode text, but the selected font still needs the necessary glyphs. TrueType embedding and face registration are separate authoring steps. A Latin-only font or an unconfigured bold face can therefore fail even when the input is valid UTF-8. [ReportLab fonts and encodings](https://docs.reportlab.com/reportlab/userguide/ch3_fonts/).

Embedding fonts reduces substitution across machines, and embedding permissions matter. An embedded subset is a normal portability technique. Embedding alone does not prove correct source text, shaping, or Unicode extraction. [Adobe font embedding](https://helpx.adobe.com/acrobat/desktop/create-documents/explore-advanced-conversion-settings/font-handling-distiller.html).

Noto CJK distinguishes Simplified Chinese, Traditional Chinese, and Hong Kong families. A universal “Chinese font” choice can miss regional preferences. Coverage also varies by file and version. [Noto CJK](https://github.com/notofonts/noto-cjk).

Google's procedure guidance supports numbered actions and clear task sequencing. Its tone guidance favors direct, helpful language over exaggerated claims. A manual should tell the reader what to do and what happens, with the relevant conditions. [Procedures](https://developers.google.com/style/procedures), [voice and tone](https://developers.google.com/style/tone).

Butterick emphasizes body text: size, line spacing, and line length carry much of a document's typographic quality. The skill adapts this into moderate starting values; it does not adopt his personal font blacklist or treat Latin character-count recommendations as Chinese typography rules. [Typography in ten minutes](https://practicaltypography.com/typography-in-ten-minutes.html).

W3C explains that PDF reading order depends on document structure and tag order. A page that looks good can still be difficult to navigate with assistive technology. The sample's visual and extraction checks therefore do not establish accessibility compliance. [W3C PDF reading order](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3).

## What a good formal document looks like

A reader should identify the subject, find a task, follow the sequence, and verify the outcome without decoding the design. The sample uses a title, a short scope statement, prerequisites, numbered actions, an expected result, and a compact troubleshooting table. These sections are present because the fictional task needs them, not because every document must have six sections.

The initial typography specimen uses a single text column, black headings, restrained gray table rules, consistent spacing, and page numbers. This is sufficient for its basic text test, but not a complete professional manual design system. The revised technical example uses annotated equipment drawings, paired procedure layouts, a reference rail, a linked opening, and section navigation. Each composition serves a different reading task while retaining a shared grid and type system.

For example, “Experience a seamless and intuitive export workflow” offers little operational information. “Select Export. Choose CSV (UTF-8), then select Download” identifies actions and exact controls. The latter still needs prerequisites and an expected result when the source supports them.

“AI feel” is treated as a shorthand for observable writing and design problems, not something that can be reliably scored from an author's identity. The skill does not promise detector evasion or require artificial variation in sentence structure.

## What was learned from Ponytail

Ponytail puts decision-making before implementation: question unnecessary work, reuse available solutions, and retain essential correctness checks. The document adaptation asks whether an element helps a reader act, compare, locate, or avoid a relevant mistake. It then uses the simplest representation that serves that purpose. [Ponytail repository](https://github.com/DietrichGebert/ponytail), [reviewed skill source](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md).

Plain Docs does not copy Ponytail's code, install its hooks, adopt persistent modes, or transfer its coding benchmarks to documents. Its short decision sequence is original wording inspired by that general approach. The public package contains one skill and one reusable checker; the remaining files make the research and sample reproducible.

## Observed evidence in this build

The local Microsoft JhengHei face covered the tested Chinese words but did not cover U+2264, U+2265, or U+2212 in its cmap. This is a result for the tested font file, not all CJK fonts or versions. It demonstrates why checking actual code points is better than checking only a font's family name.

The first Traditional Chinese render stranded a comma at the beginning of a line. Extraction succeeded. Visual inspection caught the problem; the sample sentence was rephrased without changing its operational meaning, then rendered again. This supports keeping visual review separate from text checks. The sample renderer is not a general Chinese typesetting engine.

The helper's tests deliberately exercise damaged input, a font without Chinese glyphs, a clipped PDF, a cropped page, missing expected text, and source/report path collisions. Those tests validate the helper, not the quality of future model-generated manuals. See [VALIDATION.md](VALIDATION.md) for the recorded result and [evals/scenarios.md](evals/scenarios.md) for future behavior trials.

The workflow was packaged using the available Skill Creator guidance and the public `SKILL.md` convention. Codex discovers a skill's description before loading its full instructions, so the entrypoint stays focused and detailed checks live in references. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills).
