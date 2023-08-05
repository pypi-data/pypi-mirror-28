"""
    create_python_project.scripts
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Module that implements class to enable scripts manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import fnmatch
import re

from .base import BaseScript
from .ini import IniScript
from .init import PyInitScript
from .py import PyScript
from .rst import RSTScript
from .setup import PySetupScript
from .yml import YmlScript


def is_supported(klass, file_path):
    """Evaluates if a file is compatible with a given Script class"""

    for ext in klass.supported_format:
        if re.match(fnmatch.translate(ext), file_path):
            return True
    return False


def get_script_class(file_path):
    """Return the most specific class matching path"""

    script_class = BaseScript
    for klass in [IniScript, PyScript, PyInitScript, PySetupScript, RSTScript, YmlScript]:
        if is_supported(klass, file_path) and issubclass(klass, script_class):
            script_class = klass
    return script_class


__all__ = [
    'BaseScript',
    'RSTScript',
    'PyScript',
    'PySetupScript',
    'PyInitScript',
    'IniScript',
    'YmlScript',
    'get_script_class',
]
