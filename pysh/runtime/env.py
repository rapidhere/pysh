# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the runtime env
"""
__author__ = "rapidhere"
__all__ = ("RuntimeEnv", "get", "register_command")

from typing import Dict, Callable

from .cmdobj import CommandInvoke, InvokeResult, Command, CommandArgument, NoSuchCommandInvokeError


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
        if cmd is None:
            return NoSuchCommandInvokeError(cmd_ivk.command_name)

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


def register_command(cmd_name: str):
    """
    a command register decorator
    """
    def _reg(f: Callable[..., InvokeResult], name=None) -> None:
        if name is None:
            name = f.__name__

        # noinspection PyUnresolvedReferences
        filter_map: dict[str, CommandArgument] = f.__annotations__
        filters = []

        for key, val in filter_map.items():
            # set argument name
            if len(val.argument_name) == 0:
                val.argument_name = key
            filters.append(val)

        cmd = Command(name, f, filters)
        get().register_command(cmd)

    def _f(f: Callable[..., InvokeResult]) -> Callable[..., InvokeResult]:
        _reg(f, cmd_name)
        return f

    return _f
