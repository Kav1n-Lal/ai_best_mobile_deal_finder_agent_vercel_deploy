from langchain_core.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph

from best_mobile_deal_finder_agent.llm import (
    extract_product_details,
    generate_deal_response,
    route_query,
)
from best_mobile_deal_finder_agent.memory import (
    memory,
)
from best_mobile_deal_finder_agent.mobile_info_agent import mobile_data_agent
from best_mobile_deal_finder_agent.models import PhoneDeal, ProductQuery
from best_mobile_deal_finder_agent.services.deals import (
    search_deals,
)
from best_mobile_deal_finder_agent.summary_agent import generate_chat_summary


class GraphState(MessagesState):

    user_query: str
    route: str

    extracted_query: ProductQuery

    deals: list[PhoneDeal]

    best_deal: PhoneDeal | None

    alternatives: list[PhoneDeal]

    response: str


# ---------------------------------------------------------
# Router
# ---------------------------------------------------------

def route_node(state: GraphState):

    messages = state.get("messages", [])

    result = route_query(
        user_query=state["user_query"],
        messages=messages[-10:],
    )

    print({
        "route": result.route
    })

    print("*" * 100)

    return {
        "route": result.route
    }


def route_after_classification(state: GraphState):

    if state["route"] == "deal":
        return "extract"

    if state["route"] == "summarize":
        return "summarize"

    return "mobile_info"


# ---------------------------------------------------------
# Summarization
# ---------------------------------------------------------

# def summarize_node(state: GraphState):

#     thread_id = state["user_id"]

#     history = get_chat_history(thread_id)

#     if not history:

#         response = (
#             "I don't have any previous conversation history "
#             "to summarize."
#         )

#         return {
#             "response": response,
#             "messages": [
#                 AIMessage(content=response)
#             ],
#         }

#     summary = generate_chat_summary(history)

#     return {
#         "response": summary,
#         "messages": [
#             AIMessage(content=summary)
#         ],
#     }

# ---------------------------------------------------------
# Conversation summary
# ---------------------------------------------------------

def summarize_node(state: GraphState):

    response = generate_chat_summary(
        state["messages"]
    )

    return {
        "response": response
    }



# ---------------------------------------------------------
# Mobile information
# ---------------------------------------------------------

def mobile_info_node(state: GraphState):

    response = mobile_data_agent(
        state["user_query"]
    )

    return {
        "response": response,
        "messages": [
            AIMessage(content=response)
        ],
    }


# ---------------------------------------------------------
# Deal extraction
# ---------------------------------------------------------

def extract_node(state: GraphState):

    query = extract_product_details(
        state["user_query"],
        state.get("messages", [])
    )

    print({
        "details_extracted_from_query": query.model_dump()
    })

    print("*" * 100)

    return {
        "extracted_query": query
    }


def after_extract(state: GraphState):

    query = state["extracted_query"]

    if query.budget is None:
        return "missing_budget"

    return "search"


def missing_budget_node(state: GraphState):

    response = (
        "Please provide your mobile phone budget "
        "before I search for the best deal. "
        "For example: 'iPhone 16 under ₹70,000'."
    )

    return {
        "response": response,
        "messages": [
            AIMessage(content=response)
        ],
    }


# ---------------------------------------------------------
# Retailer search
# ---------------------------------------------------------

def retailer_search_node(state: GraphState):

    deals = search_deals(
        state["extracted_query"]
    )

    return {
        "deals": deals
    }


# ---------------------------------------------------------
# Select best deal
# ---------------------------------------------------------

def best_deal_node(state: GraphState):

    deals = state.get("deals", [])

    available = list(deals)

    print('\n')
    print('Available Deals')
    print('\n')
    print(available)

    available.sort(
        key=lambda deal: deal.effective_price
    )

    if not available:
        return {
            "best_deal": None,
            "alternatives": []
        }

    best = available[0]

    alternatives = []

    used_retailers = {best.retailer}

    for deal in available[1:]:

        if deal.retailer in used_retailers:
            continue

        alternatives.append(deal)
        used_retailers.add(deal.retailer)

        if len(alternatives) == 2:
            break

    return {
        "best_deal": best,
        "alternatives": alternatives
    }


# ---------------------------------------------------------
# Generate deal response
# ---------------------------------------------------------

def response_node(state: GraphState):

    response = generate_deal_response(
        user_query=state["user_query"],
        extracted_query=state["extracted_query"],
        best_deal=state.get("best_deal"),
        alternatives=state.get("alternatives", []),
        messages=state.get("messages", []),
    )

    print(response)

    return {
        "response": response,
        "messages": [
            AIMessage(content=response)
        ],
    }


# =========================================================
# Build graph
# =========================================================

builder = StateGraph(GraphState)


builder.add_node(
    "route",
    route_node
)

builder.add_node(
    "summarize",
    summarize_node
)

builder.add_node(
    "extract",
    extract_node
)

builder.add_node(
    "missing_budget",
    missing_budget_node
)

builder.add_node(
    "search_retailers",
    retailer_search_node
)

builder.add_node(
    "select_best_deal",
    best_deal_node
)

builder.add_node(
    "generate_response",
    response_node
)

builder.add_node(
    "mobile_info",
    mobile_info_node
)


# ---------------------------------------------------------
# Edges
# ---------------------------------------------------------

builder.add_edge(
    START,
    "route"
)


builder.add_conditional_edges(
    "route",
    route_after_classification,
    {
        "extract": "extract",
        "summarize": "summarize",
        "mobile_info": "mobile_info",
    }
)


builder.add_conditional_edges(
    "extract",
    after_extract,
    {
        "search": "search_retailers",
        "missing_budget": "missing_budget",
    }
)


builder.add_edge(
    "missing_budget",
    END
)


builder.add_edge(
    "search_retailers",
    "select_best_deal"
)


builder.add_edge(
    "select_best_deal",
    "generate_response"
)


builder.add_edge(
    "generate_response",
    END
)


builder.add_edge(
    "mobile_info",
    END
)


builder.add_edge(
    "summarize",
    END
)


graph = builder.compile(
    checkpointer=memory
)
