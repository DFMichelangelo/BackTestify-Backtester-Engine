
import logging
from rich.logging import RichHandler
FORMAT = "%(message)s"


#logging.basicConfig(format=FORMAT, level="INFO",  # level=globals.config["system"]["log_level"],
#                    datefmt="[%X]", handlers=[RichHandler()])
#modular_logger = logging.getLogger("rich")
#handler = logging.StreamHandler(sys.stdout)
console_logger = logging.getLogger("console")
logging.basicConfig(format=FORMAT, level="INFO",  # level=globals.config["system"]["log_level"],
                    datefmt="[%X]", handlers=[RichHandler()])
modular_logger = logging.getLogger("rich")
