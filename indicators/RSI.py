import numpy as np
from . import Indicator


class RSI(Indicator):
    def __init__(self, periods, oversold_level, overbought_level):
        self.periods = periods
        self.oversold_level = oversold_level
        self.overbought_level = overbought_level

    def calculate(self, financial_data):
        returns = financial_data["Close"].pct_change().dropna()
        up_returns = 0 if sum(returns >= 0) == 0 else returns[returns >= 0]
        down_returns = 0 if sum(returns < 0) == 0 else returns[returns < 0]
        avg_up = np.mean(up_returns)
        avg_down = np.mean(abs(down_returns))
        RSI = 100-100/(1+(avg_up/avg_down))
        return RSI

    def amount_of_data_from_today(self):
        return self.periods
