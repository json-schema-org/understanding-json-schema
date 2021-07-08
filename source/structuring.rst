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
will present the tools available for reusing and structuring schemas
as well as some practical examples that use those tools.

.. index::
   single: schema identification
   single: structuring; schema identification

.. _schema-identification:

Schema Identification
---------------------

Like any other code, schemas are easier to maintain if they can be
broken down into logical units that reference each other as necessary.
In order to reference a schema, we need a way to identify a schema.
Schema documents are identified by non-relative URIs.

Schema documents are not required to have an identifier, but
you will need one if you want to reference one schema from
another. In this documentation, we will refer to schemas with no
identifier as "anonymous schemas".

In the following sections we will see how the "identifier" for a
schema is determined.

.. note::
   URI terminology can sometimes be unintuitive. In this document, the
   following definitions are used.

   - **URI** `[1]
     <https://datatracker.ietf.org/doc/html/rfc3986#section-3>`__ or
     **non-relative URI**: A full URI containing a scheme (``https``).
     It may contain a URI fragment (``#foo``). Sometimes this document
     will use "non-relative URI" to make it extra clear that relative
     URIs are not allowed.
   - **relative reference** `[2]
     <https://datatracker.ietf.org/doc/html/rfc3986#section-4.2>`__: A
     partial URI that does not contain a scheme (``https``). It may
     contain a fragment (``#foo``).
   - **URI-reference** `[3]
     <https://datatracker.ietf.org/doc/html/rfc3986#section-4.1>`__: A
     relative reference or non-relative URI. It may contain a URI
     fragment (``#foo``).
   - **absolute URI** `[4]
     <https://datatracker.ietf.org/doc/html/rfc3986#section-4.3>`__ A
     full URI containing a scheme (``https``) but not a URI fragment
     (``#foo``).

.. note::
   Even though schemas are identified by URIs, those identifiers are
   not necessarily network-addressable. They are just identifiers.
   Generally, implementations don't make HTTP requests (``https://``)
   or read from the file system (``file://``) to fetch schemas.
   Instead, they provide a way to load schemas into an internal schema
   database. When a schema is referenced by it's URI identifier, the
   schema is retrieved from the internal schema database.

.. index::
   single: JSON Pointer
   single: structuring; subschema identification; JSON Pointer

.. _json-pointer:

JSON Pointer
~~~~~~~~~~~~

In addition to identifying a schema document, you can also identify
subschemas. The most common way to do that is to use a `JSON Pointer
<https://tools.ietf.org/html/rfc6901>`__ in the URI fragment that
points to the subschema.

A JSON Pointer describes a slash-separated path to traverse the keys
in the objects in the document. Therefore,
``/properties/street_address`` means:

1) find the value of the key ``properties``
2) within that object, find the value of the key ``street_address``

The URI
``https://example.com/schemas/address#/properties/street_address``
identifies the highlighted subschema in the following schema.

.. schema_example::

    {
      "$id": "https://example.com/schemas/address",

      "type": "object",
      "properties": {
        "street_address":
      *    { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }

.. index::
   single: $anchor
   single: structuring; subschema identification; $anchor

.. _anchor:

$anchor
~~~~~~~

A less common way to identify a subschema is to create a named anchor
in the schema using the ``$anchor`` keyword and using that name in the
URI fragment. Anchors must start with a letter followed by any number
of letters, digits, ``-``, ``_``, ``:``, or ``.``.

.. draft_specific::

    --Draft 4
    In Draft 4, you declare an anchor the same way you do in Draft 6-7
    except that ``$id`` is just ``id`` (without the dollar sign).

    --Draft 6-7
    In Draft 6-7, a named anchor is defined using an ``$id`` that
    contains only a URI fragment. The value of the URI fragment is the
    name of the anchor.

    JSON Schema doesn't define how ``$id`` should be interpreted when
    it contains both fragment and non-fragment URI parts. Therefore,
    when setting a named anchor, you should not use non-fragment URI
    parts in the URI-reference.

.. note::
   If a named anchor is defined that doesn't follow these naming
   rules, then behavior is undefined. Your anchors might work in some
   implementation, but not others.

The URI ``https://example.com/schemas/address#street_address``
identifies the subschema on the highlighted part of the following
schema.

.. schema_example::

    {
      "$id": "https://example.com/schemas/address",

      "type": "object",
      "properties": {
        "street_address":
    *      {
    *        "$anchor": "#street_address",
    *        "type": "string"
    *      },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }

.. index::
   single: base URI
   single: structuring; base URI

.. _base-uri:

Base URI
--------

Using non-relative URIs can be cumbersome, so any URIs used in
JSON Schema can be URI-references that resolve against the schema's
base URI resulting in a non-relative URI. This section describes how a
schema's base URI is determined.

.. note::
   Base URI determination and relative reference resolution is defined
   by `RFC-3986
   <https://datatracker.ietf.org/doc/html/rfc3986#section-5>`__. If
   you are familiar with how this works in HTML, this section should
   feel very familiar.

.. index::
   single: retrieval URI
   single: structuring; base URI; retrieval URI

.. _retrieval-uri:

Retrieval URI
~~~~~~~~~~~~~

The URI used to fetch a schema is known as the "retrieval URI". It's
often possible to pass an anonymous schema to an implementation in
which case that schema would have no retrieval URI.

Let's assume a schema is referenced using the URI
``https://example.com/schemas/address`` and the following schema is
retrieved.

.. schema_example::

    {
      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }

The base URI for this schema is the same as the retrieval URI,
``https://example.com/schemas/address``.

.. index::
   single: $id
   single: structuring; base URI; $id

.. _id:

$id
~~~

You can set the base URI using the ``$id`` keyword. The value of
``$id`` is a URI-reference that resolves against the `retrieval-uri`.
The resulting URI is the base URI for the schema.

.. draft_specific::

    --Draft 4
    In Draft 4, ``$id`` is just ``id`` (without the dollar sign).

.. note::
   This is analogous to the ``<base>`` `tag in HTML
   <https://html.spec.whatwg.org/multipage/semantics.html#the-base-element>`__.

Let's assume the URIs ``https://example.com/schema/address`` and
``https://example.com/schema/billing-address`` both identify the
following schema.

.. schema_example::

    {
      "$id": "/schemas/address",

      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }

No matter which of the two URIs is used to retrieve this schema, the
base URI will be ``https://example.com/schemas/address``, which is the
result of the ``$id`` URI-reference resolving against the
`retrieval-uri`.

However, using a relative reference when setting a base URI can be
problematic. For example, we couldn't use this schema as an
anonymous schema because there would be no `retrieval-uri` and you
can't resolve a relative reference against nothing. For this and other
reasons, it's recommended that you always use an absolute URI when
declaring a base URI with ``$id``.

The base URI of the following schema will always be
``https://example.com/schemas/address`` no matter what the
`retrieval-uri` was or if it's used as an anonymous schema.

.. schema_example::

    {
      "$id": "https://example.com/schemas/address",

      "type": "object",
      "properties": {
        "street_address": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["street_address", "city", "state"]
    }

.. note::
   The behavior when setting a base URI that contains a URI fragment
   is undefined and should not be used because implementations may
   treat them differently.

.. index::
   single: $ref
   single: structuring; $ref

.. _ref:

$ref
----

A schema can reference another schema using the ``$ref`` keyword. The
value of ``$ref`` is a URI-reference that is resolved against the
schema's `base-uri`. When evaluating a schema, an implementation uses
the resolved identifier to retrieve the referenced schema and
evaluation is continued from the retrieved schema.

``$ref`` can be used anywhere a schema is expected. When an object
contains a ``$ref`` property, the object is considered a reference,
not a schema. Therefore, any other properties you put there will not
be treated as JSON Schema keywords and will be ignored by the
validator.

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

.. schema_example::

    {
      "$id": "https://example.com/schemas/customer",

      "type": "object",
      "properties": {
        "first_name": { "type": "string" },
        "last_name": { "type": "string" },
        "shipping_address": { "$ref": "/schemas/address" },
        "billing_address": { "$ref": "/schemas/address" }
      },
      "required": ["first_name", "last_name", "shipping_address", "billing_address"]
    }

The URI-references in ``$ref`` resolve against the schema's `base-uri`
(``https://example.com/schemas/customer``) which results in
``https://example.com/schemas/address``. The implementation retrieves
that schema and uses it to evaluate the "shipping_address" and
"billing_address" properties.

.. note::
   When using ``$ref`` in an anonymous schema, relative references may
   not be resolvable. Let's assume this example is used as an
   anonymous schema.

   .. schema_example::

       {
         "type": "object",
         "properties": {
           "first_name": { "type": "string" },
           "last_name": { "type": "string" },
           "shipping_address": { "$ref": "https://example.com/schemas/address" },
           "billing_address": { "$ref": "/schemas/address" }
         },
         "required": ["first_name", "last_name", "shipping_address", "billing_address"]
       }

   The ``$ref`` at ``/properties/shipping_address`` can resolve just
   fine without a non-relative base URI to resolve against, but the
   ``$ref`` at ``/properties/billing_address`` can't resolve to a
   non-relative URI and therefore can't can be used to retrieve the
   address schema.

.. index::
   single: $defs
   single: structuring; $defs

.. _defs:

$defs
-----

Sometimes we have small subschemas that are only intended for use in
the current schema and it doesn't make sense to define them as
separate schemas. Although we can identify any subschema using JSON
Pointers or named anchors, the ``$defs`` keyword gives us a
standardized place to keep subschemas intended for reuse in the
current schema document.

Let's extend the previous customer schema example to use a common
schema for the name properties. It doesn't make sense to define a new
schema for this and it will only be used in this schema, so it's a
good candidate for using ``$defs``.

.. schema_example::

    {
      "$id": "https://example.com/schemas/customer",

      "type": "object",
      "properties": {
        "first_name": { "$ref": "#/$defs/name" },
        "last_name": { "$ref": "#/$defs/name" },
        "shipping_address": { "$ref": "/schemas/address" },
        "billing_address": { "$ref": "/schemas/address" }
      },
      "required": ["first_name", "last_name", "shipping_address", "billing_address"],

      "$defs": {
        "name": { "type": "string" }
      }
    }

``$ref`` isn't just good for avoiding duplication. It can also be
useful for writing schemas that are easier to read and maintain.
Complex parts of the schema can be defined in ``$defs`` with
descriptive names and referenced where it's needed. This allows
readers of the schema to more quickly and easily understand the schema
at a high level before diving into the more complex parts.

.. note::
   It's possible to reference an external subschema, but generally you
   want to limit a ``$ref`` to referencing either an external schema
   or an internal subschema defined in ``$defs``.

.. index::
   single: recursion
   single: $ref
   single: structuring; recursion; $ref

.. _recursion:

Recursion
---------

The ``$ref`` keyword may be used to create recursive schemas that
refer to themselves. For example, you might have a ``person`` schema
that has an array of ``children``, each of which are also ``person``
instances.

.. schema_example::

    {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "children": {
          "type": "array",
    *      "items": { "$ref": "#" }
        }
      }
    }
    --
    // A snippet of the British royal family tree
    {
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

Above, we created a schema that refers to itself, effectively creating
a "loop" in the validator, which is both allowed and useful. Note,
however, that a ``$ref`` referring to another ``$ref`` could cause
an infinite loop in the resolver, and is explicitly disallowed.

.. schema_example::

    {
      "$defs": {
        "alice": { "$ref": "#/$defs/bob" },
        "bob": { "$ref": "#/$defs/alice" }
      }
    }

.. index::
   single: Extending Recursive Schemas
   single: $recursiveRef
   single: $recursiveAnchor
   single: structuring; Extending Recursive Schemas

.. _extending-recursive-schemas:

Extending Recursive Schemas
---------------------------

|Draft2019-09|

Documentation Coming Soon

.. index::
   single: bundling
   single: $id
   single: structuring; bundling; $id

.. _bundling:

Bundling
--------

Working with multiple schema documents is convenient for development,
but it is often more convenient for distribution to bundle all of your
schemas into a single schema document. This can be done using the
``$id`` keyword in a subschema. When ``$id`` is used in a subschema,
it creates a new `base-uri` that any references in that subschema and
any descendant subschemas will resolve against. The new `base-uri` is
the value of ``$id`` resolved against the `base-uri` of the schema it
appears in.

.. draft_specific::

    --Draft 4
    In Draft 4, ``$id`` is just ``id`` (without the dollar sign).

This example shows the customer schema example and the address schema
example bundled into a single schema document.

.. schema_example::

    {
      "$id": "https://example.com/schemas/customer",

      "type": "object",
      "properties": {
        "first_name": { "type": "string" },
        "last_name": { "type": "string" },
        "shipping_address": { "$ref": "/schemas/address" },
        "billing_address": { "$ref": "/schemas/address" }
      },
      "required": ["first_name", "last_name", "shipping_address", "billing_address"],

      "$defs": {
        "address": {
          "$id": "/schemas/address",

          "type": "object",
          "properties": {
            "street_address": { "type": "string" },
            "city": { "type": "string" },
            "state": { "$ref": "#/$defs/state" }
          },
          "required": ["street_address", "city", "state"],

          "$defs": {
            "state": { "enum": ["CA", "NY", "... etc ..."] }
          }
        }
      }
    }

Notice that the ``$ref`` keywords from the customer schema resolve the
same way they did before except that the address schema is now defined
at ``/$defs/address`` instead of a separate schema document. You
should also see that ``"$ref": "#/$defs/state"`` resolves to the
``$defs`` keyword in the address schema rather than the one at
the top level schema like it would if the embedded schema wasn't
used.

You might notice that this creates a situation where there are
multiple ways to identify a schema. Instead of referencing
``/schemas/address`` (``https://example.com/schemas/address``) You
could have used ``#/$defs/address``
(``https://example.com/schemas/customer#/$defs/address``). While
both of these will work, the one shown in the example is preferred.

.. note::
   It is unusual to use ``$id`` in a subschema when developing
   schemas. It's generally best not to use this feature explicitly and
   use schema bundling tools to construct bundled schemas if such a
   thing is needed.
