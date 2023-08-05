"""
    create_python_project.scripts.setup
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for python setup.py script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import _ast

from .py import PyContent, PyScript, PyParser, PyReader, PyCodeVisitor
from ..info import PySetupInfo, SetupKwargsInfo, KwargInfo


class PySetupContent(PyContent):
    """Base content for setup.py script"""

    info_class = PySetupInfo


class PyCodeVisitorWithOffset(PyCodeVisitor):
    def __init__(self, content, line_offset=None):
        super().__init__(content)
        self.line_offset = line_offset or self.content.info.docstring_lineno
        self.info = self.content.info.code.setup


class SetupKwargsVisitor(PyCodeVisitorWithOffset):

    def visit_keyword(self, node):
        if node.arg in self.info._fields:
            if isinstance(node.value, _ast.Str):
                setattr(self.info, node.arg, KwargInfo(arg=node.arg,
                                                       value=node.value.s,
                                                       lineno=node.value.lineno - self.line_offset - 1))

            elif isinstance(node.value, _ast.List):  # pragma: no branch
                setattr(self.info,
                        node.arg,
                        tuple([KwargInfo(arg=node.arg, value=elt.s, lineno=elt.lineno - self.line_offset - 1)
                               for elt in node.value.elts]))


class SetupVisitor(PyCodeVisitorWithOffset):
    def __init__(self, content):
        super().__init__(content)
        self.setup_alias = None
        self.setup_visited = False

    def visit_ImportFrom(self, node):
        if node.module == 'setuptools':
            for name in node.names:
                if name.name == 'setup':
                    self.setup_alias = name.asname or name.name

    def visit_Call(self, node):
        if not self.setup_visited and isinstance(node.func, _ast.Name) and node.func.id == self.setup_alias:
            self.content.info.code.setup = SetupKwargsInfo()
            SetupKwargsVisitor(self.content,
                               self.line_offset).visit(node)
            self.setup_visited = True


class PySetupReader(PyReader):
    """Base class for reader setup.py script"""

    content_class = PySetupContent


class PySetupParser(PyParser):
    """Base class for parsing setup.py script"""

    def parse_code(self, content):
        SetupVisitor(content).visit(content.ast)


class PySetupScript(PyScript):
    """Base class for manipulating setup.py script"""

    supported_format = ('setup.py',)

    parser_class = PySetupParser
    reader_class = PySetupReader
