from fastapi import FastAPI, HTTPException

from database.data_currency import RedisConnection

from database.data_currency import MongoConnection

app = FastAPI()




def get_crypto_price(crypto_name: str) -> float:
    cached_price = RedisConnection.get(crypto_name)
    if cached_price:
        return float(cached_price)
    else:
        #  querying the database for price
        price = get_price_from_database(crypto_name)
        RedisConnection.setex(crypto_name, 60 * 15, price)  # Cache for 15 minutes
        return price

def get_price_from_database(crypto_name: str) -> float:
    #  getting crypto price from the database

    crypto_prices = {"ABAN": 4.0}
    return crypto_prices.get(crypto_name, 0.0)

def buy_from_exchange(crypto_name: str, crypto_amount: float):
    # Logic to make HTTP request to international exchanges

    pass


# @app.post("/")
# async def place_order(crypto_name: str, crypto_amount: float):
#     price = get_crypto_price(crypto_name)
#     total_cost = price * crypto_amount
#
#     if total_cost < 10:
#         with MongoConnection() as mongo:
#             existing_order = await mongo.collection.find_one(
#             {"crypto_name": crypto_name, "processed": 0}
#         )
#
#         if existing_order:
#             with MongoConnection() as mongo:
#                 await mongo.collection.update_one(
#                 {"_id": existing_order["_id"]},
#                 {"$inc": {"crypto_amount": crypto_amount}}
#             )
#         else:
#             new_order = {"crypto_name": crypto_name, "crypto_amount": crypto_amount, "processed": 0}
#             with MongoConnection() as mongo:
#                 await mongo.collection.insert_one(new_order)
#
#     else:
#         buy_from_exchange(crypto_name, crypto_amount)
#
#     return {"message": "Order placed successfully"}