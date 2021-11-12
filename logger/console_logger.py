import logging
from rich.logging import RichHandler
import globals
FORMAT = "%(message)s"


# logging.basicConfig(format=FORMAT, level="INFO",  # level=globals.config["system"]["log_level"],
#                    datefmt="[%X]", handlers=[RichHandler()])
#modular_logger = logging.getLogger("rich")
#handler = logging.StreamHandler(sys.stdout)
console_logger = logging.getLogger("console")
log_level = "DEBUG" if globals.configuration['system']['environment'] == "Development" else "INFO"
logging.basicConfig(format=FORMAT, level=log_level,  # level=globals.config["system"]["log_level"],
                    datefmt="[%X]", handlers=[RichHandler()])
modular_logger = logging.getLogger("rich")
