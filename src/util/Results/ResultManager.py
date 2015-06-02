# -*- coding: utf-8 -*-

"""This module contain ResultManager class which will be used to
Manage the formatting and parsing of output files.
"""


class ResultManager(object):
    """Check, set and parse results from tool's output files."""
    def __init__(self):
        """Create tool_objects and results lists.

        Tool_objects will be filled with a list of tool objects.
        results will be filled with a list of ResultList.
        """
        self.__tool_objects = []
        self._results = []

    def set_tools(self, tools):
        """Set tool_objects list.

        tools is a list of Tool objects.
        """
        self.__tool_objects = tools

    def check_output(self):
        """Check the integrity of the output files.

        An Exception will be raise if the file is wrong.
        """
        for tool in self.__tool_objects:
            tool.check_output()

    def parse_output(self):
        """parse_output load results from the output file."""
        for tool in self.__tool_objects:
            self._results.append(tool.parse_output())

    def merge_results(self):
        """Merge results from the same group of FindingTools.

        Abstract method.
        """
        pass

    def write_outfile(self):
        """Write GASBI's output file

        Abstract Method.
        """
        pass

    def check_conflict(self):
        """Verify if there is conflict in the merged_results and set them.

        Abstract Method.
        """

        pass

    def __repr__(self):
        """Return a string with the representation of each tool's results."""
        message = ""
        for tool in self._results:
            message += str(tool) + "\n\n"
        return (message.strip())
