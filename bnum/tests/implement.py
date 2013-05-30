
from unittest import TestCase
from bnum import ImplicitBnum, ExplicitBnum, from_one


'''
Test various implementation details.
'''


class NoExplicitTest(TestCase):

    def test_no_explicit_in_implicit(self):

        with self.assertRaises(TypeError):
            class Colour(ImplicitBnum):
                red = 1

        with self.assertRaises(TypeError):
            class Number(int, ExplicitBnum, values=from_one):
                with implicit:
                    one = 1

