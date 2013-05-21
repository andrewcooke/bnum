A Simpler, Better Enum For Python
=================================

Note - this is just a first draft and may contain impossible syntax or
semantics.

At its simplest, a Bnum defines a collection of names:

```python
>>> class Colour(Bnum):
...     red
...     green
...     blue
...
>>> Colour.red == Color.blue
False
>>> Colour.red == Colour.red
True
>>> isinstance(Colour.red, Colour):
True
>>> Colour.red.name
'red'
>>> Colour.red.value
'red'
>>> Colour.red  # uses str()
'red'
>>> repr(Colour.red)
Colour('red')
>>> repr(Colour('red'))  # retrieves instance from name
Colour('red')
```

Values
------

Often, names are all you need (think of atoms in Lisp).  But some languages
associate *values* with enumerations.  These are often integers, counting
from 0 or 1, or bit fields.

With Bnum, you can choose the kind of value using a mixin.  The default value
is the name, but alternatives include `Bits`, `FromZero` and `FromOne`:

```python
>>> class Emphasis(Bnum, Bits):
...     underline
...     italic
...     strong
...
>>> Emphasis.underline.value
1
>>> Emphasis.strong.value
4
>>> Emphasis.strong.name
'strong'
>>> int(Emphasis.strong)
4
>>> str(Emphasis.strong)
'4'
>>> 2 & (Emphasis.italic | Emphasis.strong)
2
>>> class Weekday(Bnum, FromOne):
...     monday
...     tuesday
...     wednesday
...     thursday
...     friday
...     saturday
...     sunday
...
>>> Weekday.sunday  # uses str()
7
>>> Weekday.sunday.name
'sunday'
>>> repr(Weekday.sunday):
Weekday(name='sunday', value=7)
```

Note that values are automatically used in expressions.  This means that
that `__str__()` returns the value (as a string), so that instances will
 be correctly converted to strings.

You can also specify your own values (the default is the name):

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz  # = 'baz'
```

Retrieving Instances
--------------------

Instances can be retrieved by name or value (or both, provided they are
consistent):

```python
>>> repr(Colour('red'))  # default is name
Colour('red')
>>> repr(Colour(name='green'))
Colour('green')
>>> repr(Colour(name='blue', value='blue'))
Colour('blue')
>>> Colour(name='red', value='blue')
Error: blah blah
>>> repr(Emphasis(value=2))
Emphasis(name='italic', value=2)
>>> Emphasis(value=3)
Error: blah blah
```

Ordering
--------

When you iterate over the contents they are ordered by *value*.  The default
value is the name itself, so by default they are ordered alphabetically:

```python
>>> class Colour(Bnum):
...     red
...     green
...     blue
...
>>> for colour in Colour: print(colour)
'blue'
'green'
'red'
```

If you choose numerical values (and don't give them yourself) then the
ordering will be as given (because they are numbered in the order given):

```python
>>> class Emphasis(Bnum, Bits):
...     underline
...     italic
...     strong
...
>>> for emphasis in Emphasis: print(repr(emphasis))
Emphasis(name='underline', value=1)
Emphasis(name='italic', value=2)
Emphasis(name='strong', value=4)
```

Aliases
-------

It's an error to repeat a value unless you explicitly allow for aliases.
Aliases are valid instances, but are not listed or retrieved.

```python
>>> class Error(Bnum):
...     a = 1
...     b = 1  # an error
Error: blah blah
>>> class OK(Bnum, AllowAliases):
...     a = 1
...     b = 1  # an alias
...
>>> repr(OK('b'))
OK(name='a', value=1)
```
