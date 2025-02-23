# system
import os

### download


# pandas, numpy
import pandas as pd

import numpy as np
import xarray as xa
# dictionary file
import yaml

from tqdm import tqdm
### time
from datetime import datetime
import logging
import os
from datetime import datetime
import pandas as pd

from grapebot.storage import utils as storage_utils

from grapebot.storage import local as local_storage
from grapebot import utils as grapeutils
from grapebot import telegram
from grapebot.master.notin import fundamental_utils


logger = logging.getLogger()
DATA_PATH = storage_utils.get_data_path() + "/data/"
STORAGE_PATH = storage_utils.get_data_path()

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def strided_axis0(a, fillval, L):  # a is 1D array
    '''
    https://stackoverflow.com/questions/47417420/padding-numpy-rolling-window-operations-using-strides/47418507#47418507
    '''
    a_ext = np.concatenate((np.full(L - 1, fillval), a))
    n = a_ext.strides[0]
    strided = np.lib.stride_tricks.as_strided
    return strided(a_ext, shape=(a.shape[0], L), strides=(n, n))


def getCumulativeReturn(ret1d, numdays=5):
    '''
    how to handle Nan, Inf
    This function will get the historical of cumulative returns
    For example We would like to calculate return5= getCumRethist(return1,5)
    '''
    return np.exp((np.log(1.0 + ret1d)).rolling(numdays).sum()) - 1.


def op_Rol_TS_ewm_std(df, windows=5, half_life=8):
    wtMeanDf = df.copy()
    for name, values in df.items():
        arr = strided_axis0(values, fillval=np.nan, L=windows)
        wtMeanDf[name] = \
            (pd.DataFrame(arr).T.ewm(halflife=half_life, adjust=True).std().T)[
                windows - 1].tolist()
    return wtMeanDf


def readYAML_fiant2(_infile):
    stream = open(_infile, "r")
    mydata = yaml.load(stream, Loader=Loader)
    return pd.DataFrame.from_dict(mydata)


def cleanINF(df):
    df = df.replace(np.inf, np.nan)
    df = df.replace(-np.inf, np.nan)
    return df


def get_market_returns_df2(weight_df, inst_returns, mystocks):
    '''
    calculate market return = sum(weight_ii* return_ii)/sum(weight_ii)
    weight could be CAP, dollar_volume trading in 20days, ....
    we set all stock == the value of market to get the matrix for easy to use
    '''
    index_remove = list(set(weight_df.columns.tolist()) - set(mystocks))
    inst_returns_tmp = (inst_returns.copy())
    inst_returns_tmp[index_remove] = 0.0
    weight_df1 = weight_df.copy()
    weight_df1[index_remove] = 0.0
    tmp_return = inst_returns_tmp.clip(-0.07, 0.07)
    tmp_return = tmp_return[np.abs(tmp_return) > 1e-6]
    tmp_return = tmp_return.replace(np.inf, np.nan)
    tmp_return = tmp_return.replace(-np.inf, np.nan)
    tmpMarketReturns_df = ((weight_df1 * tmp_return).sum(axis=1)) / (
        weight_df1.sum(axis=1))

    b = pd.DataFrame(1., index=inst_returns.index, columns=inst_returns.columns)

    return (b.mul(tmpMarketReturns_df, axis=0))


def get_Beta_Stock_to_market(insReturns_df, marketReturns_df, num_days=252):
    '''
    returns_stock= beta * returns_market + residual_return
    regrssion for 252 by default, but we can change it
    this is an fast_approach way to calculate beta :), we can improve it if we get time
    '''
    # aaa= marketReturns_df.columns.tolist()[0]

    tmpMarket = marketReturns_df.copy()
    tmpStock = insReturns_df.copy()

    var_market_return_df = tmpMarket.rolling(num_days, min_periods=10).var()
    cov_stock_return_df = tmpStock.rolling(num_days, min_periods=10).cov(
        tmpMarket)
    beta_factor_daily = cov_stock_return_df.div(var_market_return_df, axis=0)
    return beta_factor_daily


def get_Beta_Stock_to_market_old(insReturns_df, marketReturns_df, num_days=252):
    '''
    returns_stock= beta * returns_market + residual_return
    regrssion for 252 by default, but we can change it
    this is an fast_approach way to calculate beta :), we can improve it if we get time
    '''
    tmpMarket = marketReturns_df.copy()
    tmpStock = insReturns_df.copy()
    var_market_return_df = tmpMarket.rolling(num_days, min_periods=10).var()
    cov_stock_return_df = tmpStock.apply(
        lambda x: x.rolling(num_days, min_periods=10).cov(tmpMarket),
        axis=0)
    beta_factor_daily = cov_stock_return_df.div(var_market_return_df, axis=0)
    return beta_factor_daily


def get_residual_return(insReturns_df, marketReturns_df):
    '''
    residual_return =  beta * returns_market - returns_stock
    '''
    tmpBeta = get_Beta_Stock_to_market(insReturns_df, marketReturns_df)
    tmp_residual_return = tmpBeta.mul(marketReturns_df, axis=0) - insReturns_df
    return tmp_residual_return


def createUniverse(dict_data_full):
    heat_Rate = dict_data_full['returns'] < -0.06
    myscore_heat_rate = 1 / (heat_Rate.rolling(252, min_periods=1).sum())
    myscore_heat_rate = myscore_heat_rate.replace(np.inf, 1) * 100
    myscore_heat_rate2 = myscore_heat_rate.pow(2)
    dollarTrading = dict_data_full['adjclose'] * dict_data_full['volume']
    mean_dollar_trading = dollarTrading.rolling(63, min_periods=1).sum()
    mean_dollar_trading2 = mean_dollar_trading.ewm(halflife=8).mean()
    mean_dollar_trading3 = mean_dollar_trading2 * myscore_heat_rate2
    rank_DT = mean_dollar_trading3.rank(pct=False, ascending=False, axis=1)
    toplist = np.arange(10, 200, 10)
    dict_top = {}
    for ii in toplist:
        tmp_top = ((rank_DT < ii))
        dict_top[ii] = tmp_top
        # print(ii, len(intersection(dict_top[ii],list_vn30)))
        # list_a= dict_top[ii]
        # list_b= list_vn30
        # print('FLC' in list_a)
        # print([x for x in list_vn30 if x not in list_a])
    return dict_top


def createUniverseDIRECT(dict_data_full,
                         hors_list=['VN30F1M', 'VN30F2M', 'VN30F1Q', 'VN30F2Q', 'VN30']):
    heat_Rate = dict_data_full['returns'] < -0.06
    myscore_heat_rate = 1 / (heat_Rate.rolling(252, min_periods=1).sum())
    myscore_heat_rate = myscore_heat_rate.replace(np.inf, 1) * 100
    myscore_heat_rate2 = myscore_heat_rate.pow(2)
    dollarTrading = dict_data_full['adjclose'] * dict_data_full['volume']
    mean_dollar_trading = dollarTrading.rolling(63, min_periods=1).mean()
    mean_dollar_trading2 = mean_dollar_trading.ewm(halflife=8).mean()
    mean_dollar_trading3 = mean_dollar_trading2 * myscore_heat_rate2
    mean_dollar_trading3[hors_list] = np.nan
    rank_DT = mean_dollar_trading3.rank(pct=False, ascending=False, axis=1)
    toplist = np.arange(10, 210, 10)
    dict_top = {}
    for ii in toplist:
        tmp_top = ((rank_DT < ii))
        dict_data_full['TOP' + str(ii)] = tmp_top
    return dict_data_full


def get_Beta_Stock_to_market2(insReturns_df, marketReturns_df, num_days=252):
    '''
    returns_stock= beta * returns_market + residual_return
    regrssion for 252 by default, but we can change it
    this is an fast_approach way to calculate beta :), we can improve it if we get time
    marketReturn is a matrix ==> take the mean
    '''
    tmpMarket = marketReturns_df.mean(1)
    tmpStock = insReturns_df.copy()
    var_market_return_df = tmpMarket.rolling(num_days, min_periods=10).var()
    cov_stock_return_df = tmpStock.apply(
        lambda x: x.rolling(num_days, min_periods=10).cov(tmpMarket),
        axis=0)
    beta_factor_daily = cov_stock_return_df.div(var_market_return_df, axis=0)
    return beta_factor_daily


def getBaseFromFiant2(indf, file_name='adjRatio'):
    tmpdf = indf.pivot(index='date', columns='symbol', values=file_name)
    if file_name == 'adjRatio':
        tmps2 = tmpdf.replace(np.nan, 1.0)
    else:
        tmps2 = tmpdf.copy()

    list_dates_str = [ii[0:4] + ii[5:7] + ii[8:10] for ii in
                      (tmps2.index.tolist())]
    tmps2.index.name = None
    list_dates = [datetime.strptime(ii, '%Y%m%d').date() for ii in
                  list_dates_str]
    tmps2.index = list_dates
    return tmps2


class PRODbasefiant:
    '''
    please copy two files Shareoutstnading and freefloat to myconstant._project_FOLDER +'/BASE_HIST4PROD/'
    if not, there is no list stock and these data
    '''

    def __init__(self):

        self.parentFolder = STORAGE_PATH
        self.list_items = ['adjRatio', 'buyCount', 'buyForeignQuantity',
                           'buyForeignValue', 'buyQuantity',
                           'currentForeignRoom',
                           'dealVolume', 'priceAverage', 'priceBasic',
                           'priceClose', 'priceHigh', 'priceLow', 'priceOpen',
                           'propTradingNetDealValue', 'propTradingNetPTValue',
                           'propTradingNetValue', 'putthroughValue',
                           'putthroughVolume', 'sellCount',
                           'sellForeignQuantity', 'sellForeignValue',
                           'sellQuantity',
                           'totalValue', 'totalVolume']
        self.list_items_short = ['adjRatio', 'buyCount', 'buyForeignQuantity',
                                 'buyForeignValue', 'buyQuantity',
                                 'currentForeignRoom',
                                 'volume', 'vwap', 'priceBasic', 'close',
                                 'high', 'low', 'open',
                                 'propTradingNetDealValue',
                                 'propTradingNetPTValue', 'propTradingNetValue',
                                 'putthroughValue',
                                 'putthroughVolume', 'sellCount',
                                 'sellForeignQuantity', 'sellForeignValue',
                                 'sellQuantity',
                                 'totalValue', 'totalVolume']

        self.important_item = ['adjRatio', 'volume', 'close', 'high', 'low',
                               'open', 'vwap']
        self.related_file = ['adjRatio', 'dealVolume', 'priceClose',
                             'priceHigh', 'priceLow', 'priceOpen',
                             'priceAverage']
        self.myliststock = ['AAA', 'AAM', 'AAT', 'AAV', 'ABR', 'ABS', 'ABT',
                            'ACB', 'ACC', 'ACL', 'ACM', 'ADC', 'ADG',
                            'ADS', 'AGG', 'AGM', 'AGR', 'ALT', 'AMC', 'AMD',
                            'AME', 'AMV', 'ANV', 'APC', 'APG', 'APH',
                            'API', 'APP', 'APS', 'ARM', 'ART', 'ASG', 'ASM',
                            'ASP', 'AST', 'ATS', 'BAB', 'BAF', 'BAX',
                            'BBC', 'BBS', 'BCC', 'BCE', 'BCF', 'BCG', 'BCM',
                            'BDB', 'BED', 'BFC', 'BHN', 'BIC', 'BID',
                            'BKC', 'BKG', 'BLF', 'BMC', 'BMI', 'BMP',
                            'BNA', 'BPC', 'BRC', 'BSC', 'BSI', 'BST',
                            'BTP', 'BTS', 'BTT', 'BTW', 'BVH', 'BVS', 'BWE',
                            'BXH', 'C32', 'C47', 'C69', 'C92', 'CAG',
                            'CAN', 'CAP', 'CAV', 'CCI', 'CCL', 'CCR', 'CDC',
                            'CDN', 'CEE', 'CEO', 'CET', 'CHP', 'CIA',
                            'CIG', 'CII', 'CJC', 'CKG', 'CKV', 'CLC', 'CLH',
                            'CLL', 'CLM', 'CLW', 'CMC', 'CMG', 'CMS',
                            'CMV', 'CMX', 'CNG', 'COM', 'CPC', 'CRC', 'CRE',
                            'CSC', 'CSM', 'CSV', 'CTB', 'CTC', 'CTD',
                            'CTF', 'CTG', 'CTI', 'CTP', 'CTR', 'CTS', 'CTT',
                            'CTX', 'CVN', 'CVT', 'CX8', 'D11', 'D2D',
                            'DAD', 'DAE', 'DAG', 'DAH', 'DAT', 'DBC', 'DBD',
                            'DBT', 'DC2', 'DC4', 'DCL', 'DCM', 'DDG',
                            'DGC', 'DGW', 'DHA', 'DHC', 'DHG', 'DHM', 'DHP',
                            'DHT', 'DIG', 'DIH', 'DL1', 'DLG', 'DMC',
                            'DNC', 'DNM', 'DNP', 'DP3', 'DPC', 'DPG', 'DPM',
                            'DPR', 'DQC', 'DRC', 'DRH', 'DRL', 'DS3',
                            'DSN', 'DST', 'DTA', 'DTC', 'DTD', 'DTK', 'DTL',
                            'DTT', 'DVG', 'DVP', 'DXG', 'DXP', 'DXS',
                            'DXV', 'DZM', 'EBS', 'ECI', 'EIB', 'EID', 'ELC',
                            'EMC', 'EVE', 'EVF', 'EVG', 'EVS', 'FCM',
                            'FCN', 'FDC', 'FID', 'FIR', 'FIT', 'FMC',
                            'FPT', 'FRT', 'FTS', 'GAB', 'GAS', 'GDT',
                            'GDW', 'GEG', 'GEX', 'GIC', 'GIL', 'GKM', 'GLT',
                            'GMA', 'GMC', 'GMD', 'GMH', 'GMX', 'GSP',
                            'GTA', 'GVR', 'HAD', 'HAG', 'HAH', 'HAP',
                            'HAR', 'HAS', 'HAT', 'HAX', 'HBC', 'HBS',
                            'HCC', 'HCD', 'HCM', 'HCT', 'HDA', 'HDB', 'HDC',
                            'HDG', 'HEV', 'HGM', 'HHC',  'HHP',
                            'HHS', 'HHV', 'HID', 'HII', 'HJS', 'HKT', 'HLC',
                            'HLD', 'HMC', 'HMH', 'HMR', 'HNG', 'HOM',
                            'HOT', 'HPG', 'HPM', 'HPX', 'HQC', 'HRC', 'HSG',
                            'HSL', 'HT1', 'HTC', 'HTI', 'HTL', 'HTN',
                            'HTP', 'HTV', 'HU1', 'HU3', 'HUB', 'HUT', 'HVH',
                            'HVN', 'HVT', 'HVX', 'IBC', 'ICG', 'ICT',
                            'IDC', 'IDI', 'IDJ', 'IDV', 'IJC', 'ILB', 'IMP',
                            'INC', 'INN', 'IPA', 'ITA', 'ITC', 'ITD',
                            'ITQ', 'IVS', 'JVC', 'KBC', 'KDC', 'KDH', 'KDM',
                            'KHG', 'KHP', 'KHS', 'KKC', 'KLF', 'KMR',
                            'KMT', 'KOS', 'KPF', 'KSB', 'KSD', 'KSF', 'KSQ',
                            'KST', 'KTS', 'KTT',  'L10', 'L14',
                            'L18',  'L40', 'L43', 'L61', 'L62', 'LAF',
                            'LAS', 'LBE', 'LBM', 'LCD', 'LCG', 'LCM',
                            'LCS', 'LDG', 'LDP', 'LEC', 'LGC', 'LGL', 'LHC',
                            'LHG', 'LIG', 'LIX', 'LM8', 'LPB',
                            'LSS', 'LUT', 'MAC', 'MAS', 'MBB', 'MBG', 'MBS',
                            'MCC', 'MCF', 'MCO', 'MCP', 'MDC',
                            'MDG', 'MED', 'MEL', 'MHC', 'MHL', 'MIG', 'MIM',
                            'MKV', 'MSB', 'MSH', 'MSN', 'MST', 'MVB',
                            'MWG', 'NAF', 'NAG', 'NAP', 'NAV', 'NBB', 'NBC',
                            'NBP', 'NBW', 'NCT', 'NDN', 'NDX', 'NET',
                            'NFC', 'NHA', 'NHC', 'NHH', 'NHT', 'NKG', 'NLG',
                            'NNC', 'NRC', 'NSC', 'NSH', 'NST', 'NT2',
                            'NTH', 'NTL', 'NTP', 'NVB', 'NVL', 'NVT', 'OCB',
                            'OCH', 'OGC', 'ONE', 'OPC', 'ORS', 'PAC',
                            'PAN', 'PBP', 'PC1', 'PCE', 'PCG', 'PCT', 'PDB',
                            'PDC', 'PDN', 'PDR', 'PEN', 'PET', 'PGC',
                            'PGD', 'PGI', 'PGN', 'PGS', 'PGT', 'PGV', 'PHC',
                            'PHN', 'PHP', 'PHR', 'PIA', 'PIC', 'PIT',
                            'PJC', 'PJT', 'PLC', 'PLP', 'PLX', 'PMB', 'PMC',
                            'PMG', 'PMP', 'PMS', 'PNC', 'PNJ', 'POM',
                            'POT', 'POW', 'PPC', 'PPE', 'PPP', 'PPS', 'PPY',
                            'PRC', 'PRE', 'PSC', 'PSD', 'PSE', 'PSH',
                            'PSI', 'PSW', 'PTB', 'PTC', 'PTD', 'PTI', 'PTL',
                            'PTS', 'PV2', 'PVB', 'PVC', 'PVD', 'PVG',
                            'PVI', 'PVS', 'PVT', 'QBS', 'QCG', 'QHD',
                            'QST', 'QTC', 'RAL', 'RCL', 'RDP', 'REE',
                            'ROS', 'S4A', 'S55', 'S99', 'SAB', 'SAF', 'SAM',
                            'SAV', 'SBA', 'SBT', 'SBV', 'SC5', 'SCD',
                            'SCG', 'SCI', 'SCR', 'SCS', 'SD2', 'SD4', 'SD5',
                            'SD6', 'SD9', 'SDA', 'SDC', 'SDG', 'SDN',
                            'SDT', 'SDU', 'SEB', 'SED', 'SFC', 'SFG', 'SFI',
                            'SFN', 'SGC', 'SGD', 'SGH', 'SGN', 'SGR',
                            'SGT', 'SHA', 'SHB', 'SHE', 'SHI', 'SHN', 'SHP',
                            'SHS', 'SIC', 'SII', 'SJ1', 'SJD', 'SJE',
                            'SJF', 'SJS', 'SKG', 'SLS', 'SMA', 'SMB', 'SMC',
                            'SMN', 'SMT', 'SPC', 'SPI', 'SPM', 'SRA',
                            'SRC', 'SRF', 'SSB', 'SSC', 'SSI', 'SSM', 'ST8',
                            'STB', 'STC', 'STG', 'STK', 'STP', 'SVC',
                            'SVD', 'SVI', 'SVN', 'SVT', 'SZB', 'SZC', 'SZL',
                            'TA9', 'TAR', 'TBC', 'TBX', 'TC6', 'TCB',
                            'TCD', 'TCH', 'TCL', 'TCM', 'TCO', 'TCR', 'TCT',
                            'TDC', 'TDG', 'TDH', 'TDM', 'TDN', 'TDP',
                            'TDT', 'TDW', 'TEG', 'TET', 'TFC', 'TGG', 'THB',
                            'THD', 'THG', 'THI', 'THS', 'THT', 'TIG',
                            'TIP', 'TIX', 'TJC', 'TKC', 'TKU', 'TLD', 'TLG',
                            'TLH', 'TMB', 'TMC', 'TMP', 'TMS', 'TMT',
                            'TMX', 'TN1', 'TNA', 'TNC', 'TNG', 'TNH', 'TNI',
                            'TNT', 'TOT', 'TPB', 'TPC', 'TPH', 'TPP',
                            'TRA', 'TRC', 'TSB', 'TSC', 'TST', 'TTA', 'TTB',
                            'TTC', 'TTE', 'TTF', 'TTH', 'TTL', 'TTT',
                            'TTZ', 'TV2', 'TV3', 'TV4', 'TVB', 'TVC', 'TVD',
                            'TVS', 'TVT', 'TXM', 'TYA', 'UIC',
                            'UNI', 'V12', 'V21', 'VAF', 'VBC', 'VC1', 'VC2',
                            'VC3', 'VC6', 'VC7', 'VC9', 'VCA', 'VCB',
                            'VCC', 'VCF', 'VCG', 'VCI', 'VCM', 'VCS', 'VDL',
                            'VDP', 'VDS', 'VE1', 'VE2', 'VE3', 'VE4',
                            'VE8', 'VFG', 'VGC', 'VGP', 'VGS', 'VHC', 'VHE',
                            'VHL', 'VHM', 'VIB', 'VIC', 'VID', 'VIE',
                            'VIF', 'VIG', 'VIP', 'VIT', 'VIX', 'VJC',
                            'VLA', 'VMC', 'VMD', 'VMS', 'VNC', 'VND',
                            'VNE', 'VNF', 'VNG', 'VNL', 'VNM', 'VNR', 'VNS',
                            'VNT', 'VOS', 'VPB', 'VPD', 'VPG', 'VPH',
                            'VPI', 'VPS', 'VRC', 'VRE', 'VSA', 'VSC', 'VSH',
                            'VSI', 'VSM', 'VTB', 'VTC', 'VTH', 'VTJ',
                            'VTO', 'VTV', 'VTZ', 'VXB', 'WCS', 'WSS',
                            'X20', 'YBM', 'YEG', 'DVM']
        self.liststock = []
        self.dict_data_full = {}

    def buildData(self):
        ###buildListStock(self):
        '''
        this version build on 27/06/2022, i fixed the universe stock base on ShareOutstanding Get from fundamental ratio
        ==> next version should build Universe
        '''
        # list_stock, list_future, list_index, mylogger= utils.getInstrument(_parent_folder)
        # get data from

        logger.info("Reading Live_share CSV building future")
        telegram.send_message("[-] Reading Live_share CSV building future")
        try:
            tmp = pd.read_csv(self.parentFolder + '/total/live_share.csv')
            tmp = tmp.set_index(['date'])
            a = sorted(tmp.columns.tolist())
            b = ['VN30', 'VN30F1M', 'VN30F1Q', 'VN30F2M', 'VN30F2Q']
            new_list = [x for x in a if (x not in b)]
            self.liststock = new_list
            # print("Nums: " + str(int(len(self.liststock))))
        except Exception as e:
            self.liststock = self.myliststock
            logger.error("FAILED TO READ LIVESHARE")
            logger.critical(e)
            exit()

        self.liststock = self.myliststock

        print("Nums: " + str(int(len(self.liststock))))
        telegram.send_message("[-] Reading FANT HOLC")
        logger.info("Reading FANT HOLC")
        new_df = pd.read_csv(self.parentFolder + '/total/fant_holc.csv')

        tmp_new_stock = list(set(new_df['symbol'].tolist()))
        # dump self.liststock = tmp_new_stock
        # dump self.liststock.remove('CMM')
        # ------
        mycommon_stock = list(set(tmp_new_stock).intersection(self.liststock))
        self.liststock = mycommon_stock

        # --

        print("Nums after: " + str(int(len(self.liststock))))
        # exit()
        for ii, jj in zip(self.list_items_short, self.list_items):
            # tmp_df = new_df.pivot(index='date', columns='symbol', values=jj)
            tmp_df = getBaseFromFiant2(new_df, file_name=jj)
            self.dict_data_full[ii] = tmp_df[self.liststock]
        # build return log and normal return
        self.dict_data_full['adjclose'] = self.dict_data_full['close'] / \
                                          self.dict_data_full['adjRatio']
        self.dict_data_full['returns'] = self.dict_data_full['adjclose'] / \
                                         self.dict_data_full['adjclose'].shift(
                                             1) - 1.
        self.dict_data_full['log_returns'] = np.log(
            self.dict_data_full['adjclose'] / self.dict_data_full[
                'adjclose'].shift(1))

        print("Nums: " + str(self.dict_data_full['log_returns'].shape))
        # print(self.dict_data_full['adjclose'].columns.tolist())

        telegram.send_message("[-] Building volumes")
        # build sma volume for ...
        logger.info("Building volumes")
        list_volume = [10, 15, 20, 60, 125, 250]
        list_name_volume = ['adv' + str(ii) for ii in list_volume]

        for windows_ii, name_ii in zip(list_volume, list_name_volume):
            tmp1 = self.dict_data_full['volume'].fillna(0)
            tmpdf = tmp1.rolling(windows_ii, min_periods=1).mean()
            tmpdf = tmpdf[np.abs(tmpdf) > 1]
            self.dict_data_full[name_ii] = tmpdf
            # build dollar trading adv20
        self.dict_data_full['dadv20'] = (
                self.dict_data_full['close'] * self.dict_data_full['adv20'])
        #####build_marketResidual(self)  :

        self.dict_data_full['marketReturn'] = get_market_returns_df2(
            self.dict_data_full['dadv20'], self.dict_data_full['returns'],
            self.liststock)
        self.dict_data_full['MarketBeta'] = get_Beta_Stock_to_market(
            self.dict_data_full['returns'],
            self.dict_data_full['marketReturn'], num_days=252)
        self.dict_data_full['residualMarketReturn'] = self.dict_data_full[
                                                          'MarketBeta'] * \
                                                      self.dict_data_full[
                                                          'marketReturn'] - \
                                                      self.dict_data_full[
                                                          'returns']
        self.dict_data_full['short_volatility'] = op_Rol_TS_ewm_std(
            self.dict_data_full['returns'].clip(-0.2, 0.2), 22, 8)

        ######def build_industry(self)  :
        name_IX = ['Sector', 'Industry', 'Exchange']
        for sector_ii in name_IX:
            sector_file = STORAGE_PATH + "/total/sector/prod/" + sector_ii + '_Master.yaml'
            with open(sector_file) as file:
                mysector_data = yaml.full_load(file)
            file.close()

            tmp = pd.DataFrame([mysector_data])[
                self.dict_data_full['returns'].columns.tolist()]
            tmp.index = [self.dict_data_full['returns'].index.tolist()[-1]]
            tmp2 = pd.DataFrame(np.nan,
                                index=self.dict_data_full['returns'].index,
                                columns=self.dict_data_full['returns'].columns)
            tmp2.iloc[-1] = tmp
            tmp3 = tmp2.bfill()
            self.dict_data_full[sector_ii] = tmp3.astype(int)

        tmp = pd.read_csv(self.parentFolder + '/total/live_share.csv')
        tmp = tmp.set_index('date')
        logger.info('Logger')
        logger.info(tmp.index.tolist())
        print(tmp.index.tolist()[0])

        list_dates_str = []
        for ii in tmp.index.tolist():
            # print(ii)
            if len(ii) < 9:
                print(ii)
            list_dates_str.append(ii[6:10] + ii[3:5] + ii[0:2])

        list_dates = [datetime.strptime(ii, '%Y%m%d').date() for ii in
                      list_dates_str]
        tmp.index = list_dates
        self.dict_data_full['ShareOutstanding'] = tmp[self.liststock]
        self.dict_data_full['MarketCap'] = self.dict_data_full[
                                               'ShareOutstanding'] * \
                                           self.dict_data_full['close']
        self.dict_data_full['MarketCap'] = self.dict_data_full['MarketCap'][
            self.liststock]
        # return self.dict_data_full
        # return dict_data_full

        dict_data_full2 = self.dict_data_full.copy()
        key_xarray = [items_ii for items_ii, value in dict_data_full2.items()]
        # print(key_xarray)
        list_xarray = []
        for item_ii in tqdm(key_xarray):
            # THIS IS PRODUCTION
            tmpdf1 = dict_data_full2[item_ii].truncate(before=datetime.strptime("20120101", '%Y%m%d').date())
            # END PRODUCTION

            # TEST

            # tmpdf1 = dict_data_full2[item_ii].truncate(before=datetime.strptime("20100101", '%Y%m%d').date())

            # END TEST
            # Change date 01-01-2012 Start day here
            '''
                @Param start day here
            '''
            tmpdf = cleanINF(tmpdf1)
            # print(tmpdf.shape)
            tmp_xa = xa.DataArray(tmpdf, coords=[
                pd.DatetimeIndex(tmpdf.index.tolist()),
                pd.Index(tmpdf.columns.tolist())], dims=["date", "uid"])
            list_xarray.append(tmp_xa)
        fullReturnsXA = xa.concat(list_xarray,
                                  pd.Index(key_xarray, name="fields"))

        date_ii = datetime.today().strftime("%Y%m%d")

        # file_backup = STORAGE_PATH + '/netcdf/backup/Fiant_Base_production.netcdf_' + str(
        #     date_ii)
        storage_utils.create_global_file("netcdf/prod/")
        file_production = STORAGE_PATH + "/netcdf/prod/S_Fiant_Base_production.netcdf"

        file_today = STORAGE_PATH + "/netcdf/S_Fiant_Base_production_" + grapeutils.today_not_in() + ".netcdf"
        telegram.send_message("[-] Export...")
        telegram.send_message("🤖 BUILDING SUCCESS !")

        local_storage.create_folder_if_not_exist(file_production)
        # local_storage.create_folder_if_not_exist(file_backup)

        fullReturnsXA.to_netcdf(file_production)
        # fullReturnsXA.to_netcdf(file_backup)

        telegram.send_message("🤖 EXPORT NETCDF !")

    def buildData_full(self):
        ###buildListStock(self):
        '''
        this version build on 27/06/2022, i fixed the universe stock base on ShareOutstanding Get from fundamental ratio
        ==> next version should build Universe
        '''
        # list_stock, list_future, list_index, mylogger= utils.getInstrument(_parent_folder)
        # get data from

        logger.info("Reading Live_share CSV building future")
        try:
            tmp = pd.read_csv(self.parentFolder + '/total/live_share.csv')
            tmp = tmp.set_index(['date'])
            a = sorted(tmp.columns.tolist())
            b = ['VN30', 'VN30F1M', 'VN30F1Q', 'VN30F2M', 'VN30F2Q']
            new_list = [x for x in a if (x not in b)]
            self.liststock = new_list
            # print("Nums: " + str(int(len(self.liststock))))
        except:
            # self.liststock = self.myliststock
            logger.error("FAILED TO READ LIVESHARE")
            exit()

        # self.liststock = self.myliststock

        print("Nums: " + str(int(len(self.liststock))))
        telegram.send_message("[-] Reading FANT HOLC")
        logger.info("Reading FANT HOLC")
        new_df = pd.read_csv(self.parentFolder + '/total/fant_holc.csv')

        tmp_new_stock = list(set(new_df['symbol'].tolist()))
        self.liststock = tmp_new_stock
        self.liststock.remove('CMM')
        # ------
        mycommon_stock = list(set(tmp_new_stock).intersection(self.liststock))
        self.liststock = mycommon_stock

        # --

        print("Nums after: " + str(int(len(self.liststock))))
        for ii, jj in zip(self.list_items_short, self.list_items):
            # tmp_df = new_df.pivot(index='date', columns='symbol', values=jj)
            tmp_df = getBaseFromFiant2(new_df, file_name=jj)
            self.dict_data_full[ii] = tmp_df[self.liststock]
        # build return log and normal return
        self.dict_data_full['adjclose'] = self.dict_data_full['close'] / \
                                          self.dict_data_full['adjRatio']
        self.dict_data_full['returns'] = self.dict_data_full['adjclose'] / \
                                         self.dict_data_full['adjclose'].shift(
                                             1) - 1.
        self.dict_data_full['log_returns'] = np.log(
            self.dict_data_full['adjclose'] / self.dict_data_full[
                'adjclose'].shift(1))

        print("Nums: " + str(self.dict_data_full['log_returns'].shape))
        # print(self.dict_data_full['adjclose'].columns.tolist())

        telegram.send_message("[-] Building volumes")
        # build sma volume for ...
        logger.info("Building volumes")
        list_volume = [10, 15, 20, 60, 125, 250]
        list_name_volume = ['adv' + str(ii) for ii in list_volume]

        for windows_ii, name_ii in zip(list_volume, list_name_volume):
            tmp1 = self.dict_data_full['volume'].fillna(0)
            tmpdf = tmp1.rolling(windows_ii, min_periods=1).mean()
            tmpdf = tmpdf[np.abs(tmpdf) > 1]
            self.dict_data_full[name_ii] = tmpdf
            # build dollar trading adv20
        self.dict_data_full['dadv20'] = (
                self.dict_data_full['close'] * self.dict_data_full['adv20'])
        #####build_marketResidual(self)  :

        self.dict_data_full['marketReturn'] = get_market_returns_df2(
            self.dict_data_full['dadv20'], self.dict_data_full['returns'],
            self.liststock)
        self.dict_data_full['MarketBeta'] = get_Beta_Stock_to_market(
            self.dict_data_full['returns'],
            self.dict_data_full['marketReturn'], num_days=252)
        self.dict_data_full['residualMarketReturn'] = self.dict_data_full[
                                                          'MarketBeta'] * \
                                                      self.dict_data_full[
                                                          'marketReturn'] - \
                                                      self.dict_data_full[
                                                          'returns']
        self.dict_data_full['short_volatility'] = op_Rol_TS_ewm_std(
            self.dict_data_full['returns'].clip(-0.2, 0.2), 22, 8)

        name_IX = ['Sector', 'Industry', 'Exchange']
        for sector_ii in name_IX:
            sector_file = STORAGE_PATH + "/total/sector/prod/" + sector_ii + '_Master.yaml'
            with open(sector_file) as file:
                mysector_data = yaml.full_load(file)
            file.close()

            tmp = pd.DataFrame([mysector_data])[
                self.dict_data_full['returns'].columns.tolist()]
            tmp.index = [self.dict_data_full['returns'].index.tolist()[-1]]
            tmp2 = pd.DataFrame(np.nan,
                                index=self.dict_data_full['returns'].index,
                                columns=self.dict_data_full['returns'].columns)
            tmp2.iloc[-1] = tmp
            tmp3 = tmp2.bfill()
            self.dict_data_full[sector_ii] = tmp3.astype(int)

        tmp = pd.read_csv(self.parentFolder + '/total/live_share.csv')
        tmp = tmp.set_index('date')
        logger.info('Logger')
        logger.info(tmp.index.tolist())
        # print(tmp.index.tolist()[0])
        list_dates_str = [ii[6:10] + ii[3:5] + ii[0:2] for ii in
                          tmp.index.tolist()]
        list_dates = [datetime.strptime(ii, '%Y%m%d').date() for ii in
                      list_dates_str]
        tmp.index = list_dates
        self.dict_data_full['ShareOutstanding'] = tmp[self.liststock]
        self.dict_data_full['MarketCap'] = self.dict_data_full[
                                               'ShareOutstanding'] * \
                                           self.dict_data_full['close']
        self.dict_data_full['MarketCap'] = self.dict_data_full['MarketCap'][
            self.liststock]
        # return self.dict_data_full
        # return dict_data_full

        dict_data_full2 = self.dict_data_full.copy()
        key_xarray = [items_ii for items_ii, value in dict_data_full2.items()]
        # print(key_xarray)
        list_xarray = []
        for item_ii in tqdm(key_xarray):
            # print(item_ii)
             #PROD CHANGE DATE 2012
            tmpdf1 = dict_data_full2[item_ii].truncate(before=datetime.strptime("20120101", '%Y%m%d').date())
            # TEST ONLY
            # tmpdf1 = dict_data_full2[item_ii].truncate(before=datetime.strptime("20100101", '%Y%m%d').date())



            tmpdf = cleanINF(tmpdf1)
            # print(tmpdf.shape)
            tmp_xa = xa.DataArray(tmpdf, coords=[
                pd.DatetimeIndex(tmpdf.index.tolist()),
                pd.Index(tmpdf.columns.tolist())], dims=["date", "uid"])
            list_xarray.append(tmp_xa)
        fullReturnsXA = xa.concat(list_xarray,
                                  pd.Index(key_xarray, name="fields"))

        date_ii = datetime.today().strftime("%Y%m%d")

        storage_utils.create_global_file("netcdf/prod/")
        file_production = STORAGE_PATH + "/netcdf/prod/FULL_S_Fiant_Base_production.netcdf"

        telegram.send_message("🤖 BUILDING SUCCESS !")

        local_storage.create_folder_if_not_exist(file_production)
        # local_storage.create_folder_if_not_exist(file_backup)

        fullReturnsXA.to_netcdf(file_production)
        # fullReturnsXA.to_netcdf(file_backup)

        telegram.send_message("🤖 EXPORTED NETCDF !")


def main():
    telegram.send_message("🤖 PREPARE ENV FOR NETCDF BUILD")
    vnd = PRODbasefiant()
    telegram.send_message("🤖 Prepare environment to build NetCDF")

    telegram.send_message("🤖 BUILDING NETCDF")

    vnd.buildData()
    # vnd.buildData_full()

    telegram.send_message("🤖 BUILDING FUNDAMENTAL")
    fundamental_utils.main()