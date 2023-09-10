import os
import email
import openpyxl
import html2text

# Function to parse an .eml file and extract relevant information
def parse_eml(eml_file):
    with open(eml_file, "r", encoding="utf-8") as eml_data:
        msg = email.message_from_file(eml_data)
        sender = msg["From"]
        subject = msg["Subject"]
        date = msg["Date"]
        body = ""

        # Extract the email body, which may be multipart or plain text
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload is not None:
                        if content_type == "text/html":
                            # Convert HTML to plain text
                            text_converter = html2text.HTML2Text()
                            payload_text = text_converter.handle(payload.decode("utf-8", errors="ignore"))
                            body += payload_text
                        else:
                            body += payload.decode("utf-8", errors="ignore")
        else:
            payload = msg.get_payload(decode=True)
            if payload is not None:
                body = payload.decode("utf-8", errors="ignore")

    return sender, subject, date, body

# Function to write email data to an Excel file
def write_to_excel(eml_files, output_file):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write headers
    headers = ["Sender", "Subject", "Date", "Body"]
    worksheet.append(headers)

    for eml_file in eml_files:
        sender, subject, date, body = parse_eml(eml_file)
        worksheet.append([sender, subject, date, body])

    workbook.save(output_file)

if __name__ == "__main__":
    eml_folder = r"C:\Users\v.garyfallos\Downloads\eml"  # Replace with the path to your .eml files folder
    output_excel = r"C:\Users\v.garyfallos\Downloads\eml\output.xlsx"       # Replace with the desired output Excel file name

    eml_files = [os.path.join(eml_folder, file) for file in os.listdir(eml_folder) if file.endswith(".eml")]

    if eml_files:
        write_to_excel(eml_files, output_excel)
        print("Data has been written to", output_excel)
    else:
        print("No .eml files found in the specified folder.")
