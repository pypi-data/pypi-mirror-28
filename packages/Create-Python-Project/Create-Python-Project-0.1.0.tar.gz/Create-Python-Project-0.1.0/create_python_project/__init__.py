"""
    create_python_project
    ~~~~~~~~~~~~~~~~~~~~~

    CLI application to facilitate Python project management

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from .git import RepositoryManager
from .project import ProjectManager

__version__ = '0.1.0'

__all__ = [
    'RepositoryManager',
    'ProjectManager',
]
