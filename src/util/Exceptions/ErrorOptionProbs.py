# -*- coding: utf-8 -*-

"""Module containing the ErrorOptionProbs class."""


class ErrorOptionProbs(Exception):
    """ErrorOptionProbs is raised if the specified option probs are not equal
    to 1.
    """
    def __init__(self, option):
        self.__option_name = option.get_name()
        self.__option_value = option.get_value()
        self.__tool = option.get_tool()

    def __str__(self):
        message = (("Error: OptionProbs: probabilities " +
                    "{} for option ".format(self.__option_value) +
                    "{} are not equal 1 ".format(self.__option_name) +
                    "at tool {}. Please, fix.".format(self.__tool)))
        return message
