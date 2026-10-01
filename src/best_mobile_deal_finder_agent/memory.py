# import sqlite3

# from langgraph.checkpoint.sqlite import SqliteSaver

# # ---------------------------------------------------------
# # SQLite database
# # ---------------------------------------------------------

# DB_PATH = "chat_memory.sqlite"


# # ---------------------------------------------------------
# # SQLite connection
# # ---------------------------------------------------------

# conn = sqlite3.connect(
#     DB_PATH,
#     check_same_thread=False,
# )


# # ---------------------------------------------------------
# # LangGraph checkpointer
# # ---------------------------------------------------------

# memory = SqliteSaver(conn)

# import os

# from dotenv import load_dotenv
# from langgraph.checkpoint.postgres import PostgresSaver
# from psycopg_pool import ConnectionPool


# load_dotenv(override=True)


# DATABASE_URL = os.getenv("NEON_DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError(
#         "NEON_DATABASE_URL is not set."
#     )


# pool = ConnectionPool(
#     conninfo=DATABASE_URL,
#     min_size=1,
#     max_size=5,
#     kwargs={
#         "autocommit": True,
#     },
# )


# memory = PostgresSaver(pool)

import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool


load_dotenv()

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("NEON_DATABASE_URL is not set.")


pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=0,
    max_size=2,
    kwargs={
        "autocommit": True,
    },
    open=False,
)

pool.open(wait=False)

memory = PostgresSaver(pool)


#                     Neon db
#                       │
#           ┌───────────┴───────────┐
#           │                       │
#           ▼                       ▼
#      psycopg2                  psycopg 3
#        db.py                    memory.py
#           │                       │
#           ▼                       ▼
#   retailer_data             PostgresSaver
#                                   │
#                                   ▼
#                          LangGraph checkpoints
