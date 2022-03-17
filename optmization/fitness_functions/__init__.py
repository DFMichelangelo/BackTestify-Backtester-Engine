from abc import ABC, abstractmethod


class Fitness_function(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def compute_fitness_function(self, *args, **kwargs):
        pass
