"""
    create_python_project.scripts.ini
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for .ini (.cfg, .coverage) script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import re

from .base import ScriptContent, BaseScript, BaseReader, BaseWriter, BaseParser


class IniContent(ScriptContent):
    """Base content for .ini scripts"""

    _section_pattern = re.compile('\[(?P<header>[^]]+)\]')
    _comment_pattern = re.compile('\s*#.*')
    _item_pattern = re.compile('((?P<option>.*?)(?P<delim>[=:]))?(?P<space>\s*)(?P<value>.*)')

    def transform(self, old_value=None, new_value=None, **kwargs):
        if isinstance(old_value, str) and isinstance(new_value, str):
            for i, line in enumerate(self.lines):
                if self._section_pattern.match(line) or self._comment_pattern.match(line):
                    continue
                elif self._item_pattern.match(line):  # pragma: no branch
                    match = self._item_pattern.match(line)

                    updated_value = self.update_value(match.group('value'), old_value, new_value)
                    self.lines[i] = self._item_pattern.sub('\g<option>\g<delim>\g<space>{value}'
                                                           .format(value=updated_value),
                                                           line)


class IniParser(BaseParser):
    """Base class for parsing .ini"""


class IniReader(BaseReader):
    """Base reader class for .ini"""

    content_class = IniContent


class IniWriter(BaseWriter):
    """Base reader class for .ini"""


class IniScript(BaseScript):
    """Base class for manipulating .ini scripts"""

    supported_format = (
        '*.ini',
        'setup.cfg',
        '.coveragerc',
    )

    parser_class = IniParser
    reader_class = IniReader
    writer_class = IniWriter
