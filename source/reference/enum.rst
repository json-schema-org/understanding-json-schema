.. index::
   single: enum
   single: enumerated values

.. _enum:

Enumerated values
=================

enum
----

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
"off".

.. schema_example::
   {
     "enum": ["red", "amber", "green", null]
   }
   --
   "red"
   --
   null
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
   // This is in the ``enum``, but it's invalid against ``"type": "string"``, so
   // it's invalid:
   null
