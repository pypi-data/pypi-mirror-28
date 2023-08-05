"""
    tests.scripts.test_init
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test PyInitScript functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest

from create_python_project.scripts import PyInitScript
from create_python_project.info import PyInitInfo, InitInfo, VarInfo


def _test_kwarg(kwarg, arg, value, lineno):
    assert kwarg.arg == arg
    assert kwarg.value == value
    assert kwarg.lineno == lineno


def _test_setup_kwargs(kwargs, arg, value, lineno):
    _test_kwarg(getattr(kwargs, arg), arg, value, lineno)


def test_init_script_info(repo_path):
    init_script = PyInitScript(source=os.path.join(repo_path, 'boilerplate_python', '__init__.py'))
    init_script.publish()
    assert init_script.content.info.docstring.title.text == 'boilerplate_python'
    assert init_script.content.info.code.version.value == '0.0.0'
    assert init_script.content.info.code.version.var == '__version__'
    assert init_script.content.info.code.version.lineno == 3


def _set_info(init_script, version=None):
    old_version_info = init_script.content.info.code.version
    version = version if version is not None else old_version_info.value
    new_version_name = VarInfo(var='__version__', value=version, lineno=old_version_info.lineno)

    new_info = PyInitInfo()
    new_info.code = InitInfo()
    new_info.code.version = new_version_name

    return new_info, version


def _test_init_script_valid_change(source, version=None):
    init_script = PyInitScript(source=source)
    init_script.publish()

    new_info, version = _set_info(init_script, version)

    publication = init_script.publish(new_info=new_info)
    version_info = init_script.content.info.code.version
    assert version_info.value == version
    return publication


def test_init_script_change():
    source = \
        '"""\n' \
        '    docstring\n' \
        '"""\n' \
        '\n' \
        '__version__ = \'0.0.0\'\n' \
        '\n' \
        '__all__ = []\n' \
        '\n'

    publication = \
        '"""\n' \
        '    docstring\n' \
        '"""\n' \
        '\n' \
        '__version__ = \'1.4.23b4\'\n' \
        '\n' \
        '__all__ = []\n' \
        '\n'
    assert _test_init_script_valid_change(source, version='1.4.23b4') == publication


def _test_invalid_init_script_change(repo_path, version=None):
    init_script = PyInitScript(source=os.path.join(repo_path, 'boilerplate_python', '__init__.py'))
    init_script.publish()

    with pytest.raises(Exception):
        new_info, version = _set_info(init_script, version)
        init_script.publish(new_info)


def test_init_script_invalid_change(repo_path):
    _test_invalid_init_script_change(repo_path, version='name\non\nmultiple\nlines')
    _test_invalid_init_script_change(repo_path, version=4)
