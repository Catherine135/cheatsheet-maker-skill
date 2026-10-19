# Developer Guide

Most users can invoke the skill directly in Codex. This guide describes manual construction and verification for maintenance and troubleshooting.

## Requirements

Use Python 3.10 or later and the packages listed in the repository's `requirements.txt`. Word construction requires `python-docx` and `lxml`; PDF page-count checks require `pypdf`. Accurate rendering also requires locally licensed Abadi MT Condensed Light and DengXian Light fonts. Font binaries are not distributed.

In supported Codex desktop environments, use the workspace dependency loader's Python interpreter and Documents renderer. Other environments may supply equivalent Python dependencies and a Word-compatible rendering workflow. The builder itself does not call an AI service, access network APIs, or infer content from lecture files.

## Construction

Run the following from the repository root, setting `PYTHON_BIN` to the selected interpreter:

```bash
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/build_cheatsheet.py \
  examples/style-demo.json work/demo.docx
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/audit_cheatsheet.py \
  work/demo.docx --expected-chapters 3
```

Within `code_template`, `{{...}}` marks replaceable gray content; other tokens receive the fixed black code style. Use explicit `code_core` or `identifier_core` runs for selective pale-blue emphasis. The JSON interface is documented in the [Formatting Specification](../skills/artifact-template-cheatsheet/references/formatting.md).

The complete example includes 17 native Word symbol types. Rebuild it with:

```bash
"$PYTHON_BIN" examples/build_demo.py
```

This script writes to `work/` by default and leaves the retained template unchanged. The basic JSON builder produces the text layout; `build_demo.py` additionally replaces the example's symbol markers with editable DrawingML groups.

## Rendering

When Documents tools are available, set `DOCUMENTS_SKILL_DIR` to their actual location:

```bash
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/render_with_fonts.py \
  work/demo.docx --documents-skill-dir "$DOCUMENTS_SKILL_DIR" --outdir work/render
"$PYTHON_BIN" skills/artifact-template-cheatsheet/scripts/audit_cheatsheet.py \
  work/demo.docx --expected-chapters 3 \
  --rendered-pdf work/render/demo.pdf --page-limit 1
```

Without Documents tools, export through Word or another supported renderer, then inspect an image of every page. `render_with_fonts.py` wraps the Documents renderer; it is not a standalone rendering engine. On supported macOS installations, it references existing Word fonts through temporary fontconfig without installing or redistributing them.

## Verification Boundaries

- The audit checks page geometry, type sizes, circled-numeral fields, highlighting, and image placement. It does not validate course coverage or subject accuracy.
- Page counts must come from rendered PDFs rather than DOCX XML.
- Inspect every page for glyph substitutions, code-token boundaries, clipping, arrowheads, and distinguishable double-line gaps. Word and LibreOffice may paginate differently.
- Do not claim exact visual reproduction when required fonts or verification tools are unavailable.
- Keep course sources, answers, generated student documents, fonts, and rendering caches outside the public package. Use an explicit publication file list rather than copying an entire private skill directory.
