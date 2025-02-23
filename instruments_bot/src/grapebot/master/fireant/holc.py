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

count = {"stock": 0, "future": 0, "index": 0}

logger = log.get_logger('base_holc_fireant.log')


# @process.tracker(logger=logger)


def getbase(stock_list=None, type=None, start=None, end=None):
    count[type.lower()] += 1
    logger.info('-' * 10)
    logger.info(f'Start get HOLC {type.upper()}: #{count[type.lower()]}')
    if (stock_list is None) or (type is None):
        logger.error("BASE HOLC EMPTY !!!!")
        return
    DATA_PATH = f"/notion/FIREANT_HOLC/{type.upper()}/"
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
        tmp_link = f'https://restv2.fireant.vn/symbols/{stock_ii}/historical-quotes?startDate={start_ii}&endDate={date_ii}&offset=0&limit=10000'
        get_link.append(tmp_link)
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
        getBase.getByList_async(get_link, [], [], 0.1, True))

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
    logger.info(mydata[0])
    for mydata_ii, stock_ii in zip(mydata, in_List):

        try:
            tmp = mydata_ii
            if len(tmp) > 0:
                tmp_data = tmp[-1]
                tmp_data['date'] = datetime.date(pd.to_datetime(str(date_ii)))

                list_dict.append(tmp_data)

        except Exception as e:
            logger.error('Problems when parse chart INDEX')
            logger.error(e)
    try:
        current_dataframe = (pd.DataFrame(list_dict))
        storage_path = storage_utils.create_daily_file(DATA_PATH,
                                                       datetime.today())
        logger.info(f"STORING at {storage_path}")
        current_dataframe.to_csv(storage_path + 'base.csv', index=False)
        current_dataframe.to_json(storage_path + 'base.json')
        current_dataframe.to_pickle(storage_path + 'base.pkl.gzip')
    except Exception as e:

        logger.error('Problems when save chart INDEX')
        logger.error(e)


# @retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def getbase_all(stock_list=None, type=None, start=None, end=None):
    count[type.lower()] += 1
    logger.info('-' * 10)
    logger.info(f'Start get HOLC {type.upper()}: #{count[type.lower()]}')
    if (stock_list is None) or (type is None):
        logger.error("BASE HOLC EMPTY !!!!")
        return
    DATA_PATH = f"/notion/HIST_FIREANT_HOLC/{type.upper()}/"
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
        tmp_link = f'https://restv2.fireant.vn/symbols/{stock_ii}/historical-quotes?startDate={start_ii}&endDate={date_ii}&offset=0&limit=10000'
        get_link.append(tmp_link)
    # print(get_link[0])
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
        getBase.getByList_async(get_link, [], [], 0.1, True))
    mydata = []
    for i in range(len(report_type_data)):
        try:
            current = json.loads(report_type_data[i])
            mydata.append(current)
        except Exception as e:
            logger.error(e)
            logger.error(list_stocks[i]['code'])
            current = []
    i = 0
    for mydata_ii, stock_ii in zip(mydata, in_List):
        if len(mydata_ii) == 0:
            continue
        tdf = pd.DataFrame(mydata_ii)

        tdf['date'] = pd.to_datetime(tdf['date'])
        tdf.reset_index()

        list_dict.append(tdf)

    print('Done')
    try:
        print('Start concat')
        current_dataframe = pd.concat(list_dict)
        print('Done concat')

        current_dataframe.reset_index(
            drop=True, inplace=True)
        current_dataframe = current_dataframe.sort_values(by=['date', 'symbol'],
                                                          ascending=True)

        storage_path = storage_utils.create_daily_file(DATA_PATH,
                                                       datetime.today())
        logger.info(f"STORING at {storage_path}")
        current_dataframe.to_csv(storage_path + 'base.csv', index=False)
        current_dataframe.to_json(storage_path + 'base.json')
        current_dataframe.to_pickle(storage_path + 'base.pkl.gzip')
    except Exception as e:

        logger.error('Problems when save chart INDEX')
        logger.error(e)


def main():
    logger.info("---- FIREANT SOURCE START ----")
    stock, future, index = instruments.list_by_type()
    getbase(stock, 'stock')
    getbase(future, 'future')
    getbase(index, 'index')

    logger.info("---- FIREANT SOURCE END ----")


def main_hist():
    logger.info("---- FIREANT SOURCE START ----")
    stock, future, index = instruments.list_by_type()
    getbase_all(stock, 'stock', start='2000-01-01')
    getbase_all(future, 'future', start='2000-01-01')
    getbase_all(index, 'index', start='2000-01-01')

    logger.info("---- FIREANT SOURCE END ----")


def index_only():
    stock, future, index = instruments.list_by_type()

    getbase_all(future, 'future', start='2000-01-01')
    getbase_all(index, 'index', start='2000-01-01')


def get_custom(start=None, end=None):
    if start != None:
        start = utils.dmy_to_ymd(start)
    if end != None:
        end = utils.dmy_to_ymd(end)

    logger.info("---- FIREANT SOURCE START ----")
    stock, future, index = instruments.list_by_type()
    getbase_all(stock, 'stock', start=start)
    getbase_all(future, 'future', start=start)
    getbase_all(index, 'index', start=start)

    logger.info("---- FIREANT SOURCE END ----")
