# S1 technical manual brief

This is an original fictional equipment concept used to test manual design. It is not a specification, operating instruction, safety assessment, or certification for a real instrument.

## Concept and source facts

The S1 temperature logger has a temperature/session display, a Ready indicator, Start and Stop keys, a sensor input, and a USB host connector. These controls are defined for this example. Start and Stop in the application perform the same session actions as the physical keys. A disconnected sensor must be reconnected before starting a new session.

Use the original sample's demonstration values: temperature range −10 °C to 50 °C, resolution 0.1 °C, stated accuracy ±0.5 °C, interval ≥ 1 s, input resistance 10 kΩ, standby current ≤ 10 µA, and sensor dimensions 20 × 30 mm. The instrument's enclosure is drawn schematically without dimensional or manufacturing claims.

The example session has four readings at 1 s intervals: 10:00:00 = 23.6 °C; 10:00:01 = 23.6 °C; 10:00:02 = 23.7 °C; 10:00:03 = 23.8 °C. The stopped instrument shows the last reading and a count of four. The CSV example contains one heading row and those four data rows. UTF-8 is the export encoding. UI labels remain English in the Chinese summaries.

## Reader and visual direction

Audience: an operator learning to identify controls, connect the system, record a session, and verify the export. The design follows a technical equipment manual direction informed by the [manufacturer study](../DESIGN-REFERENCES.md).

Page format: A4. The main text area runs from 48 to 547 pt. Page types share this grid, typography, blue navigation accent, muted rules, and running section identifiers. Full-width drawings use the same edges as tables; paired content uses a consistent gutter. The setup page uses a narrow prerequisite rail; the overview uses a two-column legend; the export page pairs steps with a file example.

Typography: Calibri regular/bold for English and diagram labels; corresponding regular/bold Chinese faces for each locale; body approximately 10.5-11 pt. Missing technical symbols use explicitly checked Latin fallback runs. Fonts are embedded as subsets.

## Page inventory

1. Document identity, instrument illustration, and linked contents.
2. Annotated instrument overview, six callouts, and matching legend.
3. Sensor/instrument/host connection diagram with numbered actions.
4. Fictional application view and recording procedure.
5. Export steps beside CSV content, then result checks.
6. Specifications and symptom/check/action recovery table.
7. Traditional Chinese quick reference with control illustration.
8. Simplified Chinese quick reference with the same functional layout.

The drawings and schematic interface are native vectors with live text. They are original to this example and use no manufacturer assets. The PDF has internal navigation and bookmarks, but it is not a tagged accessibility example.

## Acceptance checks

Verify all text frames, meaningful symbols, embedded fonts, page bounds, contents links, and bookmark destinations. Inspect all eight rendered pages for hierarchy, diagram/legend agreement, leader routing, text clearance, spacing, and Chinese line breaks. Keep screenshot comparison and extraction checks separate; neither substitutes for the other.
