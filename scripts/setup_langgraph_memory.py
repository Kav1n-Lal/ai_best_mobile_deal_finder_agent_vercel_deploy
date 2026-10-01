import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import connect
from psycopg.rows import dict_row


load_dotenv(override=True)


DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "NEON_DATABASE_URL is not set."
    )


def main():

    with connect(
        DATABASE_URL,
        autocommit=True,
        row_factory=dict_row,
    ) as conn:

        checkpointer = PostgresSaver(conn)

        checkpointer.setup()

    print(
        "LangGraph PostgreSQL checkpointer setup complete."
    )


if __name__ == "__main__":
    main()


# Neon db
# │
# ├── retailer_data
# │
# ├── checkpoints
# │
# ├── checkpoint_blobs
# │
# ├── checkpoint_writes
# │
# └── checkpoint_migrations

# uv run python scripts/setup_memory.py
