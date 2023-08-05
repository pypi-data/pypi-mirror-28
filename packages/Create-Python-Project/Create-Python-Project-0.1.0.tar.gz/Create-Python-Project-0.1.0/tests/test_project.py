"""
    tests.test_project
    ~~~~~~~~~~~~~~~~~~

    Test Project manipulation functions

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os


def test_rename_project(manager):
    assert manager.setup_info.version.value == '0.0.0'
    assert manager.setup_info.name.value == 'Boilerplate-Python'

    manager.set_project_name('New-Package-Name')

    # Test package directory has been correctly renamed
    assert os.path.isdir('new_package_name')
    info = manager.get_info(is_filtered='new_package_name/__init__.py')[0]
    assert info.docstring.title.text == 'new_package_name'

    # Test README.rst has been modified
    assert manager.get_info(is_filtered='README.rst')[0].title.text == 'New-Package-Name'

    # Test .coveragerc has been correctly modified
    publication = manager.get_scripts(is_filtered='.coveragerc')[0].publish()
    assert publication.split('\n')[2] == 'source = new_package_name'
    assert publication.split('\n')[10] == 'title = New-Package-Name coverage Report'

    # Test setup.py has been correctly modified
    assert manager.get_info(is_filtered='setup.py')[0].docstring.title.text == 'New-Package-Name'
    assert manager.setup_info.name.value == 'New-Package-Name'

    # Test modifications have been correctly committed
    assert not manager.is_dirty()


def test_set_author(manager):
    old_info = manager.setup_info

    manager.set_project_author(author_name='New Author')
    assert manager.setup_info.author.value == 'New Author'
    assert manager.setup_info.author_email.value == old_info.author_email.value

    manager.set_project_author(author_email='new@author.com')
    assert manager.setup_info.author.value == 'New Author'
    assert manager.setup_info.author_email.value == 'new@author.com'

    publication = manager.get_scripts(is_filtered='boilerplate_python/__init__.py')[0].publish()
    assert publication.split('\n')[6] == '    :copyright: Copyright 2017 by New Author.'

    assert not manager.is_dirty()


def test_set_origin(manager):
    old_urls = list(manager.remotes['origin'].urls)

    manager.set_project_origin('upstream', 'https://github.com/nmvalera/new-remote.git')
    assert list(manager.remotes['upstream'].urls) == old_urls
    assert list(manager.remotes['origin'].urls) == ['https://github.com/nmvalera/new-remote.git']

    assert manager.setup_info.url.value == 'https://github.com/nmvalera/new-remote'

    publication = manager.get_scripts(is_filtered='CONTRIBUTING.rst')[0].publish()
    assert publication.split('\n')[8] == '.. _`GitLab Issue Tracker`: https://github.com/nmvalera/new-remote/issues'

    publication = manager.get_scripts(is_filtered='setup.py')[0].publish()
    assert publication.split('\n')[25] == '    url=\'https://github.com/nmvalera/new-remote\','

    assert not manager.is_dirty()


def test_set_py_script_headers(manager):
    manager.set_project_py_script_headers(license='New license')
    publication = manager.get_scripts(is_filtered='boilerplate_python/__init__.py')[0].publish()
    assert publication.split('\n')[6] == '    :copyright: Copyright 2017 by Nicolas Maurice.'
    assert publication.split('\n')[7] == '    :license: New license'

    manager.set_project_py_script_headers(copyright='New copyright')
    publication = manager.get_scripts(is_filtered='boilerplate_python/__init__.py')[0].publish()
    assert publication.split('\n')[6] == '    :copyright: New copyright'
    assert publication.split('\n')[7] == '    :license: New license'

    assert not manager.is_dirty()
