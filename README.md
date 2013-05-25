A Better Enum For Python 3
==========================

* [Basic Use](#basic-use)
   * [Names](#names)
   * [Values](#values)
   * [Retrieving Instances](#retrieving-instances)
   * [Ordering](#ordering)
   * [Aliases](#aliases)
   


Basic Use
---------

### Names

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
>>> repr(Colour.red)
Colour('red')
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

If you have a name (as a string) then the appropriate instance can be
retrieved by calling the class:

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
...     monday
...     tuesday
...     wednesday
...     thursday
...     friday
...     saturday
...     sunday
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
>>> 2 & (Emphasis.italic | Emphasis.bold)
TypeError: blah, blah
```

To make the final line work as you might expect, see the
[section on inheritance](#Inheritance) below.

You can even mix value types, although it may make the [ordering](#Ordering)
undefined:

```python
>>> class Strange(Bnum):
...     foo = 42
...     bar = 'fish'
...     baz  # = 'baz' - implicitly the name, since no values argument given
```

The only value you cannot have is `None`, which will be treated as missing
and replaced by an implicit value.

Finally, you can implement support for alternative implicit values:

```python
TODO
```

### Retrieving Instances

If you have the value, or name (or both, as long as they are consistent), then
you can get the appropriate instance by calling the class:

```python
>>> Colour('red') is Colour.red  # default is to use the value
True
>>> repr(Emphasis(2))
Emphasis(value=2, name='italic')
>>> repr(Emphasis(name='italic'))
Emphasis(value=2, name='italic')
>>> Emphasis(name='italic')
Emphasis(value=2, name='italic')
>>> Emphasis(value=3, name='italic')
Error: blah blah
```

### Ordering

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

### Aliases

By default, it is an error to repeat a value, because mixing implicit and
explicit values could give very confusing bugs.  You can disable this safety
check by setting `allow_aliases=True`.

Aliases are valid instances, but are not listed or retrieved (frankly, I think
they're a mistake, but Bnum provides them to help inter-operate with Python's
Enum):

```python
>>> class Error(Bnum, values=from_one):
...     a
...     b = 1  # an error
Error: blah blah
>>> class OK(Bnum, values=from_one, allow_aliases=True):
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