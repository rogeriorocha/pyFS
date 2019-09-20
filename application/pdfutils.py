import os
import PyPDF2
import tempfile

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch


def union(lst):
        _, userfilename = tempfile.mkstemp()

        # Get all the PDF filenames
        pdf2merge = lst
        pdfWriter = PyPDF2.PdfFileWriter()
        #loop through all PDFs
        for filename in list(pdf2merge):
                #rb for read binary
                pdfFileObj = open(filename,'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                #Opening each page of the PDF
                for pageNum in range(pdfReader.numPages):
                        pageObj = pdfReader.getPage(pageNum)
                        pdfWriter.addPage(pageObj)

        print(len(pdf2merge))
        if len(pdf2merge) > 0:
                #save PDF to file, wb for write binary
                pdfOutput = open(userfilename, "wb")
                try:
                        #Outputting the PDF
                        pdfWriter.write(pdfOutput)
                finally:
                        #Closing the PDF writer
                        pdfOutput.close()
        return userfilename

def watermark(filename, texto):

        packet = io.BytesIO()
        c = canvas.Canvas(packet,pagesize=letter)
        c.translate(inch,inch)
        c.setFont("Helvetica", 78)

        c.setFillColorRGB(0.50, 0.50, 0.50)
        c.setFillAlpha(0.50)

        c.rotate(45)
        c.drawCentredString(6 * inch, 1 * inch, texto)

        c.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        filePdf= open(filename, "rb")
        try:
                existing_pdf = PdfFileReader(filePdf)
                output = PdfFileWriter()

                for i in range(existing_pdf.getNumPages()):
                        page = existing_pdf.getPage(i)
                        page.mergePage(new_pdf.getPage(0))
                        output.addPage(page)
                _, userfilename = tempfile.mkstemp()       
                outputStream = open(userfilename, "wb")
                try:
                        output.write(outputStream)
                finally:        
                        outputStream.close()
        finally:
                filePdf.close()
                pass

        return userfilename        
#print(watermark(r"C:\Users\rpsr\Documents\python\pyFS\testWater.pdf", "GO"))