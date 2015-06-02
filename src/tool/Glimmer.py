# -*- coding: utf-8 -*-

"""Module Containing Glimmer class which check options, launch and parse
results of Glimmer software.
"""

import os

from tool.CDSFindingTool import CDSFindingTool
from tool.BuildICM import BuildICM
from tool.Extract import Extract
from tool.LongORFs import LongORFs

from util.Logger import Logger

from util.Results.CDS import CDS
from util.Results.CDSList import CDSList


class Glimmer(CDSFindingTool):
    """Check options and launch Glimmer software.

    Launch Glimmer with start().
    Glimmer inherit from CDSFindingTool.
    Static variables for Glimmer class are: OPTIONS_PROPERTIES, NAME,
    PRELIMINARY_TOOLS.
    """
    # PRELIMINARY_TOOLS is sorted by order of activity.
    PRELIMINARY_TOOLS = ['Preliminary/{}/'.format(LongORFs.NAME),
                         'Preliminary/{}/'.format(Extract.NAME),
                         'Preliminary/{}/'.format(BuildICM.NAME)]
    # Tool's Options, their type and their key for command line.
    OPTIONS_PROPERTIES = {'IGNORE_PATH': {'type': 'str', 'key': '-i'},
                          'GENE_LEN': {'type': 'int', 'key': '-g'},
                          'ENTROPY_PATH': {'type': 'str', 'key': '-E'},
                          'TRANS_TABLE': {'type': 'int', 'key': '-z'},
                          'NO_INDEP': {'type': 'bool', 'key': '-r'},
                          'IGNORE_SCORE_LEN': {'type': 'int', 'key': '-q'},
                          'GC_PERCENT': {'type': 'float', 'key': '-C'},
                          'ICM_MODEL_PATH': {'type': 'str', 'key': None},
                          'LINEAR': {'type': 'bool', 'key': '-l'},
                          'ORF_COORDS_PATH': {'type': 'str', 'key': '-L'},
                          'FIRST_CODON': {'type': 'bool', 'key': '-f'},
                          'EXTEND': {'type': 'bool', 'key': '-X'},
                          'TRESHOLD': {'type': 'int', 'key': '-t'},
                          'MAX_OLAP': {'type': 'int', 'key': '-o'},
                          'START_CODONS': {'type': 'str', 'key': '-A'},
                          'STOP_CODON': {'type': 'str', 'key': '-Z'},
                          'RBS_PWN_PATH': {'type': 'str', 'key': '-b'},
                          'START_PROBS': {'type': 'str', 'key': '-P'},
                          }
    # Extension of the output file of interest.
    EXTENSION = 'predict'
    # Name of the class.
    NAME = 'Glimmer'

    def __init__(self, general_options, glimmer_options, preliminary_tools):
        """Initialize the glimmer_options and preliminary_tools_dict object.

        Private Attributes:
        glimmer_options is an OptionList which contain only Glimmer's options.
        preliminary-tools_dict is a dictionary which has glimmer's preliminary
        tools's names as keys and their options (OptionList) as values.
        """
        super(Glimmer, self).__init__(general_options)
        self.__glimmer_options = glimmer_options
        self.__preliminary_tools_dict = preliminary_tools

    def start(self):
        """Launches Glimmer software on command line.

        Preliminary tools are called into the method.
        """
        # Create output directory and move into it.
        os.system('mkdir -p {}'.format(self.get_output_path()))
        os.chdir('{}'.format(self.get_output_path()))
        # Calling Tool's method for launch preliminary tools.
        self.launch_preliminary_tools(self.PRELIMINARY_TOOLS,
                                      self.__preliminary_tools_dict)
        # Root command line.
        # There is no forced option for Glimmer.
        cmd_line_run = 'glimmer3'
        # Adding options to command Line
        cmd_line_run += self.load_command_line_options(self.__glimmer_options)
        # Modificating ICM_MODEL_PATH if user decided to let it set at
        # 'default'.
        if self.__glimmer_options['Basic/ICM_MODEL_PATH'] == 'default':
            self.__glimmer_options['Basic/ICM_MODEL_PATH'] = (self.get_output_path() +
                                                              '/' +
                                                              'buildicm' + '/' +
                                                              self.general_options['TAG'] +
                                                              '.icm.txt')
        # Adding obligatory parameters at the end of command line.
        cmd_line_run += (' ' + self.general_options['SEQUENCE_PATH'])
        cmd_line_run += (' ' +
                         self.__glimmer_options['Basic/ICM_MODEL_PATH'])
        cmd_line_run += (' ' + self.general_options['TAG'])
        # Save the command line.
        Logger().info('Glimmer command line: ' + cmd_line_run)
        # Moving into Glimmer's output directory.
        os.chdir('{}'.format(self.get_output_path()))
        # Executing command line.
        os.system(cmd_line_run)

        # Here is a way to deny Glimmer from writing in the standard output.
        # p = subprocess.Popen(['ls', '-a'], stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE)
        # out, err = p.communicate()
        # Modifying extensions of output Files.
        os.system('mv {}.predict {}.predict.txt'.format(self.general_options['TAG'],
                                                        self.general_options['TAG']))
        os.system('mv {}.detail {}.detail.txt'.format(self.general_options['TAG'],
                                                      self.general_options['TAG']))

    def parse_output(self):
        """Return CDSList Object containing Glimmer's results as CDS objects.

        The output file is parsed line after line thanks to the split method.
        """
        # Moving to Glimmer's Output directory
        os.chdir(self.get_output_path())
        results_file = open('{}.{}.txt'.format(self.general_options['TAG'],
                                               self.EXTENSION), 'r')
        # The sequence name is needed to instanciate CDS and CDSList.
        sequence_name = self.general_options['SEQUENCE_PATH'].strip("/ \n").split("/")[-1]
        glimmer_results = CDSList([], sequence_name, 'Glimmer')
        # Here, you can specify how many lines you want to parse.
        for line in results_file.readlines()[:50]:
            # The first line of each results contain the sequence name.
            if line[0] == '>':
                # We know sequence_name already yet.
                continue
            elif line.strip() != '':
                # Refer to the Glimmer's documentation to know how lines
                # are organized.
                cds_line = line.split()
                cds_id = cds_line[0]
                cds_start = int(cds_line[1])
                cds_stop = int(cds_line[2])
                if int(cds_line[3]) > 0:
                    cds_orient = '+'
                else:
                    cds_orient = '-'
                # Creating CDS Object for each line and appending CDSList.
                glimmer_results.append(CDS(cds_id, cds_start,
                                           cds_stop, cds_orient,
                                           self.NAME, sequence_name))
        results_file.close()
        return (glimmer_results)
