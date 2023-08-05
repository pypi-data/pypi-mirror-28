"""
    create_python_project.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements utilities functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import fnmatch
import re
from collections import OrderedDict

from .scripts import get_script_class


def get_script(blob):
    """Get a script object from a blob

    :param blob: Blob to get a script from
    :type blob:
    """
    return get_script_class(blob.path)(source=blob.abspath)


def read(blob):
    """Read a blob

    :param blob: Blob to read
    :type blob:
    """
    script = get_script(blob)
    script.read()
    return script


def get_info(blob):
    """Get script info

    :param blob: Blob to get a info from
    :type blob:
    """
    return read(blob).content.info


def publish(blob, *args, **kwargs):
    """Publish a blob

    :param blob: Blob to publish
    :type blob:
    """
    script = read(blob)
    script.set_destination(destination=kwargs.pop('destination', blob.abspath))
    publication = script.publish(*args, **kwargs)
    return publication


def is_matching(patterns, blob):
    """Tests if a blob's path and a str path are the same

    It is also possible to provide a list of str paths then it tests if the blob's path is in the list

    :param path: Path or list of path
    :type path: str or list
    :param blob: Blob to test
    :type blob:
    :rtype: bool
    """
    for pattern in patterns:
        if re.match(fnmatch.translate(pattern), blob.path):
            return True
    return False


def format_package_name(name):
    return name.lower().replace('-', '_')


def format_project_name(name):
    return '-'.join([word.capitalize() for word in name.split('-')])


def format_py_script_title(path):
    parts = path.split('/')
    return '.'.join(parts[:-1] + ([] if parts[1] == '__init__.py' else [parts[-1].split('.')[0]]))


URL_PATTERNS = OrderedDict([
    ('https+git', re.compile('https://(?P<domain>.+)/(?P<owner>.+)/(?P<repo>.+).git')),
    ('https', re.compile('https://(?P<domain>.+)/(?P<owner>.+)/(?P<repo>.+)')),
    ('ssh', re.compile('git@(?P<domain>.+):(?P<owner>.+)/(?P<repo>.+).git')),
    ('git', re.compile('git://(?P<domain>.+)/(?P<owner>.+)/(?P<repo>.+).git')),
])

URL_FORMATS = {
    'https': 'https://{domain}/{owner}/{repo}',
    'https+git': 'https://{domain}/{owner}/{repo}.git',
    'ssh': 'git@{domain}:{owner}/{repo}.git',
    'git': 'git://{domain}/{owner}/{repo}.git'
}


def is_git_url(url):
    for format in ['https+git', 'ssh', 'git']:
        if URL_PATTERNS[format].match(url):
            return True
    return False


def format_url(url, format):
    assert format in URL_FORMATS.keys(), \
        'URL compatible formats are \'git\', \'https\' or \'ssh\' but you passed {0}'.format(format)

    for pattern in URL_PATTERNS.values():
        match = pattern.match(url)
        if match:
            return URL_FORMATS[format].format(**match.groupdict())

    raise AssertionError('Impossible to format url {0}'.format(url))
