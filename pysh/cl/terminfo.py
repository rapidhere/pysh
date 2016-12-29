# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the term info support
"""
__author__ = "rapidhere"
__all__ = ("init", "get_flag", "get_bytes", "get_int")

import curses
import os
import sys

from pysh.exp import TermInfoWrongType


# ~~~ some constants
class Key(object):
    NEW_LINE = b'\n'
    RETURN = b'\r'
    BACKSPACE = b'\b'

    # ~~~ init by curses
    BACKSPACE_2 = None


def init(term_name: str = None) -> None:
    """
    init term info
    :return:
    """
    if term_name is None:
        term_name = os.environ.get("TERM", "unknown")
    curses.setupterm(term_name, sys.stdout.fileno())

    # init keys
    Key.BACKSPACE_2 = get_bytes("kbs")


def get_flag(name: str, default: bool = False) -> bool:
    """
    get as a flag
    :return:
    """
    ret = curses.tigetflag(name)
    if ret == -1:
        raise TermInfoWrongType(name, bool)

    if ret == 0:
        return default
    return ret


def get_int(name: str, default: int = None) -> int:
    """
    get as a int
    :return:
    """
    ret = curses.tigetnum(name)
    if ret == -2:
        raise TermInfoWrongType(name, int)

    if ret == -1:
        return default
    return ret


def get_bytes(name: str, default: bytes = None) -> bytes:
    """
    get as a string
    will not raise TermInfoWrongType
    """
    ret = curses.tigetstr(name)
    if ret is None:
        return default

    return ret


def pack(name: str, *args) -> bytes:
    """
    pack a term info command
    """
    return curses.tparm(curses.tigetstr(name), *args)
