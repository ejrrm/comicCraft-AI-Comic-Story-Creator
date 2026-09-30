from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from app.config import EXPORTS_DIR

def _safe(text):
    return str(text).encode("latin-1","replace").decode("latin-1")

def _lines(text, width=95):
    s=_safe(text)
    words=s.split()
    lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1 <= width:
            cur=(cur+" "+w).strip()
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines or [""]

def _write(pdf, text, bold=False, italic=False):
    style=("B" if bold else "")+("I" if italic else "")
    pdf.set_font("Helvetica",style,10)
    for line in _lines(text):
        pdf.cell(190,6,line,ln=1)

def save_pdf(layout):
    path=EXPORTS_DIR/f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    pdf=FPDF(format="A4")
    pdf.set_margins(10,10,10)
    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica","B",16)
        title=_safe(f"Panel {panel['panel']}: {panel['title']}")
        pdf.cell(190,9,title,ln=1)
        image_path=Path(panel["image_path"])
        if image_path.exists():
            pdf.image(str(image_path),x=10,y=25,w=190,h=100)
        pdf.set_y(130)
        _write(pdf,panel["scene_description"],italic=True)
        pdf.ln(2)
        _write(pdf,"Caption: "+panel["caption"],bold=True)
        pdf.ln(1)
        _write(pdf,"Narration: "+panel["narration"])
    pdf.output(str(path))
    return path
