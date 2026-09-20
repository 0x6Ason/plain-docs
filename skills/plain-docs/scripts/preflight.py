#!/usr/bin/env python3
"""Read-only document checks. No result substitutes for visual inspection."""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path


def finding(level, code, message, **where):
    return dict(level=level, code=code, message=message, **where)


def scan_text(text, location):
    issues = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for char in sorted(set(line)):
            cp = ord(char)
            category = unicodedata.category(char)
            if char == '\ufffd' or (category == 'Cc' and char not in '\t\n\r'):
                issues.append(finding('error', 'invalid_character',
                    f'Inspect U+{cp:04X} {unicodedata.name(char, "CONTROL")}.',
                    location=location, line=line_number))
            elif category == 'Co' or category == 'Cf':
                issues.append(finding('warning', 'special_character',
                    f'Review U+{cp:04X}; private-use or format character may be intentional.',
                    location=location, line=line_number))
        patterns = [
            ('error', 'tool_residue', r'\ue200(?:cite|navlist|entity)|:codex-(?:file-citation|citation)|\bturn\d+(?:search|view|fetch)\d+'),
            ('warning', 'possible_mojibake', r'\u00c3[\u0080-\u00bf]|\u00c2[\u0080-\u00bf]|\u00e2\u20ac|\u00ef\u00bf\u00bd|\u00f0\u0178'),
            ('warning', 'unmapped_cid', r'\(cid:\d+\)'),
            ('warning', 'placeholder', r'\b(?:TODO|TBD|FIXME)\b|\[(?:INSERT|PLACEHOLDER)\b'),
        ]
        for level, code, pattern in patterns:
            if re.search(pattern, line):
                issues.append(finding(level, code,
                    'Inspect this line in context; literal examples may be intentional.',
                    location=location, line=line_number))
    # splitlines treats some control characters as boundaries; check those too.
    for cp in (11, 12, 28, 29, 30, 133):
        if chr(cp) in text:
            issues.append(finding('warning', 'text_separator',
                f'Review U+{cp:04X} separator.', location=location))
    return issues


def check_font(text, font_path, index=0):
    from fontTools.ttLib import TTFont
    issues = []
    with TTFont(str(font_path), fontNumber=index) as font:
        cmap = font.getBestCmap() or {}
        needed = {ord(c) for c in text if not c.isspace()
                  and unicodedata.category(c) != 'Cf'
                  and not 0xFE00 <= ord(c) <= 0xFE0F
                  and not 0xE0100 <= ord(c) <= 0xE01EF}
        missing = sorted(cp for cp in needed if not cmap.get(cp)
                         or cmap[cp] == '.notdef')
        if missing:
            issues.append(finding('error', 'missing_glyphs',
                'Selected face does not cover all assigned text.',
                font=str(font_path), index=index,
                codepoints=[f'U+{cp:04X}' for cp in missing]))
        flags = font['OS/2'].fsType if 'OS/2' in font else None
        if flags is not None and flags & (0x0002 | 0x0200):
            issues.append(finding('error', 'embedding_restriction',
                'Font flags restrict outline embedding; check the license or use another font.',
                font=str(font_path), fsType=flags))
        if flags is not None and flags & 0x0100:
            issues.append(finding('warning', 'no_subsetting',
                'Font flags prohibit subsetting; check exporter behavior and license.',
                font=str(font_path)))
    return issues


def font_inventory(resources, seen=None):
    """Include form XObject fonts. Resources may include unused fonts."""
    seen = set() if seen is None else seen
    if not resources:
        return []
    resources = resources.get_object()
    identity = id(resources)
    if identity in seen:
        return []
    seen.add(identity)
    records = []
    fonts = resources.get('/Font', {})
    if hasattr(fonts, 'get_object'):
        fonts = fonts.get_object()
    for ref in fonts.values():
        font = ref.get_object()
        descendants = font.get('/DescendantFonts')
        if descendants is not None:
            descendants = descendants.get_object()
        parts = [x.get_object() for x in descendants] if descendants else [font]
        embedded_parts = []
        for part in parts:
            descriptor = part.get('/FontDescriptor')
            descriptor = descriptor.get_object() if descriptor else {}
            embedded_parts.append(any(descriptor.get(key) is not None
                                      for key in ('/FontFile', '/FontFile2', '/FontFile3')))
        records.append(dict(name=str(font.get('/BaseFont', 'unnamed')),
                            subtype=str(font.get('/Subtype', 'unknown')),
                            embedded=all(embedded_parts),
                            to_unicode=font.get('/ToUnicode') is not None))
    objects = resources.get('/XObject', {})
    if hasattr(objects, 'get_object'):
        objects = objects.get_object()
    for ref in objects.values():
        obj = ref.get_object()
        if obj.get('/Subtype') == '/Form':
            records.extend(font_inventory(obj.get('/Resources'), seen))
    return records


def compact(text):
    return ''.join(c for c in text if not c.isspace())


def inspect_pdf(path, expected=()):
    import pdfplumber
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    if reader.is_encrypted:
        raise ValueError('Encrypted PDF: supply a readable copy for this checker.')
    issues, texts, fonts = [], [], []
    with pdfplumber.open(path) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ''
            texts.append(text)
            issues.extend(scan_text(text, f'page {number}'))
            if not text.strip():
                issues.append(finding('warning', 'no_extractable_text',
                    'Page has no extractable text; inspect for an intentional blank or image-only page.',
                    page=number))
            x0, top, x1, bottom = page.cropbox or page.bbox
            outside = [c for c in page.chars if c.get('text', '').strip() and
                       (c['x0'] < x0 - 1 or c['x1'] > x1 + 1 or
                        c['top'] < top - 1 or c['bottom'] > bottom + 1)]
            if outside:
                issues.append(finding('error', 'outside_page',
                    'Extracted character bounds extend outside the visible page; inspect clipping.',
                    page=number, count=len(outside)))
            for record in font_inventory(reader.pages[number - 1].get('/Resources')):
                if record not in fonts:
                    fonts.append(record)
    for font in fonts:
        if not font['embedded']:
            issues.append(finding('warning', 'font_not_embedded',
                'Font resource is not embedded; determine whether used and portable.', font=font['name']))
        if not font['to_unicode']:
            issues.append(finding('warning', 'unicode_map_absent',
                'No explicit ToUnicode map; verify copying and extraction.', font=font['name']))
    combined = compact('\n'.join(texts))
    for wanted in expected:
        if compact(wanted) and compact(wanted) not in combined:
            issues.append(finding('error', 'expected_text_missing',
                'Expected text was not found after whitespace-insensitive extraction.', expected=wanted))
    root = reader.trailer['/Root']
    if not root.get('/StructTreeRoot'):
        issues.append(finding('warning', 'structure_tree_absent',
            'No PDF structure tree; do not describe this as an accessible tagged PDF.'))
    if not root.get('/Lang'):
        issues.append(finding('warning', 'language_metadata_absent', 'Document language metadata is absent.'))
    return issues, dict(pages=len(texts), fonts=fonts)


def run(args):
    details = {}
    if args.command == 'source':
        text = args.path.read_text(encoding='utf-8-sig')
        issues = scan_text(text, args.path.name)
        if args.font:
            issues.extend(check_font(text, args.font, args.font_index))
    else:
        expected = args.expect.read_text(encoding='utf-8-sig').splitlines() if args.expect else []
        issues, details = inspect_pdf(args.path, expected)
    errors = sum(i['level'] == 'error' for i in issues)
    warnings = sum(i['level'] == 'warning' for i in issues)
    status = 'errors' if errors else ('review' if warnings else 'clear')
    report = dict(file=str(args.path), status=status, errors=errors, warnings=warnings,
                  visual_review_required=True, details=details, findings=issues)
    return report, int(bool(errors or (args.warnings_as_errors and warnings)))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='command', required=True)
    for command in ('source', 'pdf'):
        sub = subparsers.add_parser(command)
        sub.add_argument('path', type=Path)
        sub.add_argument('--json', type=Path, dest='json_path')
        sub.add_argument('--warnings-as-errors', action='store_true')
        if command == 'source':
            sub.add_argument('--font', type=Path)
            sub.add_argument('--font-index', type=int, default=0)
        else:
            sub.add_argument('--expect', type=Path)
    args = parser.parse_args(argv)
    try:
        # Never overwrite an input with a report, including through a symlink.
        inputs = [args.path, getattr(args, 'font', None), getattr(args, 'expect', None)]
        if args.json_path and any(p and p.resolve() == args.json_path.resolve() for p in inputs):
            raise ValueError('JSON report must not overwrite an input file.')
        report, exit_code = run(args)
        encoded = json.dumps(report, ensure_ascii=True, indent=2) + '\n'
        if args.json_path:
            args.json_path.parent.mkdir(parents=True, exist_ok=True)
            args.json_path.write_text(encoded, encoding='utf-8')
        print(encoded, end='')
        return exit_code
    except Exception as exc:
        print(json.dumps(dict(status='could_not_check', error=f'{type(exc).__name__}: {exc}'),
                         ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
