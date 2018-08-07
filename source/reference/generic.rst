Generic keywords
================

This chapter lists some miscellaneous properties that are available
for all JSON types.

.. index::
   single: metadata
   single: title
   single: description

.. _metadata:

Metadata
--------

JSON Schema includes a few keywords, ``title``, ``description`` and
``default``, that aren't strictly used for validation, but are used to
describe parts of a schema.

The ``title`` and ``description`` keywords must be strings.  A "title"
will preferably be short, whereas a "description" will provide a more
lengthy explanation about the purpose of the data described by the
schema.  Neither are required, but they are encouraged for good
practice.

The ``default`` keyword specifies a default value for an item.  JSON
processing tools may use this information to provide a default value
for a missing key/value pair, though many JSON schema validators
simply ignore the ``default`` keyword.  It should validate against the
schema in which it resides, but that isn't required.

.. schema_example::

    {
      "title" : "Match anything",
      "description" : "This is a schema that matches anything.",
      "default" : "Default value"
    }

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
