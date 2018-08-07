.. index::
   single: type
   single: types; basic

.. _type:

Type-specific keywords
======================

The ``type`` keyword is fundamental to JSON Schema.  It specifies the
data type for a schema.

At its core, JSON Schema defines the following basic types:

   - `string`
   - `numeric`
   - `object`
   - `array`
   - `boolean`
   - `null`

These types have analogs in most programming languages, though they
may go by different names.

.. language_specific::

    --Python
    The following table maps from the names of JavaScript types to
    their analogous types in Python:

    +----------+-----------+
    |JavaScript|Python     |
    +----------+-----------+
    |string    |string     |
    |          |[#1]_      |
    +----------+-----------+
    |number    |int/float  |
    |          |[#2]_      |
    +----------+-----------+
    |object    |dict       |
    +----------+-----------+
    |array     |list       |
    +----------+-----------+
    |boolean   |bool       |
    +----------+-----------+
    |null      |None       |
    +----------+-----------+

    .. rubric:: Footnotes

    .. [#1] Since JavaScript strings always support unicode, they are
            analogous to ``unicode`` on Python 2.x and ``str`` on
            Python 3.x.

    .. [#2] JavaScript does not have separate types for integer and
            floating-point.


    --Ruby
    The following table maps from the names of JavaScript types to
    their analogous types in Ruby:

    +----------+----------------------+
    |JavaScript|Ruby                  |
    +----------+----------------------+
    |string    |String                |
    +----------+----------------------+
    |number    |Integer/Float         |
    |          |[#3]_                 |
    +----------+----------------------+
    |object    |Hash                  |
    +----------+----------------------+
    |array     |Array                 |
    +----------+----------------------+
    |boolean   |TrueClass/FalseClass  |
    +----------+----------------------+
    |null      |NilClass              |
    +----------+----------------------+

    .. rubric:: Footnotes

    .. [#3] JavaScript does not have separate types for integer and
            floating-point.

The ``type`` keyword may either be a string or an array:

- If it's a string, it is the name of one of the basic types above.

- If it is an array, it must be an array of strings, where each string
  is the name of one of the basic types, and each element is unique.
  In this case, the JSON snippet is valid if it matches *any* of the
  given types.

Here is a simple example of using the ``type`` keyword:

.. schema_example::

   { "type": "number" }
   --
   42
   --
   42.0
   --X
   // This is not a number, it is a string containing a number.
   "42"

In the following example, we accept strings and numbers, but not
structured data types:

.. schema_example::

   { "type": ["number", "string"] }
   --
   42
   --
   "Life, the universe, and everything"
   --X
   ["Life", "the universe", "and everything"]

For each of these types, there are keywords that only apply to those
types.  For example, numeric types have a way of specifying a numeric
range, that would not be applicable to other types.  In this
reference, these validation keywords are described along with each of
their corresponding types in the following chapters.
