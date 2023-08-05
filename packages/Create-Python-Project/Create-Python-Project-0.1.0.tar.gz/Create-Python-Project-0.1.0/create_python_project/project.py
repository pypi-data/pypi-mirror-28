"""
    create_python_project.project
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implement ProjectManager which is the main class for manipulating a project

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from .git import RepositoryManager
from .utils import get_script, get_info, publish, \
    format_package_name, format_project_name, format_py_script_title, \
    format_url


class ProjectManager(RepositoryManager):
    """Main class for manipulating a project"""

    def get_scripts(self, *args, **kwargs):
        """Return scripts objects"""

        scripts = []
        self.apply_func(lambda blob: scripts.append(get_script(blob)), *args, **kwargs)

        return scripts

    def get_info(self, *args, **kwargs):
        """Return info objects"""

        info = []
        self.apply_func(lambda blob: info.append(get_info(blob)), *args, **kwargs)

        return info

    def publish(self, *args, **kwargs):
        """Publish modifications for multiple scripts"""

        self.apply_func(publish, *args, **kwargs)

    @property
    def setup_info(self):
        """Return information extracted from setup.py script"""

        info = self.get_info(is_filtered='setup.py')

        return info[0].code.setup

    def check_project(self):
        """Ensure there are no uncommitted modification"""

        assert not self.is_dirty(), \
            'You have uncommmitted modifications. ' \
            'Please commit or stash all modifications before setting new project\'s name'

    def change_url(self, old_url, new_url, *args, **kwargs):
        """Replace an URL in multiple scripts

        :param old_url: URL value to be replaced
        :type old_url: str
        :param new_url: New URL value
        :type new_url: str
        """

        # Perform modifications on every URL format
        for url_format in ['https+git', 'git', 'https', 'ssh']:
            self.publish(old_value=format_url(old_url, url_format),
                         new_value=format_url(new_url, url_format),
                         *args, **kwargs)

    def set_project_name(self, name):
        """Change project name

        :param name: New name of the project
        :type name: str
        """

        # Check project can be modified
        self.check_project()

        # Format project name
        new_project_name, new_package_name = format_project_name(name), format_package_name(name)

        old_info = self.setup_info

        # Rename package folder
        self.mv(old_info.packages[0].value, new_package_name)

        # Update python scripts headers title
        self.publish(is_filtered='{folder}*.py'.format(folder=new_package_name),
                     title=lambda blob: format_py_script_title(blob.path))

        # Rename imports in .py files
        self.publish(is_filtered='*.py', old_import=old_info.packages[0].value, new_import=new_package_name)

        # Replace text
        self.publish(old_value=old_info.name.value, new_value=new_project_name)
        self.publish(old_value=old_info.packages[0].value, new_value=new_package_name)
        self.publish(old_value=old_info.packages[0].value.replace('_', '-'),
                     new_value=new_package_name.replace('_', '-'))

        # Commit modifications
        message_pattern = 'refactor(all): rename project to {name}\n' \
                          '\n' \
                          '{postfix}'
        self.commit('-am', self.make_message(message_pattern, name=new_project_name))

        return new_project_name

    def set_project_author(self, author_name=None, author_email=None):
        """Change project author information

        :param author_name: Optional new author name
        :type author_name: str
        :param author_email: Optional new author email
        :type author_email: str
        """

        # Check project can be modified
        self.check_project()

        # Update setup.py info
        old_info = self.setup_info
        self.publish(is_filtered='setup.py', author=author_name, author_email=author_email)

        # Update text
        self.publish(old_value=old_info.author.value, new_value=author_name)
        self.publish(old_value=old_info.author_email.value, new_value=author_email)

        # Commit modifications
        message_pattern = 'refactor(all): rename author\n' \
                          '\n' \
                          '{name_message}' \
                          '{email_message}' \
                          '\n' \
                          '{postfix}'
        name_message = '- set author name to {name}\n'.format(name=author_name) if author_name is not None else ''
        email_message = '- set author email to {email}\n'.format(email=author_email) if author_email is not None else ''
        self.commit('-am', self.make_message(message_pattern,
                                             name_message=name_message,
                                             email_message=email_message))

        return author_name, author_email

    def set_project_url(self, url):
        """Change the url of the project

        :param url: New project URL
        :type url: str
        """

        # Check project can be modified
        self.check_project()

        # Change project url
        old_info = self.setup_info
        self.publish(is_filtered='setup.py', url=format_url(url, 'https'))  # Start by updating setup.py script
        self.change_url(old_info.url.value, url)

        # Commit modifications
        message_pattern = 'refactor(all): set project url to {url}\n' \
                          '\n' \
                          '{postfix}'
        self.commit('-am', self.make_message(message_pattern, url=format_url(url, 'https')))

        return format_url(url, 'https')

    def set_project_origin(self, new_name, new_url=None):
        """Change remote origin of the project

        It renames the remote origin and optionally creates a new remote origin with new URL

        :param new_name: Name to rename the origin to
        :type new_name: str
        :param new_url: Optional new origin URL
        :type new_url: str
        """

        # Check project can be modified
        self.check_project()

        # Renames origin
        self.remotes['origin'].rename(new_name)

        if new_url is not None:  # pragma: no branch
            # Re-creates origin
            self.create_remote('origin', new_url)

            # Update values
            self.set_project_url(url=new_url)
            self.change_url(list(self.remotes[new_name].urls)[0],
                            list(self.remotes['origin'].urls)[0])

        # Commit modifications
        message_pattern = 'refactor(all): set origin remote to {url}\n' \
                          '\n' \
                          '{postfix}'
        self.commit('-am', self.make_message(message_pattern, url=new_url))

        return new_url

    def set_project_py_script_headers(self, license=None, copyright=None):
        """Update .py script information

        :param license: New license sentence
        :type license: str
        :param copyright: New copyright sentenced
        :type copyright: str
        """

        # Check project can be modified
        self.check_project()

        # Set license and copyright
        self.publish(is_filtered='*.py', license=license, copyright=copyright)

        # Commit modifications
        message_pattern = 'refactor(all): set .py script headers\n' \
                          '\n' \
                          '{postfix}'
        self.commit('-am', self.make_message(message_pattern))
