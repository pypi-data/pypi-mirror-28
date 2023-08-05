"""
    tests.scripts.test_rst
    ~~~~~~~~~~~~~~~~~~~~~~

    Test RSTScript functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest

from create_python_project.scripts import RSTScript
from create_python_project.info import RSTScriptInfo, RSTTitleInfo


def test_rst_script(repo_path):
    rst_script = RSTScript()
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for filename in filenames:
            if filename.split('.')[-1] == 'rst':
                rst_script.set_source(os.path.join(dirpath, filename))
                assert rst_script.source.source_path == os.path.join(dirpath, filename)
                assert rst_script.publish() is not None


def test_rst_script_title(repo_path):
    rst_script = RSTScript()
    rst_script.set_source(os.path.join(repo_path, 'AUTHORS.rst'))
    rst_script.publish()
    assert rst_script.content.info.title is None

    rst_script.set_source(os.path.join(repo_path, 'CONTRIBUTING.rst'))
    rst_script.publish()
    assert rst_script.content.info.title.text == 'Contributing guidelines'
    assert rst_script.content.info.title.lineno == 0
    assert rst_script.content.info.title.symbol == '='
    assert rst_script.content.info.title.has_overline == False

    rst_script.set_source('`````````\nOld Title\n`````````\n\nparagraph\nparagraph')
    rst_script.publish()
    assert rst_script.content.info.title.text == 'Old Title'
    assert rst_script.content.info.title.lineno == 1
    assert rst_script.content.info.title.symbol == '`'
    assert rst_script.content.info.title.has_overline == True

    rst_script.set_source(os.path.join(repo_path, 'LICENSE.rst'))
    rst_script.publish()
    assert rst_script.content.info.title is None


def _test_invalid_rst_change_title(text=None, symbol=None):
    rst_script = RSTScript()
    rst_script.set_source('Old Title\n~~~~~~~~~\n\nparagraph\nparagraph')
    rst_script.publish()
    text = text if text is not None else rst_script.content.info.title.text
    symbol = symbol if symbol is not None else rst_script.content.info.title.symbol

    with pytest.raises(Exception):
        new_info = RSTScriptInfo(title=RSTTitleInfo(text=text,
                                                    symbol=symbol,
                                                    lineno=rst_script.content.info.title.lineno,
                                                    has_overline=rst_script.content.info.title.has_overline))
        rst_script.publish(new_info=new_info)


def _test_valid_rst_change_title(source, text=None, symbol=None):
    rst_script = RSTScript()
    rst_script.set_source(source)
    rst_script.publish()

    text = text if text is not None else rst_script.content.info.title.text
    symbol = symbol if symbol is not None else rst_script.content.info.title.symbol
    new_info = RSTScriptInfo(title=RSTTitleInfo(text=text,
                                                symbol=symbol,
                                                lineno=rst_script.content.info.title.lineno,
                                                has_overline=rst_script.content.info.title.has_overline))
    publication = rst_script.publish(new_info=new_info)
    assert rst_script.content.info.title.text == text
    assert rst_script.content.info.title.symbol == symbol
    return publication


def test_rst_change_title():
    new_text = 'New Long Title\n~~~~~~~~~~~~~~\n\nparagraph\nparagraph'
    assert _test_valid_rst_change_title('Old Title\n~~~~~~~~~\n\nparagraph\nparagraph',
                                        text='New Long Title') == new_text

    new_text = '+++++++++\nOld Title\n+++++++++\n\nparagraph\nparagraph'
    assert _test_valid_rst_change_title('`````````\nOld Title\n`````````\n\nparagraph\nparagraph',
                                        symbol='+') == new_text

    new_text = 'Old Title\n~~~~~~~~~\n\nparagraph\nparagraph'
    assert _test_valid_rst_change_title('Old Title\n~~~~~~~~~\n\nparagraph\nparagraph', text=None) == new_text

    _test_invalid_rst_change_title(text='')
    _test_invalid_rst_change_title(text='title\n~~~~~')
    _test_invalid_rst_change_title(text=5)
    _test_invalid_rst_change_title(symbol='++++')
