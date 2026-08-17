# Project 2 — Multi-Agent Supervisor (LangGraph + langgraph-supervisor + Cerebras)

The "advanced" step up from Project 1: instead of one agent juggling every
tool, we split responsibilities across **specialist agents**, coordinated by
a **supervisor agent** that decides who does what.

```
multi-agent-cerebras/
├── .env.example
├── requirements.txt
├── README.md
├── src/
│   ├── config.py               # loads env vars, builds ChatCerebras clients
│   ├── tools.py                # web_search + calculator tools
│   ├── agents/
│   │   ├── research_agent.py    # specialist: web_search only
│   │   ├── math_agent.py        # specialist: calculator only
│   │   └── writing_agent.py     # specialist: no tools, drafts final prose
│   ├── supervisor.py            # create_supervisor(...) — wires it all together
│   └── main.py                   # interactive CLI
└── tests/
    └── test_supervisor.py
```

## Architecture

```
                 ┌──────────────┐
   user  ───────►│  supervisor   │◄────────────┐
                 │    (LLM)      │              │
                 └──────┬────────┘              │
        handoff tool call (one per specialist)  │ control returns
                 ┌──────┼───────────────┐        │ after each
                 ▼      ▼               ▼        │ specialist turn
          research_agent  math_agent  writing_agent
           (web_search)   (calculator)  (no tools)
```

- The **supervisor** is an LLM equipped with an auto-generated *handoff tool*
  for every worker (`transfer_to_research_agent`, etc., created by
  `langgraph_supervisor.create_supervisor`).
- Calling a handoff tool passes the **full message history** to that worker
  and hands it control.
- Each worker is itself a small `create_react_agent` ReAct loop (same pattern
  as Project 1), scoped to only the tools it needs.
- When a worker finishes, control returns to the supervisor, which decides
  the next specialist or ends the run.
- This is LangGraph's **supervisor topology** — best when you have a
  handful of clearly distinct specialists and want one orchestrator that
  stays in control end-to-end (as opposed to a flat "network" of peers, or a
  full hierarchy of supervisors-of-supervisors).

## Setup

```bash
cd multi-agent-cerebras
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # paste your CEREBRAS_API_KEY (from cloud.cerebras.ai)
```

## Run

```bash
python -m src.main
```

Try:

```
You: Find the current population of Japan and India, then give me the
     combined total and summarize it in two sentences.
```

You'll see the supervisor delegate to `research_agent` (facts + sources),
then `math_agent` (the sum), then `writing_agent` (the final two-sentence
summary) — all inside one graph run.

## Test

```bash
pytest -q
```

## Extending this further

- Add more specialists (e.g. a `code_agent`, `sql_agent`) — just build them
  the same way as the existing three and add to the `agents=[...]` list in
  `supervisor.py`.
- Swap `create_supervisor` for a hand-rolled `StateGraph` + `Command` routing
  if you need custom control flow the prebuilt supervisor doesn't support.
- Add a persistent checkpointer (e.g. `SqliteSaver`/`PostgresSaver` instead
  of `InMemorySaver`) for memory that survives process restarts.
