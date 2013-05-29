
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

        assert str(list(map(str, Colour))) == "['blue', 'green', 'red']", str(list(map(str, Colour)))

    def test_number(self):

        class Number(int, ExplicitBnum, values=from_one):
            with implicit:
                one
                two
            three = one + two

        assert isinstance(Number.two, int), type(Number.two)


class BasicTest(TestCase):

    def test_colour(self):

        class Colour(ImplicitBnum):
            red
            green
            blue

        assert Colour.red != Colour.blue
        assert Colour.red == Colour.red
        assert isinstance(Colour.red, Colour), type(Colour.red)
        assert Colour.red.name == 'red', Colour.red.name
        assert repr(Colour.red) == "Colour('red')", repr(Colour.red)
        assert str(Colour.red) == 'red'
        assert str(list(Colour)) == "[Colour('blue'), Colour('green'), Colour('red')]", str(list(Colour))
        assert len(Colour) == 3, len(Colour)
        assert Colour.red in Colour


class ValueTest(TestCase):

    def test_colour(self):

        class Colour(ImplicitBnum):
            red
            green
            blue

        assert Colour.red.value == 'red', Colour.red.value
        assert str(Colour.red) == 'red', str(Colour.red)
        assert type(Colour.red.value) == str, type(Colour.red.value)
        assert Colour('red') is Colour.red

    # GOT TO HERE!

    def test_number(self):

        class Number(int, ExplicitBnum, values=from_one):
            with implicit:
                one
                two
            three = one + two

        assert isinstance(Number.two, int), type(Number.two)
        assert Number.three == 3, Number.three
        assert repr(Number.three) == "Number(value=3, name='three')", repr(Number.three)





class OtherTest(TestCase):

    def test_no_explicit_in_implicit(self):

        with self.assertRaises(TypeError):
            class Colour(ImplicitBnum):
                red = 1

        with self.assertRaises(TypeError):
            class Number(int, ExplicitBnum, values=from_one):
                with implicit:
                    one = 1



