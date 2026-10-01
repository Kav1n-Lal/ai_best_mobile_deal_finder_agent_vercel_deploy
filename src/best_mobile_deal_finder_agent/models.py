from typing import Literal
from pydantic import BaseModel, Field


class QueryRoute(BaseModel):
    route: Literal[
        "deal",
        "summarize",
        "mobile_info"
    ]

class ProductQuery(BaseModel):
    brand: str | None = None
    # model: str | None = None
    memory: str | None = None
    storage:str | None = None
    budget: float | None = None
    
class PhoneDeal(BaseModel):
    retailer: str
    brand: str
    model: str
    memory: str
    storage: str
    mrp: float
    selling_price: float
    discount: float = 0
    cashback: float = 0
    bank_offer: float = 0
    exchange_bonus: float = 0
    delivery_charge: float = 0
    availability: bool
    stock_count: int = 0
    warranty: str = "1 year"
    effective_price: float = 0

class DealResult(BaseModel):
    query: ProductQuery
    best_deal: PhoneDeal | None = None
    alternatives: list[PhoneDeal] = Field(default_factory=list)
    message: str


