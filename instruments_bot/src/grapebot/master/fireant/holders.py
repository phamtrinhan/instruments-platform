from datetime import datetime, timedelta
import json
from pytz import timezone
import pandas as pd
import asyncio

from grapebot import log
from grapebot import process
from grapebot import utils
from grapebot.master.cate import getBase
from grapebot.master.ssi import instruments
from grapebot.storage import utils as storage_utils
from retrying import retry

from datetime import datetime

now = datetime.now()
count = {"stock": 0, "future": 0, "index": 0}

logger = log.get_logger('holder_fireant.log')


def get_all_info(stock_list=None, type=None, end=None):
    count[type.lower()] += 1
    logger.info('-' * 10)
    logger.info(f'Start get FIREANT_HOLDER {type.upper()}: #{count[type.lower()]}')
    if (stock_list is None) or (type is None):
        logger.error("FIREANT_HOLDER EMPTY !!!!")
        return
    DATA_PATH_CSV = f"/notion/FIREANT_HOLDER/CSV/"
    DATA_PATH_JSON = f"/notion/FIREANT_HOLDER/JSON/"
    DATA_PATH_PICKLE = f"/notion/FIREANT_HOLDER/PICKLE/"

    stock_dict = []
    get_link = []
    body_list = []
    for stock_i in stock_list:
        stock_ii = stock_i['code']
        stock_dict.append(stock_ii)
        body_list.append({})
        tmp_link = f'https://restv2.fireant.vn/symbols/{stock_ii}/holders'
        get_link.append(tmp_link)
    # print(get_link)
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
            getBase.getByList_async(get_link, body_list, [], False, True))
    # print(report_type_data[1])

    mydata = [json.loads(report_type_data[i]) for i
              in range(len(report_type_data))]
    # print(mydata[0])
    final = []
    for single, stock_ii in zip(mydata, stock_dict):
        for single_single in single:
            single_single['stock'] = stock_ii
            final.append(single_single)
    my_df = pd.DataFrame(final)

    storage_path_csv = storage_utils.create_daily_file(DATA_PATH_CSV + 'stock_holder.csv')
    storage_path_json = storage_utils.create_daily_file(DATA_PATH_JSON + 'stock_holder.json')

    my_df.to_csv(storage_path_csv)
    logger.info(f"STORING SECTOR at {storage_path_csv}")

    my_df.to_json(storage_path_json)



def main():
    stock, future, index = instruments.list_by_type()
    logger.info("---- FIREANT HOLDER START ----")
    logger.info(
        'Fetching list stock done. No: ' + str(len(stock)))

    get_all_info(stock, 'stock')
    logger.info("---- FIREANT HOLDER END ----")
