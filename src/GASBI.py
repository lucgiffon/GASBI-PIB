# -*- coding: utf-8 -*-

"""Main created by Luc Giffon on 26.3.15.

This module contain the main class Gasbi and the main function which
organize all steps of the process.
"""

import os
import time

from util.Constant import Constant
from util.Logger import Logger

from tool.Glimmer import Glimmer
from tool.GeneMark import GeneMark
from tool.BuildICM import BuildICM
from tool.Extract import Extract
from tool.LongORFs import LongORFs
from tool.TRNAScan import TRNAScan

from util.Options.OptionManager import OptionManager

from util.Results.tRNAFindingToolResultManager import tRNAFindingToolResultManager
from util.Results.CDSFindingToolResultManager import CDSFindingToolResultManager


class Gasbi(object):
    """Organize the processes by calling sub-managers which will do specific tasks.

    Parse configuration file with parse_options().
    Launch tools with launch_tools().
    Parse output files of each tools with parse_results().
    Analyze results of each group of FindingTools with perform_analysis().
    """
    def __init__(self, config_file):
        """Initialize sub-managers and configuration file name.

        Private attributes:
        config_file is the path (string) to find the configuration file
        from current directory.
        tool_objects is a dictionary which will contain group of finding
        tools as keys and tool objects lists as items. It is filled with
        launch_tools().
        option_manager is an OptionManager object which will manage the
        parsing of configuration file and hold options. It is filled with
        parse_options().
        results_manager is a dictionary which will contain group of finding
        tools as keys and ResultManager objects as items. They will
        manage the parsing of output file for each tool. It is filled
        with parse_results().
        """
        self.__config_file = config_file
        self.__option_manager = OptionManager()
        self.__tool_objects = {}
        self.__result_managers = {}

    def parse_options(self):
        """Make the option_manager load and check options from
        configuration file.
        """
        Logger().info('Loading Options from ' +
                      'configuration file {}'.format(self.__config_file))
        # Load options from config_file. The verification of the integrity
        # of the configuration file is done just before setting.
        self.__option_manager.set_options(self.__config_file)
        Logger().info("\tOptions setted.")
        # Verify option's quality.
        self.__option_manager.check_options()
        Logger().info("\tOptions checked and validated.")

    def launch_tools(self):
        """Launch each tool and filling the tool objects dictionary."""
        # Load options used by all tools.
        all_options = self.__option_manager.get_options()
        general_options = all_options['General']
        Logger().debug('General options: ' + str(all_options))
        if all_options['General/TAG'] == 'default':
            all_options['General/TAG']\
                = general_options['SEQUENCE_PATH'].split('/')[-1].split('.')[-2]
        Logger().debug('General options: ' + str(all_options['General/TAG']))
        # Moving into output directory
        Logger().info("Moving to Output Directory...")
        os.chdir(all_options['General/OUT_PATH'])
        Logger().info("done")
        # If it doesn't exist, create output directory
        Logger().info("Creating Output Directory...")
        os.system('mkdir -p {}'.format(all_options['General/TAG']))
        Logger().info("done")
        # Launching tools one by one and come back into base directory.
        for tool in Constant.TOOLS_LIST:
            Logger().debug(tool)
            if tool[-1] != '/':
                tool_object_name = tool.split('/')[-1]
            else:
                tool_object_name = tool.split('/')[-2]
            # Standing on output directory.
            os.chdir(all_options['General/OUT_PATH'] + '/' +
                     all_options['General/TAG'])
            Logger().info("Launching {}...".format(tool_object_name))
            # Do preliminary steps for each software.
            preliminary_tools = {}
            # Verify then load preliminary tools.
            for pre_tool in eval(tool_object_name).PRELIMINARY_TOOLS:
                # Load preliminary tool's options.
                preliminary_options = all_options[pre_tool]
                # Load preliminary tool's name.
                preliminary_tool_object_name \
                    = '{}'.format(pre_tool.split('/')[-2])
                Logger().\
                    debug(('Preliminary tool: {} ' +
                          '| Options: {}').format(preliminary_tool_object_name,
                                                  preliminary_options))
                # Instanciate preliminary tool.
                preliminary_tools[preliminary_tool_object_name] \
                    = eval(preliminary_tool_object_name)(general_options,
                                                         preliminary_options)
            # Get principal tool's options back.
            tool_options = all_options[tool]
            Logger().debug('Tool: {} | Options: {}'.format(tool_object_name,
                                                           tool_options))
            # Instanciate main tool.
            tool_object = eval('{}'.format(tool_object_name))(general_options,
                                                              tool_options,
                                                              preliminary_tools)
            # Launch main tool.
            tool_object.start()
            # Filling tool_objects dictionary
            group_name = tool_object.get_group()
            if group_name not in self.__tool_objects:
                self.__tool_objects[group_name] = [tool_object]
            else:
                self.__tool_objects[group_name].append(tool_object)
            Logger().info("{} done".format(tool_object_name))

    def parse_results(self):
        """Parse output files thanks to the tool objects dictionary."""
        all_options = self.__option_manager.get_options()
        sequence_path = all_options['General/SEQUENCE_PATH']
        sequence_name = sequence_path.strip("/ \n").split("/")[-1]
        for group in self.__tool_objects.keys():
            # Setting tool objects to each group's result manager and
            # instanciate them.
            self.__result_managers[group] = \
                eval("{}ResultManager".format(group))(sequence_name)
            self.__result_managers[group].set_tools(self.__tool_objects[group])
            # Checking the integrity of output file
            Logger().info("Checking {}'s output files...".format(group))
            # Actually calling CDSFindingToolResultManager or tRNA etc..
            self.__result_managers[group].check_output()
            Logger().info("{} done".format(group))
        for group in self.__result_managers.keys():
            # Parsing the output file
            Logger().info("Parsing {}'s output files...".format(group))
            # Actually calling CDSFindingToolResultManager or tRNA etc..
            self.__result_managers[group].parse_output()
            Logger().info("{} done".format(group))

    def perform_analysis(self):
        """Build lists containing all cds or trna."""
        # For each tool group.
        for group in self.__result_managers.keys():
            # Fill the merged list of the element searched
            self.__result_managers[group].merge_results()
            self.__result_managers[group].sort()
            self.__result_managers[group].check_conflict()

    def write_outfile(self):
        """write the outfiles in output+tag directory"""
        out_path = self.__option_manager.get_options()['General/OUT_PATH']
        out_path = out_path.rstrip("/ ") + "/"
        tag = self.__option_manager.get_options()['General/TAG']
        output_dir = out_path + tag
        os.chdir(output_dir)
        for group in self.__result_managers.keys():
            self.__result_managers[group].write_outfile()

if __name__ == '__main__':
    try:
        # Allow to calculate the processing time.
        begin_time = time.time()
        # Define log level. It will be specified by command line.
        verbosity = 3
        # Define configuration file. It will be specified by command line.
        config_file = 'configuration_file'
        # Instanciate the Logger singleton.
        Logger().set_verbosity(verbosity)
        # Instanciate the Gasbi tool with configuration file.
        manager = Gasbi(config_file)
        # Checking the integrity of configuration file.
        # Loading Options.
        # Checking if options are correct (type, existence, path..).
        manager.parse_options()
        # Launch tools which will launch preliminaries if necessary.
        manager.launch_tools()
        # Checking the integrity of results.
        # Loading results.
        manager.parse_results()
        # Merge results from the same group and sort them.
        manager.perform_analysis()
        # Write GASBI's output files.
        manager.write_outfile()
        finish_time = time.time()
        # Evaluate processing time
        processing_time = finish_time - begin_time
        Logger().info("Gasbi took %.2f seconds to run." % (processing_time))
    except:
        exit()
