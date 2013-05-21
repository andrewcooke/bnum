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
>>> isinstance(Colour.red, Colour):
True
```

Values
------

Often, names are all you need (think of atoms in Lisp).  But some languages
associate *values* with enumerations.  These are often integers, counting
from 0 or 1, or bit fields.

With Bnum, you can choose the kind of value using a mixin:

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

Note that the values are automatically used in expressions.

You can also specify your own values (the default is the name):

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz  # = 'baz'
```

Retrieving Instances
--------------------

```python
>>> Colour(name='green')
green
>>> Colour('red')  # default is name
red
>>> Colour(name='red', value='red')
red
>>> Colour(name='red', value='blue')
Error: blah blah
>>> Emphasis(value=2)
italic
>>> Emphasis(value=3)
Error: blah blah
```

Ordering
--------

When you iterate over the contents they are ordered by *value*.  The default
value is the name itself, so by default they are ordered alphabetically.

```python
>>> class Colour(Bnum):
...     red
...     green
...     blue
...
>>> for colour in Colour: print(colour)
Colour('blue')
Colour('green')
Colour('red')
```

If you choose numerical values (and don't give them yourself) then the
ordering will be as given:

```python
>>> class Emphasis(Bnum, Bits):
...     underline
...     italic
...     strong
...
>>> for emphasis in Emphasis: print(emphasis)
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
...     b = 1  # an alias
Error: blah blah
>>> class OK(Bnum, AllowAliases):
...     a = 1
...     b = 1
...
>>> OK('b')
OK('a')
```

