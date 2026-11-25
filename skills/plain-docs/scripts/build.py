#!/usr/bin/env python3
"""Build a plaindoc document with LuaLaTeX, check it and render its pages.

    python3 build.py document.tex [--render DIR] [--expect strings.txt] [--strict]

Runs latexmk -lualatex with the plaindoc class on TEXINPUTS, then check.py
on the log and PDF. With --render, writes one PNG per page plus a contact
sheet (contact.png) for review. Exit status follows check.py.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLASS_DIR = HERE.parent / "latex"
sys.path.insert(0, str(HERE))
import check  # noqa: E402


def render(pdf, outdir, dpi):
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("page-*.png"):
        old.unlink()
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(outdir / "page")], check=True)
    pages = sorted(outdir.glob("page-*.png"))
    try:
        from PIL import Image
    except ImportError:
        return pages, None
    thumbs = [Image.open(p) for p in pages]
    w, h = thumbs[0].size
    scale = 300 / w
    tw, th = int(w * scale), int(h * scale)
    cols = min(5, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 12) + 12), (128, 128, 128))
    for i, im in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet.paste(im.convert("RGB").resize((tw, th)), (12 + c * (tw + 12), 12 + r * (th + 12)))
    sheet.save(outdir / "contact.png")
    return pages, outdir / "contact.png"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tex", type=Path)
    ap.add_argument("--render", type=Path, help="directory for page images")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--expect", type=Path)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)

    for tool in ("latexmk", "lualatex", "pdffonts", "pdftotext"):
        if not shutil.which(tool):
            print(f"build.py: '{tool}' not found. See references/verification.md for setup.", file=sys.stderr)
            return 2

    tex = args.tex.resolve()
    env = dict(os.environ)
    env["TEXINPUTS"] = f"{CLASS_DIR}//:{env.get('TEXINPUTS', '')}"
    env["max_print_line"] = "10000"  # one log message per line
    cmd = ["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error",
           "-file-line-error", tex.name]
    proc = subprocess.run(cmd, cwd=tex.parent, env=env, capture_output=True, text=True)
    log, pdf = tex.with_suffix(".log"), tex.with_suffix(".pdf")
    if proc.returncode != 0 and not log.exists():
        print(proc.stdout[-3000:], proc.stderr[-2000:], sep="\n")
        return 2

    check_args = [str(log), "--pdf", str(pdf)]
    if args.expect:
        check_args += ["--expect", str(args.expect)]
    if args.strict:
        check_args.append("--strict")
    status = check.main(check_args)
    if proc.returncode != 0 and status == 0:
        status = 1
    if args.render and pdf.exists():
        pages, sheet = render(pdf, args.render, args.dpi)
        print(f"Render  {len(pages)} page image(s) in {args.render}" + (f"; contact sheet {sheet}" if sheet else ""))
    return status


if __name__ == "__main__":
    sys.exit(main())
