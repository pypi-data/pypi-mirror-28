"""
    tests.scripts.test
    ~~~~~~~~~~~~~~~~~~

    Test high level function

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from create_python_project.scripts import BaseScript, \
    PyScript, PyInitScript, PySetupScript, \
    IniScript, YmlScript, \
    RSTScript, \
    get_script_class


def test_get_script_class():
    assert get_script_class('setup.py') == PySetupScript
    assert get_script_class('file.yml') == YmlScript
    assert get_script_class('tox.ini') == IniScript
    assert get_script_class('/module/script.py') == PyScript
    assert get_script_class('/module/__init__.py') == PyInitScript
    assert get_script_class('AUTHORS.rst') == RSTScript
    assert get_script_class('/module/random.rdm') == BaseScript
    assert get_script_class('/module/setup.py') == PyScript
