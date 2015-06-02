# -*- coding: utf-8 -*-

"""Module Containing Tool class which contain method for the
treatment of tools."""

import os
from util.Checker import Checker
from util.Options.OptionList import OptionList
from util.Logger import Logger


class Tool(object):
    """Tool is the superclass of all tool's classes."""
    # General options with their type.
    OPTIONS_PROPERTIES = {'OUT_PATH': {'type': 'str', 'key': None},
                          'SEQUENCE_PATH': {'type': 'str', 'key': None},
                          'TAG': {'type': 'str', 'key': None},
                          }
    # Attributes of Tool object are for all tools.
    NAME = 'General'

    def __init__(self, general_options):
        """Initialize general_options wich will be used by all tools.

        general_options is an OptionList."""
        self.general_options = general_options

    def launch_preliminary_tools(self, tools_to_launch, tool_objects):
        """Call preliminary tool's start functions.

        Some main tools need to launch preliminary tools before their own
        run. Example: Glimmer.
        tools_to_launch is a constant list in the tool object which contain
        the name of the preliminary tools.
        tool_objects is the dictionary of preliminary tools.
        The method is generic for all tools.
        """
        # tools_to_launch is an ordered list to launch preliminary tools
        # in the right order.
        for tool in tools_to_launch:
            # tool is the path of the tool.
            tool_object_name = tool.rstrip(' /').split('/')[-1]
            Logger().info("\tLaunching {}".format(tool_object_name))
            tool_objects[tool_object_name].set_output_path(self.get_output_path())
            tool_objects[tool_object_name].start()
            # Come back into main tool's output directory.
            os.chdir('{}'.format(self.get_output_path()))
            Logger().info("\t{} done".format(tool_object_name))

    def load_command_line_options(self, tool_options):
        """Return the command line with options loaded.

        tool_options is an OptionList Object.
        Options are loaded from tool_options OptionList.
        The method is generic for all tools.
        """
        cmd_line_options = ''
        # Subgroup are basic/expert.
        for subgroup in tool_options:
            for option in tool_options[subgroup.get_name()]:
                # Adding options at the command line.
                if (option.get_value() != 'default' and
                        self.OPTIONS_PROPERTIES[option.get_name()]['key'] is not None):
                    # With boolean options, there is no value to add;
                    # only the key binding.
                    if type(option.get_value()) != bool:
                        cmd_line_options += (' ' +
                                             self.OPTIONS_PROPERTIES[option.get_name()]['key'] +
                                             str(option.get_value()))
                    elif option.get_value() is not False:
                        cmd_line_options += (' ' +
                                             self.OPTIONS_PROPERTIES[option.get_name()]['key'])
        return cmd_line_options

    def get_output_path(self):
        """Return the ouput_path concatenated with tool's folder name as a string.

        The method is generic for all tools.
        """
        return (self.general_options['General/OUT_PATH'] + '/' +
                self.general_options['General/TAG'] + '/' +
                self.NAME.lower())

    @staticmethod
    def check_options(options, available_options=None):
        """Call Checker class's methods to check the quality of the options.

        Checking: Expected Options
                Option's type
                Basic Options specified #to do
                Path Options Exists

        Error Exceptions are raised if an option is wrong.
        The method is generic for all tools.
        Static Method.
        """
        # Checking general options.
        if available_options is None:
            available_options = Tool.OPTIONS_PROPERTIES
        # Writing the expected options.
        for option in available_options:
            Logger().debug('Option properties: ' + option +
                           '| Type: ' + available_options[option]['type'] +
                           '| Key: ' + str(available_options[option]['key']))
        # Analyzing options given.
        for element in options:
            if isinstance(element, OptionList):
                # Recursion if there is a subgroup.
                Tool.check_options(element, available_options)
            else:
                # No reason to check option if value == default.
                Logger().debug(element)
                if element.get_value() != 'default':
                    Checker.is_option_available(element, available_options.keys())
                    Checker.verify_option_type(element, available_options[element.get_name()])
                    Checker.verify_option_path(element)
                    # Particular case where the value is a list
                    # of probabilities.
                    if 'PROBS' in element.get_name():
                        Checker.verify_option_probs(element)

    def check_output(self):
        """Check the integrity of tool's output file.

        Warning Exception are raised if an output file is wrong.
        The method is generic for all tools.
        """
        # Moving to tool's output directory.
        os.chdir(self.get_output_path())
        try:
            output_file = open('{}.{}.txt'.format(self.general_options['TAG'],
                                                  self.EXTENSION), 'r')
            # Verify that the file is not void.
            if output_file.read().strip() == '':
                Logger.warning('{} output invalid.'.format(self.NAME))
            output_file.close()
        # Verify that the file exists.
        except FileNotFoundError:
            Logger().warning("{} has no output file for " +
                             "checking".format(self.NAME))

    def parse_output(self):
        """parse_ouput load information from tool's output file.

        Abstract Method.
        """
        pass

    def get_group(self):
        """Return the group of the tool object. (CDSFidning, tRANFinding..)

        Abstract method.
        """
        pass

    def start(self):
        """Launches tool's softwares on command line.

        Abstract Method.
        """
        pass
