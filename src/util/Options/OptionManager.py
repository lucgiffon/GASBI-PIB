# -*- coding: utf-8 -*-

"""Module Containing OptionManager class which manipulate options."""

from util.Constant import Constant

from tool.Tool import Tool
from tool.Glimmer import Glimmer
from tool.GeneMark import GeneMark
from tool.BuildICM import BuildICM
from tool.Extract import Extract
from tool.LongORFs import LongORFs
from tool.TRNAScan import TRNAScan

from util.Options.Option import Option
from util.Options.OptionList import OptionList

from util.Logger import Logger


class OptionManager(object):
    """Check and set options for tools and manipulate them.

    Options's tools managed by OptionManager:
    Glimmer, LongOrfs, BuildICM, Extract, GeneMark, tRNAscan.

    Set options from configuration file with set_options().
    Check the quality of options with check_options().
    Gives options by get_options().
    """
    def __init__(self, optionlist=[]):
        """Initialize the OptionList object.

        Private attributes:
        all_options is an Optionlist instance filled by set_options().
        """
        self.__all_options = OptionList(optionlist, 'all_options')

    def set_options(self, config_file):
        """Load options from config file. Check the integrity of the
        configuration file by the way.

        The options are loaded by parsing the configuration file, line
        after line and searching for known pattern.
        """
        try:
            fic = open(config_file, 'r')
            # Loading the first line of the file.
            line = None
            group = ''
            tool = ''
            subgroup = ''
            path = ''
            line_no = 0
            # The line after line parsing is performed here in the while loop.
            while line != '':
                line_no += 1
                line = fic.readline()
                splitted_line = line.split(' ', 1)
                # Verify that the line is not void and not an informative
                # line for user.
                if (line.strip() == '') or (splitted_line[0] == '#'):
                    Logger().debug("Line {}: void: {}".format(line_no,
                                                              line.strip()))
                    continue
                # If the marker 'Group:' is recognized, change the group
                # of the following options.
                elif splitted_line[0] == 'Group:':
                    Logger().debug("Line {}: {}".format(line_no, line.strip()))
                    path = ''
                    group = splitted_line[1].strip(': \n')
                    # Lines in the configuration file are human readable
                    # which is not optimized for parsing.
                    if group == 'Global':
                        group = 'General'
                    elif group == 'CDS Finding Tool':
                        group = 'CDSFindingTool'
                    elif group == 'tRNA Finding Tool':
                        group = 'TRNAFindingTool'
                    # If a new group is found, resets tool and subgroup.
                    tool = 'GASBI'
                    subgroup = ''
                    # If a new group is detected, create a sub-OptionList
                    # for all_options OptionList.
                    self.__all_options.append(OptionList([], group))
                    group_path = '{}/'.format(group)
                    # The path will be used to set options on the right place.
                    path += group_path
                # Idem for tool.
                elif splitted_line[0] == 'Tool:':
                    Logger().debug("Line {}: {}".format(line_no, line.strip()))
                    path = group_path
                    tool = splitted_line[1].strip(': \n')
                    if tool == 'Build ICM':
                        tool = 'BuildICM'
                    elif tool == 'Long ORFs':
                        tool = 'LongORFs'
                    elif tool == 'tRNAscan-SE':
                        tool = 'TRNAScan'
                    subgroup = ''
                    self.__all_options[path].append(OptionList([], tool))
                    tool_path = '{}/'.format(tool)
                    path += tool_path
                # Idem for subgroup.
                elif splitted_line[0] == 'Subgroup:':
                    Logger().debug("Line {}: {}".format(line_no, line.strip()))
                    path = group_path + tool_path
                    subgroup = splitted_line[1].strip(': \n')
                    if subgroup == 'Search Mode':
                        subgroup = 'Search'
                    elif subgroup == 'Alternate Cutoffs & Data Files':
                        subgroup = 'Alternate_Parameter'
                    self.__all_options[path].append(OptionList([], subgroup))
                    subgroup_path = '{}/'.format(subgroup)
                    path += subgroup_path
                # If no marker is recognized, an option is set at the
                # current line.
                else:
                    splitted_line = line.split(':')
                    option_name = splitted_line[0].strip()
                    # Strip the characters which would have been added
                    # by the user but are not useful.
                    option_value = splitted_line[1].strip(' \n()[]\'"')
                    # Creating the option object with its attributes.
                    option = Option(option_name, option_value, group,
                                    tool, subgroup)
                    Logger().debug("Line {}: Option: {}".format(line_no,
                                                                line.strip()) +
                                   '\n' + str(option))
                    # The path is used to localize the option.
                    self.__all_options[path].append(option)
            fic.close()
        # Verify is the configuration file exists.
        except FileNotFoundError:
            Logger().error("The specified config file " +
                           "does not exists: {}".format(config_file))
            raise FileNotFoundError
        # Verify integrity of the configuration file.
        except IndexError:
            Logger().error(("The line {} is not formated " +
                            "correctly: {}").format(line_no, line))
            fic.close()
            raise IndexError

    def check_options(self):
        """Call tool's check_options().

        Each tool knows its own way to check if options are right.
        They Verify: Expected Options, Option's type, Path existence
        """
        # Particular treatment for general options.
        Tool.check_options(self.__all_options['General'])
        # The loop will check options for each tool's name in the
        # Constant list.
        for tool in Constant.TOOLS_LIST:
            Logger().debug(tool)
            object_name = tool.rstrip('/ ').split('/')[-1]
            # The checking is done with static methods and variables.
            available_options = eval(object_name).OPTIONS_PROPERTIES
            # 'tool' is the path to the OptionList for the tool.
            eval(object_name).check_options(self.__all_options[tool],
                                            available_options)

    def get_options(self):
        """Return all options in an OptionList object."""
        return (self.__all_options)

    def __repr__(self):
        """It is the OptionList object's __repr__ special method."""
        return (self.__all_options.__str__())
