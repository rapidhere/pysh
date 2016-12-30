# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

Gent arguments
"""
__author__ = "rapidhere"

from pysh.exp import ArgumentError


class GentArgument(object):
    """
    Gent argument
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


# ~~~ Common Command Arguments
class Integer(GentArgument):
    def __init__(self, min_val: int = None, max_val: int = None, *args, **kwargs):
        GentArgument.__init__(self, *args, **kwargs)
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


class String(GentArgument):
    def __init__(self, *args, **kwargs):
        GentArgument.__init__(self, *args, **kwargs)

    def filter(self, value: str) -> str:
        return value

    def fail_message(self) -> str:
        return "must be a string"
