# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

some builtin commands
"""
__author__ = "rapidhere"

import sys

from pysh.runtime.gentarg import Integer, String
from pysh.runtime.util import gent


@gent("exit")
def _exit(
        exit_code: Integer(-255, 255, "exit code to return", optional=True) = 0):
    sys.exit(exit_code)


@gent("echo")
def echo(content: String("content to display", optional=True) = ""):
    return content
