from analytics import percentage_return_annualized, volatility_annualized, downside_volatility_annualized


def sharpe_ratio_annualized(series, risk_free_rate):
    return (percentage_return_annualized(series) - risk_free_rate) / volatility_annualized(series)


def sortino_ratio_annualized(series, risk_free_rate):
    return (percentage_return_annualized(series) - risk_free_rate) / downside_volatility_annualized(series)


def calmar_ratio_annualized(percentage_return_annualized, max_drawdown):
    return percentage_return_annualized / max_drawdown if max_drawdown != 0 else "No DD"
