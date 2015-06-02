# -*- coding: utf-8 -*-

"""Module containing Checker class containing all static method useful to check
if Gasbi is processing correctly."""
import os
import time

from util.Exceptions.ErrorOptionPath import ErrorOptionPath
from util.Exceptions.ErrorOptionType import ErrorOptionType
from util.Exceptions.ErrorOptionUnavailable import ErrorOptionUnavailable
from util.Exceptions.ErrorOptionProbs import ErrorOptionProbs

from util.Logger import Logger


class Checker(object):
    """This class contain checking static methods.

    Can't be initialized.
    """

    @staticmethod
    def is_option_available(option, available_options):
        """If option not in available_options, raise
        ErrorOptionUnavailable.
        Else, return 0.
        """
        # Verify is the option's name is in the list of available options.
        if option.get_name() not in available_options:
            Logger().error(ErrorOptionUnavailable(option))
            raise ErrorOptionUnavailable(option)
        return 0

    @staticmethod
    def verify_option_type(option, available_options):
        """If option type wrong, raise ErrorOptionType.
        Else, return 0.
        """
        # Verify if the type matches.
        if (type(option.get_value()) != eval(available_options['type'])):
            Logger().error(ErrorOptionType(option, available_options))
            raise ErrorOptionType(option, available_options)
        return 0

    @staticmethod
    def verify_option_path(option):
        """If path doesn't exist, raise ErrorOptionPath.
        Else, return 0.
        """
        # Verify if the specified path exists.
        if (('PATH' in option.get_name()) and
                (os.path.exists(option.get_value()) is False)):
            Logger().error(ErrorOptionPath(option))
            raise ErrorOptionPath(option)
        return 0

    @staticmethod
    def verify_option_probs(option):
        """If probabilities are not equal to 1, raise ErrorOptionProbs.
        Else, return 0
        """
        # Verify if the sum of probabilities are equal to 1.
        prob_sum = 0
        for elm in option.get_value().split(','):
            prob_sum += float(elm)
        if prob_sum != 1:
            Logger().error(ErrorOptionProbs(option))
            raise ErrorOptionProbs(option)
        return 0
