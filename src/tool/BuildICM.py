# -*- coding: utf-8 -*-

"""Module Containing BuildICM class which check options, launch and parse
results of BuildICM software.
"""

import os

from tool.PreliminaryTool import PreliminaryTool
from util.Logger import Logger


class BuildICM(PreliminaryTool):
    """Check options and launch BuildICM software.

    Launch BuildICM with start().
    BuildICM inherit from PreliminaryTool.
    Static variables for BuildICM class are: OPTIONS_PROPERTIES, NAME
    """
    # Tool's Options, their type and their key for command line.
    OPTIONS_PROPERTIES = {'INPUT_FILE_PATH': {'typee': 'str', 'key': None},
                          'DEPTH': {'typee': 'int', 'key': '-d'},
                          'NO_STOPS': {'typee': 'bool', 'key': '-F'},
                          'PERIOD': {'typee': 'int', 'key': '-p'},
                          'REVERSE': {'typee': 'bool', 'key': '-r'},
                          'WIDTH': {'typee': 'int', 'key': '-w'},
                          'TRANS_TABLE': {'typee': 'int', 'key': '-z'},
                          'STOP_CODONS': {'typee': 'list', 'key': '-Z'},
                          }
    # Name of the class.
    NAME = 'BuildICM'

    def __init__(self, general_options, buildicm_options):
        """Initialize the BuildICM_options.

        Private Attributes:
        BuildICM_options is an OptionList which contain only BuildICM's
        options.
        parent_output_path and output_path will be set later because the
        get_output_path method from Tool object is not right for
        preliminary tools.
        """
        super(BuildICM, self).__init__(general_options)
        self.__buildicm_options = buildicm_options
        self.__parent_output_path = ''
        self.__output_path = ''

    def start(self):
        """Launches BuildICM software on command line."""
        # Root command line.
        # -v option for verbosity level at 1
        cmd_line_run = 'build-icm -v1'
        # Adding options to command Line
        cmd_line_run += self.load_command_line_options(self.__buildicm_options)
        # Modificating INPUT_FILE_PATH if the user set it to default
        if self.__buildicm_options['Basic/INPUT_FILE_PATH'] == 'default':
            self.__buildicm_options['Basic/INPUT_FILE_PATH'] = (self.__parent_output_path +
                                                                '/' +
                                                                'extract' + '/' +
                                                                self.general_options['TAG'] +
                                                                '.train.txt')
        # Adding obligatory parameters at the end of command line.
        cmd_line_run += (' ' + self.general_options['TAG'] + '.icm.txt <')
        cmd_line_run += (' ' +
                         self.__buildicm_options['Basic/INPUT_FILE_PATH'])

        # Create output directory and move into it.
        os.system('mkdir -p {}'.format(self.__output_path))
        os.chdir('{}'.format(self.__output_path))
        Logger().info('\t' + cmd_line_run)
        # Executing command line.
        os.system(cmd_line_run)

    def set_output_path(self, parent_output_path):
        """Set BuildICM output_path.

        The BuildICM output_path is set from Glimmer's Output path.
        """
        self.__parent_output_path = parent_output_path
        self.__output_path = (parent_output_path +
                              ('/{}').format(self.NAME.lower()))
