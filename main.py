import uvicorn
from routes.main_router import *
# from routes.main_router import *
# from routes.main_router import app as main_app
import asyncio
# asynciofrom config import settings
# from hypercorn.config import Config
# from hypercorn.asyncio import serve
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from security import rate_limit_handler
from database.data_currency import MongoConnection
app = FastAPI(title="aban project",
              version="0.0.1",
              docs_url="/docs")




origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MyMiddleware:
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        content_type = request.headers.get('Content-Type')
        print(content_type)

        # process the request and get the response
        response = await call_next(request)

        return response


app.mount(path="/api/v1", app=app)

@app.get("/")
async def main():
    return  "Hello "

@app.post("/")
async def place_order(crypto_name: str, crypto_amount: float):
    try:
        # Get the current price of the cryptocurrency
        price = get_crypto_price(crypto_name)
        total_cost = price * crypto_amount

        # If the total cost is less than $10, accumulate orders
        if total_cost < 10:
            with MongoConnection() as mongo:
                # Check if there's an existing order for the same cryptocurrency
                existing_order = await mongo.collection.find_one(
                    {"crypto_name": crypto_name, "processed": 0}
                )

            if existing_order:
                with MongoConnection() as mongo:
                    # Update the existing order's amount
                    await mongo.collection.update_one(
                        {"_id": existing_order["_id"]},
                        {"$inc": {"crypto_amount": crypto_amount}}
                    )
            else:
                # Create a new order for the cryptocurrency
                new_order = {"crypto_name": crypto_name, "crypto_amount": crypto_amount, "processed": 0}
                with MongoConnection() as mongo:
                    await mongo.collection.insert_one(new_order)
        else:
            # Place a direct order on the exchange for larger purchases
            buy_from_exchange(crypto_name, crypto_amount)

        return {"message": "Order placed successfully"}

    except Exception as e:
        # Handle any exceptions that might occur during the order placement process
        print(f"Error placing order: {e}")
        return {"message": "Error placing order"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)