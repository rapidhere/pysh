# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the cmdline parser
"""
__author__ = "rapidhere"
__all__ = ("parse_line", )


from pysh.runtime.cmdobj import CommandInvoke


def parse_line(line: str) -> CommandInvoke:
    """
    parse the line and return the command
    :param line: the line to parse
    :return: the parsed command
    """
    args = list(filter(lambda s: s, line.strip().split()))

    return CommandInvoke(args[0], *args[1:])
