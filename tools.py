"""
tools.py
--------
Defines the "tools" (functions) our LLM bot can call when it decides
it needs to compute or look something up, instead of guessing.

Each tool needs TWO things:
1. The actual Python function that does the work.
2. A JSON "schema" describing the tool to the LLM (name, description,
   what parameters it takes) — this is how the model knows the tool
   exists and how to call it correctly.
"""

import ast
import operator
from datetime import datetime


# =========================================================================
# TOOL 1: Calculator
# =========================================================================
# We do NOT use Python's built-in eval() here — eval() would let the model
# (or a malicious prompt) run arbitrary code, which is a security risk.
# Instead we parse the expression into a syntax tree and only allow safe
# arithmetic operations.
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node):
    """Recursively evaluate a parsed math expression, allowing only
    numbers and basic arithmetic operators."""
    if isinstance(node, ast.Constant):  # a plain number, e.g. 5 or 3.14
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed.")
    if isinstance(node, ast.BinOp):  # e.g. "3 + 4"
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed.")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):  # e.g. "-5"
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed.")
        return _ALLOWED_OPERATORS[op_type](_safe_eval(node.operand))
    raise ValueError("Unsupported expression.")


def calculator(expression: str) -> str:
    """
    Safely evaluates a basic arithmetic expression like "12 * (4 + 3)".
    Supports + - * / % ** and parentheses. Returns a string so it can be
    handed straight back to the LLM as a tool result.
    """
    try:
        parsed = ast.parse(expression, mode="eval").body
        result = _safe_eval(parsed)
        return str(result)
    except Exception as e:
        return f"Error: could not evaluate '{expression}' ({e})"


# =========================================================================
# TOOL 2: Current date/time lookup
# =========================================================================
def get_current_datetime(_unused: str = "") -> str:
    """Returns the current server date and time as a readable string."""
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


# =========================================================================
# Tool schemas — this is what gets sent to the Groq API so the model
# knows these tools exist and how to call them.
# =========================================================================
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate a basic arithmetic expression. Use this whenever "
                "the user asks for a calculation, e.g. '23 * 47' or "
                "'(15 + 5) / 4'. Supports + - * / % ** and parentheses."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '12 * (4 + 3)'.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": (
                "Get the current real-world date and time. Use this if the "
                "user asks what the date or time is right now."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]

# Maps tool name (as the LLM will refer to it) -> actual Python function to run.
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_current_datetime": get_current_datetime,
}