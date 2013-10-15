.. index::
   single: type
   single: types; basic

.. _type:

Type-specific keywords
======================

The ``type`` keyword is fundamental to JSON Schema.  It specifies the
data type for a schema.

At its core, JSON Schema defines the following basic types:

.. only:: html

    .. toctree::
       :maxdepth: 1

       string.rst
       numeric.rst
       object.rst
       array.rst
       boolean.rst
       null.rst

.. only:: latex

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
    The following table maps from the names of Javascript types to
    their analogous types in Python:

    +----------+-----------+
    |Javascript|Python     |
    +----------+-----------+
    |string    |string     |
    |          |[#1]_      |
    +----------+-----------+
    |integer   |int        |
    +----------+-----------+
    |number    |float      |
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

    .. [#1] Since Javascript strings always support unicode, they are
            analogous to ``unicode`` on Python 2.x and ``str`` on
            Python 3.x.

The ``type`` keyword may either be a string or an array.  If it's a
string, it is the name of oone of the basic types above.  If it is an
array, it must be an array of strings, where each string is the name
of one of the basic types, and each element is unique.

Each of these types have their own keywords to make the validation
more specific.  For example, numeric types have a way of specifying a
numeric range, that would not be applicable to other types.  In this
reference, these validation keywords are described along with each of
their corresponding types.

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

.. only:: latex

    .. toctree::
       :maxdepth: 1

       string.rst
       numeric.rst
       object.rst
       array.rst
       boolean.rst
       null.rst
