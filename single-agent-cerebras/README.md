# Project 1 — Single Agent (LangGraph ReAct + Cerebras)

The "basic" building block: **one LLM + a set of tools, looping until it has an answer.**

```
single-agent-cerebras/
├── .env.example        # copy to .env and add your Cerebras key
├── requirements.txt
├── README.md
├── src/
│   ├── config.py        # loads env vars, builds the ChatCerebras client
│   ├── tools.py         # calculator + web_search tools (@tool decorated)
│   ├── agent.py         # create_react_agent(...) graph definition
│   └── main.py           # interactive CLI chat loop
└── tests/
    └── test_agent.py
```

## How it works (the graph)

```
        ┌────────┐        has tool_calls?        ┌───────┐
 START →│  agent  │ ───────────────────────────► │ tools │
        │ (LLM)   │ ◄─────────────────────────── │ (exec)│
        └────────┘        loop back                └───────┘
             │  no tool_calls
             ▼
            END
```

`create_react_agent` (from `langgraph.prebuilt`) builds this exact graph for you:
1. `agent` node calls the Cerebras LLM with the running message list.
2. If the LLM's response contains `tool_calls`, LangGraph routes to the `tools`
   node, which executes each tool and appends the results as `ToolMessage`s.
3. Control returns to `agent`, which sees the tool output and decides whether
   to call another tool or give a final answer.
4. When there are no more tool calls, the graph ends and the last message is
   the answer.

An `InMemorySaver` checkpointer is attached so the agent remembers prior turns
within the same `thread_id` (short-term conversational memory).

## Setup

```bash
cd single-agent-cerebras
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then paste your CEREBRAS_API_KEY (from cloud.cerebras.ai)
```

## Run

```bash
python -m src.main
```

```
You: what's 18% of 245, then search who won the last F1 race
Agent: 18% of 245 is 44.1. According to a web search, ...
```

## Test

```bash
pytest -q
```

## Where this goes next

Once you outgrow "one agent, a few tools", you split responsibilities into
multiple specialized agents coordinated by a supervisor — see **Project 2**.
