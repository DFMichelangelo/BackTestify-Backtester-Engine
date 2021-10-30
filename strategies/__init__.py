from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def check_for_signals(self, data):
        pass

    def amount_of_data_for_strategy_from_today(self):
        def return_amount_of_data_for_indicator(indicator):
            return indicator.amount_of_data_from_today()
        return max(map(return_amount_of_data_for_indicator, self.indicators))
