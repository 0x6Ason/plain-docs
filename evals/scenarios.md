# Behavioral evaluation prompts

These are proposed manual trials, not claims of completed model benchmarks. Use a fresh task for each trial. Give the agent the prompt, the skill, and source artifacts only. Inspect the generated file and its working evidence. If comparing with a baseline, keep model, tool access, source material, and output constraints the same; use multiple runs and blinded review before claiming an improvement.

## Short manual

Prompt: “Create a formal PDF user guide from examples/manual-source.json. Use only the English content. Keep all product facts. Use Plain Docs.”

Accept: readable hierarchy; complete prerequisites, actions, outcome, and recovery; no invented support contacts or versions; no gratuitous cover; visible text and successful copy/search; final pages inspected. Don't require exact wording or an exact page count.

## Traditional Chinese and technical symbols

Source: “量測範圍為 −10 °C 至 50 °C。解析度為 0.1 °C。電阻上限為 10 kΩ。允許誤差 ≤ 0.5 °C。尺寸為 20 × 30 mm。”

Prompt: “Make a one-page Traditional Chinese reference PDF from this specification. Preserve the values, signs, and units.”

Accept: all values and symbols survive visually and in extraction; deliberate font coverage/fallback; no conversion to Simplified Chinese; no invented hazards, equipment identity, or certifications. Treat the source as a fictional specification for the trial.

## Broken input

Prompt: “This draft says `FranÃ§ais` and includes a replacement character in a product number. Repair the manual.”

Accept: investigate known encoding paths, preserve the original, and request the original product number where it cannot be recovered. Do not silently guess that number or strip all non-ASCII characters. An intentionally literal corruption example should remain intact.

## Long table and editable Word output

Fixture: create a source table with 50 distinct issue IDs, each with a short symptom and a multi-sentence resolution; include one long file path. Tell the agent the table is authoritative.

Prompt: “Turn this into a formal Word troubleshooting guide and matching PDF.”

Accept: each issue occurs once; repeated table headers; readable widths; no clipped rows or path; semantic Word headings; rendered final output inspected. This package has not yet validated a DOCX exporter end to end.

## User template takes priority

Prompt: “Use my supplied template exactly. Its blue heading color and mandatory warning boxes are required. Apply Plain Docs to the writing and text integrity.”

Accept: retain required template design and warnings. Don't impose black-only headings or remove safety content merely to simplify the page.

## Unsupported accessibility claim

Prompt: “Create an accessible tagged PDF manual from the supplied facts.”

Accept: choose a capable exporter and verify tags/reading order, or disclose what cannot be verified. A successful generic preflight report or a screenshot is not proof of accessibility.

## Lightweight edit

Prompt: “Fix this typo in an existing two-page PDF source and re-export, preserving the design.”

Accept: narrow edit, preserve the source, check affected content and final pagination. Don't add a new template, dependency stack, or research report.

## Rubric

For publication-quality manual requests, also test: “Design a technical equipment manual from the supplied verified product information. Use a manufacturer-quality layout with useful figures and navigation.” Accept a reasoned page plan, consistent grid/type/color roles, accurate and legible figures, sensible variation among page types, and working references. Reject a result that merely adds a colored cover or repeats a plain paragraph-and-table layout regardless of content. Score figure accuracy and reading order independently from visual attractiveness.

Reject an artifact with changed critical values, invented product behavior, broken characters, clipping, missing content, or false verification claims. Otherwise assess task findability, procedural usability, typography, linguistic consistency, and justified use of visuals. Record defects and reader outcomes, not an unsupported “AI percentage.”
