# tests/deal_assertions.py

from best_mobile_deal_finder_agent.models import PhoneDeal


def assert_best_deal_is_correct(result):
    """
    Verify that best_deal is actually the lowest effective-price
    available deal returned by search_deals().
    """

    deals: list[PhoneDeal] = result.get("deals", [])

    best_deal: PhoneDeal | None = result.get("best_deal")

    available_deals = [
        deal
        for deal in deals
        if deal.availability
    ]

    if not available_deals:
        assert best_deal is None, (
            "No available deals were returned, "
            "but best_deal was populated."
        )
        return

    expected = min(
        available_deals,
        key=lambda deal: deal.effective_price
    )

    assert best_deal is not None, (
        "Deals were returned but best_deal is None."
    )

    assert (
        best_deal.retailer == expected.retailer
    ), (
        f"Wrong retailer. "
        f"Expected {expected.retailer}, "
        f"got {best_deal.retailer}"
    )

    assert (
        best_deal.effective_price
        == expected.effective_price
    ), (
        f"Wrong effective price. "
        f"Expected {expected.effective_price}, "
        f"got {best_deal.effective_price}"
    )

# tests/deal_assertions.py

def assert_deal_is_valid(deal: PhoneDeal):

    assert deal.retailer
    assert deal.brand
    assert deal.model
    assert deal.memory
    assert deal.storage

    assert deal.mrp >= 0
    assert deal.selling_price >= 0

    assert deal.discount >= 0
    assert deal.cashback >= 0
    assert deal.bank_offer >= 0
    assert deal.exchange_bonus >= 0
    assert deal.delivery_charge >= 0

    assert deal.stock_count >= 0

    assert deal.effective_price >= 0

    if deal.availability:
        assert deal.stock_count > 0

def assert_all_deals_are_valid(result):

    deals = result.get("deals", [])

    for deal in deals:
        assert_deal_is_valid(deal)

# effective price

def expected_effective_price(deal: PhoneDeal) -> float:

    return (
        deal.selling_price
        - deal.cashback
        - deal.bank_offer
        - deal.exchange_bonus
        + deal.delivery_charge
    )

def assert_effective_price_is_correct(deal: PhoneDeal):

    expected = expected_effective_price(deal)

    assert abs(
        deal.effective_price - expected
    ) < 0.01, (
        f"Incorrect effective price for "
        f"{deal.brand} {deal.model} at {deal.retailer}. "
        f"Expected {expected}, "
        f"got {deal.effective_price}"
    )

def assert_all_effective_prices_are_correct(result):

    for deal in result.get("deals", []):
        assert_effective_price_is_correct(deal)
