from auxiliaries.enumerations import Position


def orders_amount_for_types(orders):
    total_orders = len(orders)
    amount_long_orders = len(orders.loc[orders["position"] == Position.LONG])

    amount_short_orders = len(orders.loc[orders["position"] == Position.SHORT])

    positive_pnl_orders_filter = orders["PnL"] > 0
    amount_profitable_long_orders = len(orders[
        (orders["position"] == Position.LONG) &
        positive_pnl_orders_filter])

    amount_profitable_short_orders = len(orders[
        (orders["position"] == Position.SHORT) &
        positive_pnl_orders_filter])

    return {
        "general": {
            "amount": total_orders,
            "percentage_profitable": (amount_profitable_long_orders + amount_profitable_short_orders)/total_orders
        },
        "long_orders": {
            "amount": amount_long_orders,
            "percentage": amount_long_orders/total_orders if total_orders > 0 else 0,
            "amount_profitable": amount_profitable_long_orders,
            "percentage_profitable": amount_profitable_long_orders/amount_long_orders if amount_long_orders > 0 else 0
        },
        "short_orders": {
            "amount": amount_short_orders,
            "percentage": amount_short_orders/total_orders if total_orders > 0 else 0,
            "amount_profitable": amount_profitable_short_orders,
            "percentage_profitable": amount_profitable_short_orders/amount_short_orders if amount_short_orders > 0 else 0
        }
    }
