# Fonts

Every language gets a fixed, professionally drawn face for each role. The
class selects them; documents do not. Use this table unless the user names a
different font or the listed font cannot be used.

LaTeX's default is Computer Modern (Latin Modern), not Times. Times New Roman
itself is a Monotype font that is not freely available on every system and has
no matching mathematics. STIX Two is the Times-style face designed for
scientific and technical publishing, with a companion math font, so it takes
that role here.

## The table

| Script and languages | Serif (reports, memos) | Sans (manuals, headings, labels) | Mono |
| --- | --- | --- | --- |
| Latin: en-US, en-GB, fr, de, es, it, pt-BR, pt-PT, nl, pl, tr, vi, id | STIX Two Text | IBM Plex Sans | IBM Plex Mono |
| Cyrillic: ru, uk | STIX Two Text | IBM Plex Sans | IBM Plex Mono |
| Greek: el | Noto Serif | IBM Plex Sans | IBM Plex Mono |
| Arabic: ar | Noto Naskh Arabic | IBM Plex Sans Arabic | – |
| Hebrew: he | Noto Serif Hebrew | IBM Plex Sans Hebrew | – |
| Devanagari: hi | Noto Serif Devanagari | IBM Plex Sans Devanagari | – |
| Thai: th | Noto Serif Thai | IBM Plex Sans Thai Looped | – |
| Chinese, Hong Kong: zh-HK | Noto Serif CJK HK | Noto Sans CJK HK | Noto Sans Mono CJK HK |
| Chinese, Taiwan: zh-TW | Noto Serif CJK TC | Noto Sans CJK TC | Noto Sans Mono CJK TC |
| Chinese, mainland: zh-CN | Noto Serif CJK SC | Noto Sans CJK SC | Noto Sans Mono CJK SC |
| Japanese: ja | Noto Serif CJK JP | Noto Sans CJK JP | Noto Sans Mono CJK JP |
| Korean: ko | Noto Serif CJK KR | Noto Sans CJK KR | Noto Sans Mono CJK KR |
| Mathematics | STIX Two Math | | |

Why these:

- **STIX Two Text**: Times-compatible proportions and colour, drawn for
  technical text, large Latin, Greek and Cyrillic coverage, true SemiBold,
  and STIX Two Math to match. Its lowercase Greek is designed for formulas,
  so running Greek text uses Noto Serif instead.
- **IBM Plex Sans**: an engineered grotesque with clear figures (1, l, I and 0,
  O are distinct), a SemiBold weight that works as the only bold, and
  companion families for Arabic, Hebrew, Devanagari and Thai, which keeps
  multilingual manuals visually related.
- **Noto CJK** (the same design as Adobe's Source Han): one family with
  separate regional builds. Hong Kong, Taiwan and mainland China draw some
  characters differently and set punctuation differently; using the wrong
  regional build is a visible error to native readers.
- **Noto Serif/Sans for other scripts**: consistent quality and full coverage
  for scripts that Plex and STIX do not cover.

## Which face sets the body

| Type | Body | Headings, labels, captions, tables heads | Bold |
| --- | --- | --- | --- |
| manual | sans | sans SemiBold | SemiBold |
| report | serif | sans SemiBold | SemiBold |
| memo | serif | sans SemiBold | SemiBold |

`body=sans` or `body=serif` overrides the default. CJK text follows the same
split: Noto Sans CJK in a sans body, Noto Serif CJK in a serif body, Noto Sans
CJK Bold for headings.

## Usage rules

- Two weights only: Regular and SemiBold (Plex and STIX SemiBold are mapped to
  `\textbf`). No Light, Thin or Black in text.
- Italic is for Latin-script emphasis, titles of works and variables. CJK,
  Arabic, Hebrew, Devanagari and Thai have no italic; the class maps italic to
  upright there. Use wording or 「」 for emphasis instead.
- Do not set running text in all capitals. Short labels (signal words, the
  brand on a cover) may be capitals with letter-spacing, which the class
  applies.
- Sizes come from the class. Do not use `\large`, `\small` and so on in the
  body.

## Fallback and substitution

If a listed face is missing, the class takes the next one in its chain and
writes `plaindoc font fallback: ...` to the log, which `scripts/check.py`
reports:

| Role | Chain |
| --- | --- |
| Latin serif | STIX Two Text → TeX Gyre Termes → Latin Modern Roman |
| Latin sans | IBM Plex Sans → TeX Gyre Heros → Latin Modern Sans |
| Mono | IBM Plex Mono → Latin Modern Mono |
| CJK | Noto CJK (region) → Source Han (region); none found is an error |

Symbols a text face lacks (STIX Two Text has no arrows, ≤ or ≥) are taken from
STIX Two Math and IBM Plex Sans automatically, and Latin letters and digits
inside Arabic, Hebrew, Devanagari and Thai text come from the Latin face of
the same style. A `Missing character` line in the log is still an error: find
a face that covers it.

When the user names a font, use it:

```latex
\documentclass[type=report]{plaindoc}
\babelfont{rm}{Source Serif 4}                    % Latin serif
\babelfont[russian]{rm}{PT Serif}                 % one language only
\setCJKfamilyfont{zh-HK-rm}{Source Han Serif HC}  % CJK, per region and role
```

Then check its coverage against the real text (`check.py` reports missing
glyphs) and say in the delivery note that the house font replaced the default.

## Installing the fonts

TeX Live 2023 or newer already contains STIX Two (`stix2-otf`) and IBM Plex
(`plex`, `plex-otf`). The other faces are system fonts.

| System | Command |
| --- | --- |
| Debian, Ubuntu | `sudo apt install texlive-luatex texlive-latex-extra texlive-fonts-extra texlive-lang-chinese texlive-lang-japanese texlive-lang-other texlive-lang-arabic texlive-lang-cyrillic texlive-lang-european fonts-noto-cjk fonts-noto-core fonts-ibm-plex latexmk poppler-utils` |
| macOS (Homebrew) | `brew install --cask mactex font-noto-serif font-noto-sans-cjk-hk font-noto-serif-cjk-hk` (swap `hk` for `tc`, `sc`, `jp` or `kr`; other scripts: `font-noto-serif-hebrew` and the matching `font-noto-*` casks) |
| Windows | Install TeX Live or MiKTeX; download Noto CJK from github.com/notofonts/noto-cjk and IBM Plex from github.com/IBM/plex, then "Install for all users". |

After installing system fonts, LuaLaTeX finds them on the next run (it
rebuilds its font database automatically; `luaotfload-tool -u` forces it).

## Resource use

LuaTeX-ja loads each CJK face at each size as a separate font. Measured on
TeX Live 2023: the 14-page example manual with one CJK region peaked at about
3.7 GB of memory; a specimen using five CJK regions in serif and sans peaked
at about 5.5 GB. Build CJK documents on a machine with at least 8 GB, and avoid
mixing more CJK regions than the document needs.
