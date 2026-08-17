"""
Math specialist: only has the calculator tool.
"""

from langgraph.prebuilt import create_react_agent

from src.config import get_llm
from src.tools import calculator

MATH_PROMPT = """You are a math specialist.
Always use the calculator tool for arithmetic instead of computing by hand.
Show the final numeric answer clearly."""


def build_math_agent():
    llm = get_llm(temperature=0.0)  # deterministic for math
    return create_react_agent(
        model=llm,
        tools=[calculator],
        prompt=MATH_PROMPT,
        name="math_agent",
    )
