from pydantic import BaseModel
#from typing import Optional
from typing import Literal


class Input_data_model(BaseModel):
    timeframe: str
    financial_instrument_name: str
    #provider: str


class Portfolio_model(BaseModel):
    initial_portfolio_value: float
    order_size_type: Literal['percentage', 'absoluteValue']
    order_size_amount: float


class Stop_loss_and_take_profit_model(BaseModel):
    take_profit_enabled: bool
    take_profit_type: Literal['percentage', 'absoluteValue']
    take_profit_amount: float
    stopLossEnabled: bool
    stopLossType: Literal['percentage', 'absoluteValue']
    stopLossAmount: float


class Backtest_strategy_model(BaseModel):
    start_date: str
    end_date: str
    strategy_name: str
    input_data: Input_data_model
    portfolio: Portfolio_model
    stop_loss_and_take_profit: Stop_loss_and_take_profit_model
    indicators_parameters: dict
    risk_free_rate: float
    benchmark_financial_instrument_name: str
