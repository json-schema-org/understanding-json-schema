.. index::
   single: combining schemas

.. _combining:

Combining schemas
=================

JSON Schema includes a few keywords for combining schemas together.
Note that this doesn't necessarily mean combining schemas from
multiple files or JSON trees, though these facilities help to enable
that and are described in `structuring`.  Combining schemas may be as
simple as allowing a value to be validated against multiple criteria
at the same time.

For example, in the following schema, the ``anyOf`` keyword is used to
say that the given value may be valid against any of the given
subschemas.  The first subschema requires a string with maximum
length 5. The second subschema requires a number with a minimum value
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

The keywords used to combine schemas are:

- `allOf`: Must be valid against *all* of the subschemas
- `anyOf`: Must be valid against *any* of the subschemas
- `oneOf`: Must be valid against *exactly one* of the subschemas

All of these keywords must be set to an array, where each item is a
schema.

In addition, there is:

- `not`: Must *not* be valid against the given schema

.. index::
   single: allOf
   single: combining schemas; allOf

.. _allOf:

allOf
-----

To validate against ``allOf``, the given data must be valid against all
of the given subschemas.

.. schema_example::

    {
      "allOf": [
        { "type": "string" },
        { "maxLength": 5 }
      ]
    }
    --
    "short"
    --X
    "too long"

Note that it's quite easy to create schemas that are logical
impossibilities with ``allOf``.  The following example creates a schema
that won't validate against anything (since something may not be both
a string and a number at the same time):

.. schema_example::

    {
      "allOf": [
        { "type": "string" },
        { "type": "number" }
      ]
    }
    --X
    "No way"
    --X
    -1

It is important to note that the schemas listed in an `allOf`, `anyOf`
or `oneOf` array know nothing of one another.  While it might be
surprising, `allOf` can not be used to "extend" a schema to add more
details to it in the sense of object-oriented inheritance.  For
example, say you had a schema for an address in a ``definitions``
section, and want to extend it to include an address type:

.. schema_example::

   {
     "definitions": {
       "address": {
         "type": "object",
         "properties": {
           "street_address": { "type": "string" },
           "city":           { "type": "string" },
           "state":          { "type": "string" }
         },
         "required": ["street_address", "city", "state"]
       }
     },

     "allOf": [
       { "$ref": "#/definitions/address" },
       { "properties": {
           "type": { "enum": [ "residential", "business" ] }
         }
       }
     ]
   }
   --
   {
      "street_address": "1600 Pennsylvania Avenue NW",
      "city": "Washington",
      "state": "DC",
      "type": "business"
   }

This works, but what if we wanted to restrict the schema so no
additional properties are allowed?  One might try adding the
highlighted line below:

.. schema_example::

   {
     "definitions": {
       "address": {
         "type": "object",
         "properties": {
           "street_address": { "type": "string" },
           "city":           { "type": "string" },
           "state":          { "type": "string" }
         },
         "required": ["street_address", "city", "state"]
       }
     },

     "allOf": [
       { "$ref": "#/definitions/address" },
       { "properties": {
           "type": { "enum": [ "residential", "business" ] }
         }
       }
     ],

     *"additionalProperties": false
   }
   --X
   {
      "street_address": "1600 Pennsylvania Avenue NW",
      "city": "Washington",
      "state": "DC",
      "type": "business"
   }

Unfortunately, now the schema will reject *everything*.  This is
because the `additionalProperties` refers to the entire schema.  And
that entire schema includes no properties, and knows nothing about the
properties in the subschemas inside of the `allOf` array.

This shortcoming is perhaps one of the biggest surprises of the
combining operations in JSON schema: it does not behave like
inheritance in an object-oriented language.  There are some proposals
to address this in the next version of the JSON schema specification.

.. index::
   single: anyOf
   single: combining schemas; anyOf

.. _anyOf:

anyOf
-----

To validate against ``anyOf``, the given data must be valid against any
(one or more) of the given subschemas.

.. schema_example::

   {
     "anyOf": [
       { "type": "string" },
       { "type": "number" }
     ]
   }
   --
   "Yes"
   --
   42
   --X
   { "Not a": "string or number" }

.. index::
   single: oneOf
   single: combining schemas; oneOf

.. _oneOf:

oneOf
-----

To validate against ``oneOf``, the given data must be valid against
exactly one of the given subschemas.

.. schema_example::

    {
      "oneOf": [
        { "type": "number", "multipleOf": 5 },
        { "type": "number", "multipleOf": 3 }
      ]
    }
    --
    10
    --
    9
    --X
    // Not a multiple of either 5 or 3.
    2
    --X
    // Multiple of *both* 5 and 3 is rejected.
    15

Note that it's possible to "factor" out the common parts of the
subschemas.  The following schema is equivalent to the one above:

.. schema_example::

   {
      "type": "number",
      "oneOf": [
        { "multipleOf": 5 },
        { "multipleOf": 3 }
      ]
    }

.. index::
   single: not
   single: combining schemas; not

.. _not:


not
---

This doesn't strictly combine schemas, but it belongs in this chapter
along with other things that help to modify the effect of schemas in
some way.  The ``not`` keyword declares that a instance validates if
it doesn't validate against the given subschema.

For example, the following schema validates against anything that is
not a string:

.. schema_example::

    { "not": { "type": "string" } }
    --
    42
    --
    { "key": "value" }
    --X
    "I am a string"
