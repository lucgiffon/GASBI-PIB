# -*- coding: utf-8 -*-

"""Module containing the Logger class which allow to write logs."""

import logging

from logging.handlers import RotatingFileHandler

from util.Singleton import singleton


@singleton
class Logger(object):
    """Logger is a singleton class which will be call anywhere in Gasbi
    to write log messages.
    """
    def __init__(self):
        """Initialize the logger calling logging methods.
        """

        self.__logger = logging.getLogger()

        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: ' +
                                      '%(message)s')

        file_handler = RotatingFileHandler('.log', 'a', 1000000, 1)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        self.__logger.addHandler(stream_handler)

    def debug(self, msg):
        """Call the loging.debug method."""
        self.__logger.debug(msg)

    def info(self, msg):
        """Call the loging.debug method."""
        self.__logger.info(msg)

    def warning(self, msg):
        """Call the loging.debug method."""
        self.__logger.warning(msg)

    def error(self, msg):
        """Call the loging.debug method."""
        self.__logger.error(msg)

    def critical(self, msg):
        """Call the loging.debug method."""
        self.__logger.critical(msg)

    def set_verbosity(self, verbosity):
        """Set the logging level.

        0 for critical
        1 for error
        2 for warning
        3 for info
        4 for debug
        """
        if verbosity == 0:
            self.__logger.setLevel(logging.CRITICAL)
        if verbosity == 1:
            self.__logger.setLevel(logging.ERROR)
        if verbosity == 2:
            self.__logger.setLevel(logging.WARNING)
        if verbosity == 3:
            self.__logger.setLevel(logging.INFO)
        if verbosity >= 4:
            self.__logger.setLevel(logging.DEBUG)
