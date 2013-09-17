.. index::
   single: combining schemas

.. _combining:

Combining schemas
=================

JSON Schema includes a few facilities for combining schemas together.
Note that this doesn't imply schemas from multiple files or JSON trees
(though that is possible and described in `structuring`).  Combining
schemas may be as simple as allowing a value to be validated against
multiple criteria at the same time.

For example, in the following schema, the ``anyOf`` keyword is used to
say that the given value may be valid against any of the given
schemas.  The first schema requires a string with maximum
length 5. The second schema requires a number with a minimum value
of 0.  As long as a value validates against *either* of these schemas,
it is considered valid against the entire combined schema.

.. schema_example::
    {
      "anyOf": [
        { "type": "string", "maxLength": 5 },
        { "type": "number", "minimum": 0 }
      ]
    }
    --
    "short"
    --X
    "too long"
    --
    12
    --X
    -5

The keywords used to combine schemas are ``allOf``, ``anyOf`` and
``oneOf``, described individually below.

.. index::
   single: allOf

allOf
-----
