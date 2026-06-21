"""
P&L calculation tool used by risk_node.

Kept as a plain Python function (not an LLM call) — same as the original
notebook. Exposed to the model via LangChain's @tool decorator so it can be
bound to a ChatAnthropic model and invoked through normal tool-calling.
"""

from langchain_core.tools import tool
from src.data import POSITIONS


@tool
def calculate_pnl(commodity: str, scenario_price_usd: float | None = None) -> str:
    """Calculate current P&L and exposure for a trader's position.

    Args:
        commodity: e.g. 'Brent Crude', 'WTI Crude', 'TTF Gas'
        scenario_price_usd: optional hypothetical price to calculate P&L against
    """
    pos = POSITIONS.get(commodity)
    if not pos:
        return f"No open position found for {commodity}."

    current = pos["current_price"]
    cost = pos.get("avg_cost_usd", pos.get("avg_cost_eur", 0))
    check_price = scenario_price_usd if scenario_price_usd else current

    if "volume_barrels" in pos:
        volume = pos["volume_barrels"]
        unit = "barrels"
    else:
        volume = pos["volume_mwh"]
        unit = "MWh"

    pnl = (check_price - cost) * volume
    if pos["direction"] == "short":
        pnl = -pnl

    label = "Scenario" if scenario_price_usd else "Current"
    return (
        f"{commodity} | {pos['direction'].upper()} {volume:,} {unit}\n"
        f"  Cost: {cost:.2f} | {label} price: {check_price:.2f}\n"
        f"  Unrealised P&L: ${pnl:,.0f}"
    )
