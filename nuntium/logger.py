#! /usr/bin/python3
""" A logger class for the old articles project.
"""
import logging


class ArticleLogger:
    """A simple logger class for the OldArticles project.\n
    - each instance has default format & file name.

    """

    # Set Default
    FORMAT: str = "%(name)s - %(asctime)s - LEVEL(%(levelname)s) - %(message)s"
    LOG_FNAME: str = "OldArticles.log"

    def __init__(self, NAME: str) -> None:
        """Creates an ArticleLogger() object with a stream & file handler.\n
        Args:\n
            NAME - a string name for the ArticleLogger object.\n
        Returns:\n
            self - creates an object.
        """
        self.file_handler = logging.FileHandler(
            filename=ArticleLogger.LOG_FNAME,
            mode="a",
        )
        self.stream_handler = logging.StreamHandler()

        logging.basicConfig(
            handlers=[self.file_handler, self.stream_handler],
            format=ArticleLogger.FORMAT,
            level=logging.DEBUG,
        )

        self.logger = logging.getLogger(name=str(NAME))

    def debug(self, MSG: str) -> None:
        "Log a debug level issue."
        self.logger.debug(f"{MSG}")

    def warning(self, MSG: str) -> None:
        "Log a warning level issue."
        self.logger.warning(f"{MSG}")

    def critical(self, MSG: str) -> None:
        "Log a critical event."
        self.logger.critical(f"{MSG}")

    def error(self, MSG: str) -> None:
        self.logger.error(f"{MSG}", stack_info=True)