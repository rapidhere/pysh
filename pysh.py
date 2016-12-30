# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the shell entry
"""
__author__ = "rapidhere"

import contextlib

import pysh


@contextlib.contextmanager
def toggle_remote_debug():
    """
    for remote debug usage only

    NOTE: Using jetbrains' python remote debug util
          for remote debug, please copy pycharm-debug-py3k.egg
          to the root of project.

          For complete remote debugging steps, please refer to pycharm's
          remote debugging documentation.

          Then start shell with `pysh.py --remote-debug`, `--remote-debug must be first argument`
    :return:
    """
    import sys
    import os

    debug_on = len(sys.argv) >= 2 and '--remote-debug' in sys.argv[1]

    if debug_on:
        egg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "pycharm-debug-py3k.egg"))
        sys.path.append(egg_path)
        import pydevd
        pydevd.settrace('localhost', port=9090)

    yield

    if debug_on:
        import pydevd
        pydevd.stoptrace()


if __name__ == "__main__":
    with toggle_remote_debug():
        pysh.main()
