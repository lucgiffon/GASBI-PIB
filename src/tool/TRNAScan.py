# -*- coding: utf-8 -*-

"""Module Containing TRNAScan class which check options, launch and parse
results of TRNAScan software.
"""

import os

from tool.tRNAFindingTool import tRNAFindingTool

from util.Logger import Logger

from util.Results.tRNAList import tRNAList
from util.Results.tRNA import tRNA


class TRNAScan(tRNAFindingTool):
    """Check options and launch TRNAScan software.

    Launch TRNAScan with start().
    TRNAScan inherit from tRNAFindingTool.
    Static variables for TRNAScan class are: OPTIONS_PROPERTIES, NAME,
    PRELIMINARY_TOOLS.
    """
    # There is no preliminary tool for TRNAScan.
    PRELIMINARY_TOOLS = []
    # Tool's Options, their type and their key for command line.
    OPTIONS_PROPERTIES = {'SEARCH_PROKARYOTIC': {'type': 'bool', 'key': '-B'},
                          'SEARCH_ARCHAEAL': {'type': 'bool', 'key': '-A'},
                          'SEARCH_ORGANELLAR': {'type': 'bool', 'key': '-O'},
                          'USE_GENERAL_MODEL': {'type': 'bool', 'key': '-G'},
                          'COVE_ANALYSIS': {'type': 'bool', 'key': '-C'},
                          'SHOW_BOTH_STRUCTURE': {'type': 'bool', 'key': '-H'},
                          'DISABLE_PSEUDOGENE_CHECKING': {'type': 'bool', 'key': '-D'},
                          'COVE_CUTOFF_SCORE': {'type': 'float', 'key': '-X'},
                          'LENGTH': {'type': 'int', 'key': '-L'},
                          'INTERMEDIATE_CUTOFF_SCORE': {'type': 'float', 'key': '-I'},
                          'NUMBER_NUCLEOTIDES_PADDING': {'type': 'int', 'key': '-B'},
                          'ALTERNATE_GENETIC_CODE_PATH': {'type': 'str', 'key': '-g'},
                          'ALTERNATE_COVARIANCE_MODEL': {'type': 'str', 'key': '-c'},
                          'SEQUENCES_NAME': {'type': 'str', 'key': '-n'},
                          'SEQUENCE_NAME_AND_CONTINUE': {'type': 'str', 'key': '-s'},
                          'TRNASCAN_ONLY': {'type': 'bool', 'key': '-T'},
                          'SEARCH_MODE': {'type': 'str', 'key': '-t'},
                          }
    # Some options have been disable. Refer to the configuration file.
    # Extension of the output file of interest.
    EXTENSION = 'out'
    # Name of the class.
    NAME = 'TRNAScan'

    def __init__(self, general_options, TRNAScan_options, preliminary_tools):
        """Initialize the TRNAScan_options and preliminary_tools_dict object.

        Private Attributes:
        TRNAScan_options is an OptionList which contain only TRNAScan's options.
        preliminary-tools_dict is void for TRNAScan but we need to instantiate
        it for generic functions.
        """
        super(TRNAScan, self).__init__(general_options)
        self.__TRNAScan_options = TRNAScan_options
        self.__preliminary_tools = preliminary_tools

    def start(self):
        """Launches TRNAScan software on command line."""
        # Create output directory and move into it.
        os.system('mkdir -p {}'.format(self.get_output_path()))
        os.chdir('{}'.format(self.get_output_path()))
        # Root command line.
        # -b option for no header output. Necessary to parse output
        # -p option for modify default '#' label
        # -o option for write output
        cmd_line_run = 'tRNAscan-SE -b -p{} -o#'.format(self.general_options['TAG'])
        # Adding options to command Line
        cmd_line_run += self.load_command_line_options(self.__TRNAScan_options)
        # Adding obligatory parameters at the end of command line.
        cmd_line_run += ' ' + self.general_options['SEQUENCE_PATH']
        Logger().info('tRNAScan command line: ' + cmd_line_run)
        # Executing command line.
        os.system(cmd_line_run)
        # Modifying extensions of output Files.
        os.system('mv {}.out {}.out.txt'.format(self.general_options['TAG'],
                                                self.general_options['TAG']))

    def parse_output(self):
        """Return tRNAList Object containing TRNAScan's results as tRNA objects.

        The output file is parsed line after line thanks to the split method.
        """
        # Moving to TRNAScan's Output directory
        os.chdir(self.get_output_path())
        results_file = open('{}.{}.txt'.format(self.general_options['TAG'],
                                               self.EXTENSION), 'r')
        # The sequence name is needed to instanciate tRNA and tRNAList.
        sequence_name = self.general_options['SEQUENCE_PATH'].strip("/ \n").split("/")[-1]
        trnascan_results = tRNAList([], sequence_name, 'TRNAScan')
        # Here, you can specify how many lines you want to parse.
        for line in results_file.readlines()[:50]:
            # Refer to the TRNAScan's documentation to know how lines
            # are organized.
            if line[0] == '>':
                continue
            elif line.strip() != '':
                trna_line = line.split()
                trna_id = 'trna' + trna_line[1]
                trna_start = int(trna_line[2])
                trna_stop = int(trna_line[3])
                if trna_start < trna_stop:
                    trna_orient = '+'
                else:
                    trna_orient = '-'
                trna_aa = trna_line[4]
                trna_ac = trna_line[5]
                # Creating tRNA Object for each line and appending tRNAList.
                trnascan_results.append(tRNA(trna_id, trna_start, trna_stop,
                                             trna_orient, trna_aa, trna_ac,
                                             'TRNAScan', sequence_name))
        results_file.close()
        return (trnascan_results)
