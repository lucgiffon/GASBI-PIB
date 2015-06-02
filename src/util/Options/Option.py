# -*- coding: utf-8 -*-

"""Module containing the Option class containing options attribute and
allow to manipulate it."""

from util.Logger import Logger


class Option(object):
    """Option with its attributes, getters and setters."""
    def __init__(self, name, value, group, tool=None, subgroup=None):
        """Initialization of Option object with name, value, tool
        and subgroup.

        If tool has no subgroup, subgroup is set at 'None'.
        """
        self.__name = name

        try:
            # The value may be a string which should behave like a list.
            if ',' in value:
                newvalue = ''
                # Then the string is splitted on comas.
                for elm in value.split(','):
                    # The value is refined.
                    newvalue += elm.strip('\' ') + ','
                self.__value = newvalue.rstrip(',')
            else:
                self.__value = eval(value)
        # Case the type of the value required is 'str', a SyntaxError
        # exception will be raise if there is no quotes.
        except (SyntaxError, NameError):
            self.__value = value

        self.__group = group

        self.__tool = tool

        self.__subgroup = subgroup

        if self.__value == '':
            Logger().warning("Option {} for tool {} is ".format(self.__name,
                                                                self.__tool) +
                             "not specified... default value has been" +
                             "set.")
            self.__value = 'default'

    def get_name(self):
        """Return the name of the option object."""
        return (self.__name)

    def get_value(self):
        """Return the value of the option object."""
        return (self.__value)

    def set_value(self, new_value):
        """Set a new value to the option object."""
        self.__value = new_value
        return 0

    def get_tool(self):
        """Return the name of the tool's option object."""
        return (self.__tool)

    def get_group(self):
        """Return the name of the group's option object."""
        return (self.__group)

    def __repr__(self):
        """Return a string representing the listing of option attributes.
        """
        message = ("Name: {}\t" +
                   "Value: {}\t" +
                   "Group: {}\t" +
                   "Tool: {}\t" +
                   "SubGroup: {}").format(self.__name,
                                          self.__value,
                                          self.__group,
                                          self.__tool,
                                          self.__subgroup)
        return (message)
