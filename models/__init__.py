from pydantic import BaseModel
#from typing import Optional
from typing import Literal


class Input_data_model(BaseModel):
    timeframe: str
    financial_instrument_name: str
    #provider: str


class Portfolio_model(BaseModel):
    initial_portfolio_value: float
    order_size_type: Literal['percentage', 'absolute_value']
    order_size_amount: float


class Stop_loss_and_take_profit_model(BaseModel):
    take_profit_enabled: bool
    take_profit_type: Literal['percentage', 'absolute_value']
    take_profit_amount: float
    stop_loss_enabled: bool
    stop_loss_type: Literal['percentage', 'absolute_value']
    stop_loss_amount: float


class Backtest_strategy_model(BaseModel):
    start_date: str
    end_date: str
    strategy_name: str
    input_data: Input_data_model
    portfolio: Portfolio_model
    stop_loss_and_take_profit: Stop_loss_and_take_profit_model
    orders_positions_limitations: Literal["no_limitations",
                                          "long_only", "short_only"]
    open_new_order_on_contrarian_signal: bool
    indicators_parameters: dict
    risk_free_rate: float
    benchmark_financial_instrument_name: str
