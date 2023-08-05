"""
    tests.test_io
    ~~~~~~~~~~~~~

    Test Input/Output classes

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os

from docutils.io import StringOutput, FileOutput, StringInput, FileInput, NullInput

from create_python_project.io import InputDescriptor, OutputDescriptor, IOMeta


def test_io_descriptor(repo_path):
    class TestClass(metaclass=IOMeta):
        source = InputDescriptor()
        destination = OutputDescriptor()

    test = TestClass()
    assert test.source is None
    assert test.destination is None

    test.source = None
    assert isinstance(test.source, NullInput)
    test.source = 'test-string'
    assert isinstance(test.source, StringInput)
    test.source = os.path.join(repo_path, 'boilerplate_python', '__init__.py')
    assert isinstance(test.source, FileInput)

    test.destination = None
    assert isinstance(test.destination, StringOutput)
    test.destination = 'test-string'
    assert isinstance(test.destination, FileOutput)
