from prometheus_client import start_http_server, Gauge
import random
import time
import json



current_stock_price = Gauge(
        'stock_price',                
        'active stock price in market',  
        ['id','start_price','current_quantity_holding', 'profit', 'symbol' , 'date']      
)   
active_stock_quage = Gauge(
        'active_stock_quage',                
        'Stating stock price gauge',  
        ['id','start_price','current_quantity_holding', 'profit', 'symbol' , 'date']      
)   
active_stock_quantity_quage = Gauge(
        'active_stock_quantity_quage',                
        'Stating stock price gauge',  
        ['id','start_price','current_quantity_holding', 'profit', 'symbol' , 'date']    
)
invested_money_dollars_quage = Gauge(
        'invested_money_by_dollars',                
        'Stating invested money gauge',  
        ['type']    
)   
invested_money_shekels_quage = Gauge(
        'invested_money_by_shekels',                
        'Stating invested money gauge',  
        ['type']    
)
active_static_profirt_by_proccessing_stocks = Gauge(
        'profit_by_active_but_not_done_stocks',                
        'profit for not done stocks',  
        ['type']    
)

taxes_by_transactions_buy_sum = Gauge(
        'taxes_by_transactions_buy_sum',                
        'taxes of all buy transactions',  
        ['type']    
)   
taxes_by_transactions_sell_sum = Gauge(
        'taxes_by_transactions_sell_sum',                
        'taxes of all sell transactions',  
        ['type']    
)    
    
def prometheus_set_gauge(gauge_to_set, data,target_value):
    gauge_to_set.labels(**data).set(target_value)



def prometheus_runner():
    start_http_server(8000)
    print("Prometheus metrics available on http://localhost:8000/metrics")


