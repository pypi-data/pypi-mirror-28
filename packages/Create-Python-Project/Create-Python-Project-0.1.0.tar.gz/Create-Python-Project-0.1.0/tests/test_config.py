"""
    tests.test_config
    ~~~~~~~~~~~~~~~~~

    Test configuration manager

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import pytest

from create_python_project.config import Config, read_config


def test_read_config(manager, config_path):
    config = read_config(config_levels=['system', 'global', 'repository'], file_paths=[config_path],
                         repo=manager, boilerplate_name='rc-config-boilerplate',
                         upstream='test-upstream', author_name='Kwarg Name',
                         boilerplate_git_url='git@github.com:nmvalera/boilerplate-kwarg.git')

    assert config.boilerplate_name == 'rc-config-boilerplate'
    assert config.author_name == 'Kwarg Name'
    assert config.author_email == 'author@rc-config.com'
    assert config.upstream == 'test-upstream'
    assert config.boilerplate_git_url == 'git@github.com:nmvalera/boilerplate-kwarg.git'


def test_config_from_kwargs():
    # Test DEFAULT boilerplate
    config = Config()
    config.from_kwargs(author_name='Author Name')
    assert config.author_name == 'Author Name'
    assert config.boilerplate_git_url is None

    config.from_kwargs(boilerplate_git_url='git@github.com:nmvalera/kwarg-boilerplate.git')
    assert config.author_name == 'Author Name'
    assert config.boilerplate_git_url == 'git@github.com:nmvalera/kwarg-boilerplate.git'


def test_config_from_git(manager):
    # Test from 'global'
    config = Config()
    config.from_git('global')
    assert config.author_name is not None
    assert config.author_email is not None
    assert config.boilerplate_git_url is None

    # Test from 'repository'
    config = Config()
    with pytest.raises(Exception):
        config.from_git('repository')

    config = Config()
    config.from_git('repository', manager)
    assert config.author_name is None
    assert config.author_email is None
    assert config.boilerplate_git_url is None


def test_config_from_file(config_path, repo_path):
    # Test DEFAULT boilerplate
    config = Config()
    config.from_file(config_path)
    assert config.boilerplate_git_url == 'git@github.com:nmvalera/rc-default-boilerplate.git'
    assert config.author_name == 'Rc Config Author'
    assert config.copyright == 'Rc Config copyright'

    # Test custom boilerplate
    config = Config('rc-config-boilerplate')
    config.from_file(config_path)
    assert config.boilerplate_git_url == 'git@github.com:nmvalera/rc-config-boilerplate.git'
    assert config.author_name == 'Rc Config Author'
    assert config.copyright == 'Rc Config copyright'

    # Test unknown boilerplate
    config = Config('unknown-boilerplate')
    config.from_file(config_path)
    assert config.boilerplate_git_url is None
    assert config.author_name == 'Rc Config Author'
    assert config.copyright == 'Rc Config copyright'

    with pytest.raises(Exception):
        config.from_file(os.path.join(repo_path, 'Makefile'))

    assert not config.from_file('unknown-file')
