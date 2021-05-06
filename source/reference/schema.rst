.. index::
   single: $schema

Declaring a Specification Version
=================================

.. contents:: :local:

Not only have there have been multiple versions of the specification,
but it's also possible to add your own extensions to create your own
version. JSON Schema provides ways for you to declare which version
a schema conforms to and provides ways to describe your custom
keywords.

.. index::
   single: $schema
   single: schema; keyword

.. _schema:

$schema
-------

The ``$schema`` keyword is used to declare which version of the JSON
Schema specification the schema was written for. The value of the
``$schema`` keyword is also the identifier for a schema that can be
used to verify that the schema is valid according to the specification
version ``$schema`` identifies. A schema that describes another schema
is called a "meta-schema".

``$schema`` applies to the entire document and must be at the root
level. It does not apply to externally referenced (``$ref``)
documents. Those schemas need to declare their own ``$schema``.

If ``$schema`` is not used, an implementation might allow you to
specify a value externally or it might make assumptions about which
specification version should be used to evaluate the schema. It's
recommended that all JSON Schemas have a ``$schema`` entry to
communicate to readers and tooling which specification version is
intended. Therefore most of the time, you'll want this at the root of
your schema::

    "$schema": "http://json-schema.org/draft-07/schema#"

.. draft_specific::

    --Draft-4
    The identifier for Draft 4 is ``http://json-schema.org/draft-04/schema#``.

    Draft 4 defined a value for ``$schema`` without a specific version
    (``http://json-schema.org/schema#``) which meant, use the latest
    version. This has since been deprecated and should no longer be
    used.

    You might come across references to Draft 5. There is no Draft 5
    release of JSON Schema. Draft 5 refers to a no-change revision of
    the Draft 4 release. It does not add, remove, or change any
    functionality. It only updates references, makes clarifications,
    and fixes bugs. Draft 5 describes the Draft 4 release. If you came
    here looking for information about Draft 5, you'll find it under
    Draft 4. We no longer use the "draft" terminology to refer to
    patch releases to avoid this confusion.

    --Draft-6
    The identifier for Draft 6 is ``http://json-schema.org/draft-06/schema#``.

.. index::
   single: $schema
   single: schema; custom
   single: schema; extending

Extending JSON Schema
---------------------

You can extended the JSON Schema language to include your own custom
keywords. To do this, you need to create a meta-schema that includes
your custom keywords. The best way to do this is to make a copy of the
meta-schema for the version you want to extend and make your changes
to your copy. You will need to choose a custom URI to identify your
custom version. This URI must not be one of the URIs used to identify
official JSON Schema specification drafts and should probably include
a domain name you own. You can use this URI with the ``$schema``
keyword to declare that your schemas use your custom version.

.. note::
   Not all implementations support extending JSON Schema.

One of the strengths of JSON Schema is that it can be written in JSON
and used in a variety of environments. For example, it can be used for
both front-end and back-end HTML Form validation. The problem with
adding custom keywords is that every environment where you want to use
your schemas needs to understand how to evaluate your custom keywords.
Meta-schemas can be used to ensure that schemas are written correctly,
but each implementation will need custom code to understand how to
evaluate the custom keywords.

Meta-data keywords are the most interoperable because they don't
affect validation. For example, you could add a ``units`` keyword.
This will always work as expecting with an compliant validator.

.. schema_example::

    {
      "type": "number",
      "units": "kg"
    }
    --
    42
    --X
    "42"

The next best candidates for custom keywords are keywords that don't
apply other schemas and don't modify the behavior of existing
keywords. An ``isEven`` keyword is an example. In contexts where some
validation is better than no validation such as validating an HTML
Form in the browser, this schema will perform as well as can be
expected. Full validation would still be required and should use a
validator that understands the custom keyword.

.. schema_example::

    {
      "type": "integer",
      "isEven": true
    }
    --
    2
    --
    // This passes because the validator doesn't understand ``isEven``
    3
    --X
    // The schema isn't completely impaired because it doesn't understand ``isEven``
    "3"

The least interoperable type of custom keyword is one that applies
other schemas or modifies the behavior of existing keywords. An
example would be something like ``requiredProperties`` that declares
properties and makes them required. This example shows how the schema
becomes almost completely useless when evaluated with a validator that
doesn't understand the custom keyword. That doesn't necessarily mean
that ``requiredProperties`` is a bad idea for a keyword, it's just not
the right choice if the schema might need to be used in a context that
doesn't understand custom keywords.

.. schema_example::

    {
      "type": "object",
      "requiredProperties": {
        "foo": { "type": "string" }
      }
    }
    --
    { "foo": "bar" }
    --
    // This passes because ``requiredProperties`` is not understood
    {}
    --
    // This passes because ``requiredProperties`` is not understood
    { "foo": 42 }
