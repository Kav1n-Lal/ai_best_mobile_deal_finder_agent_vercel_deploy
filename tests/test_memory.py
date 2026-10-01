# tests/test_memory.py

from tests.agent_runner import run_agent
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    
    GEval,
)
from deepeval import assert_test

def test_memory():

    thread_id = "memory-test-001"

    first = run_agent(
        "Show me Samsung phones under ₹50000",
        thread_id=thread_id,
    )

    second = run_agent(
        "Which one has the lowest effective price?",
        thread_id=thread_id,
    )

    assert first["response"]
    assert second["response"]

    query = second["extracted_query"]

    assert query is not None

def test_memory_preserves_brand():

    thread_id = "memory-test-002"

    run_agent(
        "Show me Samsung phones under ₹50000",
        thread_id=thread_id,
    )

    result = run_agent(
        "Which one has the lowest effective price?",
        thread_id=thread_id,
    )

    deals = result.get("deals", [])

    assert deals, "No deals returned for follow-up query."

    for deal in deals:
        assert deal.brand.lower() == "samsung"

memory_metric = GEval(
    name="Conversation Memory",

    criteria="""
    Evaluate whether the assistant correctly uses information
    established in previous turns.

    The assistant should correctly resolve references such as:

    "which one"
    "that phone"
    "the cheapest one"
    "that retailer"
    "what about the 256GB version?"

    It should not ask the user to repeat information that is
    already available in the conversation.
    """,

    evaluation_params=[
        "input",
        "actual_output",
    ],

    threshold=0.8,
    model="gpt-4o-mini",
)

def test_memory_quality():

    thread_id = "deepeval-memory-001"

    run_agent(
        "Show me Samsung phones under ₹50000",
        thread_id=thread_id,
    )

    result = run_agent(
        "Which one has the lowest effective price?",
        thread_id=thread_id,
    )

    test_case = LLMTestCase(
        input="""
        Previous conversation:

        User: Show me Samsung phones under ₹50000

        Current user message:
        Which one has the lowest effective price?
        """,

        actual_output=result["response"],
    )

    assert_test(
        test_case,
        [memory_metric],
    )
