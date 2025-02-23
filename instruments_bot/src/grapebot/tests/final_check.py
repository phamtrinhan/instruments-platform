
import os
from glob import glob
from grapebot import telegram
import xarray as xa
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


def main():
    telegram.send_message("="*5)
    telegram.send_message('Automation tests: START')
    telegram.send_message('Testing NETCDF')
    NETCDF_FILE = "{HOME}/grapechain/netcdf/prod/S_Fiant_Base_production.netcdf".format(
        HOME=os.getenv("HOME"))
    mydata = xa.open_dataset(NETCDF_FILE)
    gsXA = mydata.to_array()

    if (len(gsXA.fields) == 43):
        telegram.send_message('- NETCDF Fields: ✅ (43 fields)')
    else:
        telegram.send_message('❌ NETCDF FAILED. Not enough fields ❌')
        exit()

    df_close = gsXA.sel(fields='close')[0, :, :].to_pandas()
    is_df_today = df_close.index[-1] == pd.to_datetime(
        datetime.today().strftime('%Y-%m-%d'))
    if (is_df_today):
        telegram.send_message(
            f"- NETCDF DF_CLOSE: ✅ ({datetime.today().strftime('%Y-%m-%d')})")
    else:
        telegram.send_message('❌ NETCDF FAILED. NETCDF BUILD FAILED ❌')
        exit()
    telegram.send_message('- NETCDF: ✅')
    telegram.send_message('Testing Fundamental')
    LIST_FUNDAMENTAL = glob(
        "{HOME}/grapechain/total/FIREANT_FUNDAMENTAL/*.csv".format(HOME=os.getenv("HOME")))

    for SINGLE_FUNDAMENTAL in LIST_FUNDAMENTAL[:1]:
        current_fundamental_df = pd.read_csv(
            SINGLE_FUNDAMENTAL, index_col=[0], parse_dates=True)
        current_fundamental_df = current_fundamental_df[current_fundamental_df.index == pd.to_datetime(
            datetime.today().strftime('%Y-%m-%d'))]
        tmr_df_fundamental = current_fundamental_df[current_fundamental_df.index == pd.to_datetime(
            (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'))]
        if len(current_fundamental_df) == 0:
            telegram.send_message('❌ FUNDAMENTAL FAILED. != TODAY❌')
            exit()
        if len(tmr_df_fundamental) > 0:
            telegram.send_message('❌ FUNDAMENTAL FAILED. FUTURE BF found❌')
            exit()
    telegram.send_message('- FUNDAMENTAL: ✅')
    telegram.send_message('Testing VN30F1M')

    LISTVN30 = glob(
        "{HOME}/grapechain/total/vn30f1mdata.csv".format(HOME=os.getenv("HOME")))

    if len(LISTVN30) == 0:
        telegram.send_message('❌ VN30F1M FAILED. NOT FOUND ❌')
        exit()
    else:
        telegram.send_message('- VN30F1M FOUND: ✅')
    vn30f1m_df = pd.read_csv(LISTVN30[0], index_col=[0], parse_dates=True)
    if vn30f1m_df.shape[0] == 0:
        telegram.send_message('❌ VN30F1M FAILED. NOT FOUND. CANT READ ❌')
        exit()

    else:
        telegram.send_message('- VN30F1M SHAPE: ' + str(vn30f1m_df.shape))
        
    vn30f1m_dftd = vn30f1m_df[vn30f1m_df.index.date == pd.to_datetime(
        datetime.today().strftime('%Y-%m-%d')).date()]
    if len(vn30f1m_dftd) == 0:
        telegram.send_message('❌ VN30F1M FAILED. NOT FOUND TODAY ❌')
        exit()
    else:
        telegram.send_message('- VN30F1M TODAY: ✅ ' + pd.to_datetime(
            datetime.today().strftime('%Y-%m-%d')).date().strftime('%Y-%m-%d'))

    if (len(vn30f1m_dftd) != 243):
        telegram.send_message('❌ VN30F1M FAILED. NOT ENOUGH DATA ❌')
        telegram.send_message(str(vn30f1m_dftd))
        
    else:
        telegram.send_message('- VN30F1M TODAY: ✅ 243 rows')

    # get vn30 from 2023-12-08
    vn30f1m20231208_df = vn30f1m_df[vn30f1m_df.index.date == pd.to_datetime(
        datetime(2023, 12, 8).strftime('%Y-%m-%d')).date()]
    if (len(vn30f1m20231208_df) != 243):
        telegram.send_message('❌ VN30F1M FAILED. NOT ENOUGH DATA SOURCE ❌')
        exit()
    else:
        telegram.send_message('- VN30F1M 2023-12-08: ✅ 243 rows')

    
    time_dfsource = vn30f1m20231208_df.index.time
    time_dftd = vn30f1m_dftd.index.time
    mismatch_mask = time_dfsource != time_dftd

    # Extract non-matching elements
    non_matching_times = time_dfsource[mismatch_mask]
    
    # Convert to string format if necessary
    non_matching_times_str = non_matching_times.astype(str)
    non_matching_times_str = [str(time) for time in non_matching_times]
    print(non_matching_times_str)

    # Prepare the message
    if len(non_matching_times_str) > 0:
        mismatch_message = "❌ VN30F1M FAILED. Mismatched times: " + ', '.join(non_matching_times_str)
        telegram.send_message(mismatch_message)
        exit()
    else:
        telegram.send_message('- VN30F1M: ✅ 243 rows - FH')
        
    telegram.send_message('- VN30F1M: ✅')

    # &&
    # telegram.send_message('Testing Fund value and Current Portfolio')

    # FUND_VALUE = pd.read_csv("{HOME}/grapechain/PRODUCTION_SPACE/RUNTIME/fund_value.csv".format(HOME=os.getenv("HOME")), index_col=[0], parse_dates=True)
    # FUND_VALUE = FUND_VALUE[FUND_VALUE.index == pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))]
    # if len(FUND_VALUE) == 0:
    #     telegram.send_message('❌ FUND VALUE NOT FOUND. FAILED ❌')
    #     exit()
    # telegram.send_message('Fund value today: ' + str(FUND_VALUE.iloc[-1]['total_stock_amount']))
    # CURRENT_PORTFOLIO_DF = pd.read_csv("{HOME}/grapechain/PRODUCTION_SPACE/RUNTIME/current_port_position.csv".format(HOME=os.getenv("HOME")), index_col=[0], parse_dates=True)
    # CURRENT_PORTFOLIO_DF = CURRENT_PORTFOLIO_DF[CURRENT_PORTFOLIO_DF.index == pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))]
    # if len(CURRENT_PORTFOLIO_DF) == 0:
    #     telegram.send_message('❌ CURRENT PORTFOLIO NOT FOUND. FAILED ❌')
    #     exit()
    # CURRENT_PORTFOLIO_DF = CURRENT_PORTFOLIO_DF[(CURRENT_PORTFOLIO_DF != 0)].dropna(axis=1)
    # #%%
    # for key,value in CURRENT_PORTFOLIO_DF.T.to_dict(orient='dict').items():
    #     telegram.send_message('Current portfolio: ' + str(value))
    # telegram.send_message('- Fund value and Current Portfolio: ✅')

    telegram.send_message('✅ ALL TEST ✅ @binhot')
