"""
    create_python_project.scripts.rst
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for reStructuredText script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from docutils import SettingsSpec, nodes, utils
from docutils.frontend import OptionParser
from docutils.parsers import rst

from .base import ContentWithInfo, BaseScript, BaseReader, BaseWriter, BaseParser
from ..info import RSTScriptInfo, RSTTitleInfo


class RSTContent(ContentWithInfo):
    """Base content class for .rst script"""

    info_class = RSTScriptInfo


class RSTVisitor(nodes.NodeVisitor):
    """Base visitor class to retrieve information from rst scripts"""

    def __init__(self, document, content):
        self.content = content
        self.has_visited_paragraph = False
        self.has_visited_title = False
        super().__init__(document)

    def visit_title(self, node):
        if not self.has_visited_title:
            if not self.has_visited_paragraph:
                text, lineno = node.astext(), node.line - 2
                symbol = self.content.lines[lineno + 1][0]
                has_overline = (lineno - 1 >= 0) and \
                               (len(self.content.lines[lineno - 1]) > 0) and \
                               (self.content.lines[lineno - 1][0] == symbol)
                self.content.info.title = RSTTitleInfo(text=text,
                                                       lineno=lineno,
                                                       symbol=symbol,
                                                       has_overline=has_overline)
            self.has_visited_title = True

    def visit_paragraph(self, node):
        self.has_visited_paragraph = True

    def unknown_visit(self, node):
        pass


class RSTParser(BaseParser):
    """Base class for parsing rst"""

    _rst_visitor_class = RSTVisitor

    def setup_parse(self, input_string):
        super().setup_parse(input_string)
        self.rst_parser = rst.Parser()

        defaults = {
            'file_insertion_enabled': False,
            'debug': False,
            'report_level': 4,
        }
        settings = OptionParser(components=(self.rst_parser, SettingsSpec()),
                                defaults=defaults).get_default_values()
        self.rst_document = utils.new_document('<.rst>', settings)

    def parse(self, input_string, content):
        self.setup_parse(input_string)
        self.rst_parser.parse(input_string, self.rst_document)
        content.set_lines(self.rst_parser.statemachine.input_lines.data)
        self.retrieve_rst_info(content)

    def retrieve_rst_info(self, content):
        self.set_rst_visitor(self.rst_document, content)
        self.rst_document.walk(self.rst_visitor)

    def set_rst_visitor(self, document, content):
        self.rst_visitor = self._rst_visitor_class(document, content)


class RSTReader(BaseReader):
    """Base reader class for rst"""

    content_class = RSTContent


class RSTWriter(BaseWriter):
    """Base reader class for rst"""


class RSTScript(BaseScript):
    """Base class for manipulating rst scripts"""

    supported_format = (
        '*.rst',
        'restructuredtext',
        'rest',
        '*.restx',
        '*.rtxt',
    )

    parser_class = RSTParser
    reader_class = RSTReader
    writer_class = RSTWriter
