
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import backtest_strategy_model
from fastapi import FastAPI, status, Request
from data_downloader import download_financial_data
from strategies.RSI import RSI_strategy
from portfolio import Portfolio
import backtester_engine
from logger.std_logger import init_std_logger
from logger import Logger
from pandasgui import show
from strategies.strategies import generate_inputs, get_stategy_by_name
from analytics.portfolio import absolute_return_over_period, percentage_return_over_period, portfolio_volatility_over_period
from analytics.orders import orders_amount_for_types
init_std_logger()

log = Logger("Initialize App", "green")
logExceptions = Logger("Exceptions", "green")
#log.debug('debug message')
#log.info('info message')
#log.warning('warn message')
#log.error('error message')
#log.critical('critical message')


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logExceptions.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

origins = [
    "https://localhost:3000"
    "https://backtestify.netlify.app"
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
    #show(portfolio.value_history, portfolio.orders)
    #log.debug("Portfolio Orders")
    # log.debug(portfolio.orders)

    return {
        # "analytics": {
        #    "portfolio:": {
        #        "absolute_return_over_period": absolute_return_over_period(portfolio),
        #        "percentage_return_over_period": percentage_return_over_period(portfolio),
        #        "portfolio_volatility_over_period": portfolio_volatility_over_period(portfolio),
        #    },
        #    "orders": orders_amount_for_types(portfolio.orders)
        # },
        "raw_data": {
            "portfolio_value_history": portfolio.value_history.to_dict('records'),
            "orders": portfolio.orders.to_dict('records')
        }
    }


@app.get("/get_strategies")
def get_strategies():
    return generate_inputs(False)
