# import os

# from dotenv import load_dotenv

# from deepeval import assert_test
# from deepeval.metrics import (
#     AnswerRelevancyMetric,
#     FaithfulnessMetric,
#     GEval,
# )
# from deepeval.models import OpenAIModel
# from deepeval.test_case import LLMTestCase, SingleTurnParams

# from agent_runner import run_agent


# # =========================================================
# # Environment
# # =========================================================

# load_dotenv(override=True)

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# # =========================================================
# # DeepEval Judge Model
# # =========================================================

# eval_model = OpenAIModel(
#     # model="openai/gpt-4o-mini",
#     model="google/gemini-2.5-flash",
#     # model="anthropic/claude-sonnet-4",
#     api_key=OPENROUTER_API_KEY,
#     base_url="https://openrouter.ai/api/v1",
#     temperature=0,
#     generation_kwargs={
#         "max_tokens": 250,
#     },
# )


# # =========================================================
# # Metrics
# # =========================================================

# answer_relevancy = AnswerRelevancyMetric(
#     threshold=0.8,
#     model=eval_model,
#     include_reason=True,
# )


# deal_response_quality = GEval(
#     name="Mobile Deal Response Quality",

#     criteria="""
#     Evaluate whether the assistant's response correctly answers
#     the user's mobile phone deal request.

#     The response should:

#     - Answer the user's request directly.
#     - Respect the requested brand.
#     - Respect the requested budget.
#     - Clearly identify the best deal.
#     - Correctly mention the retailer.
#     - Correctly communicate the price.
#     - Not invent prices or retailers.
#     - Not claim unavailable products are available.
#     - Avoid irrelevant information.
#     - Present alternatives clearly when alternatives exist.
#     """,

#     evaluation_params=[
#         SingleTurnParams.INPUT,
#         SingleTurnParams.ACTUAL_OUTPUT,
#     ],

#     threshold=0.8,
#     model=eval_model,
# )


# faithfulness = FaithfulnessMetric(
#     threshold=0.9,
#     model=eval_model,
#     include_reason=True,
# )


# # =========================================================
# # Convert database results into DeepEval context
# # =========================================================
# import json

# def deals_to_context(result):

#     deals = sorted(
#         result.get("deals", []),
#         key=lambda deal: deal.effective_price
#     )

#     top_3_deals = deals[:3]

#     return [
#         json.dumps(
#             deal.model_dump(),
#             default=str
#         )
#         for deal in top_3_deals
#     ]


# # =========================================================
# # Deal response test
# # =========================================================

# def test_deal_response():

#     query = "Find me an iPhone 16 under ₹70000"

#     result = run_agent(query)

#     test_case = LLMTestCase(
#         input=query,
#         actual_output=result["response"],
#     )

#     assert_test(
#         test_case,
#         [
#             answer_relevancy,
#             deal_response_quality,
#         ],
#     )


# # =========================================================
# # Database faithfulness test
# # =========================================================

# def test_faithfulness_to_database():

#     query = "Find me an iPhone 16 under ₹70000"

#     result = run_agent(query)

#     print("\n" + "=" * 100)
#     print("DATABASE DEALS")
#     print("=" * 100)

#     for i, deal in enumerate(result.get("deals", []), start=1):
#         print(
#             f"{i}. "
#             f"{deal.brand} {deal.model} | "
#             f"RAM={deal.memory} | "
#             f"Storage={deal.storage} | "
#             f"Retailer={deal.retailer} | "
#             f"Effective Price=₹{deal.effective_price}"
#         )

#     print("\n" + "=" * 100)
#     print("SELECTED BEST DEALS")
#     print("=" * 100)

#     for label in ["best_deal", "second_best_deal", "third_best_deal"]:
#         deal = result.get(label)

#         if deal:
#             print(
#                 f"{label}: "
#                 f"{deal.brand} {deal.model} | "
#                 f"{deal.retailer} | "
#                 f"₹{deal.effective_price}"
#             )
#         else:
#             print(f"{label}: None")

#     print("\n" + "=" * 100)
#     print("LLM RESPONSE")
#     print("=" * 100)
#     print(result["response"])

#     print("\n" + "=" * 100)
#     print("RETRIEVAL CONTEXT")
#     print("=" * 100)

#     retrieval_context = deals_to_context(result)

#     for context in retrieval_context:
#         print(context)

#     print("=" * 100)

#     test_case = LLMTestCase(
#         input=query,
#         actual_output=result["response"],
#         retrieval_context=retrieval_context,
#     )

#     assert_test(
#         test_case,
#         [faithfulness],
#     )


# # uv run pytest tests/test_deepeval.py::test_faithfulness_to_database -v -s

import json
import os

import pytest
from dotenv import load_dotenv

from deepeval import assert_test
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval,
)
from deepeval.models import OpenAIModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

from agent_runner import run_agent


# =========================================================
# Environment
# =========================================================

load_dotenv(override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set."
    )


# =========================================================
# Test Query
# =========================================================

QUERY = "Find me an iPhone 16 under ₹70000"


# =========================================================
# DeepEval Judge Model
# =========================================================

# eval_model = OpenAIModel(
#     model="google/gemini-2.5-flash-lite",
#     api_key=OPENROUTER_API_KEY,
#     base_url="https://openrouter.ai/api/v1",
#     temperature=0,
#     generation_kwargs={
#         # Keep this lower to reduce OpenRouter credit requirements.
#         "max_tokens": 450,
#     },
# )

from deepeval.models import OllamaModel

eval_model = OllamaModel(
    model="gemma3:12b",
    base_url="http://localhost:11434",
    temperature=0,
    generation_kwargs={
        "num_predict": 450,
    },
)


# =========================================================
# Metrics
# =========================================================

answer_relevancy = AnswerRelevancyMetric(
    threshold=0.8,
    model=eval_model,
    include_reason=True,
)


deal_response_quality = GEval(
    name="Mobile Deal Response Quality",

    criteria="""
    Evaluate whether the assistant's response correctly answers
    the user's mobile phone deal request.

    The response should:

    - Answer the user's request directly.
    - Respect the requested brand.
    - Respect the requested budget.
    - Clearly identify the best deal.
    - Correctly mention the retailer.
    - Correctly communicate the price.
    - Not invent prices or retailers.
    - Not claim unavailable products are available.
    - Avoid irrelevant information.
    - Present alternatives clearly when alternatives exist.
    """,

    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ],

    threshold=0.8,
    model=eval_model,
)


faithfulness = FaithfulnessMetric(
    threshold=0.9,
    model=eval_model,
    include_reason=True,
)


# =========================================================
# Convert database results into DeepEval context
# =========================================================

def deals_to_context(result):
    """
    Convert ALL retrieved database deals into strings that
    DeepEval can use as retrieval context.

    We intentionally don't limit this to the top 3 because
    faithfulness should be able to verify every deal mentioned
    in the agent's response.
    """

    deals = sorted(
        result.get("deals", []),
        key=lambda deal: deal.effective_price
    )

    # top_3_deals = deals[:3]

    return [
        json.dumps(
            deal.model_dump(),
            default=str
        )
        for deal in deals
    ]
    # deals = result.get("deals", [])

    # return [
    #     json.dumps(
    #         deal.model_dump(),
    #         default=str,
    #     )
    #     for deal in deals
    # ]


# =========================================================
# Pytest Fixture
# =========================================================

@pytest.fixture(scope="module")
def deal_result():
    """
    Run the agent only ONCE.

    Both test_deal_response() and
    test_faithfulness_to_database() reuse this result.

    This prevents duplicate agent LLM calls.
    """

    result = run_agent(QUERY)

    return result


# =========================================================
# Deal Response Test
# =========================================================

def test_deal_response(deal_result):

    result = deal_result

    test_case = LLMTestCase(
        input=QUERY,
        actual_output=result["response"],
    )

    assert_test(
        test_case,
        [
            answer_relevancy,
            deal_response_quality,
        ],
    )


# =========================================================
# Database Faithfulness Test
# =========================================================

def test_faithfulness_to_database(deal_result):

    result = deal_result

    print("\n" + "=" * 100)
    print("DATABASE DEALS")
    print("=" * 100)

    for i, deal in enumerate(
        result.get("deals", []),
        start=1,
    ):
        print(
            f"{i}. "
            f"{deal.brand} {deal.model} | "
            f"RAM={deal.memory} | "
            f"Storage={deal.storage} | "
            f"Retailer={deal.retailer} | "
            f"Effective Price=₹{deal.effective_price}"
        )

    print("\n" + "=" * 100)
    print("SELECTED BEST DEALS")
    print("=" * 100)

    for label in [
        "best_deal",
        "second_best_deal",
        "third_best_deal",
    ]:
        deal = result.get(label)

        if deal:
            print(
                f"{label}: "
                f"{deal.brand} {deal.model} | "
                f"{deal.retailer} | "
                f"₹{deal.effective_price}"
            )
        else:
            print(f"{label}: None")

    print("\n" + "=" * 100)
    print("LLM RESPONSE")
    print("=" * 100)

    print(result["response"])

    print("\n" + "=" * 100)
    print("RETRIEVAL CONTEXT")
    print("=" * 100)

    retrieval_context = deals_to_context(result)

    for context in retrieval_context:
        print(context)

    print("=" * 100)

    test_case = LLMTestCase(
        input=QUERY,
        actual_output=result["response"],
        retrieval_context=retrieval_context,
    )

    assert_test(
        test_case,
        [faithfulness],
    )

# uv run pytest tests/test_deepeval.py -v -s
