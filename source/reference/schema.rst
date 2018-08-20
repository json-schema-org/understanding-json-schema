.. index::
   single: $schema
   single: schema; keyword

.. _schema:

The $schema keyword
===================

The ``$schema`` keyword is used to declare that a JSON fragment is
actually a piece of JSON Schema.  It also declares which version of
the JSON Schema standard that the schema was written against.

It is recommended that all JSON Schemas have a ``$schema`` entry,
which must be at the root.  Therefore most of the time, you'll want
this at the root of your schema::

    "$schema": "http://json-schema.org/schema#"

Advanced
--------

If you need to declare that your schema was written against a specific version
of the JSON Schema standard, you should include the draft name in the path, for
example:

- ``http://json-schema.org/draft-06/schema#``
- ``http://json-schema.org/draft-04/schema#``

Additionally, if you have extended the JSON Schema language to include
your own custom keywords for validating values, you can use a custom
URI for ``$schema``.  It must not be one of the predefined values
above, and should probably include a domain name you own.
