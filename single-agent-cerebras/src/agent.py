"""
Single-agent implementation.

Pattern: LangGraph's prebuilt ReAct loop.
    user message -> [agent node: call LLM] -> tool_calls? -> [tools node] -> back to agent
                                             -> no tool_calls -> END

We add an InMemorySaver checkpointer so the agent remembers the conversation
across multiple `.invoke()` calls as long as we pass the same thread_id.
"""

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from src.config import get_llm
from src.tools import ALL_TOOLS

SYSTEM_PROMPT = """You are a precise, helpful research and math assistant.

Rules:
- Use the `calculator` tool for any arithmetic instead of computing it yourself.
- Use the `web_search` tool whenever the question depends on current or
  unfamiliar facts.
- If a tool result is insufficient, you may call another tool.
- Always give a direct, concise final answer once you have enough information.
"""


def build_agent():
    """
    Returns a compiled LangGraph agent (a CompiledStateGraph) ready to `.invoke()`.
    """
    llm = get_llm(temperature=0.2)
    checkpointer = InMemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    return agent
