"""
    create_python_project.cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement command line interface for Create-Python-Project

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

import click
import git

from .config import read_config
from .project import ProjectManager
from .utils import is_git_url

# Location of the configuration file
CONFIG_FILE_NAME = '.crpyprojrc'
CONFIG_FILE_LOCATION = os.path.join(os.path.expanduser('~'), CONFIG_FILE_NAME)


class Progress(git.RemoteProgress):
    """Allow to output git log when cloning project"""

    def line_dropped(self, line):
        click.echo(line)

    def update(self, op_code, *args, **kwargs):
        if op_code & self.END:
            click.echo(self._cur_line)


@click.group()
@click.option('--config-file', 'file_path',
              help='Custom path to the configuration file',
              default=CONFIG_FILE_LOCATION)
@click.pass_context
def cli(ctx, file_path):
    ctx.obj = read_config(config_levels=['system', 'global'], file_paths=[file_path])


@cli.command(name='new')
@click.option('--boilerplate', '-b', 'boilerplate_git_url',
              type=str,
              default='DEFAULT',
              help='Git URL of the repository to clone a project from or '
                   'name of the boilerplate as indicated in ~/.crpyprojrc file')
@click.option('--git-url', '-u', 'project_git_url',
              type=str,
              help='Git URL of your project')
@click.option('--upstream', 'upstream',
              type=str,
              help='Name of the upstream to rename the origin remote to',
              default='boilerplate')
@click.option('--author-name', '-a', 'author_name',
              type=str,
              help='Author of the project')
@click.option('--author-email', '-e', 'author_email',
              type=str,
              help='Author\'s email of the project')
@click.argument('project_name',
                type=str,
                required=True)
@click.pass_obj
@click.pass_context
def new(ctx, config, boilerplate_git_url, project_git_url, project_name, **kwargs):
    """Creates a new project"""

    if is_git_url(boilerplate_git_url):
        config = read_config(config=config,
                             boilerplate_git_url=boilerplate_git_url,
                             **kwargs)
    else:
        config = read_config(config=config,
                             boilerplate_name=boilerplate_git_url,
                             **kwargs)

        # ensure a valid git url to clone the project from has been provided
        if config.boilerplate_git_url is None or not is_git_url(config.boilerplate_git_url):
            click.secho('Could not find a valid git URL for boilerplate \'{name}\' in {location} config file(s). '
                        'Please ensure you have correctly set up a configuration file with a [boilerplate:{name}] '
                        'section containing a valid \'url\' option.'.format(name=boilerplate_git_url,
                                                                            location=config.attempted_config_files),
                        fg='red')
            ctx.exit(1)

    click.echo('Creating new project {name} from {git_url}...'.format(name=project_name,
                                                                      git_url=config.boilerplate_git_url))

    # Clone boilerplate
    manager = ProjectManager.clone_from(url=config.boilerplate_git_url, to_path=project_name, progress=Progress())

    # Set project origins
    click.echo("Contextualizing project...")
    if project_git_url is not None:  # pragma: no branch
        manager.set_project_origin(config.upstream, project_git_url)
        click.echo('- Set project remote origin to {url}'.format(url=project_git_url))

    # Rename project
    new_name = manager.set_project_name(project_name)
    click.echo('- Project name has been set to {name}'.format(name=new_name))

    # Rename author
    if config.author_name is not None:  # pragma: no branch
        manager.set_project_author(author_name=config.author_name)
        click.echo('- Project author\'s name has been set to {name}'.format(name=config.author_name))

    if config.author_email is not None:  # pragma: no branch
        manager.set_project_author(author_email=config.author_email)
        click.echo('- Project author\'s email has been set to {email}'.format(email=config.author_email))

    click.secho('Project successfully created!! Happy coding! :-)', fg='green')
