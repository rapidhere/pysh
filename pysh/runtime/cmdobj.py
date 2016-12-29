# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the cmd objects
"""
__author__ = "rapidhere"
__all__ = ("CommandInvoke", "Command", "InvokeResult")

from typing import Callable, List, Dict

from pysh.cl.cmdline import CommandLineInterface
from pysh.exp import ArgumentError


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
    def __init__(self, ret_code: int):
        self.ret_code = ret_code

    def display(self, cl: CommandLineInterface):
        """
        display invoke result on the terminal
        :return:
        """
        pass  # simply do nothing


class StringInvokeResult(InvokeResult):
    """
    a simple string invoke result
    """
    def __init__(self, ret_code: int, content: str):
        InvokeResult.__init__(self, ret_code)
        self.content = content

    def display(self, cl: CommandLineInterface):
        cl.put_string(self.content)


class InvokeError(InvokeResult):
    """
    a invoke error
    """
    def __init__(self, ret_code: int, error):
        InvokeResult.__init__(self, ret_code)

        self.error = error

    def display(self, cl: CommandLineInterface):
        cl.put_string(str(self.error) + "\n")


class NoSuchCommandInvokeError(InvokeError):
    """
    no such command
    """
    def __init__(self, command: str):
        InvokeError.__init__(self, -1, f"no such command `${command}`")
        self.command = command


class InternalErrorInvokeResult(InvokeError):
    """
    the internal error invoke result
    """
    def __init__(self, exception: Exception):
        InvokeError.__init__(
            self, -1, f"pysh internal error: {str(exception)}")


class CommandArgument(object):
    """
    Command argument
    """
    def __init__(self, desc: str, optional: bool=False, argument_name=""):
        self.description = desc
        self.optional = optional
        self.argument_name = argument_name

    def filter(self, value: str):
        """
        filter the value
        """
        raise NotImplementedError()

    def fail(self, fail_condition=True):
        if fail_condition:
            raise ArgumentError(self.fail_message())

    def fail_message(self) -> str:
        raise NotImplementedError()


class Command(object):
    """
    a command object
    """
    def __init__(self, name: str, invoker: Callable[..., InvokeResult], args: List[CommandArgument]):
        self.name = name
        self.invoker = invoker
        self.arguments = args

        # build arg map
        self.arguments_map: Dict[str, CommandArgument] = {}
        for arg in self.arguments:
            self.arguments_map[arg.argument_name] = arg

    def invoke(self, args, kwargs) -> InvokeResult:
        """
        invoke a command
        """
        try:
            return self._invoke(args, kwargs)
        except ArgumentError as a:
            # builtin command argument error
            return InvokeError(1, str(a))
        except Exception as e:
            return InternalErrorInvokeResult(e)

    def _invoke(self, args, kwargs) -> InvokeResult:
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

        # invoke
        if self.invoker is not None:
            return self.invoker(*true_args, **true_kwargs)
        else:
            raise NotImplementedError("this command is not finished yet")


# ~~~ Command Argument Filters
class Integer(CommandArgument):
    def __init__(self, min_val: int = None, max_val: int = None, *args, **kwargs):
        CommandArgument.__init__(self, *args, **kwargs)
        self._min = min_val
        self._max = max_val

    # noinspection PyUnreachableCode
    def filter(self, value: str) -> int:
        try:
            value = int(value)
        except ValueError:
            self.fail()

        self.fail(self._min is not None and value < self._min)
        self.fail(self._max is not None and self._max < value)

        return value

    def fail_message(self) -> str:
        if self._min is None and self._max is None:
            return "require a integer"
        elif self._min is None:
            return f"require a integer less than {self._max}"
        elif self._max is None:
            return f"require a integer larger than {self._min}"
        else:
            return f"require a integer between {self._min} and {self._max}"


class String(CommandArgument):
    def __init__(self, *args, **kwargs):
        CommandArgument.__init__(self, *args, **kwargs)

    def filter(self, value: str) -> str:
        return value

    def fail_message(self) -> str:
        return "must be a string"
