.. index::
   single: integer
   single: number
   single: types; numeric

.. _numeric:

Numeric types
-------------

There are two numeric types in JSON Schema: `integer` and `number`.  They
share the same validation keywords.

.. note::

    JSON has no standard way to represent complex numbers, so there is
    no way to test for them in JSON Schema.

.. _integer:


integer
'''''''

The ``integer`` type is used for integral numbers.

.. language_specific::
    --Python
    In Python, "integer" is analogous to the ``int`` type.

.. schema_example::

    { "type": "integer" }
    --
    42
    --
    -1
    --X
    // Floating point numbers are rejected:
    5.0
    --X
    // Numbers as strings are rejected:
    "42"

.. index::
   single: number

.. _number:

number
''''''

The ``number`` type is used for any numeric type, either integers or
floating point numbers.

.. language_specific::
    --Python
    In Python, "number" is analogous to the ``float`` type.

.. schema_example::

    { "type": "number" }
    --
    42
    --
    -1
    --
    // Simple floating point number:
    5.0
    --
    // Exponential notation also works:
    2.99792458e8
    --X
    // Numbers as strings are rejected:
    "42"

.. index::
   single: multipleOf
   single: number; multiple of

Multiples
'''''''''

Numbers can be restricted to a multiple of a given number, using the
``multipleOf`` keyword.  It may be set to any positive number.

.. schema_example::
    {
        "type"       : "number",
        "multipleOf" : 10
    }
    --
    0
    --
    10
    --
    20
    --X
    // Not a multiple of 10:
    23

.. index::
   single: number; range
   single: maximum
   single: exclusiveMaximum
   single: minimum
   single: exclusiveMinimum

Range
'''''

Ranges of numbers are specified using a combination of the
``minimum``, ``maximum``, ``exclusiveMinimum`` and
``exclusiveMaximum`` keywords.

- ``minimum`` specifies a minimum numeric value.

- ``exclusiveMinimum`` is a boolean.  When ``true``, it indicates that
  the range excludes the minimum value, i.e., :math:`x >
  \mathrm{min}`.  When ``false`` (or not included), it indicates that
  the range includes the minimum value, i.e., :math:`x \ge
  \mathrm{min}`.

- ``maximum`` specifies a maximum numeric value.

- ``exclusiveMaximum`` is a boolean.  When ``true``, it indicates that
  the range excludes the maximum value, i.e., :math:`x <
  \mathrm{max}`.  When ``false`` (or not included), it indicates that
  the range does not include the maximum value, i.e., :math:`x \le
  \mathrm{max}`.

.. schema_example::
    {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "exclusiveMaximum": true
    }
    --X
    // Less than ``minimum``:
    -1
    --
    // ``exclusiveMinimum`` was not specified, so 0 is included:
    0
    --
    10
    --
    99
    --X
    // ``exclusiveMaximum`` is ``true``, so 100 is not included:
    100
    --X
    // Greater than ``maximum``:
    101
