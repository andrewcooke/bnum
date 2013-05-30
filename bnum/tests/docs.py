
from unittest import TestCase
from bnum import ImplicitBnum, ExplicitBnum, from_one, bits


'''
Test all the assertions made in the documentation.
'''


class Colour(ImplicitBnum):
    red
    green
    blue


class Number(int, ExplicitBnum, values=from_one):
    with implicit:
        one
        two
    three = one + two


class FavouriteNumbers(ExplicitBnum):
    forty_two = 42
    seven = 7


class Weekday(ImplicitBnum, values=from_one):
    monday, tuesday, wednesday, thursday, friday
    saturday, sunday


class Emphasis(ImplicitBnum, values=bits):
    underline
    italic
    bold


class Strange(ExplicitBnum):
    foo = 42
    bar = 'fish'
    with implicit:
        baz


class QuickStartTest(TestCase):

    def test_colour(self):
        assert str(list(map(str, Colour))) == "['blue', 'green', 'red']", str(list(map(str, Colour)))

    def test_number(self):
        assert isinstance(Number.two, int), type(Number.two)


class BasicTest(TestCase):

    def test_colour(self):
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
        assert Colour.red.value == 'red', Colour.red.value
        assert str(Colour.red) == 'red', str(Colour.red)
        assert type(Colour.red.value) == str, type(Colour.red.value)
        assert Colour('red') is Colour.red

    def test_favourite_numbers(self):
        assert FavouriteNumbers.seven.value == 7, FavouriteNumbers.seven.value
        assert str(FavouriteNumbers.seven) == '7', str(FavouriteNumbers.seven)

    def test_weekday(self):
        assert Weekday.sunday.name == 'sunday', Weekday.sunday.name
        assert Weekday.sunday.value == 7, Weekday.sunday.value
        assert repr(Weekday.sunday) == "Weekday(value=7, name='sunday')", repr(Weekday.sunday)

    def test_emphasis(self):
        assert Emphasis.underline.value == 1, Emphasis.underline.value
        assert Emphasis.bold.value == 4, Emphasis.bold.value
        assert Emphasis.bold.name == 'bold'
        with self.assertRaises(TypeError):
            2 & (Emphasis.italic | Emphasis.bold)

    def test_strange(self):
        assert Strange.baz.value == 'baz', Strange.baz.value


class RetrievalTest(TestCase):

    def test_colour(self):
        assert Colour('red') is Colour.red

    def test_emphasis(self):
        assert Emphasis(2) is Emphasis.italic
        assert Emphasis(name='italic') is Emphasis(value=2, name='italic') is Emphasis.italic
        with self.assertRaises(ValueError):
            Emphasis(value=3, name='italic')


class OrderingTest(TestCase):

    def test_colour(self):
        assert str(list(Colour)) == "[Colour('blue'), Colour('green'), Colour('red')]", str(list(Colour))

    def test_emphasis(self):
        assert repr(Emphasis.underline) == "Emphasis(value=1, name='underline')", repr(Emphasis.underline)
        assert repr(Emphasis.italic) == "Emphasis(value=2, name='italic')", repr(Emphasis.italic)
        assert repr(Emphasis.bold) == "Emphasis(value=4, name='bold')", repr(Emphasis.bold)


class AliasesTest(TestCase):

    def test_error(self):
        with self.assertRaises(ValueError):
            class Error(ExplicitBnum, values=from_one):
                with implicit:
                    a
                b = 1

    def test_ok(self):

        class OK(ExplicitBnum, values=from_one, allow_aliases=True):
            with implicit:
                a
            b = 1  # an alias

        assert repr(OK(name='a')) == "OK(value=1, name='a')", repr(OK(name='a'))
        assert repr(OK(name='b')) == "OK(value=1, name='a')", repr(OK(name='b'))
        assert repr(OK(value=1)) == "OK(value=1, name='a')", repr(OK(value=1))
        assert str(list(OK)) == "[OK(value=1, name='a')]", str(list(OK))


class OtherTest(TestCase):

    def test_no_explicit_in_implicit(self):

        with self.assertRaises(TypeError):
            class Colour(ImplicitBnum):
                red = 1

        with self.assertRaises(TypeError):
            class Number(int, ExplicitBnum, values=from_one):
                with implicit:
                    one = 1

    def test_constructor(self):

        class Animal(ExplicitBnum):

            def __init__(self, legs ,noise):
                self.legs = legs
                self.noise = noise

            def talk(self):
                return self.noise

            def __str__(self):
                return 'A %s has %d legs and says %r' % \
                       (self.name, self.legs, self.talk())

            pig = 4, 'oink'
            hen = 2, 'cluck'
            cow = 4, 'moo'

        assert Animal.pig in Animal
        assert str(Animal.pig) == "A pig has 4 legs and says 'oink'", str(Animal.pig)
        assert Animal((4, 'oink')) == Animal.pig
        assert Animal.pig.value == (4, 'oink'), Animal.pig.value
