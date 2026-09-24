import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

# ---------------------------------------------------------
# SQLite database
# ---------------------------------------------------------

DB_PATH = "chat_memory.sqlite"


# ---------------------------------------------------------
# SQLite connection
# ---------------------------------------------------------

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False,
)


# ---------------------------------------------------------
# LangGraph checkpointer
# ---------------------------------------------------------

memory = SqliteSaver(conn)



