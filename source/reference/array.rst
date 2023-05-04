.. index::
   single: array

.. _array:

array
-----

.. contents:: :local:

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

There are two ways in which arrays are generally used in JSON:

- **List validation:** a sequence of arbitrary length where each
  item matches the same schema.

- **Tuple validation:** a sequence of fixed length where each item may
  have a different schema.  In this usage, the index (or location) of
  each item is meaningful as to how the value is interpreted.  (This
  usage is often given a whole separate type in some programming
  languages, such as Python's ``tuple``).

.. index::
   single: array; items
   single: items

.. _items:

Items
'''''

List validation is useful for arrays of arbitrary length where each
item matches the same schema.  For this kind of array, set the
``items`` keyword to a single schema that will be used to validate all
of the items in the array.

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
''''''''''''''''

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

To do this, we use the ``prefixItems`` keyword. ``prefixItems`` is an
array, where each item is a schema that corresponds to each index of
the document's array. That is, an array where the first element
validates the first element of the input array, the second element
validates the second element of the input array, etc.

.. draft_specific::
   --Draft 4 - 2019-09
   In Draft 4 - 2019-09, tuple validation was handled by an alternate
   form of the ``items`` keyword. When ``items`` was an array of
   schemas instead of a single schema, it behaved the way
   ``prefixItems`` behaves.

Here's the example schema:

.. schema_example::

    {
      "type": "array",
      "prefixItems": [
        { "type": "number" },
        { "type": "string" },
        { "enum": ["Street", "Avenue", "Boulevard"] },
        { "enum": ["NW", "NE", "SW", "SE"] }
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

.. index::
   single: array; tuple validation; items
   single: items

.. _additionalitems:

Additional Items
~~~~~~~~~~~~~~~~

The ``items`` keyword can be used to control whether it's valid to
have additional items in a tuple beyond what is defined in
``prefixItems``. The value of the ``items`` keyword is a schema that
all additional items must pass in order for the keyword to validate.

.. draft_specific::

   --Draft 4 - 2019-09
   Before to Draft 2020-12, you would use the ``additionalItems``
   keyword to constrain additional items on a tuple. It works the same
   as ``items``, only the name has changed.

   --Draft 6 - 2019-09
   In Draft 6 - 2019-09, the ``additionalItems`` keyword is ignored if
   there is not a "tuple validation" ``items`` keyword present in the
   same schema.

Here, we'll reuse the example schema above, but set
``items`` to ``false``, which has the effect of disallowing
extra items in the tuple.

.. schema_example::

    {
      "type": "array",
      "prefixItems": [
        { "type": "number" },
        { "type": "string" },
        { "enum": ["Street", "Avenue", "Boulevard"] },
        { "enum": ["NW", "NE", "SW", "SE"] }
      ],
      "items": false
    }
    --
    [1600, "Pennsylvania", "Avenue", "NW"]
    --
    // It's ok to not provide all of the items:
    [1600, "Pennsylvania", "Avenue"]
    --X
    // But, since ``items`` is ``false``, we can't provide
    // extra items:
    [1600, "Pennsylvania", "Avenue", "NW", "Washington"]

You can express more complex constraints by using a non-boolean schema
to constrain what value additional items can have. In that case, we
could say that additional items are allowed, as long as they are all
strings:

.. schema_example::

    {
      "type": "array",
      "prefixItems": [
        { "type": "number" },
        { "type": "string" },
        { "enum": ["Street", "Avenue", "Boulevard"] },
        { "enum": ["NW", "NE", "SW", "SE"] }
      ],
      "items": { "type": "string" }
    }
    --
    // Extra string items are ok ...
    [1600, "Pennsylvania", "Avenue", "NW", "Washington"]
    --X
    // ... but not anything else
    [1600, "Pennsylvania", "Avenue", "NW", 20500]

.. index::
   single: array; tuple validation; unevaluatedItems
   single: unevaluatedItems

.. _unevaluateditems:

Unevaluated Items
'''''''''''''''''

|draft2019-09|

The ``unevaluatedItems`` keyword selects any data types not evaluated
by an ``items``, ``prefixItems``, or `contains` keyword. Just as
unevaluated"properties" affect only "properties" in an object, only
"item"-related keywords affect unevaluated"items".

It also applies inside valid subschemas with these keywords:
- ``allOf``
- ``anyOf``
- ``oneOf``
- ``not``
- ``if``
- ``then``
- ``else``

The main reason to use this keyword is to extend an array with extra
arguments.

For this first example, we'll use ``unevaluatedItems`` to select any
unexpected strings.

.. schema_example::

    {
        "items": {"type": "number"},
        "unevaluatedItems": {"type": "string"}
    }
    --X
    // If any strings appear, then the schema doesn't validate. There are no unevaluated items in that case.
    { 99, "waffles" }
    --
    // But it passes so long as JSON finds all entries in an ``items``, ``prefixItems``, or ``contains``. There *are* unevaluated items in that case.
    { 99, 0, 3.14159 }

.. note::
Watch out! The word "unevaluated" *does not* mean "not evaluated by
``items``, ``prefixItems``, or ``contains``." "Unevaluated" means
"not successfully evaluated", or "doesn't evaluate to true".

You can also set ``unevaluatedItems`` as a boolean.

.. schema_example::

    {
        "description": "unevaluatedItems with nested tuple",
        "schema": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "prefixItems": [
                { "type": "string" }
            ],
            "allOf": [
                {
                    "prefixItems": [
                      true,
                      { "type": "number" }
                    ]
                }
            ],
            "unevaluatedItems": false
        },
        "tests": [
            {
                "description": "with no unevaluated items",
                "data": ["foo", 42],
                "valid": true
            },
            {
                "description": "with unevaluated items",
                "data": ["foo", 42, null],
                "valid": false
            }
        ]
    }

In the first test, all the "data" items are evaluated, but in the
second test, the ``null`` value is a type not specified by
``prefixItems``. It's therefore valid and ``true`` that
``unevaluatedItems`` returns ``false`` in the first test, and invalid
and ``false`` in the second test. In other words, it is valid that no
unevaluated items exist until something not matching the string/number
pattern shows up.

You can also select ``unevaluatedItems`` when and only when an ``if``
statement runs.

.. schema_example::

    {
            "description": "unevaluatedItems can see annotations from if even without then and else",
            "schema": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "if": {
                    "prefixItems": [{"const": "a"}]
                },
                "unevaluatedItems": false
            },
            "tests": [
                {
                    "description": "valid in case if is evaluated",
                    "data": [ "a" ],
                    "valid": true
                },
                {
                    "description": "invalid in case if is evaluated",
                    "data": [ "b" ],
                    "valid": false
                }
            ]
    }

And an important note: ``unevaluatedItems`` can't see inside cousins
(a vertically adjacent item inside a separate pair of {curly braces}
with the same "parent"— ``anyOf``, ``if``, ``not``, or similar). Such
an instance always fails evaluation.

.. schema_example::

    {
        "description": "unevaluatedItems can't see inside cousins",
        "schema": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "allOf": [
                {
                  "prefixItems": [ true ]
                },
                { "unevaluatedItems": false }
            ]
        },
        "tests": [
            {
                "description": "always fails",
                "data": [ 1 ],
                "valid": false
            }
        ]
    }

Finally, here's an example of ``unevaluatedItems`` if you're
`structuring`. Let's make a "half-closed" schema: something useful
when you want to keep the first two arguments, but also add more in
certain situations. ("Closed" to two in some places, "open" to more
in others.)

.. schema_example::

    {
      "$id": "https://example.com/my-tuple",

      "type": "array",
      "prefixItems": [
        true,
        { "type": "boolean" }
      ],

      "$defs": {
        "closed": {
          "$anchor": "closed",
          "$ref": "#",
          "unevaluatedItems": false
        }
      }
    }

Then we can extend the tuple:

.. schema_example::

    {
      "$id": "https://example.com/my-extended-tuple",

      "$ref": "/my-tuple",
      "prefixItems": [
        true,
        true,
        { "type": "boolean" }
      ],
      "unevaluatedItems": false
    }

With this, you can use ``$ref`` to reference the first two
``prefixItems`` and keep the schema "closed" to two when necessary,
"open" to more when necessary. A reference to ``/my-tuple#closed``
would disallow more than two items, when you need it to.

.. note::
   For a tower of more examples, read our `unevaluatedItems Test Suite <https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/main/tests/draft2020-12/unevaluatedItems.json>`_ on GitHub.
   We test a lot of use cases there, including uncommon ones. Do any
   of these apply to your schema?
   - using ``unevaluatedItems`` as a schema
   - ``unevaluatedItems`` nested inside another ``unevaluatedItems``
   - ``if/then/else`` statements with ``unevaluatedItems``
   - multiples nested ``if``/``then``s
   - multiple nested instances of ``contains``
   - ignoring non-array types
   - ``not``

.. index::
   single: array; contains
   single: contains

.. _contains:

Contains
''''''''

|draft6|

While the ``items`` schema must be valid for every item in the array,
the ``contains`` schema only needs to validate against one or more
items in the array.

.. schema_example::

   {
      "type": "array",
      "contains": {
        "type": "number"
      }
   }
   --
   // A single "number" is enough to make this pass:
   ["life", "universe", "everything", 42]
   --X
   // But if we have no number, it fails:
   ["life", "universe", "everything", "forty-two"]
   --
   // All numbers is, of course, also okay:
   [1, 2, 3, 4, 5]

minContains / maxContains
~~~~~~~~~~~~~~~~~~~~~~~~~

|draft2019-09|

``minContains`` and ``maxContains`` can be used with ``contains`` to
further specify how many times a schema matches a ``contains``
constraint. These keywords can be any non-negative number including
zero.

.. schema_example::

   {
     "type": "array",
     "contains": {
       "type": "number"
     },
     "minContains": 2,
     "maxContains": 3
   }
   --X
   // Fails ``minContains``
   ["apple", "orange", 2]
   --
   ["apple", "orange", 2, 4]
   --
   ["apple", "orange", 2, 4, 8]
   --X
   // Fails ``maxContains``
   ["apple", "orange", 2, 4, 8, 16]

.. index::
   single: array; length
   single: minItems
   single: maxItems

.. _length:

Length
''''''

The length of the array can be specified using the ``minItems`` and
``maxItems`` keywords.  The value of each keyword must be a
non-negative number.  These keywords work whether doing
`list validation <items>` or `tuple-validation`.

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

.. _uniqueItems:

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
