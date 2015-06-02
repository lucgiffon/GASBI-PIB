# -*- coding: utf-8 -*-

"""Module containing the ErrorOptionMissing class."""


class ErrorOptionMissing(Exception):
    """ErrorOptionMissing if the specified option is missing.
    """
    def __init__(self, path):
        self.__pathmissing = path

    def __str__(self):
        message = ("Error: OptionMissing: Path {} " +
                   "does not exist yet.").format(self.__pathmissing)

        return message
