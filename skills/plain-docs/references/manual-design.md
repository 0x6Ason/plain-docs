# Professional manual design

Use for new manuals, substantial redesigns, and requests for manufacturer-quality presentation. This is a design workflow, not a mandatory template or a minimum page count.

## Set a direction

| Direction | Reader's need | Useful composition |
| --- | --- | --- |
| Technical equipment | Identify controls, connect correctly, operate, check results, resolve faults | Annotated instrument view; procedure and diagram pairs; numbered figures; reference tables; running section labels |
| Consumer setup | Get a product working with little prior knowledge | Clear sequence; large relevant illustrations; short actions; connection details; visible completion state |
| Software | Locate commands and understand screen states | Actual screenshots; focused annotations; steps next to the relevant screen; task navigation and related topics |
| Formal report | Understand a finding, its evidence, and its implications | Editorial hierarchy; readable prose; charts and tables tied to the argument; stable source notes |

When asked for a manufacturer's visual quality, inspect actual pages and identify what works. Study the layout, not just the brand. A manufacturer may use different systems for a reference manual, quick-start leaflet, and online help export.

## Plan the reader's journey

For equipment, a useful progression is orientation, connection, operation, output, and reference. Include safety, maintenance, or service material only when relevant and supported. Keep prerequisite information before the action that needs it. Let a reader enter at a specific task without reading the whole manual.

Before authoring, write a compact working brief:

```text
Audience and task:
Reference direction and observed principles:
Page format and grid:
Type scale and font roles:
Color roles:
Page types and navigation:
Required figures and authoritative source for each:
Language treatment:
Verification plan:
```

Then sketch a page inventory in plain text. A six-page technical sample might use an opening/contents page, an instrument overview, connections, operation, output verification, and specifications. A shorter job may combine these; a complex real product may need many more pages. Do not add pages to satisfy the example.

## Build a small design system

Use a common grid across page types. On A4, an 18-24 mm outer margin and a six-column grid with consistent gutters is a reasonable starting point. Body text may span four columns while the other two hold a short prerequisite, a control detail, or a figure key. Full-width tables and figures should align to the same outer edges. A two-column legend can sit below a wide drawing. These are choices, not automatic sidebars on every page.

Define styles once: document title, chapter title, section heading, body, step number, table heading, figure label, caption, notice, running head, and footer. Use a font with a credible range of weights and compatible CJK faces. Typical body sizes are 10.5-12 pt English and 11-12 pt Chinese; avoid shrinking core instructions to make a designed page fit. Fit content through composition, rewriting, or another page.

Choose a small palette by role. For example, near-black for reading, blue for navigation and figure callouts, pale gray for a comparison surface, and a distinct notice treatment where warranted. Color must remain distinguishable through labels, shape, or line style. A consistent accent is not the same as adding a colored box behind every paragraph.

Give the opening page a clear document identity, model/scope, and relevant product visual when available. Use verified issue/version information only. A short manual can combine the opening with contents or a quick navigation strip. Use no fake approvals, decorative certification marks, or invented corporate identity.

## Compose page types

- **Overview:** large accurate product drawing, restrained numbered callouts, and a nearby control legend. Show only the views needed to locate the parts. A second view is justified for hidden connectors.
- **Connection:** show endpoints, cable/connector identity, and direction or order. Put prerequisite checks and expected connection state nearby. Avoid decorative process arrows that carry no physical or logical meaning.
- **Procedure:** pair each visual with the action it supports. Use a consistent number column, aligned text starts, and deliberate gaps between steps. Keep the result or relevant notice adjacent. Don't make the reader search across pages for the figure.
- **Screen explanation:** use an actual screenshot from the source. For a clearly fictional demonstration, an original schematic UI is acceptable if labeled as such. Explain the controls or state the reader needs, not every pixel.
- **Reference:** organize comparable values in tables with compact identifiers, unit-aware alignment, repeatable headers, and visible grouping. Avoid placing paragraphs inside cells merely to create a grid.
- **Recovery:** map symptoms to checks and next actions. Distinguish user recovery from service work where the source does. Keep warnings tied to an actual risk and never invent hazards for visual effect.

Vary composition because content roles differ, while retaining shared typography and alignment. Repeating the same heading-list-table arrangement on every page is not a complete manual design system.

## Make technical figures useful

Use supplied CAD, drawings, product photography, or screenshots when authoritative. Prefer crisp vector drawings for ports, connections, control locations, and simple technical relationships. Keep visible text and labels as text. Do not use AI-generated product illustrations as evidence of real connector placement or operating behavior.

For an original fictional sample, define the concept's controls and relationships before drawing; label the product and UI as fictional. Keep every figure consistent with that concept. Don't import real manufacturer assets or marks into the public sample.

Use consistent line weights, view conventions, label sizes, and numbered callouts. Route leaders without crossings; end them on the intended feature, not a vague nearby area. Keep number circles away from important detail. Match every number to a legend entry, and every figure reference to a real figure. Captions should name the view or explain what the reader should notice. If the drawing isn't dimensionally authoritative, don't imply scale or manufacturing accuracy.

## Navigation and pagination

For documents that benefit from navigation, use linked contents, descriptive PDF bookmarks, running section names, and stable page numbers. Use real internal PDF destinations or authoring-tool cross-references. Regenerate and test them after pagination changes. A printed page number must agree with the link target and outline.

Keep headings, captions, and their referents together. Don't isolate a step from its figure or push a complete large section onto a new page when it can split sensibly. Judge empty space by function: grouping and orientation are useful; unexplained half-empty pages from overbroad keep-together rules are defects.

For Chinese, test line breaks and glyph forms in the actual column widths. Reflow the translated page instead of assuming the English frame will fit. Use separate language editions or clearly identified language sections when interleaving would interrupt the procedure. Preserve exact UI labels where needed and explain the language convention once.

## Design acceptance

Technical preflight is one gate. The visual gate asks:

1. Can the reader identify the document and find a task quickly?
2. Does the composition make the intended reading order obvious?
3. Do figures reduce uncertainty about the product or operation?
4. Do labels, legends, and instructions agree?
5. Are hierarchy, alignment, density, and whitespace consistent and purposeful?
6. Do the pages feel like one publication while allowing different content types?
7. Do references, navigation, and multilingual layouts work in the final file?

Don't claim improvement solely because the PDF has more illustrations or color. Fix the specific design weakness shown by the review, and preserve factual and character integrity.
