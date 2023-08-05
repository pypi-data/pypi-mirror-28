"""
    create_python_project.config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Configuration manager

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import configparser

from git import Repo, GitConfigParser


class Config:
    """Create-Python-Project configuration.

    The attributes of this class are the various settings that control the
    operation of create-python-project CLI.
    """

    BOILERPLATE_SECTION_NAME_FORMAT = 'boilerplate:{boilerplate_name}'

    CONFIG_OPTIONS = [
        # Options parameters for setting attributes from .rc files or git configuration
        # (attr, (rc_section, rc_option), (git_section, git_option))

        # [general]
        ('upstream', ('general', 'upstream')),

        # [author]
        ('author_name', ('author', 'name'), ('user', 'name')),
        ('author_email', ('author', 'email'), ('user', 'email')),

        # [py-headers]
        ('license', ('py-headers', 'license')),
        ('copyright', ('py-headers', 'copyright')),

        # [boilerplate:{boilerplate_name}]
        ('boilerplate_git_url', (BOILERPLATE_SECTION_NAME_FORMAT, 'url')),
    ]

    def __init__(self, boilerplate_name=None):
        """Initialize the configuration attributes to their defaults."""

        self.attempted_config_files = []
        self.attempted_git_config_level = []

        self.config_files = []

        # Set boilerplate name for .rc config
        self.boilerplate_name = boilerplate_name or 'DEFAULT'

        # Config attributes
        # general
        self.upstream = None

        # author information
        self.author_name = None
        self.author_email = None

        # py-headers information
        self.license = None
        self.copyright = None

        # boilerplate information
        self.boilerplate_git_url = None

    @property
    def config_options(self):
        return [self._format_option(opt) for opt in self.CONFIG_OPTIONS]

    def _format_option(self, opt):
        return tuple([opt[0], (opt[1][0].format(boilerplate_name=self.boilerplate_name), opt[1][1])] + list(opt[2:]))

    def from_kwargs(self, **kwargs):
        """Read config values from `kwargs`"""

        for opt in self.config_options:
            self._set_attr_from_kwargs(opt[0], kwargs)

    def from_file(self, file_path):
        """Read configuration from a .rc file.

        :param file_path: File to read configuration from
        :type file_path: str
        """

        self.attempted_config_files.append(file_path)

        config = configparser.ConfigParser()

        try:
            files_read = config.read(file_path)
        except configparser.Error as err:
            raise Exception("Couldn't read config file %s: %s" % (file_path, err))

        if not files_read:
            return False

        self.config_files.extend(files_read)

        for opt in self.config_options:
            self._set_attr_from_config(opt[0], config, opt[1])

        return True

    def from_git(self, config_level, repo=None):
        """Read config values from git configuration

        :param config_level: One of the following values
            system = system wide configuration
            global = user level configuration
            repository = configuration file for a repository (`repo` must be provided)
        :type config_level: str
        :param repo: Repo from which to retrieve config when `config_level` is set to 'repository'
        :type repo: Repo
        """

        assert config_level != 'repository' or isinstance(repo, Repo), \
            "When config_level is set to \'repository\', a valid Repo must be provided as well"

        self.attempted_git_config_level.append(config_level)

        config = GitConfigParser(Repo._get_config_path(repo, config_level), read_only=True)

        for opt in self.config_options:
            if len(opt) > 2:
                self._set_attr_from_git(opt[0], config, opt[2])

    def _set_attr_from_config(self, attr, config, where):
        if config.has_option(*where):
            setattr(self, attr, config.get(*where))

    def _set_attr_from_kwargs(self, attr, kwargs):
        value = kwargs.get(attr, None)
        if value is not None:
            setattr(self, attr, value)

    def _set_attr_from_git(self, attr, config, where):
        if config.has_option(*where):
            setattr(self, attr, config.get(*where))


def read_config(config_levels=(), file_paths=(), boilerplate_name=None, config=None, repo=None, **kwargs):
    """Read configuration from various sources

    :param config_levels: Optional git config levels (c.f. Config.from_git)
    :type config_levels: list
    :param file_paths: Optional config file to inspect to retrieve configuration from
    :type file_paths: list
    :param boilerplate_name: Optional name of the boilerplate
        (useful to indicate which section of config file to inspect)
    :type boilerplate_name: str
    :param config: Optional configuration to update when reading
    :type config: Config
    :param repo: Optional git repository to provide when `config_levels` contains 'repository'
    :param kwargs: Optional extra kwargs to read configuration from
    """
    config = config or Config(boilerplate_name)

    # set config from git information
    for config_level in config_levels:
        config.from_git(config_level, repo)

    # set config from files information
    for file_path in file_paths:
        config.from_file(file_path)

    # set config from kwargs
    config.from_kwargs(**kwargs)

    return config
