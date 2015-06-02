# -*- coding: utf-8 -*-

"""Module containing the ErrorOptionType class."""


class ErrorOptionType(Exception):
    """ErrorOptionType is raised if the specified option value
    has the wrong type.
    """
    def __init__(self, option, reference):
        self.__option_name = option.get_name()
        self.__option_value = option.get_value()
        self.__option_type = eval(reference['type'])
        self.__tool = option.get_tool()

    def __str__(self):
        message = ("Error: OptionType: Wrong Type ({}) for " +
                   "option {} at tool {}. {} " +
                   "was expected. ").format(type(self.__option_value),
                                            self.__option_name,
                                            self.__tool,
                                            self.__option_type)
        return message
