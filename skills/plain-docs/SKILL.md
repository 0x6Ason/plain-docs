---
name: plain-docs
description: Design professional manuals, technical equipment guides, reports, and PDF or Word documents with deliberate page composition, useful diagrams, clear English or Chinese, and verified text. Use for document design, production, or cleanup, not ordinary chat replies.
---

# Plain Docs

Make documents that look deliberately designed and help readers complete real tasks. Combine editorial structure, page composition, typography, diagrams, and reliable text. Plain means clear, not visually bare. Preserve the user's template, language, branding, and requested scope; the defaults below fill gaps, not override instructions.

## Establish the document

Identify the audience, task, source of truth, output format, and language from the request and supplied material. Ask only about missing facts that would change the content or usability. For Chinese, preserve the source's Traditional or Simplified script and regional terms; ask if the choice matters and cannot be inferred. Supporting both languages does not mean translating every document.

Read the relevant source before designing. For an existing broken file, compare its source, extracted text, and rendered pages before choosing a repair. Without a failing sample, describe likely causes rather than claiming a diagnosis.

Never invent product behavior, limits, certifications, support contacts, approvals, version numbers, or warnings to make a manual feel complete. Mark unresolved facts in the working draft, resolve them before release, or clearly deliver a draft with the missing facts identified. Don't erase uncertainty during polishing.

## Design the document before laying it out

For a new manual, substantial redesign, or a request for professional publication quality, read [manual-design.md](references/manual-design.md). Do not treat a stack of headings, paragraphs, and a table as the completed design brief.

Choose a direction suited to the task: technical equipment manual, consumer setup guide, software guide, or formal report. If the user cites manufacturers or a reference manual, inspect representative rendered pages: an overview, a procedure, and a reference page. Extract general design principles without copying logos, proprietary drawings, or unsupported product details. Do not rely on text extraction to study visual design.

Write a short internal design brief covering the reader's journey, page types, grid, type scale, color roles, navigation, and required figures. Create a page inventory at the level the work needs. Use a supplied design system first. For a small edit, retain the existing system and avoid redesigning unrelated pages.

For a technical equipment manual, consider an annotated hardware view, connection diagrams, procedures with figures beside the relevant steps, display or UI explanations, specification tables, and fault recovery. Use section identifiers, running heads, captions, internal links, and bookmarks when they improve navigation. A useful cover is allowed; it should identify the equipment and document, not merely consume a page.

## Give every element a reader-facing purpose

Before adding a section or visual, identify the reader's need:

1. What must the reader understand or locate on this page? Choose a composition that makes that task obvious.
2. Is there an ordered action? Use numbered steps with real list semantics.
3. Does the reader need to compare repeated fields? Use a table.
4. Does the reader need to locate a control or understand a spatial relationship? Use an accurate screenshot or diagram.
5. Does a notice prevent a relevant mistake or hazard? Place it at the point of action, with a meaningful label.

Omit elements that serve no purpose. Do not minimize away useful design, necessary detail, accessibility, cautions, evidence, or user requests. Use whitespace, alignment, scale, and contrast to establish relationships. Reuse a working template or style system before building another.

For a manual, organize around tasks: scope and prerequisites; the task procedure; expected results; relevant recovery steps; reference data where needed. For a memo or report, lead with the decision or finding and then the supporting explanation. These are options, not a mandatory set of sections.

## Write and typeset

Read [writing-and-layout.md](references/writing-and-layout.md) when drafting or changing presentation. Use descriptive headings, concrete verbs, exact UI labels, and consistent terminology. Remove empty introductions, promotional claims, repetitive summaries, and inflated language. Preserve explanations the reader needs. Do not use word blacklists or AI detectors as a quality measure.

Choose the grid and page composition for the content. Full-width figures, a narrow reference rail beside procedures, or a two-column control legend may be more useful than one continuous text column. Keep long prose readable and the reading order clear. Use a consistent type scale, real font weights, and a limited color system. Use color for navigation, identifiers, status, or emphasis with redundant text/shape cues. Rules, panels, diagrams, and covers are allowed when they strengthen hierarchy or understanding. Avoid generic dashboard cards, random icons, and decorative motifs unrelated to the equipment.

Use the user's requested authoring tool. For editable Word output, use semantic Word styles and lists, then export with a suitable office renderer. For a straightforward PDF, a flow-based engine such as ReportLab Platypus is sufficient. If PDF accessibility is required, choose an exporter that can produce the required tags and reading order; don't assume an arbitrary PDF generator does so. Reuse a working toolchain before adding another.

## Protect text before export

Read [text-integrity.md](references/text-integrity.md) for PDFs, multilingual material, or a broken-character report.

- Keep Unicode text in UTF-8 files. Fix a known encoding error at its source; never silently discard undecodable bytes or remove all non-ASCII characters.
- Inventory the actual characters, including bold headings, table cells, footers, code, punctuation, units, and symbols. Check each intended font against the text assigned to that face. A font family name or a single Chinese test word is not proof of coverage.
- Use explicit CJK font selection and fallback. Check Traditional/Simplified regional forms. Check symbols separately: a CJK font may cover Chinese but miss a mathematical sign. Preserve meaningful symbols and configure a font that can render them.
- Embed or subset fonts when permitted by their license. Test both appearance and extraction. Missing `/ToUnicode` is a review signal, not automatic proof that text is broken.
- Render textual labels as text. Do not generate manual pages, UI screenshots, or technical labels as AI bitmap artwork.
- Remove leaked tool citations, placeholders, and raw markup from the finished prose. Convert citations to usable source references; preserve deliberate literal examples of markup or error messages.

## Verify the actual deliverable

Read [verification.md](references/verification.md). A successful export is not a quality check.

1. Audit the final content and critical product facts against the source.
2. Run the supplied checker when its dependencies are available, or equivalent checks. Investigate errors and review warnings in context; do not automatically delete flagged characters.
3. Extract the PDF text and compare critical strings and quantities with the source. Check English and Chinese copying/searching. Extraction alone cannot validate layout.
4. Render every page of the final file. Review the sequence for coherent page types and rhythm, then inspect at readable scale for clipping, overlap, tables, line breaks, heading placement, symbols, and page furniture. Also assess whether figures explain the task, annotations are legible, alignment follows the grid, and the intended hierarchy is obvious. A contact sheet helps navigation but is not the whole review.
5. Fix demonstrated defects, rebuild, and inspect the affected pages plus any pages whose pagination changed. Verify the last file written, not a prior export.

If rendering or a necessary check is unavailable, describe the exact unverified part and provide an honestly labeled draft when useful. Do not call it verified, accessible, PDF/A, or PDF/UA without the corresponding checks. Stop once the requested content and applicable checks are complete; do not add decorative revisions for their own sake.

Return the requested document and editable source when requested or useful. Keep diagnostic output out of the document itself unless it is the requested subject. Report material limitations briefly. This skill does not authorize installation, publishing, or unrelated changes.
