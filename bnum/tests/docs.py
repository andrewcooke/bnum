
from unittest import TestCase
from bnum import ImplicitBnum, ExplicitBnum, from_one


'''
Test all the assertions made in the documentation.
'''


class QuickStartTest(TestCase):

    def test_colour(self):

        class Colour(ImplicitBnum):
            red
            green
            blue

        assert Colour.red != Colour.blue
        assert Colour.red == Colour.red
        assert isinstance(Colour.red, Colour), type(Colour.red)
        assert Colour.red.name == 'red', Colour.red.name
        assert str(Colour.red) == 'red'
        assert repr(Colour.red) == "Colour('red')", repr(Colour.red)
        assert str(list(map(str, Colour))) == "['blue', 'green', 'red']", str(list(map(str, Colour)))
        assert Colour.red in Colour

    def test_number(self):

        class Number(int, ExplicitBnum, values=from_one):
            with implicit:
                one
                two
            three = one + two

        assert isinstance(Number.two, int), type(Number.two)
        assert Number.three == 3, Number.three
        assert repr(Number.three) == "Number(value=3, name='three')", repr(Number.three)

    def test_no_explicit_in_implicit(self):

        with self.assertRaises(TypeError):
            class Colour(ImplicitBnum):
                red = 1

        with self.assertRaises(TypeError):
            class Number(int, ExplicitBnum, values=from_one):
                with implicit:
                    one = 1



