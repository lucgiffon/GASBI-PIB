# -*- coding: utf-8 -*-

"""This module Contain CDSList class which will be used to contain
CDS objects.
"""

from util.Results.CDS import CDS


class CDSList(object):
    """CDSList allow to manipulate CDS objects together"""
    def __init__(self, results, sequence_name="", tool='CDS'):
        """Initialize results, tool and sequence_name.

        Results Contain a List of CDS Objects.
        results will be filled with the append method.
        """
        self.__results = results
        self.__tool = tool
        self.__sequence_name = sequence_name

    def append(self, new):
        """Append new to the results list."""
        if isinstance(new, CDSList):
            self.__results += new.get_results_list()
        elif isinstance(new, CDS):
            self.__results.append(new)

    def get_results_list(self):
        """Return the results List."""
        return (self.__results)

    def __len__(self):
        """Return the length of the results List."""
        return(len(self.__results))

    def __iter__(self):
        """Return the iterable of the results List."""
        return(iter(self.__results))

    def __getitem__(self, n):
        """Return the item number n of the results List."""
        return(self.__results[n])

    def __repr__(self):
        """Return a string representation of the results List in gff format."""
        message = "# "
        message += ("sequence" + "\t" +
                    "tool" + "\t" +
                    "type" + "\t" +
                    "id" + "\t" +
                    "start" + "\t" +
                    "stop" + "\t" +
                    "score" + "\t" +
                    "orient" + "\t" +
                    "frame" + "\t" +
                    "conflict")
        for result in self.__results:
            message += "\n" + str(result)
        return (message + "\n")
