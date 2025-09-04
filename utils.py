CONNECTION_STRING = 'CONNECTION_STRING'
DATABASE_NAME = 'DATABASE_NAME'
MONGO = "MONGO"
JINJA_FILES_STRACTIRE = "JINJA_FILES_STRACTIRE"
COLLECTIONS = "COLLECTIONS"
ID = "id"
ACTION = 'action'
SELL = "SELL"
BUY = "BUY"
INVEST = "INVEST"
AVAILABLE_QUANTITY = "current_quantity_holding"
QUANTITY = "quantity"
END_PRICE = "end_price"
START_PRICE = "start_price"
PROFIT = "profit"
PERCETAGE_PROFIT = "profit_by_percantage"
STATUS = "status"
STOCKS_BUY_MONGO_PROJECTION = {'id': 1, 'start_price': 1,'quantity':1,'profit':1,'profit_by_percantage':1,'symbol':1,'date':1}
STOCKS_BUY_MONGO_FILTER = {'status':'done'}
STOCKS_BUY_PROCESS_MONGO_PROJECTION = {'id': 1, 'start_price': 1,'current_quantity_holding':1,'profit':1,'symbol':1,'date':1}
STOCK_BUY_PROCCESS_FILTER = {'status' : 'processing'}
STOCKS_INVEST_MONGO_PROJECTION = {'id': 1, 'shekels_invest': 1,'dollars_invest':1,'_id':0,'date':1}
TAXES = 'TAXES'
TAX_PER_TRANSACTION = 'TAX_PER_TRANSACTION'
TAX_TRANSACTION = 'tax_transaction'
TYPE = 'type'
RATES = 'RATES'






# ------------------------------------------
PIPLINE_LAST_INVEST = [
    {"$sort": {"date": -1}}, 
    {"$limit": 1}
]



PIPLINE_SUM_PROFIT_PRCCOSSING_STOCKS = [
    {"$sort": {"id": 1, "timestamp": -1}},

    {
        "$group": {
            "_id": "$id",
            "profit_active": {"$first": "$profit"},
        }
    },

    {
        "$group": {
            "_id": None,
            "totalProfitActive": {"$sum": "$profit_active"},
        }
    }
]


PIPLINE_SUM_TAXES_TRANSACTION_STOCKS = [
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