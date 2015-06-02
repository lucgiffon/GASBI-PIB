# -*- coding: utf-8 -*-

"""Module Containing GeneMark class which check options, launch and parse 
results of GeneMark software.
"""

import os

from tool.CDSFindingTool import CDSFindingTool

from util.Logger import Logger

from util.Results.CDS import CDS
from util.Results.CDSList import CDSList


class GeneMark(CDSFindingTool):
    """Check options and launch GeneMark software.

    Launch GeneMark with start().
    GeneMark inherit from CDSFindingTool.
    Static variables for GeneMark class are: OPTIONS_PROPERTIES, NAME,
    PRELIMINARY_TOOLS.
    """
    # There is no preliminary tool for GeneMark.
    PRELIMINARY_TOOLS = []
    # Tool's Options, their type and their key for command line.
    OPTIONS_PROPERTIES = {'WINDOW_SIZE': {'type': 'int', 'key': '-w'},
                          'A_PIORI_PROBABILITY': {'type': 'float', 'key': '-a'},
                          'STEP_SIZE': {'type': 'int', 'key': '-s'},
                          'MATRIX_PATH': {'type': 'str', 'key': '-m'},
                          'CODON_TRANSLATION_PATH': {'type': 'str', 'key': '-c'},
                          'TRESHOLD': {'type': 'float', 'key': '-t'},
                          'RBS_PATH': {'type': 'str', 'key': '-R'},
                          }
    # Some options have been disable. Refer to the configuration file.
    # Extension of the output file of interest.
    EXTENSION = 'ldata'
    # Name of the class.
    NAME = 'GeneMark'

    def __init__(self, general_options, genemark_options, preliminary_tools):
        """Initialize the GeneMark_options and preliminary_tools_dict object.

        Private Attributes:
        GeneMark_options is an OptionList which contain only GeneMark's
        options.
        preliminary-tools_dict is void for GeneMark but we need to instantiate
        it for generic functions.
        """
        super(GeneMark, self).__init__(general_options)
        self.__genemark_options = genemark_options
        self.__preliminary_tools_dict = preliminary_tools

    def start(self):
        """Launches GeneMark software on command line."""
        # Root command line.
        # -D option for DATA format
        # -l option for listing options
        # -v option for enable verbosity
        cmd_line_run = 'gm -D -l -g0 -r0 -o0 -v'
        # Adding options to command Line
        cmd_line_run += self.load_command_line_options(self.__genemark_options)
        # Adding obligatory parameters at the end of command line.
        cmd_line_run += ' ' + self.general_options['SEQUENCE_PATH']
        Logger().info('GeneMark command line: ' + cmd_line_run)
        # Executing command line.
        os.system(cmd_line_run)
        # Create output directory
        os.system('mkdir -p {}'.format(self.get_output_path()))
        # Moving output files into output directory.
        os.system('mv {}\.* {}'.format(self.general_options['SEQUENCE_PATH'],
                                       self.get_output_path()))
        # Moving into output directory.
        os.chdir('{}'.format(self.get_output_path()))
        # Modifying extensions of output Files.
        os.system('mv {}.lst {}.lst.txt'.format(self.general_options['SEQUENCE_PATH'].split('/')[-1],
                                                self.general_options['TAG']))
        os.system('mv {}.ldata {}.ldata.txt'.format(self.general_options['SEQUENCE_PATH'].split('/')[-1],
                                                    self.general_options['TAG']))

    def parse_output(self):
        """Return CDSList Object containing GeneMark's results as CDS objects.

        The output file is parsed line after line thanks to the split method.
        """
        # Moving to GeneMark's Output directory
        os.chdir(self.get_output_path())
        results_file = open('{}.{}.txt'.format(self.general_options['TAG'],
                                               self.EXTENSION), 'r')
        # The sequence name is needed to instanciate CDS and CDSList.
        sequence_name \
            = self.general_options['SEQUENCE_PATH'].strip("/ \n").split("/")[-1]
        genemark_results = CDSList([], sequence_name, 'GeneMark')
        cds_no = 0
        # Here, you can specify how many lines you want to parse.
        for line in results_file.readlines()[:50]:
            # Refer to the GeneMark's documentation to know how lines
            # are organized.
            if line.strip() == '#Frameshift Report':
                break
            elif line[0] == '#':
                continue
            elif line.strip() != '':
                cds_no += 1
                cds_line = line.split()
                cds_id = "orf" + str(cds_no)
                if int(cds_line[2]) <= 3:
                    cds_orient = '+'
                    cds_start = int(cds_line[0])
                    cds_stop = int(cds_line[1])
                else:
                    cds_orient = '-'
                    cds_start = int(cds_line[1])
                    cds_stop = int(cds_line[0])
                # Creating CDS Object for each line and appending CDSList.
                genemark_results.append(CDS(cds_id, cds_start,
                                            cds_stop, cds_orient,
                                            'GeneMark', sequence_name))
        results_file.close()
        return (genemark_results)
