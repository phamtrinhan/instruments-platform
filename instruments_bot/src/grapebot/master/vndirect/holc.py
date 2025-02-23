from datetime import datetime, timedelta
import json
from pytz import timezone
import pandas as pd
import asyncio

from grapebot import log
from grapebot import process
from grapebot.master.cate import getBase
from grapebot.master.ssi import instruments
from grapebot.storage import utils as storage_utils

count = {"stock": 0, "future": 0, "index": 0}


logger = log.get_logger('base_holc.log')


# @process.tracker(logger=logger)
# @retry(stop_max_attempt_number=3)
def getbase(stock_list=None, type=None, end=None):
    count[type.lower()] += 1
    logger.info('-' * 10)
    logger.info(f'Start get HOLC {type.upper()}: #{count[type.lower()]}')
    if (stock_list is None) or (type is None):
        logger.error("BASE HOLC EMPTY !!!!")
        return
    DATA_PATH = f"/notion/HOLC/{type.upper()}/"
    if end is None:
        date_ii = datetime.today().strftime("%Y%m%d")
    else:
        date_ii = str(end)
    tz = timezone("Etc/GMT+7")
    dt1 = (pd.to_datetime(date_ii)) - timedelta(1)
    # print(dt1)
    timestamp1 = str(int(dt1.replace(tzinfo=tz).timestamp()))
    list_stocks = stock_list
    list_dict = []
    in_List = []
    get_link = []
    for object in list_stocks:
        stock_ii = object['code']
        in_List.append(stock_ii)
        tmp_link = f"https://dchart-api.vndirect.com.vn/dchart/history?resolution=D&" \
                   f"symbol={stock_ii}&from={timestamp1}&to={timestamp1}"
        get_link.append(tmp_link)
        
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
            getBase.getByList_async(get_link, 0.5))
    
    mydata = [json.loads(report_type_data[i]) for i
              in range(len(report_type_data))]
    
    for mydata_ii, stock_ii in zip(mydata, in_List):
        
        try:
            tmp = mydata_ii
            if len(tmp['c']) > 0:
                tmp_data = {'Date': datetime.date(pd.to_datetime(str(date_ii))),
                            'Ticker': stock_ii,
                            'CLOSE': tmp['c'][-1], 'OPEN': tmp['o'][-1],
                            'HIGH': tmp['h'][-1],
                            'LOW': tmp['l'][-1], 'timestamp': tmp['t'][-1],
                            'VOLUME': tmp['v'][-1]}
                list_dict.append(tmp_data)
        
        except Exception as e:
            logger.error('Problems when parse chart INDEX')
            logger.error(e)
    try:
        current_dataframe = (pd.DataFrame(list_dict))
        storage_path = storage_utils.create_daily_file(DATA_PATH,
                                                       datetime.today())
        logger.info(f"STORING at {storage_path}")
        current_dataframe.to_csv(storage_path + 'base.csv')
        current_dataframe.to_pickle(storage_path + 'base.pkl.gzip')
    except Exception as e:
        
        logger.error('Problems when save chart INDEX')
        logger.error(e)


def main():
    stock, future, index = instruments.list_by_type()
    getbase(stock, 'stock')
    getbase(future, 'future')
    getbase(index, 'index')
