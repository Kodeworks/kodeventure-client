from logging import DEBUG, INFO, WARNING, ERROR
from sys import stdout


class Log:
    loglevel: int = DEBUG

    @staticmethod
    def debug(self, msg: str):
        pass

    @staticmethod
    def info(self, msg: str):
        pass

    @staticmethod
    def warning(self, msg: str):
        pass

    @staticmethod
    def error(self, msg: str):
        pass
