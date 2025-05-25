import logging
from sys import stdout


class Logger(logging.Logger):

    def __init__(self, level, format=None, datefmt=None):
        super().__init__(__name__)
        if not datefmt:
            datefmt = "%d/%m/%Y - %H:%M:%S"
        self.setLevel(level=level)
        self.addHandler(logging.StreamHandler(stdout))
        self.propagate = True
        self.formatter = logging.Formatter(format, datefmt=datefmt)
        self.handlers[0].setFormatter(self.formatter)
        self.handlers[0].setLevel(self.level)
        self.handlers[0].addFilter(lambda record: record.levelno >= self.level)

        self.warning(f"Using {level} logger level.")

    def warning(self, message: str):
        super().warning(f"[WARNING] - {message}")

    def info(self, message: str):
        super().info(f"[INFO] - {message}")

    def error(self, message: str):
        super().error(f"[ERROR] - {message}")

    def debug(self, message: str):
        super().debug(f"[DEBUG] - {message}")

    def critical(self, message: str):
        super().critical(f"[CRITICAL] - {message}")


LoggerInstance = Logger("INFO")
