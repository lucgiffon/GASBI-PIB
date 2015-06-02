# -*- coding: utf-8 -*-

"""Module containing the Constant class."""

from tool.Glimmer import Glimmer
from tool.GeneMark import GeneMark
from tool.TRNAScan import TRNAScan


class Constant(object):
    """Constant contain all constant and global variables for GASBI."""
    TOOLS_LIST = ['CDSFindingTool/{}/'.format(Glimmer.NAME),
                  'CDSFindingTool/{}/'.format(GeneMark.NAME),
                  'TRNAFindingTool/{}/'.format(TRNAScan.NAME),
                  ]
