# -*- coding: utf-8 -*-

"""Module Containing Extract class which check options, launch and parse 
results of Extract software.
"""

import os

from tool.PreliminaryTool import PreliminaryTool
from util.Logger import Logger


class Extract(PreliminaryTool):
    """Check options and launch Extract software.

    Launch Extract with start().
    Extract inherit from PreliminaryTool.
    Static variables for Extract class are: OPTIONS_PROPERTIES, NAME
    """
    # Tool's Options, their type and their key for command line.
    OPTIONS_PROPERTIES = {'INPUT_FILE_PATH': {'typee': 'str', 'key': None},
                          'MINLEN': {'typee': 'int', 'key': '-l'},
                          'NO_START': {'typee': 'bool', 'key': '-s'},
                          'NO_STOP': {'typee': 'bool', 'key': '-t'},
                          'NO_WRAP': {'typee': 'bool', 'key': '-w'},
                          'DIR': {'typee': 'bool', 'key': 'd'},
                          }
    # Name of the class.
    NAME = 'Extract'

    def __init__(self, general_options, extract_options):
        """Initialize the Extract_options.

        Private Attributes:
        Extract_options is an OptionList which contain only Extract's
        options.
        parent_output_path and output_path will be set later because the
        get_output_path method from Tool object is not right for
        preliminary tools.
        """
        super(Extract, self).__init__(general_options)
        self.__extract_options = extract_options
        self.__parent_output_path = ''
        self.__output_path = ''

    def start(self):
        """Launches Extract software on command line."""
        # Root command line.
        cmd_line_run = 'extract'
        # Adding options to command Line
        cmd_line_run += self.load_command_line_options(self.__extract_options)
        # Modificating INPUT_FILE_PATH if the user set it to default
        if self.__extract_options['Basic/INPUT_FILE_PATH'] == 'default':
            self.__extract_options['Basic/INPUT_FILE_PATH'] = (self.__parent_output_path +
                                                               '/' +
                                                               'longorfs' + '/' +
                                                               self.general_options['TAG'] +
                                                               '.longorfs.txt')
        # Adding obligatory parameters at the end of command line.
        cmd_line_run += (' ' + self.general_options['SEQUENCE_PATH'])
        cmd_line_run += (' ' + self.__extract_options['Basic/INPUT_FILE_PATH'])
        cmd_line_run += (' > ' + self.general_options['TAG'] + '.train.txt')
        # Create output directory and move into it.
        os.system('mkdir -p {}'.format(self.__output_path))
        os.chdir('{}'.format(self.__output_path))
        Logger().info('\t' + cmd_line_run)
        # Executing command line.
        os.system(cmd_line_run)

    def set_output_path(self, parent_output_path):
        """Set Extract output_path.

        The Extract output_path is set from Glimmer's Output path.
        """
        self.__parent_output_path = parent_output_path
        self.__output_path = (parent_output_path +
                              ('/{}').format(self.NAME.lower()))
