.. index::
   single: structure

.. _structuring:

Structuring a complex schema
============================

.. contents:: :local:

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
everywhere we want to store an address.  Not only would that make the
schema more verbose, but it makes updating it in the future more
difficult.  If our imaginary company were to start doing international
business in the future and we wanted to add a country field to all the
addresses, it would be better to do this in a single place rather than
everywhere that addresses are used.

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

This can be used anywhere a schema is expected. You will always use ``$ref`` as
the only key in an object: any other keys you put there will be ignored by the
validator.

The value of ``$ref`` is a URI-reference, and the part after ``#`` sign (the
"fragment" or "named anchor") is in a format called `JSON Pointer
<https://tools.ietf.org/html/rfc6901>`__.

.. note::
    JSON Pointer aims to serve the same purpose as `XPath
    <http://www.w3.org/TR/xpath/>`_ from the XML world, but it is much
    simpler.

If you're using a definition from the same document, the ``$ref`` value begins
with the pound symbol (``#``). Following that, the slash-separated items traverse
the keys in the objects in the document. Therefore, in our example
``"#/definitions/address"`` means:

1) go to the root of the document
2) find the value of the key ``"definitions"``
3) within that object, find the value of the key ``"address"``

``$ref`` can resolve to a URI that references another file, so if you prefer to
include your definitions in separate files, you can also do that.  For
example::

    { "$ref": "definitions.json#/address" }

would load the address schema from another file residing alongside
this one.

Now let's put this together and use our address schema to create a
schema for a customer:

.. schema_example::

    {
      "$schema": "http://json-schema.org/draft-07/schema#",

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

.. note::

    Even though the value of a ``$ref`` is a URI-reference, it is not a network
    locator, only an identifier. This means that the schema doesn't need to be
    accessible at the resolved URI, but it may be. It is basically up to the
    validator implementation how external schema URIs will be handled, but one
    should not assume the validator will fetch network resources indicated in
    ``$ref`` values.

Recursion
`````````

``$ref`` elements may be used to create recursive schemas that refer to themselves.
For example, you might have a ``person`` schema that has an array of ``children``, each of which are also ``person`` instances.

.. schema_example::

    {
      "$schema": "http://json-schema.org/draft-07/schema#",

      "definitions": {
        "person": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "children": {
              "type": "array",
    *          "items": { "$ref": "#/definitions/person" },
              "default": []
            }
          }
        }
      },

      "type": "object",

      "properties": {
        "person": { "$ref": "#/definitions/person" }
      }
    }
    --
    // A snippet of the British royal family tree
    {
      "person": {
        "name": "Elizabeth",
        "children": [
          {
            "name": "Charles",
            "children": [
              {
                "name": "William",
                "children": [
                  { "name": "George" },
                  { "name": "Charlotte" }
                ]
              },
              {
                "name": "Harry"
              }
            ]
          }
        ]
      }
    }

Above, we created a schema that refers to another part of itself, effectively
creating a "loop" in the validator, which is both allowed and useful. Note,
however, that a loop of ``$ref`` schemas referring to one another could cause an
infinite loop in the resolver, and is explicitly disallowed.

.. schema_example::

    {
      "definitions": {
        "alice": {
          "anyOf": [
            { "$ref": "#/definitions/bob" }
          ]
        },
        "bob": {
          "anyOf": [
            { "$ref": "#/definitions/alice" }
          ]
        }
      }
    }

.. index::
    single: $id

.. _id:

The $id property
----------------

The ``$id`` property is a URI-reference that serves two purposes:

- It declares a unique identifier for the schema.

- It declares a base URI against which ``$ref`` URI-references are resolved.

It is best practice that every top-level schema should set ``$id`` to an
absolute-URI (not a relative reference), with a domain that you control. For
example, if you own the ``foo.bar`` domain, and you had a schema for addresses,
you may set its ``$id`` as follows:

.. schema_example::

  { "$id": "http://foo.bar/schemas/address.json" }

This provides a unique identifier for the schema, as well as, in most
cases, indicating where it may be downloaded.

But be aware of the second purpose of the ``$id`` property: that it
declares a base URI for ``$ref`` URI-references elsewhere in the file.
For example, if you had:

.. schema_example::

  { "$ref": "person.json" }

in the same file, a JSON schema validation library that supported network
fetching may fetch ``person.json`` from
``http://foo.bar/schemas/person.json``, even if ``address.json`` was loaded from
somewhere else, such as the local filesystem. The drafts do not define this
area of behaviour very clearly, and validator implementations may vary in
exactly how they try to locate the referenced schema.


|draft6|

.. draft_specific::

    --Draft 4
    In Draft 4, ``$id`` is just ``id`` (without the dollar sign).

The ``$id`` property should never be the empty string or an empty fragment
(``#``), since that doesn't really make sense.

Using $id with $ref
```````````````````

``$id`` also provides a way to refer to subschema without using JSON Pointer.
This means you can refer to them by a unique name, rather than by where they
appear in the JSON tree.

Reusing the address example above, we can add an ``$id`` property to the
address schema, and refer to it by that instead.

.. schema_example::

    {
      "$schema": "http://json-schema.org/draft-07/schema#",

      "definitions": {
        "address": {
          *"$id": "#address",
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
        *"billing_address": { "$ref": "#address" },
        *"shipping_address": { "$ref": "#address" }
      }
    }

.. note::

    This functionality isn't currently supported by the Python ``jsonschema``
    library.

Extending
---------

The power of ``$ref`` really shines when it is used with the
combining keywords ``allOf``, ``anyOf`` and ``oneOf`` (see
:ref:`combining`).

Let's say that for a shipping address, we want to know whether the
address is a residential or business address, because the shipping
method used may depend on that.  For a billing address, we don't
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
      "$schema": "http://json-schema.org/draft-06/schema#",

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
