Generic keywords
================

.. contents:: :local:

This chapter lists some miscellaneous properties that are available
for all JSON types.

.. index::
   single: annotation
   single: title
   single: description
   single: default
   single: examples

.. _annotation:

Annotations
-----------

JSON Schema includes a few keywords, ``title``, ``description``, ``default``,
``examples`` that aren't strictly used for validation, but are used to describe
parts of a schema.

None of these "annotation" keywords are required, but they are encouraged for
good practice, and can make your schema "self-documenting".

The ``title`` and ``description`` keywords must be strings. A "title" will
preferably be short, whereas a "description" will provide a more lengthy
explanation about the purpose of the data described by the schema.

The ``default`` keyword specifies a default value for an item.  JSON
processing tools may use this information to provide a default value
for a missing key/value pair, though many JSON schema validators
simply ignore the ``default`` keyword.  It should validate against the
schema in which it resides, but that isn't required.

|draft6| The ``examples`` keyword is a place to provide an array of examples
that validate against the schema. This isn't used for validation, but may help
with explaining the effect and purpose of the schema to a reader. Each entry
should validate against the schema in which is resides, but that isn't strictly
required. There is no need to duplicate the ``default`` value in the
``examples`` array, since ``default`` will be treated as another example.

.. schema_example::

    {
      "title" : "Match anything",
      "description" : "This is a schema that matches anything.",
      "default" : "Default value",
      "examples" : [
        "Anything",
        4035
      ]
    }

.. index::
   single: comment
   single: $comment

.. _comments:

Comments
--------

|draft7| ``$comment``

The ``$comment`` keyword is strictly intended for adding comments to the JSON
schema source. Its value must always be a string. Unlike the annotations
``title``, ``description`` and ``examples``, JSON schema implementations aren't
allowed to attach any meaning or behavior to it whatsoever, and may even strip
them at any time. Therefore, they are useful for leaving notes to future editors
of a JSON schema, (which is quite likely your future self), but should not be
used to communicate to users of the schema.

.. index::
   single: enum
   single: enumerated values

.. _enum:

Enumerated values
-----------------

The ``enum`` keyword is used to restrict a value to a fixed set of
values.  It must be an array with at least one element, where each
element is unique.

The following is an example for validating street light colors:

.. schema_example::

   {
     "type": "string",
     "enum": ["red", "amber", "green"]
   }
   --
   "red"
   --X
   "blue"

You can use ``enum`` even without a type, to accept values of
different types.  Let's extend the example to use ``null`` to indicate
"off", and also add 42, just for fun.

.. schema_example::

   {
     "enum": ["red", "amber", "green", null, 42]
   }
   --
   "red"
   --
   null
   --
   42
   --X
   0

However, in most cases, the elements in the ``enum`` array should also
be valid against the enclosing schema:

.. schema_example::

   {
     "type": "string",
     "enum": ["red", "amber", "green", null]
   }
   --
   "red"
   --X
   // This is in the ``enum``, but it's invalid against ``{ "type":
   // "string" }``, so it's ultimately invalid:
   null

.. index::
   single: const
   single: constant values

.. _const:

Constant values
---------------

|draft6|

The ``const`` keyword is used to restrict a value to a single value.

For example, to if you only support shipping to the United States for export reasons:

.. schema_example::

   {
     "properties": {
       "country": {
         "const": "United States of America"
       }
     }
   }
   --
   { "country": "United States of America" }
   --X
   { "country": "Canada" }

It should be noted that ``const`` is merely syntactic sugar for an ``enum`` with a single element, therefore the following are equivalent::

  { "const": "United States of America" }

  { "enum": [ "United States of America" ] }
