# Languages

Set the main language with `lang=` and list every other language the document
uses in `otherlangs=`. Switch inside the text with `\begin{lang}{fr}...\end{lang}`
or `\pdlang{fr}{...}`. The class then picks the fonts, hyphenation, text
direction, decimal marker, digit grouping and quotation marks for that
language.

```latex
\documentclass[type=manual, lang=zh-HK, otherlangs={en-GB}]{plaindoc}
```

Microsoft publishes a localization style guide for each language. Its rules
are written for translating software and documentation, so they are a good
reference for register, terminology and punctuation in manuals. Index:
<https://learn.microsoft.com/globalization/reference/microsoft-style-guides>.
The notes below cover what affects typesetting; read the full guide when you
write or review a document in that language. A qualified translator should
review any translated safety text before release.

## What the class sets

| Tag | Language | Direction | Decimal / grouping (`\num{1234567.89}`) | `\enquote` / `\pdq` |
| --- | --- | --- | --- | --- |
| en-US | English (US) | LTR | 1,234,567.89 | “ ” ‘ ’ |
| en-GB | English (UK) | LTR | 1,234,567.89 | ‘ ’ “ ” |
| fr | French | LTR | 1 234 567,89 | « » |
| de | German | LTR | 1.234.567,89 | „ “ |
| es | Spanish (Spain) | LTR | 1 234 567,89 | « » |
| it | Italian | LTR | 1.234.567,89 | « » |
| pt-BR | Portuguese (Brazil) | LTR | 1.234.567,89 | “ ” |
| pt-PT | Portuguese (Portugal) | LTR | 1 234 567,89 | « » |
| nl | Dutch | LTR | 1.234.567,89 | „ ” |
| pl | Polish | LTR | 1 234 567,89 | „ ” |
| tr | Turkish | LTR | 1.234.567,89 | “ ” |
| vi | Vietnamese | LTR | 1.234.567,89 | “ ” |
| id | Indonesian | LTR | 1.234.567,89 | “ ” |
| ru | Russian | LTR | 1 234 567,89 | « » |
| uk | Ukrainian | LTR | 1 234 567,89 | « » |
| el | Greek | LTR | 1.234.567,89 | « » |
| ar | Arabic | RTL | 1,234,567.89 | « » |
| he | Hebrew | RTL | 1,234,567.89 | „ ” |
| hi | Hindi | LTR | 1,234,567.89 | “ ” |
| th | Thai | LTR | 1,234,567.89 | “ ” |
| zh-HK | Chinese (Hong Kong) | LTR | 1,234,567.89 | 「 」 |
| zh-TW | Chinese (Taiwan) | LTR | 1,234,567.89 | 「 」 |
| zh-CN | Chinese (mainland) | LTR | 1,234,567.89 | “ ” |
| ja | Japanese | LTR | 1,234,567.89 | 「 」 |
| ko | Korean | LTR | 1,234,567.89 | “ ” |

Always write numbers with units as `\qty{12.5}{\volt}` and bare numbers as
`\num{...}`: the marker and spacing then follow the language, and quantities
stay left-to-right inside Arabic and Hebrew text. Spanish in Mexico and the US
uses a decimal point; set `\sisetup{output-decimal-marker={.}}` for those
markets.

Signal words and the *Note* label are translated for every tag above except
pt-PT; the class warns when a label is missing. Set or correct one with
`\pdsetstring{pt-PT}{warning}{AVISO}`. The defaults are the common forms in
product documentation for each language; confirm them against the standard
the target market uses (for example ISO 3864-2, ANSI Z535.6, GB 2894 or the
importer's requirements) before release.

## Chinese

**Hong Kong and Taiwan (Traditional).** From Microsoft's Chinese (Traditional)
guide, documentation conventions:

- Full-width ，。、；：！？ and 「」 for quotations and new terms, 『』 inside
  「」. 《》 for book and manual titles. Parentheses ( ) stay half-width.
- Use 、 between items of a list, and 以及 before the last item where English
  has "and".
- A half-width space separates Chinese from Latin letters and digits. The
  class inserts this space automatically, so do not type one.
- Avoid the em dash: it looks like 一. Rephrase, or use a colon or parentheses.
  For numeric ranges use an en dash without spaces (`\qtyrange` does this) or 至.
- Address the reader as 您, never 你 (你們 for the plural). Put 請 before an
  instruction.
- Dates: 2026 年 11 月 25 日 (the class spaces the digits automatically when you
  type 2026年11月25日).
- No italics. Bold is kept for headings and UI labels.
- Hong Kong and Taiwan vocabulary differs; write for the market, for example
  軟件 / 軟體 (software), 網絡 / 網路 (network), 打印 / 列印 (print),
  數據 / 資料 (data).

**Mainland China (Simplified).** Punctuation follows GB/T 15834:
full-width ，。、；：！？, “ ” and ‘ ’ for quotations, 《》 for titles, —— and
…… as two-em marks. Microsoft's Simplified Chinese guide also asks for a
half-width space between Chinese and Latin letters or digits (automatic in
the class). Use 您 for the reader.

Typesetting is handled by LuaTeX-ja: line-start and line-end prohibitions,
punctuation compression, and the regional punctuation metrics (centred marks
for Hong Kong and Taiwan, corner marks for the mainland).

## Japanese

From Microsoft's Japanese guide:

- Desu/masu style for explanations; instructions end in …してください.
  Noun phrases for headings, labels and captions.
- Full-width 。、 and 「」 for help topics, input text and section titles;
  『』 for book titles. Half-width digits and Latin letters.
- A half-width space between full-width and half-width characters (automatic
  in the class); none inside brackets or around 、。.
- A half-width space between a number and its unit, except % and °
  (`\qty` handles this).
- Use から or a hyphen for ranges, not the wave dash 〜.
- Katakana for English loanwords ending in -er, -or, -ar keep the long vowel
  mark: コンピューター, not コンピュータ.

## Korean

Microsoft's Korean guide uses the -세요 ending for instructions and -십시오
only for legal text such as licence terms. Korean separates words with spaces;
follow the National Institute of Korean Language spacing rules. Use a full stop
after a sentence that ends in a verb, even where the English source has a
colon. Check Korean pages visually: LuaTeX-ja spaces Hangul as fixed-width
characters, which can look loose in long paragraphs.

## European languages

- **French**: a no-break space before : and a thin no-break space before ; ! ?,
  and inside « ». babel inserts them, so type `« mot »` or `\enquote{mot}`
  without extra spaces. Decimal comma; thin space between digit groups. Address
  the reader as *vous*.
- **German**: „…“ quotation marks, decimal comma, *Sie* for the reader. Nouns
  are capitalised; compounds with English terms are hyphenated
  (*USB-Anschluss*).
- **Spanish**: ¿…? and ¡…! open and close. The RAE prefers « » in print, then
  “ ”, then ‘ ’. Choose *usted* or *tú* for the audience and keep it
  consistent; safety text normally uses *usted*.
- **Italian, Portuguese, Dutch, Polish**: decimal comma; quotation marks as in
  the table. Brazilian and European Portuguese differ in vocabulary
  (*conectar* / *ligar*, *tela* / *ecrã*): write for the market.
- **Turkish**: dotted İ and dotless ı are different letters, including in
  capitals. Use babel's `\MakeUppercase` (the class does in running heads),
  never ASCII case conversion.
- **Vietnamese**: stacked diacritics; the fixed fonts cover them. Check that
  no tone marks collide with the line above in tight leading.

## Russian, Ukrainian, Greek

« » outside, „ “ inside (Russian and Ukrainian). Decimal comma, space between
digit groups. Russian uses a spaced em dash in sentences. Greek uses « » and
the Greek question mark ; (U+037E, normalised to ;).

## Arabic and Hebrew

Right-to-left text, set by babel's bidi support. Model names, units, numbers
and commands stay left-to-right; `\qty` and `\num` handle that, and other
Latin runs need `\babelsublr{...}`. Choose Western (0–9) or Eastern Arabic
digits (٠–٩) for the market and use one form throughout. Hebrew instructions
are commonly written with יש ל + infinitive.

## Hindi

Devanagari with the danda । as the full stop. Indian digit grouping
(12,34,567.89) is common; siunitx groups in threes, so write such numbers
literally if the market expects lakh and crore grouping.

## Thai

No spaces between words; a space separates phrases and sentences. babel's Thai
patterns provide line breaks; inspect every Thai paragraph for bad breaks and
insert a zero-width space (U+200B) where a break is wrong. Thai official
documents often use Buddhist Era years (CE + 543); ask which the reader expects.

## Style guides

Microsoft localization style guides (PDF, via the index above): [Chinese
(Traditional)](https://aka.ms/chinese-traditional-styleguide), [Chinese
(Simplified)](https://aka.ms/chinese-simplified-styleguide),
[Japanese](https://aka.ms/japanese-styleguide),
[Korean](https://aka.ms/korean-styleguide), [French
(France)](https://aka.ms/french-france-styleguide),
[German](https://aka.ms/german-styleguide), [Spanish
(Spain)](https://aka.ms/spanish-spain-styleguide), [Spanish
(Mexico)](https://aka.ms/spanish-mexico-styleguide), [Portuguese
(Brazil)](https://aka.ms/portuguese-brazil-styleguide), [Portuguese
(Portugal)](https://aka.ms/portuguese-portugal-styleguide),
[Italian](https://aka.ms/italian-styleguide),
[Dutch](https://aka.ms/dutch-styleguide),
[Polish](https://aka.ms/polish-styleguide),
[Turkish](https://aka.ms/turkish-styleguide),
[Vietnamese](https://aka.ms/vietnamese-styleguide),
[Indonesian](https://aka.ms/indonesian-styleguide),
[Russian](https://aka.ms/russian-styleguide),
[Ukrainian](https://aka.ms/ukrainian-styleguide),
[Arabic](https://aka.ms/arabic-styleguide),
[Hebrew](https://aka.ms/hebrew-styleguide),
[Hindi](https://aka.ms/hindi-styleguide), [Thai](https://aka.ms/thai-styleguide),
[English (UK)](https://aka.ms/english-uk-styleguide). For US English, the
[Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/).

Layout requirements: W3C [Requirements for Chinese Text
Layout](https://www.w3.org/TR/clreq/) and [Requirements for Japanese Text
Layout](https://www.w3.org/TR/jlreq/).
