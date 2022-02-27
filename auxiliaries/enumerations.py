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


class IntervalsInMilliseconds(Enum):
    ONE_SECOND = 1000
    FIVE_SECONDS = 5000             # INFO - 5*1000
    TEN_SECONDS = 10000             # INFO - 10*1000
    FIFTEEN_SECONDS = 15000         # INFO - 15*1000
    THIRTY_SECONDS = 30000          # INFO - 30*1000
    ONE_MINUTE = 60000              # INFO - 60*1000
    FIVE_MINUTES = 300000           # INFO - 5*60*1000
    TEN_MINUTES = 600000            # INFO - 10*60*1000
    FIFTEEN_MINUTES = 900000        # INFO - 15*60*1000
    THIRTY_MINUTES = 1800000        # INFO - 30*60*1000
    ONE_HOUR = 3600000              # INFO - 60*60*1000
    FOUR_HOURS = 14400000           # INFO - 4*60*60*1000
    ONE_DAY = 86400000              # INFO - 24*60*60*1000
    ONE_WEEK = 604800000            # INFO - 7*24*60*60*1000
    ONE_MONTH = 2419200000          # INFO - 30*24*60*60*1000
    ONE_TRADING_YEAR = 21772800000  # INFO - 252*24*60*60*1000
    ONE_YEAR = 31536000000          # INFO - 365*24*60*60*1000


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
