A Simpler, Better Enum For Python 3
===================================

At its simplest, a Bnum defines a collection of distinct names:

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

You can iterate over the instances defined in a class:

```python
>>> len(Colour)
3
>>> list(Colour)
['blue', 'green', 'red']  # TODO - check
```

Values
------

With Bnum, the default, implicit value of an instance is the name:

```python
>>> Colour.red.value
red
>>> Colour.red
red
>>> type(Colour.red.value)
<class str>
```

Often, names are all you need (think of symbols in Lisp).  But some languages
associate alternative values with enumerations.  These are usually integers,
counting from 0 or 1, or bit fields.

Using the `Bits` mixin provides bit fields:

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
```

The `FromOne` mixin provides integers counting from 1 (there's also a
`FromZero` that, yes, you guessed right):

```python
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

Note that values are automatically used in expressions involving instances.
This means that that `__str__()` returns the value (as a string), so that
the value of instances will be correctly converted to strings.

You can also specify your own, explicit values (and they can even have mixed
types, although that may make ordering unclear - see below):

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz  # = 'baz' - implicitly the name, since no mixin used
```

The only value you cannot have is `None` (that will be treated as a missing
value and an implicit value supplied - the name by default).

Finally, you can implement support for alternative implicit values:

```python
TODO
```

Retrieving Instances
--------------------

If you have the name or value (or both, as long as they are consistent), then
you can get the appropriate instance by calling the class:

```python
>>> repr(Colour('red'))  # default is name
Colour('red')
>>> Colour('red') is Colour.red
True
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

Values are used in expressions - like comparison - using instances.  So
if you sort a list of instances they will be sorted by value.  This is the
same ordering that is used for iteration over Bnum contents.

Since the default value is the name itself, the default ordering when iterating
over a Bnum is alphabetical (from comparison of the `str` values).

```python
>>> list(Colour)
['blue', 'green', 'red']  # TODO - check
```

If you choose numerical values (and don't give them yourself) then the
ordering will be as written in the class definition (because they are numbered
in the order given there):

```python
>>> for emphasis in Emphasis: print(repr(emphasis))
Emphasis(name='underline', value=1)
Emphasis(name='italic', value=2)
Emphasis(name='bold', value=4)
```

Mixing value types (like in `Strange`, above) may make comparison undefined.
In such cases, the order will be arbitrary (but fixed and error-free).

Aliases
-------

By default, it is an error to repeat a value, because mixing implicit and
explicit values could give very confusing bugs.  You can disable this safety
check by adding the `AllowAliases` mixin.

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
>>> list(OK)
[1]  # TODO - check the correct output here; maybe len() would be better?
```
