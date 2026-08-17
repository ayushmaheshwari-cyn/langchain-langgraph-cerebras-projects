"""
Tools available to the agent.
Each tool is a plain python function decorated with @tool.
The docstring IS the tool description the LLM sees, so keep it precise.
"""

import ast
import operator as op

from langchain_core.tools import tool
from ddgs import DDGS  # duckduckgo-search package's import name

# ---- Safe calculator -------------------------------------------------

_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _ALLOWED_OPERATORS[type(node.op)](
            _safe_eval(node.left), _safe_eval(node.right)
        )
    if isinstance(node, ast.UnaryOp):
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression, e.g. '12 * (3 + 4) / 2'.
    Supports + - * / ** % and parentheses. Use this for any math instead
    of doing it in your head.
    """
    try:
        tree = ast.parse(expression, mode="eval").body
        result = _safe_eval(tree)
        return str(result)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"


# ---- Web search --------------------------------------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the public web for current information (news, facts, prices, etc.)
    and return the top few results as short text snippets with sources.
    Use this when the user asks about something recent or that you are not
    fully sure about.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
        if not results:
            return "No results found."
        formatted = []
        for r in results:
            formatted.append(f"- {r.get('title')}: {r.get('body')} ({r.get('href')})")
        return "\n".join(formatted)
    except Exception as exc:
        return f"Search failed: {exc}"


ALL_TOOLS = [calculator, web_search]
