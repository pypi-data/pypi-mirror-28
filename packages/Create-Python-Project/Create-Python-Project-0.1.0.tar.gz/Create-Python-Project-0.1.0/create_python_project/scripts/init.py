"""
    create_python_project.scripts.init
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for python __init__.py script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import _ast
import ast

from .py import PyContent, PyScript, PyParser, PyReader
from ..info import PyInitInfo, VarInfo


class PyInitContent(PyContent):
    """Base content for __init__.py script"""

    info_class = PyInitInfo


class PyInitVisitor(ast.NodeVisitor):
    def __init__(self, content, line_offset=None):
        self.content = content
        self.info = content.info.code
        self.line_offset = line_offset or content.info.docstring_lineno

    def visit(self, node):
        super().visit(node)

    def visit_Assign(self, node):
        target, value = node.targets[0], node.value
        if isinstance(target, _ast.Name) and isinstance(value, _ast.Str):
            if target.id == '__version__':
                version = VarInfo(var=target.id, value=value.s, lineno=value.lineno - self.line_offset - 1)
                self.info.version = version


class PyInitReader(PyReader):
    """Base class for reader setup.py script"""

    content_class = PyInitContent


class PyInitParser(PyParser):
    """Base class for parsing setup.py script"""

    def parse_code(self, content):
        PyInitVisitor(content).visit(content.ast)


class PyInitScript(PyScript):
    """Base class for manipulating setup.py script"""

    supported_format = ('*/__init__.py',)

    parser_class = PyInitParser
    reader_class = PyInitReader
