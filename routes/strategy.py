from fastapi import APIRouter
from models import Backtest_strategy_model
from data_downloader import download_financial_data
from portfolio import Portfolio
import backtester_engine
from strategies.strategies import generate_inputs, get_stategy_by_name
from analytics import absolute_return_annualized, autocorrelation_function, partial_autocorrelation_function, absolute_return_over_period, percentage_return_over_period, volatility_over_period, absolute_return_annualized, percentage_return_annualized, volatility_annualized
from analytics.orders import orders_amount_for_types
from analytics.performance import sharpe_ratio_annualized, sortino_ratio_annualized, calmar_ratio_annualized, correlation_with_benchmark, kestner_ratio, beta
from analytics.loss_indicators import drawdown_indicator, underwater_indicator
from auxiliaries.enumerations import get_position_restriction
from logger import Logger
import time
import numpy as np

router = APIRouter()

timer_logger = Logger("Timer", "#C97C5D")


@router.post("/backtest_strategy")
def backtest_strategy(backtest_strategy_data: Backtest_strategy_model):
    # INFO - Download Data
    t0 = time.perf_counter()
    underlying_timeseries = download_financial_data(
        backtest_strategy_data.financial_instrument_name,
        backtest_strategy_data.start_date,
        backtest_strategy_data.end_date,
        backtest_strategy_data.timeframe,
        "yahoo"  # backtest_strategy_data.input_data.provider
    )

    benchmark_timeseries = download_financial_data(
        backtest_strategy_data.benchmark_financial_instrument_name,
        backtest_strategy_data.start_date,
        backtest_strategy_data.end_date,
        backtest_strategy_data.timeframe,
        "yahoo"  # backtest_strategy_data.input_data.provider
    )
    t1 = time.perf_counter()
    timer_logger.info(f"Downloaded data in {t1-t0} seconds")
    # INFO - Get Stategy
    strategy_class = get_stategy_by_name(
        backtest_strategy_data.strategy_name)

    # INFO - Select Strategy
    strategy = strategy_class(
        backtest_strategy_data.indicators_parameters)

    options = {
        "portfolio": backtest_strategy_data.portfolio.dict(),
        "stop_loss_and_take_profit": backtest_strategy_data.stop_loss_and_take_profit.dict(),
        "open_new_order_on_contrarian_signal": backtest_strategy_data.open_new_order_on_contrarian_signal,
        "orders_positions_limitations": get_position_restriction(backtest_strategy_data.orders_positions_limitations),
    }
    # INFO - Create Portfolio
    # global portfolio
    portfolio = Portfolio(
        initial_value=backtest_strategy_data.portfolio.initial_portfolio_value,
        starting_date=underlying_timeseries["Date"][strategy.amount_of_data_for_strategy_from_today(
        )],
        # starting_date=financial_data.iloc[strategy.amount_of_data_for_strategy_from_today(
        # )-1, :]["Date"],
        strategy=strategy,
        options=options
    )

    t0 = time.perf_counter()
    # INFO - Backtest
    portfolio, backtest_info = backtester_engine.backtest_strategy(
        portfolio,
        underlying_timeseries
    )

    t1 = time.perf_counter()
    timer_logger.info(f"Backtested in {t1-t0} seconds")
    t0 = time.perf_counter()
    prices_distribution = np.histogram(
        benchmark_timeseries["Adj Close"].to_list(), bins=50)

    returns_distribution = np.histogram(
        benchmark_timeseries["Adj Close"].pct_change().dropna().to_list(), bins=50)

    prices_distribution_dict = [{"amount": int(amount), "bin_edge": float(bin_edges)}
                                for amount, bin_edges in zip(prices_distribution[0], prices_distribution[1])]

    returns_distribution_dict = [{"amount": int(amount), "bin_edge": float(bin_edges)}
                                 for amount, bin_edges in zip(returns_distribution[0], returns_distribution[1])]

    drawdown = drawdown_indicator(
        portfolio.value_history["total_portfolio_value"])

    percentage_return_ann = percentage_return_annualized(
        portfolio.value_history["liquidity"])
    payload = {
        "analytics": {
            "portfolio": {
                "absolute_return_over_period": absolute_return_over_period(portfolio.value_history["liquidity"]),
                "absolute_return_annualized": absolute_return_annualized(portfolio.value_history["liquidity"]),
                "percentage_return_over_period": percentage_return_over_period(portfolio.value_history["liquidity"]),
                "percentage_return_annualized": percentage_return_ann,
                "volatility_over_period": volatility_over_period(portfolio.value_history["total_portfolio_value"]),
                "volatility_annualized": volatility_annualized(portfolio.value_history["total_portfolio_value"]),
                "drawdown": drawdown,
                "underwater": underwater_indicator(portfolio.value_history["total_portfolio_value"]),
                "initial_value": portfolio.initial_value,
            },
            "benchmark": {
                "returns": benchmark_timeseries["Adj Close"].pct_change().fillna("").to_list(),
                "returns_mean": benchmark_timeseries["Adj Close"].pct_change().dropna().mean(),
                "returns_std": benchmark_timeseries["Adj Close"].pct_change().dropna().std(),
                "prices_distribution": prices_distribution_dict,
                "returns_distribution": returns_distribution_dict,
                "absolute_return_over_period": absolute_return_over_period(benchmark_timeseries["Adj Close"]),
                "absolute_return_annualized": absolute_return_annualized(benchmark_timeseries["Adj Close"]),
                "percentage_return_over_period": percentage_return_over_period(benchmark_timeseries["Adj Close"]),
                "percentage_return_annualized": percentage_return_annualized(benchmark_timeseries["Adj Close"]),
                "volatility_over_period": volatility_over_period(benchmark_timeseries["Adj Close"]),
                "volatility_annualized": volatility_annualized(benchmark_timeseries["Adj Close"]),
                "autocorrelation_function": autocorrelation_function(benchmark_timeseries["Adj Close"]),
                "partial_autocorrelation_function": partial_autocorrelation_function(benchmark_timeseries["Adj Close"]),

            },
            "underlying": {
                "percentage_return_over_period": percentage_return_over_period(underlying_timeseries["Adj Close"]),
                "percentage_return_annualized": percentage_return_annualized(underlying_timeseries["Adj Close"]),
                "volatility_over_period": volatility_over_period(underlying_timeseries["Adj Close"]),
                "volatility_annualized": volatility_annualized(underlying_timeseries["Adj Close"]),

            },
            "orders": orders_amount_for_types(portfolio.orders),
            "performance": {
                "sharpe_ratio_annualized": sharpe_ratio_annualized(portfolio.value_history["total_portfolio_value"], backtest_strategy_data.risk_free_rate),
                "sortino_ratio_annualized": sortino_ratio_annualized(portfolio.value_history["total_portfolio_value"], backtest_strategy_data.risk_free_rate),
                "calmar_ratio_annualized": calmar_ratio_annualized(percentage_return_ann, drawdown["max_drawdown"]),
                "correlation_with_benchmark": correlation_with_benchmark(portfolio.value_history["total_portfolio_value"], benchmark_timeseries["Adj Close"]),
                "kestner_ratio": kestner_ratio(portfolio.value_history["total_portfolio_value"]),
                "beta": beta(portfolio.value_history["total_portfolio_value"], benchmark_timeseries["Adj Close"]),
            }
        },
        "raw_data": {
            "portfolio_value_history": portfolio.value_history.to_dict('records'),
            "orders": portfolio.orders.to_dict('records'),
            "dates": underlying_timeseries["Date"].to_list(),
            "underlying": underlying_timeseries["Adj Close"].to_list(),
            "benchmark": benchmark_timeseries["Adj Close"].to_list(),
        },
        "amount_of_data_for_strategy_from_today": strategy.amount_of_data_for_strategy_from_today(),
    }

    t1 = time.perf_counter()
    timer_logger.info(f"Created Payload in {t1-t0} seconds")
    return payload


@router.get("/get_strategies")
def get_strategies():
    return generate_inputs(False)


@router.post("/create_strategy")
def create_strategy():
    pass
