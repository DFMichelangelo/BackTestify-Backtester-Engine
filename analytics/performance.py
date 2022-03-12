from analytics import percentage_return_annualized, volatility_annualized, downside_volatility_annualized
import numpy as np
import statsmodels.api as sm


def sharpe_ratio_annualized(series, risk_free_rate):
    return (percentage_return_annualized(series) - risk_free_rate) / volatility_annualized(series)


def sortino_ratio_annualized(series, risk_free_rate):
    return (percentage_return_annualized(series) - risk_free_rate) / downside_volatility_annualized(series)


def calmar_ratio_annualized(percentage_return_annualized, max_drawdown):
    return percentage_return_annualized / max_drawdown if max_drawdown != 0 else "No DD"


def correlation_with_benchmark(portfolio_series, benchmark_series):
    return np.corrcoef(portfolio_series, benchmark_series[-len(portfolio_series):])[0, 1]


def beta(portfolio_series, benchmark_series):
    benchmark_series = benchmark_series[-len(portfolio_series):]
    return np.cov(portfolio_series, benchmark_series)[0, 1]/np.var(benchmark_series)


def kestner_ratio(portfolio_series):
    X = list(range(len(portfolio_series)))
    X = sm.add_constant(X)
    model = sm.OLS(portfolio_series, X)
    results = model.fit()
    return results.params.x1/(len(portfolio_series)*results.bse.x1)
