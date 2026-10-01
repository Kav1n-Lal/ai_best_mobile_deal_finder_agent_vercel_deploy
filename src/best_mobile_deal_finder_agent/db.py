import psycopg
from psycopg.rows import dict_row

from best_mobile_deal_finder_agent.config import settings
from sqlalchemy import create_engine

#local postgres connection
# def get_connection():
#     return psycopg.connect(
#         host=settings.db_host,
#         port=settings.db_port,
#         dbname=settings.db_name,
#         user=settings.db_user,
#         password=settings.db_password,
#         row_factory=dict_row,
#     )

import os
# import psycopg2
from dotenv import load_dotenv
load_dotenv(override=True)

#neon db connection
def get_connection():
    database_url = os.getenv("NEON_DATABASE_URL")

    if not database_url:
        raise ValueError(
            "NEON_DATABASE_URL is not set in your .env file."
        )

    return psycopg.connect(database_url)

