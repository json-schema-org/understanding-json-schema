.. index::
   single: boolean

.. _boolean:

boolean
-------

The boolean type matches only two special values: ``true`` and
``false``.  Note that values that *evaluate* to ``true`` or ``false``,
such as 1 and 0, are not accepted by the schema.

.. language_specific::
   --Python
   In Python, "boolean" is analogous to ``bool``.  Note that in JSON,
   ``true`` and ``false`` are lower case, whereas in Python they are
   capitalized (``True`` and ``False``).

.. schema_example::
    { "type": "boolean" }
    --
    true
    --
    false
    --X
    "true"
    --X
    // Values that evaluate to ``true`` or ``false`` are still not
    // accepted by the schema:
    0
