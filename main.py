from data_downloader import download_financial_data
import json
from strategies.RSI import RSI_strategy
from portfolio import Portfolio
from backtester_engine import backtester
from rich.traceback import install
from logger import Logger
from logger.std_logger import init_std_logger
import globals

def init():
    
    globals.init_globals()
    with open('./configuration.json') as config_file:
        globals.config = json.load(config_file)
    if globals.config['system']['environment']=="Development"
        install()
    init_std_logger("logfile.log")
    logger = Logger("Main", "green")

    logger.info("Starting main")
    # ? Select Strategy
    strategy = RSI_strategy(
        globals.config["indicators_parameters"])
    # ? Download Data
    financial_data = download_financial_data(
        globals.config["financial_instrument_name"],
        globals.config["start_date"],
        globals.config["end_date"]
    )
    1/0
    # ? Create Portfolio
    portfolio = Portfolio(
        initial_value=globals.config["initial_portfolio_value"],
        startingDate=globals.config["start_date"],
        strategy=strategy
    )
    # ? Backtest
    portfolio = backtester.backtest_strategy(
        portfolio,
        strategy,
        financial_data
    )


if __name__ == "__main__":
    init()
