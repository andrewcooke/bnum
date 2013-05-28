
A Slightly Better Enum For Python 3
===================================

Bnum is an enumeration class for Python 3.  It is broadly
[compatible](#list-of-differences) with the
[standard Enum](http://www.python.org/dev/peps/pep-0435/) (and uses much of
the same code), but has been tweaked to address
[issues](#things-you-can-do-with-bnum-that-you-cant-do-with-enum)
identified in a
[rant](http://www.acooke.org/cute/Pythonssad0.html) I wrote some time ago.

* [Quick Start](#quick-start)
* [Basic Use](#basic-use)
   * [Names](#names)
   * [Values](#values)
   * [Retrieving Instances](#retrieving-instances)
   * [Ordering](#ordering)
   * [Aliases](#aliases)
* [Advanced Use](#advanced-use)
   * [Multiple Inheritance](#multiple-inheritance)
   * [Calculating Implicit Values](#calculating-implicit-values)
* [FAQ](#faq)
   * [Why The Ellipses?](#why-the-ellipses)
* [Comparison With Enum](#comparison-with-enum)
   * [Background](#background)
   * [List Of Differences](#list-of-differences)
   * [Philosophy](#philosophy)
   * [Things You Can Do With Bnum (That You Can't Do With Enum)](#things-you-can-do-with-bnum-that-you-cant-do-with-enum)
* [Credits](#credits)

Quick Start
-----------

```bash
easy_install bnum
```

If you just need a set of names (the `...` are typed just like that - see
[FAQ](#why-the-ellipses)):

```python
>>> from bnum import Bnum
>>> class Colour(Bnum):
...     red = ...
...     green = ...
...     blue = ...
...
>>> for colour in Colour: print(colour)
blue
green
red
```

```python
>>> from bnum import Bnum
>>> class Colour(Bnum):
...     with auto():
...         red
...         green
...         blue
...
>>> for colour in Colour: print(colour)
blue
green
red
```

If you want integers from 1, and the ability to use enumeration values
in expressions (so the enumeration *is* an `int`):

```python
>>> from bnum import Bnum, from_one
>>> class Numbers(int, Bnum, values=from_one):
...     one = ...
...     two = ...
...     seven = 7
...
>>> Numbers.one + Numbers.seven
8
>>> isinstance(Number.two, int)
True
```

```python
>>> from bnum import Bnum, from_one
>>> class Numbers(int, Bnum):
...     with auto(from_one):
...         one
...         two
...     seven = 7
...
>>> Numbers.one + Numbers.seven
8
>>> isinstance(Number.two, int)
True
```

Basic Use
---------

### Names

At its simplest, a Bnum defines a collection of distinct names:

```python
>>> class Colour(Bnum):
...     red = ...
...     green = ...
...     blue = ...
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
['blue', 'green', 'red']  # TODO - check
>>> len(Colour)
3
>>> Colour.red in Colour
True
```

### Values

Instances have values as well as names.

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
>>> class FavouriteNumbers(Bnum):
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
>>> class Weekday(Bnum, values=from_one):
...     monday = ...
...     tuesday = ...
...     wednesday = ...
...     thursday = ...
...     friday = ...
...     saturday = ...
...     sunday = ...
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
>>> class Emphasis(Bnum, values=bits):
...     underline = ...
...     italic = ...
...     bold = ...
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
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz = ...  # implicitly the name, since no values argument given
```

The only value you cannot have is `...` (ellipsis), which will be treated as
missing and replaced by an implicit value.

### Retrieving Instances

If you have the value, or name (or both, as long as they are consistent), then
you can get the appropriate instance by calling the class:

```python
>>> Colour('red') is Colour.red  # default is to use the value
True
>>> Emphasis(2) is Emphasis.italic
True
>>> Emphasis(name='italic') is Emphasis(value=2, name='italic') is Emphasis.italic
True
>>> Emphasis(value=3, name='italic')
Error: blah blah
```

### Ordering

Instances are ordered by value.

Since the default value is the name itself, the default ordering when iterating
over a Bnum is alphabetical (from comparison of the values, which are names, as
strings).

```python
>>> list(Colour)
['blue', 'green', 'red']  # TODO - check
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

By default, it is an error to repeat a value, because mixing implicit and
explicit values could give very confusing bugs.  You can disable this safety
check by setting `allow_aliases=True`.

Aliases are valid instances, but are not listed or retrieved:

```python
>>> class Error(Bnum, values=from_one):
...     a = ...
...     b = 1  # an error
Error: blah blah
>>> class OK(Bnum, values=from_one, allow_aliases=True):
...     a = ...
...     b = 1  # an alias
...
>>> repr(OK('b'))
OK(name='a', value=1)
>>> list(OK)
[1]  # TODO - check the correct output here; maybe len() would be better?
```

Advanced Use
------------

### Multiple Inheritance

It can sometimes be useful to have enumerations that *are* their value,
because then you can use the instance directly in expressions.  This can be
achieved by adding the required type (typically `int` as a mixin):

```python
>>> class IntEmphasis(int, Bnum, values=bits):
...     underline = ...
...     italic = ...
...     bold = ...
...
>>> 2 & (IntEmphasis.underline | IntEmphasis.italic)
2
>>> isinstance(IntEmphasis.underline, Bnum)
True
>>> isinstance(IntEmphasis.underline, int)
True
```

This works by constructing the given type from the value (use a tuple for
multiple arguments).  You will see errors if you mix incompatible types:

```python
>>> class Confused(int, Bnum):
...     string = ...
...
Error: blah, blah
````

Here the default value is the name, which a string, which cannot be used to
construct an integer.

FAQ
---

### Why The Ellipses?

Why not use

```python
>>> class Colour(Bnum):
...     red
...     green
...     blue
```

as [described](http://www.acooke.org/cute/Pythonssad0.html#Fri17May20131519040100)
by Duncan Booth?

Unfortunately, this requires the class dictionary to supply `None` (or
some other flag value) for names that do not exist.  While that works fine in
simple cases it shadows any global references (which are first resolved against
class scope and then, on failure, against the surrounding scope).

The only solutions I can see are:

1. use a special (explicit) value;
1. use a special format for names;
1. use strings rather than identifiers;
1. use a new (`with`) scope to introduce names with implicit values.

The first, with ellipses, is what Enum uses for its auto-numbering (currently
undocumented, but visible in the source) and it seems better than the
alternatives.

A restricted scope

```python
>>> class Colour(Bnum):
...     with values(from_one):
...         red
...         green
...         blue
```

can isolate the problem to a smaller region of the class, but still has
problems with globals used to define enumeration values.

Comparison with Enum
--------------------

### Background

Python has an official Enum type,
[described in PEP 435](http://www.python.org/dev/peps/pep-0435/).  The code
used to implement that is
[currently on BitBucket](https://bitbucket.org/stoneleaf/ref435) and was
used as the basis for Bnum.

### List Of Differences

Changes to the Enum semantics include:

* values can be implicit (Enum requires explicit values in the "class" form,
  although there's undocumented support for this - see `auto_enum` in the
  tests);

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
names.

As with most designs, many choices are inter-linked; getting a consistent
set of choices is analogous to a local maximum in the "design space".
So the change in emphasis from values to names, plus a general desire for
consistency (both internally, and between Bnum and Enum), explains most
changes (and non-changes).

### Things You Can Do With Bnum (That You Can't Do With Enum)

Have a simple list of names in "class" form:

```python
>>> class Colour(Bnum):
...     red = ...
...     green = ...
...     blue = ...
```

Detect a stupid mistake:

```python
>>> class Error(Bnum, values=from_one):
...     one = ...
...     two = ...
...     three = 2
...
Error: blah, blah
```

Define bit fields:

```python
>>> class IntEmphasis(int, Bnum, values=bits):
...     underline = ...
...     italic = ...
...     bold = ...
...
>>> allowed_styles = IntEmphasis.italic | IntEmphasis.bold
```

Credits
-------

Despite my intemperate language in the rant, this work would not have been
possible without the prior work of those who developed Enum (I learnt a lot
trying to understand that code).
