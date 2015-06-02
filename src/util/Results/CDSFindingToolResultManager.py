# -*- coding: utf-8 -*-

"""This module contain CDSFIndingToolResultManager class which will be used to
Manage the formatting and parsing of output files from CDS Finding Tools.
"""

from util.Results.ResultManager import ResultManager
from util.Results.CDSList import CDSList


class CDSFindingToolResultManager(ResultManager):
    """Check, set and parse results from CDSFindingtool's output files."""
    def __init__(self, sequence_name=""):
        """Initialize ResultManager object.

        merged_CDS_results will contain all CDS found by all CDS
        Finding Tools.
        The sequence_name contain the name of the sequence where the CDSs
        have been found.
        """
        super(CDSFindingToolResultManager, self).__init__()
        self.__merged_cds_results = CDSList([])
        self.__sequence_name = sequence_name

    def merge_results(self):
        """Append merged_CDS_results with CDS results of each tools."""
        for result in self._results:
            self.__merged_cds_results.append(result)

    def sort(self):
        """Sort merged_CDS_results with the start of each CDS as key."""
        self.__merged_cds_results = CDSList(sorted(self.__merged_cds_results,
                                                   key=lambda cds: cds.get_start()),
                                            self.__sequence_name)

    def check_conflict(self):
        """Verify if there is conflict in the merged_cds_results and
        set them.
        """
        i = 0
        # Dictionary containing all regions occuped by cdss.
        intervals = {}
        while i+1 < len(self.__merged_cds_results):
            # Index of the the current cds.
            i += 1
            # For each cds, define its orientation and range on the
            # direct strand.
            intervals[self.__merged_cds_results[i-1]] = (range(self.__merged_cds_results[i-1].get_lower(),
                                                               self.__merged_cds_results[i-1].get_higher()),
                                                         self.__merged_cds_results[i-1].get_orient())

            for cds in intervals:
                if self.__merged_cds_results[i].is_overlapping(intervals[cds][0],
                                                               intervals[cds][1]):
                    cds.set_conflict(self.__merged_cds_results[i].get_id())
                    self.__merged_cds_results[i].set_conflict(self.__merged_cds_results[i].get_id())

    def write_outfile(self):
        """Write Gasbi's CDS's result file.gff."""
        o_file = open('CDS.gff', 'w')
        o_file.write(str(self.__merged_cds_results))
        o_file.close()

    def __repr__(self):
        """Return a string representing the results merged if there is
        otherwise separated results.
        """
        if len(self.__merged_cds_results) != 0:
            returned = (str(self.__merged_cds_results))
        else:
            returned = ResultManager.__repr__(self)

        return (returned)
