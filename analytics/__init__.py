import numpy as np
import statsmodels.api as sm


def sharpe_ratio_over_period(portfolio, risk_free_rate):
    # INFO - get time in days enlapsed between first and last date
    time_in_days = (
        portfolio.value_history.date[-1] - portfolio.value_history.date[0]).days
    # INFO - convert risk_free_rate annualized to the risk_free_rate of the period of the portfolio
    risk_free_over_period = (1+risk_free_rate)**(time_in_days/252)-1
    return (percentage_return_over_period(portfolio)-risk_free_over_period)/volatility_over_period(portfolio)


def annualize_rate(rate, time):
    return (1+rate)**(time/252)-1


def absolute_return_over_period(series):
    return series.iloc[-1] - series.iloc[0]


def absolute_return_annualized(series):
    profit_made_in_period = absolute_return_over_period(series)
    return 252*profit_made_in_period/len(series)


def percentage_return_over_period(series):
    return (series.iloc[-1] - series.iloc[0]) / series.iloc[0]


def percentage_return_annualized(series):
    percentage_over_period = percentage_return_over_period(series)
    return annualize_rate(percentage_over_period, len(series))


def volatility_over_period(series):
    return series.pct_change().iloc[1:].std()*np.sqrt(len(series))


def volatility_annualized(series):
    return series.pct_change().iloc[1:].std()*np.sqrt(252)


def autocorrelation_function(series):
    acf, confidence_intervals = sm.tsa.acf(
        series, nlags=50, alpha=0.05, fft=False)
    # INFO - Remove lag 0
    acf = acf[1:]
    confidence_intervals = confidence_intervals[1:]
    confidence_intervals = [[ci[0]-acf[ind], ci[1]-acf[ind]]
                            for ind, ci in enumerate(confidence_intervals)]
    return {
        "values": list(acf),
        "confidence_intervals": confidence_intervals
    }


def partial_autocorrelation_function(series):
    pacf, confidence_intervals = sm.tsa.pacf(
        series, nlags=50, alpha=0.05)
    # INFO - Remove lag 0
    pacf = pacf[1:]
    confidence_intervals = confidence_intervals[1:]
    confidence_intervals = [[ci[0]-pacf[ind], ci[1]-pacf[ind]]
                            for ind, ci in enumerate(confidence_intervals)]
    return {
        "values": list(pacf),
        "confidence_intervals": confidence_intervals
    }
