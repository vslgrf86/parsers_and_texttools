# install CB SDK and pytz
!pip install chargebee
!pip install pytz

import chargebee
import json
import gspread
from google.colab import auth
from google.auth import default
from google.colab import drive
from datetime import datetime
import time
import os
import csv
import pytz

# Constants and Configuration
LOG_FOLDER = 'xxx'
SITE = 'xxx'
SITE_API_KEY = 'xxx'
SHEET_URL = 'xxx'
TIMEZONE = pytz.timezone("CET")

# Initialize Chargebee
chargebee.configure(SITE_API_KEY, SITE)


def setup_google_drive():
    """Mount Google Drive and ensure log folder exists."""
    drive.mount('/content/drive')
    try:
        os.makedirs(LOG_FOLDER, exist_ok=True)
        print(f"Log folder verified: {LOG_FOLDER}")
    except Exception as e:
        print(f"Failed to create log folder: {e}")
        raise


def authenticate_google_sheets():
    """Authenticate Google Sheets API and open the spreadsheet."""
    auth.authenticate_user()
    creds, _ = default()
    gc = gspread.authorize(creds)
    try:
        return gc.open_by_url(SHEET_URL)
    except gspread.SpreadsheetNotFound:
        raise FileNotFoundError("Spreadsheet not found. Check the URL or sharing settings.")
    except gspread.exceptions.APIError as e:
        raise RuntimeError(f"API Error: {e}")


def get_data_from_sheet(spreadsheet, sheet_index=1):
    """Retrieve data from the specified worksheet."""
    try:
        worksheet = spreadsheet.get_worksheet(sheet_index)
        data = worksheet.get_all_values()
        return worksheet, data
    except Exception as e:
        raise RuntimeError(f"Error accessing worksheet or data: {e}")


def filter_rows(data, today, date_col_index, identifier_col_index):
    """Filter rows where the date matches and identifier starts with 'IN'."""
    headers = data[0]
    rows = data[1:]
    return [
        (index, row) for index, row in enumerate(rows, start=2)
        if row[date_col_index].strip() == today and row[identifier_col_index].strip().startswith("IN")
    ]


def record_payment(invoice_number, amount):
    """Record payment using Chargebee API."""
    amount_cents = int(float(amount.replace(",", ".")) * 100)
    payment_data = {
        "amount": amount_cents,
        "payment_method" : "BANK_TRANSFER",
        "comment": "Bank transfer recorded via CB API, Gsheets, GColab",
        "date": int(time.time())
    }
    return chargebee.Invoice.record_payment(invoice_number, payment_data)


def log_to_csv(log_filename, successful_payments, failed_payments):
    """Save logs to a CSV file."""
    try:
        with open(log_filename, "w", newline="") as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(["Invoice", "Amount", "Error"])
            for invoice, amount in successful_payments:
                log_writer.writerow([invoice, amount, ""])
            for invoice, amount, error in failed_payments:
                log_writer.writerow([invoice, amount, error])
        print(f"Logs saved to {log_filename}")
    except Exception as e:
        print(f"Error saving logs: {e}")


def process_payments(filtered_rows, worksheet, status_col_index):
    """Process payments and log results."""
    payments_pushed, errors_encountered = 0, 0
    successful_payments, failed_payments = [], []

    for row_index, row in filtered_rows:
        invoice_number = row[identifier_col_index].strip()
        amount = row[amount_col_index].strip()

        try:
            if invoice_number and amount:
                record_payment(invoice_number, amount)
                payments_pushed += 1
                successful_payments.append((invoice_number, amount))
                success_message = f"Success - {datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}"
                worksheet.update_cell(row_index, status_col_index + 1, success_message)
            else:
                print(f"Skipping invalid data: Invoice {invoice_number}, Amount {amount}")
        except Exception as e:
            errors_encountered += 1
            print(f"Error recording payment for Invoice {invoice_number}: {e}")
            failed_payments.append((invoice_number, amount, str(e)))

    return payments_pushed, errors_encountered, successful_payments, failed_payments


def main():
    """Main script execution."""
    try:
        setup_google_drive()
        spreadsheet = authenticate_google_sheets()
        worksheet, data = get_data_from_sheet(spreadsheet)

        today = datetime.now(TIMEZONE).strftime("%d.%m.%Y")
        date_col_index, amount_col_index, identifier_col_index, status_col_index = 13, 17, 19, 26

        filtered_rows = filter_rows(data, today, date_col_index, identifier_col_index)
        print(f"Found {len(filtered_rows)} rows matching today's date and identifier condition.")

        payments_pushed, errors_encountered, successful_payments, failed_payments = process_payments(
            filtered_rows, worksheet, status_col_index)

        print(f"Processing completed. Payments pushed: {payments_pushed}, Errors: {errors_encountered}")

        log_filename = f"{LOG_FOLDER}payment_logs_{datetime.now(TIMEZONE).strftime('%d%m%Y_%H%M%S')}.csv"
        log_to_csv(log_filename, successful_payments, failed_payments)
    except Exception as e:
        print(f"Script encountered an error: {e}")


if __name__ == "__main__":
    main()

"""[API documentation](https://apidocs.chargebee.com/docs/api/invoices?lang=python#record_an_invoice_payment)"""