from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from utils import STOCKS_BUY_MONGO_PROJECTION ,STOCKS_BUY_MONGO_FILTER,BUY,INVEST,STOCKS_INVEST_MONGO_PROJECTION
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

class Invest_stocks(BaseModel):
    id: str
    dollars_invest : float
    shekels_invest: float
    date: datetime

@app.get("/stocks", response_model=List[Stock_buy])
async def get_stocks():
    collection = mongo.get_collection(f'stocks_{BUY}')
    data = mongo.get_by_filter_all(collection=collection,filters=STOCKS_BUY_MONGO_FILTER,projection=STOCKS_BUY_MONGO_PROJECTION)
    return data


#invested_money = mongo.get_by_filter_all(collection=mongo.get_collection(f'stocks_{INVEST}'),filters={},projection=STOCKS_INVEST_MONGO_PROJECTION)


@app.get("/invest_history", response_model=List[Invest_stocks])
async def invest_history():
    collection = mongo.get_collection(f'stocks_{INVEST}')
    data = mongo.get_by_filter_all(collection=collection,filters={},projection=STOCKS_INVEST_MONGO_PROJECTION)
    return list(data)
#uvicorn filename:app --reload
