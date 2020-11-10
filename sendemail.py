# Modified sendemail.py from github.com/joeyuhj/pricematch
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import *


def send_an_email(subject, recipient, text_content, html_content):
    email_address = Settings.sender_email_address
    email_password = Settings.sender_email_password

    # formatting the email, creating message, subject, adding a recipient, and adding some text
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = recipient

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    # context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.sendmail(email_address, recipient, msg.as_string())
