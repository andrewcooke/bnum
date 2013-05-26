
'''
Based on Enum code, (c) 2013 Ethan Furman, ethan@stoneleaf.us
Modifications (c) 2013 Andrew Cooke, andrew@acooke.org
'''
from itertools import count

import sys
from collections import OrderedDict, defaultdict
from types import MappingProxyType
from enum import _StealthProperty, dunder, break_noisily_on_pickle, \
    _EnumDict

__all__ = ['Bnum']


# dummy value for Bnum as BnumMeta explicity checks for it, but of course until
# BnumMeta finishes running the first time the Bnum class doesn't exist.  This
# is also why there are checks in EnumMeta like `if Bnum is not None`
Bnum = None


class BnumMeta(type):
    """Metaclass for Bnum"""

    @classmethod
    def __prepare__(metacls, cls, bases):
        # return _EnumDict()
        return defaultdict(count().__next__)

    def __new__(metacls, cls, bases, classdict):
        # a Bnum class is final once enumeration items have been defined; it
        # cannot be mixed with other types (int, float, etc.) if it has an
        # inherited __new__ unless a new __new__ is defined (or the resulting
        # class will fail).
        print(classdict)
        print(classdict.keys())
        return type.__new__(metacls, cls, bases, dict(classdict))
    #     obj_type, first_enum = metacls._get_mixins(bases)
    #     __new__, save_new, use_args = (
    #         metacls._find_new(classdict, obj_type, first_enum)
    #     )
    #
    #     # save enum items into separate mapping so they don't get baked into
    #     # the new class
    #     print(classdict)
    #     print(classdict.keys())
    #     name_value = {k: classdict[k] for k in classdict._enum_names}
    #     for name in classdict._enum_names:
    #         del classdict[name]
    #
    #     # check for illegal enum names (any others?)
    #     if set(name_value) & {'mro', '_create', '_get_mixins', '_find_new'}:
    #         raise ValueError("The names 'mro', '_create', '_get_mixins', and "
    #                          "'_find_new' cannot be used for members")
    #
    #     # add _name attributes to any _StealthProperty's for nicer exceptions
    #     for name, value in classdict.items():
    #         if isinstance(value, _StealthProperty):
    #             value._name = name
    #
    #     # create our new Bnum type
    #     enum_class = super().__new__(metacls, cls, bases, classdict)
    #     enum_names = []
    #     enum_map = OrderedDict()
    #     enum_value_map = {}                         # hashable value:name map
    #     enum_class._enum_names = enum_names         # names in definition order
    #     enum_class._enum_map = enum_map             # name:value map
    #     enum_class._enum_value_map = enum_value_map # value:name map
    #
    #     # check for a __getnewargs__, and if not present sabotage
    #     # pickling, since it won't work anyway
    #     if (
    #                 obj_type is not object and
    #                 obj_type.__dict__.get('__getnewargs__') is None
    #     ):
    #         enum_class.__reduce__ = break_noisily_on_pickle
    #         enum_class.__module__ = 'uh uh'
    #
    #     # instantiate them, checking for duplicates as we go
    #     # we instantiate first instead of checking for duplicates first in case
    #     # a custom __new__ is doing something funky with the values -- such as
    #     # auto-numbering ;)
    #     for e in classdict._enum_names:
    #         value = name_value[e]
    #         if not isinstance(value, tuple):
    #             args = (value, )
    #         else:
    #             args = value
    #         if obj_type is tuple:   # special case for tuple enums
    #             args = (args, )     # wrap it one more time
    #         if not use_args:
    #             enum_item = __new__(enum_class)
    #             enum_item._value = value
    #         else:
    #             enum_item = __new__(enum_class, *args)
    #             if not hasattr(enum_item, '_value'):
    #                 enum_item._value = obj_type(*args)
    #         enum_item._obj_type = obj_type
    #         enum_item._name = e
    #         enum_item.__init__(*args)
    #         # look for any duplicate values, and, if found, use the already
    #         # created enum item instead of the new one so `is` will work
    #         # (i.e. Color.green is Color.grene)
    #         for name, canonical_enum in enum_map.items():
    #             if canonical_enum.value == enum_item._value:
    #                 enum_item = canonical_enum
    #                 break
    #         else:
    #             enum_names.append(e)
    #         enum_map[e] = enum_item
    #         try:
    #             enum_value_map[value] = enum_item
    #         except TypeError:
    #             pass
    #
    #     # double check that repr and friends are not the mixin's or various
    #     # things break (such as pickle)
    #     for name in ('__repr__', '__str__', '__getnewargs__'):
    #         class_method = getattr(enum_class, name)
    #         obj_method = getattr(obj_type, name, None)
    #         enum_method = getattr(first_enum, name, None)
    #         if obj_method is not None and obj_method is class_method:
    #             setattr(enum_class, name, enum_method)
    #
    #     # replace any other __new__ with our own (as long as Enum is not None,
    #     # anyway) -- again, this is to support pickle
    #     if Bnum is not None:
    #         # if the user defined their own __new__, save it before it gets
    #         # clobbered in case they subclass later
    #         if save_new:
    #             enum_class.__new_member__ = __new__
    #         enum_class.__new__ = Bnum.__new__
    #     return enum_class
    #
    # def __call__(cls, value, names=None, *, module=None, type=None):
    #     """Either returns an existing member, or creates a new enum class.
    #
    #     This method is used both when an enum class is given a value to match
    #     to an enumeration member (i.e. Color(3)) and for the functional API
    #     (i.e. Color = Enum('Color', names='red green blue')).
    #
    #     When used as the functional API module, if set, will be stored in the
    #     new class' __module__ attribute; type, if set, will be mixed in as the
    #     first base class.
    #
    #     Note: if module is not set this routine will attempt to discover the
    #     calling module by walking the frame stack; if this is unsuccessful
    #     the resulting class will not be pickleable.
    #
    #     """
    #     if names is None:  # simple value lookup
    #         return cls.__new__(cls, value)
    #         # otherwise, we're creating a new Enum type
    #     return cls._create(value, names, module=module, type=type)
    #
    # def __contains__(cls, enum_item):
    #     return isinstance(enum_item, cls) and enum_item.name in cls._enum_map
    #
    # def __dir__(self):
    #     return ['__class__', '__doc__', '__members__'] + self._enum_names
    #
    # @property
    # def __members__(cls):
    #     """Returns a MappingProxyType of the internal _enum_map structure."""
    #
    #     return MappingProxyType(cls._enum_map)
    #
    # def __getattr__(cls, name):
    #     """Return the enum member matching `name`
    #
    #     We use __getattr__ instead of descriptors or inserting into the enum
    #     class' __dict__ in order to support `name` and `value` being both
    #     properties for enum members (which live in the class' __dict__) and
    #     enum members themselves.
    #
    #     """
    #
    #     if dunder(name):
    #         raise AttributeError(name)
    #     try:
    #         return cls._enum_map[name]
    #     except KeyError:
    #         raise AttributeError(name) from None
    #
    # def __getitem__(cls, name):
    #     return cls._enum_map[name]
    #
    # def __iter__(cls):
    #     return (cls._enum_map[name] for name in cls._enum_names)
    #
    # def __len__(cls):
    #     return len(cls._enum_names)
    #
    # def __repr__(cls):
    #     return "<enum %r>" % cls.__name__
    #
    # def _create(cls, class_name, names=None, *, module=None, type=None):
    #     """Convenience method to create a new Enum class.
    #
    #     Called by __new__, with the same arguments, to provide the
    #     implementation.  Easier to subclass this way.
    #
    #     """
    #     metacls = cls.__class__
    #     bases = (cls, ) if type is None else (type, cls)
    #     classdict = metacls.__prepare__(class_name, bases)
    #
    #     # special processing needed for names?
    #     if isinstance(names, str):
    #         names = names.replace(',', ' ').split()
    #     if isinstance(names, (tuple, list)) and isinstance(names[0], str):
    #         names = [(e, i) for (i, e) in enumerate(names, 1)]
    #
    #     # otherwise names better be an iterable of (name, value) or a mapping
    #     for item in names:
    #         if isinstance(item, str):
    #             e, v = item, names[item]
    #         else:
    #             e, v = item
    #         classdict[e] = v
    #     enum_class = metacls.__new__(metacls, class_name, bases, classdict)
    #
    #     # TODO: replace the frame hack if a blessed way to know the calling
    #     # module is ever developed
    #     if module is None:
    #         try:
    #             module = sys._getframe(2).f_globals['__name__']
    #         except (AttributeError, ValueError) as exc:
    #             pass
    #     if module is None:
    #         enum_class.__module__ = 'uh uh'
    #         enum_class.__reduce__ = break_noisily_on_pickle
    #     else:
    #         enum_class.__module__ = module
    #
    #     return enum_class
    #
    # @staticmethod
    # def _get_mixins(bases):
    #     """Returns the type for creating enum members, and the first inherited
    #     enum class.
    #
    #     bases: the tuple of bases that was given to __new__
    #
    #     """
    #     if not bases:
    #         return object, Bnum
    #
    #     # double check that we are not subclassing a class with existing
    #     # enumeration members; while we're at it, see if any other data
    #     # type has been mixed in so we can use the correct __new__
    #     obj_type = first_enum = None
    #     for base in bases:
    #         if  (base is not Bnum and
    #                  issubclass(base, Bnum) and
    #                  base._enum_names):
    #             raise TypeError("Cannot extend enumerations")
    #         # base is now the last base in bases
    #     if not issubclass(base, Bnum):
    #         raise TypeError("new enumerations must be created as "
    #                         "`ClassName([mixin_type,] enum_type)`")
    #
    #     # get correct mix-in type (either mix-in type of Bnum subclass, or
    #     # first base if last base is Bnum)
    #     if not issubclass(bases[0], Bnum):
    #         obj_type = bases[0]     # first data type
    #         first_enum = bases[-1]  # enum type
    #     else:
    #         for base in bases[0].__mro__:
    #             if issubclass(base, Bnum):
    #                 if first_enum is None:
    #                     first_enum = base
    #             else:
    #                 if obj_type is None:
    #                     obj_type = base
    #
    #     return obj_type, first_enum
    #
    # @staticmethod
    # def _find_new(classdict, obj_type, first_enum):
    #     """Returns the __new__ to be used for creating the enum members.
    #
    #     classdict: the class dictionary given to __new__
    #     obj_type: the data type whose __new__ will be used by default
    #     first_enum: enumeration to check for an overriding __new__
    #
    #     """
    #     # now find the correct __new__, checking to see of one was defined
    #     # by the user; also check earlier enum classes in case a __new__ was
    #     # saved as __new_member__
    #     __new__ = classdict.get('__new__', None)
    #
    #     # should __new__ be saved as __new_member__ later?
    #     save_new = __new__ is not None
    #
    #     if __new__ is None:
    #         # check all possibles for __new_member__ before falling back to
    #         # __new__
    #         for method in ('__new_member__', '__new__'):
    #             for possible in (obj_type, first_enum):
    #                 target = getattr(possible, method, None)
    #                 if target not in {
    #                     None,
    #                     None.__new__,
    #                     object.__new__,
    #                     Bnum.__new__,
    #                     }:
    #                     __new__ = target
    #                     break
    #             if __new__ is not None:
    #                 break
    #         else:
    #             __new__ = object.__new__
    #
    #     # if a non-object.__new__ is used then whatever value/tuple was
    #     # assigned to the enum member name will be passed to __new__ and to the
    #     # new enum member's __init__
    #     if __new__ is object.__new__:
    #         use_args = False
    #     else:
    #         use_args = True
    #
    #     return __new__, save_new, use_args


class Bnum(metaclass=BnumMeta):
    """Valueless, unordered enumeration class"""

    # no actual assignments are made as it is a chicken-and-egg problem
    # with the metaclass, which checks for the Enum class specifically

    # def __new__(cls, value):
    #     # all enum instances are actually created during class construction
    #     # without calling this method; this method is called by the metaclass'
    #     # __call__ (i.e. Color(3) ), and by pickle
    #     if type(value) is cls:
    #         return value
    #         # by-value search for a matching enum member
    #     # see if it's in the reverse mapping (for hashable values)
    #     if value in cls._enum_value_map:
    #         return cls._enum_value_map[value]
    #         # not there, now do long search -- O(n) behavior
    #     for member in cls._enum_map.values():
    #         if member.value == value:
    #             return member
    #     raise ValueError("%s is not a valid %s" % (value, cls.__name__))
    #
    # def __repr__(self):
    #     return "<%s.%s: %r>" % (
    #         self.__class__.__name__, self._name, self._value)
    #
    # def __str__(self):
    #     return "%s.%s" % (self.__class__.__name__, self._name)
    #
    # def __dir__(self):
    #     return (['__class__', '__doc__', 'name', 'value'])
    #
    # def __eq__(self, other):
    #     if type(other) is self.__class__:
    #         return self is other
    #     return NotImplemented
    #
    # def __getnewargs__(self):
    #     return (self._value, )
    #
    # def __hash__(self):
    #     return hash(self._name)

    # _StealthProperty is used to provide access to the `name` and `value`
    # properties of enum members while keeping some measure of protection
    # from modification, while still allowing for an enumeration to have
    # members named `name` and `value`.  This works because enumeration
    # members are not set directely on the enum class -- __getattr__ is
    # used to look them up.

    # @_StealthProperty
    # def name(self):
    #     return self._name
    #
    # @_StealthProperty
    # def value(self):
    #     return self._value
    #
