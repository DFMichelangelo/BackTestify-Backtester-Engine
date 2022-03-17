from fastapi import APIRouter
from logger import Logger
from repositories.backtest import Backtest_repository
from models.backtest_entity import Backtest_save_model
from optmization.fitness_functions import fitness_functions

router = APIRouter()

backtest_repository = Backtest_repository()

logger = Logger("Optimization Routes", "#7354f5")


@router.get("/fitness_functions")
def get_fitness_functions():
    return fitness_functions.generate_inputs()


@router.get("/optimize_strategy")
def optimize_strategy():
    pass
