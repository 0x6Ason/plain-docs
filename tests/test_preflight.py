"""Small failure-oriented tests; no network or installed system fonts required."""
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT / 'skills/plain-docs/scripts/preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def test_meaningful_unicode_is_preserved(self):
        text = '繁體中文 简体中文 café 25 °C 10 µm Ω ≤ ≥ − ×'
        self.assertEqual(preflight.scan_text(text, 'test'), [])

    def test_corruption_and_residue_are_detected(self):
        issues = preflight.scan_text('Bad \ufffd\x00\n\ue200cite\ue202turn3search2\ue201\nFranÃ§ais', 'test')
        codes = {i['code'] for i in issues}
        self.assertTrue({'invalid_character', 'tool_residue', 'possible_mojibake'} <= codes)

    def test_source_is_never_rewritten(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'source.txt'
            original = '真实内容 \ufffd'.encode('utf-8')
            path.write_bytes(original)
            with redirect_stdout(io.StringIO()):
                code = preflight.main(['source', str(path)])
            self.assertEqual(code, 1)
            self.assertEqual(path.read_bytes(), original)

    def test_report_cannot_overwrite_source(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'source.txt'
            path.write_text('Keep this.', encoding='utf-8')
            with redirect_stderr(io.StringIO()):
                code = preflight.main(['source', str(path), '--json', str(path)])
            self.assertEqual(code, 2)
            self.assertEqual(path.read_text(), 'Keep this.')

    def test_invalid_utf8_fails_instead_of_dropping_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'source.txt'
            path.write_bytes(b'invalid \xff')
            with redirect_stderr(io.StringIO()):
                self.assertEqual(preflight.main(['source', str(path)]), 2)

    def test_font_coverage_finds_missing_chinese(self):
        import reportlab
        font = Path(reportlab.__file__).parent / 'fonts/Vera.ttf'
        self.assertFalse(any(i['level'] == 'error' for i in preflight.check_font('Export 123', font)))
        issues = preflight.check_font('中文', font)
        self.assertIn('missing_glyphs', {i['code'] for i in issues})

    def test_extraction_and_page_bounds(self):
        from reportlab.pdfgen.canvas import Canvas
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'bad.pdf'
            canvas = Canvas(str(path), pagesize=(300, 300))
            canvas.drawString(20, 220, 'Critical value: 25.0 V')
            canvas.drawString(290, 100, 'Clipped text')
            canvas.save()
            issues, details = preflight.inspect_pdf(path, ['25.0 V', 'Missing label'])
            self.assertEqual(details['pages'], 1)
            self.assertTrue({'outside_page', 'expected_text_missing'} <= {i['code'] for i in issues})
            self.assertFalse(any(i.get('expected') == '25.0 V' for i in issues))

    def test_visible_cropbox_is_checked(self):
        from reportlab.pdfgen.canvas import Canvas
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import RectangleObject
        with tempfile.TemporaryDirectory() as temp:
            original, cropped = Path(temp) / 'full.pdf', Path(temp) / 'crop.pdf'
            canvas = Canvas(str(original), pagesize=(300, 300))
            canvas.drawString(220, 200, 'Outside crop')
            canvas.save()
            reader = PdfReader(original)
            reader.pages[0].cropbox = RectangleObject([0, 0, 200, 300])
            writer = PdfWriter()
            writer.add_page(reader.pages[0])
            writer.write(cropped)
            issues, _ = preflight.inspect_pdf(cropped)
            self.assertIn('outside_page', {i['code'] for i in issues})

    def test_embedded_font_round_trip(self):
        import reportlab
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen.canvas import Canvas
        font = Path(reportlab.__file__).parent / 'fonts/Vera.ttf'
        pdfmetrics.registerFont(TTFont('TestVera', str(font)))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'good.pdf'
            canvas = Canvas(str(path), initialFontName='TestVera')
            canvas.setFont('TestVera', 11)
            canvas.drawString(60, 700, 'Export complete: 123')
            canvas.save()
            issues, details = preflight.inspect_pdf(path, ['Export complete: 123'])
            self.assertFalse(any(i['level'] == 'error' for i in issues))
            self.assertTrue(all(f['embedded'] for f in details['fonts']))
            self.assertTrue(all(f['to_unicode'] for f in details['fonts']))


if __name__ == '__main__':
    unittest.main()
