# -*- coding: utf-8 -*-

"""Module containing PreliminaryTool class"""

from tool.Tool import Tool


class PreliminaryTool(Tool):
    """PreliminaryTool inherit from Tool will be inherited by some tools

    Tools: BuildICM, LongORFs
    """
    def __init__(self, general_options):
        """Polymorphism PreliminaryTool -> Tool"""
        super(PreliminaryTool, self).__init__(general_options)
