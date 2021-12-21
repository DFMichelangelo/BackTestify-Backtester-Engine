from logger.console_logger import console_logger
from logger.file_logger import file_logger


class Logger:

    def __init__(self, module, color):
        self.module = module
        self.color = color

    def general(self, type, msg):
        message = f"[bold on {self.color}][{self.module}][/]" + \
            " - " + str(msg)
        message2 = f"[{self.module}]" + " - " + str(msg)

        if type == "DEBUG":
            console_logger.debug(message, extra={"markup": True})
            file_logger.debug(message2)
        elif type == "INFO":
            console_logger.info(message, extra={"markup": True})
            file_logger.info(message2)
        elif type == "WARNING":
            console_logger.warning(message, extra={"markup": True})
            file_logger.warning(message2)
        elif type == "ERROR":
            console_logger.error(message, extra={"markup": True})
            file_logger.error(message2)
        elif type == "CRITICAL":
            console_logger.critical(message, extra={"markup": True})
            file_logger.critical(message2)

    def debug(self, msg):
        return self.general("DEBUG", msg)

    def info(self, msg):
        return self.general("INFO", msg)

    def warning(self, msg):
        return self.general("WARNING", msg)

    def error(self, msg):
        return self.general("ERROR", msg)

    def critical(self, msg):
        return self.general("CRITICAL", msg)
