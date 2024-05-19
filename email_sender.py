import csv
import os
import smtplib
import ssl
from email.message import EmailMessage
from getpass import getpass

from dotenv import load_dotenv

load_dotenv()

port = 465
filename = 'receivers.csv'

sender = os.getenv('EMAIL') if 'EMAIL' in os.environ else getpass("Type your email and press enter: ")
password = os.getenv('PASSWORD') if 'PASSWORD' in os.environ else getpass("Type your password and press enter: ")

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    try:
        server.login(sender, password)
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for email, name, surname, text in reader:
                msg = EmailMessage()
                msg['Subject'] = f'Завдання з тренінг-курсу Python для {name} {surname}'
                msg['From'] = sender
                msg['To'] = email
                msg.set_content(text)
                print(f"Sending email to {name} {surname}")
                server.sendmail(sender, email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Invalid email or password")
