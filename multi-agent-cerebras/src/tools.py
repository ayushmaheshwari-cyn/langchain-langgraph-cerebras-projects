"""
Tools shared across the specialist agents.
Splitting tools by domain (research vs math vs writing) is what lets
each worker agent stay small and focused -- the supervisor decides which
specialist (and therefore which toolset) a task needs.
"""

import ast
import operator as op

from langchain_core.tools import tool
from ddgs import DDGS

# ---------------------------------------------------------------------
# Research tools
# ---------------------------------------------------------------------


@tool
def web_search(query: str) -> str:
    """
    Search the public web and return the top results as short snippets
    with sources. Use this for current events, facts, or anything you're
    not 100% certain about.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
        if not results:
            return "No results found."
        return "\n".join(
            f"- {r.get('title')}: {r.get('body')} ({r.get('href')})" for r in results
        )
    except Exception as exc:
        return f"Search failed: {exc}"


# ---------------------------------------------------------------------
# Math tools
# ---------------------------------------------------------------------

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
    Evaluate a basic arithmetic expression, e.g. '(120 - 15) * 3'.
    Supports + - * / ** % and parentheses.
    """
    try:
        tree = ast.parse(expression, mode="eval").body
        return str(_safe_eval(tree))
    except Exception as exc:
        return f"Error evaluating expression: {exc}"
