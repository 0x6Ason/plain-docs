% plaindoc.cls -- restrained LuaLaTeX class for manuals, reports and memos.
% Part of Plain Docs (MIT licence). Compile with LuaLaTeX only.
%
%   \documentclass[type=manual, lang=en-GB, otherlangs={zh-HK}]{plaindoc}
%
% Options
%   type        manual | report | memo                       (default report)
%   lang        main language as a BCP 47 tag (table below)   (default en-US)
%   otherlangs  further tags used in the document, e.g. {zh-HK, fr}
%   paper       a4 | letter                                   (default a4)
%   accent      HTML hex for navigation and figure callouts   (manual 1D4F91, others black)
%   body        serif | sans                                  (manual sans, others serif)
%   chapters    report: chapters instead of sections at the top level
%   twoside     two-sided running heads (the index column stays on the left)
%   print       convert colours to CMYK
%
% The rules behind every value here are in references/*.md.

\NeedsTeXFormat{LaTeX2e}[2022-06-01]
\ProvidesClass{plaindoc}[2026/11/25 v1.0 Plain Docs class]

\RequirePackage{iftex}
\ifluatex\else
  \ClassError{plaindoc}{Compile with LuaLaTeX}%
    {plaindoc needs LuaLaTeX (font fallback, CJK, bidi).
     Run: latexmk -lualatex file.tex}
\fi

% ==================================================================
% Options
% ==================================================================
\ExplSyntaxOn
\tl_new:N \l_pd_type_tl
\tl_new:N \l_pd_lang_tl
\clist_new:N \l_pd_otherlangs_clist
\tl_new:N \l_pd_paper_tl
\tl_new:N \l_pd_accent_tl
\tl_new:N \l_pd_body_tl
\bool_new:N \l_pd_twoside_bool
\bool_new:N \l_pd_print_bool
\bool_new:N \l_pd_chapters_bool
\keys_define:nn { plaindoc }
  {
    type       .choices:nn  = { manual, report, memo }
                              { \tl_set_eq:NN \l_pd_type_tl \l_keys_choice_tl },
    type       .initial:n   = report,
    lang       .tl_set:N    = \l_pd_lang_tl,
    lang       .initial:n   = en-US,
    otherlangs .clist_set:N = \l_pd_otherlangs_clist,
    paper      .choices:nn  = { a4, letter }
                              { \tl_set_eq:NN \l_pd_paper_tl \l_keys_choice_tl },
    paper      .initial:n   = a4,
    accent     .tl_set:N    = \l_pd_accent_tl,
    body       .choices:nn  = { serif, sans }
                              { \tl_set_eq:NN \l_pd_body_tl \l_keys_choice_tl },
    chapters   .bool_set:N  = \l_pd_chapters_bool,
    chapters   .default:n   = true,
    twoside    .bool_set:N  = \l_pd_twoside_bool,
    twoside    .default:n   = true,
    print      .bool_set:N  = \l_pd_print_bool,
    print      .default:n   = true,
  }
\ProcessKeyOptions [ plaindoc ]

\cs_new:Npn \pd@iftype #1#2#3 { \str_if_eq:VnTF \l_pd_type_tl {#1} {#2} {#3} }
\cs_new:Npn \pd@ifchapters #1#2
  { \bool_lazy_or:nnTF { \str_if_eq_p:Vn \l_pd_type_tl { manual } } { \l_pd_chapters_bool } {#1} {#2} }
\tl_if_empty:NT \l_pd_body_tl
  { \str_if_eq:VnTF \l_pd_type_tl { manual } { \tl_set:Nn \l_pd_body_tl { sans } }
                                            { \tl_set:Nn \l_pd_body_tl { serif } } }
\cs_new:Npn \pd@ifsansbody #1#2 { \str_if_eq:VnTF \l_pd_body_tl { sans } {#1} {#2} }
\cs_new:Npn \pd@iftwoside #1#2 { \bool_if:NTF \l_pd_twoside_bool {#1} {#2} }
\cs_new:Npn \pd@ifletter #1#2 { \str_if_eq:VnTF \l_pd_paper_tl { letter } {#1} {#2} }
\tl_if_empty:NT \l_pd_accent_tl
  { \str_if_eq:VnTF \l_pd_type_tl { manual } { \tl_set:Nn \l_pd_accent_tl { 1D4F91 } }
                                            { \tl_set:Nn \l_pd_accent_tl { 000000 } } }
\cs_new:Npn \pd@accenthex { \tl_use:N \l_pd_accent_tl }
\ExplSyntaxOff

% ==================================================================
% Base class: KOMA-Script
% ==================================================================
\pd@iftype{manual}{\def\pd@fontsize{10pt}}{\def\pd@fontsize{11pt}}
\edef\pd@baseopts{fontsize=\pd@fontsize, parskip=half-, numbers=noenddot,
  \pd@iftwoside{twoside}{oneside}}
\pd@ifchapters
  {\expandafter\LoadClass\expandafter[\pd@baseopts, open=any]{scrreprt}}
  {\expandafter\LoadClass\expandafter[\pd@baseopts]{scrartcl}}

% ==================================================================
% Grid. Manual: an index column (numbers, labels, captions) and a body
% column. Report and memo: one column; numbers hang into the margin.
% ==================================================================
\newlength\pd@outer  % paper edge to the full measure
\newlength\pd@hang   % index column including its gutter
\newlength\pd@full   % full measure = index column + body column
\newlength\pd@numgap % gap between a hanging label and the text it labels
\setlength\pd@numgap{4mm}
\pd@iftype{manual}
  {\setlength\pd@outer{20mm}\setlength\pd@hang{40mm}}
  {\setlength\pd@outer{40mm}\setlength\pd@hang{0mm}}
\pd@ifletter
  {\def\pd@paperopt{letterpaper}\setlength\pd@full{\dimexpr215.9mm-2\pd@outer\relax}}
  {\def\pd@paperopt{a4paper}\setlength\pd@full{\dimexpr210mm-2\pd@outer\relax}}
\RequirePackage{geometry}
\pd@iftwoside{\geometry{asymmetric}}{}
\geometry{\pd@paperopt,
  left=\dimexpr\pd@outer+\pd@hang\relax, right=\pd@outer,
  top=28mm, bottom=28mm, headsep=10mm, footskip=14mm, headheight=18pt}
\raggedbottom
\widowpenalty=10000 \clubpenalty=10000 \displaywidowpenalty=10000
\setlength\emergencystretch{1.5em}
\hfuzz=.5pt % overfull lines under 0.5 pt are invisible; anything larger is reported

% ==================================================================
% Colour roles. Documents use these names and nothing else.
% ==================================================================
\RequirePackage{xcolor}
\definecolor{pd-ink}{gray}{0}          % text: pure black, prints as 100 K
\definecolor{pd-ink2}{gray}{0.36}      % secondary text: heads, numbers, meta (7.2:1)
\definecolor{pd-rule}{gray}{0.70}      % hairlines
\definecolor{pd-surface}{gray}{0.95}   % the one tint, for figure surfaces
\definecolor{pd-accent}{HTML}{\pd@accenthex}
% Safety colours: screen approximations of ANSI Z535.1 / ISO 3864-4
% (PANTONE 186 C, 151 C, 109 C, 285 C). Only inside safety messages.
\definecolor{pd-danger}{HTML}{C8102E}
\definecolor{pd-warning}{HTML}{FF8200}
\definecolor{pd-caution}{HTML}{FFD100}
\definecolor{pd-notice}{HTML}{0072CE}
% Data colours: Okabe & Ito, Color Universal Design. Only for data.
\definecolor{oi-black}{HTML}{000000}
\definecolor{oi-orange}{HTML}{E69F00}
\definecolor{oi-skyblue}{HTML}{56B4E9}
\definecolor{oi-green}{HTML}{009E73}
\definecolor{oi-yellow}{HTML}{F0E442}
\definecolor{oi-blue}{HTML}{0072B2}
\definecolor{oi-vermilion}{HTML}{D55E00}
\definecolor{oi-purple}{HTML}{CC79A7}
\ExplSyntaxOn
\bool_if:NT \l_pd_print_bool { \selectcolormodel{cmyk} }
\ExplSyntaxOff

% ==================================================================
% Languages: one table drives babel, fonts, CJK regions, numbers, quotes.
%   tag | babel name | script | decimal marker | digit group separator
% ==================================================================
\ExplSyntaxOn
\prop_new:N \g_pd_lang_prop
\cs_new_protected:Npn \pd_deflang:nnnnn #1#2#3#4#5
  { \prop_gput:Nnn \g_pd_lang_prop {#1} { {#2}{#3}{#4}{#5} } }
\pd_deflang:nnnnn {en-US} {american}   {latn}    {.} {,}
\pd_deflang:nnnnn {en-GB} {british}    {latn}    {.} {,}
\pd_deflang:nnnnn {fr}    {french}     {latn}    {,} {\,}
\pd_deflang:nnnnn {de}    {ngerman}    {latn}    {,} {.}
\pd_deflang:nnnnn {es}    {spanish}    {latn}    {,} {\,}
\pd_deflang:nnnnn {it}    {italian}    {latn}    {,} {.}
\pd_deflang:nnnnn {pt-BR} {brazilian}  {latn}    {,} {.}
\pd_deflang:nnnnn {pt-PT} {portuguese} {latn}    {,} {\,}
\pd_deflang:nnnnn {nl}    {dutch}      {latn}    {,} {.}
\pd_deflang:nnnnn {pl}    {polish}     {latn}    {,} {\,}
\pd_deflang:nnnnn {tr}    {turkish}    {latn}    {,} {.}
\pd_deflang:nnnnn {vi}    {vietnamese} {latn}    {,} {.}
\pd_deflang:nnnnn {id}    {indonesian} {latn}    {,} {.}
\pd_deflang:nnnnn {ru}    {russian}    {cyrl}    {,} {\,}
\pd_deflang:nnnnn {uk}    {ukrainian}  {cyrl}    {,} {\,}
\pd_deflang:nnnnn {el}    {greek}      {grek}    {,} {.}
\pd_deflang:nnnnn {ar}    {arabic}     {arab}    {.} {,}
\pd_deflang:nnnnn {he}    {hebrew}     {hebr}    {.} {,}
\pd_deflang:nnnnn {hi}    {hindi}      {deva}    {.} {,}
\pd_deflang:nnnnn {th}    {thai}       {thai}    {.} {,}
\pd_deflang:nnnnn {zh-HK} {}           {hani-hk} {.} {,}
\pd_deflang:nnnnn {zh-TW} {}           {hani-tw} {.} {,}
\pd_deflang:nnnnn {zh-CN} {}           {hani-cn} {.} {,}
\pd_deflang:nnnnn {ja}    {}           {jpan}    {.} {,}
\pd_deflang:nnnnn {ko}    {}           {kore}    {.} {,}

\cs_new:Npn \pd_field:nn #1#2 { \exp_args:Ne \pd__field:nn {#1} {#2} }
\cs_new:Npn \pd__field:nn #1#2
  { \prop_if_in:NnT \g_pd_lang_prop {#1}
      { \exp_args:Ne \tl_item:nn { \prop_item:Nn \g_pd_lang_prop {#1} } {#2} } }
\cs_new:Npn \pd@field #1#2 { \pd_field:nn {#1} {#2} }
\prg_new_conditional:Npnn \pd_if_cjk:n #1 { p, T, F, TF }
  {
    \str_case_e:nnF { \pd_field:nn {#1} {2} }
      { {hani-hk}{\prg_return_true:} {hani-tw}{\prg_return_true:}
        {hani-cn}{\prg_return_true:} {jpan}{\prg_return_true:} {kore}{\prg_return_true:} }
      { \prg_return_false: }
  }
\cs_new_eq:NN \pd@ifcjk \pd_if_cjk:nTF
\msg_new:nnn { plaindoc } { unknown-lang } { Unknown~language~tag~'#1'.~Supported~tags:~#2 }
\clist_new:N \g_pd_langs_clist
\clist_gput_right:NV \g_pd_langs_clist \l_pd_lang_tl
\clist_gconcat:NNN \g_pd_langs_clist \g_pd_langs_clist \l_pd_otherlangs_clist
\clist_gremove_duplicates:N \g_pd_langs_clist
\tl_new:N \g_pd_known_tl
\prop_map_inline:Nn \g_pd_lang_prop { \tl_gput_right:Nn \g_pd_known_tl { #1~ } }
\clist_map_inline:Nn \g_pd_langs_clist
  { \prop_if_in:NnF \g_pd_lang_prop {#1}
      { \msg_error:nnnV { plaindoc } { unknown-lang } {#1} \g_pd_known_tl } }
\bool_new:N \g_pd_cjk_bool
\bool_new:N \g_pd_rtl_bool
\tl_new:N \g_pd_firstcjk_tl
\clist_map_inline:Nn \g_pd_langs_clist
  {
    \pd_if_cjk:nT {#1}
      { \bool_gset_true:N \g_pd_cjk_bool
        \tl_if_empty:NT \g_pd_firstcjk_tl { \tl_gset:Nn \g_pd_firstcjk_tl {#1} } }
    \str_case_e:nn { \pd_field:nn {#1} {2} }
      { {arab}{\bool_gset_true:N \g_pd_rtl_bool} {hebr}{\bool_gset_true:N \g_pd_rtl_bool} }
  }
\cs_new:Npn \pd@ifanycjk #1#2 { \bool_if:NTF \g_pd_cjk_bool {#1} {#2} }
\cs_new:Npn \pd@ifanyrtl #1#2 { \bool_if:NTF \g_pd_rtl_bool {#1} {#2} }
\cs_new:Npn \pd@firstcjk { \tl_use:N \g_pd_firstcjk_tl }
\cs_new:Npn \pd@mainlang { \tl_use:N \l_pd_lang_tl }

% babel handles every non-CJK language. CJK text is typeset by LuaTeX-ja
% (via ctex); with a CJK main language babel only hyphenates Latin words.
\tl_new:N \g_pd_babelmain_tl
\pd_if_cjk:nTF { \l_pd_lang_tl }
  { \tl_gset:Nn \g_pd_babelmain_tl { american } }
  { \tl_gset:Ne \g_pd_babelmain_tl { \pd_field:nn { \l_pd_lang_tl } {1} } }
\ExplSyntaxOff
\pd@ifanyrtl{\RequirePackage[bidi=basic]{babel}}{\RequirePackage{babel}}
\ExplSyntaxOn
% Build the \babelprovide calls here, run them with normal catcodes below.
\tl_new:N \g_pd_babelprovide_tl
\clist_map_inline:Nn \g_pd_langs_clist
  {
    \pd_if_cjk:nF {#1}
      {
        \tl_set:Ne \l_tmpa_tl { \pd_field:nn {#1} {1} }
        \tl_if_eq:NNF \l_tmpa_tl \g_pd_babelmain_tl
          { \tl_gput_right:Ne \g_pd_babelprovide_tl
              { \exp_not:N \babelprovide [import] { \l_tmpa_tl } } }
      }
  }
\tl_gput_right:Ne \g_pd_babelprovide_tl
  { \exp_not:N \babelprovide [import, main] { \g_pd_babelmain_tl } }
\cs_new:Npn \pd@babelprovides { \tl_use:N \g_pd_babelprovide_tl }
\ExplSyntaxOff
\pd@babelprovides

% ==================================================================
% Fonts: a fixed face per script and role (references/fonts.md).
% A missing face falls back down its chain and logs "plaindoc font
% fallback"; scripts/check.py reports it. No usable face is an error.
% ==================================================================
\RequirePackage{fontspec}
\newcommand\pd@pickfont[3]{% #1 result macro, #2 role, #3 candidates
  \let#1\relax\def\pd@first{}%
  \@for\pd@cand:=#3\do{%
    \ifx\pd@first\@empty\edef\pd@first{\pd@cand}\fi
    \ifx#1\relax\IfFontExistsTF{\pd@cand}{\edef#1{\pd@cand}}{}\fi}%
  \ifx#1\relax
    \ClassError{plaindoc}{No usable #2 font (tried: #3)}%
      {Install the fonts listed in references/fonts.md.}%
  \else\ifx#1\pd@first\else
    \ClassWarningNoLine{plaindoc}{plaindoc font fallback: #2 '\pd@first'
      not found, using '#1'}%
  \fi\fi}

\pd@pickfont\pd@serif{Latin serif}{STIX Two Text,TeX Gyre Termes,Latin Modern Roman}
\pd@pickfont\pd@sans{Latin sans}{IBMPlexSans,TeX Gyre Heros,Latin Modern Sans}
\pd@pickfont\pd@mono{Latin mono}{IBMPlexMono,Latin Modern Mono}
\pd@pickfont\pd@math{math}{STIX Two Math,Latin Modern Math}

% Glyphs a face lacks (STIX Two Text has no arrows, <= or >=) come from
% this chain rather than becoming empty boxes.
\def\pd@fallbacks{}
\@for\pd@cand:={STIX Two Math,IBMPlexSans,Noto Sans Symbols,Noto Sans Symbols 2,DejaVu Sans}\do{%
  \IfFontExistsTF{\pd@cand}{\edef\pd@fallbacks{\pd@fallbacks"\pd@cand:mode=node;",}}{}}
\directlua{luaotfload.add_fallback("pdsymbols", {\pd@fallbacks})}
\defaultfontfeatures{Ligatures=TeX}

\def\pd@stix{STIX Two Text}\def\pd@plex{IBMPlexSans}\def\pd@plexmono{IBMPlexMono}
\ifx\pd@serif\pd@stix
  \babelfont{rm}[RawFeature={fallback=pdsymbols}, BoldFont={STIX Two Text SemiBold},
    BoldItalicFont={STIX Two Text SemiBold Italic}]{STIX Two Text}
\else
  \edef\pd@tmp{\noexpand\babelfont{rm}[RawFeature={fallback=pdsymbols}]{\pd@serif}}\pd@tmp
\fi
\ifx\pd@sans\pd@plex
  \babelfont{sf}[RawFeature={fallback=pdsymbols}, ItalicFont=IBMPlexSans-Italic, BoldFont=IBMPlexSans-SemiBold,
    BoldItalicFont=IBMPlexSans-SemiBoldItalic]{IBMPlexSans}
\else
  \edef\pd@tmp{\noexpand\babelfont{sf}[RawFeature={fallback=pdsymbols}]{\pd@sans}}\pd@tmp
\fi
\ifx\pd@mono\pd@plexmono
  \babelfont{tt}[RawFeature={fallback=pdsymbols}, Scale=MatchLowercase, ItalicFont=IBMPlexMono-Italic,
    BoldFont=IBMPlexMono-SemiBold]{IBMPlexMono}
\else
  \edef\pd@tmp{\noexpand\babelfont{tt}[RawFeature={fallback=pdsymbols}, Scale=MatchLowercase]{\pd@mono}}\pd@tmp
\fi
\pd@ifsansbody{\renewcommand\familydefault{\sfdefault}}{}

% Complex scripts: serif and sans pairs, shaped by HarfBuzz. These faces
% have no Latin letters or digits, so Latin text inside them (model names,
% units, numbers) falls back to the Latin face of the same style.
\ifx\pd@serif\pd@stix\def\pd@serifbold{STIX Two Text SemiBold}\else\let\pd@serifbold\pd@serif\fi
\ifx\pd@sans\pd@plex\def\pd@sansbold{IBMPlexSans-SemiBold}\else\let\pd@sansbold\pd@sans\fi
\directlua{
  local m = "\luaescapestring{\pd@math}"
  local function chain(face) return { face .. ":mode=harf;", m .. ":mode=harf;" } end
  luaotfload.add_fallback("pdrm",  chain("\luaescapestring{\pd@serif}"))
  luaotfload.add_fallback("pdrmb", chain("\luaescapestring{\pd@serifbold}"))
  luaotfload.add_fallback("pdsf",  chain("\luaescapestring{\pd@sans}"))
  luaotfload.add_fallback("pdsfb", chain("\luaescapestring{\pd@sansbold}"))
}
\newcommand\pd@scriptfonts[3]{% #1 babel name, #2 serif list, #3 sans list
  \pd@pickfont\pd@tmpa{#1 serif}{#2}\pd@pickfont\pd@tmpb{#1 sans}{#3}%
  \edef\pd@tmp{%
    \noexpand\babelfont[#1]{rm}[Renderer=HarfBuzz, RawFeature={fallback=pdrm},
      BoldFeatures={RawFeature={fallback=pdrmb}}]{\pd@tmpa}%
    \noexpand\babelfont[#1]{sf}[Renderer=HarfBuzz, RawFeature={fallback=pdsf},
      BoldFeatures={RawFeature={fallback=pdsfb}}]{\pd@tmpb}}\pd@tmp}
\ExplSyntaxOn
\clist_map_inline:Nn \g_pd_langs_clist
  {
    \tl_set:Ne \l_tmpa_tl { \pd_field:nn {#1} {1} }
    \str_case_e:nn { \pd_field:nn {#1} {2} }
      {
        {arab}{ \exp_args:NV \pd@scriptfonts \l_tmpa_tl
                {Noto~Naskh~Arabic,Noto~Sans~Arabic} {IBM~Plex~Sans~Arabic,Noto~Sans~Arabic} }
        {hebr}{ \exp_args:NV \pd@scriptfonts \l_tmpa_tl
                {Noto~Serif~Hebrew,Noto~Sans~Hebrew} {IBM~Plex~Sans~Hebrew,Noto~Sans~Hebrew} }
        {deva}{ \exp_args:NV \pd@scriptfonts \l_tmpa_tl
                {Noto~Serif~Devanagari,Noto~Sans~Devanagari} {IBM~Plex~Sans~Devanagari,Noto~Sans~Devanagari} }
        {grek}{ \pd@pickfont\pd@tmpa{Greek~serif}{Noto~Serif,GFS~Didot,STIX~Two~Text}
                \use:e { \exp_not:N \babelfont [ \l_tmpa_tl ] {rm}
                  [RawFeature={fallback=pdsymbols}] { \pd@tmpa } } }
        {thai}{ \exp_args:NV \pd@scriptfonts \l_tmpa_tl
                {Noto~Serif~Thai,Noto~Sans~Thai} {IBM~Plex~Sans~Thai~Looped,Noto~Sans~Thai} }
      }
  }
\ExplSyntaxOff

\RequirePackage[warnings-off={mathtools-colon,mathtools-overbracket}]{unicode-math}
\edef\pd@tmp{\noexpand\setmathfont{\pd@math}}\pd@tmp

% CJK: ctex on LuaTeX-ja. One rm/sf/tt family per region; \begin{lang}
% and \pdlang switch region. Curly quotes, dashes and the ellipsis keep
% Western metrics everywhere, so —— and …… stay continuous.
\newcommand\pd@cjkregion[5]{% #1 key, #2 JFM, #3 serif list, #4 sans list, #5 mono list
  \pd@pickfont\pd@tmpa{#1 CJK serif}{#3}%
  \pd@pickfont\pd@tmpb{#1 CJK sans}{#4}%
  \pd@pickfont\pd@tmpc{#1 CJK mono}{#5}%
  \edef\pd@tmp{%
    \noexpand\setCJKfamilyfont{#1-rm}[JFM=#2, BoldFont={\pd@tmpa\space Bold},
      ItalicFont={\pd@tmpa}, BoldItalicFont={\pd@tmpa\space Bold}]{\pd@tmpa}%
    \noexpand\setCJKfamilyfont{#1-sf}[JFM=#2, BoldFont={\pd@tmpb\space Bold},
      ItalicFont={\pd@tmpb}, BoldItalicFont={\pd@tmpb\space Bold}]{\pd@tmpb}%
    \noexpand\setCJKfamilyfont{#1-tt}[JFM=#2]{\pd@tmpc}}\pd@tmp}
\pd@ifanycjk{%
  \RequirePackage[scheme=plain, punct=quanjiao]{ctex}%
  \pd@cjkregion{zh-HK}{zh_TW/quanjiao}{Noto Serif CJK HK,Source Han Serif HC,Noto Serif CJK TC}%
    {Noto Sans CJK HK,Source Han Sans HC}{Noto Sans Mono CJK HK,Noto Sans CJK HK}%
  \pd@cjkregion{zh-TW}{zh_TW/quanjiao}{Noto Serif CJK TC,Source Han Serif TC}%
    {Noto Sans CJK TC,Source Han Sans TC}{Noto Sans Mono CJK TC,Noto Sans CJK TC}%
  \pd@cjkregion{zh-CN}{zh_CN/quanjiao}{Noto Serif CJK SC,Source Han Serif SC}%
    {Noto Sans CJK SC,Source Han Sans SC}{Noto Sans Mono CJK SC,Noto Sans CJK SC}%
  \pd@cjkregion{ja}{ja_JP/quanjiao}{Noto Serif CJK JP,Source Han Serif JP}%
    {Noto Sans CJK JP,Source Han Sans JP}{Noto Sans Mono CJK JP,Noto Sans CJK JP}%
  \pd@cjkregion{ko}{zh_CN/banjiao}{Noto Serif CJK KR,Source Han Serif K}%
    {Noto Sans CJK KR,Source Han Sans K}{Noto Sans Mono CJK KR,Noto Sans CJK KR}%
  \newcommand\pd@usecjk[1]{%
    \renewcommand\CJKrmdefault{#1-rm}\renewcommand\CJKsfdefault{#1-sf}%
    \renewcommand\CJKttdefault{#1-tt}%
    \ifx\f@family\sfdefault\CJKfamily{#1-sf}\else
      \ifx\f@family\ttdefault\CJKfamily{#1-tt}\else\CJKfamily{#1-rm}\fi\fi}%
  \AtBeginDocument{\pd@usecjk{\pd@firstcjk}}%
  \ltjsetparameter{jacharrange={-9}}% ‘ ’ “ ” – — … keep Western metrics
}{}

% ==================================================================
% Microtypography, links, units, quotes
% ==================================================================
\RequirePackage[final, protrusion=true, expansion=true, tracking=true,
  letterspace=60]{microtype}
\RequirePackage{ragged2e}
\RequirePackage[autostyle=true]{csquotes}
\DeclareQuoteStyle{vietnamese}{\textquotedblleft}{\textquotedblright}{\textquoteleft}{\textquoteright}
\DeclareQuoteStyle{indonesian}{\textquotedblleft}{\textquotedblright}{\textquoteleft}{\textquoteright}
\DeclareQuoteStyle{hindi}{\textquotedblleft}{\textquotedblright}{\textquoteleft}{\textquoteright}
\DeclareQuoteStyle{thai}{\textquotedblleft}{\textquotedblright}{\textquoteleft}{\textquoteright}
\DeclareQuoteStyle{arabic}{«}{»}{“}{”}
\DeclareQuoteStyle{hebrew}{„}{”}{‚}{’}
\DeclareQuoteAlias[quotes]{turkish}{turkish}
\RequirePackage{siunitx}
\sisetup{per-mode=symbol, range-phrase={\,–\,}, range-units=single,
  product-units=single, list-units=single, uncertainty-mode=separate,
  mode=text, reset-text-family=false, reset-text-series=false}
\RequirePackage{enumitem}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{xltabular}
\RequirePackage{multicol}
\RequirePackage{fancyvrb}
\RequirePackage{caption}
\RequirePackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\RequirePackage[most]{tcolorbox}

% ==================================================================
% Language switching: \begin{lang}{fr} ... \end{lang}, \pdlang{fr}{...}
% Sets babel language (direction, hyphenation, quotes), CJK region,
% decimal marker and line spacing.
% ==================================================================
\newcommand\pd@langsetup[1]{%
  \frenchspacing % one word space after a full stop, in every language
  \protected@edef\pd@curlang{#1}%
  \protected@edef\pd@tmp{\noexpand\sisetup{output-decimal-marker={\pd@field{#1}{3}},
    group-separator={\pd@field{#1}{4}}}}\pd@tmp
  \pd@ifcjk{#1}{%
    \pd@usecjk{#1}%
    \linespread{1.12}\selectfont}{}}
\NewDocumentEnvironment{lang}{m}{%
  \pd@ifcjk{#1}{\pd@langsetup{#1}}%
    {\edef\pd@tmp{\noexpand\otherlanguage{\pd@field{#1}{1}}}\pd@tmp\pd@langsetup{#1}}}%
  {\pd@ifcjk{\pd@curlang}{}{\endotherlanguage}}
\NewDocumentCommand\pdlang{m+m}{%
  \pd@ifcjk{#1}{{\pd@langsetup{#1}#2}}%
    {\edef\pd@tmp{\noexpand\foreignlanguage{\pd@field{#1}{1}}}%
     \pd@tmp{\pd@langsetup{#1}#2}}}
\AtBeginDocument{\pd@langsetup{\pd@mainlang}}
% Quantities stay left-to-right inside Arabic and Hebrew text.
\pd@ifanyrtl{%
  \AtBeginDocument{%
    \NewCommandCopy\pd@siqty\qty
    \RenewDocumentCommand\qty{O{}mm}{\babelsublr{\pd@siqty[#1]{#2}{#3}}}}}{}

% Quotation marks for CJK (csquotes covers babel languages).
\newcommand\pd@cjkquote[1]{%
  \pd@ifcjk{\pd@curlang}{%
    \edef\pd@s{\pd@field{\pd@curlang}{2}}%
    \def\pd@cn{hani-cn}\def\pd@ko{kore}%
    \ifx\pd@s\pd@cn “#1”\else\ifx\pd@s\pd@ko “#1”\else 「#1」\fi\fi}%
  {\enquote{#1}}}
\let\pdq\pd@cjkquote

% ==================================================================
% Localised labels (class-owned strings). Override: \pdsetstring{tag}{key}{text}
% ==================================================================
\ExplSyntaxOn
\prop_new:N \g_pd_str_prop
\cs_new_protected:Npn \pd_str:nnnnnnnn #1#2#3#4#5#6#7#8
  { % tag: note danger warning caution notice figure table contents
    \prop_gput:Nnn \g_pd_str_prop {#1/note}{#2}
    \prop_gput:Nnn \g_pd_str_prop {#1/danger}{#3}
    \prop_gput:Nnn \g_pd_str_prop {#1/warning}{#4}
    \prop_gput:Nnn \g_pd_str_prop {#1/caution}{#5}
    \prop_gput:Nnn \g_pd_str_prop {#1/notice}{#6}
    \prop_gput:Nnn \g_pd_str_prop {#1/figure}{#7}
    \prop_gput:Nnn \g_pd_str_prop {#1/table}{#8}
  }
\pd_str:nnnnnnnn {en-US}{Note}{DANGER}{WARNING}{CAUTION}{NOTICE}{Figure}{Table}
\pd_str:nnnnnnnn {en-GB}{Note}{DANGER}{WARNING}{CAUTION}{NOTICE}{Figure}{Table}
\pd_str:nnnnnnnn {fr}{Remarque}{DANGER}{AVERTISSEMENT}{ATTENTION}{AVIS}{Figure}{Tableau}
\pd_str:nnnnnnnn {de}{Hinweis}{GEFAHR}{WARNUNG}{VORSICHT}{HINWEIS}{Abbildung}{Tabelle}
\pd_str:nnnnnnnn {es}{Nota}{PELIGRO}{ADVERTENCIA}{PRECAUCIÓN}{AVISO}{Figura}{Tabla}
\pd_str:nnnnnnnn {it}{Nota}{PERICOLO}{AVVERTENZA}{ATTENZIONE}{AVVISO}{Figura}{Tabella}
\pd_str:nnnnnnnn {pt-BR}{Observação}{PERIGO}{ADVERTÊNCIA}{CUIDADO}{AVISO}{Figura}{Tabela}
\pd_str:nnnnnnnn {nl}{Opmerking}{GEVAAR}{WAARSCHUWING}{VOORZICHTIG}{LET~OP}{Afbeelding}{Tabel}
\pd_str:nnnnnnnn {pl}{Uwaga}{NIEBEZPIECZEŃSTWO}{OSTRZEŻENIE}{PRZESTROGA}{NOTYFIKACJA}{Rysunek}{Tabela}
\pd_str:nnnnnnnn {tr}{Not}{TEHLİKE}{UYARI}{DİKKAT}{BİLGİ}{Şekil}{Tablo}
\pd_str:nnnnnnnn {vi}{Lưu~ý}{NGUY~HIỂM}{CẢNH~BÁO}{THẬN~TRỌNG}{THÔNG~BÁO}{Hình}{Bảng}
\pd_str:nnnnnnnn {id}{Catatan}{BAHAYA}{PERINGATAN}{HATI-HATI}{PEMBERITAHUAN}{Gambar}{Tabel}
\pd_str:nnnnnnnn {ru}{Примечание}{ОПАСНО}{ПРЕДУПРЕЖДЕНИЕ}{ОСТОРОЖНО}{ВНИМАНИЕ}{Рисунок}{Таблица}
\pd_str:nnnnnnnn {uk}{Примітка}{НЕБЕЗПЕКА}{ПОПЕРЕДЖЕННЯ}{ОБЕРЕЖНО}{УВАГА}{Рисунок}{Таблиця}
\pd_str:nnnnnnnn {el}{Σημείωση}{ΚΙΝΔΥΝΟΣ}{ΠΡΟΕΙΔΟΠΟΙΗΣΗ}{ΠΡΟΣΟΧΗ}{ΕΙΔΟΠΟΙΗΣΗ}{Σχήμα}{Πίνακας}
\pd_str:nnnnnnnn {ar}{ملاحظة}{خطر}{تحذير}{تنبيه}{إشعار}{شكل}{جدول}
\pd_str:nnnnnnnn {he}{הערה}{סכנה}{אזהרה}{זהירות}{הודעה}{איור}{טבלה}
\pd_str:nnnnnnnn {hi}{नोट}{खतरा}{चेतावनी}{सावधानी}{सूचना}{चित्र}{तालिका}
\pd_str:nnnnnnnn {th}{หมายเหตุ}{อันตราย}{คำเตือน}{ข้อควรระวัง}{ประกาศ}{รูป}{ตาราง}
\pd_str:nnnnnnnn {zh-HK}{注意}{危險}{警告}{小心}{須知}{圖}{表}
\pd_str:nnnnnnnn {zh-TW}{注意}{危險}{警告}{小心}{須知}{圖}{表}
\pd_str:nnnnnnnn {zh-CN}{注意}{危险}{警告}{小心}{须知}{图}{表}
\pd_str:nnnnnnnn {ja}{注記}{危険}{警告}{注意}{通知}{図}{表}
\pd_str:nnnnnnnn {ko}{참고}{위험}{경고}{주의}{알림}{그림}{표}
\msg_new:nnn { plaindoc } { no-string }
  { No~'#2'~label~for~language~'#1';~using~English.~Set~one~with~\pdsetstring{#1}{#2}{...}. }
\cs_new:Npn \pd@str #1 { \exp_args:Ne \pd__str:n { \pd@curlang / #1 } }
\cs_new:Npn \pd__str:n #1
  {
    \prop_if_in:NnTF \g_pd_str_prop {#1}
      { \prop_item:Nn \g_pd_str_prop {#1} }
      { \pd__str_key:w #1 \q_stop }
  }
\cs_new:Npn \pd__str_key:w #1 / #2 \q_stop { \prop_item:Nn \g_pd_str_prop { en-US / #2 } }
\NewDocumentCommand \pdsetstring { m m m }
  { \prop_gput:Nnn \g_pd_str_prop {#1/#2} {#3} }
\clist_map_inline:Nn \g_pd_langs_clist
  { \prop_if_in:NnF \g_pd_str_prop { #1/warning }
      { \msg_warning:nnnn { plaindoc } { no-string } {#1} { warning } } }
\ExplSyntaxOff
\def\pd@curlang{en-US}
% CJK main language: localise the kernel names babel would otherwise set.
\AtBeginDocument{\pd@ifcjk{\pd@mainlang}{%
  \renewcommand\figurename{\pd@str{figure}}\renewcommand\tablename{\pd@str{table}}%
  \edef\pd@s{\pd@field{\pd@mainlang}{2}}\def\pd@cn{hani-cn}\def\pd@ja{jpan}\def\pd@ko{kore}%
  \ifx\pd@s\pd@cn\renewcommand\contentsname{目录}\else
  \ifx\pd@s\pd@ja\renewcommand\contentsname{目次}\else
  \ifx\pd@s\pd@ko\renewcommand\contentsname{목차}\else
  \renewcommand\contentsname{目錄}\fi\fi\fi}{}}

% ==================================================================
% Document metadata: \pdset{title=..., ...}
% ==================================================================
\ExplSyntaxOn
\keys_define:nn { plaindoc/meta }
  {
    title     .tl_gset:N = \g_pd_title_tl,
    subtitle  .tl_gset:N = \g_pd_subtitle_tl,
    brand     .tl_gset:N = \g_pd_brand_tl,
    product   .tl_gset:N = \g_pd_product_tl,
    doctype   .tl_gset:N = \g_pd_doctype_tl,
    docid     .tl_gset:N = \g_pd_docid_tl,
    version   .tl_gset:N = \g_pd_version_tl,
    date      .tl_gset:N = \g_pd_date_tl,
    author    .tl_gset:N = \g_pd_author_tl,
    org       .tl_gset:N = \g_pd_org_tl,
    to        .tl_gset:N = \g_pd_to_tl,
    from      .tl_gset:N = \g_pd_from_tl,
    cc        .tl_gset:N = \g_pd_cc_tl,
    status    .tl_gset:N = \g_pd_status_tl,
  }
\NewDocumentCommand \pdset { m } { \keys_set:nn { plaindoc/meta } {#1} }
\NewExpandableDocumentCommand \pdmeta { m } { \tl_use:c { g_pd_#1_tl } }
\NewDocumentCommand \pdifmeta { m +m +m } { \tl_if_empty:cTF { g_pd_#1_tl } {#3} {#2} }
\ExplSyntaxOff

% ==================================================================
% Type: sizes and fonts for each element
% ==================================================================
\newcommand\pd@sffont{\normalfont\sffamily}
\newcommand\pd@headfont{\pd@sffont\bfseries\color{pd-ink}}
\newcommand\pd@numfont{\pd@sffont\color{pd-ink2}}
\newcommand\pd@labelfont{\pd@sffont\bfseries\small\color{pd-ink}}
\newcommand\pd@metafont{\pd@sffont\footnotesize\color{pd-ink2}}
\pd@iftype{manual}{\linespread{1.18}}{\linespread{1.12}}

\setkomafont{disposition}{\pd@headfont}
\setkomafont{pageheadfoot}{\pd@metafont}
\setkomafont{pagenumber}{\pd@sffont\footnotesize\bfseries\color{pd-ink}}
\setkomafont{footnote}{\normalfont\footnotesize}
\setkomafont{descriptionlabel}{\pd@sffont\bfseries}
\deffootnote{1.5em}{0em}{\makebox[1.5em][l]{\thefootnotemark}}

% Section numbers hang left of the text column, so heading text aligns
% with body text and numbers form a scannable column.
\renewcommand*{\sectionformat}{\makebox[0pt][r]{\pd@numfont\thesection\hspace{\pd@numgap}}}
\renewcommand*{\subsectionformat}{\makebox[0pt][r]{\pd@numfont\thesubsection\hspace{\pd@numgap}}}
\renewcommand*{\subsubsectionformat}{\makebox[0pt][r]{\pd@numfont\thesubsubsection\hspace{\pd@numgap}}}
\pd@iftype{memo}{%
  \RedeclareSectionCommand[beforeskip=-1.3\baselineskip, afterskip=.3\baselineskip,
    font=\pd@headfont\normalsize]{section}%
}{%
  \RedeclareSectionCommand[beforeskip=-2.1\baselineskip, afterskip=.55\baselineskip,
    font=\pd@headfont\fontsize{14}{18}\selectfont]{section}%
}
\RedeclareSectionCommand[beforeskip=-1.5\baselineskip, afterskip=.35\baselineskip,
  font=\pd@headfont\normalsize]{subsection}
\RedeclareSectionCommand[beforeskip=-1.1\baselineskip, afterskip=.2\baselineskip,
  font=\pd@headfont\normalsize]{subsubsection}
\RedeclareSectionCommand[beforeskip=.8\baselineskip, afterskip=-1em,
  font=\pd@headfont\normalsize]{paragraph}
\setcounter{secnumdepth}{\subsectionnumdepth}
\setcounter{tocdepth}{\subsectionnumdepth}

% Chapter (manual, report with chapters): number in the index column,
% title on the body column, new page.
\pd@ifchapters{%
  \RedeclareSectionCommand[beforeskip=0pt, afterskip=2.4\baselineskip,
    font=\pd@headfont\fontsize{26}{31}\selectfont]{chapter}
  \renewcommand*{\chapterformat}{%
    \makebox[0pt][r]{\pd@sffont\fontsize{26}{31}\selectfont\color{pd-accent}\thechapter
      \hspace{\pd@numgap}}}
  \renewcommand*{\chapterlinesformat}[3]{\@hangfrom{#2}{#3}}
  \renewcommand*{\chapterlineswithprefixformat}[3]{#2#3}
  \renewcommand*{\raggedchapter}{\raggedright}
}{}
\renewcommand*{\raggedsection}{\raggedright}

% Bibliographies are set ragged right: long identifiers stay whole.
\AddToHook{begindocument/before}{\@ifpackageloaded{biblatex}{%
  \appto\bibsetup{\RaggedRight}\setlength\bibitemsep{.3\baselineskip}}{}}

% Body alignment: manuals and memos ragged right; reports justified.
\pd@iftype{report}{}{\AtBeginDocument{\RaggedRight\hyphenpenalty=10000 }}
\setlength\RaggedRightParindent{0pt}

% ==================================================================
% Running heads and folios (scrlayer-scrpage)
% ==================================================================
\RequirePackage{scrlayer-scrpage}
\edef\pd@tmp{\noexpand\KOMAoptions{headwidth=\the\pd@full:-\the\pd@hang,
  footwidth=\the\pd@full:-\the\pd@hang}}\pd@tmp
\clearpairofpagestyles
\pd@ifchapters{\automark[chapter]{chapter}}{\automark[section]{section}}
\newcommand\pd@headleft{%
  \pdifmeta{product}{\pdmeta{product}\pdifmeta{doctype}{\enspace·\enspace\pdmeta{doctype}}{}}%
    {\pdmeta{title}}}
\newcommand\pd@footleft{%
  \pdifmeta{docid}{\pdmeta{docid}}{}%
  \pdifmeta{version}{\pdifmeta{docid}{\enspace·\enspace}{}\pdmeta{version}}{}}
\pd@iftype{memo}{%
  \ofoot*{\pagemark}%
}{%
  \ihead{\pd@headleft}\ohead{\rightmark}%
  \ifoot*{\pd@footleft}\ofoot*{\pagemark}%
}
\pagestyle{scrheadings}
\pd@ifchapters{\renewcommand*{\chapterpagestyle}{scrheadings}}{}

% ==================================================================
% Lists, steps, results, notes
% ==================================================================
\setlist{topsep=.25\baselineskip, partopsep=0pt, itemsep=.2\baselineskip, parsep=0pt}
\setlist[itemize]{leftmargin=1.1em, label=\textbullet}
\setlist[itemize,2]{label=–}
\setlist[enumerate]{leftmargin=1.6em, label=\arabic*.}
\setlist[enumerate,2]{label=\alph*.}
\setlist[description]{leftmargin=0pt, labelindent=0pt, style=nextline}

% Procedures: step numbers hang in the index column.
\newlist{steps}{enumerate}{2}
\setlist[steps,1]{label={\pd@sffont\bfseries\arabic*}, align=right, leftmargin=0pt,
  labelwidth=10mm, labelsep=\pd@numgap, itemsep=.55\baselineskip,
  topsep=.4\baselineskip}
\setlist[steps,2]{label={\pd@sffont\alph*}, align=left, leftmargin=1.4em,
  labelsep=.5em, itemsep=.15\baselineskip}
% Result of a step. The arrow is language neutral.
\newcommand\result[1]{\par\pd@resultbody{#1}}
\newcommand\pd@resultbody[1]{\hangindent=1.3em\hangafter=1\noindent
  \makebox[1.3em][l]{\textcolor{pd-ink2}{→}}#1\par}

% Note: label in the index column, text in the body column.
\NewDocumentEnvironment{note}{o}{%
  \par\addvspace{.3\baselineskip}\noindent
  \makebox[0pt][r]{\pd@labelfont\IfValueTF{#1}{#1}{\pd@str{note}}\hspace{\pd@numgap}}%
  \ignorespaces}{\par\addvspace{.3\baselineskip}}
\newcommand\pdlabel[1]{\par\noindent\makebox[0pt][r]{\pd@labelfont#1\hspace{\pd@numgap}}\ignorespaces}

% ==================================================================
% Safety messages (ANSI Z535.6 / ISO 3864-2 structure):
% signal word panel + message panel. Levels: danger, warning, caution,
% notice. Write: hazard, consequence, how to avoid it.
% ==================================================================
\newcommand\pd@alertsymbol[2]{% #1 triangle colour, #2 mark colour
  \tikz[x=1em, y=1em, baseline=-.02em]{%
    \fill[#1, line join=round, draw=#1, line width=.06em] (0,0) -- (1.12,0) -- (.56,.98) -- cycle;
    \fill[#2] (.505,.34) -- (.615,.34) -- (.645,.80) -- (.475,.80) -- cycle;
    \fill[#2] (.56,.17) circle (.075);}}
\newcommand\pd@safety@danger{\def\pd@sbg{pd-danger}\def\pd@sfg{white}\def\pd@ssym{\pd@alertsymbol{white}{pd-danger}\enspace}}
\newcommand\pd@safety@warning{\def\pd@sbg{pd-warning}\def\pd@sfg{black}\def\pd@ssym{\pd@alertsymbol{black}{pd-warning}\enspace}}
\newcommand\pd@safety@caution{\def\pd@sbg{pd-caution}\def\pd@sfg{black}\def\pd@ssym{\pd@alertsymbol{black}{pd-caution}\enspace}}
\newcommand\pd@safety@notice{\def\pd@sbg{pd-notice}\def\pd@sfg{white}\def\pd@ssym{}}
\NewDocumentEnvironment{safety}{m o}{%
  \ifcsname pd@safety@#1\endcsname\csname pd@safety@#1\endcsname\else
    \ClassError{plaindoc}{Unknown safety level '#1'}{Use danger, warning, caution or notice.}\fi
  \def\pd@slevel{#1}\def\pd@notice{notice}%
  \begin{tcolorbox}[enhanced, breakable=false, arc=0pt, outer arc=0pt,
      boxrule=.7pt, titlerule=0pt, colframe=black, colback=white,
      colbacktitle=\pd@sbg, coltitle=\pd@sfg,
      left=3mm, right=3mm, top=2.2mm, bottom=2.4mm,
      lefttitle=3mm, toptitle=1mm, bottomtitle=1mm,
      before skip=.9\baselineskip, after skip=.9\baselineskip,
      fonttitle=\pd@sffont\bfseries\normalsize,
      fontupper=\normalfont\pd@ifsansbody{}{\sffamily},
      title={\pd@ssym\ifx\pd@slevel\pd@notice\itshape\fi\textls[60]{\pd@str{#1}}}]
  \IfValueT{#2}{{\bfseries #2}\par}}%
  {\end{tcolorbox}}

% ==================================================================
% Interface vocabulary
% ==================================================================
\newcommand\ui[1]{{\bfseries #1}}                     % on-screen label
\newcommand\key[1]{\tikz[baseline=(k.base)]\node[draw=pd-ink, line width=.45pt,
  rounded corners=1.2pt, inner xsep=.28em, inner ysep=.16em, minimum height=1.25em,
  font=\pd@sffont\footnotesize\bfseries](k){\strut #1};}% physical key
\newcommand\menu[1]{{\bfseries\pd@menu#1>\relax}}      % \menu{File>Export}
\def\pd@menu#1>#2\relax{#1\if\relax\detokenize{#2}\relax\else\,\textcolor{pd-ink2}{›}\,\pd@menu#2\relax\fi}
\newcommand\cmd[1]{\texttt{#1}}
\DefineVerbatimEnvironment{code}{Verbatim}{fontsize=\small, frame=leftline,
  framerule=.8pt, rulecolor=\color{pd-rule}, xleftmargin=0pt, framesep=3mm,
  baselinestretch=1.1}

% ==================================================================
% Figures, captions, tables
% ==================================================================
% Wide content spans the index column too (manual); full width elsewhere.
\newcommand\pdwide[1]{\par\noindent\makebox[\linewidth][r]{%
  \begin{minipage}[t]{\dimexpr\linewidth+\pd@hang\relax}#1\end{minipage}}\par}
\DeclareCaptionFormat{pdhang}{\makebox[0pt][r]{#1\hspace{\pd@numgap}}#3\par}
\DeclareCaptionLabelSeparator{pdnone}{}
\captionsetup{format=pdhang, labelsep=pdnone, singlelinecheck=false,
  justification=raggedright, labelfont={sf,bf}, font={sf,small}, skip=7pt}
\captionsetup[table]{position=top, skip=6pt}
\def\fps@figure{htbp}\def\fps@table{htbp}
\renewcommand\topfraction{.85}\renewcommand\bottomfraction{.6}
\renewcommand\textfraction{.12}\renewcommand\floatpagefraction{.75}

% Tables: booktabs rules, no vertical rules, no fills.
\setlength\heavyrulewidth{.8pt}\setlength\lightrulewidth{.4pt}
\setlength\cmidrulewidth{.4pt}
\setlength\aboverulesep{.5ex}\setlength\belowrulesep{.6ex}
% L: a tabularx column set ragged right (justified narrow cells leave holes).
\newcolumntype{L}{>{\RaggedRight\arraybackslash}X}
\newcolumntype{P}[1]{>{\RaggedRight\arraybackslash}p{#1}}
\newcommand\hd[1]{{\pd@sffont\bfseries\footnotesize #1}}
\NewExpandableDocumentCommand\pdgroup{O{2}m}{\multicolumn{#1}{@{}l}{\pd@sffont\bfseries\footnotesize #2}\\[1pt]}
\AtBeginEnvironment{tabular}{\small}
\AtBeginEnvironment{tabular*}{\small}
\AtBeginEnvironment{tabularx}{\small}
\AtBeginEnvironment{xltabular}{\small}

% ==================================================================
% Technical drawings: TikZ styles and callouts
%   \begin{tikzpicture}[pd/drawing] ... \pdcallout{1}{(x,y)}{(mx,my)}
% ==================================================================
\tikzset{
  pd/drawing/.style={line cap=round, line join=round, font=\pd@sffont\scriptsize},
  pd/part/.style={draw=pd-ink, line width=.75pt, fill=white},
  pd/detail/.style={draw=pd-ink, line width=.4pt},
  pd/hidden/.style={draw=pd-ink2, line width=.4pt, dash pattern=on 2pt off 1.5pt},
  pd/surface/.style={fill=pd-surface},
  pd/label/.style={font=\pd@sffont\scriptsize\bfseries, text=pd-ink},
  pd/marker/.style={circle, fill=pd-accent, text=white, inner sep=0pt,
    minimum size=4.3mm, font=\pd@sffont\fontsize{7.5}{7.5}\selectfont\bfseries},
  pd/leader/.style={draw=pd-accent, line width=.55pt},
  pd/dim/.style={draw=pd-ink2, line width=.35pt, <->, >={Stealth[length=3pt]}},
}
\newcommand\pdcallout[3]{% {n}{target}{marker position}
  \draw[pd/leader] #2 -- #3;
  \fill[pd-accent] #2 circle (.75pt);
  \node[pd/marker] at #3 {#1};}
\newcommand\pdmarker[1]{\tikz[baseline=(m.base)]\node[pd/marker](m){#1};}
% Two-column legend matching the callout numbers.
\NewDocumentEnvironment{pdlegend}{O{2}}{%
  \par\addvspace{.4\baselineskip}\setlength\columnsep{8mm}%
  \begin{multicols}{#1}\raggedcolumns
  \begin{list}{}{\setlength\leftmargin{7mm}\setlength\labelwidth{5mm}%
    \setlength\labelsep{2mm}\setlength\itemsep{.45\baselineskip}%
    \setlength\topsep{0pt}\setlength\parsep{0pt}}}%
  {\end{list}\end{multicols}\par}
\newcommand\legenditem[3]{\item[\pdmarker{#1}]{\bfseries #2}\par #3}

% Charts: Okabe–Ito colours plus marks and dash patterns, so series stay
% distinguishable in greyscale and for colour-vision deficiency.
\pgfplotscreateplotcyclelist{pd}{%
  {oi-blue, mark=*, mark size=1.4pt, line width=1pt},
  {oi-vermilion, mark=square*, mark size=1.3pt, line width=1pt, dashed},
  {oi-green, mark=triangle*, mark size=1.7pt, line width=1pt, dotted},
  {oi-orange, mark=diamond*, mark size=1.7pt, line width=1pt, dashdotted},
  {oi-purple, mark=pentagon*, mark size=1.6pt, line width=1pt},
  {oi-skyblue, mark=o, mark size=1.5pt, line width=1pt, dashed}}
\pgfplotsset{
  pd/axis/.style={
    cycle list name=pd, axis lines=left, axis line style={pd-ink, line width=.5pt},
    tick style={pd-ink, line width=.4pt}, major tick length=2.5pt,
    grid=major, major grid style={pd-rule, line width=.3pt},
    ymajorgrids=true, xmajorgrids=false,
    tick label style={font=\pd@sffont\scriptsize},
    /pgf/number format/assume math mode=true,   % tick numbers in the text face
    xticklabel={\pgfmathprintnumber{\tick}}, yticklabel={\pgfmathprintnumber{\tick}},
    label style={font=\pd@sffont\scriptsize},
    legend style={font=\pd@sffont\scriptsize, draw=none, fill=none,
      legend cell align=left},
    every axis plot/.append style={line join=round},
  }}

% ==================================================================
% Title blocks
% ==================================================================
\newcommand\pd@coverfigure{}
\newcommand\pdcover[1]{\renewcommand\pd@coverfigure{#1}}
\renewcommand\maketitle{\pd@iftype{manual}{\pd@title@manual}%
  {\pd@iftype{memo}{\pd@title@memo}{\pd@title@report}}}

\newcommand\pd@title@manual{%
  \begin{titlepage}\pdfbookmark[0]{\pdmeta{title}}{title}%
  \newgeometry{left=\pd@outer, right=\pd@outer, top=24mm, bottom=24mm}%
  \pd@sffont\color{pd-ink}\RaggedRight
  \pdifmeta{brand}{{\bfseries\small\textls[80]{\MakeUppercase{\pdmeta{brand}}}}\par\vspace*{18mm}}{\vspace*{22mm}}%
  {\fontsize{30}{35}\selectfont\bfseries\pdmeta{title}\par}%
  \pdifmeta{subtitle}{\vspace{3mm}{\fontsize{30}{35}\selectfont\color{pd-ink2}\pdmeta{subtitle}\par}}{}%
  \vfill
  {\pd@coverfigure\par}%
  \vfill
  {\small\pdifmeta{docid}{\pdmeta{docid}\hspace{10mm}}{}%
   \pdifmeta{version}{\pdmeta{version}\hspace{10mm}}{}%
   \pdifmeta{date}{\pdmeta{date}}{}\par}
  \pdifmeta{org}{\vspace{6mm}{\pd@metafont\pdmeta{org}}\par}{}%
  \restoregeometry
  \end{titlepage}\setcounter{page}{2}}

\newcommand\pd@title@report{%
  \begingroup\pd@sffont\RaggedRight
  \pdifmeta{org}{{\pd@sffont\footnotesize\bfseries\color{pd-ink2}\pdmeta{org}}\par\vspace{5mm}}{}%
  {\fontsize{22}{27}\selectfont\bfseries\color{pd-ink}\pdmeta{title}\par}%
  \pdifmeta{subtitle}{\vspace{2mm}{\fontsize{13}{17}\selectfont\color{pd-ink2}\pdmeta{subtitle}\par}}{}%
  \vspace{6mm}%
  {\pd@metafont
    \pdifmeta{author}{\pdmeta{author}}{}%
    \pdifmeta{date}{\pdifmeta{author}{\enspace·\enspace}{}\pdmeta{date}}{}%
    \pdifmeta{docid}{\enspace·\enspace\pdmeta{docid}}{}%
    \pdifmeta{version}{\enspace·\enspace\pdmeta{version}}{}%
    \pdifmeta{status}{\enspace·\enspace\pdmeta{status}}{}\par}%
  \endgroup
  \vspace{4mm}{\color{pd-rule}\rule{\linewidth}{.4pt}}\par\vspace{2mm}%
  \thispagestyle{plain.scrheadings}}

\newcommand\pd@memorow[2]{\pdifmeta{#1}{\pd@metafont #2 & \pdmeta{#1}\\}{}}
\newcommand\pd@title@memo{%
  \begingroup\pd@sffont\RaggedRight
  \pdifmeta{org}{{\footnotesize\bfseries\color{pd-ink2}\pdmeta{org}}\par\vspace{5mm}}{}%
  {\fontsize{18}{23}\selectfont\bfseries\pdmeta{title}\par}\vspace{5mm}%
  \begin{tabular}{@{}l@{\hspace{6mm}}l@{}}
    \pd@memorow{to}{To}\pd@memorow{from}{From}\pd@memorow{cc}{Cc}%
    \pd@memorow{date}{Date}\pd@memorow{docid}{Ref.}%
  \end{tabular}\par
  \endgroup
  \vspace{4mm}{\color{pd-rule}\rule{\linewidth}{.4pt}}\par\vspace{1mm}}

% Summary block for reports: label hangs like a section number.
\NewDocumentEnvironment{summary}{O{Summary}}{%
  \par\noindent\makebox[0pt][r]{\pd@labelfont #1\hspace{\pd@numgap}}\ignorespaces}%
  {\par\vspace{.5\baselineskip}}

% ==================================================================
% Contents: numbers hang in the index column (manual) or the margin
% (report, memo), exactly like the headings they point to; titles start
% on the text edge. No dot leaders.
% ==================================================================
\newlength\pd@tochang
\pd@iftype{manual}{\setlength\pd@tochang{\pd@hang}}{\setlength\pd@tochang{14mm}}
\newcommand\pd@tocnum[1]{\hfill#1\hspace{\pd@numgap}}
\edef\pd@tocin{-\the\pd@tochang}\edef\pd@tocnw{\the\pd@tochang}
\pd@ifchapters{%
  \DeclareTOCStyleEntry[beforeskip=.8\baselineskip, indent=\pd@tocin,
    numwidth=\pd@tocnw, dynnumwidth=false, entrynumberformat=\pd@tocnum,
    entryformat=\pd@sffont\bfseries, pagenumberformat=\pd@sffont\bfseries,
    linefill=\hfill]{tocline}{chapter}
  \DeclareTOCStyleEntry[indent=\pd@tocin, numwidth=\pd@tocnw,
    dynnumwidth=false, entrynumberformat=\pd@tocnum,
    entryformat=\pd@sffont, pagenumberformat=\pd@sffont,
    linefill=\hfill]{tocline}{section}
  \DeclareTOCStyleEntry[indent=\pd@tocin, numwidth=\pd@tocnw,
    dynnumwidth=false, entrynumberformat=\pd@tocnum,
    entryformat=\pd@sffont\color{pd-ink2}, pagenumberformat=\pd@sffont\color{pd-ink2},
    linefill=\hfill]{tocline}{subsection}
}{%
  \DeclareTOCStyleEntry[beforeskip=.4\baselineskip, indent=\pd@tocin,
    numwidth=\pd@tocnw, dynnumwidth=false, entrynumberformat=\pd@tocnum,
    entryformat=\pd@sffont\bfseries, pagenumberformat=\pd@sffont\bfseries,
    linefill=\hfill]{tocline}{section}
  \DeclareTOCStyleEntry[indent=\pd@tocin, numwidth=\pd@tocnw,
    dynnumwidth=false, entrynumberformat=\pd@tocnum,
    entryformat=\pd@sffont, pagenumberformat=\pd@sffont,
    linefill=\hfill]{tocline}{subsection}
}

% ==================================================================
% PDF: metadata, bookmarks, quiet links
% ==================================================================
\RequirePackage{hyperref}
\RequirePackage{bookmark}
\RequirePackage[nameinlink, noabbrev]{cleveref}
\hypersetup{hidelinks, bookmarksnumbered, bookmarksopen, pdfdisplaydoctitle,
  pdfcreator={LuaLaTeX + plaindoc}}
\AtBeginDocument{\hypersetup{pdftitle={\pdmeta{title}}, pdfauthor={\pdmeta{author}},
  pdfsubject={\pdmeta{subtitle}}, pdflang={\pd@mainlang}}}

\endinput
