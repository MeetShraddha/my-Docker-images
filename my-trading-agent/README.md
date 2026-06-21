# Trading Desk Multi-Agent — LangGraph + LangSmith

## First-time setup

1. Copy `.env.example` to `.env` and fill in your real `ANTHROPIC_API_KEY`
   and `LANGSMITH_API_KEY`.

2. **Push your prompts to LangSmith Hub** (one-time, before the graph can run).
   The graph pulls prompts by name at runtime — they don't exist yet until
   you push them. Open a notebook or `python -i` session and run something
   like:

   ```python
   from langsmith import Client
   from langchain_core.prompts import ChatPromptTemplate
   from src.prompts_registry import INTENT_PROMPT

   client = Client()

   intent_prompt = ChatPromptTemplate.from_messages([
       ("system", """You are an intent classifier for a commodity trading desk.
   Classify the trader's query into:
   - query_type: one of [position_risk, market_outlook, hedge_decision, scenario_analysis, general]
   - commodities: list of commodities mentioned or implied
   - urgency: high / medium / low
   - needs_pnl_calc: true/false
   - needs_market_context: true/false

   Return JSON only: {{"query_type": "...", "commodities": [...], "urgency": "...",
   "needs_pnl_calc": true, "needs_market_context": true, "summary": "..."}}"""),
       ("human", "{query}"),
   ])

   client.push_prompt(INTENT_PROMPT, object=intent_prompt)
   ```

   Repeat for `MARKET_PROMPT`, `RISK_PROMPT`, `RECOMMENDATION_PROMPT`,
   `EVALUATOR_PROMPT` — the original prompt text for each is in the
   original notebook's agent functions; move it into a `ChatPromptTemplate`
   the same way.

3. Build the Docker image:
   ```bash
   docker build -t my-trading-agent .
   ```

4. Run it (Jupyter + LangGraph CLI ports both exposed):
   ```bash
   docker run -d --name trading-agent \
     -p 8888:8888 -p 2024:2024 \
     -v "$(pwd)":/home/jovyan/work \
     --env-file .env \
     my-trading-agent
   ```

5. View the graph visually:
   ```bash
   docker exec -it trading-agent langgraph dev --host 0.0.0.0
   ```
   Then open the LangGraph Studio URL it prints — you'll see each node
   execute, inspect state at every step, and replay individual runs.

6. Every run is also traced in LangSmith automatically (since
   `LANGSMITH_TRACING=true` is set) — no extra code needed.

## Running the eval suite

```bash
docker exec trading-agent python -m evals.run_eval_suite
```
