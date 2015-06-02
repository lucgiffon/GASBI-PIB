# -*- coding: utf-8 -*-

"""Module Containing LongORFs class which check options, launch and parse
results of LongORFs software.
"""

import os

from tool.PreliminaryTool import PreliminaryTool
from util.Logger import Logger


class LongORFs(PreliminaryTool):
    """Check options and launch LongORFs software.

    Launch LongORFs with start().
    LongORFs inherit from PreliminaryTool.
    Static variables for LongORFs class are: OPTIONS_PROPERTIES, NAME
    """
    # Tool's Options, their type and their key for command line.
    OPTIONS_PROPERTIES = {'START_CODONS': {'typee': 'list', 'key': '-A'},
                          'ENTROPY_PATH': {'typee': 'str', 'key': '-E'},
                          'FIXED': {'typee': 'bool', 'key': '-f'},
                          'MIN_LEN': {'typee': 'int', 'key': '-g'},
                          'IGNORE_PATH': {'typee': 'str', 'key': '-i'},
                          'LINEAR': {'typee': 'bool', 'key': '-l'},
                          'LENGTH_OPT': {'typee': 'bool', 'key': '-L'},
                          'MAX_OLAP': {'typee': 'int', 'key': '-o'},
                          'CUTOFF': {'typee': 'float', 'key': '-t'},
                          'WITHOUT_STOPS': {'typee': 'bool', 'key': '-w'},
                          'TRANS_TABLE': {'typee': 'int', 'key': '-z'},
                          'STOP_CODONS': {'typee': 'list', 'key': '-Z'},
                          }
    # Name of the class.
    NAME = 'LongORFs'

    def __init__(self, general_options, LongORFs_options):
        """Initialize the LongORFs_options.

        Private Attributes:
        LongORFs_options is an OptionList which contain only LongORFs's 
        options.
        parent_output_path and output_path will be set later because the
        get_output_path method from Tool object is not right for 
        preliminary tools.
        """
        super(LongORFs, self).__init__(general_options)
        self.__LongORFs_options = LongORFs_options
        self.__parent_output_path = ''
        self.__output_path = ''

    def start(self):
        """Launches LongORFs software on command line."""
        # Root command line.
        # -n option for no header output.
        cmd_line_run = 'long-orfs -n'
        # Adding options to command Line
        cmd_line_run += self.load_command_line_options(self.__LongORFs_options)
        # Adding obligatory parameters at the end of command line.
        cmd_line_run += (' ' + self.general_options['SEQUENCE_PATH'])
        cmd_line_run += (' ' + self.general_options['TAG'] + '.longorfs.txt')
        # Create output directory and move into it.
        os.system('mkdir -p {}'.format(self.__output_path))
        os.chdir('{}'.format(self.__output_path))
        Logger().info('\t' + cmd_line_run)
        # Executing command line.
        os.system(cmd_line_run)

    def set_output_path(self, parent_output_path):
        """Set LongORFs output_path.

        The LongORFs output_path is set from Glimmer's Output path.
        """
        self.__parent_output_path = parent_output_path
        self.__output_path = (parent_output_path +
                              ('/{}').format(self.NAME.lower()))
