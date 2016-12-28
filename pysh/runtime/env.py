# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the runtime env
"""
__author__ = "rapidhere"
__all__ = ("RuntimeEnv", "get", "register_command")

from typing import Dict, Callable

from .cmdobj import CommandInvoke, InvokeResult, Command


class RuntimeEnv(object):
    """
    the runtime env
    """
    def __init__(self):
        self._commands: Dict[str, Command] = {}

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


def register_command(cmd_name: str=""):
    """
    a command register decorator
    """
    def _f(f: Callable[..., InvokeResult]) -> Callable[..., InvokeResult]:
        nonlocal cmd_name
        if len(cmd_name) == 0:
            cmd_name = f.__name__

        cmd = Command(cmd_name, f)
        get().register_command(cmd)
        return f

    return _f
