import logging

# INFO - Create formatter
fh_formatter = logging.Formatter(
    "%(asctime)s: %(levelname)s - %(message)s (Path: %(pathname)s - Function: %(funcName)s")

# INFO - Create file logger and set level to debug
file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.DEBUG)

# INFO - Create file handler and set level to debug
fh = logging.FileHandler("./logs/logfile.log")
fh.setLevel(logging.DEBUG)

# INFO - add formatter to fh
fh.setFormatter(fh_formatter)
file_logger.addHandler(fh)
