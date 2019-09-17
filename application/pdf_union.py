
#geektechstuff
#Python script to merge multiple PDF files into one PDF

#Requires the “PyPDF2” and “OS” modules to be imported
import os, PyPDF2


userpdflocation=r"C:\Users\rpsr\temp\pythonTest";
os.chdir(userpdflocation)
userfilename=r"union"

# Get all the PDF filenames
pdf2merge = []
for filename in os.listdir('.'):
    if filename.endswith('.pdf'):
       print("=== "+filename)   
       pdf2merge.append(filename)

pdfWriter = PyPDF2.PdfFileWriter()

#loop through all PDFs
for filename in pdf2merge:
#rb for read binary
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#Opening each page of the PDF
    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

print(len(pdf2merge))
#save PDF to file, wb for write binary
try:
        pdfOutput = open(userfilename+".pdf", "wb")
        #Outputting the PDF
        pdfWriter.write(pdfOutput)
finally:
        #Closing the PDF writer
        pdfOutput.close()