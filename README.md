# pdf.py
A simple .pdf parser. It parses text from .pdf files and writes it into .xlsx files.

dependencies: openpyxl, pyPDF2


# eml_parser
A simple .eml parser. It parses text from downloaded emails and writes it into .xlsx files.

dependencies: os, email, openpyxl, html2text


# py_html_to_docx_parser
A simple py parser. It copies text from webpages and writes it into .docx files.

dependencies: requests, BeautifulSoup, docx


# text_to_py_list
It splits a text input into py list items by word

dependencies: nltk


# py_merge_multiple_csv_files.py
it merges multiple .csv files into one based on a name convention

# NLTK_Churn
analysing churn trends from customer feedback

dependencies: nltk

# Sankey P&L
a Sankey P&L chart

dependencies: plotly

![alt text](https://github.com/vslgrf86/py_everyday_toolkit/blob/main/plot.png?raw=true)
![alt text](https://github.com/vslgrf86/py_everyday_toolkit/blob/main/plot2.png?raw=true)


# bank_clearings.py

Here’s a description you can use for your Google Sheet in the context of the GitHub repository:

---

### Google Sheet Overview

The Google Sheet serves as a centralized data source for recording and managing bank clearing payments. It is integrated with the Python script to automate the process of recording payments in Chargebee. Below is a description of the sheet's structure and usage:

#### Sheet Structure

| Column | Name/Description                    | Example Values        |
|--------|-------------------------------------|-----------------------|
| A-Z    | (Various columns)                  | (Data irrelevant to the script) |
| M      | **Date**                            | `dd.mm.yyyy` (e.g., `11.12.2024`) |
| Q      | **Amount**                          | `123.45` or `1,234.56` |
| S      | **Invoice Identifier**              | `IN016692`, `IN016693` |
| Z      | **Status**                          | Empty or logs processing status |

#### Key Columns Referenced by the Script:
- **Date Column (Index 13 / Column M)**: Contains the date for filtering rows based on the current date.
- **Amount Column (Index 17 / Column Q)**: Holds the payment amounts.
- **Invoice Identifier Column (Index 19 / Column S)**: Includes unique invoice numbers starting with `IN`.
- **Status Column (Index 26 / Column Z)**: Updated by the script to reflect the payment processing status (e.g., "Success" or error details).

#### Usage
1. **Input Data**:
   - Populate the sheet with invoice data, ensuring the **Date**, **Amount**, and **Invoice Identifier** columns are filled.
   - Only rows matching the current date and invoice identifier conditions will be processed by the script.

2. **Automated Processing**:
   - The script reads the sheet, filters rows based on today's date and identifiers starting with "IN," and processes the payments via the Chargebee API.
   - Status updates (e.g., "Success" or error details) are logged directly in the **Status Column**.

3. **Logs**:
   - A detailed log of successful and failed payments is saved as a CSV file in the specified directory within Google Drive.
