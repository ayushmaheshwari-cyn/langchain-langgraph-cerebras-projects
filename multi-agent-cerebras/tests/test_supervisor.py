"""
Smoke test for the supervisor graph.
Run with: pytest -q
Requires a valid CEREBRAS_API_KEY (these hit the real API).
"""

from src.supervisor import build_supervisor_app


def test_supervisor_routes_math_task():
    app = build_supervisor_app()
    config = {"configurable": {"thread_id": "test-thread"}}
    result = app.invoke(
        {"messages": [{"role": "user", "content": "What is 45 * 12? Just the number."}]},
        config=config,
    )
    final_text = result["messages"][-1].content
    assert "540" in final_text
