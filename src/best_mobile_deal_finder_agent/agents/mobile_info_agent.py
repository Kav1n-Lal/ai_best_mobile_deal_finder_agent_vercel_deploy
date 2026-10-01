from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

from best_mobile_deal_finder_agent.config import settings

from best_mobile_deal_finder_agent.tools.mobile_tools import (
    get_only_the_available_mobile_brands,
    get_available_mobile_brands_and_models,
    get_retailer_count,
    check_delivery_charge,
)


llm = ChatOpenAI(
    model=settings.openrouter_model,
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    temperature=0,
    max_completion_tokens=500
)

# llm = ChatOpenAI(
#     model="qwen3:8b",
#     base_url="http://localhost:11434/v1",
#     api_key="ollama",
#     temperature=0,
# )





mobile_tools = [
    get_only_the_available_mobile_brands,
    get_available_mobile_brands_and_models,
    get_retailer_count,
    check_delivery_charge,
]

mobile_llm = llm.bind_tools(mobile_tools)


TOOL_MAP = {
    "get_only_the_available_mobile_brands": get_only_the_available_mobile_brands,
    "get_available_mobile_brands_and_models": get_available_mobile_brands_and_models,
    "get_retailer_count": get_retailer_count,
    "check_delivery_charge": check_delivery_charge,
}


def mobile_data_agent(user_query: str) -> str:

    messages = [
        SystemMessage(
            content="""
                You are a mobile phone information assistant.

                Answer questions using the available tools.

                You can answer questions about:
                - available phone brands
                - available phone models
                - retailers
                - delivery charges
                - cheapest mobile brands
                - phone availability
                - stock
                - warranty
                - other information contained in the retailer database

                IMPORTANT:
                - Always use a tool when the answer depends on retailer database information.
                - Never invent information.
                - If the database does not contain the requested information,
                clearly say that the information is unavailable.
                """
        ),
        HumanMessage(content=user_query),
    ]

    max_iterations = 5

    for iteration in range(max_iterations):

        print(f"\n--- LLM ITERATION {iteration + 1} ---")

        response = mobile_llm.invoke(messages)

        print("LLM RESPONSE:")
        print(response)

        print("CONTENT:")
        print(response.content)

        print("TOOL CALLS:")
        print(response.tool_calls)

        messages.append(response)

        # -----------------------------------------
        # LLM has finished
        # -----------------------------------------

        if not response.tool_calls:
            return response.content

        # -----------------------------------------
        # Execute requested tools
        # -----------------------------------------

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            print(f"\nCALLING TOOL: {tool_name}")
            print(f"ARGS: {tool_args}")

            tool = TOOL_MAP.get(tool_name)

            if tool is None:

                tool_result = {
                    "error": f"Unknown tool: {tool_name}"
                }

            else:

                try:
                    tool_result = tool.invoke(tool_args)

                except Exception as e:

                    tool_result = {
                        "error": str(e)
                    }

            print("TOOL RESULT:")
            print(tool_result)

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id,
                )
            )

    return "I was unable to retrieve the requested mobile information."

