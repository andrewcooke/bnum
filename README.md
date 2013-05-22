A Better Enum For Python 3
==========================

At its simplest, a Bnum defines a collection of distinct names:

```python
>>> class Colour(Bnum):
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
>>> Colour.red  # uses str() on the value - see more below
red
>>> repr(Colour.red)
Colour('red')
```

If you have a name (as a string) then the appropriate instance can be
retrieved by calling the class:

```python
>>> Colour('red') is Colour.red
True
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

Values
------

Instances have values as well as names.

The default, implicit value of an instance is its name (which is why the
initial `Colour` example returned the name):

```python
>>> Colour.red.value
red
>>> Colour.red  # this is str() of the value, which is the value, which is the name
red
>>> type(Colour.red.value)
<class str>
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
>>> FavouriteNumbers.seven  # the value is used when you reference the instance
7
```

But usually you want integers, counting from 0 or 1, or bit fields and
Bnum will provide these if you use an appropriate mixin.

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

The final line above shows that when an instance's name and value differ, both
are shown in the output from `repr()`.  That same syntax can also be used to
retrieve values - see the next section.

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

Note that values are automatically used in expressions involving instances.
This means that that `__str__()` returns the value (as a string), so that
the value of instances will be correctly converted to strings.

You can even mix value types, although it make make the ordering undefined
(see below):

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz  # = 'baz' - implicitly the name, since no mixin used
```

The only value you cannot have is `None`, which will be treated as missing
and replaced by an implicit value.

Finally, you can implement support for alternative implicit values:

```python
TODO
```

Retrieving Instances
--------------------

If you have the name or value (or both, as long as they are consistent), then
you can get the appropriate instance by calling the class:

```python
>>> Colour('red') is Colour.red  # default is to use the name
True
>>> Colour(name='green') is Colour.green
True
>>> repr(Emphasis(value=2))
Emphasis(name='italic', value=2)
>>> Emphasis(name='italic', value=3)
Error: blah blah
```

Ordering
--------

Values are used in expressions - like comparison - using instances.  So
if you sort a list of instances they will be sorted by value.  This is the
same ordering that is used when iterating over the instances of a Bnum.

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

Aliases are valid instances, but are not listed or retrieved (frankly, I think
they're a mistake, but Bnum provides them to help inter-operate with Enum):

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

Comparison with Enum
--------------------

Python has an official Enum type, described ...

Differences:

* Something

Summary.