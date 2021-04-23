.. index::
   single: integer
   single: number
   single: types; numeric

.. _numeric:

Numeric types
-------------

.. contents:: :local:

There are two numeric types in JSON Schema: `integer` and `number`.  They
share the same validation keywords.

.. note::

    JSON has no standard way to represent complex numbers, so there is
    no way to test for them in JSON Schema.

.. _integer:


integer
'''''''

The ``integer`` type is used for integral numbers. JSON does not have
distinct types for integers and floating-point values. Therefore, the
presence or absence of a decimal point is not enough to distinguish
between integers and non-integers. For example, ``1`` and ``1.0`` are
two ways to represent the same value in JSON. JSON Schema considers
that value an integer no matter which representation was used.

.. language_specific::

    --Python
    In Python, "integer" is analogous to the ``int`` type.
    --Ruby
    In Ruby, "integer" is analogous to the ``Integer`` type.

.. schema_example::

    { "type": "integer" }
    --
    42
    --
    -1
    --
    // Numbers with a zero fractional part are considered integers
    1.0
    --X
    // Floating point numbers are rejected:
    3.1415926
    --X
    // Numbers as strings are rejected:
    "42"

.. _number:

number
''''''

The ``number`` type is used for any numeric type, either integers or
floating point numbers.

.. language_specific::

    --Python
    In Python, "number" is analogous to the ``float`` type.
    --Ruby
    In Ruby, "number" is analogous to the ``Float`` type.

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

.. _multiples:

Multiples
'''''''''

Numbers can be restricted to a multiple of a given number, using the
``multipleOf`` keyword.  It may be set to any positive number.

.. schema_example::

    {
        "type": "number",
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
``minimum`` and ``maximum`` keywords, (or ``exclusiveMinimum`` and
``exclusiveMaximum`` for expressing exclusive range).

If *x* is the value being validated, the following must hold true:

  - *x* ≥ ``minimum``
  - *x* > ``exclusiveMinimum``
  - *x* ≤ ``maximum``
  - *x* < ``exclusiveMaximum``

While you can specify both of ``minimum`` and ``exclusiveMinimum`` or both of
``maximum`` and ``exclusiveMaximum``, it doesn't really make sense to do so.

.. schema_example::

    {
      "type": "number",
      "minimum": 0,
      "exclusiveMaximum": 100
    }
    --X
    // Less than ``minimum``:
    -1
    --
    // ``minimum`` is inclusive, so 0 is valid:
    0
    --
    10
    --
    99
    --X
    // ``exclusiveMaximum`` is exclusive, so 100 is not valid:
    100
    --X
    // Greater than ``maximum``:
    101

.. draft_specific::

    --Draft 4
    In JSON Schema Draft 4, ``exclusiveMinimum`` and ``exclusiveMaximum`` work
    differently. There they are boolean values, that indicate whether
    ``minimum`` and ``maximum`` are exclusive of the value. For example:

    - if ``exclusiveMinimum`` is ``false``, *x* ≥ ``minimum``.
    - if ``exclusiveMinimum`` is ``true``, *x* > ``minimum``.

    This was changed to have better keyword independence.

    Here is an example using the older Draft 4 convention:

    .. schema_example:: 4

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
