from analytics import create_analytics
import globals
from data_downloader import download_financial_data
from strategies.RSI import RSI_strategy
from portfolio import Portfolio
import backtester_engine
from rich.traceback import install
from logger import Logger
from logger.std_logger import init_std_logger


def init():
    install()
    # INFO - Select Strategy
    strategy = RSI_strategy(
        globals.configuration["indicators_parameters"])

    # INFO - Create file logger
    init_std_logger("logfile.log")

    # INFO - Create logger
    logger = Logger("Init", "green")

    # INFO - Download Data
    financial_data = download_financial_data(
        globals.configuration["input_data"]["financial_instrument_name"],
        globals.configuration["start_date"],
        globals.configuration["end_date"],
        globals.configuration["input_data"]["timeframe"],
        globals.configuration["input_data"]["provider"]
    )

    # INFO - Create Portfolio
    #global portfolio
    portfolio = Portfolio(
        initial_value=globals.configuration["initial_portfolio_value"],
        starting_date=globals.configuration["start_date"],
        strategy=strategy
    )

    # INFO - Backtest
    portfolio, backtest_info = backtester_engine.backtest_strategy(
        portfolio,
        strategy,
        financial_data
    )

    create_analytics(portfolio, financial_data)


if __name__ == "__main__":
    init()
