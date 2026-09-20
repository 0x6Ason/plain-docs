# Validation record

Date: 20 September 2026.

## Designed technical manual

The primary design example is [technical-manual.pdf](examples/technical-manual.pdf), an eight-page manual for the fictional SampleLogger S1. Its source concept and page plan are recorded in [the design brief](examples/technical-manual-brief.md).

| Check | Result |
| --- | --- |
| Skill Creator structural validator after design revision | Passed |
| Sample generation | 8 pages, including Traditional and Simplified Chinese quick references |
| Source-to-PDF extraction comparison | All 315 recorded source strings found in their own text-frame regions after removing whitespace |
| Technical symbols | Minus, plus/minus, inequalities, micro sign, ohm, multiplication, and degree symbols preserved |
| Final PDF font resources | 6 font subsets; all embedded and all with ToUnicode maps |
| Text and page-bound checks | 0 errors |
| Internal navigation | All 16 links resolve; contents and export cross-reference targets checked |
| Bookmarks | 8 destinations, in the expected page order |
| Automated review warnings | 1: missing PDF structure tree; expected for this untagged specimen |
| Final page images | All 8 inspected at 135 dpi; no observed missing glyphs, clipping, overlaps, or stranded opening-line Chinese punctuation |
| Design review | Checked figure callouts, legend correspondence, procedure/figure proximity, table alignment, running navigation, and Chinese reflow |

The builder measures text frames and uses explicit Latin-font fallback for symbols missing from the Chinese fonts. The drawings and schematic interface are original vectors. Product specifications are fictional demonstration data, not claims about real equipment. Passing these checks does not establish usability equivalence with a manufacturer manual.

Reviewed technical manual SHA-256:

```text
06c3c478d5d55e6aea756dd890d9be2ad436419c8691e67edf95334be873b825
```

## Earlier typography specimen and checker tests

| Check | Result |
| --- | --- |
| Skill Creator structural validator | Passed |
| Checker regression tests | 9 passed |
| Sample generation | 3 pages: English, Traditional Chinese, Simplified Chinese |
| Source-to-PDF extraction comparison | All 66 source text strings found on their expected pages after removing whitespace |
| Font coverage | Sample display text checked in every supplied regular/bold face before generation |
| Final PDF font resources | 6 font subsets; all embedded and all with ToUnicode maps |
| Text and page-bound checks | 0 errors |
| Automated review warnings | 1: missing PDF structure tree; expected for this untagged specimen |
| Final page images | All 3 inspected at 150 dpi; no observed missing glyphs, clipping, overlaps, or stranded opening-line Chinese punctuation |

The regression tests cover valid multilingual symbols, corrupt text, leaked tool syntax, missing font glyphs, source preservation, report/input collision protection, invalid UTF-8, extraction failures, clipping against a CropBox, and an embedded-font round trip. Multiple related checks occur in some tests.

The specimen is a demonstration for a fictional product. It was generated through ReportLab 4.4.9 and checked with pypdf 6.10.0, pdfplumber 0.11.9, FontTools 4.65.0, and Poppler on Windows. The tested interpreter was Python 3.12. Regular and bold fonts were Calibri, Microsoft JhengHei, and Microsoft YaHei; collection index 0 was used for the Chinese fonts. Font files are not included in the repository.

Earlier three-page sample PDF SHA-256:

```text
4223b5f50613a3a38c749168ef9228bdde7c6e8ced5198d40f1303468bcfc611
```

PDF timestamps and environment differences may change the binary hash on rebuild. The hash identifies the reviewed file; it is not a promise of reproducible bytes.

## Limits

This validates the helper and the supplied samples, not the future behavior of every model. The samples have no structure tree or language-run tags, and no PDF/UA, PDF/A, or accessibility certification is claimed. Full Word export, large-document stress cases, and cross-agent behavior trials remain untested. Proposed trials are in [evals/scenarios.md](evals/scenarios.md).

The checker reports selected technical signals. Human or model visual inspection is still required, and technical facts must still be checked against a trustworthy source. A reader usability study has not been performed.
