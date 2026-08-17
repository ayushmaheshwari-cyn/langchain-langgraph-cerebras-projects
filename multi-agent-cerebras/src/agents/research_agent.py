"""
Research specialist: only has web_search. Kept narrow on purpose --
a focused toolset makes the worker more reliable and its prompt simpler.
"""

from langgraph.prebuilt import create_react_agent

from src.config import get_llm
from src.tools import web_search

RESEARCH_PROMPT = """You are a research specialist.
Use the web_search tool to find current, accurate information.
Report findings concisely with sources. Do not do math and do not write
long-form prose -- hand facts back to whoever asked."""


def build_research_agent():
    llm = get_llm(temperature=0.2)
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=RESEARCH_PROMPT,
        name="research_agent",  # required: supervisor routes by this name
    )
