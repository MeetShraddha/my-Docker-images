"""
risk_node — calculates P&L exposure using the calculate_pnl tool.

Ported from risk_agent() in the original notebook. Uses LangChain's
tool-binding instead of manually parsing tool_use blocks from the raw
Anthropic SDK response.
"""

from langchain_anthropic import ChatAnthropic
from langsmith import Client

from src.state import TradingState
from src.data import POSITIONS
from src.tools import calculate_pnl
from src.prompts_registry import RISK_PROMPT

_client = Client()
_model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1500).bind_tools([calculate_pnl])


def risk_node(state: TradingState) -> dict:
    prompt = _client.pull_prompt(RISK_PROMPT, include_model=False)
    chain = prompt | _model

    response = chain.invoke({
        "query": state["query"],
        "positions": ", ".join(POSITIONS.keys()),
        "commodities": ", ".join(state["commodities"]),
    })

    results = []
    for call in response.tool_calls:
        if call["name"] == "calculate_pnl":
            results.append(calculate_pnl.invoke(call["args"]))

    if not results:
        # fallback: calculate for every relevant commodity with an open position
        results = [
            calculate_pnl.invoke({"commodity": c})
            for c in state["commodities"]
            if c in POSITIONS
        ]

    output = "\n\n".join(results) if results else "No matching positions found."
    return {"pnl": output}
