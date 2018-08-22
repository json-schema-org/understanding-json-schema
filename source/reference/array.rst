.. index::
   single: array

.. _array:

array
-----

Arrays are used for ordered elements.  In JSON, each element in an
array may be of a different type.

.. language_specific::

   --Python
   In Python, "array" is analogous to a ``list`` or ``tuple`` type,
   depending on usage.  However, the ``json`` module in the Python
   standard library will always use Python lists to represent JSON
   arrays.
   --Ruby
   In Ruby, "array" is analogous to a ``Array`` type.

.. schema_example::

    { "type": "array" }
    --
    [1, 2, 3, 4, 5]
    --
    [3, "different", { "types" : "of values" }]
    --X
    {"Not": "an array"}


.. index::
   single: array; items
   single: items
   single: additionalItems

Items
'''''

By default, the elements of the array may be anything at all.
However, it's often useful to validate the items of the array against
some schema as well.  This is done using the ``items`` and
``additionalItems`` keywords.

There are two ways in which arrays are generally used in JSON:

- **List validation:** a sequence of arbitrary length where each
  item matches the same schema.

- **Tuple validation:** a sequence of fixed length where each item may
  have a different schema.  In this usage, the index (or location) of
  each item is meaningful as to how the value is interpreted.  (This
  usage is often given a whole separate type in some programming
  languages, such as Python's ``tuple``).

.. index::
   single: array; list validation

.. _list-validation:

List validation
~~~~~~~~~~~~~~~

List validation is useful for arrays of arbitrary length where each
item matches the same schema.  For this kind of array, set the
``items`` keyword to a single schema that will be used to validate all
of the items in the array.

.. note::
   When ``items`` is a single schema, the ``additionalItems`` keyword
   is meaningless, and it should not be used.

In the following example, we define that each item in an array is a
number:

.. schema_example::

   {
     "type": "array",
     "items": {
       "type": "number"
     }
   }
   --
   [1, 2, 3, 4, 5]
   --X
   // A single "non-number" causes the whole array to be invalid:
   [1, 2, "3", 4, 5]
   --
   // The empty array is always valid:
   []


.. index::
   single: array; tuple validation

.. _tuple-validation:

Tuple validation
~~~~~~~~~~~~~~~~

Tuple validation is useful when the array is a collection of items
where each has a different schema and the ordinal index of each item
is meaningful.

For example, you may represent a street address such as::

    1600 Pennsylvania Avenue NW

as a 4-tuple of the form:

    [number, street_name, street_type, direction]

Each of these fields will have a different schema:

- ``number``: The address number.  Must be a number.

- ``street_name``: The name of the street.  Must be a string.

- ``street_type``: The type of street.  Should be a string from a
  fixed set of values.

- ``direction``: The city quadrant of the address.  Should be a string
  from a different set of values.

To do this, we set the ``items`` keyword to an array, where each item
is a schema that corresponds to each index of the document's array.
That is, an array where the first element validates the first element
of the input array, the second element validates the second element of
the input array, etc.

Here's the example schema:

.. schema_example::

    {
      "type": "array",
      "items": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "string",
          "enum": ["Street", "Avenue", "Boulevard"]
        },
        {
          "type": "string",
          "enum": ["NW", "NE", "SW", "SE"]
        }
      ]
    }
    --
    [1600, "Pennsylvania", "Avenue", "NW"]
    --X
    // "Drive" is not one of the acceptable street types:
    [24, "Sussex", "Drive"]
    --X
    // This address is missing a street number
    ["Palais de l'Élysée"]
    --
    // It's okay to not provide all of the items:
    [10, "Downing", "Street"]
    --
    // And, by default, it's also okay to add additional items to end:
    [1600, "Pennsylvania", "Avenue", "NW", "Washington"]

The ``additionalItems`` keyword controls whether it's valid to have
additional items in the array beyond what is defined in ``items``.
Here, we'll reuse the example schema above, but set
``additionalItems`` to ``false``, which has the effect of disallowing
extra items in the array.

.. schema_example::

    {
      "type": "array",
      "items": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "string",
          "enum": ["Street", "Avenue", "Boulevard"]
        },
        {
          "type": "string",
          "enum": ["NW", "NE", "SW", "SE"]
        }
      ],
      "additionalItems": false
    }
    --
    [1600, "Pennsylvania", "Avenue", "NW"]
    --
    // It's ok to not provide all of the items:
    [1600, "Pennsylvania", "Avenue"]
    --X
    // But, since ``additionalItems`` is ``false``, we can't provide
    // extra items:
    [1600, "Pennsylvania", "Avenue", "NW", "Washington"]

The ``additionalItems`` keyword may also be a schema to validate against every
additional item in the array. In that case, we could say that additional items
are allowed, as long as they are all strings:

.. schema_example::

    {
      "type": "array",
      "items": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "string",
          "enum": ["Street", "Avenue", "Boulevard"]
        },
        {
          "type": "string",
          "enum": ["NW", "NE", "SW", "SE"]
        }
      ],
      "additionalItems": { "type": "string" }
    }
    --
    // Extra string items are ok...
    [1600, "Pennsylvania", "Avenue", "NW", "Washington"]
    --X
    // ..but not anything else
    [1600, "Pennsylvania", "Avenue", "NW", 20500]

.. note::

    ``additionalItems`` doesn't make sense if you're doing "list validation"
    (``items`` is an object), and is ignored in the case.

.. index::
   single: array; length
   single: minItems
   single: maxItems

Length
''''''

The length of the array can be specified using the ``minItems`` and
``maxItems`` keywords.  The value of each keyword must be a
non-negative number.  These keywords work whether doing
`list-validation` or `tuple-validation`.

.. schema_example::

   {
     "type": "array",
     "minItems": 2,
     "maxItems": 3
   }
   --X
   []
   --X
   [1]
   --
   [1, 2]
   --
   [1, 2, 3]
   --X
   [1, 2, 3, 4]


.. index::
   single: array; uniqueness
   single: uniqueItems

Uniqueness
''''''''''

A schema can ensure that each of the items in an array is unique.
Simply set the ``uniqueItems`` keyword to ``true``.

.. schema_example::

   {
     "type": "array",
     "uniqueItems": true
   }
   --
   [1, 2, 3, 4, 5]
   --X
   [1, 2, 3, 3, 4]
   --
   // The empty array always passes:
   []
