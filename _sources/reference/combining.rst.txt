.. index::
   single: schema composition

.. _combining:

Schema Composition
==================

.. contents:: :local:

JSON Schema includes a few keywords for combining schemas together.
Note that this doesn't necessarily mean combining schemas from
multiple files or JSON trees, though these facilities help to enable
that and are described in `structuring`.  Combining schemas may be as
simple as allowing a value to be validated against multiple criteria
at the same time.

These keywords correspond to well known boolean algebra concepts like
AND, OR, XOR, and NOT. You can often use these keywords to express
complex constraints that can't otherwise be expressed with standard
JSON Schema keywords.

The keywords used to combine schemas are:

- `allOf`: (AND) Must be valid against *all* of the subschemas
- `anyOf`: (OR) Must be valid against *any* of the subschemas
- `oneOf`: (XOR) Must be valid against *exactly one* of the subschemas

All of these keywords must be set to an array, where each item is a
schema.

In addition, there is:

- `not`: (NOT) Must *not* be valid against the given schema

.. index::
   single: allOf
   single: schema composition; allOf

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

.. note::
   `allOf` can not be used to "extend" a schema to add more details to
   it in the sense of object-oriented inheritance. Instances must
   independently be valid against "all of" the schemas in the
   ``allOf``. See the section on `subschemaindependence` for more
   information.

.. index::
   single: anyOf
   single: schema composition; anyOf

.. _anyOf:

anyOf
-----

To validate against ``anyOf``, the given data must be valid against any
(one or more) of the given subschemas.

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

.. index::
   single: oneOf
   single: schema composition; oneOf

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

.. index::
   single: not
   single: schema composition; not

.. _not:

not
---

The ``not`` keyword declares that an instance validates if it doesn't
validate against the given subschema.

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

.. index::
   single: not
   single: schema composition; subschema independence

.. _composition:

Properties of Schema Composition
--------------------------------

.. _subschemaindependence:

Subschema Independence
''''''''''''''''''''''

It is important to note that the schemas listed in an `allOf`, `anyOf`
or `oneOf` array know nothing of one another. For example, say you had
a schema for an address in a ``$defs`` section, and want to
"extend" it to include an address type:

.. schema_example::

   {
     "$defs": {
       "address": {
         "type": "object",
         "properties": {
           "street_address": { "type": "string" },
           "city": { "type": "string" },
           "state": { "type": "string" }
         },
         "required": ["street_address", "city", "state"]
       }
     },

     "allOf": [
       { "$ref": "#/$defs/address" },
       {
         "properties": {
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
     "$defs": {
       "address": {
         "type": "object",
         "properties": {
           "street_address": { "type": "string" },
           "city": { "type": "string" },
           "state": { "type": "string" }
         },
         "required": ["street_address", "city", "state"]
       }
     },

     "allOf": [
       { "$ref": "#/$defs/address" },
       {
         "properties": {
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
because ``additionalProperties`` knows nothing about the properties
declared in the subschemas inside of the `allOf` array.

To many, this is one of the biggest surprises of the combining
operations in JSON schema: it does not behave like inheritance in an
object-oriented language. There are some proposals to address this in
the next version of the JSON schema specification.

.. _illogicalschemas:

Illogical Schemas
'''''''''''''''''

Note that it's quite easy to create schemas that are logical
impossibilities with these keywords. The following example creates a
schema that won't validate against anything (since something may not
be both a string and a number at the same time):

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

.. _factoringschemas:

Factoring Schemas
'''''''''''''''''

Note that it's possible to "factor" out the common parts of the
subschemas.  The following two schemas are equivalent.

.. schema_example::

    {
      "oneOf": [
        { "type": "number", "multipleOf": 5 },
        { "type": "number", "multipleOf": 3 }
      ]
    }

.. schema_example::

   {
      "type": "number",
      "oneOf": [
        { "multipleOf": 5 },
        { "multipleOf": 3 }
      ]
    }
