"""
Basic smoke tests.
Run with: pytest -q
Requires a valid CEREBRAS_API_KEY in your environment (these hit the real API).
"""

from src.agent import build_agent
from src.tools import calculator


def test_calculator_tool_direct():
    result = calculator.invoke({"expression": "12 * (3 + 4) / 2"})
    assert result == "42.0"


def test_agent_answers_math_question():
    agent = build_agent()
    config = {"configurable": {"thread_id": "test-thread"}}
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is 17 * 23?"}]},
        config=config,
    )
    final_text = result["messages"][-1].content
    assert "391" in final_text
