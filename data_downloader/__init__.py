import pandas_datareader.data as web
import datetime as dt
from datetime import datetime
import requests_cache
from logger import Logger

expire_after = dt.timedelta(days=3)

session = requests_cache.CachedSession(
    cache_name='financial_data_cache', backend='sqlite', expire_after=expire_after)

logger = Logger("Data Downloader", "magenta")


def download_financial_data(financial_instrument_name, start_date, end_date, timeframe, provider):
    start_date_dt = datetime.fromtimestamp(
        float(start_date)/1000)
    end_date_dt = dt.datetime.fromtimestamp(
        float(end_date)/1000)
    df = web.DataReader(
        financial_instrument_name,
        provider,
        start=start_date_dt,
        end=end_date_dt,
    )
    df.reset_index(inplace=True, drop=False)
    df["Date"] = df["Date"].apply(lambda x: int(x.timestamp()*1000))
    logger.info(
        f"Downloaded Financial Data: {financial_instrument_name} from {start_date_dt} to {end_date_dt}")
    return df
