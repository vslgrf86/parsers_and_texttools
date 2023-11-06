import PyPDF2
import openpyxl

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_filename):
    text = ""
    with open(pdf_filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to save text to an XLSX file
def save_text_to_xlsx(text, xlsx_filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    lines = text.split('\n')
    for row_num, line in enumerate(lines, start=1):
        sheet.cell(row=row_num, column=1, value=line)
    workbook.save(xlsx_filename)

# Example usage
pdf_filename = 'q1kontoauszug.pdf'  # Replace with your PDF file
xlsx_filename = 'pdf.xlsx'  # Replace with the desired output XLSX file

extracted_text = extract_text_from_pdf(pdf_filename)
save_text_to_xlsx(extracted_text, xlsx_filename)

print(f"Text extracted from {pdf_filename} and saved to {xlsx_filename}.")
