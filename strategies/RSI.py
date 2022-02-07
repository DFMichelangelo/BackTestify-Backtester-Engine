from . import Strategy
from indicators.RSI import RSI
from auxiliaries.enumerations import Position


class RSI_strategy(Strategy):
    name = "RSI Strategy"
    indicators_parameters_config = [
        {
            "name": "periods",
            "default_value": 5
        },
        {
            "name": "overbought_level",
            "default_value": 0.7
        }, {
            "name": "oversold_level",
            "default_value": 0.3
        }]

    def __init__(self, indicators_parameters):
        super().__init__(indicators_parameters)
        self.indicators = {
            "RSI": RSI(indicators_parameters)
        }

    def check_for_signals(self, data):
        rsi_value = self.indicators["RSI"].calculate(data)
        if rsi_value > self.indicators["RSI"].overbought_level:
            return Position.SHORT
        elif rsi_value < self.indicators["RSI"].oversold_level:
            return Position.LONG
        return Position.IDLE

    def amount_of_data_for_strategy_from_today(self):
        return self.indicators["RSI"].periods
