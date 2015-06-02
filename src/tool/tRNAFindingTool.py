# -*- coding: utf-8 -*-

"""Module containing tRNAFindingTool class"""

from tool.Tool import Tool


class tRNAFindingTool(Tool):
    """tRNAFindingTool inherit from Tool will be inherited by some tools

    Tools:"""
    def __init__(self, general_options):
        """Polymorphism tRNAFindingTool -> Tool"""
        super(tRNAFindingTool, self).__init__(general_options)

    def get_group(self):
        return ("tRNAFindingTool")
