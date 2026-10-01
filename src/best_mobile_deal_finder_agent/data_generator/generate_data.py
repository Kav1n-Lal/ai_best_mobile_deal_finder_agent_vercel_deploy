# import random

# from .connection import get_connection


# RETAILERS = [
#     "Amazon",
#     "Flipkart",
#     "Croma",
# ]


# PHONES = [
#     {
#         "brand": "Apple",
#         "model": "iPhone 16",
#         "memory": "8GB",
#         "storage": "128GB",
#         "mrp": 79999,
#         "warranty": "1 year Apple warranty",
#     },
#     {
#         "brand": "Apple",
#         "model": "iPhone 16",
#         "memory": "8GB",
#         "storage": "256GB",
#         "mrp": 89999,
#         "warranty": "1 year Apple warranty",
#     },
#     {
#         "brand": "Apple",
#         "model": "iPhone 16 Pro",
#         "memory": "8GB",
#         "storage": "256GB",
#         "mrp": 119999,
#         "warranty": "1 year Apple warranty",
#     },
#     {
#         "brand": "Apple",
#         "model": "iPhone 16 Pro Max",
#         "memory": "8GB",
#         "storage": "256GB",
#         "mrp": 139999,
#         "warranty": "1 year Apple warranty",
#     },
#     {
#         "brand": "Samsung",
#         "model": "Galaxy S25",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 84999,
#         "warranty": "1 year Samsung warranty",
#     },
#     {
#         "brand": "Samsung",
#         "model": "Galaxy S25 Ultra",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 129999,
#         "warranty": "1 year Samsung warranty",
#     },
#     {
#         "brand": "Samsung",
#         "model": "Galaxy S25 Ultra",
#         "memory": "12GB",
#         "storage": "512GB",
#         "mrp": 149999,
#         "warranty": "1 year Samsung warranty",
#     },
#     {
#         "brand": "OnePlus",
#         "model": "OnePlus 13",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 69999,
#         "warranty": "1 year OnePlus warranty",
#     },
#     {
#         "brand": "OnePlus",
#         "model": "OnePlus 13",
#         "memory": "16GB",
#         "storage": "512GB",
#         "mrp": 79999,
#         "warranty": "1 year OnePlus warranty",
#     },
#     {
#         "brand": "Google",
#         "model": "Pixel 9",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 79999,
#         "warranty": "1 year Google warranty",
#     },
#     {
#         "brand": "Google",
#         "model": "Pixel 9 Pro",
#         "memory": "16GB",
#         "storage": "256GB",
#         "mrp": 109999,
#         "warranty": "1 year Google warranty",
#     },
#     {
#         "brand": "Xiaomi",
#         "model": "Xiaomi 15",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 64999,
#         "warranty": "1 year Xiaomi warranty",
#     },
#     {
#         "brand": "Nothing",
#         "model": "Nothing Phone 3",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 59999,
#         "warranty": "1 year Nothing warranty",
#     },
#     {
#         "brand": "Vivo",
#         "model": "Vivo X200",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 65999,
#         "warranty": "1 year Vivo warranty",
#     },
#     {
#         "brand": "Oppo",
#         "model": "Oppo Find X8",
#         "memory": "12GB",
#         "storage": "256GB",
#         "mrp": 69999,
#         "warranty": "1 year Oppo warranty",
#     },
# ]


# def generate_deal(retailer, phone):

#     mrp = phone["mrp"]

#     discount = random.choice([
#         2000,
#         3000,
#         4000,
#         5000,
#         6000,
#         7000,
#         8000,
#     ])

#     selling_price = mrp - discount

#     cashback = random.choice([
#         0,
#         500,
#         1000,
#         1500,
#         2000,
#         2500,
#         3000,
#     ])

#     bank_offer = random.choice([
#         0,
#         500,
#         1000,
#         1500,
#         2000,
#         2500,
#     ])

#     exchange_bonus = random.choice([
#         0,
#         500,
#         1000,
#         1500,
#         2000,
#         2500,
#     ])

#     delivery_charge = random.choice([
#         0,
#         0,
#         0,
#         49,
#         99,
#         149,
#     ])

#     availability = random.random() > 0.12

#     if availability:
#         stock_count = random.randint(1, 30)
#     else:
#         stock_count = 0

#     effective_price = (
#         selling_price
#         - cashback
#         - bank_offer
#         - exchange_bonus
#         + delivery_charge
#     )

#     return (
#         retailer,
#         phone["brand"],
#         phone["model"],
#         phone["memory"],
#         phone["storage"],
#         mrp,
#         selling_price,
#         discount,
#         cashback,
#         bank_offer,
#         exchange_bonus,
#         delivery_charge,
#         availability,
#         stock_count,
#         phone["warranty"],
#         effective_price,
#     )


# def generate_data():

#     data = []

#     for retailer in RETAILERS:

#         for _ in range(100):

#             phone = random.choice(PHONES)

#             data.append(
#                 generate_deal(
#                     retailer,
#                     phone
#                 )
#             )

#     return data


# def insert_data(data):

#     connection = get_connection()

#     query = """
#         INSERT INTO retailer_data (
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
#         )
#         VALUES (
#             %s, %s, %s, %s, %s,
#             %s, %s, %s, %s, %s,
#             %s, %s, %s, %s, %s,
#             %s
#         )
#     """

#     try:

#         with connection.cursor() as cursor:

#             cursor.executemany(
#                 query,
#                 data
#             )

#         connection.commit()

#         print(
#             f"Successfully inserted {len(data)} records."
#         )

#     except Exception as error:

#         connection.rollback()

#         print("Database error:")
#         print(error)

#     finally:

#         connection.close()


# def main():

#     data = generate_data()

#     print(f"Generated {len(data)} records.")

#     insert_data(data)


# if __name__ == "__main__":
#     main()

import random
from datetime import datetime, timezone

from best_mobile_deal_finder_agent.data_generator.connection import get_connection


RETAILERS = [
    "Amazon",
    "Flipkart",
    "Croma",
]


# Base phone catalog.
# We will generate 100 comparable product variants
# from these products.
PHONES = [
    {
        "brand": "Apple",
        "model": "iPhone 16",
        "memory": "8GB",
        "storage": "128GB",
        "mrp": 79999,
        "warranty": "1 year Apple warranty",
    },
    {
        "brand": "Apple",
        "model": "iPhone 16",
        "memory": "8GB",
        "storage": "256GB",
        "mrp": 89999,
        "warranty": "1 year Apple warranty",
    },
    {
        "brand": "Apple",
        "model": "iPhone 16 Pro",
        "memory": "8GB",
        "storage": "256GB",
        "mrp": 119999,
        "warranty": "1 year Apple warranty",
    },
    {
        "brand": "Apple",
        "model": "iPhone 16 Pro Max",
        "memory": "8GB",
        "storage": "256GB",
        "mrp": 139999,
        "warranty": "1 year Apple warranty",
    },
    {
        "brand": "Samsung",
        "model": "Galaxy S25",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 84999,
        "warranty": "1 year Samsung warranty",
    },
    {
        "brand": "Samsung",
        "model": "Galaxy S25 Ultra",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 129999,
        "warranty": "1 year Samsung warranty",
    },
    {
        "brand": "Samsung",
        "model": "Galaxy S25 Ultra",
        "memory": "12GB",
        "storage": "512GB",
        "mrp": 149999,
        "warranty": "1 year Samsung warranty",
    },
    {
        "brand": "OnePlus",
        "model": "OnePlus 13",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 69999,
        "warranty": "1 year OnePlus warranty",
    },
    {
        "brand": "OnePlus",
        "model": "OnePlus 13",
        "memory": "16GB",
        "storage": "512GB",
        "mrp": 79999,
        "warranty": "1 year OnePlus warranty",
    },
    {
        "brand": "Google",
        "model": "Pixel 9",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 79999,
        "warranty": "1 year Google warranty",
    },
    {
        "brand": "Google",
        "model": "Pixel 9 Pro",
        "memory": "16GB",
        "storage": "256GB",
        "mrp": 109999,
        "warranty": "1 year Google warranty",
    },
    {
        "brand": "Xiaomi",
        "model": "Xiaomi 15",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 64999,
        "warranty": "1 year Xiaomi warranty",
    },
    {
        "brand": "Nothing",
        "model": "Nothing Phone 3",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 59999,
        "warranty": "1 year Nothing warranty",
    },
    {
        "brand": "Vivo",
        "model": "Vivo X200",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 65999,
        "warranty": "1 year Vivo warranty",
    },
    {
        "brand": "Oppo",
        "model": "Oppo Find X8",
        "memory": "12GB",
        "storage": "256GB",
        "mrp": 69999,
        "warranty": "1 year Oppo warranty",
    },
]


# Different retailers get different pricing behavior.
# This creates meaningful price comparisons.

RETAILER_CONFIG = {
    "Amazon": {
        "discount_min": 0.04,
        "discount_max": 0.12,
        "cashback": [0, 500, 1000, 1500, 2000, 2500],
        "bank_offer": [0, 500, 1000, 1500, 2000],
        "exchange_bonus": [0, 500, 1000, 1500, 2000],
        "delivery_charge": [0, 0, 0, 49, 99],
    },

    "Flipkart": {
        "discount_min": 0.05,
        "discount_max": 0.14,
        "cashback": [0, 500, 1000, 1500, 2000, 3000],
        "bank_offer": [0, 500, 1000, 1500, 2000, 2500],
        "exchange_bonus": [0, 500, 1000, 1500, 2000, 2500],
        "delivery_charge": [0, 0, 0, 0, 49, 99],
    },

    "Croma": {
        "discount_min": 0.03,
        "discount_max": 0.10,
        "cashback": [0, 500, 1000, 1500, 2000],
        "bank_offer": [0, 500, 1000, 1500],
        "exchange_bonus": [0, 500, 1000, 1500],
        "delivery_charge": [0, 0, 49, 99, 149],
    },
}


def generate_deal(retailer, phone):
    """
    Generate one retailer-specific deal
    for a specific phone.
    """

    config = RETAILER_CONFIG[retailer]

    mrp = phone["mrp"]

    # Generate a percentage discount.
    discount_percentage = random.uniform(
        config["discount_min"],
        config["discount_max"],
    )

    discount = int(
        mrp * discount_percentage
    )

    # Round discount to nearest 100.
    discount = round(discount / 100) * 100

    selling_price = mrp - discount

    cashback = random.choice(
        config["cashback"]
    )

    bank_offer = random.choice(
        config["bank_offer"]
    )

    exchange_bonus = random.choice(
        config["exchange_bonus"]
    )

    delivery_charge = random.choice(
        config["delivery_charge"]
    )

    # Around 90% of products are available.
    availability = random.random() < 0.90

    if availability:
        stock_count = random.randint(1, 30)
    else:
        stock_count = 0

    # Effective price represents the final comparable price.
    effective_price = (
        selling_price
        - cashback
        - bank_offer
        - exchange_bonus
        + delivery_charge
    )

    return {
        "retailer": retailer,
        "brand": phone["brand"],
        "model": phone["model"],
        "memory": phone["memory"],
        "storage": phone["storage"],
        "mrp": mrp,
        "selling_price": selling_price,
        "discount": discount,
        "cashback": cashback,
        "bank_offer": bank_offer,
        "exchange_bonus": exchange_bonus,
        "delivery_charge": delivery_charge,
        "availability": availability,
        "stock_count": stock_count,
        "warranty": phone["warranty"],
        "effective_price": effective_price,
        "updated_at": datetime.now(timezone.utc),
    }


def generate_product_catalog():
    """
    Create exactly 100 product variants.

    The original catalog contains 15 phones.
    We create additional variants by combining
    those phones with different color/storage options.

    These variants are shared across all retailers.
    """

    catalog = []

    colors = [
        "Black",
        "White",
        "Blue",
        "Green",
        "Silver",
        "Gold",
        "Titanium",
        "Purple",
        "Red",
        "Gray",
    ]

    variant_id = 1

    while len(catalog) < 100:

        phone = random.choice(PHONES)

        color = colors[
            (variant_id - 1) % len(colors)
        ]

        product = phone.copy()

        product["color"] = color
        product["variant_id"] = variant_id

        catalog.append(product)

        variant_id += 1

    return catalog


def generate_data():
    """
    Generate 100 comparable products for each retailer.

    100 products × 3 retailers = 300 records.
    """

    catalog = generate_product_catalog()

    data = []

    for retailer in RETAILERS:

        for phone in catalog:

            deal = generate_deal(
                retailer,
                phone
            )

            deal["color"] = phone["color"]

            data.append(deal)

    return data


def create_table(connection):
    """
    Create the retailer_data table.
    """

    query = """
        CREATE TABLE IF NOT EXISTS retailer_data (

            id SERIAL PRIMARY KEY,

            retailer VARCHAR(100) NOT NULL,

            brand VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            memory VARCHAR(50) NOT NULL,
            storage VARCHAR(50) NOT NULL,
            color VARCHAR(50) NOT NULL,

            mrp INTEGER NOT NULL,
            selling_price INTEGER NOT NULL,
            discount INTEGER NOT NULL,

            cashback INTEGER DEFAULT 0,
            bank_offer INTEGER DEFAULT 0,
            exchange_bonus INTEGER DEFAULT 0,
            delivery_charge INTEGER DEFAULT 0,

            availability BOOLEAN NOT NULL,
            stock_count INTEGER NOT NULL,

            warranty VARCHAR(255),

            effective_price INTEGER NOT NULL,

            updated_at TIMESTAMP WITH TIME ZONE
                DEFAULT CURRENT_TIMESTAMP
        );
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

    connection.commit()

    print("Table checked/created successfully.")


def clear_old_data(connection):
    """
    Remove previous generated data.

    This makes every run produce exactly
    300 current records instead of continuously
    adding more records.
    """

    query = """
        TRUNCATE TABLE retailer_data
        RESTART IDENTITY;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

    connection.commit()

    print("Old data cleared.")


def insert_data(connection, data):

    query = """
        INSERT INTO retailer_data (

            retailer,

            brand,
            model,
            memory,
            storage,
            color,

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

            effective_price,

            updated_at
        )

        VALUES (

            %s,

            %s, %s, %s, %s, %s,

            %s, %s, %s,

            %s, %s, %s, %s,

            %s, %s,

            %s,

            %s,

            %s
        );
    """

    values = []

    for deal in data:

        values.append(
            (
                deal["retailer"],

                deal["brand"],
                deal["model"],
                deal["memory"],
                deal["storage"],
                deal["color"],

                deal["mrp"],
                deal["selling_price"],
                deal["discount"],

                deal["cashback"],
                deal["bank_offer"],
                deal["exchange_bonus"],
                deal["delivery_charge"],

                deal["availability"],
                deal["stock_count"],

                deal["warranty"],

                deal["effective_price"],

                deal["updated_at"],
            )
        )

    with connection.cursor() as cursor:

        cursor.executemany(
            query,
            values
        )

    connection.commit()

    print(
        f"Successfully inserted {len(values)} records."
    )


def main():

    connection = None

    try:

        connection = get_connection()

        print(
            "Connected to Neon PostgreSQL."
        )

        create_table(connection)

        clear_old_data(connection)

        data = generate_data()

        print(
            f"Generated {len(data)} records."
        )

        insert_data(
            connection,
            data
        )

        print(
            "Data successfully stored in Neon."
        )

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            "Database error:"
        )

        print(error)

    finally:

        if connection:

            connection.close()

        print(
            "Database connection closed."
        )


if __name__ == "__main__":
    main()

