# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the python shell
"""
__author__ = "rapidhere"
__all__ = ("main", )


def main() -> None:
    """
    the main entry for shell
    :return:
    """
    from . import cl
    cl.get_cl().main_loop()
