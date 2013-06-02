
This project has been abandoned in favour of
[simple-enum](https://github.com/andrewcooke/simple-enum).

A (Slightly) Better Enum For Python 3
=====================================

Bnum is a better enumeration class for Python 3.  It is broadly
[compatible](#list-of-differences) with the
[standard Enum](http://www.python.org/dev/peps/pep-0435/) (and uses much of
the same code), but has been tweaked to address
[issues](#things-you-can-do-with-bnum-that-you-cant-do-with-enum)
identified in a
[rant](http://www.acooke.org/cute/Pythonssad0.html) I wrote some time ago
(see [TYCDWB(TYCDWE)](#things-you-can-do-with-bnum-that-you-cant-do-with-enum)).

* [Quick Start](#quick-start)
* [Basic Use](#basic-use)
   * [Names](#names)
   * [Values](#values)
   * [Retrieving Instances](#retrieving-instances)
   * [Ordering](#ordering)
   * [Aliases](#aliases)
* [Advanced Use](#advanced-use)
   * [Constructors And Methods](#constructors-and-methods)
   * [Multiple Inheritance](#multiple-inheritance)
   * [Providing Implicit Values](#providing-implicit-values)
* [Comparison With Enum](#comparison-with-enum)
   * [Background](#background)
   * [List Of Differences](#list-of-differences)
   * [Philosophy](#philosophy)
   * [Things You Can Do With Bnum (That You Can't Do With Enum)](#things-you-can-do-with-bnum-that-you-cant-do-with-enum)
* [FAQ](#faq)
   * [Why Implicit And Explicit?](#why-implicit-and-explicit)
   * [Didn't You Say This Was A Syntax Error?](#didnt-you-say-this-was-a-syntax-error)
   * [Isn't Explicit Better Than Implicit?](#isnt-explicit-better-than-implicit)
   * [Why Not Influence The Official Design?](#why-not-influence-the-official-design)
   * [So This Is What You Think Enum Should Be?](#so-this-is-what-you-think-enum-should-be)
* [Credits](#credits)

Quick Start
-----------

If you just need a set of names:

```python
>>> from bnum import ImplicitBnum
>>> class Colour(ImplicitBnum):
...     red
...     green
...     blue
...
>>> for colour in Colour: print(colour)
blue
green
red
```

(they are printed in alphabetical [order](#ordering), btw).

At the other, hopefully less-used, extreme, if you want integers from 1,
explicit values, and the ability to use enumeration values in expressions,
then you can do that too:

```python
>>> from bnum import ExplicitBnum, from_one
>>> class Number(int, ExplicitBnum, values=from_one):
...     with implicit:
...         one
...         two
...     three = one + two
...     four = 4
...
>>> isinstance(Number.two, int)
True
```

Basic Use
---------

### Names

At its simplest, a Bnum defines a collection of distinct names:

```python
>>> class Colour(ImplicitBnum):
...     red
...     green
...     blue
```

These can be tested for equality, are instances of the class on which they
are declared, and can be displayed in the usual ways:

```python
>>> Colour.red == Color.blue
False
>>> Colour.red == Colour.red
True
>>> isinstance(Colour.red, Colour):
True
>>> Colour.red.name
red
>>> repr(Colour.red)
Colour('red')
>>> Colour.red  # this is the value - see below
red
```

And the class itself behaves as a collection of the instances it contains:

```python
>>> list(Colour)
[Colour('blue'), Colour('green'), Colour('red')]
>>> len(Colour)
3
>>> Colour.red in Colour
True
```

### Values

Instances have values as well as [names](#names).

The default, implicit value of an instance is its name:

```python
>>> Colour.red.value
red
>>> Colour.red  # this is str() of the value, which is the value, which is the name
red
>>> type(Colour.red.value)
<class str>
```

If you have a value then the appropriate instance can be retrieved by calling
the class:

```python
>>> Colour('red') is Colour.red
True
```

Often, names are all you need (think of symbols in Lisp), but some languages
associate alternative values with enumerations (think of enums in Java).

You can specify the value explicitly:

```python
>>> class FavouriteNumbers(ExplicitBnum):
...     forty_two = 42
...     seven = 7
...
>>> FavouriteNumbers.seven.value
7
>>> FavouriteNumbers.seven  # this is str() of the value
7
```

But usually you want integers, counting from 0 or 1, or bit fields, and
Bnum will provide these if you use a suitable `values` argument in the
class.

For example, `values=from_one` provides integers counting from 1 (there's
also a `from_zero` that, yes, you guessed right):

```python
>>> class Weekday(ImplicitBnum, values=from_one):
...     monday, tuesday, wednesday, thursday, friday
...     saturday, sunday
...
>>> Weekday.sunday.name
sunday
>>> Weekday.sunday.value
7
>>> repr(Weekday.sunday):
Weekday(value=7, name='sunday')
```

The final line above shows that when an instance's name and value differ, both
are shown in the output from `repr()`.  That same syntax can also be used to
retrieve values - see the next section.

Using `values=bits` provides bit fields:

```python
>>> class Emphasis(ImplicitBnum, values=bits):
...     underline
...     italic
...     bold
...
>>> Emphasis.underline.value
1
>>> Emphasis.bold.value
4
>>> Emphasis.bold.name
bold
>>> 2 & (Emphasis.italic | Emphasis.bold)  # this can be made to work - see later
TypeError: blah, blah
```

To make the final line work as you might expect, see the
[section on multiple inheritance](#multiple-inheritance) below.

You can even mix value types, although it may make the [ordering](#Ordering)
undefined:

```python
>>> class Strange(ExplicitBnum):
...     foo = 42
...     bar = 'fish'
...     with implicit:
...         baz  # value will be 'baz' as no alternative values given
```

### Retrieving Instances

If you have the [value](#values), or [name](#names) (or both, as long as
they are consistent), then you can get the appropriate instance by calling the
class:

```python
>>> Colour('red') is Colour.red  # default is to use the value
True
>>> Emphasis(2) is Emphasis.italic
True
>>> Emphasis(name='italic') is Emphasis(value=2, name='italic') is Emphasis.italic
True
>>> Emphasis(value=3, name='italic')
ValueError: blah blah
```

### Ordering

Instances are ordered by [value](#values).

Since the default value is the name itself, the default ordering when iterating
over a Bnum is alphabetical (from comparison of the values, which are names, as
strings).

```python
>>> list(Colour)
[Colour('blue'), Colour('green'), Colour('red')]
```

If you choose numerical values (and don't give them yourself) then the
ordering will be as written in the class definition (because they are numbered
in the order given there):

```python
>>> for emphasis in Emphasis: print(repr(emphasis))
Emphasis(value=1, name='underline')
Emphasis(value=2, name='italic')
Emphasis(value=4, name='bold')
```

Mixing value types (like in `Strange`, above) may make comparison undefined.
In such cases, the order will be arbitrary (but fixed and error-free).

### Aliases

By default, it is an error to repeat a [value](#values), because mixing
implicit and explicit values could give very confusing bugs.  You can disable
this safety check by setting `allow_aliases=True`.

Aliases are not listed or retrieved, but can be used to identify the
"fundamental" instance:

```python
>>> class Error(ExplicitBnum, values=from_one):
...     with implicit:
...         a
...     b = 1  # an error
ValueError: Duplicate value for b, a
>>> class OK(ExplicitBnum, values=from_one, allow_aliases=True):
...     with implicit:
...         a
...     b = 1  # an alias
...
>>> repr(OK('b'))
OK(value=1, name='a')
>>> list(OK)
[OK(value=1, name='a')]
```

Advanced Use
------------

### Constructors And Methods

The following example shows how `ExplicitBnum` can define and instantiate
arbitrary classes:

```python
>>> class Animal(ExplicitBnum):
...
...     def __init__(self, legs, noise):
...         self.legs = legs
...         self.noise = noise
...
...     def talk(self):
...         return self.noise
...
...     def __str__(self):
...         return 'A %s has %d legs and says %r' % \
...                (self.name, self.legs, self.talk())
...
...     pig = 4, 'oink'
...     hen = 2, 'cluck'
...     cow = 4, 'moo'
...
>>> repr(Animal.pig)
Animal(value=(4, 'oink'), name='pig')
>>> Animal.pig
A pig has 4 legs and says 'oink'
>>> Animal((4, 'oink')) is Animal.pig
True
>>> Animal.pig.value
(4, 'oink')
```

Note that `value` is the value given in the definition, and not the instance.

`ImplicitBnum` does not support this (see the [FAQ](#faq)), but you can
still use `with implicit` inside an `ExplicitBnum`.

### Multiple Inheritance

It can sometimes be useful to have enumerations that *are* their value,
because then you can use the instance directly in expressions.  This can be
achieved by adding the value type (typically `int`) as a mixin:

```python
>>> class IntEmphasis(int, ImplicitBnum, values=bits):
...     underline
...     italic
...     bold
...
>>> 2 & (IntEmphasis.underline | IntEmphasis.italic)
2
>>> isinstance(IntEmphasis.underline, ImplicitBnum)
True
>>> isinstance(IntEmphasis.underline, int)
True
```

This works by constructing the given type from the value (use a tuple for
multiple arguments).  You will see errors if you mix incompatible types:

```python
>>> class Confused(int, ExplicitBnum):
...     foo = 'one'
...
ValueError: invalid literal for int() with base 10: 'one'
````

Here the default value is the name, which a string, which cannot be used to
construct an integer.

### Providing Implicit Values

The `values` parameter expects a no-argument function (called once per class
definition), which returns a second function from names to values.

So, for example, to give random values:

```python
>>> from random import random
>>> def random_values():
...     def value(name):
...         return random()
...     return value
...
>>> class Random(ImplicitBnum, values=random_values):
...     a, b, c
...
>>> list(Random)
[Random(value=0.49267653329514594, name='c'), Random(value=0.5521902021074088, name='b'), Random(value=0.5540234367417308, name='a')]
```

Comparison with Enum
--------------------

### Background

Python has an official Enum type,
[described in PEP 435](http://www.python.org/dev/peps/pep-0435/).  The code
expected (by me, at least) to implement that is
[currently on BitBucket](https://bitbucket.org/stoneleaf/ref435) and was
used as the basis for Bnum.

### List Of Differences

Changes to the Enum semantics include:

* values can be implicit (Enum requires explicit values in the "class" form,
  although there's undocumented support for this - see `auto_enum` in the
  tests - that uses a `name = ...` syntax, with an ellipsis);

* the default implicit value is the name;

* alternative implicit values are defined via `values` (Enum numbers from 1
  in the "functional" form, equivalent to `values=from_one`);

* instances can be retrieved by name or value when calling the class;

* aliases must be explicitly enabled;

* the default `__str__` implementation displays the value;

* ordering is by value;

* the "functional" form is not supported (please email me,
  [andrew@acooke.org](mailto:andrew@acooke.org),
  if you think something like this is important).

In addition, I debated for a long time whether to support multiple inheritance.
It is an awfully complicated way to avoid typing `.value`.

The most significant of these are related to the *definition* of enumerations.
So changing from Enum to Bnum will often require changing only one part of
the code base.

### Philosophy

You could characterise the Enum design as one driven by enumerations as
values (in particular, integers, reflecting a C or Java influence).
In contrast, I started from the idea that the simplest enumeration is a set of
symbols (names).

As with most designs, many choices are inter-linked; getting a consistent
set of choices is analogous to a local maximum in the "design space".
So the change in emphasis from values to names, plus a general desire for
consistency (both internally, and between Bnum and Enum), explains most
changes (and non-changes).

### Things You Can Do With Bnum (That You Can't Do With Enum)

Have a simple list of names in "class" form:

```python
>>> class Colour(ImplicitBnum):
...     red
...     green
...     blue
```

Detect a stupid mistake:

```python
>>> class Error(ExplicitBnum, values=from_one):
...     with implicit:
...         one
...         two
...     three = 2
...
ValueError: Duplicate value for three, two
```

Define bit fields:

```python
>>> class IntEmphasis(int, ImplicitBnum, values=bits):
...     underline
...     italic
...     bold
...
>>> allowed_styles = IntEmphasis.italic | IntEmphasis.bold
```

FAQ
---

### Why Implicit And Explicit?

The approach used to provide implicit values can only be used in a restricted
context (`with implicit`) or a class without other members (`ImplicitBnum`).

In a little more detail, implicit values are generated by providing a default
value for any name requested from the class dictionary.  This causes problems
when the name exists in an outer scope, because it is shadowed by the
default value.

This is not an issue if you are *only* defining a list of names.  So implicit
values are restricted to that case - either in a class that can only define
names, or within a scope.

### Didn't You Say This Was A Syntax Error?

Yes, I [did](http://www.acooke.org/cute/Pythonssad0.html).  I was wrong.

[Duncan Booth](http://www.acooke.org/cute/Pythonssad0.html#Fri17May20131519040100)
provided the solution *and* the motivation to question my betters.

### Isn't Explicit Better Than Implicit?

Not in this case, apparently.

But, if you disagree, you're free to write:

```python
>>> class Colour(ExplicitBnum):
...     red = 'red'
...     green = 'green'
...     blue = 'blue'
```

### Why Not Influence The Official Design?

I think a good design comes from one person.  There should be discussion, but
one person should *own* the design and care enough to make it consistent and
elegant (so, for example, the language Go has a consistent, elegant design,
even if it's [nothing like](http://www.acooke.org/cute/GoRocksHow0.html)
my perfect language).  That seems to have been lost in the Python process for
Enum (even though generally, with the BDFL approach, they do this quite well).

### So This Is What You Think Enum Should Be?

No.  Not at all.  This design accepts that Enum exists and makes *many*
compromises to provide something as similar as possible.
If I were starting from scratch, the design would be much simpler -
inheritance has *way* too much emphasis here.

Which is why I abandoned this project.

Credits
-------

Despite my intemperate language in the rant, this work would not have been
possible without the prior work of those who developed Enum.  Particularly
Ethan Furman (I learnt a lot trying to understand that code).
