# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

some exceptions
"""
__author__ = "rapidhere"


class PyShellException(Exception):
    """
    base py shell exception
    """
    pass


class TermInfoException(PyShellException):
    """
    exceptions happened when getting term info
    """
    pass


class TermInfoWrongType(TermInfoException):
    """
    term info is not specified type
    """
    def __init__(self, name: str, _type: type):
        TermInfoException.__init__(
            self, f"cap name `{name}` is not of type `{_type}`")


class ArgumentError(PyShellException):
    """
    Argument error
    """
    def __init__(self, *args, **kwargs):
        PyShellException.__init__(self, *args, **kwargs)
