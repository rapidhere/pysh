# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

The cmd-line support class
"""
__author__ = "rapidhere"
__all__ = ("CommandLineInterface", "get")

import atexit
import codecs
import copy
import os
import sys
import termios

from . import terminfo
from .terminfo import Key


class CommandLineInterface(object):
    """
    the command line interface

    TODO: unicode support is on the way
    """
    def __init__(self):
        # TODO: set encoding
        self._decoder = codecs.getincrementaldecoder("gbk")()
        # decoded string
        self._buff: str = ""

        # stored old terminal attr
        self._old_term_attr = None

        self._input_fd = sys.stdin.fileno()
        self._output_fd = sys.stdout.fileno()

        # last buff len
        self._last_buff_len = 0
        self._on_erase = False

        # prompt len
        self._prompt_len = 0

        # parser
        from . import parser
        self.lparser = parser

    @property
    def env(self):
        """
        get env
        :return:
        """
        from pysh.runtime import get_env
        return get_env()

    def prepare(self) -> None:
        """
        prepare to start the command line interface
        :return:
        """
        # ~~~ init term info
        terminfo.init()

        # ~~~ setup tty
        self._setup_tty()

        # ~~~ restore before exit application
        atexit.register(self._on_exit)

    def main_loop(self) -> None:
        """
        start the cli main-loop
        :return:
        """
        self.prepare()

        while True:
            # display prompt
            self._display_prompt()

            # handle input
            self._handle_input()

            cmd_ivk = self.lparser.parse_line(self._buff)
            res = self.env.invoke_command(cmd_ivk)

            res.display(self)
            self.cr_down()

    def put_string(self, string: str) -> None:
        """
        put a string to terminal
        :return:
        """
        # TODO: byte encoding
        self.put(string.encode("gbk"))

    def put(self, data: bytes) -> None:
        """
        put some data into terminal
        :return:
        """
        os.write(self._output_fd, data)

    def cr_up(self, dt: int = 1) -> None:
        """
        move cursor up
        :return:
        """
        self.put(terminfo.pack("cuu", dt))

    def cr_down(self, dt: int = 1) -> None:
        """
        move cursor down
        :return:
        """
        self.put(terminfo.pack("cud", dt))

    def cr_left(self, dt: int = 1) -> None:
        """
        move cursor left
        :return:
        """
        self.put(terminfo.pack("cub", dt))

    def cr_right(self, dt: int = 1) -> None:
        """
        move cursor right
        :return:
        """
        self.put(terminfo.pack("cuf", dt))

    def erase(self, num: int = 1) -> None:
        """
        erase char at current location
        :return:
        """
        self.put(terminfo.pack("ech", num))

    def _display_prompt(self) -> None:
        """
        display the prompt
        :return:
        """
        # put cursor
        # TODO: tricky
        self.cr_left(1000)

        prompt = self.env.prompt
        prompt_len = len(prompt)

        self.put_string(prompt)
        self._prompt_len = prompt_len

    def _handle_input(self) -> None:
        """
        handle input, input will put in self._buff
        :return:
        """
        # clear buff
        self._buff = ""
        self._decoder.reset()
        self._last_buff_len = 0

        while True:
            b = os.read(self._input_fd, 1)

            if b in (Key.NEW_LINE, Key.RETURN):
                self._buff += self._decoder.decode(b'', final=True)
                break
            elif b in (Key.BACKSPACE, Key.BACKSPACE_2):
                if len(self._buff) > 0:
                    self._buff = self._buff[:-1]
                    self._on_erase = True
            else:
                self._on_erase = False
                self._buff += self._decoder.decode(b)

            # refresh buff display
            self._display_buff()
            self._last_buff_len = len(self._buff)

        # refresh buff display
        self._display_buff()
        self._last_buff_len = len(self._buff)

        # put cursor
        self.cr_left(self._last_buff_len + self._prompt_len)
        self.cr_down()

    def _display_buff(self) -> None:
        """
        display buff content
        :return:
        """
        self.cr_left(self._last_buff_len)
        self.put_string(self._buff)

        # erase last char on need
        if self._on_erase:
            self.erase()

    def _setup_tty(self) -> None:
        """
        setup tty
        :return:
        """
        attr = termios.tcgetattr(self._input_fd)
        # store attr for recover usage
        self._old_term_attr = copy.deepcopy(attr)

        # setup input flags
        attr[0] &= ~(
            termios.BRKINT      # disable break flush
            | termios.ICRNL     # disable nl-cr translate
            | termios.INPCK     # disable parity check
            | termios.ISTRIP    # disable eight bit strip
            | termios.IXON)     # disable xon flow control

        # setup output flags
        # disable all
        attr[1] = 0

        # setup control flags
        attr[2] &= ~(
            termios.CSIZE       # redefine c-size
            | termios.PARENB)   # disable parity check
        attr[2] |= termios.CS8  # set control size to CS8

        # setup local flags
        attr[3] &= ~(
            termios.ECHO        # disable echo
            | termios.ECHONL    # disable newline
            | termios.ICANON    # disable canonical mode
            | termios.IEXTEN    # disable implementation-defined input processing
            | termios.ISIG)     # disable signals

        # setup cc attributes
        attr[6][termios.VMIN] = 1   # read up 1 char at least
        attr[6][termios.VTIME] = 0  # timeout is 0

        # setup now
        termios.tcsetattr(self._input_fd, termios.TCSANOW, attr)

    def _on_exit(self) -> None:
        """
        do some clean on exit
        """
        if self._old_term_attr is not None:
            termios.tcsetattr(
                self._input_fd, termios.TCSADRAIN, self._old_term_attr)


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
