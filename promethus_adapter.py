from mongo_connection import MongoConnection
from utils import BUY, STOCK_BUY_PROCCESS_FILTER,STOCKS_BUY_PROCESS_MONGO_PROJECTION,START_PRICE,\
    AVAILABLE_QUANTITY,INVEST,STOCKS_INVEST_MONGO_PROJECTION, PIPLINE_SUM_INVEST, TYPE,PIPLINE_SUM_PROFIT_PRCCOSSING_STOCKS,PIPLINE_SUM_TAXES_TRANSACTION_STOCKS,SELL
from prometheus import current_stock_price, active_stock_quage,active_stock_quantity_quage, prometheus_set_gauge,\
                        invested_money_dollars_quage, invested_money_shekels_quage, active_static_profirt_by_proccessing_stocks,\
                            taxes_by_transactions_buy_sum,taxes_by_transactions_sell_sum
from tracking_stocks import track_stock
import time 

def static_data_metrics(mongo: MongoConnection):
    invested_money = mongo.get_by_aggregation(collection=mongo.get_collection(f'stocks_{INVEST}'),pipeline=PIPLINE_SUM_INVEST)
    invested_dollars = invested_money[0]["totalDollarsInvested"]
    invested_shekels = invested_money[0]["totalShekelInvested"]
    profit_by_proccessing_stocks = mongo.get_by_aggregation(collection=mongo.get_collection(f'stocks_{BUY}'),pipeline=PIPLINE_SUM_PROFIT_PRCCOSSING_STOCKS)
    profit_by_proccessing_stocks_value = profit_by_proccessing_stocks[0]['totalProfitActive']
    collection = mongo.get_collection(f'stocks_{BUY}')
    data_buy = mongo.get_by_aggregation(collection=collection,pipeline=PIPLINE_SUM_TAXES_TRANSACTION_STOCKS)
    data_taxes_buy = data_buy[0]["totalTaxOfLastPerId"]
    collection = mongo.get_collection(f'stocks_{SELL}')
    data_sell = mongo.get_by_aggregation(collection=collection,pipeline=PIPLINE_SUM_TAXES_TRANSACTION_STOCKS)
    data_taxes_sell = data_sell[0]["totalTaxOfLastPerId"]

    prometheus_set_gauge(gauge_to_set=invested_money_dollars_quage, data={TYPE:"dollars"}, target_value=invested_dollars)
    prometheus_set_gauge(gauge_to_set=invested_money_shekels_quage, data={TYPE:"shekels"}, target_value=invested_shekels)
    prometheus_set_gauge(gauge_to_set=active_static_profirt_by_proccessing_stocks, data={TYPE:"dollars"}, target_value=profit_by_proccessing_stocks_value)
    prometheus_set_gauge(gauge_to_set=taxes_by_transactions_buy_sum, data={TYPE:"dollars"}, target_value=data_taxes_buy)
    prometheus_set_gauge(gauge_to_set=taxes_by_transactions_sell_sum, data={TYPE:"dollars"}, target_value=data_taxes_sell)


def stocks_live_metrics(mongo: MongoConnection):
    active_stocks = mongo.get_by_filter_all(collection=mongo.get_collection(f'stocks_{BUY}'),filters=STOCK_BUY_PROCCESS_FILTER,projection=STOCKS_BUY_PROCESS_MONGO_PROJECTION)
    for active_stock in active_stocks:
        active_stock.pop("_id", None)
        prometheus_set_gauge(gauge_to_set=active_stock_quage, data=active_stock, target_value=active_stock[START_PRICE])
        prometheus_set_gauge(gauge_to_set=current_stock_price, data=active_stock, target_value=track_stock(active_stock["symbol"])['price'])
        prometheus_set_gauge(gauge_to_set=active_stock_quantity_quage, data=active_stock, target_value=active_stock[AVAILABLE_QUANTITY])

    while True:
       time.sleep(100)
       for active_stock_symbol in active_stocks:
            price_of_stock = track_stock(active_stock_symbol["symbol"])['price']
            prometheus_set_gauge(gauge_to_set=current_stock_price, data=active_stock, target_value=price_of_stock)


