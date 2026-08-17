# LangChain + LangGraph + Cerebras: Basic → Advanced

Two standalone projects, meant to be worked through in order.

| Project | Concept | Pattern |
|---|---|---|
| `single-agent-cerebras/` | **Basic**: one agent, a few tools | `langgraph.prebuilt.create_react_agent` |
| `multi-agent-cerebras/` | **Advanced**: several specialist agents + orchestrator | `langgraph_supervisor.create_supervisor` |

Both use `langchain-cerebras`'s `ChatCerebras` as the LLM backend, wired up
via a `.env` file — get a free key at https://cloud.cerebras.ai.

## Quick start (either project)

```bash
cd single-agent-cerebras   # or multi-agent-cerebras
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add CEREBRAS_API_KEY
python -m src.main
```

## Why this order

1. **Single agent** teaches you the core loop everything else is built on:
   LLM ↔ tools, running inside a LangGraph graph, with memory via a
   checkpointer.
2. **Multi-agent supervisor** teaches you how to compose *multiple* of those
   same ReAct loops as specialist "workers," coordinated by an orchestrator
   LLM — the natural next step once one agent with many tools becomes hard
   to prompt reliably.

Each project's own `README.md` has a diagram of its graph and setup/run
instructions.
