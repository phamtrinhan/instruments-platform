__version__ = '1.1.2'

import datetime

# CONFIG BY DEFAULT
USER_AGENT_DEFAULT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

# PATH
INTRADAY_STOCK_PATH = 'data/{source}/{YYYY}/{MM}/{DD}/{HH}_{mm}_{ss}/{file_name}.json'
DEFAULT_PATH = INTRADAY_STOCK_PATH
# DEFAULT_PATH = 'data/{source}/{YYYY}/{MM}/{DD}/{file_name}.json'

# TELEGRAM
TELEGRAM_SEND_MESSAGE = "https://api.telegram.org/bot{token}/sendMessage"

# SSI
SSI_GRAPHQL_GATEWAY_EP = "https://wgateway-iboard.ssi.com.vn/graphql"
SSI_STOCK_EP = "https://fiin-technical.ssi.com.vn/PriceData/GetLatestPrice?language=en&OrganCode={stock}&Code={stock}"
SSI_STOCK_TICKER_SERIES = "https://fiin-market.ssi.com.vn/WatchList/GetTickerSeries?language=en&OrganCode={stock}&TimeRange={time}&id=1"
SSI_STOCK_INDUSTRY = "https://fiin-core.ssi.com.vn/Master/GetAllIcbIndustry?language={lang}"
SSI_COM_LIST = "https://fiin-core.ssi.com.vn/Master/GetAllCompanyGroup?language={lang}"
SSI_HISTORY_CHART = "https://iboard.ssi.com.vn/dchart/api/history?resolution={res}&symbol={stock}&from={fromDate}&to={toDate}"
SSI_LATEST_PRICE = "https://fiin-technical.ssi.com.vn/PriceData/GetLatestPrice?language=en&Code={stock}"
SSI_FINANCE_REPORT = "https://fiin-fundamental.ssi.com.vn/Snapshot/GetSnapshotNoneBank?language=en&OrganCode={stock}"
SSI_COMPANY_SCORE = "https://fiin-fundamental.ssi.com.vn/Snapshot/GetCompanyScore?language=en&OrganCode={stock}"
SSI_SNAPSHOT = "https://fiin-fundamental.ssi.com.vn/Snapshot/GetSnapshotNoneBank?language=en&OrganCode{stock}"
SSI_BALANCE_SHEET = "https://fiin-fundamental.ssi.com.vn/FinancialStatement/GetBalanceSheet?language=en&OrganCode={stock}"

# VNDIRECT
VNDIRECT_STOCK_LIST_INDUSTRY = "https://api-finfo.vndirect.com.vn/v4/industry_classification?q=industryLevel:{level}"
VNDIRECT_TRADE_DAY = "https://finfo-api.vndirect.com.vn/v4/trading_calendars?sort=date:desc&fields=date&size=9999&q=date:lte:{milestone}"

# FIREANT
FIREANT_FINANCE_REPORT = "https://restv2.fireant.vn/symbols/{stock}/full-financial-reports?type=1&year={year}&quarter={quarter}"
FIREANT_HISTORICAL = "https://restv2.fireant.vn/symbols/{stock}/historical-quotes?startDate={start_date}&endDate={end_date}&limits={limit}"
FIREANT_INSTRUMENTS = "https://restv2.fireant.vn/instruments"
FIREANT_HISTORICAL_QUOTE_BEFORE = "https://svr6.fireant.vn/api/Data/Markets/HistoricalQuotesBefore?symbol={stock}&day={day}"
FIREANT_ALL_FINANCE_INFO = "https://svr6.fireant.vn/api/Data/Finance/AllLastestFinancialInfo"
FIREANT_LATEST_FINANCE_REPORT = "https://svr9.fireant.vn/api/Data/Finance/LastestFinancialReports?symbol={stock}&type=1&year={year}&quarter={quarter}&count={count}"
FIREANT_QUARTER_FINANCE_REPORT = "https://svr8.fireant.vn/api/Data/Finance/QuarterlyFinancialInfo?symbol={stock}&fromYear=2000&fromQuarter=1&toYear={year}&toQuarter=4"
FIREANT_YEARLY_FINANCE_REPORT = "https://svr8.fireant.vn/api/Data/Finance/YearlyFinancialInfo?symbol={stock}&fromYear=2000&toYear={year}"
FIREANT_INTRADAY_QUOTES_8 = "https://svr8.fireant.vn/api/Data/Markets/IntradayQuotes?symbol={stock}"
FIREANT_FUNDAMENTAL = "https://restv2.fireant.vn/symbols/{stock}/fundamental"
FIREANT_TIMESCALE = "https://restv2.fireant.vn/symbols/{stock}/timescale-marks?startDate=2000-01-01&endDate=2037-01-01"
FIREANT_COMPANY_PROFILE = "https://restv2.fireant.vn/symbols/{stock}/profile"
FIREANT_OFFICERS = "https://restv2.fireant.vn/symbols/{stock}/profile"
FIREANT_SUBSIDIARIES = "https://restv2.fireant.vn/symbols/{stock}/subsidiaries"
FIREANT_HOLDERS = "https://restv2.fireant.vn/symbols/{stock}/holders"
FIREANT_DIVIDENDS = "https://restv2.fireant.vn/symbols/{stock}/dividends"
FIREANT_FINANCE_INDICATORS = "https://restv2.fireant.vn/symbols/{stock}/financial-indicators"
FIREANT_FULL_FINANCE_REPORTS = "https://restv2.fireant.vn/symbols/{stock}/full-financial-reports?type=1&year={year}&quarter={quarter}&limit=100"
FIREANT_FINANCE_REPORT_BY_TYPE = "https://restv2.fireant.vn/symbols/{stock}/financial-reports?type={type}&period={period}&compact=True&offset=0&limit=1000"
FIREANT_HOLDERS_TRANSACTION = "https://restv2.fireant.vn/symbols/{stock}/holder-transactions?startDate=&endDate=&executedOnly=false&offset=0&limit=2000"
FIREANT_TIMESCALE_MARKS = "https://restv2.fireant.vn/symbols/{stock}/timescale-marks?startDate={start_date}&endDate={end_date}"
FIREANT_INTRADAY_QUOTES_6 = "https://svr6.fireant.vn/api/Data/Markets/IntradayQuotes?symbol={stock}"
FIREANT_INTRADAY_MARKET = "https://svr6.fireant.vn/api/Data/Markets/IntradayMarketStatistic?symbol={stock}"

# HOSE
HOSE_END_WORKING_HOURS = 17
HOSE_INDEX_END_DAY = "https://www.hsx.vn/Modules/Rsde/Report/QuoteReport?pageFieldName1=Date&pageFieldValue1={date}&pageFieldOperator1=eq&pageFieldName2=KeyWord&pageFieldValue2=&pageFieldOperator2=&pageFieldName3=IndexType&pageFieldValue3=0&pageFieldOperator3=&pageCriteriaLength=3&_search=false&nd=1618727259771&rows=2147483647&page=1&sidx=id&sord=desc"
HOSE_FOREIGN_BUY_VOLUME = "https://www.hsx.vn/Modules/Chart/StaticChart/GetForeignBuyVolumnChart?stockSymbol={stock}&rangeSelector=8"
HOSE_FOREIGN_SELL_VOLUME = "https://www.hsx.vn/Modules/Chart/StaticChart/GetForeignSellVolumnChart?stockSymbol={stock}&rangeSelector=8"
HOSE_AVG_BUY_ORDER = "https://www.hsx.vn/Modules/Chart/StaticChart/GetAvgBuyOrderChart?stockSymbol={stock}&rangeSelector=8"
HOSE_AVG_SELL_ORDER = "https://www.hsx.vn/Modules/Chart/StaticChart/GetAvgSellOrderChart?stockSymbol={stock}&rangeSelector=8"
HOSE_BOS_RATIO = "https://www.hsx.vn/Modules/Chart/StaticChart/GetBuyOnSellRatioChart?stockSymbol={stock}&rangeSelector=8"
HOSE_BOS_VOLUME = "https://www.hsx.vn/Modules/Chart/StaticChart/GetBuyOnSellVolumnChart?stockSymbol={stock}&rangeSelector=8"
HOSE_BOS_ORDER = "https://www.hsx.vn/Modules/Chart/StaticChart/GetBuyOnSellOrderChart?stockSymbol={stock}&rangeSelector=8"
