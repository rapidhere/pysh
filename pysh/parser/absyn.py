# -*- coding: utf-8 -*-
"""
Ranttu-Inc. rapidhere@gmail.com
Copyright(c) 2011-2016 ALL RIGHTS RESERVED

abstract syntax tree
"""
__author__ = "rapidhere"

from typing import List, Dict


class AstNode(object):
    """
    A ast node
    """


class PythonStatement(AstNode):
    """
    a python statement
    """
    def __init__(self, py_code: str):
        self.py_code = py_code


class PyshInvokeStatement(AstNode):
    """
    a pysh invoke statement
    """
    def __init__(self, expression):
        self.expression = expression


class PyshSimpleExpression(AstNode):
    """
    the base pysh expression
    """
    def __init__(self, invoke_name: str, arguments: List[str], keyword_arguments: Dict[str, str]):
        self.invoke_name = invoke_name
        self.arguments = arguments
        self.keyword_arguments = keyword_arguments


class PyshBinaryExpression(AstNode):
    """
    the binary pysh invoke expression
    """
    def __init__(self, operator: str, left, right):
        self.operator = operator
        self.left = left
        self.right = right


class PythonExpression(AstNode):
    """
    the python expression
    """
    def __init__(self, py_code: str):
        self.py_code = py_code
