.. index::
   single: array

.. _array:

array
-----

Arrays are used for ordered elements.  In JSON, each element in an
array may be of a different type.

.. note::
   In Python, this is analogous to a ``list`` or ``tuple`` type,
   depending on usage.  However, the ``json`` module in the Python
   standard library will always use Python lists to represent JSON
   arrays.

.. schema_example::
    { "type": "array" }
    --
    [1, 2, 3, 4, 5]
    --
    [3, "different", { "types" : "of values" }]
    --X
    {"Not": "an array"}

.. index::
   single: array; types
   single: items
   single: additionalItems

Types
-----

The types of the individual items in an array are controlled using the
``items`` and ``additionalItems`` keywords.

There are two
