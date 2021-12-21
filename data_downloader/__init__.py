import pandas_datareader.data as web
import datetime as dt
import requests_cache
from logger import Logger

expire_after = dt.timedelta(days=3)

session = requests_cache.CachedSession(
    cache_name='financial_data_cache', backend='sqlite', expire_after=expire_after)

logger = Logger("Data Downloader", "magenta")


def download_financial_data(financial_instrument_name, start_date, end_date, timeframe, provider):
    start_date_dt = dt.datetime.strptime(start_date, '%d/%m/%Y')
    end_date_dt = dt.datetime.strptime(end_date, '%d/%m/%Y')
    df = web.DataReader(
        financial_instrument_name,
        provider,
        start=start_date_dt,
        end=end_date_dt,

    )
    df.reset_index(inplace=True, drop=False)
    df["Date"] = df["Date"].dt.strftime("%d/%m/%Y %H:%M:%S")
    logger.info(
        f"Downloaded Financial Data: {financial_instrument_name} from {start_date} to {end_date}")
    return df
