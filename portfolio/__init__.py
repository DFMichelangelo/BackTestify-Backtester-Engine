import pandas as pd
import uuid
from auxiliaries.dates_converters import convert_from_DDMMYYYY_date_string_to_DDMMYYYYhhmmss_datetime
from auxiliaries.enumerations import Order_Status, Position
from logger import Logger

log = Logger("Backtester Engine", "purple")


class Portfolio:
    def __init__(self, initial_value, starting_date, strategy):
        self.value_history = pd.DataFrame(
            data={
                "date": [starting_date],
                "liquidity": [initial_value],
                "assets_value": [0]
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
            "take_profit_price": [],
            "stop_loss_price": [],
            "close_price": [],
            "close_date": [],

            # "financial_instrument_name": [],
            # "financial_instrument_type": [],
            # "commission":[],
            # "open_order_commission":[],
            # "closed_order_commission":[],
            # "other_order_commission":[],
            # "value":[],
            # trail_stop_loss_amount:[],
            # trail_stop_loss_percentage:[],
            # trail_take_profit_amount:[],
            # trail_take_profit_percentage:[],

        })

    def liquidity(self):
        # INFO - get the current liquidity of the portfolio from value_history
        return self.value_history.iloc[-1]["liquidity"]

    def assets_value(self):
        # INFO - get the current assets_value of the portfolio from value_history
        return self.value_history.iloc[-1]["assets_value"]

    def update_orders_value(self, today_price):
        open_orders_filter = self.orders["status"] == Order_Status.OPEN

        self.orders.loc[open_orders_filter, "value"] = today_price

        ''' PNL
        # INFO - get open orders (Short and Long) and calculate their P&L using the today_price and their opening price
        open_orders_filter = self.orders["status"] == Order_Status.OPEN
        long_orders_filter = self.orders["position"] == Position.LONG
        short_orders_filter = self.orders["position"] == Position.SHORT

        # INFO - Long & Open Positions - Long Valuation: S_t-S_0
        self.orders.loc[open_orders_filter & long_orders_filter, "value"] = today_price - \
            self.orders.loc[open_orders_filter &
                            long_orders_filter, "open_price"]

        # INFO - Short & Open Positions - Short Valuation: S_0-S_t
        self.orders.loc[open_orders_filter & short_orders_filter,
                        "value"] = self.orders.loc[open_orders_filter & short_orders_filter, "open_price"] - today_price
        '''

    def update_portfolio_assets_value(self, today_date):
        # INFO - Update the value history
        self.value_history.loc[len(self.value_history)] = {
            "date": today_date,
            "liquidity": self.liquidity(),
            "assets_value": self.orders[self.orders["status"] == Order_Status.OPEN]["value"].sum()
        }

    def create_order(self, creation_price, creation_date, position):
        tp_perc = 1.02 if position == Position.LONG else 0.98  # TODO - Provisional
        sl_perc = 0.98 if position == Position.LONG else 1.02  # TODO - Provisional

        order = {
            "ID": uuid.uuid4(),
            "creation_date": creation_date,
            "creation_price": creation_price,
            "status": Order_Status.OPEN,
            "position": position,
            # "order_type": order_type,
            "open_price": creation_price,  # TODO - Provisional
            "open_date": creation_price,
            "close_price": None,
            "close_date": None,
            "take_profit_price": creation_price*tp_perc,  # TODO - Provisional
            "stop_loss_price": creation_price*sl_perc,  # TODO - Provisional
            "value": creation_price,
            "size": 1  # TODO - Provisional
        }

        # INFO - Add the order to the orders dataframe
        self.orders.loc[len(self.orders)] = order

        # INFO - Update the value history of portfolio
        portfolio_new_value_history = {
            "date": creation_date,
            "liquidity": self.liquidity()-creation_price,
            "assets_value": self.assets_value()+order["value"]
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
            "assets_value": portfolio_assets_value
        }
        #log.debug(f"Order closed. Order ID: {open_order['ID']}")
        return open_order

    def check_for_orders_to_close(self, today_price, today_date):
        # INFO - Filters
        orders_long_filter = self.orders["position"] == Position.LONG
        orders_short_filter = self.orders["position"] == Position.SHORT
        order_open_filter = self.orders["status"] == Order_Status.OPEN
        # INFO - Select OPEN orders with LONG position where today_price>=take_profit or today_price<=stop_loss
        long_orders_to_close_in_tp = (orders_long_filter & order_open_filter & (
            self.orders["take_profit_price"] <= today_price))
        long_orders_to_close_in_sl = (orders_long_filter & order_open_filter & (
            self.orders["stop_loss_price"] >= today_price))

        short_orders_to_close_in_tp = (orders_short_filter & order_open_filter & (
            self.orders["take_profit_price"] <= today_price))
        short_orders_to_close_in_tp = (orders_short_filter & order_open_filter & (
            self.orders["stop_loss_price"] <= today_price))

        orders_to_close = self.orders[long_orders_to_close_in_tp |
                                      long_orders_to_close_in_sl | short_orders_to_close_in_tp | short_orders_to_close_in_tp]

        # INFO - for each open order long and to close, set the order closed and calculate value for each order
        for (order_index, order) in orders_to_close.iterrows():
            self.close_order(order, today_price, today_date)

    def get_open_orders(self, position):
        order_open_filter = self.orders["status"] == Order_Status.OPEN
        position_filter = self.orders["position"] == position
        return self.orders.loc[position_filter & order_open_filter]
