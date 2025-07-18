import pandas as pd
import json
import math
from funcs_utils import hash_creator




def reading_excel():
    df = pd.read_excel("data.xlsx", engine="openpyxl")
    stocks_data = {}
    temp_price = 0 
    temp_price_shekels = 0

    for index, row in df.iterrows():
        action = row.iloc[1]  
        if "קניה חול מטח" == action:
            hash_key_buy = hash_creator(f'{row.iloc[3]}+{row.iloc[4]}+{row.iloc[5]}+{row.iloc[0]}+buy')
            temp_dict = {"symbol": row.iloc[3], "quantity": row.iloc[4], "start_price": row.iloc[5], "date":row.iloc[0],"action":"BUY"}
            stocks_data[hash_key_buy] = temp_dict
        if "קניה שח" == action and row.iloc[2] != "מס ששולם":
            temp_price = temp_price + row.iloc[4]
            rounded = round(abs(row.iloc[10]) / 100) * 100
            temp_price_shekels = temp_price_shekels + rounded
            hash_key_invest = hash_creator(f'{row.iloc[4]}+{rounded}+invest')
            stocks_data[hash_key_invest] =  {"dollars" : temp_price , "shekels" : temp_price_shekels, "action":"INVEST" ,"date":row.iloc[0]}
        if "מכירה חול מטח" == action:
            hash_key_sell = hash_creator(f'{row.iloc[3]}+{row.iloc[4]}+{row.iloc[5]}+{row.iloc[0]}+sell')
            temp_dict_sell = {"symbol": row.iloc[3], "quantity": row.iloc[4], "end_price": row.iloc[5], "date":row.iloc[0],"action":"SELL"}
            stocks_data[hash_key_sell] = temp_dict_sell
            
        

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(stocks_data, f, ensure_ascii=False, indent=4)


    

    print("Data saved to data.json")