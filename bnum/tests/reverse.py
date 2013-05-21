
'''
Check / learn / reverse engineer a bunch of details about Python.
'''
from unittest import TestCase


class Display:

    def __str__(self):
        return 'str'

    def __repr__(self):
        return 'repr'


class DisplayTest(TestCase):

    def test_print(self):
        print(Display())  # displays str

