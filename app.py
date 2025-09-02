import asyncio
import logging
import gradio as gr
from agent import Manager
from openai.types.responses import ResponseTextDeltaEvent
from agents import Runner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

email_manager = Manager()

async def chat_with_agent(message, history):
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    messages.append({"role": "user", "content": message})

    result = Runner.run_streamed(email_manager.agent, input=messages)

    response_text = ""
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            response_text += event.data.delta

    logging.info(f"AI Response: {response_text[:100]}...")
    return response_text


def chat_wrapper(message, history):
    return asyncio.run(chat_with_agent(message, history))


with gr.Blocks(title="📧 Email Butler") as app:
    gr.Markdown(
        """
        <h1 style="text-align:center; color:#2A3F54;">📧 Email Butler</h1>
        <p style="text-align:center; font-size:14px; color:#555;">
        Draft and send professional emails effortlessly. Your AI assistant will guide you step by step.
        </p>
        """
    )

    gr.HTML("<hr style='margin: 20px 0;'>")

    chatbot = gr.ChatInterface(
        fn=chat_wrapper,
        type="messages"
    )

    gr.Markdown(
        """
        <p style="text-align:center; font-size:12px; color:#888; margin-top:10px;">
        Powered by your Email Manager AI.
        </p>
        """
    )

if __name__ == "__main__":
    app.launch(share=False, debug=True)
