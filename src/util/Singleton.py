# -*- coding: utf-8 -*-

"""Module containing singleton decorator for creating singleton classes"""


def singleton(classe):
    """This decorator permit to get only one object for each decorated class"""
    instances = {}

    def get_instance():
        if classe not in instances:
            instances[classe] = classe()
        return instances[classe]
    return get_instance
