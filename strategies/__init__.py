from abc import ABC, abstractmethod


class Strategy(ABC):

    def __init__(self, indicators_parameters):
        self.indicators_parameters = indicators_parameters

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def indicators_parameters_config(self):
        pass

    @abstractmethod
    def check_for_signals(self, data):
        pass

    def amount_of_data_for_strategy_from_today(self):
        def return_amount_of_data_for_indicator(indicator):
            return indicator.amount_of_data_from_today()
        return max(map(return_amount_of_data_for_indicator, self.indicators))
