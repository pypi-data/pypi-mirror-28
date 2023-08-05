"""
    create_python_project.scripts.yml
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for .yml script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import re
from functools import partial

import yaml
from yaml.tokens import ScalarToken, ValueToken, BlockEntryToken, FlowEntryToken, FlowSequenceStartToken

from .base import ScriptContent, BaseScript, BaseReader, BaseWriter, BaseParser


class YmlContent(ScriptContent):
    _comment_pattern = re.compile('(?P<start>[^#]*)(?P<comment>#.*)')

    def prepare_transform(self):
        self.tokens = yaml.scan(self.output())

    def transform(self, old_value=None, new_value=None, **kwargs):
        if isinstance(old_value, str) and isinstance(new_value, str):
            self.prepare_transform()
            for token in self.tokens:
                if isinstance(token, ValueToken) or isinstance(token, BlockEntryToken) or \
                        isinstance(token, FlowEntryToken) or isinstance(token, FlowSequenceStartToken):
                    token = next(self.tokens)
                    if isinstance(token, ScalarToken):
                        start_mark, end_mark = token.start_mark, token.end_mark
                        self.lines[start_mark.line] = '{start}{value}{end}'. \
                            format(start=self.lines[start_mark.line][:start_mark.column],
                                   value=self.update_value(token.value, old_value, new_value),
                                   end=self.lines[start_mark.line][end_mark.column:])

            # comments are not parsed by PYyaml so we need to transform it manually
            self.transform_comment(old_value=old_value, new_value=new_value)

    def transform_comment(self, old_value=None, new_value=None):
        for i, line in enumerate(self.lines):
            self.lines[i] = self._comment_pattern.sub(partial(self.replace_comment, old_value, new_value), line)

    def replace_comment(self, old_value, new_value, match):
        return (match.group('start') or '') + self.update_value(match.group('comment'),
                                                                old_value,
                                                                new_value)


class YmlParser(BaseParser):
    """Base class for parsing .ini"""


class YmlReader(BaseReader):
    """Base reader class for .ini"""

    content_class = YmlContent


class YmlWriter(BaseWriter):
    """Base reader class for .ini"""


class YmlScript(BaseScript):
    """Base class for manipulating .ini scripts"""

    supported_format = (
        '*.yml',
        '*.yaml',
    )

    parser_class = YmlParser
    reader_class = YmlReader
    writer_class = YmlWriter
