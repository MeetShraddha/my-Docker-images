"""
evaluator_node — scores the recommendation quality (used offline for
model/prompt improvement).

Ported from evaluator_agent() in the original notebook.
"""

import json
import re
from langchain_anthropic import ChatAnthropic
from langsmith import Client

from src.state import TradingState
from src.prompts_registry import EVALUATOR_PROMPT

_client = Client()
_model = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1500)


def _parse_json(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    return json.loads(match.group()) if match else {}


def evaluator_node(state: TradingState) -> dict:
    prompt = _client.pull_prompt(EVALUATOR_PROMPT, include_model=False)
    chain = prompt | _model

    response = chain.invoke({
        "query": state["query"],
        "recommendation": state["recommendation"],
    })

    return {"eval": _parse_json(response.content)}
