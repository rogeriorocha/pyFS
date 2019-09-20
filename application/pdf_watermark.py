from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch

packet = io.BytesIO()
c = canvas.Canvas(packet,pagesize=letter)
c.translate(inch,inch)
c.setFont("Helvetica", 78)

c.setFillColorRGB(0.50, 0.50, 0.50)
c.setFillAlpha(0.50)


c.rotate(45)
c.drawCentredString(6 * inch, 1 * inch, "M I N U T A")

c.save()

packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open(r"C:\Users\rpsr\Documents\python\pyFS\testWater.pdf", "rb"))
output = PdfFileWriter()

for i in range(existing_pdf.getNumPages()):
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
outputStream = open(r"C:\Users\rpsr\Documents\python\pyFS\testWater_out.pdf", "wb")
output.write(outputStream)
outputStream.close()