from collections import defaultdict
from itertools import count
from unittest import TestCase

'''
Check / learn / reverse engineer a bunch of details about Python.
'''


class Display:

    def __str__(self):
        return 'str'

    def __repr__(self):
        return 'repr'


class DisplayTest(TestCase):

    def test_print(self):
        print(Display())  # displays str



class MetaIter(type):

    def __iter__(self):
        return iter([1,2,3])


class Iter(object, metaclass=MetaIter):

    pass


class IterTest(TestCase):

    def test_iter(self):
        assert list(Iter) == [1,2,3]



class Int:

    def __init__(self, x):
        self.x = x

    def __int__(self):
        return self.x


class IntTest(TestCase):

    def test_int(self):
        a = Int(1)
        b = Int(2)
        assert int(a) + int(b) == 3


class AutoEnum(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return defaultdict(count().__next__)
    def __new__(cls, name, bases, classdict):
        print(classdict)
        print(classdict.keys())
        result = type.__new__(cls, name, bases, dict(classdict))
        return result

class Enum(metaclass=AutoEnum): pass

class TestAuto(TestCase):

    def test_auto(self):
        class MyClass(Enum):
            a
            b
        assert MyClass.a == 1

