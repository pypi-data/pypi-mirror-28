"""
    create_python_project.scripts.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from ..info import BaseInfo
from ..io import IOMeta, InputDescriptor, OutputDescriptor


class ScriptContent:
    """Base content class for every script"""

    def __init__(self, lines=None):
        self.lines = lines

    def set_lines(self, lines=None):
        self.lines = lines

    def output(self):
        return '\n'.join(self.lines)

    def update_value(self, value, old, new):
        return value.replace(old, new)

    def update_line(self, lineno, old, new):
        self.lines[lineno] = self.update_value(self.lines[lineno], old, new)

    def transform(self, old_value=None, new_value=None, **kwargs):
        if isinstance(old_value, str) and isinstance(new_value, str):  # pragma: no branch
            for lineno in range(len(self.lines)):
                self.update_line(lineno, old_value, new_value)


class ContentWithInfo(ScriptContent):
    info_class = BaseInfo

    def __init__(self, info=None, lines=None):
        super().__init__(lines)
        if info is not None:
            assert isinstance(info, self.info_class), \
                '{0} info must be an instance of {1}'.format(type(self), self.info_class)
            self.info = info
        else:
            self.info = self.info_class()

    def transform(self, old_value=None, new_value=None, new_info=None, **kwargs):
        self.info.update(new_info, self.lines, **kwargs)
        super().transform(old_value=old_value, new_value=new_value)


class BaseParser:
    """Base parser for scripts"""

    content_class = ScriptContent

    def setup_parse(self, input_string):
        self.input_string = input_string

    def parse(self, input_string, content):
        self.setup_parse(input_string)
        content.set_lines(self.input_string.split('\n'))


class BaseReader:
    """Base reader for scripts"""

    content_class = ScriptContent

    def __init__(self, parser=None):
        self.parser = parser

        self.input = None
        self.content = None

    def read(self, source, parser):
        self.init_content()
        self.source = source
        self.parser = parser or self.parser
        self.input = self.source.read()
        self.parse()
        return self.content

    def parse(self):
        self.parser.parse(self.input, self.content)

    def init_content(self):
        self.content = self.content_class()


class BaseWriter:
    """Base writer for scripts"""

    def write(self, content, destination):
        self.content = content
        self.destination = destination
        self.translate(content)
        output = self.destination.write(self.output)
        return output

    def translate(self, content):
        self.output = content.output()


class BaseScript(metaclass=IOMeta):
    """Base class for manipulating scripts"""

    supported_format = ('*',)

    source = InputDescriptor()
    destination = OutputDescriptor()

    reader_class = BaseReader
    writer_class = BaseWriter
    parser_class = BaseParser

    def __init__(self, source=None, destination=None,
                 reader=None, parser=None, writer=None):
        self.source = source
        self.destination = destination

        self.reader = reader or self.reader_class()
        self.parser = parser or self.parser_class()
        self.writer = writer or self.writer_class()

        self.content = None

    def read(self):
        if self.content is None:
            self.content = self.reader.read(self.source, self.parser)

    def apply_transform(self, *args, **kwargs):
        self.content.transform(*args, **kwargs)

    def write(self):
        return self.writer.write(self.content, self.destination)

    def publish(self, *args, **kwargs):
        self.read()
        self.apply_transform(*args, **kwargs)
        output = self.write()
        return output

    def set_source(self, source=None, source_path=None):
        self.source = source or source_path
        self.reset()

    def reset(self, reader=None, parser=None, writer=None):
        self.content = None

        self.reader = reader or self.reader_class()
        self.parser = parser or self.parser_class()
        self.writer = writer or self.writer_class()

    def set_destination(self, destination=None, destination_path=None):
        self.destination = destination or destination_path
