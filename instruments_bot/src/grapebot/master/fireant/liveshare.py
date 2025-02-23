import logging

import pandas as pd
import requests
from datetime import datetime
import json
from retrying import retry
from grapebot.auth import fireant_authorizer
from grapebot.storage import utils as storage_utils
from grapebot.storage import csv_storage
from grapebot.storage import json_storage

logger = logging.getLogger()

DATA_PATH_JSON = "/notion/fant/all_financial.json"

DATA_PATH_TOTAL = "/total/all_financial.json"

FANT_AFI_API = "https://svr5.fireant.vn/api/Data/Finance/AllLastestFinancialInfo"


def load(date: datetime):
    return csv_storage.load(storage_utils.create_daily_file(DATA_PATH_JSON, date))


def download(date: datetime = datetime.today()):
    data = download_financial_information()
    store(data, date)
    return data


@retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def download_financial_information():
    logger.info('Get FANT AFI')
    try:
        response = requests.get(FANT_AFI_API, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', })
        if response.status_code != 200:
            logger.error("Can't get AFI Fant at " + str(FANT_AFI_API))
        # print(response.text)
        return response.text

    except Exception as e:
        logger.critical("Fant AFI Return not JSON")


def download_instruments_dict():
    response = requests.get(FANT_AFI_API)
    if response.status_code != 200:
        logger.error("Can't get AFI Fant")
    return json.loads(response.text)['data']


def store(data, date: datetime):
    json_path = storage_utils.create_daily_file(DATA_PATH_JSON, date)
    json_storage.write(json_path, json.loads(data))
