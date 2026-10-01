# tests/test_deals.py

from agent_runner import run_agent
from deal_assertions import (
    assert_best_deal_is_correct,
    assert_all_deals_are_valid,
    assert_all_effective_prices_are_correct,
)


def test_iphone_deal_pipeline():

    result = run_agent(
        "Find me an iPhone 16 under ₹70000"
    )

    # Router
    assert result["route"] == "deal"

    # Extraction
    query = result["extracted_query"]

    assert query is not None
    assert query.brand is not None
    assert query.budget is not None

    # Database results
    assert_all_deals_are_valid(result)

    # Price calculations
    assert_all_effective_prices_are_correct(result)

    # Best deal
    assert_best_deal_is_correct(result)

    # Final response
    assert result["response"]

# This single test now validates:

# User query
#    ↓
# Router
#    ↓
# ProductQuery extraction
#    ↓
# PostgreSQL search
#    ↓
# PhoneDeal validation
#    ↓
# effective_price
#    ↓
# best deal
#    ↓
# final response