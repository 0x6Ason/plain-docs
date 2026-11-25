"""Tests for lint.py, check.py and (when LuaLaTeX is installed) build.py.

    python3 -m unittest discover -s tests -v
"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "plain-docs" / "scripts"))
import build  # noqa: E402
import check  # noqa: E402
import lint  # noqa: E402


def codes(findings):
    return {f["code"] for f in findings}


class LintTests(unittest.TestCase):
    def test_clean_source_passes(self):
        src = (r"\section{Connect a load}" "\n"
               r"Switch the output off with \key{OUTPUT}, then connect the load." "\n"
               r"Set the limit to \qty{0.5}{\ampere}." "\n")
        self.assertEqual(lint.lint_text(src), [])

    def test_errors(self):
        src = ("TODO: write this\n"
               "\\usepackage{tcolorbox}\n"
               "\\textcolor{red}{Danger}\n"
               "\U0001F680 Launch\n"
               "I hope this helps.\n")
        found = codes(f for f in lint.lint_text(src) if f["level"] == "error")
        self.assertEqual(found, {"placeholder", "fighting-package", "raw-colour", "emoji", "chat-residue"})

    def test_role_colours_allowed(self):
        self.assertEqual(lint.lint_text(r"\textcolor{pd-ink2}{x} \color{oi-blue}"), [])

    def test_padding_and_headings(self):
        src = "\\section{Unlock The Power Of Your Supply}\nA seamless, robust workflow.\n"
        found = codes(lint.lint_text(src))
        self.assertIn("padding", found)
        self.assertIn("title-case", found)

    def test_sentence_case_heading_ok(self):
        self.assertEqual(lint.lint_text(r"\section{Set voltage and current limit}"), [])

    def test_drawing_and_tables_are_not_prose(self):
        src = ("\\begin{tikzpicture}[x=1mm]\n\\node[font=\\scriptsize] at (0,0) {5 mm};\n\\end{tikzpicture}\n"
               "\\begin{tabular}{ll}\n\\textbf{a} & \\textbf{b} \\\\\n\\textbf{c} & d \\\\\n\\end{tabular}\n")
        self.assertEqual(lint.lint_text(src), [])

    def test_verbatim_ignored(self):
        self.assertEqual(lint.lint_text("\\begin{code}\nTODO \"x\" ...\n\\end{code}\n"), [])

    def test_cjk_halfwidth(self):
        self.assertIn("cjk-halfwidth", codes(lint.lint_text("請按下按鈕,然後關閉.")))


LOG = r"""
Overfull \hbox (3.62936pt too wide) in paragraph at lines 147--147
Overfull \hbox (0.4pt too wide) in paragraph at lines 10--12
Missing character: There is no 𐀀 (U+10000) in font STIXTwoText:mode=node;script=latn;language=dflt;!
LaTeX Warning: Reference `sec:set' on page 3 undefined on input line 194.
Package plaindoc Warning: plaindoc font fallback: Latin sans 'IBMPlexSans' not found, using 'TeX Gyre Heros'.
Underfull \hbox (badness 10000) in paragraph at lines 5--6
! Undefined control sequence.
"""


class CheckLogTests(unittest.TestCase):
    def test_log_rules(self):
        f = check.check_log(LOG)
        errors = codes(x for x in f if x["level"] == "error")
        warnings = codes(x for x in f if x["level"] == "warning")
        self.assertEqual(errors, {"overfull", "missing-glyph", "undefined-ref", "tex-error"})
        self.assertEqual(warnings, {"font-fallback", "underfull"})

    def test_wrapped_log_line(self):
        wrapped = ("Missing character: There is no ✓ (U+2713) in font IBMPlexSans:mode=node;script=latn;languag\n"
                   "e=dflt;!\n")
        self.assertIn("missing-glyph", codes(check.check_log(wrapped)))

    def test_clean_log(self):
        self.assertEqual(check.check_log("This is LuaHBTeX\nOutput written on x.pdf (1 page).\n"), [])


@unittest.skipUnless(shutil.which("lualatex") and shutil.which("latexmk") and shutil.which("pdffonts"),
                     "LuaLaTeX toolchain not installed")
class BuildTests(unittest.TestCase):
    def build(self, body, cls_opts="type=report"):
        tmp = Path(tempfile.mkdtemp())
        tex = tmp / "t.tex"
        tex.write_text("\\documentclass[%s]{plaindoc}\n\\pdset{title={Test}}\n\\begin{document}\n%s\n\\end{document}\n"
                       % (cls_opts, body), encoding="utf-8")
        expect = tmp / "expect.txt"
        expect.write_text("−10 °C\n≤ 0.5\n", encoding="utf-8")
        return build.main([str(tex), "--expect", str(expect)])

    def test_clean_build(self):
        self.assertEqual(self.build(r"\section{Range}Range −10 °C to 50 °C, error ≤ 0.5 °C."), 0)

    def test_missing_glyph_fails(self):
        # Linear B is in none of the configured fonts.
        self.assertEqual(self.build("\\section{Range}Range −10 °C, ≤ 0.5. \U00010000"), 1)


if __name__ == "__main__":
    unittest.main()
