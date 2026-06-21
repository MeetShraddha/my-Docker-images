"""
Offline evaluation across different query types.

Ported from run_eval_suite() in the original notebook — same test cases,
now invoking the compiled LangGraph graph instead of orchestrator().

In production: log all queries + scores to a database, track score trends
over time, flag regressions. With LangSmith tracing on, every run here is
already captured automatically — this script just prints a summary.
"""

from src.graph import graph

TEST_CASES = [
    {
        "query": "Brent just spiked 3%. We're long 500k barrels. Should I hedge?",
        "expected_query_type": "hedge_decision",
    },
    {
        "query": "What's driving TTF gas today?",
        "expected_query_type": "market_outlook",
    },
    {
        "query": "Show me my current P&L on WTI.",
        "expected_query_type": "position_risk",
    },
    {
        "query": "If Brent drops to $78, what does that do to our book?",
        "expected_query_type": "scenario_analysis",
    },
]


def run_eval_suite():
    results = []

    for i, tc in enumerate(TEST_CASES, 1):
        print(f"\n{'#' * 65}")
        print(f"  TEST CASE {i}/{len(TEST_CASES)}: {tc['query']}")
        print(f"{'#' * 65}")

        output = graph.invoke({"query": tc["query"]})

        intent = output["intent"]
        actual_type = intent.get("query_type")
        expected_type = tc["expected_query_type"]
        routing_correct = actual_type == expected_type

        eval_scores = output.get("eval", {})

        results.append({
            "query": tc["query"],
            "routing_correct": routing_correct,
            "expected_type": expected_type,
            "actual_type": actual_type,
            "eval_scores": eval_scores,
            "overall": eval_scores.get("overall"),
            "improvement": eval_scores.get("improvement"),
        })

    routing_acc = sum(r["routing_correct"] for r in results) / len(results) * 100
    avg_score = sum(r["overall"] for r in results if r["overall"]) / len(results)

    print(f"\n{'=' * 65}")
    print("  EVAL SUMMARY")
    print(f"{'=' * 65}")
    print(f"  Routing accuracy : {routing_acc:.0f}%")
    print(f"  Avg overall score: {avg_score:.1f}/5")

    print("\n  Areas to improve:")
    for r in results:
        if r["improvement"]:
            print(f"  • [{r['actual_type']}] {r['improvement']}")

    return results


if __name__ == "__main__":
    run_eval_suite()
