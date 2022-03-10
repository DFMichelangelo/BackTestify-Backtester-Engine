from pydantic import BaseModel
#from typing import Optional


class Input_data_model(BaseModel):
    timeframe: str
    financial_instrument_name: str
    #provider: str


class Backtest_strategy_model(BaseModel):
    start_date: str
    end_date: str
    strategy_name: str
    input_data: Input_data_model
    initial_portfolio_value: float
    indicators_parameters: dict
    risk_free_rate: float
    benchmark_financial_instrument_name: str
