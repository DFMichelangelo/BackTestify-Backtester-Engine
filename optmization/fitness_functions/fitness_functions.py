from optmization.fitness_functions.TY_function import TY_function
fitness_functions_classes = [TY_function]


def generate_inputs():
    # extract name and parameters from each strategy
    return [fitness_function.name for fitness_function in fitness_functions_classes]


def get_fitness_function_by_name(name):
    for fitness_function in fitness_functions_classes:
        if fitness_function.name == name:
            return fitness_function
