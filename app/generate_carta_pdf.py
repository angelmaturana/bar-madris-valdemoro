import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak,
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
carta_path = BASE_DIR / "content" / "carta.json"
site_path = BASE_DIR / "content" / "site.json"
output_path = BASE_DIR / "static" / "carta" / "Carta_Real_Cafe_Madris.pdf"

with open(carta_path, encoding="utf-8") as f:
    carta = json.load(f)
with open(site_path, encoding="utf-8") as f:
    site = json.load(f)

styles = getSampleStyleSheet()

style_h1 = ParagraphStyle(
    "h1",
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    alignment=TA_CENTER,
    spaceAfter=6,
    textColor=colors.HexColor("#e62929"),
)
style_h2 = ParagraphStyle(
    "h2",
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=20,
    alignment=TA_LEFT,
    spaceBefore=18,
    spaceAfter=6,
    textColor=colors.HexColor("#11100d"),
    borderBottomPadding=4,
    borderPadding=0,
)
style_h3 = ParagraphStyle(
    "h3",
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=15,
    alignment=TA_LEFT,
    spaceBefore=14,
    spaceAfter=4,
    textColor=colors.HexColor("#11100d"),
)
style_eslogan = ParagraphStyle(
    "eslogan",
    fontName="Helvetica-Oblique",
    fontSize=11,
    alignment=TA_CENTER,
    spaceAfter=14,
    textColor=colors.HexColor("#999999"),
)
style_dir = ParagraphStyle(
    "dir",
    fontName="Helvetica",
    fontSize=9,
    alignment=TA_CENTER,
    spaceAfter=20,
    textColor=colors.HexColor("#666666"),
)
style_item_name = ParagraphStyle(
    "item_name",
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=12,
    alignment=TA_LEFT,
    spaceAfter=0,
    textColor=colors.HexColor("#11100d"),
)
style_item_detail = ParagraphStyle(
    "item_detail",
    fontName="Helvetica-Oblique",
    fontSize=8,
    leading=10,
    alignment=TA_LEFT,
    spaceAfter=0,
    textColor=colors.HexColor("#555555"),
    leftIndent=6,
)
style_item_price = ParagraphStyle(
    "item_price",
    fontName="Helvetica",
    fontSize=9.5,
    leading=12,
    alignment=TA_RIGHT,
    spaceAfter=0,
    textColor=colors.HexColor("#e62929"),
)
style_allergen = ParagraphStyle(
    "allergen",
    fontName="Helvetica",
    fontSize=7.5,
    alignment=TA_CENTER,
    spaceBefore=8,
    spaceAfter=20,
    textColor=colors.HexColor("#666666"),
)

doc = SimpleDocTemplate(
    str(output_path),
    pagesize=A4,
    leftMargin=18 * mm,
    rightMargin=18 * mm,
    topMargin=16 * mm,
    bottomMargin=16 * mm,
)

flow = []


def fmt_price(p):
    return f"{p:.2f} €"


def fmt_bocata(pb, pm):
    return f"{pb:.2f} € / {pm:.2f} €"


# ---- Header ----
flow.append(Paragraph("Bar Madris", style_h1))
flow.append(Paragraph(f"<i>{carta['restaurante']['eslogan']}</i>", style_eslogan))
addr = carta["restaurante"]["direccion"]
phone = site["site"].get("phone", "")
flow.append(Paragraph(f"{addr}  ·  Tlf: {phone}", style_dir))

# ---- secciones ----
sec_labels = {
    "hamburguesas": "HAMBURGUESAS",
    "sandwich": "SÁNDWICH",
    "tostas": "TOSTAS",
    "raciones": "RACIÓNES",
    "platos_combinados": "PLATOS COMBINADOS",
    "huevos_rotos": "HUEVOS ROTOS",
    "bocatas": "BOCATAS",
    "paleto": "PALETO",
}

for sec_name, sec_data in carta["secciones"].items():
    label = sec_labels.get(sec_name, sec_name.replace("_", " ").title())
    items = sec_data if isinstance(sec_data, list) else sec_data.get("items", [])

    if sec_name == "bocatas":
        flow.append(Paragraph(label, style_h3))
        data = [["Producto", "Precio"]]
        for it in items:
            data.append([it["nombre"], fmt_bocata(it["precio_bocadillo"], it["precio_montado"])])
        table = Table(data, colWidths=[60 * mm, 30 * mm])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
        ]))
        flow.append(table)
    elif sec_name == "paleto":
        flow.append(Paragraph(label, style_h3))
        for it in items:
            flow.append(Paragraph(f"{it['nombre']}  —  {fmt_price(it['precio'])}", style_item_name))
            if it.get("detalle"):
                flow.append(Paragraph(it["detalle"], style_item_detail))
            flow.append(Spacer(1, 3))
    else:
        flow.append(Paragraph(label, style_h3))
        data = [["Producto", "Precio"]]
        for it in items:
            row = [it["nombre"], fmt_price(it["precio"])]
            data.append(row)
        table = Table(data, colWidths=[90 * mm, 30 * mm])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
        ]))
        flow.append(table)

    flow.append(Spacer(1, 6))

# Allergen note
legend = carta.get("leyenda_alergenos", {})
if legend:
    leyenda_str = "  ·  ".join(f"{k}: {v}" for k, v in legend.items())
    flow.append(Paragraph(f"Alérgenos: {leyenda_str}", style_allergen))

doc.build(flow)
print(f"PDF generated: {output_path}")
