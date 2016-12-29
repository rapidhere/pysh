# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the cmd objects
"""
__author__ = "rapidhere"
__all__ = ("CommandInvoke", "Command", "InvokeResult")


from typing import Callable


class CommandInvoke(object):
    """
    represent a command invoke
    """
    def __init__(self, command_name: str, *args, **kwargs):
        self.command_name: str = command_name
        self.arguments: list = args
        self.key_arguments: dict = kwargs


class InvokeResult(object):
    """
    the result of the command invoking
    """
    pass


class Command(object):
    """
    a command object
    """
    def __init__(self, name: str, invoker: Callable[..., InvokeResult]):
        self.name = name
        self.invoker = invoker

    def invoke(self, args, kwargs) -> InvokeResult:
        """
        invoke a command
        """
        if self.invoker is not None:
            return self.invoker(*args, **kwargs)
        else:
            raise NotImplementedError("this command is not finished yet")
