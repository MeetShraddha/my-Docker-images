"""
market_node — interprets current market conditions relevant to the query.

Ported from market_agent() in the original notebook.
"""

from langchain_anthropic import ChatAnthropic
from langsmith import Client

from src.state import TradingState
from src.data import MARKET_CONTEXT
from src.prompts_registry import MARKET_PROMPT

_client = Client()
_model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1500)


def market_node(state: TradingState) -> dict:
    prompt = _client.pull_prompt(MARKET_PROMPT, include_model=False)
    chain = prompt | _model

    response = chain.invoke({
        "query": state["query"],
        "commodities": ", ".join(state["commodities"]),
        "market_context": MARKET_CONTEXT,
    })

    return {"market_read": response.content}
