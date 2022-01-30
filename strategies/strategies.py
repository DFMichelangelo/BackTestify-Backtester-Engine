from strategies.RSI import RSI_strategy
from strategies.MA_Crossover import MA_crossover_strategy
strategies_classes = [MA_crossover_strategy, RSI_strategy]


def spread_strategy_in_object(strategy, add_strategy_class):
    # extract name and parameters from each strategy
    strategy_spreaded = {
        "name": strategy.name,
        "indicators_parameters_name": strategy.indicators_parameters_name
    }
    if add_strategy_class:
        strategy_spreaded["strategy"] = strategy

    return strategy_spreaded


def generate_inputs(add_strategy_class):
    # extract name and parameters from each strategy
    return[spread_strategy_in_object(strategy, add_strategy_class) for strategy in strategies_classes]


def get_stategy_by_name(name):
    for strategy in strategies_classes:
        if strategy.name == name:
            return strategy
