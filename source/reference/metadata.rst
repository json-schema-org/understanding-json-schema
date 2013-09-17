.. index::
   single: metadata
   single: title
   single: description

.. _metadata:

Metadata
========

JSON Schema includes a couple keywords, ``title`` and ``description``,
that aren't strictly used for validation, but are used to describe
parts of a schema.  Both values must be strings.  A title will
preferrably be short, whereas a description will provide explanation
about the purpose of data described by the schema.  Neither are
required, but they are encouraged for good practice.

.. schema_example::
    {
      "title" : "Match anything",
      "description" : "This is a schema that matches anything."
    }
