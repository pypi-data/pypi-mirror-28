"""
    tests.test_vli
    ~~~~~~~~~~~~~~

    Test CLI application

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import click

from create_python_project import ProjectManager
from create_python_project.cli import cli, Progress


def test_progress(cli_runner):
    progress = Progress()

    @click.command()
    @click.option('-c', 'op_code', type=int)
    @click.argument('line')
    def test(op_code, line):
        if op_code is None:
            progress.line_dropped(line)
        else:
            progress._cur_line = line
            progress.update(op_code)

    result = cli_runner.invoke(test, ['Line'])
    assert not result.exception
    assert result.output == 'Line\n'

    result = cli_runner.invoke(test, ['-c', 4, 'Current Line'])
    assert not result.exception
    assert result.output == ''

    result = cli_runner.invoke(test, ['-c', 34, 'Current Line'])
    assert not result.exception
    assert result.output == 'Current Line\n'


def test_new_with_kwargs(cli_runner, manager):
    result = cli_runner.invoke(cli, ['new',
                                     '-b', 'git@github.com:nmvalera/kwarg-boilerplate.git',
                                     '-u', 'https://github.com/nmvalera/new-project-name.git',
                                     '-a', 'New Kwarg Author',
                                     '-e', 'new@kwarg-author.com',
                                     'new-project-name'])

    assert result.exit_code == 0

    # Test clone from has been correctly called
    call = ProjectManager.clone_from.call_args_list[0]
    assert call[1]['url'] == 'git@github.com:nmvalera/kwarg-boilerplate.git'
    assert call[1]['to_path'] == 'new-project-name'

    # Test remotes have been correctly updated
    assert list(manager.remotes['origin'].urls) == ['https://github.com/nmvalera/new-project-name.git']

    # Test project has been correctly renamed
    assert manager.get_info(is_filtered='README.rst')[0].title.text == 'New-Project-Name'
    assert manager.get_info(is_filtered='new_project_name/__init__.py')[0].docstring.title.text == 'new_project_name'

    # Test author has been correctly renamed
    assert manager.setup_info.author.value == 'New Kwarg Author'
    assert manager.setup_info.author_email.value == 'new@kwarg-author.com'


def test_new_with_no_kwargs(cli_runner, manager, config_path):
    result = cli_runner.invoke(cli, ['--config-file', config_path,
                                     'new',
                                     '-u', 'https://github.com/nmvalera/new-project-name.git',
                                     'new-project-name'])

    assert result.exit_code == 0

    # Test clone from has been correctly called
    call = ProjectManager.clone_from.call_args_list[0]
    assert call[1]['url'] == 'git@github.com:nmvalera/rc-default-boilerplate.git'
    assert call[1]['to_path'] == 'new-project-name'

    # Test remotes have been correctly updated
    assert list(manager.remotes['origin'].urls) == ['https://github.com/nmvalera/new-project-name.git']

    # Test project has been correctly renamed
    assert manager.get_info(is_filtered='README.rst')[0].title.text == 'New-Project-Name'
    assert manager.get_info(is_filtered='new_project_name/__init__.py')[0].docstring.title.text == 'new_project_name'

    # Test author has been correctly renamed
    assert manager.setup_info.author.value == 'Rc Config Author'
    assert manager.setup_info.author_email.value == 'author@rc-config.com'


def test_new_with_error(cli_runner):
    result = cli_runner.invoke(cli, ['--config-file', 'unknown-file',
                                     'new',
                                     '-u', 'https://github.com/nmvalera/new-project-name.git',
                                     'new-project-name'])

    assert result.exit_code == 1
