from langchain_core.tools import tool
from best_mobile_deal_finder_agent.db import get_connection

@tool
def get_only_the_available_mobile_brands() -> list[str]:
    """Get all phone brands currently available in the database."""

    query = """
        SELECT DISTINCT brand
        FROM retailer_data
        WHERE brand IS NOT NULL
          AND availability = TRUE
        ORDER BY brand;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return [row[0] for row in rows]


@tool
def get_available_mobile_brands_and_models() -> list[dict]:
    """Get all unique available phone brand and model combinations."""

    query = """
        SELECT DISTINCT
            brand,
            model
        FROM retailer_data
        WHERE brand IS NOT NULL
          AND model IS NOT NULL
          AND availability = TRUE
        ORDER BY brand, model;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return [
        {
            "brand": row[0],
            "model": row[1],
        }
        for row in rows
    ]


@tool
def get_retailer_count() -> int:
    """Get the number of unique retailers currently selling available phones."""

    query = """
        SELECT COUNT(DISTINCT retailer)
        FROM retailer_data
        WHERE retailer IS NOT NULL
          AND availability = TRUE;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

    return row[0] if row else 0


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
        ORDER BY updated_at DESC
        LIMIT 1;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (brand, model, retailer),
            )

            row = cursor.fetchone()

    if not row:
        return {
            "found": False,
            "message": "No matching phone listing found.",
        }

    return {
        "found": True,
        "retailer": row[0],
        "brand": row[1],
        "model": row[2],
        "delivery_charge": row[3],
        "availability": row[4],
    }



