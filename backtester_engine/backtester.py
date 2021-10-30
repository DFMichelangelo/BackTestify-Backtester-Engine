from auxiliaries.enumerations import Position
from logger import Logger
from rich.progress import Progress
import time


def is_order_of_this_position(order, position_type):
    return order["position"] == position_type


def backtest_strategy(portfolio, strategy, financial_data):
    logger = Logger("Backtester", "#BADA2A")
    amount_of_data_for_strategy_from_today = strategy.amount_of_data_for_strategy_from_today()
    amount_of_financial_data = len(financial_data.index)
    with Progress() as progress:
        backtesting_task = progress.add_task(
            "[red]Backtesting...", total=amount_of_financial_data-amount_of_data_for_strategy_from_today)
        progress_advance = 1
        for date_index in range(amount_of_data_for_strategy_from_today, amount_of_financial_data):
            data_input_for_strategy = financial_data[(
                date_index-amount_of_data_for_strategy_from_today):date_index]
            today_price = financial_data.iloc[date_index, 1:]
            today_date = financial_data.index[date_index]
            progress.update(backtesting_task, advance=progress_advance)
            time.sleep(0.02)

        # ? 1) check if you can close orders that go in take profit or stop loss
#            portfolio.check_for_orders_to_close(today_price, today_date)
#            if portfolio.value() <= 0:
#                break
#        # ? in the last day, close all orders that are open at the close price
#            if date_index == amount_of_financial_data:
#                portfolio.close_all_orders(today_price, today_date)
#                break
#
#        # ? 2) check what strategy says (buy/sell/idle)
#            position = strategy.check_for_signals(data_input_for_strategy)
#            if position == Position.IDLE:
#                next
#
#            # ? 3) check if there are orders open
#            open_orders = portfolio.check_for_open_orders(position)
#            # ? 4) if no order is open, open the order
#            if(open_orders == None or len(open_orders) == 0):
#                portfolio.add_order(
#                    open_price=today_price,
#                    open_date=today_date,
#                    position=position
#                )
#
#        # ? 5) check if the order is the same of the signal
#        # elif isOrderOfThisType(ordersOpen, orderType)):
#                # pass
#
#        # ? 6) check if the order is the opposite of the signal
#            elif (not(is_order_of_this_position(open_orders, position))):
#                # ? 7) close the opposite order
#                portfolio = portfolio.close_order(
#                    open_orders, today_price, today_date)
#    # ? 8) open new order
#                portfolio.add_order(
#                    open_price=today_price,
#                    open_date=today_date,
#                    position=position
#                )

    return portfolio
