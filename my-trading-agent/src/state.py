"""
Shared state schema for the trading desk graph.

Every node receives this state, returns a partial update (a dict with only
the keys it changed), and LangGraph merges that into the running state for
the next node. This replaces the `context = {}` dict that was being built
up manually inside orchestrator() in the original notebook.
"""

from typing import TypedDict, Optional


class TradingState(TypedDict, total=False):
    # input
    query: str

    # set by intent_node
    intent: dict
    commodities: list[str]

    # set by market_node (only runs if intent says it's needed)
    market_read: Optional[str]

    # set by risk_node (only runs if intent says it's needed)
    pnl: Optional[str]

    # set by recommendation_node
    recommendation: Optional[str]

    # set by evaluator_node
    eval: Optional[dict]
