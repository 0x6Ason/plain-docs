# Layout and components

## The grid

**Manual (A4).** 20 mm outer margins and a 170 mm full measure, split into a
40 mm *index column* and a 130 mm *body column*. Everything that identifies
sits in the index column: chapter and section numbers, step numbers, figure
and table labels, the *Note* label. Everything to be read sits in the body
column. The reader scans down the left edge to find a place and reads to the
right. Wide figures and tables (`\pdwide`) span both columns. The contents
page follows the same rule: numbers in the index column, titles on the text
edge. The layout is deliberately asymmetric; do not centre the text block or
centre-align text to "balance" a page.

**Report and memo (A4).** One 130 mm column with 40 mm margins. Section numbers,
figure labels and the *Summary* label hang into the left margin so that every
text line starts on the same edge.

Letter paper keeps the same margins; the measure adapts. Body lines run about
75–85 characters in English, inside the 45–90 range recommended by Butterick's
*Practical Typography*; CJK lines hold about 35–40 characters.

## Type scale

| Element | Manual | Report, memo |
| --- | --- | --- |
| Body | Plex Sans 10 pt on 14.2 pt | STIX Two 11 pt on 15.2 pt |
| Chapter | 26 pt SemiBold, number in accent | (with `chapters`) same |
| Section | 14 pt SemiBold | 14 pt SemiBold (memo: 11 pt) |
| Subsection | body size SemiBold | body size SemiBold |
| Tables | small | small |
| Captions, running heads | sans, small / footnote size | same |

Paragraphs are separated by half a line and not indented. Manuals and memos
are ragged right without hyphenation (instructions are easier to follow and to
translate); reports are justified with hyphenation and microtype.

## Components

| Need | Use | Not |
| --- | --- | --- |
| An ordered task | `steps` with `\result{...}` after the step that produces it | a paragraph with "first… then…" |
| A hazard | `safety` with `danger`, `warning`, `caution` or `notice` | bold red text, a coloured box |
| The same hazard again, at a step | `\pdhazard{notice}{One sentence.}` | the full box repeated |
| Terms and their meanings | `description` (terms hang in the index column) | bold term on its own line |
| A table with three or more text columns | `widetable` (spans the index column) | a narrow table that wraps every cell |
| Context the reader may need | `note` (label in the index column) | "Please note that…" |
| Parts of a product | TikZ drawing with `\pdcallout` + `pdlegend` | a photo with arrows added later |
| Comparable values | `xltabular` or `tabularx` with booktabs rules | paragraphs in table cells |
| A physical key / on-screen label | `\key{OUTPUT}` / `\ui{Export}` | quotation marks, capitals |
| A menu path | `\menu{File>Export>PDF}` | "click File, then Export" |
| Code, commands | `\cmd{...}`, `code` environment | screenshots of a terminal |
| A quantity | `\qty{12.5}{\volt}`, `\qtyrange{0}{30}{\volt}` | 12.5V, 12,5 V typed by hand |
| Another language | `lang` environment, `\pdlang` | switching fonts by hand |

### Procedures

```latex
\begin{steps}
\item Press \key{LIMIT}.
      \result{The display shows the set values.}
\item Turn the \ui{VOLTAGE} knob to the voltage your load needs.
\end{steps}
```

One action per step. Put the condition before the action ("If OUT is lit,
press …"). Put the safety message *before* the steps it applies to.

### Safety messages

```latex
\begin{safety}{warning}[Electric shock from damaged mains connections]
A damaged power cord or inlet can expose mains voltage.
\begin{itemize}
\item Use only the supplied power cord.
\item Do not use the instrument if the cord or case is damaged.
\end{itemize}
\end{safety}
```

The structure follows ANSI Z535.6 and ISO 3864-2: a signal word panel
(safety alert symbol, signal word, hazard colour) and a message panel with
the hazard, the consequence and how to avoid it. Levels:

| Level | Use when not avoiding the hazard |
| --- | --- |
| `danger` | will cause death or serious injury |
| `warning` | could cause death or serious injury |
| `caution` | could cause minor or moderate injury |
| `notice` | could damage property; no personal injury (no alert symbol) |

Choose the level from the actual risk. Do not raise a level for emphasis, do
not stack several messages for one hazard, and do not invent hazards. Run the
hazard check in `writing.md` before writing any of them.

After a hazard has had its full message, later steps carry an embedded
message, a signal-word label at the start of one sentence:

```latex
\item Press \ui{Home motor}.
      \pdhazard{notice}{Only \key{SW1} or \ui{STOP} cuts the motor's power during a homing.}
```

### Figures and technical drawings

```latex
\begin{figure}[h]
\pdwide{\centering
\begin{tikzpicture}[pd/drawing, x=1mm, y=1mm]
  \draw[pd/part, rounded corners=3mm] (0,0) rectangle (150,66);   % outline
  \draw[pd/detail] (8,28) rectangle (80,58);                      % detail
  \pdcallout{1}{(30,58)}{(30,76)}  % number, point on the part, marker position
\end{tikzpicture}}
\caption{Front panel. Numbers refer to the list below.}
\end{figure}
\begin{pdlegend}
\legenditem{1}{Display}{Output voltage and current, mode and status.}
\end{pdlegend}
```

Drawing conventions:

- Two line weights: `pd/part` 0.75 pt for outlines, `pd/detail` 0.4 pt for
  everything inside. `pd/hidden` (dashed) for hidden edges, `pd/surface` for a
  recessed or glass area.
- Labels printed on the product are live text in the drawing, at the size
  they would read on the product relative to the drawing.
- Callout markers sit outside the outline on one side or two opposite
  sides (above and below, or left and right), never all four. Numbers run
  left to right along the top row, then left to right along the bottom row
  (top to bottom for side columns). A skipped or out-of-order number is an
  error. Leaders are straight, vertical or horizontal where possible, end on
  the feature with a dot, and never cross another leader or run through
  text.
- The legend lists every number once, in order, with the part name as printed
  on the product.
- Draw only what the reader must locate. A drawing is not a photograph.
- For a fictional or schematic product, say so in the caption. Never present
  an AI-generated image as the product.

### Term lists

`description` hangs each term in the index column (manuals) or the margin
(reports, memos), right-aligned like the other labels, with its meaning on
the text edge. Long terms wrap inside the column. Use it for indicator
meanings, parts of a system, status categories.

### Tables

Booktabs rules only: a heavy rule at top and bottom, a light rule under the
header, no vertical rules, no fills. Use `L` (ragged-right `X`) and `P{width}`
(ragged-right `p`) columns so narrow cells do not justify into gaps. Short
tables are `tabularx` and stay in one piece; tables that may cross a page are
`xltabular` with the head repeated through `\endhead`. In manuals, a table
with three or more columns of running text is a `widetable`, which spans the
index column as well, takes its caption as an optional argument and breaks
across pages:

```latex
\begin{widetable}[{Problems you can see on the screen.\label{tab:screen}}]{P{40mm}LL}
\toprule \hd{Seen} & \hd{Cause} & \hd{Do} \\ \midrule \endhead
...
\bottomrule
\end{widetable}
```

The class sets a taller row strut, so rows whose cells wrap stay distinct
without rules between them. Column heads with `\hd{...}`, group rows
with `\pdgroup{...}`, units in the cells through `\qty` or in the head in
parentheses. Align decimal columns with siunitx `S` columns.

### Charts

`\begin{axis}[pd/axis, ...]`: left and bottom axes only, light horizontal
grid, Okabe–Ito colours with markers and dash patterns. Label lines directly
at their ends instead of using a legend box when there is room, and draw
limits as grey dashed lines labelled in words.

## Page flow

- Manual chapters start on a new page; a chapter title never sits at the
  bottom of a page.
- Keep a figure on the page where it is first referred to, or the next one.
- Never leave a heading, a step number or a table head alone at the bottom of
  a page; the class sets the penalties, check the result.
- Cover (manuals): brand, product and document type, one product drawing,
  document number, version and date. No background images, no colour fields.
  The subtitle is the document type in a few words ("User manual"); the scope
  goes in *About this manual*. The brand line is left out automatically when
  it repeats the product name.
- Running heads: product and document type on the left, chapter on the right;
  document number and version in the footer, page number at the outer edge.

## Visual slop to remove on sight

Coloured or gradient headings · icons before headings · emoji · tinted
"callout" boxes for ordinary notes · rounded cards and drop shadows ·
zebra-striped tables · vertical rules in tables · all-caps paragraphs · centred
body text · decorative full-width rules between sections · a cover with a
stock photo or abstract shapes · several accent colours · figures that only
fill space · bullet lists where a sentence would do · bold scattered through
running text.
