"""
Writing specialist: no tools, just strong prompting.
Takes facts/numbers gathered by the other agents and turns them into
clean, well-structured prose for the end user.
"""

from langgraph.prebuilt import create_react_agent

from src.config import get_llm

WRITING_PROMPT = """You are a writing specialist.
Turn the information already gathered in the conversation into a clear,
well-organized final answer for the user. Do not invent facts or numbers
that weren't already provided -- if something is missing, say so."""


def build_writing_agent():
    llm = get_llm(temperature=0.5)  # a bit more creative for prose
    return create_react_agent(
        model=llm,
        tools=[],  # pure language task, no tool calls needed
        prompt=WRITING_PROMPT,
        name="writing_agent",
    )
