# -*- coding: utf-8 -*-

"""Module containing CDS object with getter and setter of its attributes."""

import math


class CDS(object):
    """CDS Object contain all attribute of a given CDS result."""
    def __init__(self, idc, start, stop, orientation, tool, sequence_name=""):
        """Initialize all attribute of the CDS result.

        idc is a string containing the id of the cds result.
        start is an int containing CDS's begining position.
        stop is an int containing CDS's end position.
        orientation is an int which can be '+' or '-'. '+' for direct
        strand, '-' for reverse.
        tool is a string containing the tool's name which have given the
        CDS result.
        sequence_name is the sequence's name in which the CDS is located.
        """
        self.__id = idc
        self.__start = start
        self.__stop = stop
        self.__orient = orientation
        self.__tool = tool
        self.__sequence_name = sequence_name
        self.__conflict = False
        self.__score = 0
        self.__frame = math.fabs(self.__stop - self.__start) % 3

    def get_tool(self):
        """Return the CDS's tool's name."""
        return(self.__tool)

    def get_start(self):
        """Return the CDS's start position"""
        return(self.__start)

    def get_stop(self):
        """Return the CDS's stop position"""
        return(self.__stop)

    def get_orient(self):
        """Return the CDS's orientation"""
        return(self.__orient)

    def get_id(self):
        """Return the CDS's id."""
        return(self.__id)

    def get_conflict(self):
        """Return the CDS's conflict."""
        return(self.__conflict)

    def get_higher(self):
        """Return the higher position of the CDS on the direct strand."""
        return(max(self.__start, self.__stop))

    def get_lower(self):
        """Return the lower position of the CDS on the direct strand."""
        return(min(self.__start, self.__stop))

    def is_overlapping(self, interval, other_orient):
        """Return a boolean saying if there is overlapping."""
        return ((self.__start in interval or
                self.__stop in interval) and
                self.__orient == other_orient)

    def set_conflict(self, name):
        """Set the name of the other object with which there is overlapping."""
        self.__conflict = name

    def __repr__(self):
        """Return a string representing the line of the CDS result in
        gff file.
        """
        message = (self.__sequence_name + "\t" +
                   self.__tool + "\t" +
                   self.__class__.__name__ + "\t" +
                   self.__id + "\t" +
                   str(self.__start) + "\t" +
                   str(self.__stop) + "\t" +
                   str(self.__score) + "\t" +
                   self.__orient + "\t" +
                   str(self.__frame) + "\t" +
                   str(self.__conflict))
        return message
