import logging

import requests
from datetime import datetime
import json

from grapebot.auth import fireant_authorizer
from grapebot.storage import utils as storage_utils
from grapebot.storage import csv_storage
from grapebot.storage import json_storage

logger = logging.getLogger()

DATA_PATH = "/fireant/instruments.csv"
DATA_PATH_JSON = "/fireant/instruments.json"
DATA_FIELDS = ("instrument",
               "symbol",
               "name",
               "exchange",
               "unit",
               "type",
               "supportStopOrder",
               "supportLimitOrder")
FIREANT_API = "https://restv2.fireant.vn/instruments"


def load(date: datetime):
    return csv_storage.load(storage_utils.create_daily_file(DATA_PATH, date))


def download(date: datetime = datetime.today()):
    data = download_instruments()
    store(data, date)
    store_json(data, date)
    return data


def download_instruments():
    response = requests.get(FIREANT_API, headers=fireant_authorizer.get_authorization_header())
    return response.text


def store(data, date: datetime):
    instrument_path = storage_utils.create_daily_file(DATA_PATH, date)
    stored_data = json.loads(data)
    stored_data.sort(key=lambda x: x["symbol"])
    csv_storage.store(instrument_path, DATA_FIELDS, stored_data)


def store_json(data, date: datetime):
    instrument_path = storage_utils.create_daily_file(DATA_PATH_JSON, date)
    stored_data = json.loads(data)
    stored_data.sort(key=lambda x: x["symbol"])
    stock_by_exchange_board = {}
    for stock in stored_data:
        if stock['exchange'] not in stock_by_exchange_board:
            stock_by_exchange_board[stock['exchange']] = [stock]
        else:
            stock_by_exchange_board[stock['exchange']].append(stock)
    json_storage.write(instrument_path, stock_by_exchange_board)


def list_by_type(input=False):
    if not input:
        data = json.loads(download_instruments())

    data.sort(key=lambda x: x["type"])
    stock_by_type = {}
    for stock in data:
        if stock['type'] not in stock_by_type:
            stock_by_type[stock['type']] = [stock]
        else:
            stock_by_type[stock['type']].append(stock)
    return stock_by_type['stock'], stock_by_type['future'], stock_by_type['index']

