from prometheus import prometheus_runner
from utils import ID,ACTION ,SELL
import json
from tracking_stocks import track_stock,building_stock_stracture,stock_sell_manager, stock_non_sell_manager,epoche_updater
from promethus_adapter import stocks_live_metrics,static_data_metrics
from excel_reader import reading_excel
#from mongo_connection  import MongoConnection
from conf_loader import mongo_conf,jinja_stractures_conf
import uvicorn
from mongo_db_adapter import mongo
import threading


def run_server():
    uvicorn.run("mongo_to_grafana_plugin:app", host="127.0.0.1", port=3001)

def file_opener(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data



def active_stokcs(stocks_json,epoch_stock):
    epoch_flag = False
    if not epoch_stock:
        return stocks_json
    else:
        for stock in (list(stocks_json.keys())):
            if stock == epoch_stock[ID]:
                epoch_flag = True
                stocks_json.pop(stock)
            if  not epoch_flag :
                 stocks_json.pop(stock)
        print(stocks_json)
        return stocks_json
                 

if __name__ == '__main__':
    print ("intialting the oz stocks tracker for revenues in the future inshalla!")
    reading_excel()
    stocks_json = file_opener("data.json")
    epoch_stock = mongo.get_epoch(mongo.get_collection("stocks_EPOCH"))
    active_stocks_actions = active_stokcs(stocks_json=stocks_json,epoch_stock=epoch_stock)
    for stock_id in (list(active_stocks_actions.keys())):
        stock = active_stocks_actions[stock_id]
        if stock[ACTION] == SELL:
            stock_sell_manager(jinja_stractures_conf,stock, mongo,stock_id)
        else:
            stock_non_sell_manager(jinja_stractures_conf=jinja_stractures_conf,mongo_client= mongo,stock= stock,stock_id=stock_id)
    try:
        last_action_id = list((list(active_stocks_actions.keys())))[-1]
        last_action = active_stocks_actions[last_action_id]
        last_action = mongo.get_by_filter(collection=mongo.get_collection(f"stocks_{last_action[ACTION]}"),filters={ID:last_action_id})
        epoche_updater(last_action,jinja_stractures_conf,epoch_stock,mongo)
    except IndexError as e:
        pass
    static_data_metrics(mongo)

    prometheus_runner()
    print("Prometheus metrics available on http://localhost:8000/metrics")
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    stocks_live_metrics(mongo=mongo)
    

    