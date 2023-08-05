"""
    tests.test_info
    ~~~~~~~~~~~~~~~

    Test Info implementation functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import pytest

from create_python_project.info import ComplexInfo, RSTScriptInfo, RSTTitleInfo, TextInfo, IntTupleInfo


def test_eq():
    assert not TextInfo() == IntTupleInfo()
    assert RSTTitleInfo(text='title1') != RSTTitleInfo(text='title2')


def _invalid_modification(instance, attr, value):
    with pytest.raises(Exception):
        setattr(instance, attr, value)
    assert instance == instance.copy()


def _valid_modification(instance, attr, value):
    setattr(instance, attr, value)
    assert getattr(instance, attr) == value
    assert instance == instance.copy()


def test_text_info():
    text_info = TextInfo()
    _valid_modification(text_info, 'text', 'test')
    _valid_modification(text_info, 'text', '')
    _invalid_modification(text_info, 'text', 4)
    _valid_modification(text_info, 'lineno', 234)
    _invalid_modification(text_info, 'lineno', 3.4)
    _invalid_modification(text_info, 'lineno', '4')


def test_item_tuple_info():
    class TestInfo(ComplexInfo):
        integers = IntTupleInfo()

    test = TestInfo()

    with pytest.raises(TypeError):
        test.integers = (TestInfo(),)


def test_rst_title_info():
    rst_title = RSTTitleInfo()

    _valid_modification(rst_title, 'has_overline', True)
    _invalid_modification(rst_title, 'text', '')
    _invalid_modification(rst_title, 'text', 'multi\nline\ntitle')
    _valid_modification(rst_title, 'symbol', '_')
    _invalid_modification(rst_title, 'symbol', '')
    _invalid_modification(rst_title, 'symbol', '4')
    _invalid_modification(rst_title, 'symbol', '==')


def test_rst_script_info():
    rst_script_info = RSTScriptInfo(title='title1')

    _invalid_modification(rst_script_info,
                          'title',
                          TextInfo(text='title2', lineno=5))
