from datetime import datetime
import logging
import pandas as pd
import asyncio
import json

from grapebot.master.cate import getBase
from grapebot.storage import utils as storage_utils
from grapebot import process

FOREIGN_HIST = "/VNDIRECT/FOREIGN_HIST/"
FOREIGN_PATH = storage_utils.create_daily_file(FOREIGN_HIST)

logger = logging.getLogger()

'''
    Uodate 05/10/2022: QC Pass

'''


@process.tracker(logger=logger)
def getAllHist():
    from datetime import datetime as dt
    listdate = pd.bdate_range(start='1/1/2016', end='05/20/2021')
    
    str_list = [
        str(datetime.date(datetime.strptime(str(ii), '%Y-%m-%d %H:%M:%S'))) for
        ii in listdate]
    # convert to datetime.date only
    myDates = [(datetime.date(datetime.strptime(str(ii), '%Y-%m-%d %H:%M:%S')))
               for ii in listdate]
    urls_list = []
    for date_ii, mydate_ii in zip(str_list, myDates):
        url = 'https://api-finfo.vndirect.com.vn/v4/foreigns?q=tradingDate:' + str(
                date_ii) + '&size=10000'
        urls_list.append(url)
    
    logger.info(f"Prepare URLs: Complete. Total {len(urls_list)}")
    loop = asyncio.get_event_loop()
    report_type_data = loop.run_until_complete(
            getBase.getByList_async(urls_list, 0.5))
    my_data = []
    for i in range(len(report_type_data)):
        try:
            new_data = json.loads(report_type_data[i])
            my_data.append(new_data)
            # logger.info(new_data)
        except Exception as e:
            logger.error("JSON Failed")
            logger.error(report_type_data[i].decode(encoding='UTF-8'))
    listDf = []
    for single_data in my_data:
        
        if len(single_data['data']) >= 1:
            tmpDf = pd.DataFrame(single_data['data'])
            listDf.append(tmpDf)
    # print(listDf)
    fullhistory = pd.concat(listDf, axis=0)
    fullhistory.insert(0, 'uid', range(0, len(fullhistory)))
    # fullhistory = fullhistory.clip(10)
    file = FOREIGN_PATH + "foreign_flow_hist_" + dt.today().strftime(
            '%Y%m%d') + '.pkl.gzip'
    fullhistory.to_pickle(file)
    file_csv = FOREIGN_PATH + "foreign_flow_hist_" + dt.today().strftime(
            '%Y%m%d') + '.csv'
    fullhistory.to_csv(file_csv)
    file_json = FOREIGN_PATH + "foreign_flow_hist_" + dt.today().strftime(
            '%Y%m%d') + '.json'
    fullhistory.to_json(file_json)
    logger.info("Finish get foreign_flow_hist")
    logger.info(f"STORING at {FOREIGN_PATH}")
