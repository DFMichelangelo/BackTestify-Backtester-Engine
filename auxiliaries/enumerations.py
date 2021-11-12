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


class Financial_Instrument_Type(Enum):
    EQUITY = "EQUITY"
    OPTION = "OPTION"


class Order_Status(Enum):
    SUBMITTED = "SUBMITTED"  # sent to the broker and awaiting confirmation
    OPEN = "OPEN",
    CLOSED = "CLOSED"
    # Accepted: accepted by the broker
    # Partial: partially executed
    # Completed: fully exexcuted
    # Canceled/Cancelled: canceled by the user
    #Expired: expired
    # Margin: not enough cash to execute the order.
    # Rejected: Rejected by the broker
