
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from models import backtest_strategy_model
from fastapi import FastAPI
from data_downloader import download_financial_data
from analytics import create_analytics
from strategies.RSI import RSI_strategy
from portfolio import Portfolio
import backtester_engine
from logger.std_logger import init_std_logger
from logger import Logger

init_std_logger()

log = Logger("Init", "green")
log.debug('debug message')
log.info('info message')
log.warning('warn message')
log.error('error message')
log.critical('critical message')


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    1/0
    return f'''
       <html >
           <head >
               <title > BackTestiPy Backend < /title >
           </head >
           <body >
               <h1 > BackTestiPy Backend < /h1 >
               <a href = {str(request.url)+"docs"} > <h2 > API Documentation in Swagger < /h2 > </a >
               <a href = {str(request.url)+"redoc"} > <h2 > API Documentation in Redoc < /h2 > </a >
           </body >
       </html >
       '''


@app.post("/backtest_strategy")
def backtest_strategy(backtest_strategy_data: backtest_strategy_model):

    # INFO - Download Data
    financial_data = download_financial_data(
        backtest_strategy_data.input_data.financial_instrument_name,
        backtest_strategy_data.start_date,
        backtest_strategy_data.end_date,
        backtest_strategy_data.input_data.timeframe,
        backtest_strategy_data.input_data.provider
    )

    # INFO - Select Strategy
    strategy = RSI_strategy(
        backtest_strategy_data.indicators_parameters)

    # INFO - Create Portfolio
    # global portfolio
    portfolio = Portfolio(
        initial_value=backtest_strategy_data.initial_portfolio_value,
        starting_date=backtest_strategy_data.start_date,
        strategy=strategy
    )

    # INFO - Backtest
    portfolio, backtest_info = backtester_engine.backtest_strategy(
        portfolio,
        strategy,
        financial_data
    )

    #create_analytics(portfolio, financial_data)
