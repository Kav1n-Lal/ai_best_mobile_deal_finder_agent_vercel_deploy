from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from best_mobile_deal_finder_agent.graph import graph
from best_mobile_deal_finder_agent.memory import memory
from best_mobile_deal_finder_agent.db import get_connection

from uuid import UUID


app = FastAPI(
    title="Best Mobile Deals Agent",
    description="AI-powered mobile phone deal comparison agent",
    version="1.0.0",
)


# ---------------------------------------------------------
# Templates / Static files
# ---------------------------------------------------------

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class DealRequest(BaseModel):
    query: str
    thread_id: UUID



# ---------------------------------------------------------
# Pages
# ---------------------------------------------------------

@app.get("/")
def root():
    return RedirectResponse(url="/thread")


@app.get("/thread")
def thread_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/chat")
def chat_page(
    request: Request,
    thread_id: str,
):
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "thread_id": thread_id,
        },
    )

# ---------------------------------------------------------
# Deals API
# ---------------------------------------------------------

@app.post("/deals")
def find_best_deal(request: DealRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    if not str(request.thread_id).strip():
        raise HTTPException(
            status_code=400,
            detail="thread_id cannot be empty.",
        )

    config = {
        "configurable": {
            "thread_id": str(request.thread_id),
        }
    }

    try:
        

        result = graph.invoke(
        {
            "user_query": request.query,
            "messages": [
                HumanMessage(content=request.query)
            ],
        },
        config=config,
)


        best_deal = result.get("best_deal")
        extracted_query = result.get("extracted_query")

        second_best_deal = result.get("second_best_deal")
        third_best_deal = result.get("third_best_deal")

        return {
            "query": request.query,

            "route": result.get("route"),

            "extracted": (
                extracted_query.model_dump()
                if extracted_query
                else None
            ),

            "best_deal": (
                best_deal.model_dump()
                if best_deal
                else None
            ),

            "alternatives": [
                deal.model_dump()
                for deal in [
                    second_best_deal,
                    third_best_deal,
                ]
                if deal
            ],

            "response": result.get("response", ""),
        }


    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process deal request: {exc!s}",
        ) from exc


@app.get("/history/{thread_id}")
def get_chat_history(thread_id: str):

    if not thread_id.strip():
        raise HTTPException(
            status_code=400,
            detail="thread_id cannot be empty.",
        )

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    try:

        state = graph.get_state(config)

        messages = []

        for message in state.values.get(
            "messages",
            []
        ):

            messages.append({
                "type": message.type,
                "content": message.content,
            })

        return {
            "thread_id": thread_id,
            "messages": messages,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to load chat history: {exc!s}",
        ) from exc

# @app.get("/history/{thread_id}")
# def get_chat_history(thread_id: UUID):
#     thread_id_str = str(thread_id)

#     config = {
#         "configurable": {
#             "thread_id": thread_id_str,
#         }
#     }

#     try:
#         state = graph.get_state(config)

#         messages = []

#         for message in state.values.get("messages", []):
#             messages.append({
#                 "type": message.type,
#                 "content": message.content,
#             })

#         return {
#             "thread_id": thread_id_str,
#             "messages": messages,
#         }

#     except Exception as exc:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to load chat history: {exc!s}",
#         ) from exc


@app.delete("/history/{thread_id}")
def clear_chat_history(thread_id: str):

    if not thread_id.strip():
        raise HTTPException(
            status_code=400,
            detail="thread_id cannot be empty.",
        )

    try:

        memory.delete_thread(
            thread_id
        )

        return {
            "success": True,
            "thread_id": thread_id,
            "message": "Chat history cleared.",
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear chat history: {exc!s}",
        ) from exc

# ---------------------------------------------------------
# Debug
# ---------------------------------------------------------

@app.get("/debug/{thread_id}")
def debug_thread(
    thread_id: str,
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }


    state = graph.get_state(
        config
    )


    messages = []


    for message in state.values.get(
        "messages",
        [],
    ):

        messages.append({

            "type": message.type,

            "content": message.content,
        })


    return {

        "thread_id": thread_id,

        "messages": messages,
    }