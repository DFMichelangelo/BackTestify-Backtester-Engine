def absolute_return_over_period(portfolio):
    return portfolio.value_history.iloc[-1]["liquidity"] - portfolio.value_history.iloc[0]["liquidity"]


def percentage_return_over_period(portfolio):
    return (portfolio.value_history.iloc[-1]["liquidity"] - portfolio.value_history.iloc[0]["liquidity"]) / portfolio.value_history.iloc[0]["liquidity"]


def portfolio_volatility_over_period(portfolio):
    return (portfolio.value_history["liquidity"]+portfolio.value_history["assets_value"]).pct_change().iloc[1:, :].std()


def sharpe_ratio_over_period(portfolio, risk_free_rate):
    # INFO - get time in days enlapsed between first and last date
    time_in_days = (
        portfolio.value_history.date[-1] - portfolio.value_history.date[0]).days
    # INFO - convert risk_free_rate annualized to the risk_free_rate of the period of the portfolio
    risk_free_over_period = (1+risk_free_rate)**(time_in_days/252)-1
    return (percentage_return_over_period(portfolio)-risk_free_over_period)/portfolio_volatility_over_period(portfolio)
