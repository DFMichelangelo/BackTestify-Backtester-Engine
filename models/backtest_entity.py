from pydantic import BaseModel
from models import Backtest_strategy_model


class Drawdown_model(BaseModel):
    values: list[float]
    max_drawdown: float
    max_duration: int
    duration_of_max_drawdown: int
    drawdown_of_max_duration: float
    info: dict


class Underwater_model(BaseModel):
    values: list[float]
    max_underwater: float
    max_duration: int
    underwater_of_max_duration: float
    duration_of_max_underwater: int
    info: dict


class Portfolio_model(BaseModel):
    absolute_return_over_period: float
    absolute_return_annualized: float
    percentage_return_over_period: float
    percentage_return_annualized: float
    volatility_over_period: float
    volatility_annualized: float
    drawdown: Drawdown_model
    underwater: Underwater_model


class ACF_PACF_function_model(BaseModel):
    values: list[float]
    confidence_intervals: list[list[float]]


class Benchmark_model(BaseModel):
    returns: list
    returns_mean: float
    returns_std: float
    prices_distribution: list[dict]
    returns_distribution: list[dict]
    absolute_return_over_period: float
    absolute_return_annualized: float
    percentage_return_over_period: float
    percentage_return_annualized: float
    volatility_over_period: float
    volatility_annualized: float
    autocorrelation_function: ACF_PACF_function_model
    partial_autocorrelation_function: ACF_PACF_function_model


class Underlying_model(BaseModel):
    percentage_return_over_period: float
    percentage_return_annualized: float
    volatility_over_period: float
    volatility_annualized: float


class Performance_model(BaseModel):
    sharpe_ratio_annualized: float
    sortino_ratio_annualized: float
    calmar_ratio_annualized: float


class Order_general_model(BaseModel):
    amount: int


class Order_long_short_model(BaseModel):
    amount: int
    percentage: float
    amount_profitable: int
    percentage_profitable: float


class Orders_model(BaseModel):
    general: Order_general_model
    long_orders: Order_long_short_model
    short_orders: Order_long_short_model


class Analytics_model(BaseModel):
    portfolio: Portfolio_model
    benchmark: Benchmark_model
    underlying: Underlying_model
    orders: Orders_model
    performance: Performance_model


class Raw_data_model(BaseModel):
    portfolio_value_history: list[dict]
    orders: list[dict]
    dates: list[float]
    underlying: list[float]
    benchmark: list[float]


class Backtest_result_model(BaseModel):
    analytics: Analytics_model
    raw_data: Raw_data_model
    amount_of_data_for_strategy_from_today: int


class Backtest_save_model(BaseModel):
    input: Backtest_strategy_model
    result: Backtest_result_model
