from langchain_openai import ChatOpenAI

from best_mobile_deal_finder_agent.config import settings

from best_mobile_deal_finder_agent.models import ProductQuery, QueryRoute

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatOpenAI(
    model=settings.openrouter_model,
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    temperature=0,
    max_completion_tokens=500,
)

# llm = ChatOpenAI(
#     model="qwen3:8b",
#     base_url="http://localhost:11434/v1",
#     api_key="ollama",
#     temperature=0,
# )

# ---------------------------------------------------------
# Query Router
# ---------------------------------------------------------

router_llm = llm.with_structured_output(QueryRoute)


def route_query(
    user_query: str,
    messages: list[BaseMessage] | None = None,
) -> QueryRoute:
    """
    Determine whether the user wants:

    - deal: phone/deal search or recommendations
    - summarize: summary/recap of the conversation
    - mobile_info: general mobile-phone information

    Conversation history is used to understand follow-up queries.
    """

    messages = messages or []

    conversation = []

    for message in messages:
        conversation.append(f"{message.type}: {message.content}")

    history = "\n".join(conversation)

    response = router_llm.invoke(
        [
            {
                "role": "system",
                "content": """
    You classify mobile phone conversations.

    Return exactly ONE of these categories:

    1. deal
    2. summarize
    3. mobile_info


    =========================================================
    CATEGORY: summarize
    =========================================================

    Use "summarize" when the user wants a summary, recap,
    overview, or condensed version of the PREVIOUS conversation.

    This includes requests such as:

    - summarize our conversation
    - summarize our chat
    - summarize everything
    - give me a summary
    - what have we talked about?
    - what did we discuss?
    - recap our conversation
    - recap our chat
    - give me an overview of our discussion
    - summarize what we discussed about phones
    - summarize the conversation so far
    - what have we discussed so far?

    IMPORTANT:

    If the user explicitly asks to summarize, recap, review,
    or give an overview of the conversation/history, ALWAYS
    classify it as "summarize".

    Do NOT classify a summary request as "deal" just because
    the conversation contains phone deals.

    Do NOT classify a summary request as "mobile_info" just
    because the conversation contains mobile-phone information.


    =========================================================
    CATEGORY: deal
    =========================================================

    Use "deal" when the user wants to find, compare, calculate,
    or recommend a phone deal.

    This includes:

    - finding phones
    - finding prices
    - comparing prices
    - cheapest phone
    - best deal
    - best offer
    - discounts
    - retailer deals
    - phone recommendations based on budget
    - phones under a specific budget
    - comparing retailer prices
    - finding the cheapest retailer
    - asking for alternatives to a deal


    Examples:

    "Find me an iPhone"
    => deal

    "Which retailer has the cheapest iPhone 16?"
    => deal

    "Show me the best iPhone 16 deal"
    => deal

    "iPhone 16 under 75000"
    => deal

    "Find Samsung phones under ₹50,000"
    => deal

    "Is there a cheaper option?"
    => deal

    "Show me another retailer"
    => deal


    =========================================================
    CATEGORY: mobile_info
    =========================================================

    Use "mobile_info" when the user asks for factual or
    general information about mobile phones, brands, models,
    retailers, delivery, warranty, stock, specifications,
    availability, or related topics.

    Examples:

    "What brands are available?"
    => mobile_info

    "How many retailers sell phones?"
    => mobile_info

    "What brands and models are available?"
    => mobile_info

    "Does Retailer A charge delivery for iPhone 16?"
    => mobile_info

    "What is the battery capacity of the iPhone 16?"
    => mobile_info

    "When was the Samsung S25 released?"
    => mobile_info

    "Does this phone have wireless charging?"
    => mobile_info


    =========================================================
    FOLLOW-UP QUESTIONS
    =========================================================

    Use the conversation history to understand follow-up
    questions.

    If the current query is a continuation of a previous
    shopping/deal conversation, classify it as "deal" when
    the user is still discussing:

    - prices
    - phones
    - retailers
    - budgets
    - recommendations
    - deals
    - alternatives

    For example:

    Previous:
    "I want an iPhone under ₹70,000"

    Current:
    "Can you find a cheaper one?"

    => deal


    If the current query is a continuation of a factual/mobile
    information conversation, classify it as "mobile_info".

    For example:

    Previous:
    "Does the iPhone 16 support MagSafe?"

    Current:
    "What about the iPhone 15?"

    => mobile_info


    =========================================================
    SUMMARY HAS PRIORITY
    =========================================================

    If the current query asks to summarize, recap, condense,
    review, or give an overview of the previous conversation,
    ALWAYS return "summarize", regardless of what the previous
    conversation was about.

    For example:

    Previous:
    "Find me an iPhone 16 under ₹70,000"

    Current:
    "Summarize our conversation"

    => summarize


    Previous:
    "Does the iPhone 16 support MagSafe?"

    Current:
    "What have we talked about so far?"

    => summarize


    Previous:
    "Find Samsung phones under ₹50,000"

    Current:
    "Give me a summary of everything"

    => summarize


    =========================================================
    OUTPUT
    =========================================================

    Return exactly ONE category:

    deal

    summarize

    mobile_info

    Do not return explanations.
    """,
            },
            {
                "role": "user",
                "content": f"""
    Conversation history:

    {history}

    Current user query:

    {user_query}
    """,
            },
        ]
    )

    return response


# ---------------------------------------------------------
# Product Query Extraction
# ---------------------------------------------------------

structured_llm = llm.with_structured_output(ProductQuery)


def extract_product_details(user_query: str, messages) -> ProductQuery:

    history = "\n".join(
        f"{message.type}: {message.content}" for message in messages[:-1]
    )

    response = structured_llm.invoke(
        [
            {
                "role": "system",
                "content": f"""
You extract structured phone requirements from a user's request.

Use the previous conversation when the current request
is a follow-up to an earlier request.

Previous conversation:

{history}

Return:

- brand
- memory
- storage
- budget

Rules:

- brand means phone manufacturer.
- memory means RAM.
- storage means internal storage.
- budget means the maximum effective price the user is willing to pay.

Examples:

"Samsung 8GB 256GB"
brand = Samsung
memory = 8GB
storage = 256GB

"iPhone 16 256GB"
brand = Apple
memory = null
storage = 256GB

"under 70000"
budget = 70000

If the current request doesn't explicitly repeat
a requirement, use the previous conversation when
appropriate.

Do not invent requirements.
""",
            },
            {
                "role": "user",
                "content": user_query,
            },
        ]
    )

    return response


def generate_deal_response(
    user_query: str,
    extracted_query: ProductQuery,
    best_deal,
    second_best_deal,
    third_best_deal,
    messages,
):

    best_deal_text = (
        best_deal.model_dump_json() if best_deal else "No available deal found."
    )

    second_best_deal_text=(
        second_best_deal.model_dump_json() if second_best_deal else "No available deal found."
    )

    third_best_deal_text=(
            third_best_deal.model_dump_json() if third_best_deal else "No available deal found."
        )

    # alternatives_text = "\n".join(deal.model_dump_json() for deal in alternatives)

    prompt = f"""
You are a helpful mobile phone deal assistant.

Current user request:

{user_query}

Extracted requirements:

{extracted_query.model_dump_json()}

Best available deal:

{best_deal_text}

Second best deal:

{second_best_deal_text}

third best deal:

{third_best_deal_text}

Rules:

1. Use the conversation history to understand follow-up questions.

2. If the user refers to something previously discussed,
   use the previous conversation to resolve the reference.

3. Do not invent information, be factual while interpreting bank offers,discount, cash back, delivery charges,exchange bonus,etc.

4. The effective_price provided by the database is the
   authoritative deal price.

5. Do not recalculate effective_price.

6. If there is no matching available deal, clearly say so.

7. Keep the response concise.

8. If the user asks to summarize the conversation,
   summarize the conversation using the previous messages.
"""

    # Don't pass the current user message twice.
    previous_messages = messages[:-1]

    response = llm.invoke(
        [
            SystemMessage(content=prompt),
            *previous_messages,
            HumanMessage(content=user_query),
        ]
    )

    return response.content
