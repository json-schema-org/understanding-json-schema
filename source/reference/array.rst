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

The ``unevaluatedItems`` keyword applies to any values not evaluated
by an ``items``, ``prefixItems``, or ``contains`` keyword. Just as
``unevaluatedProperties`` affects only **properties** in an object,
``unevaluatedItems`` affects only **items** in an array.

.. note::
    Watch out! The word "unevaluated" *does not* mean "not evaluated by
    ``items``, ``prefixItems``, or ``contains``." "Unevaluated" means
    "not successfully evaluated", or "doesn't evaluate to true".

For this first example, let's make a "half-closed" schema: something
useful when you want to keep the first two arguments, but also add
more in certain situations. ("Closed" to two arguments in some
places, "open" to more arguments when you need it to be.)

.. schema_example::

    {
      "$id": "https://example.com/my-tuple",

      "type": "array",
      "items": [
        true,
        { "type": "boolean" }
      ],

      "$defs": {
        "closed": {
          "$anchor": "closed",
          "$ref": "#"
        }
      }
    }

``items`` evaluates only the items in the initial array. Any items
you add when you extend the tuple later *are not evaluated*. When
you extend the tuple, the schema passes validation only if you include
``unevaluatedItems`` like this:

.. schema_example::

    {
      "$id": "https://example.com/my-extended-tuple",

      "$ref": "https://example.com/my-tuple",
      "prefixItems": [
        true,
        true,
        { "type": "boolean" }
      ],
      "unevaluatedItems": false
    }

With this, you can use ``$ref`` to reference the first two
``prefixItems`` and keep the schema "closed" to two arguments when
you need it, "open" to more arguments when you need it. A reference to
``/my-tuple#closed`` would disallow more than two items. And because
``unevaluatedItems`` only sees inside its own subschema, if you
want to add an item, add it inside that subschema.

This means you can also put ``unevaluatedItems`` in a nested tuple.

.. schema_example::

    {
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
    }
    --
    ["foo", 42]
    // All the array items are evaluated. The schema passes validation.
    --X
    ["foo", 42, null]
    // The third value is unevaluated, so ``unevaluatedItems`` is true,
    // not false. The schema fails validation.

Note these two restraints, though. First, ``items`` doesn't "see
inside" any instances of ``allOf``, ``anyOf``, or ``oneOf`` in the
same subschema. In this next example, ``items`` ignores ``allOf`` and
thus fails to validate.

.. schema_example::

    {
      "allOf": [{ "prefixItems": [{ "enum": [1, "a"] }]  }],
      "items": { "const": 2 }
    }
    --X
    [1, "a", 2]

Second, ``unevaluatedItems`` can't "see inside" cousins (vertically
adjacent properties inside a separate pair of {curly braces} with the
same "parent"— ``anyOf``, ``if``, ``not``, or similar). For instance,
in the example below, the ``unevaluatedItems`` doesn't "see inside"
the ``prefixItems`` cousin before it. All instances fail validation
because ``"prefixItems": [ true ]`` matches only length 1 arrays, and
``{ "unevaluatedItems": false }`` matches only empty arrays.

.. schema_example::

    {
      "allOf": [
        { "prefixItems": [true] },
        { "unevaluatedItems": false }
      ]
    }
    --X
    [1]

.. note::
   For a tall list of more examples, read our `unevaluatedItems Test Suite <https://github.com/json-schema-org/JSON-Schema-Test-Suite/blob/main/tests/draft2020-12/unevaluatedItems.json>`_ on GitHub. We test a lot of use cases
   there, including uncommon ones.

Here are some of our examples in the suite:
   * ``unevaluatedItems`` nested inside another ``unevaluatedItems``
   * ``if/then/else`` statements interacting with ``unevaluatedItems``
   * nested ``if/then/else`` statements interacting with ``unevaluatedItems``
   * ``unevaluatedItems`` ignoring non-arrays
   * ``unevaluatedItems`` interacting with the ``not`` keyword
   * and more

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
