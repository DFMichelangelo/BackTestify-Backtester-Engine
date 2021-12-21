import logging
from rich.logging import RichHandler
import os


def init_sys_loggers():
    if os.getenv('ENVIRONMENT') == 'development':
        logger = logging.getLogger("uvicorn.access")
        logger.addHandler(RichHandler(rich_tracebacks=True))
        logger = logging.getLogger("uvicorn.error")
        logger.addHandler(RichHandler(rich_tracebacks=True))
        return True
    elif os.getenv('ENVIRONMENT') == 'production':
        return False
    else:
        raise Exception('ENVIRONMENT not set')
