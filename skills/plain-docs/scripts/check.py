#!/usr/bin/env python3
"""Check a LuaLaTeX build: log problems, font embedding, expected text.

    python3 check.py document.log [--pdf document.pdf] [--expect strings.txt] [--json out.json]

Exit status: 0 clean, 1 errors found, 2 could not run.
Warnings never change the exit status unless --strict is given.
A clean result does not replace looking at every rendered page.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# (level, code, pattern, message). Patterns run on the unwrapped log.
LOG_RULES = [
    ("error", "tex-error", r"^! (.+)$", "TeX error: {0}"),
    ("error", "missing-glyph", r"Missing character: There is no (.+?) in font ([^!]+?)!?$",
     "Missing glyph {0} in font {1}: the character prints as nothing or a box"),
    ("error", "overfull", r"^Overfull \\hbox \(([\d.]+)pt too wide\) (.+)$",
     "Line {1} sticks out by {0} pt"),
    ("error", "overfull-v", r"^Overfull \\vbox \(([\d.]+)pt too high\) (.+)$",
     "Box {1} too tall by {0} pt"),
    ("error", "undefined-ref", r"LaTeX Warning: Reference `([^']+)' on page (\d+) undefined",
     "Undefined reference '{0}' on page {1}"),
    ("error", "undefined-cite", r"(?:LaTeX|Package natbib|Package biblatex) Warning: Citation [`']([^']+)' .*undefined",
     "Undefined citation '{0}'"),
    ("error", "font-missing", r"No usable (.+?) font \(tried: (.+?)\)",
     "No usable {0} font (tried {1})"),
    ("warning", "font-fallback", r"plaindoc font fallback: (.+?) '(.+?)' not found, using '(.+?)'",
     "{0}: '{1}' is not installed, '{2}' was used instead. Install it or tell the reader"),
    ("warning", "no-label", r"No '(\w+)' label for language '([\w-]+)'",
     "No translated '{0}' label for {1}: set one with \\pdsetstring"),
    ("warning", "underfull", r"^Underfull \\hbox \(badness 10000\) (.+)$",
     "Very loose line {0}"),
    ("warning", "font-shape", r"Font shape `([^']+)' undefined",
     "Font shape {0} undefined: a substitute was used"),
    ("warning", "rerun", r"(Label\(s\) may have changed|Rerun to get)",
     "Cross-references may be stale: run the build again"),
]


def unwrap_log(text):
    """TeX wraps log lines at 79 columns. Join the continuations we can detect."""
    lines = text.splitlines()
    out = []
    for line in lines:
        if out and len(out[-1]) == 79 and not line.startswith(("!", "(", ")", "[", "Overfull", "Underfull", "LaTeX", "Package")):
            out[-1] += line
        else:
            out.append(line)
    return out


def check_log(text):
    findings = []
    seen = set()
    for line in unwrap_log(text):
        for level, code, pattern, message in LOG_RULES:
            m = re.search(pattern, line)
            if not m:
                continue
            if code == "tex-error" and line.startswith("!  ==> Fatal"):
                continue
            msg = message.format(*[g.strip() for g in m.groups()])
            if (code, msg) in seen:
                continue
            seen.add((code, msg))
            findings.append({"level": level, "code": code, "message": msg})
    return findings


def run(cmd):
    if not shutil.which(cmd[0]):
        raise FileNotFoundError(cmd[0])
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout


def check_fonts(pdf):
    findings = []
    out = run(["pdffonts", str(pdf)])
    rows = out.splitlines()[2:]
    fonts = []
    for row in rows:
        parts = row.split()
        if len(parts) < 7:
            continue
        # name type... encoding emb sub uni object-id gen
        name, emb, uni = parts[0], parts[-5], parts[-3]
        ftype = " ".join(parts[1:-6])
        fonts.append(name)
        if emb != "yes":
            findings.append({"level": "error", "code": "not-embedded",
                             "message": f"Font {name} is not embedded"})
        if uni != "yes":
            findings.append({"level": "warning", "code": "no-tounicode",
                             "message": f"Font {name} has no ToUnicode map: copied text may be wrong"})
        if "Type 3" in ftype:
            findings.append({"level": "warning", "code": "type3",
                             "message": f"Type 3 font {name}: usually a bitmap or a missing outline font"})
    return findings, sorted({re.sub(r"^[A-Z]{6}\+", "", f) for f in fonts})


def normalise(s):
    return re.sub(r"\s+", "", s)


def check_text(pdf, expect_file):
    findings = []
    text = normalise(run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"]))
    for raw in Path(expect_file).read_text(encoding="utf-8").splitlines():
        want = raw.strip()
        if want and normalise(want) not in text:
            findings.append({"level": "error", "code": "missing-text",
                             "message": f"Expected text not found in PDF: {want}"})
    return findings


def page_count(pdf):
    m = re.search(r"^Pages:\s+(\d+)", run(["pdfinfo", str(pdf)]), re.M)
    return int(m.group(1)) if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("log", type=Path)
    ap.add_argument("--pdf", type=Path)
    ap.add_argument("--expect", type=Path, help="UTF-8 file, one required string per line")
    ap.add_argument("--json", type=Path)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    try:
        findings = check_log(args.log.read_text(encoding="utf-8", errors="replace"))
        fonts, pages = [], None
        if args.pdf:
            if not args.pdf.exists():
                findings.append({"level": "error", "code": "no-pdf", "message": f"{args.pdf} was not produced"})
            else:
                f, fonts = check_fonts(args.pdf)
                findings += f
                pages = page_count(args.pdf)
                if args.expect:
                    findings += check_text(args.pdf, args.expect)
    except FileNotFoundError as e:
        print(f"check.py: cannot run: {e} (install poppler-utils)", file=sys.stderr)
        return 2

    errors = [f for f in findings if f["level"] == "error"]
    warnings = [f for f in findings if f["level"] == "warning"]
    for f in findings:
        print(f"{f['level'].upper():7} {f['code']:14} {f['message']}")
    if fonts:
        print("Fonts   " + ", ".join(fonts))
    if pages:
        print(f"Pages   {pages}")
    print(f"Result  {len(errors)} error(s), {len(warnings)} warning(s). "
          "Now render and look at every page.")
    if args.json:
        args.json.write_text(json.dumps({"errors": errors, "warnings": warnings,
                                         "fonts": fonts, "pages": pages}, indent=2,
                                        ensure_ascii=False), encoding="utf-8")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
