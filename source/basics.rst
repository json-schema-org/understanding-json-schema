.. _basics:

The basics
==========

.. contents:: :local:

In :ref:`about`, we described what a schema is, and hopefully
justified the need for schema languages.  Here, we proceed to
write a simple JSON Schema.

Hello, World!
-------------

When learning any new language, it's often helpful to start with the
simplest thing possible.  In JSON Schema, an empty object is a
completely valid schema that will accept any valid JSON.

.. schema_example::

   { }
   --
   // This accepts anything, as long as it's valid JSON
   42
   --
   "I'm a string"
   --
   { "an": [ "arbitrarily", "nested" ], "data": "structure" }

|draft6|

You can also use ``true`` in place of the empty object to represent a schema
that matches anything, or ``false`` for a schema that matches nothing.

.. schema_example::

   true
   --
   // This accepts anything, as long as it's valid JSON
   42
   --
   "I'm a string"
   --
   { "an": [ "arbitrarily", "nested" ], "data": "structure" }

.. schema_example::

   false
   --X
   "Resistance is futile...  This will always fail!!!"

The type keyword
----------------

Of course, we wouldn't be using JSON Schema if we wanted to just
accept any JSON document.  The most common thing to do in a JSON
Schema is to restrict to a specific type.  The ``type`` keyword is
used for that.

.. note::

    When this book refers to JSON Schema "keywords", it means the
    "key" part of the key/value pair in an object.  Most of the work
    of writing a JSON Schema involves mapping a special "keyword" to a
    value within an object.

For example, in the following, only strings are
accepted:

.. schema_example::

   { "type": "string" }
   --
   "I'm a string"
   --X
   42

The ``type`` keyword is described in more detail in `type`.

Declaring a JSON Schema
-----------------------

Since JSON Schema is itself JSON, it's not always easy to tell when
something is JSON Schema or just an arbitrary chunk of JSON.  The
``$schema`` keyword is used to declare that something is JSON Schema.
It's generally good practice to include it, though it is not required.

.. note::
    For brevity, the ``$schema`` keyword isn't included in most of the
    examples in this book, but it should always be used in the real
    world.

.. schema_example::

    { "$schema": "https://json-schema.org/draft/2019-09/schema" }

See `schema` for more information on particular JSON Schema versions and their 
``$schema`` URI.

Declaring a unique identifier
-----------------------------

It is also best practice to include an ``$id`` property as a unique
identifier for each schema.  For now, just set it to a URL at a domain
you control, for example::

   { "$id": "http://yourdomain.com/schemas/myschema.json" }

The details of `id` become more apparent when you start `structuring`.

|draft6|

.. draft_specific::

    --Draft 4
    In Draft 4, ``$id`` is just ``id`` (without the dollar-sign).
