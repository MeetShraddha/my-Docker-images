"""
Dynamic routing — decides which agents run based on the intent
classification. Same logic as route() in the original notebook, just
reshaped into LangGraph's conditional-edge contract: it returns the name(s)
of the next node(s) to run.

No LLM call here — intent_node already produced everything needed to
route in pure Python.
"""

from src.state import TradingState


def route_after_intent(state: TradingState) -> list[str]:
    """Returns the list of next node names to execute after intent_node."""
    intent = state["intent"]
    next_nodes = []

    if intent.get("needs_market_context"):
        next_nodes.append("market")

    if intent.get("needs_pnl_calc"):
        next_nodes.append("risk")

    if not next_nodes:
        # nothing extra needed — go straight to recommendation
        next_nodes.append("recommendation")

    return next_nodes
