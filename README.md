A Better Enum For Python
========================

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
>>> Colour.red.name
'red'
```

Values
------

Often, names are all you need (think of atoms in Lisp).  But some languages
associate *values* with enumerations.  These are often integers, counting
from 0 or 1, or bit fields.

With Bnum, you can choose the kind of value using a mixin:

```python
>>> class Emphasis(Bnum, Bits):
...     italic
...     strong
...     underline
...
>>> Emphasis.italic.value
1
>>> Emphasis.underline.value
4
>>> 2 & (Emphasis.italic | Emphasis.strong)
2
>>> class Weekday(Bnum, FromOne):
...     monday
...     ...
...     sunday
...
>>> Weekday.sunday.value
7
```

You can also specify your own values:

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
```

but by default it's an error to repeat a value:

```python
>>> class Error(Bnum):
...     a = 1
...     b = 1
Error: blah blah
>>> class OK(Bnum, AllowAliases):
...     a = 1
...     b = 1
...
>>> OK('b')
OK('a')
```

Ordering
--------

By default, contents are ordered as given in the source.

```python
>>> for colour in Colour: print(str(colour))
red
green
blue
>>> for colour in Colour: print(repr(colour))
Colour('red')
Colour('green')
Colour('blue')
```

but you can also order by value:

```python
>>> class Colour(Bnum, OrderByValue):
...     red = 2
...     green = 1
...     blue = 3
...
>>> for colour in Colour: print(str(colour))
green
red
blue
```
