"""Check personal cheatsheet geometry, semantic styling, images and optional page limit."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as ET
from copy import deepcopy
import argparse,json,re

N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
   'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
   'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture',
   'wpg':'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
   'wps':'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'}
W='{'+N['w']+'}'
ROOT=Path(__file__).resolve().parents[1]
CJK=r'[\u3400-\u9fff\u3000-\u303f\uff01-\uff60\uffe0-\uffe6]'

def value(run,name):
    el=run.find('w:rPr/w:'+name,N)
    return None if el is None else el.get(W+'val','1')

def merge_properties(parts,tag):
    out=ET.Element(W+tag)
    for part in parts:
        if part is None:continue
        for child in part:
            previous=out.find(child.tag)
            if previous is None:out.append(deepcopy(child))
            elif child.tag in {W+'rFonts',W+'spacing',W+'lang'}:previous.attrib.update(child.attrib)
            else:out.replace(previous,deepcopy(child))
    return out

class Formatting:
    def __init__(self,styles):
        self.styles={x.get(W+'styleId'):x for x in styles.findall('w:style',N)}
        self.normal=next((k for k,s in self.styles.items() if s.get(W+'type')=='paragraph' and s.get(W+'default')=='1'),'a')
        self.rdefault=styles.find('w:docDefaults/w:rPrDefault/w:rPr',N)
        self.pdefault=styles.find('w:docDefaults/w:pPrDefault/w:pPr',N)
    def chain(self,key,seen=None):
        seen=set() if seen is None else seen
        if key in seen or key not in self.styles:return []
        seen.add(key);style=self.styles[key];base=style.find('w:basedOn',N)
        return (self.chain(base.get(W+'val'),seen) if base is not None else [])+[style]
    def paragraph_styles(self,p):
        style=p.find('w:pPr/w:pStyle',N)
        return self.chain(style.get(W+'val') if style is not None else self.normal)
    def run(self,run,p):
        char=run.find('w:rPr/w:rStyle',N)
        styles=self.paragraph_styles(p)+(self.chain(char.get(W+'val')) if char is not None else [])
        parts=[self.rdefault]+[s.find('w:rPr',N) for s in styles]+[run.find('w:rPr',N)]
        result=ET.Element(W+'r');result.append(merge_properties(parts,'rPr'));return result
    def paragraph(self,p):
        return merge_properties([self.pdefault]+[s.find('w:pPr',N) for s in self.paragraph_styles(p)]+[p.find('w:pPr',N)],'pPr')

def field_instructions(root):
    stack=[];result={}
    for run in root.findall('.//w:r',N):
        for child in run:
            if child.tag==W+'fldChar':
                typ=child.get(W+'fldCharType')
                if typ=='begin':stack.append({'instruction':'','separated':False})
                elif typ=='separate' and stack:stack[-1]['separated']=True
                elif typ=='end' and stack:stack.pop()
            elif child.tag==W+'instrText' and stack:stack[-1]['instruction']+=child.text or ''
            elif child.tag==W+'t' and stack and stack[-1]['separated']:result[run]=stack[-1]['instruction']
    return result

def check(path,expected_chapters=None,rendered_pdf=None,page_limit=None):
    errors=[];warnings=[];titles=[];chapter_keys=set()
    counts=dict(english_regular=0,english_bold=0,red_bold=0,fixed_code=0,gray_code_or_output=0,images=0,inline_shapes=0,circles=0)
    with ZipFile(path) as z,ZipFile(ROOT/'assets/reference.docx') as ref:
        root=ET.fromstring(z.read('word/document.xml'));baseline=ET.fromstring(ref.read('word/document.xml'))
        fmt=Formatting(ET.fromstring(z.read('word/styles.xml')));fields=field_instructions(root)
        sections=root.findall('.//w:sectPr',N);base=baseline.find('.//w:sectPr',N)
        if len(sections)!=1:errors.append('Expected one three-column section')
        for sec in sections:
            for name in ['pgSz','pgMar','cols','docGrid']:
                actual=sec.find('w:'+name,N);expected=base.find('w:'+name,N)
                if actual is None or dict(actual.attrib)!=dict(expected.attrib):errors.append('Geometry changed: '+name)
        size=base.find('w:pgSz',N);margin=base.find('w:pgMar',N);cols=base.find('w:cols',N)
        column_twips=(int(size.get(W+'w'))-int(margin.get(W+'left'))-int(margin.get(W+'right'))
                      -int(cols.get(W+'space'))*(int(cols.get(W+'num'))-1))/int(cols.get(W+'num'))
        for i,p in enumerate(root.findall('.//w:body//w:p',N)):
            sp=fmt.paragraph(p).find('w:spacing',N);has_image=p.find('.//pic:pic',N) is not None
            for drawing in p.findall('.//w:drawing',N):
                if drawing.find('.//wpg:wgp',N) is None and drawing.find('.//wps:wsp',N) is None:continue
                counts['inline_shapes']+=1
                if drawing.find('wp:anchor',N) is not None:errors.append(f'P{i}: notation shape must be inline')
                ext=drawing.find('wp:inline/wp:extent',N)
                if ext is None:errors.append(f'P{i}: notation shape needs an inline extent')
                elif int(ext.get('cy'))>6*12700 or int(ext.get('cx'))>column_twips*635:
                    errors.append(f'P{i}: notation shape exceeds its one-line/column bounds')
            if has_image:
                counts['images']+=1
                if sp is None or sp.get(W+'lineRule','auto')!='auto':errors.append(f'P{i}: image needs automatic line height')
                if p.find('.//wp:anchor',N) is not None:errors.append(f'P{i}: floating image needs inline placement')
                for ext in p.findall('.//wp:inline/wp:extent',N):
                    if int(ext.get('cx'))>column_twips*635:errors.append(f'P{i}: image exceeds column width')
            elif sp is None or sp.get(W+'line')!='120' or sp.get(W+'lineRule')!='exact' or sp.get(W+'after','0')!='0' or sp.get(W+'before','0')!='0':
                errors.append(f'P{i}: expected fixed 6 pt text line and zero after spacing')
            if p.xpath('.//w:highlight[@w:val="yellow"]',namespaces=N):
                title=''.join(p.xpath('.//w:t/text()',namespaces=N)).strip();titles.append(title)
                match=re.search(r'\bchapter\s*(\d+)',title,re.I)
                key=match.group(1) if match else title.casefold()
                if key in chapter_keys:errors.append(f'P{i}: repeated chapter title {title}')
                chapter_keys.add(key)
            visible_sizes=[]
            for actual_run in p.findall('.//w:r',N):
                run=fmt.run(actual_run,p)
                text=''.join(actual_run.xpath('.//w:t/text()',namespaces=N))
                if actual_run.find('w:br',N) is not None and value(run,'sz') not in {'11','13','15'}:
                    errors.append(f'P{i}: break inherited an oversized/unsupported font')
                if not text.strip():continue
                size=value(run,'sz');high=value(run,'highlight');color=value(run,'color')
                if size and size.isdigit():visible_sizes.append(int(size))
                bold=value(run,'b') not in {None,'0','false','off'}
                font=run.find('w:rPr/w:rFonts',N)
                if size not in {'11','13','15'}:warnings.append(f'P{i}: incidental/unsupported font size {size}')
                circles=[ch for ch in text if '①'<=ch<='⑳']
                if circles:
                    counts['circles']+=len(circles)
                    if size!='11':errors.append(f'P{i}: circled numeral is not 5.5 pt')
                    if bold:errors.append(f'P{i}: circled numeral must not be bold')
                    if font is None or font.get(W+'hint')!='eastAsia':errors.append(f'P{i}: circled numeral needs the sample eastAsia glyph hint')
                    instruction=fields.get(actual_run,'')
                    match=re.fullmatch(r'\s*=\s*(\d+)\s+\\\*\s+GB3\s*',instruction)
                    if len(text)!=1 or not match or int(match.group(1))!=ord(text[0])-ord('①')+1:
                        errors.append(f'P{i}: use the approved GB3 field, not plain circled Unicode')
                    if high:errors.append(f'P{i}: circled numeral must not inherit heading/code highlight')
                if high=='blue' and color!='FFFFFF':errors.append(f'P{i}: blue heading highlight needs white text')
                if high=='black' and color not in {'FFFFFF','95DCF7'}:errors.append(f'P{i}: fixed code needs white or approved pale-blue core text')
                if high=='black':
                    counts['fixed_code']+=len(text)
                    if not bold:errors.append(f'P{i}: fixed code must be bold')
                if high=='lightGray':
                    counts['gray_code_or_output']+=len(text)
                    if color not in {'000000','95DCF7'}:errors.append(f'P{i}: gray variable/output needs black or approved pale-blue core text')
                    if bold and re.search('[A-Za-z]',text):errors.append(f'P{i}: gray English identifiers should be regular weight')
                if color in {'EE0000','FF0000'}:
                    counts['red_bold']+=len(text)
                    if not bold:errors.append(f'P{i}: red emphasis must also be bold')
                circle=bool(text) and all('①'<=ch<='⑳' for ch in text)
                chinese=bool(re.fullmatch(CJK+'+',text))
                if chinese:
                    if size!=('13' if high=='yellow' else '11'):errors.append(f'P{i}: Chinese text/punctuation has the wrong size')
                    if not bold:errors.append(f'P{i}: Chinese text/punctuation must be bold')
                if high=='yellow' and not circle and size!=('13' if chinese else '15'):
                    errors.append(f'P{i}: chapter title needs +1 pt from language baseline')
                if not high and color in {'000000',None} and size=='13':
                    counts['english_bold' if bold else 'english_regular']+=len(re.findall('[A-Za-z]',text))
                if font is not None and font.get(W+'ascii') not in {None,'Abadi MT Condensed Light','Cambria Math','Arial','Calibri','Calibri Light','Times New Roman'}:
                    warnings.append(f'P{i}: check intentional fallback font')
            marker=ET.Element(W+'r')
            mark=p.find('w:pPr/w:rPr',N)
            if mark is not None:marker.append(deepcopy(mark))
            marker_size=value(fmt.run(marker,p),'sz')
            allowed=2 if has_image else max([13]+visible_sizes)
            if marker_size and marker_size.isdigit() and int(marker_size)>allowed:
                errors.append(f'P{i}: paragraph mark is larger than the text/image anchor')
    if expected_chapters is not None and len(titles)!=expected_chapters:
        errors.append(f'Expected {expected_chapters} chapter titles, found {len(titles)}')
    letters=counts['english_regular']+counts['english_bold']
    if letters>200 and counts['english_bold']/letters>0.7:warnings.append('Most ordinary English is bold; check against regular body style')
    if counts['fixed_code']>100 and not counts['gray_code_or_output']:warnings.append('Code has no gray identifiers; check fixed/variable token distinction')
    if letters>500 and not counts['red_bold']:warnings.append('No red bold emphasis; review discriminating terms and error conditions')
    pages=None
    if page_limit is not None and rendered_pdf is None:errors.append('page-limit needs a rendered PDF; OOXML cannot prove page count')
    if rendered_pdf is not None:
        from pypdf import PdfReader
        pages=len(PdfReader(rendered_pdf).pages)
        if page_limit is not None and pages>page_limit:errors.append(f'Rendered {pages} pages exceeds limit {page_limit}')
    return {'errors':errors,'warnings':warnings,'chapter_titles':titles,'counts':counts,'rendered_pages':pages,'passed':not errors}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docx',type=Path);parser.add_argument('--expected-chapters',type=int)
    parser.add_argument('--rendered-pdf',type=Path);parser.add_argument('--page-limit',type=int)
    args=parser.parse_args()
    result=check(args.docx,args.expected_chapters,args.rendered_pdf,args.page_limit)
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['passed'] else 1)
