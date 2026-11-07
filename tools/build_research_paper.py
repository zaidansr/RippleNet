"""Typeset the public aggregate manuscript as a readable research PDF.

Requires ReportLab and pypdf; use the Codex bundled document Python runtime.
No market observations or model-bearing private artifacts are read.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import re
import sys

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/"docs/research-paper.md"
OUTPUT = ROOT/"paper/RippleNet_research_report.pdf"

EQUATIONS = {
    "eq1": '<i>x</i><sub>t</sub> = A<i>x</i><sub>t-1</sub> + <i>w</i><sub>t</sub> + <i>s</i><sub>t</sub>, '
           '   <i>y</i><sub>t</sub> = <i>x</i><sub>t</sub> + <i>v</i><sub>t</sub> + <i>o</i><sub>t</sub>.   (1)',
    "eq2": 'R(<i>g</i> | H) = tr(Q)/n + Σ<sub>z</sub> π<sub>z</sub> tr(A P<sub>z</sub> A<super>T</super>)/n'
           '<br/>+ π<sub>O</sub>π<sub>S</sub> ‖A(<i>m</i><sub>S</sub>-<i>m</i><sub>O</sub>)‖<super>2</super>/n'
           ' + ‖<i>g</i>-A mbar‖<super>2</super>/n.   (2)',
    "eq3": 'E[(F-μ<sub>H</sub>)<super>2</super>] - E[(F-μ<sub>H,U</sub>)<super>2</super>]'
           ' = E[(μ<sub>H,U</sub>-μ<sub>H</sub>)<super>2</super>].   (3)',
    "eq4": 'Y<sub>P</sub>(t,h) = Y<sub>M</sub>(t,h) + g(t+h) - g(t).   (4)',
    "eq7": 'Y<sub>A,k</sub> = log P<sub>k+10</sub> - log P<sub>k</sub>, '
           '  Y<sub>B,k</sub> = log P<sub>k+11</sub> - log P<sub>k+1</sub>.   (5)',
    "eq5": 'Σ<sub>d,i</sub> w<sub>di</sub>(y<sub>di</sub>-b-z<sub>di</sub><super>T</super>β)<super>2</super>'
           ' + α‖β‖<super>2</super>,   w<sub>di</sub> = 1/(D n<sub>d</sub>).   (6)',
    "eq6": 'G = 1 - mean MSE<sub>model</sub> / mean MSE<sub>reference</sub>.   (7)',
}


def fonts() -> None:
    windows = Path("C:/Windows/Fonts")
    if (windows/"times.ttf").exists():
        files = ("times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf")
        base = windows
    else:
        base = Path("/usr/share/fonts/truetype/dejavu")
        files = ("DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf", "DejaVuSerif-Italic.ttf", "DejaVuSerif-BoldItalic.ttf")
    for name, file in zip(("Paper", "Paper-Bold", "Paper-Italic", "Paper-BoldItalic"), files):
        pdfmetrics.registerFont(TTFont(name, str(base/file)))
    pdfmetrics.registerFontFamily("Paper", normal="Paper", bold="Paper-Bold", italic="Paper-Italic", boldItalic="Paper-BoldItalic")
    mono = windows/"consola.ttf"
    if mono.exists():
        pdfmetrics.registerFont(TTFont("Code", str(mono)))
    else:
        pdfmetrics.registerFont(TTFont("Code", str(Path(reportlab.__file__).parent/"fonts/VeraMono.ttf")))


def inline(text: str) -> str:
    links = []
    def link(match: re.Match) -> str:
        label, url = match.group(1), match.group(2)
        links.append(f'<link href="{html.escape(url, quote=True)}" color="#233c55">{html.escape(label)}</link>')
        return f"LINKTOKEN{len(links)-1}END"
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", link, text)
    def bare(match: re.Match) -> str:
        url = match.group(0)
        label = "View repository evidence snapshot" if "github.com/zaidansr" in url else url.removeprefix("https://")
        links.append(f'<link href="{html.escape(url, quote=True)}" color="#233c55">{html.escape(label)}</link>')
        return f"LINKTOKEN{len(links)-1}END"
    text = re.sub(r"https?://[^\s]+", bare, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r'<font name="Code" size="8.8">\1</font>', text)
    for i, value in enumerate(links):
        text = text.replace(f"LINKTOKEN{i}END", value)
    return text


class PaperDocument(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs) -> None:
        super().__init__(filename, **kwargs)
        self.section_count = 0

    def afterFlowable(self, item) -> None:
        if isinstance(item, Paragraph) and item.style.name in ("Section", "Subsection"):
            self.section_count += 1
            key = f"section-{self.section_count}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(item.getPlainText(), key, 0 if item.style.name == "Section" else 1, closed=False)


def build() -> None:
    fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    margin = 48
    body_width = width-2*margin
    doc = PaperDocument(str(OUTPUT), pagesize=A4, leftMargin=margin, rightMargin=margin,
                        topMargin=48, bottomMargin=45, title="Observation Distortions, Market Shocks, and Forecast Value",
                        author="RippleNet research project", subject="Research pilot synthesis and limitations")
    def page(canvas, document) -> None:
        canvas.saveState()
        canvas.setFont("Paper-Italic", 8)
        canvas.setFillColor(colors.HexColor("#333333"))
        canvas.drawString(margin, 24, "RippleNet research report")
        canvas.drawRightString(width-margin, 24, str(document.page))
        canvas.restoreState()
    doc.addPageTemplates(PageTemplate(id="paper", frames=Frame(margin,45,body_width,height-93,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=page))
    styles = {
        "body": ParagraphStyle("Body",fontName="Paper",fontSize=10.5,leading=13.6,alignment=TA_JUSTIFY,spaceAfter=6,allowWidows=0,allowOrphans=0),
        "title": ParagraphStyle("Title",fontName="Paper-Bold",fontSize=20,leading=23,alignment=TA_CENTER,spaceAfter=10),
        "subtitle": ParagraphStyle("Subtitle",fontName="Paper-Italic",fontSize=11,leading=14,alignment=TA_CENTER,spaceAfter=8),
        "meta": ParagraphStyle("Metadata",fontName="Paper",fontSize=9,leading=12,alignment=TA_CENTER,spaceAfter=7),
        "section": ParagraphStyle("Section",fontName="Paper-Bold",fontSize=12.5,leading=16,spaceBefore=12,spaceAfter=6,keepWithNext=True,textColor=colors.black),
        "subsection": ParagraphStyle("Subsection",fontName="Paper-Bold",fontSize=11,leading=14,spaceBefore=9,spaceAfter=5,keepWithNext=True,textColor=colors.black),
        "equation": ParagraphStyle("Equation",fontName="Paper",fontSize=10.5,leading=17,spaceBefore=4,spaceAfter=9,leftIndent=12,rightIndent=4),
        "caption": ParagraphStyle("Caption",fontName="Paper-Italic",fontSize=8.8,leading=11.4,spaceAfter=10),
        "reference": ParagraphStyle("Reference",fontName="Paper",fontSize=9,leading=12,spaceAfter=6,alignment=TA_LEFT,splitLongWords=True),
        "cell": ParagraphStyle("Cell",fontName="Paper",fontSize=8.6,leading=11,alignment=TA_CENTER),
        "cellleft": ParagraphStyle("CellLeft",fontName="Paper",fontSize=8.6,leading=11,alignment=TA_LEFT),
        "head": ParagraphStyle("TableHeader",fontName="Paper-Bold",fontSize=8.6,leading=11,alignment=TA_CENTER,textColor=colors.white),
    }
    source = SOURCE.read_text(encoding="utf-8")
    lines = source.splitlines()
    story, i, table_no = [], 0, 0
    in_refs = False
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]),styles["title"]));i+=1;continue
        if line.startswith("## "):
            title=line[3:];in_refs=title=="References"
            story.append(Paragraph(inline(title),styles["section"]));i+=1;continue
        if line.startswith("### "):
            story.append(Paragraph(inline(line[4:]),styles["subsection"]));i+=1;continue
        if line.startswith("```math"):
            key=lines[i+1].strip().removeprefix("% ")
            story.append(Paragraph(EQUATIONS[key],styles["equation"]))
            i+=1
            while i<len(lines) and lines[i].strip()!="```":i+=1
            i+=1;continue
        if line.startswith("|"):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith("|"):
                parts=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r"[:\- ]+",c) for c in parts):rows.append(parts)
                i+=1
            table_no+=1
            proportions={1:[.45,.25,.30],2:[.30,.28,.42],3:[.46,.27,.27],4:[.34,.20,.20,.26],5:[.14,.20,.25,.20,.21],6:[.28,.20,.26,.26],7:[.23,.23,.24,.30]}
            fractions=proportions[table_no]
            cells=[[Paragraph(inline(c),styles['head' if r==0 else ('cellleft' if col==0 or table_no==7 else 'cell')])for col,c in enumerate(row)]for r,row in enumerate(rows)]
            table=Table(cells,colWidths=[body_width*f for f in fractions],repeatRows=1,hAlign='CENTER')
            commands=[('BACKGROUND',(0,0),(-1,0),colors.HexColor('#333333')),('GRID',(0,0),(-1,-1),.45,colors.HexColor('#D9D9D9')),
                      ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                      ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]
            for row in range(1,len(rows)):
                if row%2==0:commands.append(('BACKGROUND',(0,row),(-1,row),colors.HexColor('#F3F3F3')))
            table.setStyle(TableStyle(commands))
            while i<len(lines) and not lines[i].strip():i+=1
            group=[Spacer(1,5),table,Spacer(1,5)]
            # Keep the appendix heading with its evidence table, including the
            # table spacer; otherwise the spacer consumes keepWithNext.
            if table_no == 7 and isinstance(story[-1], Paragraph):
                group.insert(0, story.pop())
            if i<len(lines) and re.match(r"Table \d+\.",lines[i]):
                group.append(Paragraph(inline(lines[i].strip()),styles['caption']));i+=1
            if table.wrap(body_width,1000)[1]<340:story.append(KeepTogether(group))
            else:story.extend(group)
            continue
        paragraph=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#','|','```')):
            paragraph.append(lines[i].strip());i+=1
        text=' '.join(paragraph)
        style=styles['reference' if in_refs else 'body']
        if text.startswith('*A reproducible'):style=styles['subtitle']
        elif text.startswith('RippleNet research project |') or text.startswith('Research report and manuscript'):style=styles['meta']
        story.append(Paragraph(inline(text),style))
    doc.build(story)
    pdf=PdfReader(str(OUTPUT))
    metadata={'source':'docs/research-paper.md','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'pdf':'paper/RippleNet_research_report.pdf','pdf_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
              'pages':len(pdf.pages),'source_word_count':len(source.split()),'reportlab':reportlab.Version,
              'python':sys.version.split()[0],'format':'A4 single-column research manuscript; embedded serif fonts',
              'contains_new_experiment':False,'restricted_models_or_records_included':False}
    (OUTPUT.parent/'build-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(metadata))


if __name__=='__main__':build()
