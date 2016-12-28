# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

The cmd-line support class
"""
__author__ = "rapidhere"
__all__ = ("CommandLineInterface", "get")

import atexit
import curses

from pysh.runtime import get_env
from . import parser


class CommandLineInterface(object):
    """
    the command line interface
    """
    def __init__(self):
        self._screen = None
        self._buff: str = ''

    def prepare(self) -> None:
        """
        prepare to start the command line interface
        :return:
        """
        self._screen = curses.initscr()

        # ~~~ setup curses
        # don't echo chars
        curses.noecho()
        # react on any input
        curses.cbreak()

        # ~~~ setup screen
        # keypad, handle special sequences
        self._screen.keypad(True)

        # ~~~ restore before exit application
        atexit.register(self._on_exit)

    def main_loop(self) -> None:
        """
        start the cli main-loop
        :return:
        """
        self.prepare()

        while True:
            cmd_ivk = parser.parse_line(self._buff)
            get_env().invoke_command(cmd_ivk)

    @staticmethod
    def _on_exit() -> None:
        """
        do some clean on exit
        """
        curses.endwin()


# the interface singleton
_interface: CommandLineInterface = None


def get() -> CommandLineInterface:
    """
    get the interface singleton
    :return:
    """
    global _interface
    if _interface is None:
        _interface = CommandLineInterface()

    return _interface
