# Diagrams and Inline Symbols

## Three Distinct Uses

- **Overview:** when shapes or line patterns are examinable, retain the source's complete symbol-to-name overview. Names alone or approximate redrawings are insufficient.
- **Drawing instructions:** supplement specific references to rectangles, ellipses, or double lines with native Word shapes and necessary connectors beside the explanation. Keep the group within the body line.
- **Complete examples:** when multiple connections, directions, roles, or labels determine meaning, use the original example crop and explain its specific elements. Editability does not justify replacing a complex diagram with an inaccurate sketch.

Notation is not always an independent shape. Role names may be written directly on the relevant lines. Explain this general representation before discussing the example's labels, arrows, cardinalities, and participation constraints. Do not substitute an unlabeled loop or generalize one example's constraints to every relationship.

Crops must preserve relevant entities, attributes, connectors, arrowheads, double lines, dashes, and labels. Use proportional inline placement in a separate automatic-height paragraph, normally 184 pt wide and always within the column. Image runs and paragraph marks are 1 pt with zero indentation and paragraph spacing. Full screenshots are not subject to the one-line height limit.

## Inline Component Requirements

- Overall native group height: **5.2 pt / 66040 EMU** within a fixed 6 pt line. Shape run: 1 pt. The bound applies to the entire group, including connectors.
- Default stroke: **0.40 pt / 5080 EMU**, verified as a moderate increase from 0.32 pt. Preserve dimensions and inspect double rectangles, double diamonds, double ellipses, composite connectors, dashes, and arrowheads. If gaps merge, adjust locally and render again rather than increasing all strokes.
- Use `wp:inline`, no floating anchors or wrapping distances, and a width within the column. Preserve line patterns, directions, and proportions. Where `mc:AlternateContent` exists, check DrawingML strokes and VML fallback strokes together.
- Distinguish native shapes from `pic:pic` images. Not every `w:drawing` requires automatic paragraph height.

## Reusable Library

`assets/inline-er-glyphs.xml` contains 17 native components: entity, attribute, relationship, one, many, total, partial, key, weak, identifying, discriminator, isa, isa_total, isa_partial, composite, multivalued, and derived. It contains no screenshots, course text, or generic Role sketch.

Each `glyph` contains a deep-copyable `w:r` with native DrawingML and no media relationship. Allocate unique `wp:docPr/@id`, `wps:cNvPr/@id`, and other applicable drawing IDs on insertion. Select notation from the actual course source rather than treating this ER library as a universal standard. Word may create VML or internal previews when saving; do not insert fallback previews as duplicate images.

Inspect surrounding text and symbol clarity on every rendered page. Use enlarged comparisons for complex groups. Where needed, inspect the document in native Word to confirm the components remain editable groups without changing line height or obscuring text.
