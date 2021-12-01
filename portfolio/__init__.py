import pandas as pd
import uuid
from auxiliaries.enumerations import Order_Status, Position


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
            "position": [],
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
            "pnl": [],
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

    def add_order(self, order):
        #self.orders = self.orders.append(order, ignore_index=True)
        self.orders.loc[len(self.orders)+1] = order

    def close_order(self, open_order, price, date):
        order = self.orders[self.orders["ID"] == open_order["ID"]]
        order["status"] = Order_Status.CLOSED
        order["close_date"] = date
        order["close_price"] = price
        if order["position"] == Position.LONG:
            order["pnl"] = order["size"] * (price-order["open_price"])
        elif order["position"] == Position.SHORT:
            order["pnl"] = order["size"] * ((order["open_price"]-price))
        self.orders[self.orders["ID"] == open_order["ID"]] = order

        porfolio_value_before_order_close = self.value()
        portfolio_value = porfolio_value_before_order_close+order["pnl"]
        self.value_history.append(
            {
                "date": date,
                "value": portfolio_value
            })

    def check_for_orders_to_close(self, today_price, today_date):
        print("TO BE DONE")
        pass

    def check_for_open_orders(self, position):
        return self.orders[self.orders["position"] == position]

    def create_order(self, creation_price, creation_date, position):
        tp_perc = 1.02 if position == Position.LONG else 0.98
        sl_perc = 0.98 if position == Position.LONG else 1.02

        order = {
            "ID": uuid.uuid4(),
            "creation_date": creation_date,
            "creation_price": creation_price,
            "status": Order_Status.SUBMITTED,
            "position": position,
            # "order_type": order_type,
            "open_price": None,
            "open_date": None,
            "close_price": None,
            "close_date": None,
            "take_profit_price": creation_price*tp_perc,
            "stop_loss_price": creation_price*sl_perc,
            "size": 1,
        }
        portfolio_new_value_history = {
            "date": creation_date,
            "value": self.value()-creation_price
        }

        self.add_order(order)
        self.value_history.loc[len(
            self.value_history)+1] = portfolio_new_value_history
        # self.value_history = self.value_history.append(
        #    portfolio_new_value_history, ignore_index=True)

        return order
