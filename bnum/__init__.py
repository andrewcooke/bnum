
from collections import OrderedDict
from itertools import count
from types import MappingProxyType
from enum import dunder, break_noisily_on_pickle, _StealthProperty

'''
Based on Enum, (c) 2013 Ethan Furman, ethan@stoneleaf.us
Modifications (c) 2013 Andrew Cooke, andrew@acooke.org
'''


__all__ = ['ImplicitBnum', 'ExplicitBnum']


# this is needed because BnumMeta runs multiple times - to create Bnum etc
# and then to create enum subclasses.  on the first runs, Bnum etc don't exist.
Bnum ,ImplicitBnum, ExplicitBnum = None, None, None


ILLEGAL_NAMES = {'mro', '_create', '_get_mixins', '_find_new'}


def names():
    def value(name):
        return name
    return value

def from_counter(start, step=1):
    def outer():
        counter = count(start, step)
        def value(name):
            nonlocal counter
            return next(counter)
        return value
    return outer

from_one = from_counter(1)
from_zero = from_counter(0)

def bits():
    count = 0
    def value(name):
        nonlocal count
        count += 1
        return 2 ** (count - 1)
    return value


class BnumDict(OrderedDict):
    '''
    The dictionary supplied by BnumMeta to store the class contents.  We
    provide a default value when implicit is true, and allow implicit to
    be enabled via "with implicit".

    An ordered dict is needed to preserve the order of side-effects (things
    like which alias is preferred).
    '''

    def __init__(self, implicit=False, values=names):
        super().__init__()
        self.implicit = implicit
        self.values = values

    def __enter__(self):
        self.implicit = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.implicit = False

    def __getitem__(self, item):
        '''Provide a default value of None.'''
        if self.implicit:
            if item not in self and not dunder(item):
                super().__setitem__(item, self.values(item))
        else:
            if item not in self and item == 'implicit':
                return self
        return super().__getitem__(item)

    def __setitem__(self, name, value):
        if self.implicit and not dunder(name):
            raise TypeError('Cannot use explicit value for %s' % name)
        return super().__setitem__(name, value)


class BnumMeta(type):
    '''
    The class responsible for constructing Bnum instances (both the class,
    directly, and subclasses).  This is done in two steps.  First, __prepare__
    provides a dictionary.  Second (after the class has been evaluated),
    __new__ constructs the class.
    '''

    def __init__(metacls, cls, bases=None, dict=None,
                 values=None, allow_aliases=False):
        super().__init__(cls, bases, dict)

    def __new__(metacls, cls, bases, classdict,
                values=None, allow_aliases=False):
        '''

        '''

        # i'm just going to trust Enum has this inheritance stuff right...
        obj_type, first_enum = metacls._get_mixins(bases)
        __new__, save_new, use_args = \
            metacls._find_new(classdict, obj_type, first_enum)

        # separate enumerations from other class members
        enum_dict, others = metacls._split_class_contents(classdict)
        enums_by_value = {}
        enums_by_name = {}

        # check for illegal enum names
        if set(enum_dict.keys()) & ILLEGAL_NAMES:
            raise ValueError('Enumeration names cannot include '
                             + ','.join(ILLEGAL_NAMES))

        # create the (empty) Bnum type
        enum_class = super().__new__(metacls, cls, bases, others)
        # define early so that __members__ can be used in construction
        enum_class._enums_by_name = enums_by_name

        # again, trust Enum on this...
        if obj_type is not object and obj_type.__dict__.get('__getnewargs__') is None:
            enum_class.__reduce__ = break_noisily_on_pickle
            enum_class.__module__ = 'uh uh'  # wtf does this mean?

        # instantiate and then check for values (as Enum - someone could use
        # the constructor to do auto-numbering...)
        for name, value in enum_dict.items():
            # again, trust Enum...
            if not isinstance(value, tuple):
                args = (value, )
            else:
                args = value
            if obj_type is tuple:   # special case for tuple enums
                args = (args, )     # wrap it one more time
            if not use_args:
                enum_item = __new__(enum_class)
                enum_item._value = value
            else:
                enum_item = __new__(enum_class, *args)
                if not hasattr(enum_item, '_value'):
                    enum_item._value = obj_type(*args)
            enum_item._obj_type = obj_type
            enum_item._name = name
            enum_item.__init__(*args)

            print(repr(enum_item))
            if enum_item.value in enums_by_value:
                if allow_aliases:
                    enums_by_name[name] = enums_by_value[enum_item.value]
                else:
                    raise ValueError('Duplicate value for %s, %s' %
                                     (name, enums_by_value[enum_item.value].name))
            else:
                enums_by_name[name] = enum_item
                enums_by_value[enum_item.value] = enum_item

        # more pickle-related logic from Enum
        for name in ('__repr__', '__str__', '__getnewargs__'):
            class_method = getattr(enum_class, name)
            obj_method = getattr(obj_type, name, None)
            enum_method = getattr(first_enum, name, None)
            if obj_method is not None and obj_method is class_method:
                setattr(enum_class, name, enum_method)
        if Bnum is not None:
            if save_new:
                enum_class.__new_member__ = __new__
            enum_class.__new__ = Bnum.__new__

        try:
            enum_class._enums_by_value = \
                OrderedDict((value, enums_by_value[value])
                            for value in sorted(enums_by_value.keys()))
        except:
            enum_class._enums_by_value = enums_by_value

        return enum_class

    @staticmethod
    def _split_class_contents(classdict):
        enums, others = OrderedDict(), dict()
        for (name, value) in classdict.items():
            if dunder(name) or hasattr(value, '__get__'):
                others[name] = value
            else:
                enums[name] = value
        return enums, others

    def __call__(cls, value=None, name=None):
        if type(value) is cls:
            if name is None or name == value.name:
                return value
        elif value is None:
            if name is None:
                raise ValueError('Give name or value')
            elif name in cls._enums_by_name:
                return cls._enums_by_name[name]
            else:
                print(cls._enums_by_name)
                raise ValueError('No name %r' % name)
        elif name is None:
            if value in cls._enums_by_value:
                return cls._enums_by_value[value]
            else:
                raise ValueError('No value %r' % value)
        elif name in cls._enums_by_name:
            enum = cls._enums_by_name[name]
            if value in cls._enums_by_value and \
                        enum is cls._enums_by_value[value]:
                return enum
        raise ValueError('Inconsistent name (%r) and value (%r)' %
                        (name, value))

    # def __contains__(cls, enum_item):
    #     return isinstance(enum_item, cls) and enum_item.name in cls._enum_map

    def __dir__(self):
        return ['__class__', '__doc__', '__members__'] + list(self._enums_by_name.keys())

    @property
    def __members__(cls):
        return MappingProxyType(cls._enums_by_name)

    def __getattr__(cls, name):
        """Return the enum member matching `name`

        We use __getattr__ instead of descriptors or inserting into the enum
        class' __dict__ in order to support `name` and `value` being both
        properties for enum members (which live in the class' __dict__) and
        enum members themselves.

        """

        if dunder(name):
            raise AttributeError(name)
        try:
            return cls._enums_by_name[name]
        except KeyError:
            raise AttributeError(name) from None

    def __getitem__(cls, name):
        return cls._enums_by_name[name]

    def __iter__(cls):
        return (cls._enums_by_value[value] for value in cls._enums_by_value)

    def __len__(cls):
        return len(cls._enums_by_name)

    # def __repr__(cls):
    #     return "<enum %r>" % cls.__name__

    @staticmethod
    def _get_mixins(bases):
        """Returns the type for creating enum members, and the first inherited
        enum class.

        bases: the tuple of bases that was given to __new__

        """
        if not bases:
            return object, Bnum

        # double check that we are not subclassing a class with existing
        # enumeration members; while we're at it, see if any other data
        # type has been mixed in so we can use the correct __new__
        obj_type = first_enum = None
        for base in bases:
            if  base not in (Bnum, ImplicitBnum, ExplicitBnum) \
                    and issubclass(base, Bnum) \
                    and base._enums_by_name:
                raise TypeError("Cannot extend enumerations")
            # base is now the last base in bases
        if not issubclass(base, Bnum):
            raise TypeError("new enumerations must be created as "
                            "`ClassName([mixin_type,] enum_type)`")

        # get correct mix-in type (either mix-in type of Bnum subclass, or
        # first base if last base is Bnum)
        if not issubclass(bases[0], Bnum):
            obj_type = bases[0]     # first data type
            first_enum = bases[-1]  # enum type
        else:
            for base in bases[0].__mro__:
                if issubclass(base, Bnum):
                    if first_enum is None:
                        first_enum = base
                else:
                    if obj_type is None:
                        obj_type = base

        return obj_type, first_enum

    @staticmethod
    def _find_new(classdict, obj_type, first_enum):
        """Returns the __new__ to be used for creating the enum members.

        classdict: the class dictionary given to __new__
        obj_type: the data type whose __new__ will be used by default
        first_enum: enumeration to check for an overriding __new__

        """
        # now find the correct __new__, checking to see of one was defined
        # by the user; also check earlier enum classes in case a __new__ was
        # saved as __new_member__
        __new__ = classdict.get('__new__', None)

        # should __new__ be saved as __new_member__ later?
        save_new = __new__ is not None

        if __new__ is None:
            # check all possibles for __new_member__ before falling back to
            # __new__
            for method in ('__new_member__', '__new__'):
                for possible in (obj_type, first_enum):
                    target = getattr(possible, method, None)
                    if target not in {
                        None,
                        None.__new__,
                        object.__new__,
                        Bnum.__new__,
                        }:
                        __new__ = target
                        break
                if __new__ is not None:
                    break
            else:
                __new__ = object.__new__

        # if a non-object.__new__ is used then whatever value/tuple was
        # assigned to the enum member name will be passed to __new__ and to the
        # new enum member's __init__
        if __new__ is object.__new__:
            use_args = False
        else:
            use_args = True

        return __new__, save_new, use_args


class ImplicitBnumMeta(BnumMeta):

    @classmethod
    def __prepare__(metacls, cls, bases,
                values=None, allow_aliases=False):
        return BnumDict(implicit=True, values=values() if values else names())


class ExplicitBnumMeta(BnumMeta):

    @classmethod
    def __prepare__(metacls, cls, bases,
                values=None, allow_aliases=False):
        return BnumDict(implicit=False, values=values() if values else names())




class Bnum():
    """Valueless, unordered enumeration class"""

    # no actual assignments are made as it is a chicken-and-egg problem
    # with the metaclass, which checks for the Enum class specifically

    def __new__(cls, value):
        return value

        # # all enum instances are actually created during class construction
        # # without calling this method; this method is called by the metaclass'
        # # __call__ (i.e. Color(3) ), and by pickle
        # if type(value) is cls:
        #     return value
        #     # by-value search for a matching enum member
        # # see if it's in the reverse mapping (for hashable values)
        # if value in cls._enum_value_map:
        #     return cls._enum_value_map[value]
        #     # not there, now do long search -- O(n) behavior
        # for member in cls._enum_map.values():
        #     if member.value == value:
        #         return member
        # raise ValueError("%s is not a valid %s" % (value, cls.__name__))

    def __repr__(self):
        if self._name == self._value:
            return '%s(%r)' % (self.__class__.__name__, self._value)
        else:
            return "%s(value=%r, name=%r)" % \
                   (self.__class__.__name__, self._value, self._name)

    def __str__(self):
        return str(self._value)

    def __dir__(self):
        return (['__class__', '__doc__', 'name', 'value'])

    def __eq__(self, other):
        if type(other) is self.__class__:
            return self is other
        return NotImplemented

    def __getnewargs__(self):
        return (self._value, )

    def __hash__(self):
        return hash(self._name)

    @_StealthProperty
    def name(self):
        return self._name

    @_StealthProperty
    def value(self):
        return self._value


class ImplicitBnum(Bnum, metaclass=ImplicitBnumMeta):

    pass


class ExplicitBnum(Bnum, metaclass=ExplicitBnumMeta):

    pass


