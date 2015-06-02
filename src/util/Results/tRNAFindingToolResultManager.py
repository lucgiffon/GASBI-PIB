# -*- coding: utf-8 -*-

"""This module contain tRNAFIndingToolResultManager class which will be used to
Manage the formatting and parsing of output files from tRNA Finding Tools.
"""

from util.Results.ResultManager import ResultManager
from util.Results.tRNAList import tRNAList


class tRNAFindingToolResultManager(ResultManager):
    """Check, set and parse results from tRNAFindingtool's output files."""
    def __init__(self, sequence_name=""):
        """Initialize ResultManager object.

        merged_trna_results will contain all tRNA found by all tRNA
        Finding Tools.
        The sequence_name contain the name of the sequence where the tRNAs
        have been found.
        """
        super(tRNAFindingToolResultManager, self).__init__()
        self.__merged_trna_results = tRNAList([])
        self.__sequence_name = sequence_name

    def merge_results(self):
        """Append merged_trna_results with tRNA results of each tools."""
        for result in self._results:
            self.__merged_trna_results.append(result)

    def sort(self):
        """Sort merged_trna_results with the start of each tRNA as key."""
        self.__merged_trna_results = tRNAList(sorted(self.__merged_trna_results,
                                                     key=lambda trna: trna.get_start()), self.__sequence_name)

    def check_conflict(self):
        """Verify if there is conflict in the merged_trna_results and set
        them.
        """
        i = 0
        # Dictionary containing all regions occuped by trnas.
        intervals = {}
        while i+1 < len(self.__merged_trna_results):
            # Index of the the current trna.
            i += 1
            # For each trna, define its orientation and range on the
            # direct strand.
            intervals[self.__merged_trna_results[i-1]] = (range(self.__merged_trna_results[i-1].get_lower(),
                                                                self.__merged_trna_results[i-1].get_higher()),
                                                          self.__merged_trna_results[i-1].get_orient())

            for trna in intervals:
                if self.__merged_trna_results[i].is_overlapping(intervals[trna][0],
                                                                intervals[trna][1]):
                    trna.set_conflict(self.__merged_trna_results[i].get_id())
                    self.__merged_trna_results[i].set_conflict(self.__merged_trna_results[i].get_id())

    def write_outfile(self):
        """Write Gasbi's tRNA's result file.gff."""
        o_file = open('tRNA.gff', 'w')
        o_file.write(str(self.__merged_trna_results))
        o_file.close()

    def __repr__(self):
        """Return a string representing the results merged if there is
        otherwise separated results.
        """
        if len(self.__merged_trna_results) != 0:
            returned = (str(self.__merged_trna_results))
        else:
            returned = ResultManager.__repr__(self)

        return (returned)
