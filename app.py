


import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os
from num2words import num2words
from email.utils import formataddr
import re
import tempfile
import pandas as pd
from num2words import num2words
from tkinter import messagebox
from pathlib import Path
# Email credentials
SENDER_EMAIL ='bysreceipts75@gmail.com'
EMAIL_PASSWORD ='cotz ghvy njhq htlh'

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os
import inflect
import sys
# Function to convert amount to words
import inflect
def convert_number_to_words(amount):
    p = inflect.engine()
    if amount.is_integer():
        words = p.number_to_words(int(amount))
    else:
        words = p.number_to_words(amount)
    return ' '.join([word.capitalize() for word in words.split()])


def resource_path(relative_path):
    """Get the absolute path to the resource (sign.jpg, stamp.jpg), handling PyInstaller's _MEIPASS."""
    if getattr(sys, 'frozen', False):
        # When running as a bundled executable
        base_path = sys._MEIPASS
    else:
        # When running as a script
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# Example usage in your code
signature_path = resource_path("sign.jpg")
stamp_path = resource_path("stamp.jpg")
# Generate receipt function
def generate_receipt(data, output_path):
    data['Amount_in_words'] = convert_number_to_words(data['Amount'])
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    top_y = height - 1 * inch  # Top starting point

    # Draw outer border
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(1 * inch, height - 10 * inch, 6.5 * inch, 9 * inch)

    # Title Section
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, top_y - 0.5 * inch, "BOMBAY YOGAKSHEMA SABHA (Regd.)")

    # Sub-header and contact details
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, top_y - 0.8 * inch, "(Reg. Under the Society's Reg. Act 1960 No. 26/76 G.B.B.S.D. Bombay)")
    c.drawCentredString(width / 2, top_y - 1.0 * inch, "(Reg. Under the Bombay Public Trust Act 1950 No. F3873 Bombay)")
    c.line(1 * inch, top_y - 1.2 * inch, 7.5 * inch, top_y - 1.2 * inch)

    # Admin Office Information and PAN
    c.drawCentredString(width / 2, top_y - 1.5 * inch, "Admn. Office : G-2, Nav Haridarshan CHS. Ltd., Jai Hind Colony, G. Gupte Road,")
    c.drawCentredString(width / 2, top_y - 1.7 * inch, "Dombivli (West) 421 201")
    c.drawCentredString(width / 2, top_y - 1.9 * inch, "(I.T. Exemption No. THN/ CIT-I/Tech-I/80 G/389/2007-08/3031)")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, top_y - 2.4 * inch, "PAN No. AAAAB4113E")

    # Receipt Details
    c.setFont("Helvetica", 10)
    c.drawString(1.2 * inch, top_y - 2.8 * inch, f"Receipt No. {data['Receipt_No']}")
    c.drawRightString(7.3 * inch, top_y - 2.8 * inch, f"Date: {data['Date']}")

    # # Left-aligned "Received with thanks from"
    # c.drawString(1.2 * inch, top_y - 3.2 * inch, f"Received with thanks from Mr. / Mrs. / M/s. {data['Name']}")
    # Set font to regular for the first part
    c.setFont("Helvetica", 12)  # Regular font
    text_regular = "Received with thanks from Mr. / Mrs. / M/s. "
    c.drawString(1.2 * inch, top_y - 3.2 * inch, text_regular)

    # Switch to bold font for the Name
    c.setFont("Helvetica-Bold", 12)  # Bold font
    name_x = 1.2 * inch + c.stringWidth(text_regular, "Helvetica", 12)  # Calculate where the name should start
    c.drawString(name_x, top_y - 3.2 * inch, data['Name'])

    # # Bold Amount in Words
    # c.setFont("Helvetica-Bold", 10)
    # c.drawString(1.2 * inch, top_y - 3.6 * inch, f"the sum of : Rupees {data['Amount_in_words']} only")
    # Regular text (non-bold)
    # Regular text (non-bold) before "Rupees"
    c.setFont("Helvetica", 10)  # Regular font
    text_regular = "the sum of : "
    c.drawString(1.2 * inch, top_y - 3.6 * inch, text_regular)

    # Bold "Rupees {Amount_in_words} only"
    c.setFont("Helvetica-Bold", 10)  # Bold font
    amount_in_words = f"Rupees {data['Amount_in_words']} only"
    amount_x = 1.2 * inch + c.stringWidth(text_regular, "Helvetica", 10)  # Calculate where the bold amount should start
    c.drawString(amount_x, top_y - 3.6 * inch, amount_in_words)



    # Bold Payment Mode and Donation Purpose on the Same Line
    c.setFont("Helvetica", 10)
    combined_text = f"by {data['Payment_Mode']} towards : {data['Towards']}"
    c.drawString(1.2 * inch, top_y - 4.0 * inch, combined_text)

    # Bold Amount (Numerical)
    c.setFont("Helvetica", 12)
    amount = int(data['Amount'])
    c.drawString(1.2 * inch, top_y - 4.6 * inch, f"RS. {amount} /-")
    c.drawRightString(6.8 * inch, top_y - 6.1 * inch, "For Bombay Yogakshema Sabha (Regd.)")




    # # Load and attach signature image if it exists
    # signature_path = r"C:\Users\umesh\OneDrive\Documents\Datascience\Jithin_mullappilli\sign.jpg"
    # stamp_path = r"C:\Users\umesh\OneDrive\Documents\Datascience\Jithin_mullappilli\stamp.jpg"
    # Draw the signature
    if os.path.exists(signature_path):
        try:
            # Signature adjustment: bigger and shifted left
            c.drawImage(signature_path, 5.8 * inch, top_y - 6.8 * inch, width=1.4 * inch, height=0.6 * inch)
        except Exception as e:
            print(f"Error loading signature image: {e}")
    else:
        print("Signature image not found, drawing line instead.")
        c.line(6.8 * inch, top_y - 6.8 * inch, 7.3 * inch, top_y - 7.3 * inch)

    # Draw the stamp
    if os.path.exists(stamp_path):
        try:
            # Stamp adjustment: slightly lower and shifted right
            c.drawImage(stamp_path, 4.8 * inch, top_y - 7.1 * inch, width=1.0 * inch, height=1.0 * inch)  # Adjust size and position
        except Exception as e:
            print(f"Error loading stamp image: {e}")
    else:
        print("Stamp image not found.")

    # Position for "Secretary / Treasurer" below the signature
    c.drawRightString(6.8 * inch, top_y - 7.3 * inch, "Secretary / Treasurer")  # Adjusted position for better spacing

    # Save the PDF
    c.save()



# Function to send email with the attached receipt
def send_email(receiver_email, subject, body, attachment):
    msg = MIMEMultipart()
    # msg['From'] = SENDER_EMAIL
    msg['From'] = formataddr(("BYS Acknowledgement", SENDER_EMAIL))
    msg['To'] = receiver_email
    msg['Subject'] = subject
    # Email body content
    body = """Please find the attached receipt for your donation.

Thank you for your valuable contribution.

Regards,  
BYS Committee"""
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the PDF
    part = MIMEBase('application', 'octet-stream')
    with open(attachment, 'rb') as f:
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
    msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Authentication Error", "Failed to authenticate with the email server.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while sending the email: {e}")



def process_and_send_emails(file_path):
    # Load Excel file and ensure column names match
    df = pd.read_excel(file_path)

    # Create a temporary directory within the executable's working directory
    base_dir = Path(tempfile.gettempdir()) / "receipts"
    base_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Process each row in the DataFrame
    for _, row in df.iterrows():
        # Check and convert the 'Amount' value to float, handling empty or invalid entries
        amount_str = str(row['Amount']).strip()
        if not amount_str or not re.search(r'\d', amount_str):
            print("Warning: Skipping row due to missing or invalid Amount value.")
            continue

        # Clean and convert the amount value
        try:
            amount_number = float(re.sub(r'[^\d.]', '', amount_str))
        except ValueError:
            print(f"Warning: Invalid Amount format for row: {row['Amount']}")
            continue

        # Convert the amount to words
        amount_in_words = num2words(amount_number, to='currency', lang='en_IN')

        # Prepare data for PDF generation
        receipt_no = int(row['Receipt No.'])  # Convert to integer to remove `.0`
        date = pd.to_datetime(row['DATE']).strftime('%d-%m-%Y')  # Format date to remove time
        towards = row['Towards'] if 'Towards' in row else 'Donation - Anudanind Ashamrashala'

        data = {
            'Receipt_No': receipt_no,
            'Date': date,
            'Name': row['Received From'],
            'Amount': amount_number,
            'Amount_in_words': amount_in_words,
            'Payment_Mode': row['COD'],
            'Towards': towards,
            'Email': row['Email ID']
        }
        print(f"Processing Payment Mode: {data['Payment_Mode']}")

        # Create the PDF file path in the temporary receipts directory
        output_path = base_dir / f"Receipt_{receipt_no}.pdf"

        # Generate PDF and send email
        generate_receipt(data, str(output_path))
        send_email(data['Email'], "Your Donation Receipt", "Please find attached your donation receipt.", str(output_path))

        # Delete the PDF after sending the email
        os.remove(output_path)
        print(f"Deleted the file: {output_path}")

    messagebox.showinfo("Success", "Emails sent successfully.")

# def process_and_send_emails(file_path):
#     # Load Excel file and ensure column names match
#     df = pd.read_excel(file_path)

#     # Directory to save PDFs
#     output_dir = "receipts"
#     os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

#     # Process each row in the DataFrame
#     for _, row in df.iterrows():
#         # Check and convert the 'Amount' value to float, handling empty or invalid entries
#         amount_str = str(row['Amount']).strip()
#         if not amount_str or not re.search(r'\d', amount_str):
#             print("Warning: Skipping row due to missing or invalid Amount value.")
#             continue

#         # Clean and convert the amount value
#         try:
#             amount_number = float(re.sub(r'[^\d.]', '', amount_str))
#         except ValueError:
#             print(f"Warning: Invalid Amount format for row: {row['Amount']}")
#             continue

#         # Convert the amount to words
#         amount_in_words = num2words(amount_number, to='currency', lang='en_IN')

#         # Prepare data for PDF generation
#         receipt_no = int(row['Receipt No.'])  # Convert to integer to remove `.0`
#         date = pd.to_datetime(row['DATE']).strftime('%d-%m-%Y')  # Format date to remove time
#         towards = row['Towards'] if 'Towards' in row else 'Donation - Anudanind Ashamrashala'
        
#         data = {
#             'Receipt_No': receipt_no,
#             'Date': date,
#             'Name': row['Received From'],
#             'Amount': amount_number,
#             'Amount_in_words': amount_in_words,
#             'Payment_Mode': row['COD'],
#             'Towards': towards,
#             'Email': row['Email ID']
#         }
#         print(data['Payment_Mode'])


#         output_dir = tempfile.mkdtemp(prefix="receipts_")

#         # Create the PDF file path in the 'receipts' directory
#         output_path = os.path.join(output_dir, f"Receipt_{receipt_no}.pdf")

#         # Generate PDF and send email
#         generate_receipt(data, output_path)
#         send_email(data['Email'], "Your Donation Receipt", "Please find attached your donation receipt.", output_path)

#         # Delete the PDF after sending the email
#         os.remove(output_path)
#         print(f"Deleted the file: {output_path}")

#     messagebox.showinfo("Success", "Emails sent successfully.")


# # # Function to process the Excel file and send emails
# def process_and_send_emails(file_path):
#     # Load Excel file and ensure column names match
#     df = pd.read_excel(file_path)

#     # Process each row in the DataFrame
#     for _, row in df.iterrows():
#         # Check and convert the 'Amount' value to float, handling empty or invalid entries
#         amount_str = str(row['Amount']).strip()
#         if not amount_str or not re.search(r'\d', amount_str):
#             print("Warning: Skipping row due to missing or invalid Amount value.")
#             continue

#         # Clean and convert the amount value
#         try:
#             amount_number = float(re.sub(r'[^\d.]', '', amount_str))
#         except ValueError:
#             print(f"Warning: Invalid Amount format for row: {row['Amount']}")
#             continue

#         # Convert the amount to words
#         amount_in_words = num2words(amount_number, to='currency', lang='en_IN')

#         # Prepare data for PDF generation
#         receipt_no = int(row['Receipt No.'])  # Convert to integer to remove `.0`
#         date = pd.to_datetime(row['DATE']).strftime('%d-%m-%Y')  # Format date to remove time
#         # Add 'Towards' field from the row (assuming it exists in the Excel file)
#         towards = row['Towards'] if 'Towards' in row else 'Donation - Anudanind Ashamrashala'
#         data = {
#             'Receipt_No': receipt_no,
#             'Date': date,
#             'Name': row['Received From'],
#             'Amount': amount_number,
#             'Amount_in_words': amount_in_words,
#             'Payment_Mode': row['COD'],
#             'Towards': towards,  # Add Towards to the data dictionary
#             'Email': row['Email ID']
#         }
#         print(data['Payment_Mode'])

#         # Create a temporary file in the system's temp directory
#         with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
#             output_path = temp_file.name


#         # Generate PDF and send email
#         generate_receipt(data, output_path)
#         send_email(data['Email'], "Your Donation Receipt", "Please find attached your donation receipt.", output_path)

#     messagebox.showinfo("Success", "Emails sent successfully.")

# GUI Setup
def on_browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def on_send():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showwarning("Input Error", "Please select an Excel file.")
        return
    process_and_send_emails(file_path)

# Setup main window
root = tk.Tk()
root.title("Excel to PDF Emailer")
root.geometry("400x300")
root.config(bg="white")

# UI Elements
file_label = tk.Label(root, text="Select Excel File", bg="white")
file_label.pack(pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=5)
browse_button = tk.Button(root, text="Browse", command=on_browse_file, bg="#4CAF50", fg="white")
browse_button.pack(pady=5)
send_button = tk.Button(root, text="Send PDF", command=on_send, bg="#2196F3", fg="white")
send_button.pack(pady=20)

# Run the application
root.mainloop()



































































































































































