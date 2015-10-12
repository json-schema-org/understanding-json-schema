.. index::
   single: structure

.. _structuring:

Structuring a complex schema
============================

When writing computer programs of even moderate complexity, it's
commonly accepted that "structuring" the program into reusable
functions is better than copying-and-pasting duplicate bits of code
everywhere they are used.  Likewise in JSON Schema, for anything but
the most trivial schema, it's really useful to structure the schema
into parts that can be reused in a number of places.  This chapter
will present some practical examples that use the tools available for
reusing and structuring schemas.

Reuse
-----

For this example, let's say we want to define a customer record, where
each customer may have both a shipping and a billing address.
Addresses are always the same---they have a street address, city and
state---so we don't want to duplicate that part of the schema
everywhere we want to store an address.  Not only does it make the
schema more verbose, but it makes updating it in the future more
difficult.  If our imaginary company were to start international
business in the future and we wanted to add a country field to all the
addresses, it would be better to do this in a single place rather than
everywhere that addresses are used.

.. note::
    This is part of the draft 4 spec only, and does not exist in draft 3.

So let's start with the schema that defines an address::

    {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city":           { "type": "string" },
        "state":          { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }

Since we are going to reuse this schema, it is customary (but not
required) to put it in the parent schema under a key called
``definitions``::

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
      }
    }

.. index::
    single: $ref

We can then refer to this schema snippet from elsewhere using the
``$ref`` keyword.  The easiest way to describe ``$ref`` is that it
gets logically replaced with the thing that it points to.  So, to
refer to the above, we would include::

    { "$ref": "#/definitions/address" }

The value of ``$ref`` is a string in a format called `JSON Pointer
<https://tools.ietf.org/html/rfc6901>`__.

.. note::
    JSON Pointer aims to serve the same purpose as `XPath
    <http://www.w3.org/TR/xpath/>`_ from the XML world, but it is much
    simpler.

The pound symbol (``#``) refers to the current document, and then the
slash (``/``) separated keys thereafter just traverse the keys in the
objects in the document.  Therefore, in our example
``"#/definitions/address"`` means:

1) go to the root of the document
2) find the value of the key ``"definitions"``
3) within that object, find the value of the key ``"address"``

``$ref`` can also be a relative or absolute URI, so if you prefer to
include your definitions in separate files, you can also do that.  For
example::

    { "$ref": "definitions.json#/address" }

would load the address schema from another file residing alongside
this one.

Now let's put this together and use our address schema to create a
schema for a customer:

.. schema_example::

    {
      "$schema": "http://json-schema.org/draft-04/schema#",

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

      "type": "object",

      "properties": {
        "billing_address": { "$ref": "#/definitions/address" },
        "shipping_address": { "$ref": "#/definitions/address" }
      }
    }
    --
    {
      "shipping_address": {
        "street_address": "1600 Pennsylvania Avenue NW",
        "city": "Washington",
        "state": "DC"
      },
      "billing_address": {
        "street_address": "1st Street SE",
        "city": "Washington",
        "state": "DC"
      }
    }

.. _id:

The id property
---------------

The ``id`` property serves two purposes:

- It declares a unique identifier for the schema.

- It declares a base URL against which ``$ref`` URLs are resolved.

It is best practice that ``id`` is a URL, preferably in a domain that
you control.  For example, if you own the ``foo.bar`` domain, and you
had a schema for addresses, you may set its ``id`` as follows::

  "id": "http://foo.bar/schemas/address.json"

This provides a unique identifier for the schema, as well as, in most
cases, indicating where it may be downloaded.

But be aware of the second purpose of the ``id`` property: that it
declares a base URL for relative ``$ref`` URLs elsewhere in the file.
For example, if you had::

  { "$ref": "person.json" }

in the same file, a JSON schema validation library would fetch
``person.json`` from ``http://foo.bar/schemas/person.json``, even if
``address.json`` was loaded from the local filesystem.

Extending
---------

The power of ``$ref`` really shines when it is combined with the
combining keywords ``allOf``, ``anyOf`` and ``oneOf`` (see
:ref:`combining`).

Let's say that for shipping address, we want to know whether the
address is a residential or business address, because the shipping
method used may depend on that.  For the billing address, we don't
want to store that information, because it's not applicable.

To handle this, we'll update our definition of shipping address::

    "shipping_address": { "$ref": "#/definitions/address" }

to instead use an ``allOf`` keyword entry combining both the core
address schema definition and an extra schema snippet for the address
type::

    "shipping_address": {
      "allOf": [
        // Here, we include our "core" address schema...
        { "$ref": "#/definitions/address" },

        // ...and then extend it with stuff specific to a shipping
        // address
        { "properties": {
            "type": { "enum": [ "residential", "business" ] }
          },
          "required": ["type"]
        }
      ]
    }

Tying this all together,

.. schema_example::

    {
      "$schema": "http://json-schema.org/draft-04/schema#",

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

      "type": "object",

      "properties": {
        "billing_address": { "$ref": "#/definitions/address" },
        "shipping_address": {
          "allOf": [
            { "$ref": "#/definitions/address" },
            { "properties":
              { "type": { "enum": [ "residential", "business" ] } },
              "required": ["type"]
            }
          ]
        }
      }
    }
    --X
    // This fails, because it's missing an address type:
    {
      "shipping_address": {
        "street_address": "1600 Pennsylvania Avenue NW",
        "city": "Washington",
        "state": "DC"
      }
    }
    --
    {
      "shipping_address": {
        "street_address": "1600 Pennsylvania Avenue NW",
        "city": "Washington",
        "state": "DC",
        "type": "business"
      }
    }

From these basic pieces, it's possible to build very powerful
constructions without a lot of duplication.
