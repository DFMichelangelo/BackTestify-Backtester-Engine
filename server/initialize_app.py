
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
from strategies.strategies import generate_inputs, get_stategy_by_name
from analytics import absolute_return_annualized, absolute_return_over_period, percentage_return_over_period, volatility_over_period, absolute_return_annualized, percentage_return_annualized, volatility_annualized
from analytics.orders import orders_amount_for_types
import numpy as np
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
    "https://localhost:3000",
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
    underlying_timeseries = download_financial_data(
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
        underlying_timeseries
    )

    prices_distribution = np.histogram(
        underlying_timeseries["Adj Close"].to_list(), bins=50)

    returns_distribution = np.histogram(
        underlying_timeseries["Adj Close"].pct_change().dropna().to_list(), bins=50)

    prices_distribution_dict = [{"amount": int(amount), "bin_edge": float(bin_edges)}
                                for amount, bin_edges in zip(prices_distribution[0], prices_distribution[1])]

    returns_distribution_dict = [{"amount": int(amount), "bin_edge": float(bin_edges)}
                                 for amount, bin_edges in zip(returns_distribution[0], returns_distribution[1])]
    return {
        "analytics": {
            "portfolio": {
                "absolute_return_over_period": absolute_return_over_period(portfolio.value_history["liquidity"]),
                "absolute_return_annualized": absolute_return_annualized(portfolio.value_history["liquidity"]),
                "percentage_return_over_period": percentage_return_over_period(portfolio.value_history["liquidity"]),
                "percentage_return_annualized": percentage_return_annualized(portfolio.value_history["liquidity"]),
                "percentage_return_over_period": percentage_return_over_period(portfolio.value_history["liquidity"]),
                "volatility_over_period": volatility_over_period(portfolio.total_assets_series),
                "volatility_annualized": volatility_annualized(portfolio.total_assets_series),
            },
            "underlying": {
                "returns": underlying_timeseries["Adj Close"].pct_change().fillna("").to_list(),
                "returns_mean": underlying_timeseries["Adj Close"].pct_change().dropna().mean(),
                "returns_std": underlying_timeseries["Adj Close"].pct_change().dropna().std(),
                "prices_distribution": prices_distribution_dict,
                "returns_distribution": returns_distribution_dict,
                "absolute_return_over_period": absolute_return_over_period(underlying_timeseries["Adj Close"]),
                "absolute_return_annualized": absolute_return_annualized(underlying_timeseries["Adj Close"]),
                "percentage_return_over_period": percentage_return_over_period(underlying_timeseries["Adj Close"]),
                "percentage_return_annualized": percentage_return_annualized(underlying_timeseries["Adj Close"]),
                "percentage_return_over_period": percentage_return_over_period(underlying_timeseries["Adj Close"]),
                "volatility_over_period": volatility_over_period(underlying_timeseries["Adj Close"]),
                "volatility_annualized": volatility_annualized(underlying_timeseries["Adj Close"]),
            },
            "orders": orders_amount_for_types(portfolio.orders)
        },

        "raw_data": {
            "portfolio_value_history": portfolio.value_history.to_dict('records'),
            "orders": portfolio.orders.to_dict('records'),
            "dates": [str(date) for date in portfolio.value_history.date],
            "underlying": underlying_timeseries["Adj Close"].to_list(),

        }
    }


@app.get("/get_strategies")
def get_strategies():
    return generate_inputs(False)


@app.post("/create_strategy")
def create_strategy():
    pass
