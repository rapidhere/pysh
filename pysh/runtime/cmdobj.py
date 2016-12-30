# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the cmd objects
"""
__author__ = "rapidhere"

from typing import Dict

from pysh.cl.cmdline import CommandLineInterface
from pysh.exp import ArgumentError
from .gentarg import GentArgument


class InvokeError(object):
    """
    a invoke error
    """
    def __init__(self, error):
        self.error = error

    def display(self, cl: CommandLineInterface):
        cl.put_string(str(self.error) + "\n")


class NoSuchCommandInvokeError(InvokeError):
    """
    no such command
    """
    def __init__(self, command: str):
        InvokeError.__init__(self, f"no such command `{command}`")
        self.command = command


class InternalErrorInvokeResult(InvokeError):
    """
    the internal error invoke result
    """
    def __init__(self, exception: Exception):
        InvokeError.__init__(
            self, f"pysh internal error: {str(exception)}")


class Command(object):
    """
    a command object
    """
    def invoke(self, args, kwargs):
        """
        invoke the command
        :return:
        """
        raise NotImplementedError()


class Gent(Command):
    """
    Gent is a light-weight builtin python command
    """
    name = None
    arguments = []

    def __init__(self):
        # build arg map
        self.arguments_map: Dict[str, GentArgument] = {}
        for arg in self.arguments:
            self.arguments_map[arg.argument_name] = arg

    def invoke(self, args, kwargs):
        """
        invoke a command
        """
        true_args = []
        true_kwargs = {}
        # do filter
        for i in range(0, len(args)):
            try:
                f = self.arguments[i]
            except IndexError:
                raise ArgumentError(f"wrong number of arguments {len(args)}")
            true_args.append(f.filter(args[i]))

        for key, val in kwargs:
            f = self.arguments_map.get(key, None)
            if f is None:
                raise ArgumentError(f"unknown option {key}")
            true_kwargs[key] = f.filter(val)

            return self._execute(*true_args, **true_kwargs)
        else:
            raise NotImplementedError("this command is not finished yet")

    def _execute(self, *args, **kwargs):
        """
        try execute entry
        """
        raise NotImplementedError()
