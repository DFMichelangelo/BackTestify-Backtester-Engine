import pandas as pd
import uuid
from auxiliaries.dates_converters import convert_from_DDMMYYYY_date_string_to_DDMMYYYYhhmm_datetime
from auxiliaries.enumerations import Order_Status, Position
from logger import Logger
log = Logger("Backtester Engine", "purple")


class Portfolio:
    def __init__(self, initial_value, starting_date, strategy):
        starting_date_formatted = convert_from_DDMMYYYY_date_string_to_DDMMYYYYhhmm_datetime(
            starting_date)
        self.value_history = pd.DataFrame(
            data={
                "date": [starting_date_formatted],
                "liquidity": [initial_value],
                "unrealized_pnl": [0]
            })
        self.strategy = strategy
        self.orders = pd.DataFrame(data={
            "ID": [],
            # "financial_instrument_name": [],
            # "financial_instrument_type": [],
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

    def liquidity(self):
        return self.value_history["liquidity"].iloc[-1]

    def update_orders_unrealized_pnls(self, today_price):
        pass

    def update_portfolio_unrealized_pnls(self, today_date, today_price):
        pass

    def add_order(self, order):
        #self.orders = self.orders.append(order, ignore_index=True)
        self.orders.loc[len(self.orders)+1] = order

    def create_order(self, creation_price, creation_date, position):
        tp_perc = 1.02 if position == Position.LONG else 0.98
        sl_perc = 0.98 if position == Position.LONG else 1.02

        order = {
            "ID": uuid.uuid4(),
            "creation_date": creation_date,
            "creation_price": creation_price,
            "status": Order_Status.OPEN,
            "position": position,
            # "order_type": order_type,
            "open_price": creation_price,  # TODO - Provisional
            "open_date": None,
            "close_price": None,
            "close_date": None,
            "take_profit_price": creation_price*tp_perc,
            "stop_loss_price": creation_price*sl_perc,
            "pnl": 0,
            "size": 1
        }
        portfolio_new_value_history = {
            "date": creation_date,
            "value": self.liquidity()-creation_price
        }

        self.add_order(order)
        self.value_history.loc[len(
            self.value_history)+1] = portfolio_new_value_history
        # self.value_history = self.value_history.append(
        #    portfolio_new_value_history, ignore_index=True)

        return order

    def close_all_orders(self, today_price, today_date):
        # INFO - select OPEN orders
        orders_open = self.orders[self.orders["status"] == Order_Status.OPEN]

        # INFO - for each open order, close it
        for (order_index, order) in orders_open.iterrows():
            self.close_order(order, today_price, today_date)

    def close_order(self, open_order, price, date):
        order = self.orders[self.orders["ID"] == open_order["ID"]].iloc[0]
        order["status"] = Order_Status.CLOSED
        order["close_date"] = date
        order["close_price"] = price
        if order["position"] == Position.LONG:
            order["pnl"] = order["size"] * (price-order["open_price"])
        elif order["position"] == Position.SHORT:
            order["pnl"] = order["size"] * ((order["open_price"]-price))

        self.orders.where(self.orders["ID"] ==
                          open_order["ID"]).iloc[0] = order
        #self.orders.loc[self.orders["ID"] == open_order["ID"]] = order

        porfolio_value_before_order_close = self.liquidity()
        portfolio_value = porfolio_value_before_order_close+order["pnl"]
        self.value_history.loc[len(self.value_history)+1] = {
            "date": date,
            "value": portfolio_value
        }
        log.debug(f"Order closed. Order ID: {order['ID']}")
        return order

    def check_for_orders_to_close(self, today_price, today_date):
        # INFO - select OPEN orders with LONG position where today_price>=take_profit or today_price<=stop_loss
        long_orders_to_close_in_tp = ((self.orders["position"] == Position.LONG) & (
            self.orders["take_profit_price"] <= today_price) & (self.orders["status"] == Order_Status.OPEN))
        long_orders_to_close_in_sl = ((self.orders["position"] == Position.LONG) & (
            self.orders["stop_loss_price"] >= today_price) & (self.orders["status"] == Order_Status.OPEN))

        short_orders_to_close_in_tp = ((self.orders["position"] == Position.SHORT) & (
            self.orders["take_profit_price"] <= today_price) & (self.orders["status"] == Order_Status.OPEN))
        short_orders_to_close_in_tp = ((self.orders["position"] == Position.SHORT) & (
            self.orders["stop_loss_price"] <= today_price) & (self.orders["status"] == Order_Status.OPEN))

        orders_to_close = self.orders[long_orders_to_close_in_tp |
                                      long_orders_to_close_in_sl | short_orders_to_close_in_tp | short_orders_to_close_in_tp]

        # INFO for each open order long and to close, set the order closed and calculate pnl for each order
        for (order_index, order) in orders_to_close.iterrows():
            self.close_order(order, today_price, today_date)

    def check_for_open_orders(self, position):
        return self.orders[self.orders["position"] == position]
