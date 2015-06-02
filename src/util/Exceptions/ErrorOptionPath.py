# -*- coding: utf-8 -*-

"""Module containing the ErrorOptionPath class."""


class ErrorOptionPath(Exception):
    """ErrorOptionPath is raised if the specified option path
    doesn't exist.
    """
    def __init__(self, option):
        self.__option_name = option.get_name()
        self.__option_value = option.get_value()
        self.__tool = option.get_tool()

    def __str__(self):
        message = (("Error: OptionPath: {} doesn't exist for {} " +
                   "option at tool {}").format(self.__option_value,
                                               self.__option_name,
                                               self.__tool))
        return message
