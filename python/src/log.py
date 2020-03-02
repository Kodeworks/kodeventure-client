from logging import DEBUG, INFO, WARNING, ERROR
from sys import stderr
from typing import Any

from colorama import init, Fore

# Wraps stdout and stderr in a proxy object that resets any terminal color after print()
init(autoreset=True)


class Log:
    """
    Simple console output utility
    """

    loglevel: int = DEBUG

    @staticmethod
    def debug(msg: str):
        """
        Print in a lightblue color
        :param str: The message
        """

        if Log.loglevel == DEBUG:
            print(f'{Fore.LIGHTBLUE_EX}{msg}')

    @staticmethod
    def server(event_type: str, msg: str):
        """
        Print a server message in a cyan color.
        :param event_type: The event type from the server payload
        :param msg: The message
        """

        print(f'{Fore.CYAN}[SERVER] ({event_type}) {msg}')

    @staticmethod
    def info(msg: str):
        """
        Print a regular unformatted message
        :param str: The message
        """

        if Log.loglevel <= INFO:
            print(msg)

    @staticmethod
    def warning(msg: str):
        """
        Print a warning message in yellow color.
        :param msg: The message
        """

        if Log.loglevel <= WARNING:
            print(f'{Fore.YELLOW}{msg}')

    @staticmethod
    def error(msg: str):
        """
        Print an error mesage to stderr in red
        :param msg: The message
        """

        if Log.loglevel <= ERROR:
            print(f'{Fore.RED}{msg}', file=stderr)
