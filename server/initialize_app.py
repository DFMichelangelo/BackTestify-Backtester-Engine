
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from models import backtest_strategy_model
from fastapi import FastAPI
from data_downloader import download_financial_data
from strategies.RSI import RSI_strategy
from portfolio import Portfolio
import backtester_engine
from logger.std_logger import init_std_logger
from logger import Logger
from strategies.strategies import generate_inputs, get_stategy_by_name
init_std_logger()

log = Logger("Initialize App", "green")
#log.debug('debug message')
#log.info('info message')
#log.warning('warn message')
#log.error('error message')
#log.critical('critical message')


app = FastAPI()

origins = [
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    html_content = f'''
    <html>
        <head>
            <title>BackTestiPy Backend</title >
        </head>
        <body>
            <h1> BackTestiPy Backend </h1>
            <a href = {str(request.url)+"docs"}> <h2> API Documentation in Swagger </h2> </a>
            <a href = {str(request.url)+"redoc"}> <h2> API Documentation in Redoc </h2> </a>
         </body>
     </html>
     '''
    return HTMLResponse(content=html_content, status_code=200)

    # return HTMLResponse(content=html_content, status_code=200)


@app.post("/backtest_strategy")
def backtest_strategy(backtest_strategy_data: backtest_strategy_model):

    # INFO - Download Data
    financial_data = download_financial_data(
        backtest_strategy_data.input_data.financial_instrument_name,
        backtest_strategy_data.start_date,
        backtest_strategy_data.end_date,
        backtest_strategy_data.input_data.timeframe,
        "yahoo"  # backtest_strategy_data.input_data.provider
    )

    # INFO - Get Stategy
    strategy_class = get_stategy_by_name(backtest_strategy_data.strategy_name)

    # INFO - Select Strategy
    strategy = strategy_class(
        backtest_strategy_data.indicators_parameters)

    # INFO - Create Portfolio
    # global portfolio
    portfolio = Portfolio(
        initial_value=backtest_strategy_data.initial_portfolio_value,
        starting_date=backtest_strategy_data.start_date,
        # starting_date=financial_data.iloc[strategy.amount_of_data_for_strategy_from_today(
        # )-1, :]["Date"],
        strategy=strategy
    )

    # INFO - Backtest
    portfolio, backtest_info = backtester_engine.backtest_strategy(
        portfolio,
        strategy,
        financial_data
    )

    log.debug("Portfolio Value")
    log.debug(portfolio.value_history)
    log.debug("Portfolio Orders")
    log.debug(portfolio.orders)


@app.get("/get_strategies")
def get_strategies():
    return generate_inputs(False)
