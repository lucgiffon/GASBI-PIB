# -*- coding: utf-8 -*-

"""Module containing the ErrorOptionUnavailable class."""


class ErrorOptionUnavailable(Exception):
    """ErrorOptionUnavailable is raised if the specified option
    doesn't exist.
    """
    def __init__(self, option):
        self.__option_name = option.get_name()
        self.__tool = option.get_tool()

    def __str__(self):
        message = ("Error: OptionUnavailable: {} Option is not " +
                   "available for the tool {}. Please, modify or " +
                   "clear this line.").format(self.__option_name,
                                              self.__tool)
        return message
