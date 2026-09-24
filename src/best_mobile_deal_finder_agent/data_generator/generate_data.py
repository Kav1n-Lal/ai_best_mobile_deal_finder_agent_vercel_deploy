import random

from connection import get_connection


RETAILERS = [
    "Retailer A",
    "Retailer B",
    "Retailer C",
]


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


def generate_deal(retailer, phone):

    mrp = phone["mrp"]

    discount = random.choice([
        2000,
        3000,
        4000,
        5000,
        6000,
        7000,
        8000,
    ])

    selling_price = mrp - discount

    cashback = random.choice([
        0,
        500,
        1000,
        1500,
        2000,
        2500,
        3000,
    ])

    bank_offer = random.choice([
        0,
        500,
        1000,
        1500,
        2000,
        2500,
    ])

    exchange_bonus = random.choice([
        0,
        500,
        1000,
        1500,
        2000,
        2500,
    ])

    delivery_charge = random.choice([
        0,
        0,
        0,
        49,
        99,
        149,
    ])

    availability = random.random() > 0.12

    if availability:
        stock_count = random.randint(1, 30)
    else:
        stock_count = 0

    effective_price = (
        selling_price
        - cashback
        - bank_offer
        - exchange_bonus
        + delivery_charge
    )

    return (
        retailer,
        phone["brand"],
        phone["model"],
        phone["memory"],
        phone["storage"],
        mrp,
        selling_price,
        discount,
        cashback,
        bank_offer,
        exchange_bonus,
        delivery_charge,
        availability,
        stock_count,
        phone["warranty"],
        effective_price,
    )


def generate_data():

    data = []

    for retailer in RETAILERS:

        for _ in range(100):

            phone = random.choice(PHONES)

            data.append(
                generate_deal(
                    retailer,
                    phone
                )
            )

    return data


def insert_data(data):

    connection = get_connection()

    query = """
        INSERT INTO retailer_data (
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
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s
        )
    """

    try:

        with connection.cursor() as cursor:

            cursor.executemany(
                query,
                data
            )

        connection.commit()

        print(
            f"Successfully inserted {len(data)} records."
        )

    except Exception as error:

        connection.rollback()

        print("Database error:")
        print(error)

    finally:

        connection.close()


def main():

    data = generate_data()

    print(f"Generated {len(data)} records.")

    insert_data(data)


if __name__ == "__main__":
    main()
