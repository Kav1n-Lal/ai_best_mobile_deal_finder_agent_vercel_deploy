
from langchain_core.tools import tool

from best_mobile_deal_finder_agent.db import get_connection


@tool
def get_only_the_available_mobile_brands() -> list[str]:
    """Get all phone brands available in the PostgreSQL database."""

    query = """
        SELECT DISTINCT brand
        FROM retailer_data
        WHERE brand IS NOT NULL
        ORDER BY brand;
    """

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

    return [row["brand"] for row in rows]


@tool
def get_available_mobile_brands_and_models() -> list[dict]:
    """Get all unique phone brand and model combinations."""

    query = """
        SELECT DISTINCT
            brand,
            model
        FROM retailer_data
        WHERE brand IS NOT NULL
          AND model IS NOT NULL
        ORDER BY brand, model;
    """

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

    return [
        {
            "brand": row["brand"],
            "model": row["model"],
        }
        for row in rows
    ]


@tool
def get_retailer_count() -> int:
    """Get the number of unique retailers selling phones."""

    query = """
        SELECT COUNT(DISTINCT retailer) AS retailer_count
        FROM retailer_data
        WHERE retailer IS NOT NULL;
    """

    with get_connection() as conn:
        row = conn.execute(query).fetchone()

    return row["retailer_count"]




@tool
def check_delivery_charge(
    brand: str,
    model: str,
    retailer: str,
) -> dict:
    """Check the delivery charge for a specific phone at a specific retailer."""

    query = """
        SELECT
            retailer,
            brand,
            model,
            delivery_charge,
            availability
        FROM retailer_data
        WHERE LOWER(brand) = LOWER(%s)
          AND LOWER(model) = LOWER(%s)
          AND LOWER(retailer) = LOWER(%s)
        LIMIT 1;
    """

    with get_connection() as conn:
        row = conn.execute(
            query,
            (brand, model, retailer),
        ).fetchone()

    if not row:
        return {
            "found": False,
            "message": "No matching phone listing found.",
        }

    return {
        "found": True,
        "retailer": row["retailer"],
        "brand": row["brand"],
        "model": row["model"],
        "delivery_charge": row["delivery_charge"],
        "availability": row["availability"],
    }
