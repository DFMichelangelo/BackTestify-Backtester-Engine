import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import requests_cache
import datetime as dt
from logger import Logger

expire_after = dt.timedelta(days=3)

session = requests_cache.CachedSession(
    cache_name='financial_data_cache', backend='sqlite', expire_after=expire_after)

logger = Logger("Data Downloader", "#bafa")


def download_financial_data(financial_instrument_name, start_date, end_date):
    df = web.DataReader(
        financial_instrument_name,
        'yahoo',
        start=start_date,
        end=end_date
    )
    df.reset_index(inplace=True, drop=False)
    logger.info("Downloaded Financial Data: " + financial_instrument_name)
    return df
#    df = web.DataReader(
#        financial_instrument_name,
#        'yahoo',
#        timeframe,
#        start=dt.datetime.strptime(start_date, '%d/%m/%Y'),
#        end=dt.datetime.strptime(end_date, '%d/%m/%Y'),
#        # api_key=api_key,
#        session=session)
#
