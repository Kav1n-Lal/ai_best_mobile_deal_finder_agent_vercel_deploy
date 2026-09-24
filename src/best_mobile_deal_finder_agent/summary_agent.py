from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen3:8b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0,
)


def generate_chat_summary(messages):

    prompt = """
You are summarizing a conversation between a user and an assistant.

Create a concise but useful summary of the conversation.

Include:
- The user's main requests
- Important preferences or requirements
- Products discussed
- Decisions or conclusions
- Important unresolved questions
- Relevant context needed to continue the conversation

Do not invent information.

Conversation:
"""

    conversation_text = "\n".join(
        f"{message.type}: {message.content}" for message in messages
    )

    response = llm.invoke([HumanMessage(content=prompt + "\n\n" + conversation_text)])

    return response.content
