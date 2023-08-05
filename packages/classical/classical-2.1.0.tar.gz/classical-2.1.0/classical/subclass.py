"""
Tools for creating subclasses
"""

import types


def argumented_subclass(cls: type, name: str, *args, **kwargs):
    """
    Create a subclass of ``cls`` identical to the original
    except for its name and additional arguments passed to ``__init__``

    :param cls: the class to be subclassed
    :param name: name of the new class
    :param args: positional arguments for ``__init__``
    :param kwargs: keyword arguments for ``__init__``
    :return: a subclass of ``cls``

    Say you have
    ::

        class Square:
            def __init__(self, size, color=None):
                pass  # implementation goes here

    The 'standard' way to subclass with fixed argument values would be to
    ::

        class RedSquare1x1(Square):
            def __init__(self):
                super().__init__(1, color='red)

    Consider the less-verbose alternative
    (kind of like the ``partial`` function, but for classes):
    ::

        RedSquare1x1 = argumented_subclass(Square, 'RedSquare1x1', 1, color='red')

    .. note::
        Existence of ``__slots__``
        (and, consequently, the absence of the instance ``__dict__``)
        is preserved during subclassing
    """
    def new_init(self, *_args, **_kwargs):
        cls.__init__(self, *(args + _args), **dict(kwargs, **_kwargs))

    new_init.__name__ = '__init__'

    def set_subclass_attrs(ns):
        ns['__init__'] = new_init
        if hasattr(cls, '__slots__'):
            ns['__slots__'] = ()  # no new instance attributes, so empty slots

    return types.new_class(name, (cls,), exec_body=set_subclass_attrs)


def attributed_subclass(cls: type, name: str, **attributes):
    """
    Create a subclass of ``cls`` identical to the original,
    but with additional or redefined attributes

    :param cls: the class to be subclassed
    :param name: name of the new class
    :param attributes: new attributes
    :return: a subclass of ``cls``

    ::

        class Animal:
            pass  # implementation goes here

        Bird = attributed_subclass(Animal, 'Bird', wings=2)
        pelican = Bird()  # pelican.wings == 2

    .. note::
        Existence of ``__slots__``
        (and, consequently, the absence of the instance ``__dict__``)
        is preserved during subclassing
    """
    def set_subclass_attrs(ns):
        ns.update(attributes.items())
        if hasattr(cls, '__slots__'):
            ns['__slots__'] = ()  # no new instance attributes, so empty slots

    return types.new_class(name, (cls,), exec_body=set_subclass_attrs)
