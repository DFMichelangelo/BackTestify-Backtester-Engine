import logging

file_logger = logging.getLogger("file")
file_handler = logging.FileHandler("./logs/logfile.log")
file_handler.setLevel("INFO")
#sh = logging.StreamHandler(sys.stdout)
#se = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter(
    "%(asctime)s: %(levelname)s - %(message)s (Path: %(pathname)s - Function: %(funcName)s")
file_handler.setFormatter(formatter)
#sh.setFormatter(formatter)
#se.setFormatter(formatter)
file_logger.addHandler(file_handler)
#file_logger.addHandler(sh)
#file_logger.addHandler(se)
file_logger.propagate = False