"""
    tests.test_utils
    ~~~~~~~~~~~~~~~~

    Test utilities functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest
from mock import Mock

from create_python_project.info import BaseInfo
from create_python_project.scripts import BaseScript, PyScript, IniScript
from create_python_project.utils import get_script, get_info, publish, is_matching, \
    format_project_name, format_package_name, format_py_script_title, \
    format_url, is_git_url


def test_is_git_url():
    assert is_git_url('git@github.com:nmvalera/rc-config-boilerplate.git')
    assert is_git_url('https://github.com/nmvalera/create-python-project.git')
    assert is_git_url('git://github.com/nmvalera/create-python-project.git')
    assert not is_git_url('boilerplate-test')


def _make_blob(path):
    blob = Mock()
    blob.path = path
    blob.abspath = os.path.abspath(path)
    blob.name = os.path.basename(path)
    return blob


def _test_get_script(path):
    script = get_script(_make_blob(path))
    assert isinstance(script, BaseScript)
    return script


def test_get_script(repo_path):
    assert isinstance(_test_get_script('setup.cfg'), IniScript)
    assert isinstance(_test_get_script('boilerplate_python/__init__.py'), PyScript)


def _test_get_info(path):
    info = get_info(_make_blob(path))
    assert isinstance(info, BaseInfo)
    return info


def test_get_info(repo_path):
    setup_info = _test_get_info('setup.py')
    assert setup_info.code.setup.name.value == 'Boilerplate-Python'

    package_info = _test_get_info('boilerplate_python/__init__.py')
    assert package_info.code.version.value == '0.0.0'


def test_publish(repo_path):
    publication = publish(_make_blob('CONTRIBUTING.rst'), destination=None)
    assert len(publication.split('\n')) > 1


def _test_is_matching(regexp, path, result=True):
    assert is_matching(regexp, _make_blob(path)) == result


def test_is_matching():
    _test_is_matching(['*.py'], 'script.py')
    _test_is_matching(['script.py'], 'script.py')
    _test_is_matching(['*.py'], 'script.txt', False)
    _test_is_matching(['*.py'], 'folder/script.py')
    _test_is_matching(['script.py'], 'folder/script.py', False)
    _test_is_matching(['folder*.py'], 'script.py', False)
    _test_is_matching(['folder*.py', 'script*'], 'script.py')
    _test_is_matching(['folder*.py'], 'folder/script.py')
    _test_is_matching(['folder*.py'], 'folder/sub-folder/script.py')
    _test_is_matching(['folder*'], 'folder/sub-folder/script.txt')


def test_format_project_name():
    assert format_project_name('new-name') == 'New-Name'
    assert format_project_name('New-name') == 'New-Name'


def test_format_package_name():
    assert format_package_name('new-name') == 'new_name'
    assert format_package_name('New-name') == 'new_name'


def test_format_py_script_title():
    assert format_py_script_title('boilerplate_python/__init__.py') == 'boilerplate_python'
    assert format_py_script_title('boilerplate_python/script.py') == 'boilerplate_python.script'
    assert format_py_script_title('tests/sub_package/script.py') == 'tests.sub_package.script'


def test_format_url():
    url = 'git@github.com:nmvalera/create-python-project.git'

    assert format_url(url, 'https') == 'https://github.com/nmvalera/create-python-project'
    assert format_url(url, 'https+git') == 'https://github.com/nmvalera/create-python-project.git'
    assert format_url(url, 'ssh') == url
    assert format_url(url, 'git') == 'git://github.com/nmvalera/create-python-project.git'

    with pytest.raises(AssertionError):
        format_url('git@github.com/nmvalera/create-python-project.git', 'https')
