from . import Strategy
from auxiliaries.enumerations import Position
import talib as ta


class MA_crossover_strategy(Strategy):
    name = "MA Crossover Strategy"
    indicators_parameters_config = [
        {
            "name": "fast_SMA_periods",
            "default_value": 5
        },
        {
            "name": "slow_SMA_periods",
            "default_value": 15
        }
    ]

    def __init__(self, indicators_parameters):
        super().__init__(indicators_parameters)

    def check_for_signals(self, data):
        fast_SMA_value = ta.SMA(
            data["Adj Close"], self.indicators_parameters["fast_SMA_periods"]).iloc[-1]
        slowSMA_value = ta.SMA(
            data["Adj Close"], self.indicators_parameters["slow_SMA_periods"]).iloc[-1]

        if fast_SMA_value < slowSMA_value:
            return Position.SHORT
        elif fast_SMA_value > slowSMA_value:
            return Position.LONG
        return Position.IDLE

    def amount_of_data_for_strategy_from_today(self):
        return max(self.indicators_parameters["fast_SMA_periods"], self.indicators_parameters["slow_SMA_periods"])
