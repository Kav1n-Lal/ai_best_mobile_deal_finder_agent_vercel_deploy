# tests/agent_runner.py

from uuid import uuid4

from best_mobile_deal_finder_agent.graph import graph


def run_agent(
    user_query: str,
    thread_id: str | None = None,
):
    """
    Execute one turn of the mobile deals LangGraph.

    Returns the complete graph state so tests can inspect
    both the final response and intermediate results.
    """

    if thread_id is None:
        thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
        {
            "user_query": user_query,
            "messages": [],
        },
        config=config,
    )

    return result
