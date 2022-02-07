

def sharpe_ratio_over_period(portfolio, risk_free_rate):
    # INFO - get time in days enlapsed between first and last date
    time_in_days = (
        portfolio.value_history.date[-1] - portfolio.value_history.date[0]).days
    # INFO - convert risk_free_rate annualized to the risk_free_rate of the period of the portfolio
    risk_free_over_period = (1+risk_free_rate)**(time_in_days/252)-1
    return (percentage_return_over_period(portfolio)-risk_free_over_period)/portfolio_volatility_over_period(portfolio)
