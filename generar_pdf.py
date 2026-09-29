import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors

def markdown_a_pdf(archivo_md, archivo_pdf):
    if not os.path.exists(archivo_md):
        print(f"Error: No se encontró el archivo {archivo_md}")
        return

    doc = SimpleDocTemplate(
        archivo_pdf,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    estilo_nombre = ParagraphStyle(
        'NombreATS',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )

    estilo_contacto = ParagraphStyle(
        'ContactoATS',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#333333")
    )

    estilo_titulo_seccion = ParagraphStyle(
        'TituloSeccionATS',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#000000"),
        spaceBefore=10,
        spaceAfter=4
    )

    estilo_texto = ParagraphStyle(
        'TextoATS',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#222222"),
        spaceAfter=3
    )

    story = []

    with open(archivo_md, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    lineas_limpias = [l.strip() for l in lineas if l.strip()]

    if not lineas_limpias:
        print(f"El archivo {archivo_md} está vacío.")
        return

    story.append(Paragraph(lineas_limpias[0], estilo_nombre))
    if len(lineas_limpias) > 1:
        story.append(Paragraph(lineas_limpias[1], estilo_contacto))
    story.append(Spacer(1, 10))

    for linea in lineas_limpias[2:]:
        if linea.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CCCCCC"), spaceBefore=6, spaceAfter=6))
        elif linea.isupper() and len(linea) < 40:
            story.append(Paragraph(linea, estilo_titulo_seccion))
        else:
            story.append(Paragraph(linea, estilo_texto))

    doc.build(story)
    print(f"✅ PDF generado exitosamente: {archivo_pdf}")

if __name__ == "__main__":
    markdown_a_pdf("cv_maestro.md", "CV_Rosa_Marin_ATS.pdf")
    markdown_a_pdf("cv_santiago.md", "CV_Santiago_ATS.pdf")