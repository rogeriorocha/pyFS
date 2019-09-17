from PyPDF2 import PdfFileWriter, PdfFileReader

#try:
#    from StringIO import StringIO ## for Python 2
#except ImportError:
#from io import StringIO ## for Python 3
import io
 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
#packet = StringIO.StringIO()

#packet = StringIO()
packet = io.BytesIO()
# create a new PDF with Reportlab
c = canvas.Canvas(packet,pagesize=letter)
c.translate(inch,inch)
c.setFont("Helvetica", 78)
#c.setFillColorRGB(1.05, 1.05, 1.05)
c.setFillColorRGB(1, 1, 1)
c.setFillAlpha(0.50)
#c.setStrokeGray(1)

#can.drawString(100,100, "Watermark")
# draw a rectangle
#c.rect(inch,inch,6*inch,9*inch, fill=1)
# make text go straight up
c.rotate(45)
# change color
#c.setFillColorRGB(0,0,0.77)
# say hello (note after rotate the y coord needs to be negative!)
#c.drawString(3*inch, -3*inch, "Hello World")


#c.setFillGray(0.50)
 
#c.drawCentredString(3*inch, -3*inch, "Hello World")
#c.drawCentredString(6 * inch, 1 * inch, "W a t e r m a r k   d e m o")
c.drawCentredString(6 * inch, 1 * inch, "OK")
#c.drawCentredString(35, 190, "Hello World")
c.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(r"C:\Users\rpsr\temp\pythonTest\testWater.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page

for i in range(existing_pdf.getNumPages()):
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file
outputStream = open(r"C:\Users\rpsr\temp\pythonTest\testWater_2.pdf", "wb")
output.write(outputStream)
outputStream.close()