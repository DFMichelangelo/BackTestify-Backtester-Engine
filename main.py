import globals
from data_downloader import download_financial_data
from strategies.RSI import RSI_strategy
from portfolio import Portfolio
from backtester_engine import backtester
from rich.traceback import install
from logger import Logger
from logger.std_logger import init_std_logger


def init():

    # ? Use rich logger for errors in development
    if globals.configuration['system']['environment'] == "Development":
        install()

    # ? Create file logger
    init_std_logger("logfile.log")

    # ? Create logger
    logger = Logger("Main", "green")
    logger.info("Starting Main")

    # ? State Environment
    logger.info("Environment: " +
                globals.configuration['system']['environment'])

    # ? Select Strategy
    strategy = RSI_strategy(
        globals.configuration["indicators_parameters"])

    # ? Download Data
    financial_data = download_financial_data(
        globals.configuration["financial_instrument_name"],
        globals.configuration["start_date"],
        globals.configuration["end_date"]
    )

    # ? Create Portfolio
    global portfolio
    portfolio = Portfolio(
        initial_value=globals.configuration["initial_portfolio_value"],
        starting_date=globals.configuration["start_date"],
        strategy=strategy
    )

    # ? Backtest
    backtester.backtest_strategy(
        portfolio,
        strategy,
        financial_data
    )


if __name__ == "__main__":
    init()
