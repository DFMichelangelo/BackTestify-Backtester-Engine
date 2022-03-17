from optmization.fitness_functions import Fitness_function


class TY_function(Fitness_function):
    name = "T Function"

    def __init__(self):
        pass

    def compute_fitness_function(self, PnL, Max_DD, trading_days, num_trades):
        inactivity_penality = min(1, num_trades/(1+trading_days*0.16))
        metric = (PnL-Max_DD)*inactivity_penality
        return metric
