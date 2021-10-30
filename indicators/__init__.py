from abc import ABC, abstractmethod


class Indicator(ABC):

    @abstractmethod
    def __init__(self, data):
        pass

    @abstractmethod
    def calculate(self, *args):
        pass

    @abstractmethod
    def amount_of_data_from_today(self):
        pass
