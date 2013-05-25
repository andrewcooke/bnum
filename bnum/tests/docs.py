
from unittest import TestCase
from bnum import Bnum


'''
Test all the assertions made in the documentation.
'''


class NameOnlyTest(TestCase):

    def test_colour(self):

        class Colour(Bnum):
            red
            green
            blue

        assert Colour.red != Colour.blue
        assert Colour.red == Colour.red
        assert isinstance(Colour.red, Colour), type(Colour.red)
        assert Colour.red.name == 'red', Colour.red.name
        assert str(Colour.red) == 'red'
        assert repr(Colour.red) == "Colour('red')", repr(Colour.red)
