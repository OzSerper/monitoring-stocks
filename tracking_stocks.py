import finnhub
from funcs_utils import stock_add_load_jinja
from utils import ACTION, BUY , AVAILABLE_QUANTITY, QUANTITY, END_PRICE, START_PRICE, PERCETAGE_PROFIT,PROFIT,\
    STATUS,ID,TAX_PER_TRANSACTION,TAX_TRANSACTION,INVEST
from mongo_connection import MongoConnection
from bson.json_util import dumps
from datetime import datetime
from conf_loader import taxes_conf

def track_stock(stock_symbol):
    finnhub_client = finnhub.Client(api_key="d11m1rhr01qjtpe7ok8gd11m1rhr01qjtpe7ok90")
    stock_data = finnhub_client.quote(stock_symbol)
    return {"symbol":stock_symbol,"price":stock_data['c']}

def building_stock_stracture(jinjas_file_conf :dict, **data):
    return stock_add_load_jinja(jinja_file=jinjas_file_conf[data[ACTION]], **data)

def stock_sell_manager(jinja_stractures_conf,stock,mongo_client: MongoConnection,stock_id:str):
    filters = stock_add_load_jinja(jinja_file=jinja_stractures_conf[f'{stock[ACTION]}_FILTER'], **stock)
    collection = mongo_client.get_collection(f'stocks_{BUY}')
    stock_sold_quantity = stock[QUANTITY]
    stock_end_price = stock[END_PRICE]
    
    for bought_stock in mongo_client.get_by_filter_all_date_order(collection=collection,filters = filters):
        stock_start_prict = bought_stock[START_PRICE]
        singel_stock_profit = round(stock_end_price - stock_start_prict ,2)
        bought_stock.pop("_id", None)
        if bought_stock[AVAILABLE_QUANTITY] -  stock_sold_quantity == 0:
            profit = stock_sold_quantity * singel_stock_profit + bought_stock[PROFIT]
            profit_by_percatage = round((profit/(stock_start_prict * stock_sold_quantity)) * 100,2)
            stock_updater(bought_stock,[PROFIT,PERCETAGE_PROFIT,AVAILABLE_QUANTITY,STATUS],
                          [profit,profit_by_percatage,0,"done"])
            mongo_client.update_document(collection=collection, filter_query={ID :bought_stock[ID]},update_fields=bought_stock)
            stock_updater(stock,[PROFIT,START_PRICE],[profit,bought_stock[START_PRICE]])
            stock_uploader(stock,jinja_stractures_conf,stock_id,mongo_client)
            break       
        elif bought_stock[AVAILABLE_QUANTITY] -  stock_sold_quantity > 0:
            stocks_sold_quantity_on_bought_stock = bought_stock[AVAILABLE_QUANTITY] -  stock_sold_quantity
            profit = stocks_sold_quantity_on_bought_stock * singel_stock_profit + bought_stock[PROFIT]
            profit_for_sell_cut = stocks_sold_quantity_on_bought_stock * singel_stock_profit
            profit_by_percatage = round((profit/(stock_start_prict*stocks_sold_quantity_on_bought_stock)) * 100,2)
            stock_updater(bought_stock,[PROFIT,PERCETAGE_PROFIT,AVAILABLE_QUANTITY],
                          [profit,profit_by_percatage,bought_stock[AVAILABLE_QUANTITY]-stocks_sold_quantity_on_bought_stock])
            mongo_client.update_document(collection=collection, filter_query={ID :bought_stock[ID]},update_fields=bought_stock)
            stock_updater(stock,[PROFIT,START_PRICE],[profit_for_sell_cut,bought_stock[START_PRICE]])
            stock_uploader(stock,jinja_stractures_conf,stock_id,mongo_client)
            break
        elif bought_stock[AVAILABLE_QUANTITY] -  stock_sold_quantity < 0:
            
            profit = bought_stock[AVAILABLE_QUANTITY] * singel_stock_profit + bought_stock[PROFIT]
            profit_for_sell_cut = bought_stock[AVAILABLE_QUANTITY] * singel_stock_profit
            profit_by_percatage = round((profit/(stock_start_prict *bought_stock[AVAILABLE_QUANTITY]))* 100,2)
            stock_updater(bought_stock,[PROFIT,PERCETAGE_PROFIT,AVAILABLE_QUANTITY,STATUS],
                          [profit,profit_by_percatage,0,"done"])
            mongo_client.update_document(collection=collection, filter_query={ID :bought_stock[ID]},update_fields=bought_stock)
            stock_sold_quantity =- bought_stock[AVAILABLE_QUANTITY]
            stock_updater(stock,[PROFIT,START_PRICE,QUANTITY],[profit_for_sell_cut,bought_stock[START_PRICE,bought_stock[AVAILABLE_QUANTITY]]])
            stock_uploader(stock,jinja_stractures_conf,stock_id,mongo_client)

def stock_non_sell_manager(jinja_stractures_conf,stock,mongo_client: MongoConnection,stock_id:str):
    stock_uploader(stock,jinja_stractures_conf,stock_id,mongo_client)

        
def stock_updater(stock_to_update,labels_to_update:list,values_to_update:list):
    for label in range(len(labels_to_update)):
        stock_to_update[labels_to_update[label]] = values_to_update[label]
        
def stock_uploader(stock,jinja_stractures_conf,stock_id,mongo:MongoConnection):
    stock[ID] = stock_id
    if stock[ACTION] != INVEST:
        stock[TAX_TRANSACTION] = taxes_conf[TAX_PER_TRANSACTION]
    stock_template = (building_stock_stracture(jinjas_file_conf=jinja_stractures_conf,**stock))
    stock_template["date"] = datetime.strptime(stock_template['string_date'], "%d/%m/%Y")
    mongo.insert_doc(mongo.get_collection(f'stocks_{stock[ACTION]}'),**stock_template)
        
def epoche_updater(action,jinja_stractures_conf,epoch_stock,mongo:MongoConnection):
    string_date = action['string_date']
    stock_template = (building_stock_stracture(jinjas_file_conf=jinja_stractures_conf,**action))
    stock_template["date"] = datetime.strptime(string_date, "%d/%m/%Y")
    stock_template['epoch'] = True
    if epoch_stock != None:
        mongo.delete_doc(mongo.get_collection(f'stocks_EPOCH'),**{ID:epoch_stock[ID]})
    mongo.insert_doc(mongo.get_collection(f'stocks_EPOCH'),**stock_template)
    
    
