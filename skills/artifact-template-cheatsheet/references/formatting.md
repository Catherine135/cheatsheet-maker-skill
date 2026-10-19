# Word Formatting Specification

## Page Geometry and Paragraphs

Use one A4 portrait section: `pgSz w=11906 h=16838` twips. All margins are 57 twips; gutter is 0. Retain header and footer distances of 851 and 992 twips without adding visible headers or footers. Use three equal columns, `num=3 space=67`, without column rules. Retain `docGrid type=lines linePitch=312`. Available column width is approximately 194.3 pt.

Text paragraphs and headings use exact 6 pt line spacing: `spacing line=120 lineRule=exact before=0 after=0`. Use left alignment except for centered yellow chapter headings. Use explicit text markers rather than automatic Word lists. Do not add a cover, contents page, decorative borders, or unnecessary blank space.

Set document defaults and Normal explicitly to 6.5 pt. Paragraph marks, soft breaks, spaces, and column breaks must use the appropriate font metrics rather than an inherited 11 pt default. Apply indentation only where needed for code readability. Do not reduce font size or spacing, or change the column count, to meet capacity.

## Typography

- English, numbers, and code: Abadi MT Condensed Light, explicit ascii/hAnsi font, 6.5 pt body. Do not substitute a monospaced code font.
- Optional Chinese annotations and punctuation: DengXian Light, 5.5 pt, bold. The theme's major Hans font must resolve to DengXian Light; runs may use `eastAsiaTheme=majorHAnsi`.
- Chapter headings: 7.5 pt English or 6.5 pt Chinese, bold. Internal English topic and subheading text remains 6.5 pt.
- Ordinary English explanations remain regular weight. Use local black bold terms and red bold conditions rather than carrying heading or code weight into complete paragraphs.
- Circled numerals ①–⑳: 5.5 pt, **not bold**, using the `= n \* GB3` complex Word field. Field boundary runs are also 5.5 pt; cached results use `rFonts hint=eastAsia` and inherit DengXian Light. Clone the actual component rather than substituting bold Unicode. Following English text remains 6.5 pt.

## Semantic Color Roles

Use character-level `w:highlight`, not paragraph shading. Marker characters do not automatically determine heading colors.

- `yellow / FFFF00`: chapter heading, bold black text, centered.
- `cyan / 00FFFF`: internal topic, bold black text.
- `blue / 0000FF`: genuine subheading, bold white text. Ordinary numbered points do not receive blue highlights.
- `black / 000000`: fixed keywords, specific functions, operators, and punctuation; bold white text.
- `lightGray / C0C0C0`: replaceable names, aliases, parameters, values, and appropriate comments or output; regular black English text.
- Text color `95DCF7`: the few tokens that distinguish a method, preserving their original background and weight.
- Text color `EE0000`, bold: decisive properties, conditions, directions, comparisons, and error-prone distinctions. Do not color every technical term.

## Images and Native Shapes

Screenshots use separate `wp:inline` paragraphs with proportional scaling, automatic line height, zero paragraph spacing and indentation, 1 pt image runs and paragraph marks, and zero wrapping distances. Default width is 184 pt and must remain within the column. Never place a full screenshot in an exact 6 pt paragraph.

Native inline symbols remain within the 6 pt body line: overall height 5.2 pt, run size 1 pt, default stroke width 0.40 pt. Preserve visible gaps in double outlines. See [Diagrams and Inline Symbols](inline-notation.md) for component IDs and source-image requirements.

## Builder Input

`paragraphs` are in reading order. An item may contain `role` and `text`, or a `runs` array whose entries contain `text` and `role`. Supported roles: body, major, topic, term, concept, rule, code, code_core, identifier, identifier_core, comment, output, gloss, circle.

- `major` may include `chapter_id` to reject duplicate chapters. Use `topic` for actual topics and `concept` for genuine blue subheadings, not merely because a line starts with a number.
- `rule` applies red bold text; `term` applies black bold text; `body` preserves regular English.
- `code_template` renders `{{...}}` as replaceable gray content and other characters as fixed black code; lines remain together.
- `code_core` retains code background and weight, changing only the text color to `95DCF7`. `identifier_core` does the same for regular gray identifiers.
- `keep_next` and `keep_lines` preserve local units. Use `column_break_before:true` only when requested or necessary for an intact knowledge block, not for every topic.
- `image:{path,width_pt,alt}` inserts an inspected source image with proportional scaling and automatic line height.
- `clone_paragraph` is limited to intentional reuse of components and relationships from the selected reference. Indices from another DOCX are invalid. Do not copy demonstration content or course-specific forced breaks into new output.

```json
{"title":"Example Cheat Sheet","paragraphs":[
  {"role":"major","chapter_id":"one","text":"Chapter 1 Example"},
  {"role":"topic","text":"I. Topic"},
  {"role":"concept","text":"1. A Subtopic"},
  {"runs":[{"role":"body","text":"(1) "},{"role":"term","text":"Term:"},{"role":"body","text":" short definition; "},{"role":"rule","text":"deciding condition"}]},
  {"runs":[{"role":"circle","text":"①"},{"role":"body","text":" Syntax:"}],"keep_next":true},
  {"code_template":"SELECT {{column}} FROM {{table_name}} WHERE {{condition}};"},
  {"runs":[{"role":"circle","text":"②"},{"role":"body","text":" A concise explanation."}]}
]}
```

Examples demonstrate the interface, not required course content. The builder does not replace source-based selection.

## Rendering Limitations

Compare revisions using the same rendering engine. Do not silently substitute unavailable fonts. The rendering helper can reference locally licensed Office fonts through temporary fontconfig without installing or distributing them. Word and LibreOffice may paginate differently; use native Word verification for strict limits when available. XML checks do not replace inspection of every rendered page.
