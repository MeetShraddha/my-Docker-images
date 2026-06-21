DIrectory Structure:

my-trading-agent/

├── langgraph.json

├── .env                      # ANTHROPIC_API_KEY, LANGSMITH_API_KEY, LANGSMITH_TRACING=true

├── requirements.txt
├── Dockerfile
├── src/
│   ├── state.py              # shared TypedDict across all nodes
│   ├── data.py                # POSITIONS, MARKET_CONTEXT (your mock data)
│   ├── tools.py               # PNL_TOOL + run_pnl_calc
│   ├── nodes/
│   │   ├── intent.py
│   │   ├── market.py
│   │   ├── risk.py
│   │   ├── recommendation.py
│   │   └── evaluator.py
│   ├── routing.py            # route() → conditional_edge function
│   └── graph.py              # builds + compiles StateGraph — CLI entry point
└── evals/
    └── run_eval_suite.py
