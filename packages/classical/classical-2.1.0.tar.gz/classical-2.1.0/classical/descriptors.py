"""
Descriptors/properties for classes
"""

import copy
from typing import Optional, Tuple

from .subclass import argumented_subclass, attributed_subclass


class FactoryProperty:
    """
    A descriptor that returns an object related to the owner class
    and created by ``factory`` when accessed.

    :param factory: the object factory. Should have the following signature:
        ``factory(cls, name, *args, **kwargs)``.
        For example, :func:`~classical.subclass.argumented_subclass`
        can be used here
    :param args: positional arguments for ``factory``
    :param kwargs: keyword arguments for ``factory``

    ``FactoryProperty`` is the base class for:

        - :class:`~classical.descriptors.ArgumentedSubclass`
        - :class:`~classical.descriptors.AttributedSubclass`
        - :class:`~classical.descriptors.AutoProperty`
        - :class:`~classical.descriptors.DummySubclass`
    """

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        self.args = args
        self.kwargs = kwargs
        self._cls_map = {}
        self._name = None  # type: str
        self._owner = None  # type: type
        self._is_terminal = False

    def __set_name__(self, owner: type, name: str):
        self._name = name
        self._owner = owner

    def _get_owner_and_name(self, owner: type) -> Tuple[Optional[type], Optional[str]]:
        """Resolve the original owner and name of the attribute"""
        try:
            own_name = [
                name for name, attr in owner.__dict__.items()
                if attr is self
            ][0]
            return owner, own_name

        except IndexError:
            for base in owner.__bases__:
                original_owner, own_name = self._get_owner_and_name(base)
                if own_name:
                    return original_owner, own_name

        return None, None

    def __get__(self, instance, owner):
        if self._name is None:  # has not been set yet
            # get the name of the attribute - it will serve as the name
            # of the new partial class
            original_owner, own_name = self._get_owner_and_name(owner)
            if not own_name:
                raise RuntimeError('Property is not bound to any class')

            self.__set_name__(owner=original_owner, name=own_name)

        if self._is_terminal:
            # always return subclass of the original owner
            owner = self._owner

        if owner not in self._cls_map:
            self._cls_map[owner] = self.factory(owner, self._name, *self.args, **self.kwargs)

        return self._cls_map[owner]

    @property
    def terminal(self) -> 'FactoryProperty':
        """
        Return a "terminal" version of the property:
        if the owner class is subclassed, the object factory will be applied
        to the original owner of the property instead of the subclass

        Consider:
        ::

            class Thing:
                my_thing = AutoProperty()
                terminal_thing = AutoProperty().terminal

            class ClassyThing(Thing):
                pass

            isinstance(ClassyThing.my_thing, ClassyThing)  # True
            isinstance(ClassyThing.terminal_thing, ClassyThing)  # False

            ClassyThing.my_thing.__class__  # ClassyThing
            ClassyThing.terminal_thing.__class__  # Thing

        """
        self_copy = copy.copy(self)
        self_copy._is_terminal = True
        return self_copy


class DummySubclass(FactoryProperty):
    """
    A descriptor that returns a copy of the owner class when accessed
    (but with a new name equal to the attribute's name).
    """

    def __init__(self):
        super().__init__(argumented_subclass)


class ArgumentedSubclass(FactoryProperty):
    """
    A descriptor that returns an :func:`~classical.subclass.argumented_subclass`
    of the owner class when accessed.

    It allows a class to have attributes that are its own subclasses
    with additional arguments passed to ``__init__``:
    ::

        class Tree:
            Peach = ArgumentedSubclass(fruit='peach')
            Pine = ArgumentedSubclass(fruit='cone')
            # both will return subclasses of Tree when accessed

            def __init__(self, fruit):
                self.fruit = fruit

        issubclass(Tree.Pine, Tree)  # True
        Tree.Pine().fruit  # 'cone'

    These properties can be used recursively in combination with each other:
    ::

        class Polygon:
            Blue = ArgumentedSubclass(color='blue')
            Pentagon = ArgumentedSubclass(sides=5)

            def __init__(self, color=None, sides=3):
                self.color = color
                self.sides = sides

        blue_pentagon = Polygon.Pentagon.Blue()
        # blue_pentagon.color == 'blue'
        # blue_pentagon.sides == 5
    """

    def __init__(self, *args, **kwargs):
        super().__init__(argumented_subclass, *args, **kwargs)


class AttributedSubclass(FactoryProperty):
    """
    A descriptor that returns an :func:`~classical.subclass.attributed_subclass`
    of the owner class when accessed.

    It allows a class to have attributes that are its own subclasses
    with additional or redefined class attributes:
    ::

        class Paint:
            solvent = None

            Oil = AttributedSubclass(solvent='turpentine')
            Watercolor = AttributedSubclass(solvent='water')

        issubclass(Paint.Oil, Paint)  # True
        Paint.Oil.solvent  # 'turpentine'

    These properties can be used recursively and in combination with one another.
    """

    def __init__(self, **attributes):
        super().__init__(attributed_subclass, **attributes)


def _instance_factory(cls, name, *args, **kwargs):
    return cls(*args, **kwargs)


class AutoProperty(FactoryProperty):
    """
    A descriptor that returns an instance of the owner class when accessed.

    The instance is created with the custom arguments
    that are passed to the property's constructor.

    Acts somewhat like an ``Enum``
    ::

        class Thing:
            book = AutoProperty(color='brown', size=5)
            pencil = AutoProperty(color='green', size=1)
            # both will return instances of Thing when accessed

            def __init__(self, color, size):
                self.color = color
                self.size = size

        isinstance(Thing.book, Thing)  # True
        Thing.book.color  # 'brown'
        Thing.book is Thing.book  # True (the same instance is returned every time)

    These properties can be used in a subclass to produce instances of the subclass:
    ::

        class ClassyThing(Thing):
            pass

        isinstance(ClassyThing.book, ClassyThing)  # True

    Use ``AutoProperty(...).terminal`` to produce instances
    of the **original owner** class inside a subclass:
    ::

        class Thing:
            terminal_thing = AutoProperty().terminal

        class ClassyThing(Thing):
            pass

        isinstance(ClassyThing.terminal_thing, ClassyThing)  # False
        ClassyThing.terminal_thing.__class__  # Thing
    """

    def __init__(self, *args, **kwargs):
        super().__init__(_instance_factory, *args, **kwargs)
