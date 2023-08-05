"""
    tests.conftest
    ~~~~~~~~~~~~~~

    Implements fixture for tests

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import logging
import os
import shutil

import pytest
import semver
from click.testing import CliRunner
from git import Git

from create_python_project import RepositoryManager, ProjectManager

DIR_NAME = os.path.dirname(__file__)


@pytest.fixture(scope='function')
def config_path():
    yield os.path.join(DIR_NAME, 'config', '.crpyprojrc')


@pytest.fixture(scope='function')
def repo_path():
    # Set Directory to test repository to ensure consistency in tests
    initial_dir = os.getcwd()
    _test_repo = os.path.join(DIR_NAME, 'repo')
    os.chdir(_test_repo)

    yield _test_repo

    os.chdir(initial_dir)


def _prepare_repo(repo_class, repo_path, mocker, monkeypatch, caplog):
    with caplog.at_level(logging.ERROR):  # Set log level to avoid to overcharge logs with GitPython logs
        # Initialize repository for testing
        repo = repo_class.init(path=repo_path)

        # Monkey patch and Mock _repo.git.push function so we do not need to effectively push to remotes during tests.
        # We cannot patch the git.push function due to GitPython implementation of Git class with __slots__
        # (c.f. https://github.com/gitpython-developers/GitPython/blob/master/git/cmd.py)
        # So we need to monkey path the full _repo.git attribute
        class MockGit(Git):
            def push(self, *args, **kwargs):
                pass

        monkeypatch.setattr(repo, 'git', value=MockGit(repo.working_dir))
        mocker.patch.object(repo.git, 'push')

        # Add files, commits and tags to the repository
        version = '0.0.0'
        for i, file in enumerate(repo.untracked_files):
            repo.git.add(file)
            repo.git.commit(file, '-m', 'add {file}'.format(file=file))
            if i % 2 == 0:
                repo.create_tag('v{version}'.format(version=version),
                                message='Release v{version}'.format(version=version))
                if i > 0 and i % 8 == 0:
                    version = semver.bump_major(version)
                elif i > 0 and i % 4 == 0:
                    version = semver.bump_minor(version)
                else:
                    version = semver.bump_patch(version)

        repo.create_remote('origin', 'git@github.com:nmvalera/boilerplate-python.git')
    return repo


def _finalize_repo(repo, repo_path, initial_commit):
    # Reset changes performed during tests
    repo.git.reset('--hard', initial_commit)
    shutil.rmtree(os.path.join(repo_path, '.git'))


@pytest.fixture(scope='function')
def repo(repo_path, monkeypatch, mocker, caplog):
    _repo = _prepare_repo(RepositoryManager, repo_path, mocker, monkeypatch, caplog)

    initial_commit = _repo.head.commit

    yield _repo

    _finalize_repo(_repo, repo_path, initial_commit)


@pytest.fixture(scope='function')
def manager(repo_path, monkeypatch, mocker, caplog):
    _manager = _prepare_repo(ProjectManager, repo_path, mocker, monkeypatch, caplog)

    initial_commit = _manager.head.commit

    yield _manager

    _finalize_repo(_manager, repo_path, initial_commit)


@pytest.fixture(scope='function')
def cli_runner(mocker, manager):
    _cli_runner = CliRunner()

    # mock clone_from function
    mocker.patch.object(ProjectManager, 'clone_from', return_value=manager)

    yield _cli_runner
