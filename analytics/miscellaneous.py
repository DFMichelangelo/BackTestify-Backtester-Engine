def TY_Indicator(PnL, Max_DD, trading_days, num_trades):
    inactivity_penality = min(1, num_trades/(1+trading_days*0.16))
    metric = (PnL-Max_DD)*inactivity_penality
    return metric
