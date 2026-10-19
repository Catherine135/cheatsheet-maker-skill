"""Render with the Documents packaged renderer and local Office fonts, without installing fonts.

Usage: python render_with_fonts.py file.docx --documents-skill-dir PATH --outdir PATH
"""
from pathlib import Path
import argparse,os,subprocess,sys
from xml.sax.saxutils import escape
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('docx',type=Path);parser.add_argument('--documents-skill-dir',type=Path,required=True)
parser.add_argument('--outdir',type=Path,required=True);args=parser.parse_args()
args.outdir.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
dependencies=Path(sys.executable).resolve().parents[2]
if dependencies.name=='dependencies':
    env['PATH']=str(dependencies/'bin/override')+os.pathsep+str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
    cfg=dependencies/'native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fontconfig/fonts.conf'
    office=Path('/Applications/Microsoft Word.app/Contents/Resources/DFonts')
    if cfg.exists() and office.exists():
        fc=args.outdir/'fonts.conf'
        fc.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><include>'+escape(str(cfg))+'</include><dir>'+escape(str(office))+'</dir><cachedir>'+escape(str(args.outdir.resolve()/'font-cache'))+'</cachedir></fontconfig>')
        env['FONTCONFIG_FILE']=str(fc.resolve())
command=[sys.executable,str(args.documents_skill_dir/'render_docx.py'),str(args.docx.resolve()),'--output_dir',str(args.outdir.resolve()),'--emit_pdf','--dpi','180']
raise SystemExit(subprocess.run(command,env=env).returncode)
