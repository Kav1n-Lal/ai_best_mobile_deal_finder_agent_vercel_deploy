# import os

# import psycopg2
# from dotenv import load_dotenv


# load_dotenv()


# def get_connection():
#     return psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#     )

# # from database.connection import get_connection


# def main():
#     connection = get_connection()

#     print("Successfully connected to PostgreSQL!")

#     connection.close()


# if __name__ == "__main__":
#     main()

import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_url = os.getenv("NEON_DATABASE_URL")

    if not database_url:
        raise ValueError(
            "NEON DATABASE_URL is not set in your .env file."
        )

    return psycopg2.connect(database_url)


def main():
    connection = get_connection()

    print("Successfully connected to Neon PostgreSQL!")

    connection.close()


if __name__ == "__main__":
    main()

