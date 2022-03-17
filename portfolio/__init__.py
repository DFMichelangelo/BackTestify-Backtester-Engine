import pandas as pd
import uuid
from auxiliaries.enumerations import Order_Status, Order_Type, Position
from logger import Logger
from abc import ABC
import time

log = Logger("Backtester Engine", "purple")

timer_logger = Logger("Timer", "#C89F9C")


class Portfolio(ABC):
    def __init__(self, initial_value, starting_date, strategy, options):
        self.options = options
        self.initial_value = initial_value
        self.value_history = pd.DataFrame(
            data={
                "date": [starting_date],
                "liquidity": [initial_value],
                "assets_value": [0],
                "total_portfolio_value": [initial_value]
            })
        self.strategy = strategy
        self.orders = pd.DataFrame(data={
            "ID": [],
            "creation_date": [],
            "creation_price": [],
            "position": [],
            "status": [],
            "size": [],
            "value": [],
            "open_price": [],
            "open_date": [],
            "order_type": [],
            "take_profit_price": [],
            "stop_loss_price": [],
            "close_price": [],
            "close_date": [],
            "PnL": []
            # "financial_instrument_name": [],
            # "financial_instrument_type": [],
            # "commission":[],
            # "open_order_commission":[],
            # "closed_order_commission":[],
            # "other_order_commission":[],
            # trail_stop_loss_amount:[],
            # trail_stop_loss_percentage:[],
            # trail_take_profit_amount:[],
            # trail_take_profit_percentage:[],

        })

    # INFO - get the current liquidity of the portfolio from value_history
    def liquidity(self):
        return self.value_history.iloc[-1]["liquidity"]

    def total_portfolio_value(self):
        return self.value_history.iloc[-1]["total_portfolio_value"]
    # INFO - get the current assets_value of the portfolio from value_history

    def assets_value(self):
        return self.value_history.iloc[-1]["assets_value"]

    def update_orders_value(self, today_price):
        open_orders_filter = self.orders["status"] == Order_Status.OPEN

        self.orders.loc[open_orders_filter, "value"] = today_price * \
            self.orders.loc[open_orders_filter, "size"]

        # INFO - Calculate PnL for each order
        # INFO - get open orders (Short and Long) and calculate their P&L using the today_price and their opening price
        long_orders_filter = self.orders["position"] == Position.LONG
        short_orders_filter = self.orders["position"] == Position.SHORT

        # INFO - Long & Open Positions - Long Valuation: (S_t-S_0)*Size
        self.orders.loc[open_orders_filter & long_orders_filter, "PnL"] = (today_price -
                                                                           self.orders.loc[open_orders_filter &
                                                                                           long_orders_filter, "open_price"])*self.orders.loc[open_orders_filter &
                                                                                                                                              long_orders_filter, "size"]
        # INFO - Short & Open Positions - Short Valuation: (S_0-S_t)*size
        self.orders.loc[open_orders_filter & short_orders_filter, "PnL"] = (
            self.orders.loc[open_orders_filter & short_orders_filter, "open_price"] - today_price)*self.orders.loc[open_orders_filter & short_orders_filter, "size"]

    def update_portfolio_assets_value(self, today_date):
        # INFO - Update the value history
        assets_value = self.orders[self.orders["status"]
                                   == Order_Status.OPEN]["value"].sum()
        self.value_history.loc[len(self.value_history)] = {
            "date": today_date,
            "liquidity": self.liquidity(),
            "assets_value": assets_value,
            "total_portfolio_value": self.liquidity() + assets_value
        }

    def create_order(self, creation_price, creation_date, position):
        # INFO - Set Take Profit and Stop Loss
        take_profit_price = None

        if self.options["stop_loss_and_take_profit"]["take_profit_enabled"]:
            tp_amount = self.options["stop_loss_and_take_profit"]["take_profit_amount"]
            if self.options["stop_loss_and_take_profit"]["take_profit_type"] == "percentage":
                tp_perc = 1 + tp_amount if position == Position.LONG else 1 - tp_amount
                take_profit_price = creation_price*tp_perc
            else:
                take_profit_price = creation_price + \
                    tp_amount if position == Position.LONG else creation_price - tp_amount

        stop_loss_price = None

        if self.options["stop_loss_and_take_profit"]["stop_loss_enabled"]:
            sl_amount = - \
                self.options["stop_loss_and_take_profit"]["stop_loss_amount"]
            if self.options["stop_loss_and_take_profit"]["stop_loss_type"] == "percentage":
                sl_perc = 1 - sl_amount if position == Position.LONG else 1 + sl_amount
                stop_loss_price = creation_price*sl_perc
            else:
                stop_loss_price = creation_price - \
                    sl_amount if position == Position.LONG else creation_price + sl_amount

        # INFO - Set Order Size
        size = None
        final_order_price = None
        order_size_type = self.options["portfolio"]["order_size_type"]
        order_size_amount = self.options["portfolio"]["order_size_amount"]
        if order_size_type == "absolute_value":
            size = order_size_amount/creation_price
            final_order_price = order_size_amount
        elif order_size_type == "percentage":
            final_order_price = self.total_portfolio_value(
            )*order_size_amount
            size = final_order_price/creation_price

        if self.liquidity() < final_order_price:
            log.error("Not enough liquidity to create order")
            return None

        order = {
            "ID": uuid.uuid4(),
            "creation_date": creation_date,
            "creation_price": creation_price,
            "status": Order_Status.OPEN,
            "position": position,
            "order_type": Order_Type.MARKET_ORDER,      # TODO - Provisional
            "open_price": creation_price,               # TODO - Provisional
            "open_date": creation_date,                 # TODO - Provisional
            "close_price": None,
            "close_date": None,
            "take_profit_price": take_profit_price,
            "stop_loss_price": stop_loss_price,
            "value": final_order_price,
            "size": size,
            "PnL": 0
        }

        # INFO - Add the order to the orders dataframe
        self.orders.loc[len(self.orders)] = order

        # INFO - Update the value history of portfolio
        portfolio_new_value_history = {
            "date": creation_date,
            "liquidity": self.liquidity()-order["value"],
            "assets_value": self.assets_value()+order["value"],
            "total_portfolio_value": self.liquidity()+self.assets_value()
        }

        self.value_history.loc[len(
            self.value_history)-1] = portfolio_new_value_history

        return order

    def close_all_orders(self, today_price, today_date):
        # INFO - select OPEN orders
        orders_open = self.orders[self.orders["status"] == Order_Status.OPEN]

        # INFO - for each open order, close it
        for (order_index, order) in orders_open.iterrows():
            self.close_order(order, today_price, today_date)

    def close_order(self, open_order, price, date):
        open_order["status"] = Order_Status.CLOSED
        open_order["close_date"] = date
        open_order["close_price"] = price

        self.orders.iloc[self.orders["ID"] == open_order["ID"]] = open_order

        portfolio_liquidity = self.liquidity()+open_order["value"]
        portfolio_assets_value = self.assets_value()-open_order["value"]
        self.value_history.loc[len(self.value_history)-1] = {
            "date": date,
            "liquidity": portfolio_liquidity,
            "assets_value": portfolio_assets_value,
            "total_portfolio_value": portfolio_liquidity+portfolio_assets_value
        }
        # log.debug(f"Order closed. Order ID: {open_order['ID']}")
        return open_order

    def check_for_orders_to_close(self, today_price, today_date):
        # INFO - Filters
        orders_long_filter = self.orders["position"] == Position.LONG
        orders_short_filter = self.orders["position"] == Position.SHORT
        order_open_filter = self.orders["status"] == Order_Status.OPEN
        # INFO - Select OPEN orders with LONG position where today_price>=take_profit or today_price<=stop_loss
        long_orders_to_close_in_tp = (orders_long_filter & order_open_filter & (
            today_price >= self.orders["take_profit_price"]))
        long_orders_to_close_in_sl = (orders_long_filter & order_open_filter & (
            today_price <= self.orders["stop_loss_price"]))

        # INFO - Select OPEN orders with SHORT position where today_price<=take_profit or today_price>=stop_loss
        short_orders_to_close_in_tp = (orders_short_filter & order_open_filter & (
            today_price <= self.orders["take_profit_price"]))
        short_orders_to_close_in_tp = (orders_short_filter & order_open_filter & (
            today_price >= self.orders["stop_loss_price"]))

        orders_to_close = self.orders[long_orders_to_close_in_tp |
                                      long_orders_to_close_in_sl | short_orders_to_close_in_tp | short_orders_to_close_in_tp]

        # INFO - for each open order long and to close, set the order closed and calculate value for each order
        for (order_index, order) in orders_to_close.iterrows():
            self.close_order(order, today_price, today_date)

    def get_open_orders_of_certain_position(self, position):
        order_open_filter = self.orders["status"] == Order_Status.OPEN
        position_filter = self.orders["position"] == position
        return self.orders.loc[position_filter & order_open_filter]
