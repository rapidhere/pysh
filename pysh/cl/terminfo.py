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
import enum
from typing import Dict

from pysh.exp import TermInfoWrongType


# ~~~ some constants
class TerminfoKey(enum.Enum):
    unknown = 0
    new_line = 1
    return_key = 2
    backspace = 3


class Terminfo(object):
    """
    terminfo manager
    """
    _terminfo_default_map = {
        b'\010': TerminfoKey.backspace,
        b'\177': TerminfoKey.backspace,
        b'\n': TerminfoKey.new_line,
        b'\r': TerminfoKey.return_key,
    }

    _terminfo_control_map = {
        "kbs": TerminfoKey.backspace
    }

    def __init__(self):
        self._info_map: Dict[bytes, TerminfoKey] = self._terminfo_default_map.copy()

        # init info map
        for ctrl, t in self._terminfo_control_map.items():
            seq = get_bytes(ctrl)

            if seq:
                self._info_map[seq] = t

    def map_sequence(self, seq: bytes) -> TerminfoKey:
        """
        map a sequence to a terminfo key
        """
        return self._info_map.get(seq, TerminfoKey.unknown)


def init(term_name: str = None) -> None:
    """
    init term info
    :return:
    """
    if term_name is None:
        term_name = os.environ.get("TERM", "unknown")
    curses.setupterm(term_name, sys.stdout.fileno())


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
