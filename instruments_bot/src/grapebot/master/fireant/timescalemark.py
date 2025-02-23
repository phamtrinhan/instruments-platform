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
from grapebot.storage import local as storage_local
from retrying import retry

count = {"stock": 0, "future": 0, "index": 0}

logger = log.get_logger('base_timescale_mark_fireant.log')

DATA_PATH = f"/notion/FIREANT_TIMESCALE_MARK/"

# @process.tracker(logger=logger)


def getbase(stock_list=None, type=None, start=None, end=None):
    count[type.lower()] += 1
    logger.info('-' * 10)
    logger.info(
        f'Start get TIMESCALE_MARK {type.upper()}: #{count[type.lower()]}')
    if (stock_list is None) or (type is None):
        logger.error("TIMESCALE_MARK EMPTY !!!!")
        return
    if end is None:
        date_ii = utils.today_in_ymd()
    else:
        date_ii = str(end)
    if start is None:
        start_ii = utils.today_in_ymd()
    else:
        start_ii = str(start)
    list_stocks = stock_list
    list_dict = []
    in_List = []
    get_link = []
    for stock_i in list_stocks:
        stock_ii = stock_i['code']
        in_List.append(stock_ii)
        tmp_link = f'https://restv2.fireant.vn/symbols/{stock_ii}/timescale-marks?startDate={start_ii}&endDate={date_ii}&offset=0&limit=10000'
        get_link.append(tmp_link)
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
        getBase.getByList_async(get_link, [], [], 0.5, True))

    # mydata = [json.loads(report_type_data[i]) for i
    #           in range(len(report_type_data))]
    mydata = []
    for index in range(len(report_type_data)):
        try:
            data = json.loads(report_type_data[index])
            mydata.append(data)
        except Exception as e:
            logger.error(e)
            mydata.append([])

    for mydata_ii, stock_ii in zip(mydata, in_List):
        for single_day in mydata_ii:
            try:
                tmp = single_day
                tmp['stock'] = stock_ii
                if tmp['label'] == "F":
                    id_label = tmp['id'].split("_")
                    tmp['year'] = int(id_label[1])

                    tmp['quarter'] = int(id_label[2])
                    if tmp['quarter'] == 0:
                        tmp['quarter'] = 5
                else:
                    tmp['year'] = ''
                    tmp['quarter'] = ''
                tmp['date'] = datetime.date(pd.to_datetime(tmp['date']))
                # print(tmp)
                # exit()
                list_dict.append(tmp)

            except Exception as e:
                logger.error('Problems when parse TIMESCALE MARK')
                logger.error(e)
    try:
        current_dataframe = pd.DataFrame(list_dict)
        storage_path = storage_utils.create_daily_file(DATA_PATH,
                                                       datetime.today())
        logger.info(f"STORING at {storage_path}")
        current_dataframe.to_csv(
            storage_path + 'timescale_mark.csv', index=False)
        current_dataframe.to_json(storage_path + 'timescale_mark.json')
        current_dataframe.to_pickle(storage_path + 'timescale_mark.pkl.gzip')

        return current_dataframe
    except Exception as e:

        logger.error('Problems when save chart INDEX')
        logger.error(e)


# @retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)

def get_custom():
    logger.info("---- FIREANT TIMESCALE START ----")
    stock, future, index = instruments.list_by_type()
    getbase(stock, 'stock', start='1999-01-01')

    logger.info("---- FIREANT TIMESCALE END ----")


def get_all():
    check_path = storage_utils.create_daily_file(
        DATA_PATH, datetime.today()) + "timescale_mark.csv"
    if storage_local.check_file_exist(check_path):
        df_all = pd.read_csv(check_path)
    else:
        stock, future, index = instruments.list_by_type()
        df_all = getbase(stock, 'stock', start='1999-01-01')
    return df_all
