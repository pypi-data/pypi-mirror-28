"""
    pyutils.pep487
    ~~~~~~~~~~~~~~

    Implement patch for pep487

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

__all__ = [
    'object_with_init_subclass'
]

is_pep487_implemented = hasattr(object, '__init_subclass__')

if is_pep487_implemented:
    object_with_init_subclass = object

else:
    import types

    class pep487_type(type):
        """Base meta class for pep487"""

        def __new__(mcls, name, bases, ns, **kwargs):
            __init_subclass__ = ns.get('__init_subclass__')
            if isinstance(__init_subclass__, types.FunctionType):
                ns['__init_subclass__'] = classmethod(__init_subclass__)
            cls = super().__new__(mcls, name, bases, ns)

            for k, v in cls.__dict__.items():
                func = getattr(v, '__set_name__', None)
                if func is not None:
                    func(cls, k)
            super(cls, cls).__init_subclass__(**kwargs)
            return cls

        def __init__(self, name, bases, ns, **kwargs):
            super().__init__(name, bases, ns)

    class pep487_object(object):
        """Base object for pep487"""

        @classmethod
        def __init_subclass__(cls):
            pass

    class object_with_init_subclass(pep487_object, metaclass=pep487_type):
        """Base class to inherit from to get pep487"""
