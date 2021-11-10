from enum import Enum


class Position(Enum):
    LONG = "LONG"
    IDLE = "IDLE"
    SHORT = "SHORT"


class Order_Type(Enum):
    MARKET_ORDER = "MARKET_ORDER"
    LIMIT_ORDER = "LIMIT_ORDER"
    STOP_ORDER = "STOP_ORDER"
    BUY_STOP_ORDER = "BUY_STOP_ORDER"


class Financial_Instrument(Enum):
    EQUITY = "EQUITY"
    OPTION = "OPTION"
