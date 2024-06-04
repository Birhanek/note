from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime

def file_cropping(start, end, file):
    input_file = PdfFileReader(open(file,'rb'))
    output_file = PdfFileWriter()

    streaming_file = open("note\\" + file.split('.')[0] + "- cropped.pdf", 'wb')

    for page_number in range(start, end + 1):
        page = input_file.getPage(page_number)
        output_file.addPage(page)
        output_file.write(streaming_file)
    streaming_file.close()