# Colour

Colour in a professional document is information. Each colour has one job,
and a reader who learns the job on page 2 can rely on it on page 40. The class
defines every colour a document may use; documents refer to the role names
and never define their own.

## Roles

| Name | Value | Job | Contrast on white |
| --- | --- | --- | --- |
| `pd-ink` | black (100 K) | All text, rules in tables, drawing outlines | 21:1 |
| `pd-ink2` | 36 % grey | Running heads, section numbers, metadata, secondary labels | 6.7:1 |
| `pd-rule` | 70 % grey | Hairlines between blocks, chart grid lines | 2.1:1 (non-text) |
| `pd-surface` | 5 % grey | Recessed surfaces in technical drawings, nothing else | – |
| `pd-accent` | manual: `#1D4F91`; report and memo: black | Chapter numbers, figure callout markers and leaders | 8.1:1 |
| `pd-danger` `pd-warning` `pd-caution` `pd-notice` | ANSI Z535.1 / ISO 3864-4 safety red, orange, yellow, blue | The signal word panel of a safety message | – |
| `oi-*` | Okabe–Ito palette | Data series in charts | – |

## Rules

1. **Text is black.** Body text, headings, table text, emphasis and links are
   `pd-ink`. Hierarchy comes from size, weight and position, not hue. Coloured
   headings are the single most common sign of a generated document.
2. **One accent, two jobs.** The accent marks navigation (chapter numbers)
   and figure callouts, so the eye can go from a numbered marker in a drawing
   to the same number in the legend. Reports and memos have no accent by
   default. Do not add a second accent.
3. **Every colour must refer to something.** A product colour, a hazard
   level, a data series. If you cannot say what a colour refers to, remove it.
4. **Safety colours belong to safety messages.** They follow the hazard level
   (ANSI Z535.6, ISO 3864-2) and appear only in the signal word panel. Never
   use red for emphasis or orange as a highlight: a reader trained by the
   safety messages will read them as hazards.
5. **Never colour alone.** Data series also differ by marker and dash pattern
   (the `pd/axis` style does this); status in a table is also a word. Charts
   must survive greyscale printing and colour-vision deficiency (WCAG 2.2,
   success criterion 1.4.1).
6. **No decoration.** No tinted boxes behind paragraphs, no gradients,
   shadows, rounded cards, zebra-striped tables, coloured table headers,
   coloured bars beside headings, icons in front of headings, or emoji.
   `scripts/lint.py` rejects raw colour commands for this reason.
7. **Contrast.** Text at least 4.5:1 against its background, large text and
   graphical marks at least 3:1 (WCAG 2.2, 1.4.3 and 1.4.11). `pd-rule` is
   below 3:1 on purpose: hairlines separate, they do not carry meaning.

## Choosing an accent

Use `accent=` only for a real reason, normally the product's or the
organisation's identity colour:

```latex
\documentclass[type=manual, accent=00594F]{plaindoc}
```

Check that it

- reaches 4.5:1 against white (the chapter number and callout digits sit on it
  or are drawn in it);
- is not red, orange or yellow, which are reserved for hazard levels;
- stays dark enough to separate from black ink in greyscale (render with
  `pdftoppm -gray` and look);
- prints: avoid saturated RGB values with no CMYK equivalent.

## Print

The `print` option converts the colour model to CMYK. Body text is pure black
(100 K), never rich black, so small type does not register badly. Keep tints
out of small text: a grey made of halftone dots looks ragged below about 8 pt,
which is why `pd-ink2` is only used at 8 pt and above.

## Charts

Use the `pd/axis` pgfplots style. Series take Okabe–Ito colours in this order:
blue, vermilion, green, orange, purple, sky blue, each with its own marker and
dash pattern. Prefer labelling lines directly at their ends over a legend.
Use grey (`pd-ink2`) for reference lines such as limits and thresholds, and
label them in words.
