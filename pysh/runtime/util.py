# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

useful utils
"""
__author__ = "rapidhere"

from .cmdobj import Gent


def gent(cmd_name: str):
    """
    gent create decorator
    """
    def _f(f: callable) -> callable:
        name = cmd_name
        if name is None:
            name = f.__name__

        # noinspection PyUnresolvedReferences
        arg_map: dict[str, GentArgument] = f.__annotations__
        args = []

        for key, val in arg_map.items():
            # set argument name
            if len(val.argument_name) == 0:
                val.argument_name = key
            args.append(val)

        gent_cls = type(name, (Gent, ), {
            "name": name,
            "arguments": args,
            "_execute": lambda self, *ars, **kwargs: f(*ars, **kwargs)})

        return gent_cls

    return _f
