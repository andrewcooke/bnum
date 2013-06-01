
import unittest
from collections import OrderedDict
from pickle import dumps, loads, PicklingError
from bnum import ExplicitBnum

try:
    class Stooges(ExplicitBnum):
        LARRY = 1
        CURLY = 2
        MOE = 3
except Exception as exc:
    Stooges = exc

try:
    class IntStooges(int, ExplicitBnum):
        LARRY = 1
        CURLY = 2
        MOE = 3
except Exception as exc:
    IntStooges = exc

try:
    class FloatStooges(float, ExplicitBnum):
        LARRY = 1.39
        CURLY = 2.72
        MOE = 3.142596
except Exception as exc:
    FloatStooges = exc

# for pickle test and subclass tests
try:
    class StrExplicitBnum(str, ExplicitBnum):
        'accepts only string values'
    class Name(StrExplicitBnum):
        BDFL = 'Guido van Rossum'
        FLUFL = 'Barry Warsaw'
except Exception as exc:
    Name = exc

try:
    Question = ExplicitBnum('Question', 'who what when where why', module=__name__)
except Exception as exc:
    Question = exc

try:
    Answer = ExplicitBnum('Answer', 'him this then there because')
except Exception as exc:
    Answer = exc

class TestBnum(unittest.TestCase):
    def setUp(self):
        class Season(ExplicitBnum):
            SPRING = 1
            SUMMER = 2
            AUTUMN = 3
            WINTER = 4
        self.Season = Season

    def test_bnum_in_bnum_out(self):
        Season = self.Season
        self.assertIs(Season(Season.WINTER), Season.WINTER)

    def test_bnum_value(self):
        Season = self.Season
        self.assertEqual(Season.SPRING.value, 1)

    def test_int_bnum_value(self):
        self.assertEqual(IntStooges.CURLY.value, 2)

    def test_dir_on_class(self):
        Season = self.Season
        self.assertEqual(
            set(dir(Season)),
            set(['__class__', '__doc__', '__members__',
                'SPRING', 'SUMMER', 'AUTUMN', 'WINTER']),
            )

    def test_dir_on_item(self):
        Season = self.Season
        self.assertEqual(
            set(dir(Season.WINTER)),
            set(['__class__', '__doc__', 'name', 'value']),
            )

    def test_bnum(self):
        Season = self.Season
        lst = list(Season)
        self.assertEqual(len(lst), len(Season))
        self.assertEqual(len(Season), 4, Season)
        self.assertEqual(
            [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER], lst)

        for i, season in enumerate('SPRING SUMMER AUTUMN WINTER'.split(), 1):
            e = Season(i)
            self.assertEqual(e, getattr(Season, season))
            self.assertEqual(e.value, i)
            self.assertNotEqual(e, i)
            self.assertEqual(e.name, season)
            self.assertIn(e, Season)
            self.assertIs(type(e), Season)
            self.assertIsInstance(e, Season)
            # self.assertEqual(str(e), 'Season.' + season)
            # self.assertEqual(
            #         repr(e),
            #         '<Season.{0}: {1}>'.format(season, i),
            #         )

    def test_value_name(self):
        Season = self.Season
        self.assertEqual(Season.SPRING.name, 'SPRING')
        self.assertEqual(Season.SPRING.value, 1)
        with self.assertRaises(AttributeError):
            Season.SPRING.name = 'invierno'
        with self.assertRaises(AttributeError):
            Season.SPRING.value = 2

    def test_invalid_names(self):
        with self.assertRaises(ValueError):
            class Wrong(ExplicitBnum):
                mro = 9
        with self.assertRaises(ValueError):
            class Wrong(ExplicitBnum):
                _create= 11
        with self.assertRaises(ValueError):
            class Wrong(ExplicitBnum):
                _get_mixins = 9
        with self.assertRaises(ValueError):
            class Wrong(ExplicitBnum):
                _find_new = 1


    def test_contains(self):
        Season = self.Season
        self.assertIn(Season.AUTUMN, Season)
        self.assertNotIn(3, Season)

        val = Season(3)
        self.assertIn(val, Season)

        class OtherExplicitBnum(ExplicitBnum):
            one = 1; two = 2
        self.assertNotIn(OtherExplicitBnum.two, Season)

    def test_comparisons(self):
        Season = self.Season
        with self.assertRaises(TypeError):
            Season.SPRING < Season.WINTER
        with self.assertRaises(TypeError):
            Season.SPRING > 4

        self.assertNotEqual(Season.SPRING, 1)

        class Part(ExplicitBnum):
            SPRING = 1
            CLIP = 2
            BARREL = 3

        self.assertNotEqual(Season.SPRING, Part.SPRING)
        with self.assertRaises(TypeError):
            Season.SPRING < Part.CLIP

    def test_bnum_duplicates(self):
        class Season(ExplicitBnum, allow_aliases=True):
            SPRING = 1
            SUMMER = 2
            AUTUMN = FALL = 3
            WINTER = 4
            ANOTHER_SPRING = 1
        lst = list(Season)
        self.assertEqual(
            lst,
            [Season.SPRING, Season.SUMMER,
             Season.AUTUMN, Season.WINTER,
            ])
        self.assertIs(Season.FALL, Season.AUTUMN)
        self.assertEqual(Season.FALL.value, 3)
        self.assertEqual(Season.AUTUMN.value, 3)
        self.assertIs(Season(3), Season.AUTUMN)
        self.assertIs(Season(1), Season.SPRING)
        self.assertEqual(Season.FALL.name, 'AUTUMN')
        self.assertEqual(
            {k for k,v in Season.__members__.items() if v.name != k},
            {'FALL', 'ANOTHER_SPRING'},
                )

    def test_bnum_with_value_name(self):
        class Huh(ExplicitBnum):
            name = 1
            value = 2
        self.assertEqual(
            list(Huh),
            [Huh.name, Huh.value],
            )
        self.assertIs(type(Huh.name), Huh)
        self.assertEqual(Huh.name.name, 'name')
        self.assertEqual(Huh.name.value, 1)

    def test_int_bnum(self):
        class WeekDay(int, ExplicitBnum):
            SUNDAY = 1
            MONDAY = 2
            TUESDAY = 3
            WEDNESDAY = 4
            THURSDAY = 5
            FRIDAY = 6
            SATURDAY = 7

        self.assertEqual(['a', 'b', 'c'][WeekDay.MONDAY], 'c')
        self.assertEqual([i for i in range(WeekDay.TUESDAY)], [0, 1, 2])

        lst = list(WeekDay)
        self.assertEqual(len(lst), len(WeekDay))
        self.assertEqual(len(WeekDay), 7)
        target = 'SUNDAY MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY'
        target = target.split()
        for i, weekday in enumerate(target, 1):
            e = WeekDay(i)
            self.assertEqual(e, i)
            self.assertEqual(int(e), i)
            self.assertEqual(e.name, weekday)
            self.assertIn(e, WeekDay)
            self.assertEqual(lst.index(e)+1, i)
            self.assertTrue(0 < e < 8)
            self.assertIs(type(e), WeekDay)
            self.assertIsInstance(e, int)
            self.assertIsInstance(e, ExplicitBnum)

    def test_int_bnum_duplicates(self):
        class WeekDay(int, ExplicitBnum, allow_aliases=True):
            SUNDAY = 1
            MONDAY = 2
            TUESDAY = TEUSDAY = 3
            WEDNESDAY = 4
            THURSDAY = 5
            FRIDAY = 6
            SATURDAY = 7
        self.assertIs(WeekDay.TEUSDAY, WeekDay.TUESDAY)
        self.assertEqual(WeekDay(3).name, 'TUESDAY')
        self.assertEqual([k for k,v in WeekDay.__members__.items()
                if v.name != k], ['TEUSDAY', ])

    def test_pickle_bnum(self):
        if isinstance(Stooges, Exception):
            raise Stooges
        self.assertIs(Stooges.CURLY, loads(dumps(Stooges.CURLY)))
        self.assertIs(Stooges, loads(dumps(Stooges)))

    def test_pickle_int(self):
        if isinstance(IntStooges, Exception):
            raise IntStooges
        self.assertIs(IntStooges.CURLY, loads(dumps(IntStooges.CURLY)))
        self.assertIs(IntStooges, loads(dumps(IntStooges)))

    def test_pickle_float(self):
        if isinstance(FloatStooges, Exception):
            raise FloatStooges
        self.assertIs(FloatStooges.CURLY, loads(dumps(FloatStooges.CURLY)))
        self.assertIs(FloatStooges, loads(dumps(FloatStooges)))

    def test_pickle_bnum_function(self):
        if isinstance(Answer, Exception):
            raise Answer
        self.assertIs(Answer.him, loads(dumps(Answer.him)))
        self.assertIs(Answer, loads(dumps(Answer)))

    def test_pickle_bnum_function_with_module(self):
        if isinstance(Question, Exception):
            raise Question
        self.assertIs(Question.who, loads(dumps(Question.who)))
        self.assertIs(Question, loads(dumps(Question)))

    # def test_exploding_pickle(self):
    #     BadPickle = ExplicitBnum('BadPickle', 'dill sweet bread-n-butter')
    #     BadPickle.__module__ = 'uh uh'
    #     BadPickle.__reduce__ = ExplicitBnum.break_noisily_on_pickle
    #     globals()['BadPickle'] = BadPickle
    #     with self.assertRaises(TypeError):
    #         dumps(BadPickle.dill)
    #     with self.assertRaises(PicklingError):
    #         dumps(BadPickle)

    def test_string_ExplicitBnum(self):
        class SkillLevel(str, ExplicitBnum):
            master = 'what is the sound of one hand clapping?'
            journeyman = 'why did the chicken cross the road?'
            apprentice = 'knock, knock!'
        self.assertEqual(SkillLevel.apprentice, 'knock, knock!')

    def test_getattr_getitem(self):
        class Period(ExplicitBnum):
            morning = 1
            noon = 2
            evening = 3
            night = 4
        self.assertIs(Period(2), Period.noon)
        self.assertIs(getattr(Period, 'night'), Period.night)
        self.assertIs(Period['morning'], Period.morning)

    def test_getattr_dunder(self):
        Season = self.Season
        self.assertTrue(getattr(Season, '__eq__'))

    # def test_iteration_order(self):
    #     class Season(ExplicitBnum):
    #         SUMMER = 2
    #         WINTER = 4
    #         AUTUMN = 3
    #         SPRING = 1
    #     self.assertEqual(
    #             list(Season),
    #             [Season.SUMMER, Season.WINTER, Season.AUTUMN, Season.SPRING],
    #             )

    # def test_programatic_function_string(self):
    #     SummerMonth = ExplicitBnum('SummerMonth', 'june july august')
    #     lst = list(SummerMonth)
    #     self.assertEqual(len(lst), len(SummerMonth))
    #     self.assertEqual(len(SummerMonth), 3, SummerMonth)
    #     self.assertEqual(
    #             [SummerMonth.june, SummerMonth.july, SummerMonth.august],
    #             lst,
    #             )
    #     for i, month in enumerate('june july august'.split(), 1):
    #         e = SummerMonth(i)
    #         self.assertEqual(int(e.value), i)
    #         self.assertNotEqual(e, i)
    #         self.assertEqual(e.name, month)
    #         self.assertIn(e, SummerMonth)
    #         self.assertIs(type(e), SummerMonth)

    # def test_programatic_function_string_list(self):
    #     SummerMonth = ExplicitBnum('SummerMonth', ['june', 'july', 'august'])
    #     lst = list(SummerMonth)
    #     self.assertEqual(len(lst), len(SummerMonth))
    #     self.assertEqual(len(SummerMonth), 3, SummerMonth)
    #     self.assertEqual(
    #             [SummerMonth.june, SummerMonth.july, SummerMonth.august],
    #             lst,
    #             )
    #     for i, month in enumerate('june july august'.split(), 1):
    #         e = SummerMonth(i)
    #         self.assertEqual(int(e.value), i)
    #         self.assertNotEqual(e, i)
    #         self.assertEqual(e.name, month)
    #         self.assertIn(e, SummerMonth)
    #         self.assertIs(type(e), SummerMonth)

    # def test_programatic_function_iterable(self):
    #     SummerMonth = ExplicitBnum(
    #             'SummerMonth',
    #             (('june', 1), ('july', 2), ('august', 3))
    #             )
    #     lst = list(SummerMonth)
    #     self.assertEqual(len(lst), len(SummerMonth))
    #     self.assertEqual(len(SummerMonth), 3, SummerMonth)
    #     self.assertEqual(
    #             [SummerMonth.june, SummerMonth.july, SummerMonth.august],
    #             lst,
    #             )
    #     for i, month in enumerate('june july august'.split(), 1):
    #         e = SummerMonth(i)
    #         self.assertEqual(int(e.value), i)
    #         self.assertNotEqual(e, i)
    #         self.assertEqual(e.name, month)
    #         self.assertIn(e, SummerMonth)
    #         self.assertIs(type(e), SummerMonth)

    # def test_programatic_function_from_dict(self):
    #     SummerMonth = ExplicitBnum(
    #             'SummerMonth',
    #             OrderedDict((('june', 1), ('july', 2), ('august', 3)))
    #             )
    #     lst = list(SummerMonth)
    #     self.assertEqual(len(lst), len(SummerMonth))
    #     self.assertEqual(len(SummerMonth), 3, SummerMonth)
    #     self.assertEqual(
    #             [SummerMonth.june, SummerMonth.july, SummerMonth.august],
    #             lst,
    #             )
    #     for i, month in enumerate('june july august'.split(), 1):
    #         e = SummerMonth(i)
    #         self.assertEqual(int(e.value), i)
    #         self.assertNotEqual(e, i)
    #         self.assertEqual(e.name, month)
    #         self.assertIn(e, SummerMonth)
    #         self.assertIs(type(e), SummerMonth)

    # def test_programatic_function_type(self):
    #     SummerMonth = ExplicitBnum('SummerMonth', 'june july august', type=int)
    #     lst = list(SummerMonth)
    #     self.assertEqual(len(lst), len(SummerMonth))
    #     self.assertEqual(len(SummerMonth), 3, SummerMonth)
    #     self.assertEqual(
    #             [SummerMonth.june, SummerMonth.july, SummerMonth.august],
    #             lst,
    #             )
    #     for i, month in enumerate('june july august'.split(), 1):
    #         e = SummerMonth(i)
    #         self.assertEqual(e, i)
    #         self.assertEqual(e.name, month)
    #         self.assertIn(e, SummerMonth)
    #         self.assertIs(type(e), SummerMonth)

    # def test_programatic_function_type_from_subclass(self):
    #     SummerMonth = IntExplicitBnum('SummerMonth', 'june july august')
    #     lst = list(SummerMonth)
    #     self.assertEqual(len(lst), len(SummerMonth))
    #     self.assertEqual(len(SummerMonth), 3, SummerMonth)
    #     self.assertEqual(
    #             [SummerMonth.june, SummerMonth.july, SummerMonth.august],
    #             lst,
    #             )
    #     for i, month in enumerate('june july august'.split(), 1):
    #         e = SummerMonth(i)
    #         self.assertEqual(e, i)
    #         self.assertEqual(e.name, month)
    #         self.assertIn(e, SummerMonth)
    #         self.assertIs(type(e), SummerMonth)

    def test_subclassing(self):
        if isinstance(Name, Exception):
            raise Name
        self.assertEqual(Name.BDFL, 'Guido van Rossum')
        self.assertTrue(Name.BDFL, Name('Guido van Rossum'))
        self.assertIs(Name.BDFL, getattr(Name, 'BDFL'))
        self.assertIs(Name.BDFL, loads(dumps(Name.BDFL)))

    def test_extending(self):
        class Color(ExplicitBnum):
            red = 1
            green = 2
            blue = 3
        with self.assertRaises(TypeError):
            class MoreColor(Color):
                cyan = 4
                magenta = 5
                yellow = 6

    def test_exclude_methods(self):
        class whatever(ExplicitBnum):
            this = 'that'
            these = 'those'
            def really(self):
                return 'no, not %s' % self.value
        self.assertIsNot(type(whatever.really), whatever)
        self.assertEqual(whatever.this.really(), 'no, not that')

    def test_overwrite_bnums(self):
        class Why(ExplicitBnum):
            question = 1
            answer = 2
            propisition = 3
            def question(self):
                print(42)
        self.assertIsNot(type(Why.question), Why)
        # self.assertNotIn(Why.question, Why._ExplicitBnum_names)
        self.assertNotIn(Why.question, Why)

    def test_wrong_inheritance_order(self):
        with self.assertRaises(TypeError):
            class Wrong(ExplicitBnum, str):
                NotHere = 'error before this point'

    def test_wrong_ExplicitBnum_in_call(self):
        class Monochrome(ExplicitBnum):
            black = 0
            white = 1
        class Gender(ExplicitBnum):
            male = 0
            female = 1
        self.assertRaises(ValueError, Monochrome, Gender.male)

    def test_wrong_ExplicitBnum_in_mixed_call(self):
        class Monochrome(IntExplicitBnum):
            black = 0
            white = 1
        class Gender(ExplicitBnum):
            male = 0
            female = 1
        self.assertRaises(ValueError, Monochrome, Gender.male)

    def test_mixed_bnum_in_call_1(self):
        class Monochrome(int, ExplicitBnum):
            black = 0
            white = 1
        class Gender(int, ExplicitBnum):
            male = 0
            female = 1
        self.assertIs(Monochrome(Gender.female), Monochrome.white)

    def test_mixed_bnum_in_call_2(self):
        class Monochrome(ExplicitBnum):
            black = 0
            white = 1
        class Gender(int, ExplicitBnum):
            male = 0
            female = 1
        self.assertIs(Monochrome(Gender.male), Monochrome.black)

    def test_flufl_ExplicitBnum(self):
        class Fluflnum(ExplicitBnum):
            def __int__(self):
                return int(self.value)
        class MailManOptions(Fluflnum):
            option1 = 1
            option2 = 2
            option3 = 3
        self.assertEqual(int(MailManOptions.option1), 1)

    def test_no_such_bnum_member(self):
        class Color(ExplicitBnum):
            red = 1
            green = 2
            blue = 3
        with self.assertRaises(ValueError):
            Color(4)
        with self.assertRaises(KeyError):
            Color['chartreuse']

    def test_new_repr(self):
        class Color(ExplicitBnum):
            red = 1
            green = 2
            blue = 3
            def __repr__(self):
                return "don't you just love shades of %s?" % self.name
        self.assertEqual(
                repr(Color.blue),
                "don't you just love shades of blue?",
                )

    def test_inherited_repr(self):
        class MyExplicitBnum(ExplicitBnum):
            def __repr__(self):
                return "My name is %s." % self.name
        class MyIntExplicitBnum(int, MyExplicitBnum):
            this = 1
            that = 2
            theother = 3
        self.assertEqual(repr(MyIntExplicitBnum.that), "My name is that.")

    # def test_multiple_mixin_mro(self):
    #     class auto_ExplicitBnum(type(ExplicitBnum)):
    #         def __new__(metacls, cls, bases, classdict):
    #             temp = type(classdict)()
    #             names = set(classdict._ExplicitBnum_names)
    #             i = 0
    #             for k in classdict._ExplicitBnum_names:
    #                 v = classdict[k]
    #                 if v is Ellipsis:
    #                     v = i
    #                 else:
    #                     i = v
    #                 i += 1
    #                 temp[k] = v
    #             for k, v in classdict.items():
    #                 if k not in names:
    #                     temp[k] = v
    #             return super(auto_ExplicitBnum, metacls).__new__(
    #                     metacls, cls, bases, temp)
    #
    #     class AutoNumberedExplicitBnum(ExplicitBnum, metaclass=auto_ExplicitBnum):
    #         pass
    #
    #     class AutoIntExplicitBnum(int, ExplicitBnum, metaclass=auto_ExplicitBnum):
    #         pass
    #
    #     class TestAutoNumber(AutoNumberedExplicitBnum):
    #         a = ...
    #         b = 3
    #         c = ...
    #
    #     class TestAutoInt(AutoIntExplicitBnum):
    #         a = ...
    #         b = 3
    #         c = ...

    def test_subclasses_with_getnewargs(self):
        class NamedInt(int):
            def __new__(cls, *args):
                _args = args
                name, *args = args
                if len(args) == 0:
                    raise TypeError("name and value must be specified")
                self = int.__new__(cls, *args)
                self._intname = name
                self._args = _args
                return self
            def __getnewargs__(self):
                return self._args
            @property
            def __name__(self):
                return self._intname
            def __repr__(self):
                # repr() is updated to include the name and type info
                return "{}({!r}, {})".format(type(self).__name__,
                                             self.__name__,
                                             int.__repr__(self))
            def __str__(self):
                # str() is unchanged, even if it relies on the repr() fallback
                base = int
                base_str = base.__str__
                if base_str.__objclass__ is object:
                    return base.__repr__(self)
                return base_str(self)
            # for simplicity, we only define one operator that
            # propagates expressions
            def __add__(self, other):
                temp = int(self) + int( other)
                if isinstance(self, NamedInt) and isinstance(other, NamedInt):
                    return NamedInt(
                        '({0} + {1})'.format(self.__name__, other.__name__),
                        temp )
                else:
                    return temp

        class NEI(NamedInt, ExplicitBnum):
            x = ('the-x', 1)
            y = ('the-y', 2)

        self.assertIs(NEI.__new__, ExplicitBnum.__new__)
        self.assertEqual(repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)', 3)")
        globals()['NamedInt'] = NamedInt
        globals()['NEI'] = NEI
        NI5 = NamedInt('test', 5)
        self.assertEqual(NI5, 5)
        self.assertEqual(loads(dumps(NI5)), 5)
        self.assertEqual(NEI.y.value, 2)
        self.assertIs(loads(dumps(NEI.y)), NEI.y)

    def test_subclasses_without_getnewargs(self):
        class NamedInt(int):
            def __new__(cls, *args):
                _args = args
                name, *args = args
                if len(args) == 0:
                    raise TypeError("name and value must be specified")
                self = int.__new__(cls, *args)
                self._intname = name
                self._args = _args
                return self
            @property
            def __name__(self):
                return self._intname
            def __repr__(self):
                # repr() is updated to include the name and type info
                return "{}({!r}, {})".format(type(self).__name__,
                                             self.__name__,
                                             int.__repr__(self))
            def __str__(self):
                # str() is unchanged, even if it relies on the repr() fallback
                base = int
                base_str = base.__str__
                if base_str.__objclass__ is object:
                    return base.__repr__(self)
                return base_str(self)
            # for simplicity, we only define one operator that
            # propagates expressions
            def __add__(self, other):
                temp = int(self) + int( other)
                if isinstance(self, NamedInt) and isinstance(other, NamedInt):
                    return NamedInt(
                        '({0} + {1})'.format(self.__name__, other.__name__),
                        temp )
                else:
                    return temp

        class NEI(NamedInt, ExplicitBnum):
            x = ('the-x', 1)
            y = ('the-y', 2)

        self.assertIs(NEI.__new__, ExplicitBnum.__new__)
        self.assertEqual(repr(NEI.x + NEI.y), "NamedInt('(the-x + the-y)', 3)")
        globals()['NamedInt'] = NamedInt
        globals()['NEI'] = NEI
        NI5 = NamedInt('test', 5)
        self.assertEqual(NI5, 5)
        self.assertEqual(NEI.y.value, 2)
        with self.assertRaises(TypeError):
            dumps(NEI.x)
        with self.assertRaises(PicklingError):
            dumps(NEI)

    def test_tuple_subclass(self):
        class SomeTuple(tuple, ExplicitBnum):
            first = (1, 'for the money')
            second = (2, 'for the show')
            third = (3, 'for the music')
        self.assertIs(type(SomeTuple.first), SomeTuple)
        self.assertIsInstance(SomeTuple.second, tuple)
        self.assertEqual(SomeTuple.third, (3, 'for the music'))
        globals()['SomeTuple'] = SomeTuple
        self.assertIs(loads(dumps(SomeTuple.first)), SomeTuple.first)

    def test_duplicate_values_give_unique_bnum_items(self):
        class AutoNumber(ExplicitBnum):
            first = ()
            second = ()
            third = ()
            def __new__(cls):
                value = len(cls.__members__) + 1
                obj = object.__new__(cls)
                obj._value = value
                return obj
            def __int__(self):
                return int(self._value)
        self.assertEqual(
                list(AutoNumber),
                [AutoNumber.first, AutoNumber.second, AutoNumber.third],
                )
        self.assertEqual(int(AutoNumber.second), 2)
        self.assertIs(AutoNumber(1), AutoNumber.first)

    def test_inherited_new_from_enhanced_bnum(self):
        class AutoNumber(ExplicitBnum):
            def __new__(cls):
                value = len(cls.__members__) + 1
                obj = object.__new__(cls)
                obj._value = value
                return obj
            def __int__(self):
                return int(self._value)
        class Color(AutoNumber):
            red = ()
            green = ()
            blue = ()
        self.assertEqual(list(Color), [Color.red, Color.green, Color.blue])
        self.assertEqual(list(map(int, Color)), [1, 2, 3])

    def test_inherited_new_from_mixed_ExplicitBnum(self):
        class AutoNumber(int, ExplicitBnum):
            def __new__(cls):
                value = len(cls.__members__) + 1
                obj = int.__new__(cls, value)
                obj._value = value
                return obj
        class Color(AutoNumber):
            red = ()
            green = ()
            blue = ()
        self.assertEqual(list(Color), [Color.red, Color.green, Color.blue])
        self.assertEqual(list(map(int, Color)), [1, 2, 3])

    def test_ordered_mixin(self):
        class OrderedExplicitBnum(ExplicitBnum):
            def __ge__(self, other):
                if self.__class__ is other.__class__:
                    return self._value >= other._value
                return NotImplemented
            def __gt__(self, other):
                if self.__class__ is other.__class__:
                    return self._value > other._value
                return NotImplemented
            def __le__(self, other):
                if self.__class__ is other.__class__:
                    return self._value <= other._value
                return NotImplemented
            def __lt__(self, other):
                if self.__class__ is other.__class__:
                    return self._value < other._value
                return NotImplemented
        class Grade(OrderedExplicitBnum):
            A = 5
            B = 4
            C = 3
            D = 2
            F = 1
        self.assertGreater(Grade.A, Grade.B)
        self.assertLessEqual(Grade.F, Grade.C)
        self.assertLess(Grade.D, Grade.A)
        self.assertGreaterEqual(Grade.B, Grade.B)


if __name__ == '__main__':
    unittest.main()
