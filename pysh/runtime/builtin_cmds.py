# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

some builtin commands
"""
__author__ = "rapidhere"

import sys

from .env import register_command


@register_command("exit")
def _exit():
    sys.exit(0)
