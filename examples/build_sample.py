#!/usr/bin/env python3
"""Build a three-language specimen from explicit font paths; no font downloads."""
import argparse
import importlib.util
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                               Table, TableStyle, ListFlowable, ListItem)

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT / 'skills/plain-docs/scripts/preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            if key != 'locale':
                yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def build(args):
    data = json.loads(args.source.read_text(encoding='utf-8'))
    mappings = {'en': 'latin', 'zh-Hant': 'tc', 'zh-Hans': 'sc'}
    for entry in data['locales']:
        prefix = mappings[entry['locale']]
        display = '\n'.join(strings(entry)) + '\n' + data['product'] + '\n0123456789 /'
        # This small specimen checks both faces against all text: conservative but simple.
        for weight in ('regular', 'bold'):
            path = getattr(args, f'{prefix}_{weight}')
            issues = preflight.scan_text(display, entry['locale']) + preflight.check_font(display, path)
            errors = [i for i in issues if i['level'] == 'error' or i['code'] == 'no_subsetting']
            if errors:
                raise ValueError(json.dumps(errors, ensure_ascii=True))
            name = f'{prefix}-{weight}'
            pdfmetrics.registerFont(TTFont(name, str(path), subfontIndex=0))
        pdfmetrics.registerFontFamily(prefix, normal=f'{prefix}-regular', bold=f'{prefix}-bold')

    args.out.parent.mkdir(parents=True, exist_ok=True)
    width = A4[0] - 48 * mm - 12  # SimpleDocTemplate frame has 6 pt padding per side.
    doc = SimpleDocTemplate(str(args.out), pagesize=A4,
                            leftMargin=24 * mm, rightMargin=24 * mm,
                            topMargin=21 * mm, bottomMargin=22 * mm,
                            title='Archive Desk record export guide', author='Plain Docs',
                            subject='Fictional user manual specimen in English and Chinese')
    story = []
    for idx, entry in enumerate(data['locales']):
        if idx:
            story.append(PageBreak())
        prefix = mappings[entry['locale']]
        cjk = prefix != 'latin'
        regular, bold = f'{prefix}-regular', f'{prefix}-bold'
        body = ParagraphStyle('body', fontName=regular, fontSize=11,
                              leading=17 if cjk else 15, spaceAfter=8,
                              wordWrap='CJK' if cjk else None)
        title = ParagraphStyle('title', parent=body, fontName=bold, fontSize=23,
                               leading=30, spaceAfter=4, keepWithNext=True)
        heading = ParagraphStyle('heading', parent=body, fontName=bold, fontSize=13,
                                 leading=19, spaceBefore=9, spaceAfter=5, keepWithNext=True)
        small = ParagraphStyle('small', parent=body, fontSize=9, leading=13,
                               textColor=colors.HexColor('#555555'), spaceAfter=12)
        brand = ParagraphStyle('brand', parent=body, fontName=bold, fontSize=10, leading=14)
        tablebody = ParagraphStyle('cell', parent=body, fontSize=10, leading=15, spaceAfter=0)
        tablehead = ParagraphStyle('tablehead', parent=tablebody, fontName=bold)
        story.extend([Paragraph(escape(data['product']), brand),
                      Paragraph(escape(entry['title']), title),
                      Paragraph(escape(entry['disclosure']), small),
                      Paragraph(escape(entry['intro']), body)])
        for section in ('before', 'steps', 'result', 'trouble'):
            story.append(Paragraph(escape(entry[f'{section}_title']), heading))
            if section == 'steps':
                steps = [ListItem(Paragraph(escape(step), body)) for step in entry['steps']]
                story.append(ListFlowable(steps, bulletType='1', start='1',
                             leftIndent=17, bulletFontName=regular, bulletFontSize=11,
                             bulletOffsetY=0, spaceAfter=0))
            elif section == 'trouble':
                rows = [[Paragraph(escape(t), tablehead) for t in entry['table_headers']]]
                rows += [[Paragraph(escape(t), tablebody) for t in row] for row in entry['rows']]
                table = Table(rows, colWidths=[width * .29, width * .71], repeatRows=1,
                              hAlign='LEFT')
                table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), regular),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0F0F0')),
                    ('LINEBELOW', (0, 0), (-1, 0), .5, colors.HexColor('#B5B5B5')),
                    ('LINEBELOW', (0, 1), (-1, -1), .35, colors.HexColor('#D8D8D8')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 7),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ]))
                story.append(table)
            else:
                story.append(Paragraph(escape(entry[section]), body))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont('latin-regular', 9)
        canvas.setFillColor(colors.HexColor('#555555'))
        canvas.drawString(24 * mm + 6, 12 * mm, data['product'])
        canvas.drawRightString(A4[0] - 24 * mm - 6, 12 * mm, str(document.page))
        canvas.restoreState()

    def make_canvas(*cargs, **kwargs):
        kwargs.update(initialFontName='latin-regular', lang='en')
        return Canvas(*cargs, **kwargs)

    doc.build(story, onFirstPage=footer, onLaterPages=footer, canvasmaker=make_canvas)
    print(args.out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).with_name('manual-source.json'))
    parser.add_argument('--out', type=Path, required=True)
    for prefix in ('latin', 'tc', 'sc'):
        for weight in ('regular', 'bold'):
            parser.add_argument(f'--{prefix}-{weight}', type=Path, required=True)
    build(parser.parse_args())


if __name__ == '__main__':
    main()
