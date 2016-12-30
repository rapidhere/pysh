# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

the runtime env
"""
__author__ = "rapidhere"

from .confman import ConfigManager


class RuntimeEnv(object):
    """
    the runtime env
    """
    def __init__(self):
        # the true runtime context
        # can be invoked in shell
        self._context = {}

        # set config manager
        self.config = ConfigManager()

        # config env
        self._context["__env__"] = self
        self._context["__conf__"] = self.config
        self._context["resmod"] = self.resolve_module

        # import built-ins
        self.resolve_module("pysh.lib.builtin")

    def execute(self, cmd_line: str) -> None:
        """
        execute a task from cmd line
        :return:
        """
        exec(self.parse(cmd_line), self._context, self._context)

    def resolve_module(self, module_path: str) -> None:
        """
        resolve a module, and import module contents
        :return:
        """
        exec(f"import {module_path}", self._context, self._context)

    def parse(self, cmd_line: str):
        """
        parse a command line
        :return:
        """

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
