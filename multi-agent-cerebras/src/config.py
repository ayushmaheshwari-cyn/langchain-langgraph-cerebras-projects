"""
Central place to load environment variables and build LLM clients.
Each agent can in principle use a different Cerebras model/temperature;
here we expose one factory so it's easy to swap per-agent later.
"""

import os
from dotenv import load_dotenv
from langchain_cerebras import ChatCerebras

load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_MODEL = os.getenv("CEREBRAS_MODEL", "llama-3.3-70b")

if not CEREBRAS_API_KEY:
    raise RuntimeError(
        "CEREBRAS_API_KEY is not set. Copy .env.example to .env and add your key "
        "from https://cloud.cerebras.ai"
    )


def get_llm(temperature: float = 0.2, model: str | None = None) -> ChatCerebras:
    """Returns a configured ChatCerebras chat model."""
    return ChatCerebras(
        model=model or CEREBRAS_MODEL,
        api_key=CEREBRAS_API_KEY,
        temperature=temperature,
    )
