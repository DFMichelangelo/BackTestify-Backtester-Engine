from auxiliaries.enumerations import Position
from logger import Logger


def is_order_of_this_type(order, position):
    return (order["position"] == position).any()


log = Logger("Backtester Engine", "purple")


def backtest_strategy(portfolio, financial_data):
    backtest_info = {}
    amount_of_data_for_strategy_from_today = portfolio.strategy.amount_of_data_for_strategy_from_today()
    amount_of_financial_data = len(financial_data.index)

    for date_index in range(amount_of_data_for_strategy_from_today, amount_of_financial_data):

        # SECTION - ALPHA
        # INFO - get data input for strategy
        data_input_for_strategy = financial_data[(
            date_index-amount_of_data_for_strategy_from_today):date_index]
        # INFO - get today price and today date
        today_price = financial_data.iloc[date_index, :]["Adj Close"]
        today_date = financial_data.iloc[date_index, :]["Date"]
        # END SECTION - ALPHA

        # log.debug(
        #    f"[NEW DAY] Date Index: {date_index} | Date: {today_date} | Price: {today_price} ")

        # SECTION - BETA
        portfolio.update_orders_value(today_price)
        # END SECTION - BETA

        # SECTION - GAMMA
        portfolio.update_portfolio_assets_value(today_date)
        # END SECTION - GAMMA

        # SECTION - DELTA
        # INFO - Check if you can close orders that go in take profit or stop loss
        portfolio.check_for_orders_to_close(today_price, today_date)
        # END SECTION - DELTA

        #log.critical(f"Portfolio: {portfolio.value_history}")
        #log.critical(f"Orders: {portfolio.orders}")

        # SECTION - EPSILON
        # INFO - If the portfolio is empty or  is the last day, close all orders that are open at the close price, then stop the backtesting
        if portfolio.liquidity() <= 0 or (date_index == amount_of_financial_data-1):
            portfolio.close_all_orders(today_price, today_date)
            break
        # END SECTION - EPSILON

        # SECTION - ZETA
        # INFO - check what strategy says (buy/sell/idle)
        position = portfolio.strategy.check_for_signals(
            data_input_for_strategy)
        # END SECTION - ZETA

        # SECTION - ETA
        if position == Position.IDLE:
            continue
        # END SECTION - ETA
        #log.debug(f"Position: {position}")
        # SECTION - THETA
        # INFO - check if there are orders open
        open_orders = portfolio.get_open_orders_of_certain_position(position)
        #log.debug(f"Open Orders: {open_orders}")
        # END SECTION - THETA

        # SECTION - IOTA
        # INFO - check if the order is the same of the signal
        if is_order_of_this_type(open_orders, position):
            continue
        # END SECTION - IOTA

        # SECTION - KAPPA
        # INFO - if no order is open, open the order
        elif(open_orders.empty):
            order_created = portfolio.create_order(
                creation_price=today_price,
                creation_date=today_date,
                position=position
            )
            # log.debug(
            #    f"New Order. Order ID: {order_created['ID']}")
        # END SECTION - KAPPA

        # SECTION - LAMBDA
        # INFO - check if the order is the opposite of the signal
        elif (not(is_order_of_this_type(open_orders, position))):
            # INFO - close the opposite order
            # TODO - handle multiple close of orders
            portfolio.close_order(open_orders, today_price, today_date)
            # INFO - open new order
            order_created = portfolio.create_order(
                open_price=today_price,
                open_date=today_date,
                position=position
            )
            # log.debug(
            #    f"New Order. Order ID: {order_created['ID']}")
        # END SECTION - LAMBDA

    return portfolio, backtest_info
