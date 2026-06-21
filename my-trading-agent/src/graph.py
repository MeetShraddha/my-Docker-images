"""
Builds and compiles the trading desk StateGraph.

This is the module LangGraph CLI loads (see langgraph.json -> graphs).
Run `langgraph dev` from the project root to launch it in LangGraph Studio,
where you can watch each node execute, inspect state at every step, and
replay individual runs.

Graph shape:

    intent ──> [market?] ──┐
           └─> [risk?]   ──┼──> recommendation ──> evaluator
           └─────────────┘
           (skips straight to recommendation if neither is needed)

market and risk run as separate branches that both fan into
recommendation — LangGraph waits for both before proceeding.
"""

from langgraph.graph import StateGraph, START, END

from src.state import TradingState
from src.nodes.intent import intent_node
from src.nodes.market import market_node
from src.nodes.risk import risk_node
from src.nodes.recommendation import recommendation_node
from src.nodes.evaluator import evaluator_node
from src.routing import route_after_intent


def build_graph():
    builder = StateGraph(TradingState)

    builder.add_node("intent", intent_node)
    builder.add_node("market", market_node)
    builder.add_node("risk", risk_node)
    builder.add_node("recommendation", recommendation_node)
    builder.add_node("evaluator", evaluator_node)

    builder.add_edge(START, "intent")

    # conditional fan-out: market and/or risk, or straight to recommendation
    builder.add_conditional_edges(
        "intent",
        route_after_intent,
        ["market", "risk", "recommendation"],
    )

    # both market and risk (if they ran) feed into recommendation
    builder.add_edge("market", "recommendation")
    builder.add_edge("risk", "recommendation")

    builder.add_edge("recommendation", "evaluator")
    builder.add_edge("evaluator", END)

    return builder.compile()


# module-level instance — this is what langgraph.json points to
graph = build_graph()
