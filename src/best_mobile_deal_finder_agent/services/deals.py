
from best_mobile_deal_finder_agent.db import get_connection
from best_mobile_deal_finder_agent.models import PhoneDeal, ProductQuery


def search_deals(query: ProductQuery) -> list[PhoneDeal]:

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
        FROM retailer_data
        WHERE availability = 't'
                  AND stock_count > 0
                  AND effective_price IS NOT NULL
    """

    params = []

    if query.brand:
        sql += " AND LOWER(brand) = LOWER(%s)"
        params.append(query.brand)
        # print(':::::::::brand: ',sql)
        # print('*'*300)

    if query.memory:
        sql += " AND LOWER(memory) = LOWER(%s)"
        params.append(query.memory)

    if query.storage:
        sql += " AND LOWER(storage) = LOWER(%s)"
        params.append(query.storage)

    # Budget = maximum effective price
    if query.budget is not None:
        sql += " AND effective_price <= %s"
        params.append(query.budget)

    sql += """
        ORDER BY effective_price ASC
    """

    with get_connection() as conn:

        rows = conn.execute(
            sql,
            params
        ).fetchall()

    return [
        PhoneDeal(**row)
        for row in rows
    ]



def get_best_deal(query: ProductQuery) -> PhoneDeal | None:

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
        FROM retailer_data
        WHERE effective_price IS NOT NULL
          
    """

    params = []

    if query.brand:
        sql += " AND LOWER(brand) = LOWER(%s)"
        params.append(query.brand)

    if query.memory:
        sql += " AND LOWER(memory) = LOWER(%s)"
        params.append(query.memory)

    if query.storage:
        sql += " AND LOWER(storage) = LOWER(%s)"
        params.append(query.storage)

    # Budget = maximum effective price
    if query.budget is not None:
        sql += " AND effective_price <= %s"
        params.append(query.budget)

    sql += """
        ORDER BY effective_price ASC
        LIMIT 1
    """

    with get_connection() as conn:

        row = conn.execute(
            sql,
            params
        ).fetchone()

    if not row:
        return None

    return PhoneDeal(**row)
