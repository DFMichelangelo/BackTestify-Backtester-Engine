from fastapi import APIRouter
from logger import Logger
from repositories.backtest import Backtest_repository
from models.backtest_entity import Backtest_save_model

router = APIRouter()

backtest_repository = Backtest_repository()

logger = Logger("Backtest Routes", "#4287f5")


@router.get("/all")
def get_backtests():
    a = backtest_repository.get_all()
    return a


@router.post("/")
def save_backtest(save_backtest_data: Backtest_save_model):
    return backtest_repository.create_one(save_backtest_data.dict())


@router.get("/{id}")
def get_backtest():
    pass


@router.delete("/{id}")
def delete_backtest():
    pass
