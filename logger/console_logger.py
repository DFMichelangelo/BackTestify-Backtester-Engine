import logging
import uvicorn
from rich.logging import RichHandler
FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

# INFO - Create formatter
ch_formatter = uvicorn.logging.DefaultFormatter(
    FORMAT, datefmt="%d-%m-%Y %H:%M:%S")

# INFO - create console logger and set level to debug
console_logger = logging.getLogger('console_logger')
console_logger.setLevel(logging.DEBUG)

# INFO -Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# INFO - add formatter to ch
ch.setFormatter(ch_formatter)

# INFO - add ch to logger
# console_logger.addHandler(ch)
console_logger.addHandler(RichHandler(rich_tracebacks=True))
