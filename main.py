from fastapi import FastAPI
import globals
from typing import Optional
from pydantic import BaseModel
from fastapi.logger import logger
'''
from data_downloader import download_financial_data
from analytics import create_analytics

from strategies.RSI import RSI_strategy
from portfolio import Portfolio
import backtester_engine
from rich.traceback import install

from logger import Logger
from logger.std_logger import init_std_logger
# INFO - Use rich logger for errors in development
if globals.configuration['system']['environment'] == "Development":
    install()

# INFO - Create file logger
init_std_logger("logfile.log")

# INFO - Create logger
logger = Logger("Main", "green")
logger.info("Starting Main")
# INFO - State Environment
logger.info("Environment: " +
            globals.configuration['system']['environment'])
'''
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
def echo():
    return {"Hello": "World"}


class input_data_model(BaseModel):
    timeframe: str
    financial_instrument_name: str
    provider: str


class backtest_strategy_model(BaseModel):
    start_date: str
    end_date: str
    input_data: input_data_model
    initial_portfolio_value: float
    indicators_parameters: list


@app.post("/backtest_strategy")
def backtest_strategy(backtest_strategy_data: backtest_strategy_model):
    # def backtest_strategy(backtest_strategy_data: backtest_strategy_model):
    return backtest_strategy_data
    # INFO - Download Data
    financial_data = download_financial_data(
        globals.configuration["input_data"]["financial_instrument_name"],
        globals.configuration["start_date"],
        globals.configuration["end_date"],
        globals.configuration["input_data"]["timeframe"],
        globals.configuration["input_data"]["provider"]
    )

    # INFO - Select Strategy
    strategy = RSI_strategy(
        globals.configuration["indicators_parameters"])

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
