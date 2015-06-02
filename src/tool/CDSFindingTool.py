# -*- coding: utf-8 -*-

"""Module containing CDSFindingTool class"""

from tool.Tool import Tool


class CDSFindingTool(Tool):
    """CDSFindingTool inherit from Tool will be inherited by some tools

    Tools: Glimmer, GeneMark
    """
    def __init__(self, general_options):
        """Polymorphism CDSFindingTool -> Tool"""
        super(CDSFindingTool, self).__init__(general_options)

    def get_group(self):
        return ("CDSFindingTool")
