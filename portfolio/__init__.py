import pandas as pd
import numpy as np
import uuid


class Portfolio:
    def __init__(self, initial_value, starting_date, strategy):
        self.value_history = pd.DataFrame(
            data={"date": [starting_date], "value": [initial_value], "change": [np.nan]})
        self.strategy = strategy
        self.orders = pd.DataFrame(data={
            "ID": [],
            #               "financial_instrument_name": [],
            #               "financial_instrument_type": [],
            "creation_date": [],
            "creation_price": [],
            "status": [],
            "order_type": [],
            "open_price": [],
            "open_date": [],
            "close_price": [],
            "close_date": [],
            "position": []
        })

    def value(self):
        return self.value_history["value"].iloc[-1]

    def close_all_orders(self, today_price, today_date):
        print("TO BE DONE")
        pass

    def add_order(self, order):
        print(order)
#        order = {
#            "ID": uuid.uuid4(),
#            "creation_date":
# creation_price
# creation_date
# position
#        }
#        self.orders.append()
        print("TO BE DONE")
        pass

    def close_order(self, order_index, price, date):
        print("TO BE DONE")
        pass

    def check_for_orders_to_close(self, price, date):
        print("TO BE DONE")
        pass

    def check_for_open_orders(self, order_type):
        print("TO BE DONE check_for_open_orders")
        return None

    def create_order(self, open_price, open_date, position):
        print("TO BE DONE")
        pass
