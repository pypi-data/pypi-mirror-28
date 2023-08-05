"""
    Create-Python-Project
    ~~~~~~~~~~~~~~~~~~~~~

    Create-Python-Project is a CLI application to facilitate Python project management

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see LICENSE.rst for more details.
"""

import os

from setuptools import setup, find_packages


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ''


setup(
    name='Create-Python-Project',
    version='0.1.0',
    license=read('LICENSE.rst'),
    url='https://github.com/nicolas-maurice/create-python-project',
    author='Nicolas Maurice',
    author_email='nicolas.maurice.valera@gmail.com',
    description='Create-Python-Project is a CLI application to facilitate Python project management',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'click==6.3',
        'docutils==0.14.0',
        'gitpython==2.1.7',
        'semver==2.7.9',
        'twine==1.9.1',
        'pyyaml==3.12.0'
    ],
    extras_require={
        'dev': [
            'autoflake',
            'autopep8',
            'coverage',
            'flake8',
            'mock==2.0.0',
            'pytest>=3',
            'pytest-mock==1.6.3',
            'tox==2.9.1',
            'sphinx',
        ],
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    entry_points='''
        [console_scripts]
        create-python-project=create_python_project.cli:cli
    '''
)
