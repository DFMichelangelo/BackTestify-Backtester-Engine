def absolute_return_over_period(portfolio):
    return portfolio.value_history.iloc[-1]["liquidity"] - portfolio.value_history.iloc[0]["liquidity"]


def percentage_return_over_period(portfolio):
    return (portfolio.value_history.iloc[-1]["liquidity"] - portfolio.value_history.iloc[0]["liquidity"]) / portfolio.value_history.iloc[0]["liquidity"]


def portfolio_volatility_over_period(portfolio):
    return (portfolio.value_history["liquidity"]+portfolio.value_history["assets_value"]).pct_change().iloc[1:, :].std()
