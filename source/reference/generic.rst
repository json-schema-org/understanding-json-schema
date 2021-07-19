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
   single: readOnly
   single: writeOnly
   single: deprecated

.. _annotation:

Annotations
-----------

JSON Schema includes a few keywords, that aren't strictly used for
validation, but are used to describe parts of a schema. None of these
"annotation" keywords are required, but they are encouraged for good
practice, and can make your schema "self-documenting".

The ``title`` and ``description`` keywords must be strings. A "title"
will preferably be short, whereas a "description" will provide a more
lengthy explanation about the purpose of the data described by the
schema.

The ``default`` keyword specifies a default value. This value is not
used to fill in missing values during the validation process.
Non-validation tools such as documentation generators or form
generators may use this value to give hints to users about how to use
a value. However, ``default`` is typically used to express that if a
value is missing, then the value is semantically the same as if the
value was present with the default value. The value of ``default``
should validate against the schema in which it resides, but that isn't
required.

|draft6| The ``examples`` keyword is a place to provide an array of
examples that validate against the schema. This isn't used for
validation, but may help with explaining the effect and purpose of the
schema to a reader. Each entry should validate against the schema in
which it resides, but that isn't strictly required. There is no need
to duplicate the ``default`` value in the ``examples`` array, since
``default`` will be treated as another example.

|draft7| The boolean keywords ``readOnly`` and ``writeOnly`` are
typically used in an API context. ``readOnly`` indicates that a value
should not be modified. It could be used to indicate that a ``PUT``
request that changes a value would result in a ``400 Bad Request``
response. ``writeOnly`` indicates that a value may be set, but will
remain hidden. In could be used to indicate you can set a value with a
``PUT`` request, but it would not be included when retrieving that
record with a ``GET`` request.

|draft2019-09| The ``deprecated`` keyword is a boolean that indicates
that the instance value the keyword applies to should not be used and
may be removed in the future.

.. schema_example::

    {
      "title": "Match anything",
      "description": "This is a schema that matches anything.",
      "default": "Default value",
      "examples": [
        "Anything",
        4035
      ],
      "deprecated": true,
      "readOnly": true,
      "writeOnly": false
    }

.. index::
   single: comment
   single: $comment

.. _comments:

Comments
--------

|draft7| ``$comment``

The ``$comment`` keyword is strictly intended for adding comments to
a schema. Its value must always be a string. Unlike the annotations
``title``, ``description``, and ``examples``, JSON schema
implementations aren't allowed to attach any meaning or behavior to it
whatsoever, and may even strip them at any time. Therefore, they are
useful for leaving notes to future editors of a JSON schema, but
should not be used to communicate to users of the schema.

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

.. index::
   single: const
   single: constant values

.. _const:

Constant values
---------------

|draft6|

The ``const`` keyword is used to restrict a value to a single value.

For example, if you only support shipping to the United States for
export reasons:

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
