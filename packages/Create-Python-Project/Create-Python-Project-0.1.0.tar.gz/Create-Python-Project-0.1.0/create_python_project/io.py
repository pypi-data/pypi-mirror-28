"""
    create_python_project.io
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Base class for input/output scripts

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

import os
from collections import OrderedDict

from docutils.io import FileInput, StringInput, NullInput, FileOutput, StringOutput


class IODescriptor:
    """Base class for Input/Output descriptors"""

    def __init__(self, name=None):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value

    def set_name(self, name):
        self._name = name


class InputDescriptor(IODescriptor):
    """Base Source descriptor

    It enables straightforward switching between inputs
    """

    def __set__(self, instance, value):
        if isinstance(value, str):
            if os.path.isfile(value):
                source = FileInput(source_path=os.path.abspath(value))
            else:
                source = StringInput(value)
        else:
            source = NullInput()
        super().__set__(instance, source)


class OutputDescriptor(IODescriptor):
    """Base Destination descriptor

    It enables straightforward switching between outputs
    """

    def __set__(self, instance, value, *args, **kwargs):
        if isinstance(value, str):
            destination = FileOutput(destination_path=os.path.abspath(value))
        else:
            destination = StringOutput(encoding='unicode')
        super().__set__(instance, destination)


class IOMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, dict(ns))

        _ios = sum([list(base._ios) for base in bases if hasattr(base, '_ios')], [])

        for name, io in ns.items():
            if isinstance(io, IODescriptor):
                io.set_name(name)
                _ios.append(io)
        cls._ios = tuple(set(_ios))

        return cls
