import logging

import requests
from datetime import datetime
import json

from grapebot.auth import fireant_authorizer
from grapebot.storage import utils as storage_utils
from grapebot.storage import csv_storage
from grapebot.storage import json_storage

logger = logging.getLogger()

DATA_PATH = "/vndirect/instruments.csv"
DATA_PATH_JSON = "/vndirect/instruments.json"
DATA_FIELDS = ("companyName",
               "companyNameEng",
               "shortName"
               "code",
               "floor",
               "type",)
VNDIRECT = "https://finfo-api.vndirect.com.vn/v4/stocks?&size=10"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}


def load(date: datetime):
    return csv_storage.load(storage_utils.create_daily_file(DATA_PATH, date))


def download(date: datetime = datetime.today()):
    data = download_instruments()
    store(data, date)
    store_json(data, date)
    return data


def download_instruments():
    response = requests.get(VNDIRECT, headers=headers)
    return response.text


def store(data, date: datetime):
    instrument_path = storage_utils.create_daily_file(DATA_PATH, date)
    stored_data = json.loads(data)['data']
    stored_data.sort(key=lambda x: x["code"])
    csv_storage.store(instrument_path, DATA_FIELDS, stored_data)


def store_json(data, date: datetime):
    instrument_path = storage_utils.create_daily_file(DATA_PATH_JSON, date)
    stored_data = json.loads(data)['data']
    stored_data.sort(key=lambda x: x["code"])
    stock_by_exchange_board = {}
    for stock in stored_data:
        if stock['exchange'] not in stock_by_exchange_board:
            stock_by_exchange_board[stock['exchange']] = [stock]
        else:
            stock_by_exchange_board[stock['exchange']].append(stock)
    json_storage.write(instrument_path, stock_by_exchange_board)