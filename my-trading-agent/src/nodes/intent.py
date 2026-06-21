"""
intent_node — classifies what the trader is actually asking.

Ported from intent_agent() in the original notebook. Same JSON-out
contract: query_type, commodities, urgency, needs_pnl_calc,
needs_market_context, summary.
"""

import json
import re
from langchain_anthropic import ChatAnthropic
from langsmith import Client

from src.state import TradingState
from src.prompts_registry import INTENT_PROMPT

_client = Client()
_model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1500)


def _parse_json(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    return json.loads(match.group()) if match else {}


def intent_node(state: TradingState) -> dict:
    prompt = _client.pull_prompt(INTENT_PROMPT, include_model=False)
    chain = prompt | _model

    response = chain.invoke({"query": state["query"]})
    intent = _parse_json(response.content)

    return {
        "intent": intent,
        "commodities": intent.get("commodities") or ["Brent Crude"],
    }
