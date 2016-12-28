# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the command line supports
"""
__author__ = "rapidhere"

# check curses support
try:
    import curses as unused
except ImportError:
    raise ImportError("lib curses is not supported in this environment")

from .cmdline import get as get_cl
