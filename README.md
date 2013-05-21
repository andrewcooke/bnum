A Simpler, Better Enum For Python 3
===================================

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
red
>>> Colour.red  # uses str() on the value - see more below
red
>>> repr(Colour.red)
Colour('red')
>>> repr(Colour('red'))  # retrieves instance from name
Colour('red')
```

Values
------

Often, names are all you need (think of atoms in Lisp).  But some languages
associate alternative *values* with enumerations.  These are usually integers,
counting from 0 or 1, or bit fields.

With Bnum, the default value is the name:

```python
>>> Colour.red.value
red
>>> Colour.red
red
>>> type(Colour.red.value)
<class str>
```

You can choose a different value using a mixin.  Alternatives include `Bits`,
`FromZero` and `FromOne`:

```python
>>> class Emphasis(Bnum, Bits):
...     underline
...     italic
...     bold
...
>>> Emphasis.underline.value
1
>>> type(Emphasis.underline.value)
<class int>
>>> Emphasis.bold.value
4
>>> Emphasis.bold.name
bold
>>> int(Emphasis.bold)
4
>>> str(Emphasis.bold)
4
>>> 2 & (Emphasis.italic | Emphasis.bold)
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
>>> Weekday.sunday.value
7
>>> Weekday.sunday.name
sunday
>>> Weekday.sunday  # uses str(), which converts the value to a string
7
>>> repr(Weekday.sunday):
Weekday(name='sunday', value=7)
```

Note that values are automatically used in expressions.  This means that
that `__str__()` returns the value (as a string), so that the value of
instances will be correctly converted to strings.

You can also specify your own values:

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz  # = 'baz' since no other value mixin used
```

The only value you can't have is `None` (that will be treated as a missing
value and an implicit value supplied - the name by default).

Retrieving Instances
--------------------

Instances can be retrieved by name or value (or both, provided they are
consistent):

```python
>>> repr(Colour('red'))  # default is name
Colour('red')
>>> repr(Colour(name='green'))
Colour('green')
>>> repr(Colour(value='blue'))
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
blue
green
red
```

If you choose numerical values (and don't give them yourself) then the
ordering will be as given (because they are numbered in the order given):

```python
>>> class Emphasis(Bnum, Bits):
...     underline
...     italic
...     bold
...
>>> for emphasis in Emphasis: print(repr(emphasis))
Emphasis(name='underline', value=1)
Emphasis(name='italic', value=2)
Emphasis(name='bold', value=4)
```

Mixing value types (like in `Strange`, above) may make comparison undefined.
In such cases, the order will be arbitrary (but fixed and error-free).

Aliases
-------

It's an error to repeat a value, because mixing implicit and explicit values
could give very confusing bugs, unless you explicitly allow for aliases.

Aliases are valid instances, but are not listed or retrieved:

```python
>>> class Error(Bnum, FromOne):
...     a
...     b = 1  # an error
Error: blah blah
>>> class OK(Bnum, FromOne, AllowAliases):
...     a
...     b = 1  # an alias
...
>>> repr(OK('b'))
OK(name='a', value=1)
```
