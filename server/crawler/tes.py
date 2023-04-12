from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

# Abra o arquivo PDF em modo de leitura binária
with open('2023.1.pdf', 'rb') as pdf_file:
    resource_manager = PDFResourceManager()
    output_string = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, output_string, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, converter)
    for page in PDFPage.get_pages(pdf_file, check_extractable=True):
        interpreter.process_page(page)
    text = output_string.getvalue()
    converter.close()
    output_string.close()

# Exiba o texto extraído
print(text)
