import pandas as pd
import numpy as np


class Portfolio:
    def __init__(self, initial_value, startingDate, strategy):
        self.value_history = pd.DataFrame(
            data={"date": [startingDate], "value": [initial_value], "change": [np.nan]})
        self.strategy = strategy
        self.orders = pd.DataFrame(data={
            "ID": [],
            "creation_date": [],
            "status": [],
            "order_type": [],
            "open_price": [],
            "open_date": [],
            "close_price": [],
            "close_date": [],
            "position": []}
        )

    def value(self):
        return self.value_history["value"].iloc[-1]

    def close_all_orders(self, todayPrice, todayDate):
        print("TO BE DONE")
        pass

        def add_order(self, order):
            print(order)
            print("TO BE DONE")
            pass

    def close_order(self, orderIndex, price, date):
        print("TO BE DONE")
        pass

    def check_for_orders_to_close(self, price, date):
        print("TO BE DONE")
        pass

    def check_for_open_orders(self, orderType):
        print("TO BE DONE check_for_open_orders")
        return None

    def create_order(self, open_price, open_date, position):
        print("TO BE DONE")
        pass
