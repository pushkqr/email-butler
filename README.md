# Email Butler 📧

Email Butler is a professional AI-powered email assistant that helps you draft, polish, and send emails effortlessly. Powered by an intelligent Email Manager Agent, this tool ensures your communication is clear, professional, and goal-oriented.

## Features

* Draft polished, professional emails using AI.
* Automatically generate compelling subject lines and HTML email content.
* Send emails to single or multiple recipients via SMTP.
* Step-by-step guidance and draft review before sending.
* Modular architecture for easy maintenance and customization.

## Project Structure

```
email-butler/
├── agent.py          # Defines Agents, Tools, and EmailContent model
├── tools.py          # Optional: Separate tools (send_email, etc.)
├── prompts.py        # Centralized prompts for AI agents
├── app.py            # Gradio UI and main entrypoint
├── .env              # SMTP credentials and API keys
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/email-butler.git
cd email-butler
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
venv\Scripts\activate    
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:

```
LLM_API_KEY=your_api_key
BASE_URL=your_api_base_url
SMTP_SERVER=smtp.example.com
SMTP_EMAIL=your_email@example.com
SMTP_PASSWORD=your_email_app_key/password
```

## Usage

Run the Gradio interface:

```bash
python app.py
```

* Open the local URL displayed in the console.
* Start a chat with the Email Manager to draft emails.
* Review drafts and confirm sending.

## Logging & Maintenance

* Logs are output to the console for easier debugging and maintenance.
* SMTP configuration warnings and errors are logged.
* Responses from the AI are partially logged for monitoring.


