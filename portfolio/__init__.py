import pandas as pd
import numpy as np
import uuid
from auxiliaries.enumerations import Order_Status


class Portfolio:
    def __init__(self, initial_value, starting_date, strategy):
        self.value_history = pd.DataFrame(
            data={"date": [starting_date], "value": [initial_value]})
        self.strategy = strategy
        self.orders = pd.DataFrame(data={
            "ID": [],
            #               "financial_instrument_name": [],
            #               "financial_instrument_type": [],
            "creation_date": [],
            "creation_price": [],
            "order_type": [],
            "status": [],
            "open_price": [],
            "open_date": [],
            "close_price": [],
            "close_date": [],
            "take_profit_price": [],
            "stop_loss_price": [],
            "size": [],
            # "commission":[],
            # "open_order_commission":[],
            # "closed_order_commission":[],
            # "other_order_commission":[],
            # "PnL":[],
            # "value":[],
            # trail_stop_loss_amount:[],
            # trail_stop_loss_percentage:[],
            # trail_take_profit_amount:[],
            # trail_take_profit_percentage:[],

        })

    def value(self):
        return self.value_history["value"].iloc[-1]

    def close_all_orders(self, today_price, today_date):
        print("TO BE DONE")
        pass

    def add_order(self, creation_price, creation_date, order_type):
        order = self.create_order(creation_price, creation_date, order_type)
        self.orders = self.orders.append(order, ignore_index=True)

    def close_order(self, order_index, price, date):
        print("TO BE DONE")
        pass

    def check_for_open_orders(self, order_type):
        print("TO BE DONE check_for_open_orders")
        return None

    def create_order(self, creation_price, creation_date, order_type):
        order = {
            "ID": uuid.uuid4(),
            "creation_date": creation_date,
            "creation_price": creation_price,
            "status": Order_Status.SUBMITTED,
            "order_type": order_type,
            "open_price": None,
            "open_date": None,
            "close_price": None,
            "close_date": None,
            "take_profit_price": creation_price*1.02,
            "stop_loss_price": creation_price*0.98,
            "size": 1,
        }
        portfolio_new_value_history = {
            "date": creation_date,
            "value": self.value()-creation_price
        }
        self.value_history = self.value_history.append(
            portfolio_new_value_history, ignore_index=True)
        return order
