# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the runtime env
"""
__author__ = "rapidhere"
__all__ = ("RuntimeEnv", "get", "register_command")

from typing import Dict, Callable, Union

from .cmdobj import CommandInvoke, InvokeResult, Command


class RuntimeEnv(object):
    """
    the runtime env
    """
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    @property
    def prompt(self):
        """
        resolve the prompt
        :return:
        """
        # TODO
        return "> "

    def invoke_command(self, cmd_ivk: CommandInvoke) -> InvokeResult:
        """
        invoke a command
        :param cmd_ivk: the command invoke
        :return:
        """
        cmd = self.resolve_command(cmd_ivk.command_name)
        return cmd.invoke(cmd_ivk.arguments, cmd_ivk.key_arguments)

    def resolve_command(self, cmd_name: str) -> Command:
        """
        resolve a command to run
        """
        return self._commands.get(cmd_name)

    def register_command(self, cmd: Command) -> None:
        """
        register a command
        """
        self._commands[cmd.name] = cmd

# the runtime env singleton
_env = None


def get() -> RuntimeEnv:
    """
    get the runtime env singleton
    :return: get the runtime env singleton
    """
    global _env
    if _env is None:
        _env = RuntimeEnv()

    return _env


def register_command(cmd_name: Union[str, Callable[..., InvokeResult]]):
    """
    a command register decorator
    """
    def _reg(f, name=None) -> None:
        if name is None:
            name = f.__name__

        cmd = Command(name, f)
        get().register_command(cmd)

    if callable(cmd_name):
        _reg(cmd_name)
        return cmd_name
    else:
        def _f(f: Callable[..., InvokeResult]) -> Callable[..., InvokeResult]:
            _reg(f, cmd_name)
            return f

        return _f
