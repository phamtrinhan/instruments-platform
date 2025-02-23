from datetime import datetime, timedelta
import json
from pytz import timezone
import pandas as pd
import asyncio
from grapebot.master.fireant import timescalemark

from grapebot import log
from grapebot import process
from grapebot import utils
from grapebot.master.cate import getBase
from grapebot.master.ssi import instruments
from grapebot.storage import utils as storage_utils
from grapebot.storage import local as storage_local

from retrying import retry

from datetime import datetime

now = datetime.now()
count = {"stock": 0, "future": 0, "index": 0}

logger = log.get_logger('all_fireant_fundamental.log')


# @retry(stop_max_attempt_number=3, wait_exponential_multiplier=100, wait_exponential_max=10000)
def get_all_info(stock_list=None, type=None, end=None):
    count[type.lower()] += 1
    logger.info('-' * 10)
    logger.info(f'Start get FIREANT FUNDAMENTAL {type.upper()}: #{count[type.lower()]}')
    if (stock_list is None) or (type is None):
        logger.error("FIREANT FUNDAMENTAL EMPTY !!!!")
        return
    DATA_PATH_CSV = storage_utils.create_daily_file(f"/notion/HIST_FIREANT_FUNDAMENTAL/CSV/")
    DATA_PATH_JSON = storage_utils.create_daily_file(f"/notion/HIST_FIREANT_FUNDAMENTAL/JSON/")
    DATA_PATH_PICKLE = storage_utils.create_daily_file(f"/notion/HIST_FIREANT_FUNDAMENTAL/PICKLE/")

    stock_dict = []
    get_link = []
    body_list = []

    year = utils.year()
    for stock_i in stock_list:
        for type in [1,2,3,4]:
            stock_ii = stock_i['code']
            stock_dict.append({'stock': stock_ii, 'type': type})
            body_list.append({})
            tmp_link = f'https://restv2.fireant.vn/symbols/{stock_ii}/full-financial-reports?type={type}&year={str(year)}&quarter={str(4)}&limit=2000'
            get_link.append(tmp_link)
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
        getBase.getByList_async(get_link, body_list, [], False, True))

    mapping_type = {
        1: {
            'longcode': 'balance-sheet',
            'short': 'bs'
        },
        2: {
            'longcode': 'income-statement',
            'short': 'is'
        },

        3: {
            'longcode': 'cash-flow-direct',
            'short': 'cfd'
        },
        4: {
            'longcode': 'cash-flow-indirect',
            'short': 'cfi'
        },

    }
    mydata = [json.loads(report_type_data[i]) for i
              in range(len(report_type_data))]
    final = []
    tsmm = timescalemark.get_all()
    dem = 0
    for mydata_ii, stock_ii in zip(mydata, stock_dict):

        # try:
        if (mydata_ii == None):

            logger.warn(f"Not found on {stock_ii['stock']} on {mapping_type[int(stock_ii['type'])]}")
            continue

        tmp = mydata_ii
        tsm = tsmm[tsmm.stock == stock_ii['stock']]

        for section in tmp:
            # if section['level'] == 1:
            #     print(section)
            #     continue
            for single in section['values']:
                if single['quarter'] == 0:
                    query = tsm[(tsm.quarter == 5) & (tsm.year == single['year']) & (tsm.stock == stock_ii['stock'])]

                    if len(query) > 0:
                        published_date = query.iloc[0].date
                    else:
                        published_date = "nan"
                else:
                    query = tsm[(tsm.quarter == single['quarter']) & (tsm.year == single['year']) & (tsm.stock == stock_ii['stock'])]

                    if len(query) > 0:
                        published_date = query.iloc[0].date
                    else:
                        published_date = "nan"
                final.append({
                    'year': single['year'],
                    'quarter': single['quarter'],
                    'name': utils.no_accent_vietnamese(section['name']),
                    'type': mapping_type[int(stock_ii['type'])]['longcode'],
                    'stock': stock_ii['stock'],
                    'short': mapping_type[int(stock_ii['type'])]['short'] + str(section['id']),
                    'long': mapping_type[int(stock_ii['type'])]['longcode'] + "-" + str(section['id']),
                    'published_date': str(published_date),
                    'value': single['value']
                })
        # except Exception as e:
        #     logger.error('Problems when parse chart FIREANT FUNDAMENTAL')
        #     logger.error(e)
    tmp_data = pd.DataFrame(final)

    tmp_data.reset_index(drop=True, inplace=True)

    # logger.info('Saving '  + str(stock_ii.upper()) + ": " + storage_path_csv + stock_ii.upper()+'.csv' )
    tmp_data.to_csv(DATA_PATH_CSV + 'final.csv')
    tmp_data.to_json(DATA_PATH_JSON + 'final.json')
    tmp_data.to_pickle(DATA_PATH_PICKLE + 'final.pkl.gzip')

def main():
    stock, future, index = instruments.list_by_type()
    logger.info("---- FIREANT FUNDAMENTAL START ----")
    logger.info(
        'Fetching list stock done. No: ' + str(len(stock)))

    # get_all_info([{'code': 'HPG'}],'stock')
    get_all_info(stock, 'stock')
    logger.info("---- FIREANT FUNDAMENTAL END ----")
