from repositories.base import Base_repository


class Backtest_repository(Base_repository):
    def __init__(self):
        super().__init__("backtests")
