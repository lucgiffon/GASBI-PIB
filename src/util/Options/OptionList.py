# -*- coding: utf-8 -*-

"""Module containing the OptionList class. OptionList is a container
for option Objects and allow to access options by xPATH indices"""

from util.Options.Option import Option
from util.Exceptions.ErrorOptionMissing import ErrorOptionMissing
from util.Logger import Logger


class OptionList(object):
    """OptionList is a container for option objects. It can be
    manipulated like a list by index keys specifying the path to options.
    """
    def __init__(self, options, name):
        """Initialize OptionList object with an OptionList or classic
        list and a name for the optionList.
        """
        assert (isinstance(options, OptionList) or
                isinstance(options, list))
        self.__options = options
        self.__name = name

    def __getitem__(self, path):
        """Return an element of the OptionList by specifying a path to the option.

        The accession to the path is done by recursion.

        example:
        CDSFindingTool/Glimmer/Basic/ICM_MODEL_PATH
        or
        TRNAFindingTool/tRNAScan/
        etc..
        """
        returned = None
        # Recovering the first element of the searched option's path.
        splitted_path = path.split('/', 1)
        # Within Options or OptionList of my OptionList
        for option in self.__options:
            # If the path is not finished
            if (len(splitted_path) >= 2 and
                splitted_path[1] != '' and
                # and if the element is an OptionList
                isinstance(option, OptionList) and
                # anf if the name of the object matches the path's element
                    option.get_name() == splitted_path[0]):
                # I look for the following path in the element -> recursion
                returned = option[splitted_path[1]]
                # Break the loop
                break

            # If the path is finished
            elif (len(splitted_path) <= 2 and
                  # and if the name of the element matches the path's element
                  option.get_name() == splitted_path[-1] and
                  # search for Option priority
                  isinstance(option, Option)):
                returned = option.get_value()
                # Break the loop
                break

            # If the path is finished
            elif (len(splitted_path) <= 2 and
                  # and if the name of the object matches the path's element
                  option.get_name() == splitted_path[0] and
                  # and if the element is an OptionList
                  isinstance(option, OptionList)):
                returned = option
                # Break the loop
                break

        if returned is not None:
            return returned
        else:
            Logger().error(ErrorOptionMissing(path))
            raise ErrorOptionMissing(path)

    def __setitem__(self, path, value):
        """Modify an element of the OptionList by specifying a path to the option.

        The accession to the path is done by recursion.

        example:
        CDSFindingTool/Glimmer/Basic/ICM_MODEL_PATH
        or
        TRNAFindingTool/tRNAScan/
        etc..
        """
        success = False
        # Recovering the first element of the searched option's path.
        splitted_path = path.split('/', 1)
        # Within Options or OptionList of my OptionList
        for option in self.__options:
            # If the path is not finished
            if (len(splitted_path) > 1 and
                # and if the element is an OptionList
                isinstance(option, OptionList) and
                # anf if the name of the object matches the path's element
                    option.get_name() == splitted_path[0]):
                # I look for the following path in the element -> recursion
                option[splitted_path[1]] = value
                # Break the loop
                success = True
                break
            # If the path is finished
            elif (len(splitted_path) == 1 and
                  isinstance(option, Option) and
                  # and if the name of the element matches the path's element
                  option.get_name() == splitted_path[0]):
                option.set_value(value)
                success = True
                # Break the loop
                break
        if success is True:
            return
        else:
            Logger().error(ErrorOptionMissing(path))
            raise ErrorOptionMissing(path)

    def append(self, option):
        """Append an element to OptionList.

        append method for OptionList is similar to append build-in
        function for lists but it takes only Option or OptionList
        objects as argument.
        """
        if isinstance(option, Option) or isinstance(option, OptionList):
            self.__options.append(option)
        else:
            Logger().error("Impossible d'ajouter l'option {} à une" +
                           " OptionList car ce n'est pas une option")
        return

    def get_name(self):
        """Return the name attribute of the OptionList."""
        return (self.__name)

    def __iter__(self):
        """Return options iterable.

        Useful for 'for-loops'.
        """
        return (iter(self.__options))

    def __repr__(self):
        """Return a string representing the OptionList object."""
        message = '{}'.format(self.__options)
        return (message)
