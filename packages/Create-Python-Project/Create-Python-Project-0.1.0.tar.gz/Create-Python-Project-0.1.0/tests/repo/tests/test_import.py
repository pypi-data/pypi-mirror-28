"""
    tests.test_import
    ~~~~~~~~~~~~~~~~~

    Test import are correct

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import boilerplate_python


def test_import():
    assert hasattr(boilerplate_python, '__version__')
    assert hasattr(boilerplate_python, '__all__')
