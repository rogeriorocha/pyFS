
import os
import PyPDF2
import tempfile

def union(args):
        new_file, userfilename = tempfile.mkstemp()

        # Get all the PDF filenames
        pdf2merge = args

        pdfWriter = PyPDF2.PdfFileWriter()

        print(len(pdf2merge))



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
                try:
                        pdfOutput = open(userfilename, "wb")
                        #Outputting the PDF
                        pdfWriter.write(pdfOutput)
                        

                finally:
                        #Closing the PDF writer
                        pdfOutput.close()
        return userfilename

#union(r"C:\Users\rpsr\Downloads\b.pdf", r"C:\Users\rpsr\Downloads\b.pdf")


#tup1 = (12, 34.56)
#tup1 = tup1 + (5,)
#print(tup1)


from werkzeug.utils import secure_filename
file =secure_filename("C:\\Users\\rpsr\\a.exe")    
print(file)