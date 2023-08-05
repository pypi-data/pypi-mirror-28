"""
    tests.test_git
    ~~~~~~~~~~~~~~

    Test Git repository functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os
import re

from mock import Mock, call


def test_get_blobs(repo):
    assert len(repo.get_blobs()) == 24


def test_mv(repo):
    old_folder = 'boilerplate_python'
    assert os.path.isdir(old_folder)
    old_blobs = repo.get_blobs(is_filtered='{folder}*'.format(folder=old_folder))

    new_folder = 'boilerplate_python_test'
    repo.mv(old_folder, new_folder)

    assert os.path.isdir(new_folder)
    assert not os.path.isdir('boilerplate_python')
    assert repo.get_blobs(is_filtered='{folder}*'.format(folder=new_folder)) == old_blobs


def _test_apply_func(repo, calls_count, is_filtered=None):
    args, kwargs, func = (Mock(return_value='arg'), 'test'), \
        {'keyword': Mock(return_value='kwarg'),
         'test': 'test'}, Mock()
    repo.apply_func(func, is_filtered=is_filtered, *args, **kwargs)

    assert args[0].call_args_list == kwargs['keyword'].call_args_list
    calls = [call(blob[0][0], 'arg', 'test', keyword='kwarg', test='test') for blob in args[0].call_args_list]
    assert func.call_args_list == calls
    assert len(calls) == calls_count


def test_apply_func(repo):
    _test_apply_func(repo, 24)
    _test_apply_func(repo, 1, is_filtered='boilerplate_python*')
    _test_apply_func(repo, 5, is_filtered=['*.py'])
    _test_apply_func(repo, 2, is_filtered=lambda blob: re.compile('setup').match(blob.path))


def test_tags(repo):
    assert len(repo.get_tags()) == 12


def test_get_commits(repo):
    assert len(repo.get_commits()) == 24
    assert len(repo.get_commits('v1.0.1')) == 11
    assert len(repo.get_commits('v0.0.2')) == 19


def test_push(repo):
    repo.push()
    assert repo.git.push.call_args == (('--follow-tags',),)
    repo.push(push_tags=False)
    assert repo.git.push.call_args == ()
