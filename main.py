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
    # ? Initialize global variables
    globals.init_globals()

    # ? Set configuration file as global variable    
    with open('./configuration.json') as config_file:
        globals.config = json.load(config_file)
    
    # ? Use rich logger for errors in development
    if globals.config['system']['environment'] == "Development":
        install()
    
    # ? Create file logger
    init_std_logger("logfile.log")

    # ? Create logger
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
    # ? Create Portfolio
    portfolio = Portfolio(
        initial_value=globals.config["initial_portfolio_value"],
        starting_date=globals.config["start_date"],
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
