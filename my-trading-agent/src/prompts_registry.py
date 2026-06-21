"""
Registry of prompt names this graph depends on.

Prompt *text* lives in LangSmith Hub (edited via the web UI, no redeploy
needed). This file just records *which* prompts exist so the dependency is
visible in git, even though the content isn't.

First time setup: push each prompt once, e.g. from a notebook cell:

    from langsmith import Client
    client = Client()
    client.push_prompt(INTENT_PROMPT, object=your_chat_prompt_template)

After that, every node pulls by name at runtime.
"""

INTENT_PROMPT = "trading-desk/intent-agent"
MARKET_PROMPT = "trading-desk/market-agent"
RISK_PROMPT = "trading-desk/risk-agent"
RECOMMENDATION_PROMPT = "trading-desk/recommendation-agent"
EVALUATOR_PROMPT = "trading-desk/evaluator-agent"
