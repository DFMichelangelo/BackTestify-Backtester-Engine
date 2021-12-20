import logging
from rich.logging import RichHandler
import globals
FORMAT = "%(message)s"

#console_logger = logging.getLogger("console")
#log_level = "DEBUG" if globals.configuration['system']['environment'] == "Development" else "INFO"
logging.basicConfig(format=FORMAT, level="INFO",
                    datefmt="[%X]", handlers=[RichHandler()])
# console_logger.setLevel(globals.configuration["system"]["log_level"])
console_logger = logging.getLogger("rich")
console_logger.setLevel(globals.configuration["system"]["log_level"])
