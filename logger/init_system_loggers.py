import logging
from rich.logging import RichHandler
import os


def init_sys_loggers():
    logger = logging.getLogger("uvicorn.access")
    logger.addHandler(RichHandler(rich_tracebacks=True))
    logger = logging.getLogger("uvicorn.error")
    logger.addHandler(RichHandler(rich_tracebacks=True))
