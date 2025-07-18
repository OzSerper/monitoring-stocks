from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from utils import STOCKS_BUY_MONGO_PROJECTION ,STOCKS_BUY_MONGO_FILTER,BUY,SELL
from fastapi.middleware.cors import CORSMiddleware
from mongo_db_adapter import mongo


app = FastAPI()

origins = [
    "http://127.0.0.1:3000"
]

class Stock_buy(BaseModel):
    id: str
    start_price: float
    quantity: int
    profit: float
    profit_by_percantage: float
    symbol: str
    date: datetime

class Stock_taxes(BaseModel):
    buy_taxes : int
    sell_taxes: int
    total_taxes: int

@app.get("/stocks", response_model=List[Stock_buy])
async def get_stocks():
    collection = mongo.get_collection(f'stocks_{BUY}')
    data = mongo.get_by_filter_all(collection=collection,filters=STOCKS_BUY_MONGO_FILTER,projection=STOCKS_BUY_MONGO_PROJECTION)
    return data


#invested_money = mongo.get_by_filter_all(collection=mongo.get_collection(f'stocks_{INVEST}'),filters={},projection=STOCKS_INVEST_MONGO_PROJECTION)

'''
@app.get("/stocks_taxes", response_model=List[Stock_taxes])
async def get_stocks():
    pipeline = [
    {"$sort": {"_id": 1, "timestamp": -1}},  
    {
        "$group": {
            "_id": "$id",
            "tax": {"$first": "$tax_transaction"},
        }
    },
    {
        "$group": {
            "_id": None,
            "totalTaxOfLastPerId": {"$sum": "$tax"}
        }
    }
]
    collection = mongo.get_collection(f'stocks_{BUY}')
    data_buy = mongo.get_by_aggregation(collection=collection,pipeline=pipeline)
    data_taxes_buy = data_buy[0]["totalTaxOfLastPerId"]
    collection = mongo.get_collection(f'stocks_{SELL}')
    data_sell = mongo.get_by_aggregation(collection=collection,pipeline=pipeline)
    data_taxes_sell = data_sell[0]["totalTaxOfLastPerId"]
    total_tax = data_taxes_buy + data_taxes_sell

    return [
    {
        "buy_taxes": data_taxes_buy,
        "sell_taxes": data_taxes_sell,
        "total_taxes": total_tax
    }
]

#uvicorn filename:app --reload
'''