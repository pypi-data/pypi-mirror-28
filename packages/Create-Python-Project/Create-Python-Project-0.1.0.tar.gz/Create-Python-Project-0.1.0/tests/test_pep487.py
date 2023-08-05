"""
    tests.test_pep487
    ~~~~~~~~~~~~~~~~~~

    Test pep487 implementation

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from create_python_project.pyutils.pep487 import object_with_init_subclass


def test_pep487(mocker):
    class Descriptor:
        def __get__(self, instance, owner):
            pass

        def __set__(self, instance, value):
            pass

        def __set_name__(self, owner, name):
            pass

    mocker.patch.object(Descriptor, '__set_name__')

    class TestClass(object_with_init_subclass):
        descriptor = Descriptor()

    assert Descriptor.__set_name__.call_args is not None

    mocker.patch.object(TestClass, '__init_subclass__')

    class TestSubClass(TestClass):
        pass

    TestClass.__init_subclass__.call_args is not None
