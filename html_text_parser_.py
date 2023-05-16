import requests
from bs4 import BeautifulSoup
from docx import Document

# URL of the HTML page you want to scrape

url = ""

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(response.content, "html.parser")

# Find all text elements in the HTML
text_elements = soup.find_all(text=True)

# Filter out unwanted elements, such as scripts and styles
filtered_text = [element.strip() for element in text_elements if element.parent.name not in ["script", "style"]]

# Create a new Word document
document = Document()

# Add the extracted text to the Word document
for text in filtered_text:
    document.add_paragraph(text)

# Save the Word document
document.save("scraped_text.docx")
