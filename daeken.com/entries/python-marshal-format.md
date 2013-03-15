#title Python Marshal Format
#date 2010-02-20

Earlier this week, I had to deal with some files in Python's marshal format (some `.pyc` files, specifically) in Ruby and discovered that the details of this format aren't documented. Since it's meant to be purely internal, the Python team has decided not to document it in any way.

The marshal format is used in `.pyc` files, lots of internal storage for random apps, etc. It's a shame that it's undocumented, as this means that there are, to my knowledge, no implementations for other languages. This also means that if you have a malicious marshal blob, you have to load it up with Python to play around with it; not a good idea.

Fortunately, you can read the source [(Python/marshal.c)][1] and figure out how it works pretty easily. However, to make it even easier, I've decided to write up some simple documentation on the format. I'll give types as `int/uint` where n is the number of bits. The `object` type indicates that this is a marshalled object.

 [1]: http://svn.python.org/view/python/trunk/Python/marshal.c?view=markup

# Format

The marshal format in and of itself is very simple. It consists of a series of nested objects, represented by a type (`uint8` -- a char, in fact) followed by some serialized data. All data is little-endian.

Note: I wrote all of this for the 2.x line. I don't know how much has changed in 3.x.

# Types

## Constants

These types contain no data and are simply representations of Python constants.

*   `0` (`TYPE_NULL`) -- Used to null terminate dictionaries and to represent the serialization of a null object internally (not sure if this can happen or not).
*   `N` (`TYPE_NONE`) -- Represents the `None` object.
*   `F` (`TYPE_FALSE`) -- Represents the `False` object.
*   `T` (`TYPE_TRUE`) -- Represents the `True` object.
*   `S` (`TYPE_STOPITER`) -- Represents the `StopIteration` exception object.
*   `.` (`TYPE_ELLIPSIS`) -- Represents the `Ellipsis` object.

## Numbers

*   `i` (`TYPE_INT`) -- Represents a `int` on a 32-bit machine. Stored as an `int32`.
*   `I` (`TYPE_INT64`) -- Represents a `int` on a 64-bit machine. Stored as an `int64`. When read on a 32-bit machine, this may automatically become a `long` (if it's above `2**31`).
*   `f` (`TYPE_FLOAT`) -- Represents a `float` in the old (< 1) marshal format. Stored as a string with a `uint8` before it indicating the size.
*   `g` (`TYPE_BINARY_FLOAT`) -- Represents a `float` in the new marshal format. Stored as a `float64`. (Thanks to Trevor Blackwell for noting that these are not `float32` (along with `TYPE_BINARY_COMPLEX`).)
*   `x` (`TYPE_COMPLEX`) -- Represents a `complex` in the old (< 1) marshal format. Contains the real and imaginary components stored like TYPE_FLOAT; that is, as strings.
*   `y` (`TYPE_BINARY_COMPLEX`) -- Represents a `complex` in the new marshal format. Stored as two `float64`s representing the real and imaginary components.
*   `l` (`TYPE_LONG`) -- Represents a `long`. Haven't yet figured out how this works; I'll update shortly with that.

## Strings

*   `s` (`TYPE_STRING`) -- Represents a `str`. Stored as a `int32` representing the size, followed by that many bytes.
*   `t` (`TYPE_INTERNED`) -- Represents a `str`. Identical to `TYPE_STRING`, with the exception that it's added to an "interned" list as well.
*   `R` (`TYPE_STRINGREF`) -- Represents a `str`. Stored as a `int32` reference into the interned list mentioned above. Note that this is zero-indexed.
*   `u` (`TYPE_UNICODE`) -- Represents a `unicode`. Stored as a `int32` representing the size, followed by that many bytes. This is always UTF-8.

## Collections

*   `(` (`TYPE_TUPLE`) -- Represents a `tuple`. Stored as a `int32` followed by that many objects, which are marshalled as well.
*   `[` (`TYPE_LIST`) -- Represents a `list`. Stored identically to `TYPE_TUPLE`.
*   `{` (`TYPE_DICT`) -- Represents a `dict`. Stored as a series of marshalled key-value pairs. At the end of the dict, you'll have a "key" that consists of a `TYPE_NULL`; there's no value following it.
*   `>` (`TYPE_FROZENSET`) -- Represents a `frozenset`. Stored identically to `TYPE_TUPLE`.

## Code objects

Code objects (like that in a `.pyc` file, or in the `func_code` property of a function) use the `c` (`TYPE_CODE`) type flag. Even in the case of the top level (as in a `.pyc`), they represent a function.

They consist of the following fields:

*   `argcount` (`int32`) -- Number of arguments.
*   `nlocals` (`int32`) -- Number of local variables.
*   `stacksize` (`int32`) -- Max stack depth used.
*   `flags` (`int32`) -- Flags for the function. 
    *   `0x04` -- Has `*args`.
    *   `0x08` -- Has `**kwargs`.
    *   `0x20` -- Generator.
    *   This list is not all encompassing; certain `__future__` declarations will set their own flags.
*   `code` (`object`) -- String representation of the bytecode.
*   `consts` (`object`) -- Tuple of constants used.
*   `names` (`object`) -- Tuple of names.
*   `varnames` (`object`) -- Tuple of variable names (this includes arguments and locals).
*   `freevars` (`object`) -- Tuple of "free" variables. (Can anyone clarify this a bit?)
*   `cellvars` (`object`) -- Tuple of variables used in nested functions.
*   `filename` (`object`) -- String containing the original filename this code object was generated from.
*   `name` (`object`) -- Name of the function. If it's the top level code object in a `.pyc`, this will be `<module>`.
*   `firstlineno` (`int32`) -- First line number of the code this code object was generated from.
*   `lnotab` (`object`) -- String mapping bytecode offsets to line numbers. Haven't delved into the details here.

# RMarshal

I've implemented support for unmarshalling objects as well as reading `.pyc`s in a Ruby gem called RMarshal. You can get it from [Gemcutter][2] or from [Github][3].

 [2]: http://gemcutter.org/gems/rmarshal
 [3]: http://github.com/daeken/RMarshal

# Closing

Hopefully this will be of use to someone. One potential use is in studying malicious marshalled data; the Python guys strongly recommend against unmarshalling untrusted data, but we all know how well such notices are regarded. In addition, it may help you manipulate Python bytecode from non-Python languages.

Drop me a line if you do anything cool with it.

Happy Hacking,   
- Cody Brocious (Daeken)
