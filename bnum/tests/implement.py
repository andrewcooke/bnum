
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

class ImplicitTest(TestCase):

    def test_implicit(self):

        class Foo(ImplicitBnum):
            implicit
            explicit

        assert Foo.implicit in Foo
        assert repr(Foo.implicit) == "Foo('implicit')", repr(Foo.implicit)

    def test_explicit(self):

        with self.assertRaises(AttributeError):
            # this one has the initial implicit shadowing the context
            class Bar(ExplicitBnum):
                implicit = 1
                with implicit:
                    explicit

        class Baz(ExplicitBnum):
            explicit = 1
            with implicit:
                implicit

        assert Baz.implicit in Baz
        assert Baz.explicit in Baz
        assert repr(Baz.implicit) == "Baz('implicit')", repr(Baz.implicit)

        class Baf(ExplicitBnum):
            with implicit:
                explicit
            implicit = 1

        assert Baf.implicit in Baf
        assert Baf.explicit in Baf
        assert repr(Baf.implicit) == "Baf(value=1, name='implicit')", repr(Baf.implicit)

