"""
Mock data for the trading desk demo.

In production: POSITIONS would come from a live CTRM feed,
MARKET_CONTEXT from Bloomberg/Argus/Reuters feeds.
"""

POSITIONS = {
    "Brent Crude": {
        "direction": "long",
        "volume_barrels": 500_000,
        "avg_cost_usd": 82.50,
        "current_price": 85.10,  # just spiked
    },
    "WTI Crude": {
        "direction": "short",
        "volume_barrels": 200_000,
        "avg_cost_usd": 80.20,
        "current_price": 79.90,
    },
    "TTF Gas": {
        "direction": "long",
        "volume_mwh": 150_000,
        "avg_cost_eur": 34.50,
        "current_price": 35.80,
    },
}

MARKET_CONTEXT = """
Date: 2024-01-15 14:32 UTC

Recent market events:
- Brent Crude up 3.1% today following Houthi attacks on Red Sea shipping lanes
- US crude inventories drew down 4.2M barrels last week (above 2.1M expected)
- Saudi Arabia signaled no production increase before Q2 review
- IEA revised 2024 demand forecast up 200k bpd citing stronger Asia demand
- USD weakened 0.4% against basket — supportive for dollar-denominated commodities
- Goldman Sachs raised Brent 3-month target from $85 to $91

Risk events this week:
- OPEC+ meeting Thursday
- US CPI data Wednesday
- EIA weekly inventory report Wednesday 15:30 UTC
"""
