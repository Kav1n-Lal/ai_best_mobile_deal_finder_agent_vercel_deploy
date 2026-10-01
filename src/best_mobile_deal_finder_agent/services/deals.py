from best_mobile_deal_finder_agent.db import get_connection
from best_mobile_deal_finder_agent.models import PhoneDeal, ProductQuery


BASE_DEAL_QUERY = """
    FROM retailer_data
    WHERE availability = TRUE
      AND stock_count > 0
      AND effective_price IS NOT NULL
"""


def search_deals(query: ProductQuery) -> list[PhoneDeal]:
    """
    Search available phone deals from Neon PostgreSQL.

    Results are ordered from lowest effective price
    to highest effective price.
    """

    sql = """
        SELECT
            retailer,
            brand,
            model,
            memory,
            storage,
            mrp,
            selling_price,
            discount,
            cashback,
            bank_offer,
            exchange_bonus,
            delivery_charge,
            availability,
            stock_count,
            warranty,
            effective_price
    """ + BASE_DEAL_QUERY

    params = []

    # Filter by brand
    if query.brand:
        sql += """
            AND LOWER(brand) = LOWER(%s)
        """
        params.append(query.brand)

    # # Filter by model
    # if query.model:
    #     sql += """
    #         AND LOWER(model) = LOWER(%s)
    #     """
    #     params.append(query.model)

    # Filter by RAM
    if query.memory:
        sql += """
            AND LOWER(memory) = LOWER(%s)
        """
        params.append(query.memory)

    # Filter by storage
    if query.storage:
        sql += """
            AND LOWER(storage) = LOWER(%s)
        """
        params.append(query.storage)

    # Budget means maximum effective price
    if query.budget is not None:
        sql += """
            AND effective_price <= %s
        """
        params.append(query.budget)

    sql += """
        ORDER BY effective_price ASC
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                sql,
                params
            )

            rows = cursor.fetchall()

    return [
        PhoneDeal(
            retailer=row[0],
            brand=row[1],
            model=row[2],
            memory=row[3],
            storage=row[4],
            mrp=row[5],
            selling_price=row[6],
            discount=row[7],
            cashback=row[8],
            bank_offer=row[9],
            exchange_bonus=row[10],
            delivery_charge=row[11],
            availability=row[12],
            stock_count=row[13],
            warranty=row[14],
            effective_price=row[15],
        )
        for row in rows
    ]


# def get_best_deal(
#     query: ProductQuery
# ) -> PhoneDeal | None:
#     """
#     Get the single lowest effective-price deal
#     matching the user's product requirements.
#     """

#     sql = """
#         SELECT
#             retailer,
#             brand,
#             model,
#             memory,
#             storage,
#             mrp,
#             selling_price,
#             discount,
#             cashback,
#             bank_offer,
#             exchange_bonus,
#             delivery_charge,
#             availability,
#             stock_count,
#             warranty,
#             effective_price
#     """ + BASE_DEAL_QUERY

#     params = []

#     # Filter by brand
#     if query.brand:
#         sql += """
#             AND LOWER(brand) = LOWER(%s)
#         """
#         params.append(query.brand)

#     # # Filter by model
#     # if query.model:
#     #     sql += """
#     #         AND LOWER(model) = LOWER(%s)
#     #     """
#     #     params.append(query.model)

#     # Filter by RAM
#     if query.memory:
#         sql += """
#             AND LOWER(memory) = LOWER(%s)
#         """
#         params.append(query.memory)

#     # Filter by storage
#     if query.storage:
#         sql += """
#             AND LOWER(storage) = LOWER(%s)
#         """
#         params.append(query.storage)

#     # Budget means maximum effective price
#     if query.budget is not None:
#         sql += """
#             AND effective_price <= %s
#         """
#         params.append(query.budget)

#     sql += """
#         ORDER BY effective_price ASC
#         LIMIT 1
#     """

#     with get_connection() as conn:
#         with conn.cursor() as cursor:

#             cursor.execute(
#                 sql,
#                 params
#             )

#             row = cursor.fetchone()

#     if not row:
#         return None

#     return PhoneDeal(
#         retailer=row[0],
#         brand=row[1],
#         model=row[2],
#         memory=row[3],
#         storage=row[4],
#         mrp=row[5],
#         selling_price=row[6],
#         discount=row[7],
#         cashback=row[8],
#         bank_offer=row[9],
#         exchange_bonus=row[10],
#         delivery_charge=row[11],
#         availability=row[12],
#         stock_count=row[13],
#         warranty=row[14],
#         effective_price=row[15],
#     )


