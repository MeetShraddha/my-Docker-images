"""
recommendation_node — produces a clear, trader-friendly recommendation.

Ported from recommendation_agent() in the original notebook.
"""

from langchain_anthropic import ChatAnthropic
from langsmith import Client

from src.state import TradingState
from src.prompts_registry import RECOMMENDATION_PROMPT

_client = Client()
_model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1500)


def recommendation_node(state: TradingState) -> dict:
    context_str = ""
    if state.get("market_read"):
        context_str += f"Market context:\n{state['market_read']}\n\n"
    if state.get("pnl"):
        context_str += f"Position & P&L:\n{state['pnl']}\n\n"

    prompt = _client.pull_prompt(RECOMMENDATION_PROMPT, include_model=False)
    chain = prompt | _model

    response = chain.invoke({
        "query": state["query"],
        "context": context_str,
    })

    return {"recommendation": response.content}
