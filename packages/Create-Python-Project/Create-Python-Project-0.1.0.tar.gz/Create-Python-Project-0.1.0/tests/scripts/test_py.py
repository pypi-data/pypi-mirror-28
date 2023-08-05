"""
    tests.scripts.test_py
    ~~~~~~~~~~~~~~~~~~~~~

    Test PyScript functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""
import os

import pytest

from create_python_project.info import PyDocstringInfo, RSTTitleInfo, SingleLineTextInfo, PyInfo
from create_python_project.scripts import PyScript


def test_py_script(repo_path):
    py_script = PyScript()
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for filename in filenames:
            if filename.split('.')[-1] == 'py':
                py_script.set_source(os.path.join(dirpath, filename))
                assert py_script.source.source_path == os.path.join(dirpath, filename)
                assert py_script.publish() is not None


def test_py_script_info(repo_path):
    py_script = PyScript()

    py_script.set_source(os.path.join(repo_path, 'setup.py'))
    py_script.publish()
    assert py_script.content.info.docstring.title.text == 'Boilerplate-Python'
    assert py_script.content.info.docstring.copyright is None
    assert py_script.content.info.docstring.license is None

    py_script.set_source(os.path.join(repo_path, 'boilerplate_python', '__init__.py'))
    py_script.publish()
    assert py_script.content.info.docstring.title.text == 'boilerplate_python'
    assert py_script.content.info.docstring.copyright.text == 'Copyright 2017 by Nicolas Maurice.'
    assert py_script.content.info.docstring.copyright.lineno == 5
    assert py_script.content.info.docstring.license.text == 'BSD, see :ref:`license` for more details.'
    assert py_script.content.info.docstring.license.lineno == 6

    py_script.set_source('""":image: My image"""')
    py_script.publish()
    assert py_script.content.info.docstring.title is None
    assert py_script.content.info.docstring.copyright is None
    assert py_script.content.info.docstring.license is None


def _set_info(py_script, title=None, copyright=None, license=None):
    title = title if title is not None else py_script.content.info.docstring.title.text
    title_info = RSTTitleInfo(text=title,
                              symbol=py_script.content.info.docstring.title.symbol)

    copyright = copyright if copyright is not None else py_script.content.info.docstring.copyright.text \
        if py_script.content.info.docstring.copyright is not None else None
    copyright_info = SingleLineTextInfo(text=copyright)

    license = license if license is not None else py_script.content.info.docstring.license.text \
        if py_script.content.info.docstring.license is not None else None
    license_info = SingleLineTextInfo(text=license)

    new_info = PyInfo(docstring=PyDocstringInfo(title=title_info,
                                                copyright=copyright_info,
                                                license=license_info))

    return new_info, title, copyright, license


def _test_py_script_valid_change(source, title=None, copyright=None, license=None):
    py_script = PyScript()
    py_script.set_source(source)
    py_script.publish()

    new_info, title, copyright, license = _set_info(py_script, title, copyright, license)

    publication = py_script.publish(new_info=new_info)
    assert py_script.content.info.docstring.title.text == title
    assert py_script.content.info.docstring.copyright.text == copyright
    assert py_script.content.info.docstring.license.text == license

    return publication


def test_py_script_change():
    source = \
        '"""\n' \
        '    title\n' \
        '    =====\n' \
        '\n' \
        '    body\n' \
        '\n' \
        '    :copyright: Copyright\n' \
        '    :license: :ref:`license`\n' \
        '"""\n' \
        '\n' \
        '__version__ = \'0.0.1\'\n'

    publication = \
        '"""\n' \
        '    title\n' \
        '    =====\n' \
        '\n' \
        '    body\n' \
        '\n' \
        '    :copyright: New Copyright\n' \
        '    :license: New License\n' \
        '"""\n' \
        '\n' \
        '__version__ = \'0.0.1\'\n'
    assert _test_py_script_valid_change(source=source,
                                        copyright='New Copyright',
                                        license='New License') == publication

    publication = \
        '"""\n' \
        '    New Title\n' \
        '    =========\n' \
        '\n' \
        '    body\n' \
        '\n' \
        '    :copyright: Copyright\n' \
        '    :license: :ref:`license`\n' \
        '"""\n' \
        '\n' \
        '__version__ = \'0.0.1\'\n'
    assert _test_py_script_valid_change(source=source,
                                        title='New Title') == publication

    source = \
        '"""\n' \
        '    title\n' \
        '    ~~~~~\n' \
        '\n' \
        '    body\n' \
        '\n' \
        '"""\n' \
        '\n'

    publication = \
        '"""\n' \
        '    New Title\n' \
        '    ~~~~~~~~~\n' \
        '\n' \
        '    body\n' \
        '"""\n' \
        '\n'
    assert _test_py_script_valid_change(source=source, title='New Title') == publication


def _test_py_script_invalid_change(source, title=None, copyright=None, license=None):
    py_script = PyScript()
    py_script.set_source(source)
    py_script.publish()

    with pytest.raises(Exception):
        new_info, title, copyright, license = _set_info(py_script, title, copyright, license)
        py_script.publish(new_info=new_info)


def test_py_script_invalid_change(repo_path):
    source = os.path.join(repo_path, 'boilerplate_python', '__init__.py')
    _test_py_script_invalid_change(source, copyright=5)
    _test_py_script_invalid_change(source, copyright='')
    _test_py_script_invalid_change(source, license='license\nNew license')


def test_py_script_import_change():
    source = \
        '"""\n' \
        '    New Title\n' \
        '    =========\n' \
        '\n' \
        '    body\n' \
        '\n' \
        '    :copyright: Copyright\n' \
        '    :license: :ref:`license`\n' \
        '"""\n' \
        '\n' \
        'import old_project\n' \
        'from old_project.module import function\n' \
        '\n' \
        'function()\n' \
        'old_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=old_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    py_script = PyScript(source=source)

    updated_source = \
        '"""\n' \
        '    New Title\n' \
        '    =========\n' \
        '\n' \
        '    body\n' \
        '\n' \
        '    :copyright: Copyright\n' \
        '    :license: :ref:`license`\n' \
        '"""\n' \
        '\n' \
        'import new_project\n' \
        'from new_project.module import function\n' \
        '\n' \
        'function()\n' \
        'new_project.function()\n' \
        '\n' \
        'def function2(new_project,\n' \
        '              arg2=new_project):\n' \
        '    return new_project.function()\n' \
        '\n'
    assert py_script.publish(old_import='old_project', new_import='new_project') == updated_source

    source = \
        '\n' \
        'import old_project as alias_project\n' \
        'from old_project.module import function\n' \
        '\n' \
        'function()\n' \
        'alias_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=alias_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    py_script = PyScript(source=source)

    updated_source = \
        '\n' \
        'import new_project as alias_project\n' \
        'from new_project.module import function\n' \
        '\n' \
        'function()\n' \
        'alias_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=alias_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    assert py_script.publish(old_import='old_project', new_import='new_project') == updated_source

    source = \
        '\n' \
        'import old_project\n' \
        'from package import old_project\n' \
        '\n' \
        'function()\n' \
        'old_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=old_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    py_script = PyScript(source=source)

    updated_source = \
        '\n' \
        'import new_project\n' \
        'from package import old_project\n' \
        '\n' \
        'function()\n' \
        'old_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=old_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    assert py_script.publish(old_import='old_project', new_import='new_project') == updated_source

    source = \
        '\n' \
        'import old_project\n' \
        'import package as old_project\n' \
        '\n' \
        'function()\n' \
        'old_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=old_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    py_script = PyScript(source=source)

    updated_source = \
        '\n' \
        'import new_project\n' \
        'import package as old_project\n' \
        '\n' \
        'function()\n' \
        'old_project.function()\n' \
        '\n' \
        'def function2(old_project,\n' \
        '              arg2=old_project):\n' \
        '    return old_project.function()\n' \
        '\n'
    assert py_script.publish(old_import='old_project', new_import='new_project') == updated_source
