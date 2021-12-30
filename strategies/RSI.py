from . import Strategy
from indicators.RSI import RSI
from auxiliaries.enumerations import Position


class RSI_strategy(Strategy):
    def __init__(self, indicators_parameters):
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
