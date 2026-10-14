import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-5.5")

client = OpenAI(api_key=api_key) if api_key else None


def get_ai_response(message: str) -> str:
    if client is None:
        return "The AI assistant is not configured yet."

    response = client.responses.create(
        model=model,
        instructions=(
            "You are the SmartEvent assistant. Help users discover "
            "events, understand bookings, and get ticket support. "
            "Never invent event details, prices, ticket availability, "
            "or booking information. Use only verified data supplied "
            "by the application for SmartEvent-specific questions."
        ),
        input=message,
    )

    return response.output_text