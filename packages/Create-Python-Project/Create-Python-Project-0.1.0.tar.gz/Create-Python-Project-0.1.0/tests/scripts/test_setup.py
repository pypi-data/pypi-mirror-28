"""
    tests.scripts.test_setup
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test SetupScript functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest

from create_python_project.scripts import PySetupScript
from create_python_project.info import PySetupInfo, SetupInfo, SetupKwargsInfo, KwargInfo


def _test_kwarg(kwarg, arg, value, lineno):
    assert kwarg.arg == arg
    assert kwarg.value == value
    assert kwarg.lineno == lineno


def _test_setup_kwargs(kwargs, arg, value, lineno):
    _test_kwarg(getattr(kwargs, arg), arg, value, lineno)


def test_setup_script_info(repo_path):
    setup_script = PySetupScript(source=os.path.join(repo_path, 'setup.py'))
    setup_script.publish()
    assert setup_script.content.info.docstring.title.text == 'Boilerplate-Python'
    kwargs = setup_script.content.info.code.setup
    _test_setup_kwargs(kwargs, 'name', 'Boilerplate-Python', 14)
    _test_setup_kwargs(kwargs, 'version', '0.0.0', 15)
    _test_setup_kwargs(kwargs, 'url', 'https://github.com/nmvalera/boilerplate-python', 17)
    _test_setup_kwargs(kwargs, 'author', 'Nicolas Maurice', 18)
    _test_setup_kwargs(kwargs, 'author_email', 'nicolas.maurice.valera@gmail.com', 19)
    _test_setup_kwargs(kwargs, 'description', 'Boilerplate-Python is an empty Python project', 20)
    _test_kwarg(kwargs.packages[0], 'packages', 'boilerplate_python', 21)


def _set_info(setup_script, name=None, version=None, package=None):
    old_setup_info = setup_script.content.info.code.setup
    old_name_info = old_setup_info.name
    name = name if name is not None else old_name_info.value
    new_name_info = KwargInfo(arg='name', value=name, lineno=old_name_info.lineno)

    old_version_info = old_setup_info.version
    version = version if version is not None else old_version_info.value
    new_version_info = KwargInfo(arg='version', value=version, lineno=old_version_info.lineno)

    old_packages_info = old_setup_info.packages
    package = package if package is not None else old_packages_info[0].value
    new_package_info = KwargInfo(arg='packages', value=package, lineno=old_packages_info[0].lineno)

    new_info = PySetupInfo()
    new_info.code = SetupInfo()
    new_info.code.setup = SetupKwargsInfo(name=new_name_info, version=new_version_info)
    new_info.code.setup.packages = (new_package_info,)

    return new_info, name, version, package


def _test_setup_script_valid_change(source, name=None, version=None, package=None):
    setup_script = PySetupScript(source=source)
    setup_script.publish()

    new_info, name, version, package = _set_info(setup_script, name, version, package)

    publication = setup_script.publish(new_info=new_info)
    setup_info = setup_script.content.info.code.setup
    assert setup_info.name.value == name
    assert setup_info.version.value == version
    assert setup_info.packages[0].value == package
    return publication


def test_setup_script_change():
    source = \
        'from setuptools import setup\n' \
        '\n' \
        'setup(\n' \
        '    name="Boilerplate-Python",\n' \
        '    version="0.0.1",\n' \
        '    packages=["my_package", ]\n' \
        ')\n'

    publication = \
        'from setuptools import setup\n' \
        '\n' \
        'setup(\n' \
        '    name="New-Name",\n' \
        '    version="0.0.1",\n' \
        '    packages=["my_package", ]\n' \
        ')\n'
    assert _test_setup_script_valid_change(source, name='New-Name') == publication

    publication = \
        'from setuptools import setup\n' \
        '\n' \
        'setup(\n' \
        '    name="Boilerplate-Python",\n' \
        '    version="10.1.2",\n' \
        '    packages=["my_package", ]\n' \
        ')\n'

    assert _test_setup_script_valid_change(source, version='10.1.2') == publication

    publication = \
        'from setuptools import setup\n' \
        '\n' \
        'setup(\n' \
        '    name="Boilerplate-Python",\n' \
        '    version="0.0.1",\n' \
        '    packages=["new_package", ]\n' \
        ')\n'
    assert _test_setup_script_valid_change(source, package='new_package') == publication

    source = \
        '"""\n' \
        '    title\n' \
        '    ~~~~~\n' \
        '\n' \
        '    docstring\n' \
        '"""\n' \
        '\n' \
        'from setuptools import setup as alias_setup, sandbox\n' \
        '\n' \
        'alias_setup(\n' \
        '    name="Boilerplate-Python",\n' \
        '    version="0.0.1",\n' \
        '    packages=[\n' \
        '        "my_package",\n' \
        '    ]\n' \
        ')\n'

    publication = \
        '"""\n' \
        '    title\n' \
        '    ~~~~~\n' \
        '\n' \
        '    docstring\n' \
        '"""\n' \
        '\n' \
        'from setuptools import setup as alias_setup, sandbox\n' \
        '\n' \
        'alias_setup(\n' \
        '    name="Boilerplate-Python",\n' \
        '    version="0.0.1",\n' \
        '    packages=[\n' \
        '        "new_package",\n' \
        '    ]\n' \
        ')\n'
    assert _test_setup_script_valid_change(source, package='new_package') == publication


def _test_invalid_setup_script_change(repo_path, name=None, version=None, package=None):
    setup_script = PySetupScript(source=os.path.join(repo_path, 'setup.py'))
    setup_script.publish()

    with pytest.raises(Exception):
        new_info, name, version, package = _set_info(setup_script, name, version, package)
        setup_script.publish(new_info=new_info)


def test_py_script_invalid_change(repo_path):
    _test_invalid_setup_script_change(repo_path, name='name\non\nmultiple\nlines')
    _test_invalid_setup_script_change(repo_path, package=4)
    _test_invalid_setup_script_change(repo_path, version=8)
