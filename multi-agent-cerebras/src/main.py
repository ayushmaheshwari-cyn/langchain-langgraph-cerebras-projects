"""
Run:  python -m src.main

Interactive CLI around the supervisor multi-agent system. Try a prompt that
needs more than one specialist, e.g.:

    "Find the current population of Japan and India, then tell me the
     combined total and summarize it in two sentences."

Watch how the supervisor routes to research_agent -> math_agent ->
writing_agent in turn.
"""

from src.supervisor import build_supervisor_app


def main():
    app = build_supervisor_app()
    thread_id = "cli-session-1"
    config = {"configurable": {"thread_id": thread_id}}

    print("Multi-agent supervisor (Cerebras + LangGraph). Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        result = app.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )

        final_message = result["messages"][-1]
        print(f"\nFinal answer: {final_message.content}\n")

        # Uncomment to see the full routing trail (who said what):
        # for m in result["messages"]:
        #     print(f"[{getattr(m, 'name', m.type)}] {m.content}")


if __name__ == "__main__":
    main()
