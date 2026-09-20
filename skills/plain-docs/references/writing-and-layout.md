# Writing and layout

## Editorial decisions

Use these editorial defaults without a supplied style guide. They are house preferences, not a certification standard. For professional manual composition, use [manual-design.md](manual-design.md) before choosing the page layout.

- Give each heading a recognizable subject or task. Prefer `Export records` to `Unlocking seamless export capabilities`.
- Use instructions that can be followed: location, action, and expected result. Include prerequisites before the step that depends on them.
- Put one main action in a step. Keep a short consequence or explanation with that step. Use substeps only for an actual dependency.
- Keep exact UI labels, commands, paths, limits, units, and warnings. Distinguish product text from its translated explanation.
- Replace claims with information. `Select Export. The file is saved to Downloads.` is more useful than `Enjoy a seamless and intuitive export experience.` Only assert the save location if the product source establishes it.
- Use consistent nouns. If the UI says `record`, don't alternate between `item`, `entry`, and `asset` just to vary the prose.
- Introduce acronyms where the intended reader needs them. Keep formal writing direct rather than stiff or impersonal.
- Remove a recap when it repeats an already short section. Keep summaries that help readers decide or act.

For Chinese, prefer natural technical prose to word-for-word translation. For example, use `選取「匯出」。` instead of `為了實現無縫的操作體驗，請進行匯出功能的使用。` Preserve distinctions between `匯出` and `导出`, or `檔案` and `文件`, according to the requested locale. Do not auto-convert names, quotations, or UI labels.

## Starting style

Adjust these values to the font, language, readership, and supplied template. Larger type may be needed for accessibility or complex Chinese glyphs. Don't treat the sample PDF as a fixed page budget.

| Element | Starting point |
| --- | --- |
| Page | A4 or Letter according to the request; use A4 if unspecified and state the choice if relevant |
| Margins | About 18-25 mm according to the grid; reserve separate space for page furniture |
| Body | 11 pt English; 11-12 pt Chinese; left aligned |
| Line spacing | About 1.3-1.45 for English and 1.45-1.6 for Chinese; inspect glyph clearance |
| Title | A deliberate scale: often 24-42 pt for document identity and 20-28 pt for chapter titles; calibrate to the page |
| Main headings | 14-16 pt, real bold, sentence case for English |
| Subheadings | 11-12 pt, real bold; usually no more than three visible levels |
| Secondary text | Usually 9-10 pt; keep instructions in body size |
| Color | Near-black body; a limited accent for navigation, callouts, and emphasis; color must not be the sole signal |
| Paragraphs | Consistent spacing; never align using repeated spaces |

Body-text comfort matters more than a dramatic cover. Keep English lines at a readable length; the approximate character-count guidance used for Latin text does not transfer directly to Chinese glyph counts. Judge the actual text block.

## Page behavior

Use the layout engine's paragraph flow, widow/orphan controls where supported, keep-with-next for headings, and repeatable table headers. Don't absolutely position long body paragraphs. Avoid keeping a whole long section together: it can create an unnecessary half-empty page.

Use soft wrapping for long paths and URLs without changing the copied value. Break tables at rows where possible; allow very tall cells to split if necessary. Repeat column headings on each continuation. Give descriptive columns more room than short identifiers. Align comparable numbers consistently and put units in a clear place.

Use tables for comparisons and reference values, not as containers for every paragraph. Keep borders and shading consistent with their role. An ordinary note can be a paragraph with a bold lead-in; a designed notice can use a differentiated surface or rule when it needs prominence. A mandated safety notice must retain its required prominence and content.

Use real screenshots only when the reader needs them. Crop to the relevant context; retain enough of the UI to locate the control. Captions should identify what the reader needs to notice. Don't add a diagram merely to fill white space.

## Document semantics

Use semantic headings, lists, links, captions, and table headers in the authoring format. Add a document title and language metadata. Long PDFs benefit from bookmarks. For a bilingual document, distinguish language runs and reading order when the exporter supports it. Two side-by-side translations can complicate reading order and pagination; use them only when they help the intended audience.

Visual quality and accessibility are separate checks. A readable, selectable PDF may still lack heading tags, useful reading order, or table structure. If those are required, use and validate a tagged export.
