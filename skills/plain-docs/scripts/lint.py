#!/usr/bin/env python3
"""Lint plaindoc LaTeX sources for slop: decoration, colour misuse, padded prose.

    python3 lint.py file.tex [more.tex ...] [--json out.json]

Errors are things that should never ship (placeholders, emoji, chat residue,
raw colours, packages that fight the class). Warnings are prompts to look
again; some are fine in context. Exit status: 1 if any error, else 0.
"""
import argparse
import json
import re
import sys
from pathlib import Path

# -- source-level rules: (level, code, regex, message) -----------------------
SOURCE_RULES = [
    ("error", "placeholder", r"\b(TODO|TBD|FIXME|XXX)\b|lorem ipsum|\[(INSERT|PLACEHOLDER)",
     "Placeholder text"),
    ("error", "chat-residue",
     r"(As an AI\b|I hope this helps|Certainly!|Here is (the|your) |turn\d+(search|view|fetch)\d+|【\d|\ue200)",
     "Chatbot residue in the document"),
    ("error", "emoji", "[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF\u2B50\u2705\u274C\u2728]",
     "Emoji: use words, a table, or a safety message instead"),
    ("error", "raw-colour",
     r"\\(definecolor|colorlet)\b|\\(textcolor|color|colorbox|cellcolor|rowcolor)\{(?!pd-|oi-|white\}|black\})[^}]*\}",
     "Colour outside the plaindoc roles (pd-*, oi-* for data)"),
    ("error", "fighting-package",
     r"\\usepackage(\[[^\]]*\])?\{[^}]*\b(tcolorbox|mdframed|fontawesome5?|fontawesome|times|mathptmx|helvet|lmodern|fontenc|inputenc|fancyhdr|titlesec|geometry|xcolor)\b[^}]*\}",
     "Package that overrides the class design; use the class features"),
    ("warning", "manual-space", r"\\(vspace|hspace)\*?\{(?!\\fill)",
     "Manual spacing: let the class set space, or explain why"),
    ("warning", "forced-break", r"(?<!\\)\\\\\s*$(?![^\n]*&)", "Forced line break at end of line"),
    ("warning", "size-command", r"\\(tiny|scriptsize|large|Large|LARGE|huge|Huge)\b",
     "Size change in the body: the type scale belongs to the class"),
    ("warning", "underline", r"\\underline\{", "Underlining: use the class emphasis"),
    ("warning", "straight-quote", r'(?<![\\=])"(?=\w)', "Straight quote: use “ ”, \\enquote or \\pdq"),
    ("warning", "three-dots", r"(?<!\.)\.\.\.(?!\.)", "Three full stops: use … or \\dots"),
    ("warning", "spaced-hyphen", r'(?<=[\w"\u201d\u2019)]) - (?=\w)', "Spaced hyphen used as a dash: use – or —"),
    ("warning", "exclamation", r"[A-Za-z]!+(\s|$)", "Exclamation mark in prose"),
    ("warning", "bare-unit",
     r"(?:(?<=\s)|^)\d+(\.\d+)?\s?(mV|mA|kV|kW|kHz|MHz|GHz|mm|cm|kg|°C|ms|µs)\b(?!\s*[,=\]])",
     "Number with unit outside \\qty: spacing and decimal marker will not follow the language"),
    ("warning", "cjk-halfwidth",
     r"[\u4e00-\u9fff\u3040-\u30ff][,.:;!?](?=[\u4e00-\u9fff\u3040-\u30ff\s]|$)",
     "Half-width punctuation after CJK text: use ，。：；！？"),
]

# Words and phrases that inflate or sell instead of inform. Review, don't
# blindly delete: replace with the fact the sentence should carry.
PADDING = [
    r"seamless(ly)?", r"leverag(e|es|ed|ing)", r"robust", r"cutting[- ]edge", r"state[- ]of[- ]the[- ]art",
    r"delv(e|es|ing)", r"unlock(s|ing)? (the|your|new)", r"unleash", r"empower(s|ing)?", r"elevat(e|es|ing)",
    r"streamlin(e|ed|es|ing)", r"holistic", r"synerg(y|ies)", r"game[- ]chang(er|ing)", r"world[- ]class",
    r"best[- ]in[- ]class", r"next[- ]generation", r"revolutioni[sz]", r"effortless(ly)?", r"intuitive(ly)?",
    r"user[- ]friendly", r"in today'?s", r"it is important to note", r"it'?s worth noting", r"(crucial|vital|pivotal) role",
    r"a testament to", r"navigat(e|ing) the", r"embark", r"\bjourney\b", r"harness(es|ing)?", r"tapestry",
    r"\bboasts?\b", r"nestled", r"vibrant", r"\bfurthermore\b", r"\bmoreover\b", r"in conclusion",
    r"key takeaways?", r"dive (in|into)", r"look no further", r"whether you'?re", r"rest assured",
    r"\bsimply\b", r"\beasily\b", r"please note", r"\bcomprehensive\b", r"\bpowerful\b", r"\bsleek\b",
]
PADDING_RE = re.compile(r"\b(" + "|".join(PADDING) + r")", re.I)

HEADING_RE = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?(\[[^\]]*\])?\{([^}]*)\}")
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "via", "with"}


def strip_comment(line):
    return re.sub(r"(?<!\\)%.*$", "", line)


def heading_findings(title, lineno, path):
    out = []
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", title)
    content = [w for w in words[1:] if w.lower() not in SMALL_WORDS]
    if len(content) >= 2 and all(w[0].isupper() for w in content) and not all(w.isupper() for w in content):
        out.append(("warning", "title-case", f"Heading in Title Case: use sentence case ('{title}')"))
    if re.search(r":\s*\S", title) and not re.search(r"[\u4e00-\u9fff]", title):
        out.append(("warning", "colon-heading", f"Two-part heading with a colon: say it once ('{title}')"))
    if title.rstrip().endswith(("?", "!")):
        out.append(("warning", "heading-punct", f"Heading ends with ? or ! ('{title}')"))
    return [{"file": str(path), "line": lineno, "level": l, "code": c, "message": m} for l, c, m in out]


VERBATIM_ENVS = {"code", "Verbatim", "verbatim", "lstlisting", "minted"}
DRAWING_ENVS = {"tikzpicture", "axis", "scope"}
TABLE_ENVS = {"tabular", "tabular*", "tabularx", "xltabular", "longtable", "array", "align", "align*"}
ENV_RE = re.compile(r"\\(begin|end)\{([^}]+)\}")
# Rules that only make sense in running prose.
PROSE_ONLY = {"forced-break", "bare-unit", "three-dots", "size-command", "spaced-hyphen",
              "exclamation", "straight-quote", "manual-space"}


def lint_text(text, path="<string>"):
    findings = []
    stack = []
    para_bold = 0
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = strip_comment(raw)
        in_verbatim = any(e in VERBATIM_ENVS for e in stack)
        for kind, env in ENV_RE.findall(line):
            if kind == "begin":
                stack.append(env)
            elif env in stack:
                del stack[len(stack) - 1 - stack[::-1].index(env)]
        if in_verbatim or any(e in VERBATIM_ENVS for e in stack):
            continue
        opened = {env for kind, env in ENV_RE.findall(line) if kind == "begin"}
        in_drawing = any(e in DRAWING_ENVS for e in stack) or bool(opened & DRAWING_ENVS) or "\\tikz" in line
        in_table = any(e in TABLE_ENVS for e in stack) or bool(opened & TABLE_ENVS)
        if not line.strip():
            para_bold = 0
            continue
        for level, code, pattern, message in SOURCE_RULES:
            if code in PROSE_ONLY and (in_drawing or in_table):
                continue
            if code == "manual-space" and re.search(r"\\pdset|\\newcommand|\\def", line):
                continue
            if re.search(pattern, line):
                findings.append({"file": str(path), "line": lineno, "level": level, "code": code, "message": message})
        if in_drawing:
            continue
        prose = re.sub(r"\\[A-Za-z@]+\*?(\[[^\]]*\])?", " ", line)
        for m in PADDING_RE.finditer(prose):
            findings.append({"file": str(path), "line": lineno, "level": "warning", "code": "padding",
                             "message": f"'{m.group(0)}': state the fact instead"})
        if not in_table:
            para_bold += len(re.findall(r"\\textbf\{", line))
            if para_bold > 2:
                findings.append({"file": str(path), "line": lineno, "level": "warning", "code": "bold-density",
                                 "message": "More than two bold spans in one paragraph: bold is for UI labels and lead-ins"})
                para_bold = -100  # once per paragraph
        for m in HEADING_RE.finditer(line):
            findings += heading_findings(m.group(3), lineno, path)
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args(argv)
    findings = []
    for f in args.files:
        findings += lint_text(f.read_text(encoding="utf-8"), f)
    for f in findings:
        print(f"{f['file']}:{f['line']}: {f['level']}: [{f['code']}] {f['message']}")
    errors = sum(f["level"] == "error" for f in findings)
    print(f"{errors} error(s), {len(findings) - errors} warning(s)")
    if args.json:
        args.json.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
