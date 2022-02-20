from analytics import percentage_return_annualized, volatility_annualized, downside_volatility_annualized


def sharpe_ratio_annualized(series, risk_free_rate):
    return (percentage_return_annualized(series) - risk_free_rate) / volatility_annualized(series)


def sortino_ratio_annualized(series, risk_free_rate):
    return (percentage_return_annualized(series) - risk_free_rate) / downside_volatility_annualized(series)
