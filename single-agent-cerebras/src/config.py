"""
Central place to load environment variables and build the LLM client.
Keeping this separate means every other module just imports `get_llm()`
instead of re-reading os.environ everywhere.
"""

import os
from dotenv import load_dotenv
from langchain_cerebras import ChatCerebras

# Load variables from a local .env file (never commit this file, only .env.example)
load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_MODEL = os.getenv("CEREBRAS_MODEL", "llama-3.3-70b")

if not CEREBRAS_API_KEY:
    raise RuntimeError(
        "CEREBRAS_API_KEY is not set. Copy .env.example to .env and add your key "
        "from https://cloud.cerebras.ai"
    )


def get_llm(temperature: float = 0.3) -> ChatCerebras:
    """
    Returns a configured ChatCerebras chat model.
    Cerebras' Wafer-Scale Engine gives very high tokens/sec, which is why
    it's a great backend for agent loops that call the model many times.
    """
    return ChatCerebras(
        model=CEREBRAS_MODEL,
        api_key=CEREBRAS_API_KEY,
        temperature=temperature,
    )
