import logging
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, Runner
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict, List
from pydantic import BaseModel
from prompts import Prompts
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from tools import send_email

load_dotenv(override=True)

api_key = os.environ.get("GOOGLE_API_KEY")
base_url = os.environ.get("BASE_URL")

external_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)


class EmailContent(BaseModel):
    subject: str
    body: str


@function_tool
def send_email(to_addr: str | List, email: EmailContent) -> Dict[str, str]:
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = 587
    sender_email = os.environ.get("SMTP_EMAIL")
    sender_password = os.environ.get("SMTP_PASSWORD")

    if not smtp_server or not sender_email or not sender_password:
        logging.warning("SMTP configuration missing")
        return {"status": "error", "message": "Missing SMTP configuration"}

    recipients = to_addr if isinstance(to_addr, list) else [to_addr]

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = email.subject
            msg["From"] = sender_email
            msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(email.body, "html"))
            server.sendmail(sender_email, recipients, msg.as_string())
            logging.info(f"Emails sent successfully to {', '.join(recipients)}")
        return {"status": "success", "message": f"Emails sent to {', '.join(recipients)}"}
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return {"status": "error", "message": f"Failed to send email: {e}"}


class Writer:
    def __init__(self):
        self.agent = Agent(
            name="Email Writer",
            instructions=Prompts.Writer.instructions,
            model=model,
            output_type=EmailContent
        )


class Manager:
    def __init__(self):
        self.writer = Writer()
        self.manager_tools = [
            self.writer.agent.as_tool(tool_name="Writer", tool_description=Prompts.Writer.tool_description),
            send_email
        ]
        self.agent = Agent(
            name="Email Manager",
            instructions=Prompts.Manager.instructions,
            tools=self.manager_tools,
            model=model
        )
