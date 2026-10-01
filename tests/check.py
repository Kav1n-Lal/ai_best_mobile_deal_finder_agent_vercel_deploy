# from agent_runner import run_agent
# from best_mobile_deal_finder_agent.models import PhoneDeal
# def a():
#     query = "Find me an iPhone 16 under ₹70000"
    
#     result = run_agent(query)

#     deals = result.get("deals", [])
#     print(deals)
    
#     available_deals = sorted(
#     deals,
#     key=lambda deal: deal.effective_price
# )



    

# #     #The best deals
# #     best_deals=[]
                
# #     for deal in available_deals:
# #         best_deals.append({
# #                         "retailer": deal.retailer,
# #                         "brand": deal.brand,
# #                         "model": deal.model,
# #                         "memory": deal.memory,
# #                         "storage": deal.storage,
# #                         "mrp": deal.mrp,
# #                         "selling_price": deal.selling_price,
# #                         "discount": deal.discount,
# #                         "cashback": deal.cashback,
# #                         "bank_offer": deal.bank_offer,
# #                         "exchange_bonus": deal.exchange_bonus,
# #                         "delivery_charge": deal.delivery_charge,
# #                         "availability": deal.availability,
# #                         "stock_count": deal.stock_count,
# #                         "effective_price": deal.effective_price,
# #                                 })

    
    
            

# #     return [
# #     {
# #         "best_deal": best_deals[0] if len(best_deals) > 0 else None
# #     },
# #     {
# #         "second_best_deal": best_deals[1] if len(best_deals) > 1 else None
# #     },
# #     {
# #         "third_best_deal": best_deals[2] if len(best_deals) > 2 else None
# #     },
# # ]


# b=a()
# print(b)

# # from best_mobile_deal_finder_agent.models import PhoneDeal
# # a=[PhoneDeal(retailer='Retailer A', brand='Apple', model='iPhone 16', memory='8GB', storage='128GB', mrp=79999.0,
# #               selling_price=73999.0, discount=6000.0, cashback=3000.0, bank_offer=2500.0, exchange_bonus=500.0, 
# #               delivery_charge=49.0, availability=True, stock_count=22, warranty='1 year Apple warranty', effective_price=68048.0),
# #               PhoneDeal(retailer='Retailer A', brand='Apple', model='iPhone 16', memory='8GB', storage='128GB', mrp=79999.0,
# #               selling_price=73999.0, discount=6000.0, cashback=3000.0, bank_offer=2500.0, exchange_bonus=500.0, 
# #               delivery_charge=49.0, availability=True, stock_count=22, warranty='1 year Apple warranty', effective_price=68048.0)]

# # d=[]
# # e=a[:2]
# # for deal in e :
# #    d.append ({"retailer": deal.retailer,
# #             "brand": deal.brand,
# #             "model": deal.model,
# #             "memory": deal.memory,
# #             "storage": deal.storage,
# #             "mrp": deal.mrp,
# #             "selling_price": deal.selling_price,
# #             "discount": deal.discount,
# #             "cashback": deal.cashback,
# #             "bank_offer": deal.bank_offer,
# #             "exchange_bonus": deal.exchange_bonus,
# #             "delivery_charge": deal.delivery_charge,
# #             "availability": deal.availability,
# #             "stock_count": deal.stock_count,
# #             "effective_price": deal.effective_price,})
# # print(d[0])

import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("OPENROUTER_API_KEY")

# response = requests.get(
#     "https://openrouter.ai/api/v1/key",
#     headers={"Authorization": f"Bearer {api_key}"}
# )

# response.raise_for_status()
# key_info = response.json()["data"]

# print("Limit:          ", key_info.get("limit"))
# print("Limit remaining:", key_info.get("limit_remaining"))
# print("Usage:          ", key_info.get("usage"))
# print("Daily usage:    ", key_info.get("usage_daily"))
# print("Weekly usage:   ", key_info.get("usage_weekly"))
# print("Monthly usage:  ", key_info.get("usage_monthly"))

import os
import requests
import json

# API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "google/gemini-2.5-flash"

url = f"https://openrouter.ai/api/v1/models/{MODEL}"

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {api_key}"}
)

response.raise_for_status()

data = response.json()["data"]

print("Model:", data["id"])
print("Context length:", data.get("context_length"))
print("Per-request limits:", data.get("per_request_limits"))
print("Top provider:", json.dumps(data.get("top_provider"), indent=2))
print("Pricing:", json.dumps(data.get("pricing"), indent=2))
