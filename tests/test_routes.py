# tests/test_routes.py

from tests.agent_runner import run_agent


def test_deal_route():

    result = run_agent(
        "Find me an iPhone 16 under ₹70000"
    )

    assert result["route"] == "deal"


def test_summary_route():

    thread_id = "summary-test"

    run_agent(
        "Show me Samsung phones under ₹50000",
        thread_id=thread_id,
    )

    result = run_agent(
        "Summarize our conversation",
        thread_id=thread_id,
    )

    assert result["route"] == "summarize"
    assert result["response"]


def test_mobile_info_route():

    result = run_agent(
        "What is an AMOLED display?"
    )

    assert result["route"] == "mobile_info"
    assert result["response"]

def test_missing_budget():

    result = run_agent(
        "Find me the best iPhone 16 deal"
    )

    assert result["route"] == "deal"

    assert result["extracted_query"].budget is None

    assert result["response"]

    assert "budget" in result["response"].lower()

    assert result.get("deals", []) == []

def test_alternatives_are_different_retailers():

    result = run_agent(
        "Find me an iPhone 16 under ₹70000"
    )

    best = result.get("best_deal")
    alternatives = result.get("alternatives", [])

    if best is None:
        return

    retailers = {
        best.retailer
    }

    for deal in alternatives:
        assert deal.retailer not in retailers
        retailers.add(deal.retailer)

def test_max_two_alternatives():

    result = run_agent(
        "Find me an iPhone 16 under ₹70000"
    )

    alternatives = result.get("alternatives", [])

    assert len(alternatives) <= 2

# uv run pytest tests/
# uv run pytest tests/test_example.py