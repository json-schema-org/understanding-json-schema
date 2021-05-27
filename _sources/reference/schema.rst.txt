.. index::
   single: $schema
   single: schema; keyword

.. _schema:

The $schema keyword
===================

.. contents:: :local:

The ``$schema`` keyword is used to declare that a JSON fragment is
actually a piece of JSON Schema.  It also declares which version of
the JSON Schema standard that the schema was written against.

It is recommended that all JSON Schemas have a ``$schema`` entry,
which must be at the root.  Therefore most of the time, you'll want
this at the root of your schema::

    "$schema": "http://json-schema.org/draft/2019-09/schema#"

Advanced
--------

You should declare that your schema was written against a specific version
of the JSON Schema standard and include the draft name in the path, for
example:

- ``http://json-schema.org/draft/2019-09/schema#``
- ``http://json-schema.org/draft-07/schema#``
- ``http://json-schema.org/draft-06/schema#``
- ``http://json-schema.org/draft-04/schema#``

The possibility to declare ``$schema`` without specific version (``http://json-schema.org/schema#``) was deprecated after Draft 4 and should no longer be used.

Additionally, if you have extended the JSON Schema language to include
your own custom keywords for validating values, you can use a custom
URI for ``$schema``.  It must not be one of the predefined values
above, and should probably include a domain name you own.
