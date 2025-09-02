import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from pydantic import EmailStr, ValidationError
from agents import function_tool
import logging

logging.basicConfig(level=logging.INFO)

@function_tool
def send_email(to_addr: str | List[EmailStr], subject: str, body: str) -> Dict[str, str]:
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = 587
    sender_email = os.environ.get("SMTP_EMAIL")
    sender_password = os.environ.get("SMTP_PASSWORD")

    if not smtp_server or not sender_email or not sender_password:
        logging.warning("SMTP configuration missing")
        return {"status": "error", "message": "Missing SMTP configuration"}

    recipient_emails = to_addr if isinstance(to_addr, list) else [to_addr]
    for r in recipient_emails:
        try:
            EmailStr.validate(r)
        except ValidationError:
            logging.error(f"Invalid recipient email: {r}")
            return {"status": "error", "message": f"Invalid recipient email: {r}"}

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = ", ".join(recipient_emails)
            msg.attach(MIMEText(body, "html"))

            server.sendmail(sender_email, recipient_emails, msg.as_string())
            logging.info(f"Emails sent successfully to {', '.join(recipient_emails)}")
        return {"status": "success", "message": f"Emails sent to {', '.join(recipient_emails)}"}
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return {"status": "error", "message": f"Failed to send email: {e}"}
