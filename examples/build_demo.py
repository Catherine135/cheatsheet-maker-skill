"""Rebuild the source-free demonstration, including editable native Word glyphs."""
from pathlib import Path
from copy import deepcopy
import argparse
import importlib.util
import json
import re

from docx import Document
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "artifact-template-cheatsheet"
NS = {
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
}


def build(output):
    spec = importlib.util.spec_from_file_location("cheatsheet_builder", SKILL / "scripts/build_cheatsheet.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    data = json.loads((ROOT / "examples/style-demo.json").read_text(encoding="utf-8"))
    builder.build(data, output)
    doc = Document(output)
    library = etree.parse(str(SKILL / "assets/inline-er-glyphs.xml"))
    next_id = 10000
    for paragraph in doc.paragraphs:
        match = re.search(r"\[\[glyph:([a-z_]+)\]\]", paragraph.text)
        if not match:
            continue
        label = paragraph.text[:match.start()]
        for run in list(paragraph._p.findall(builder.qn("w:r"))):
            paragraph._p.remove(run)
        builder.add_text(paragraph, label, "body", "approved")
        source = library.find(f"glyph[@name='{match.group(1)}']")
        if source is None:
            raise ValueError(f"Unknown example glyph: {match.group(1)}")
        run = deepcopy(source.find(builder.qn("w:r")))
        for node in run.iter():
            if node.tag in {f"{{{NS['wp']}}}docPr", f"{{{NS['wps']}}}cNvPr"}:
                node.set("id", str(next_id))
                next_id += 1
        paragraph._p.append(run)
        builder.paragraph_mark(paragraph)
    doc.save(output)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "work/style-demo.docx")
    args = parser.parse_args()
    print(build(args.output))
