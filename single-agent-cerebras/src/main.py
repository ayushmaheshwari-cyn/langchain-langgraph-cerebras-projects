"""
Run:  python -m src.main

A minimal interactive CLI around the single agent, so you can see the
ReAct loop (thought -> tool call -> observation -> answer) working live.
"""

from src.agent import build_agent


def main():
    agent = build_agent()
    thread_id = "cli-session-1"  # same id => same conversation memory
    config = {"configurable": {"thread_id": thread_id}}

    print("Single-agent (Cerebras + LangGraph). Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )

        final_message = result["messages"][-1]
        print(f"\nAgent: {final_message.content}\n")


if __name__ == "__main__":
    main()
