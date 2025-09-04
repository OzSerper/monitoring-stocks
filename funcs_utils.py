import json
from jinja2 import Environment, FileSystemLoader
import hashlib
from datetime import datetime
from conf_loader import rates_conf
import requests
import yfinance as yf

env = Environment(loader=FileSystemLoader("jinjas_template"))

def stock_add_load_jinja(jinja_file,**data):
    template = env.get_template(jinja_file)
    rendered = template.render(**data)
    json_compitable = json.loads(rendered)
    return json_compitable


def hash_creator(text):
    text_bytes = text.encode('utf-8')
    hash_object = hashlib.sha256(text_bytes)
    return hash_object.hexdigest()





def get_usd_ils_rate(date_str):
    import datetime
    date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    next_day = date + datetime.timedelta(days=1)

    data = yf.download("USDILS=X", start=date.strftime("%Y-%m-%d"), end=next_day.strftime("%Y-%m-%d"), progress=False, auto_adjust=False)
    if data.empty:
        raise Exception("No data returned for the given date")
    rate = float(data["Close"].iloc[0])
    print(f"USD to ILS on {date.date()}: {rate}")
    return rate

def normalize_date(d: str) -> datetime:
    return datetime.strptime(d, "%d/%m/%Y")
