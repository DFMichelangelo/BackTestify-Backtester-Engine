from auxiliaries.enumerations import Position
from logger import Logger
from rich.progress import Progress


def is_order_of_this_type(order, position):
    return (order["position"] == position).any()


def backtest_strategy(portfolio, strategy, financial_data):
    backtest_info = {}

    amount_of_data_for_strategy_from_today = strategy.amount_of_data_for_strategy_from_today()
    amount_of_financial_data = len(financial_data.index)

    with Progress() as progress:
        backtesting_task = progress.add_task(
            "[red]Backtesting...", total=amount_of_financial_data-amount_of_data_for_strategy_from_today)
        progress_advance = 1
        for date_index in range(amount_of_data_for_strategy_from_today, amount_of_financial_data):

            # INFO - get data input for strategy
            data_input_for_strategy = financial_data[(
                date_index-amount_of_data_for_strategy_from_today):date_index]

            # INFO - get today price and today date
            today_price = financial_data.iloc[date_index, :]["Adj Close"]
            today_date = financial_data.iloc[date_index, :]["Date"]

            # INFO - 1) Check if you can close orders that go in take profit or stop loss
            portfolio.check_for_orders_to_close(today_price, today_date)
            # INFO - 2) If the portfolio is empty, then stop the backtesting
            if portfolio.value() <= 0:
                break
            # INFO - In the last day, close all orders that are open at the close price
            if date_index == amount_of_financial_data:
                portfolio.close_all_orders(today_price, today_date)
                break

            # INFO - 3) check what strategy says (buy/sell/idle)
            position = strategy.check_for_signals(data_input_for_strategy)
            if position == Position.IDLE:
                continue

            # INFO - 4) check if there are orders open
            open_orders = portfolio.check_for_open_orders(position)

            # INFO - 5) check if the order is the same of the signal
            if is_order_of_this_type(open_orders, position):
                continue
            # INFO - 5.1) if no order is open, open the order
            elif(open_orders.empty):
                portfolio.create_order(
                    creation_price=today_price,
                    creation_date=today_date,
                    position=position
                )

            # INFO - 6) check if the order is the opposite of the signal
            elif (not(is_order_of_this_type(open_orders, position))):
                # INFO 6.1) close the opposite order7
                # TODO handle multiple close of orders
                portfolio.close_order(open_orders, today_price, today_date)
                # INFO - 7) open new order
                portfolio.create_order(
                    open_price=today_price,
                    open_date=today_date,
                    position=position
                )

            # INFO - update progress bar (add one "tick")
            progress.update(backtesting_task, advance=progress_advance)
    return portfolio, backtest_info
