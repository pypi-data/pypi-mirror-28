'''
    tests.scripts.test_ini
    ~~~~~~~~~~~~~~~~~~~~~~

    Base class for .ini script manipulation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
'''

import os

from create_python_project.scripts import IniScript


def test_ini_script(repo_path):
    ini_script = IniScript()
    for filename in ['tox.ini', '.coveragerc', 'setup.cfg']:
        ini_script.set_source(os.path.join(repo_path, filename))
        assert ini_script.source.source_path == os.path.join(repo_path, filename)
        assert ini_script.publish() is not None


def test_ini_script_change():
    source = \
        '\n' \
        '[section1]\n' \
        'option1 = value1\n' \
        '# comment\n' \
        'option2 = value2.1\n' \
        '   value2.2\n' \
        '\n' \
        '[section2]\n' \
        'option1 = option2\n' \
        'option2 =\n' \
        '# comment option2 \n' \
        'option3 =\n' \
        '     value3.1\n' \
        '     option2\n' \
        '\n'

    ini_script = IniScript(source=source)
    updated_source = \
        '\n' \
        '[section1]\n' \
        'option1 = value1\n' \
        '# comment\n' \
        'option2 = new_value2.1\n' \
        '   new_value2.2\n' \
        '\n' \
        '[section2]\n' \
        'option1 = option2\n' \
        'option2 =\n' \
        '# comment option2 \n' \
        'option3 =\n' \
        '     value3.1\n' \
        '     option2\n' \
        '\n'
    assert ini_script.publish(old_value='value2', new_value='new_value2') == updated_source

    updated_source = \
        '\n' \
        '[section1]\n' \
        'option1 = value1\n' \
        '# comment\n' \
        'option2 = new_value2.1\n' \
        '   new_value2.2\n' \
        '\n' \
        '[section2]\n' \
        'option1 = new_option2\n' \
        'option2 =\n' \
        '# comment option2 \n' \
        'option3 =\n' \
        '     value3.1\n' \
        '     new_option2\n' \
        '\n'
    assert ini_script.publish(old_value='option2', new_value='new_option2') == updated_source
