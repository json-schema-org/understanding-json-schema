.. index::
   single: object

.. _object:

object
------

.. contents:: :local:

Objects are the mapping type in JSON.  They map "keys" to "values".
In JSON, the "keys" must always be strings.  Each of these pairs is
conventionally referred to as a "property".

.. language_specific::
   --Python
   In Python, "objects" are analogous to the ``dict`` type.  An
   important difference, however, is that while Python dictionaries
   may use anything hashable as a key, in JSON all the keys
   must be strings.

   Try not to be confused by the two uses of the word "object" here:
   Python uses the word ``object`` to mean the generic base class for
   everything, whereas in JSON it is used only to mean a mapping from
   string keys to values.

   --Ruby
   In Ruby, "objects" are analogous to the ``Hash`` type. An important
   difference, however, is that all keys in JSON must be strings, and therefore
   any non-string keys are converted over to their string representation.

   Try not to be confused by the two uses of the word "object" here:
   Ruby uses the word ``Object`` to mean the generic base class for
   everything, whereas in JSON it is used only to mean a mapping from
   string keys to values.


.. schema_example::

    { "type": "object" }
    --
    {
       "key": "value",
       "another_key": "another_value"
    }
    --
    {
        "Sun": 1.9891e30,
        "Jupiter": 1.8986e27,
        "Saturn": 5.6846e26,
        "Neptune": 10.243e25,
        "Uranus": 8.6810e25,
        "Earth": 5.9736e24,
        "Venus": 4.8685e24,
        "Mars": 6.4185e23,
        "Mercury": 3.3022e23,
        "Moon": 7.349e22,
        "Pluto": 1.25e22
    }
    --X
    // Using non-strings as keys is invalid JSON:
    {
        0.01: "cm",
        1: "m",
        1000: "km"
    }
    --X
    "Not an object"
    --X
    ["An", "array", "not", "an", "object"]


.. index::
   single: object; properties
   single: properties

.. _properties:

Properties
''''''''''

The properties (key-value pairs) on an object are defined using the
``properties`` keyword.  The value of ``properties`` is an object,
where each key is the name of a property and each value is a schema
used to validate that property. Any property that doesn't match any of
the property names in the ``properties`` keyword is ignored by this
keyword.

.. note::
   See `additionalproperties` and `unevaluatedproperties` for how to
   disallow properties that don't match any of the property names in
   ``properties``.

For example, let's say we want to define a simple schema for an
address made up of a number, street name and street type:

.. schema_example::

    {
      "type": "object",
      "properties": {
        "number": { "type": "number" },
        "street_name": { "type": "string" },
        "street_type": { "enum": ["Street", "Avenue", "Boulevard"] }
      }
    }
    --
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }
    --X
    // If we provide the number in the wrong type, it is invalid:
    { "number": "1600", "street_name": "Pennsylvania", "street_type": "Avenue" }
    --
    // By default, leaving out properties is valid.  See
    // `required`.
    { "number": 1600, "street_name": "Pennsylvania" }
    --
    // By extension, even an empty object is valid:
    { }
    --
    // By default, providing additional properties is valid:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }

.. index::
   single: object; properties; regular expression
   single: patternProperties

.. _patternProperties:

Pattern Properties
''''''''''''''''''

Sometimes you want to say that, given a particular kind of property
name, the value should match a particular schema. That's where
``patternProperties`` comes in: it maps regular expressions to
schemas. If a property name matches the given regular expression, the
property value must validate against the corresponding schema.

.. note::
   Regular expressions are not anchored. This means that when defining
   the regular expressions for ``patternProperties``, it's important
   to note that the expression may match anywhere within the property
   name. For example, the regular expression ``"p"`` will match any
   property name with a ``p`` in it, such as ``"apple"``, not just a
   property whose name is simply ``"p"``. It's therefore usually less
   confusing to surround the regular expression in ``^...$``, for
   example, ``"^p$"``.

In this example, any properties whose names start with the prefix
``S_`` must be strings, and any with the prefix ``I_`` must be
integers. Any properties that do not match either regular expression
are ignored.

.. schema_example::

    {
      "type": "object",
      "patternProperties": {
        "^S_": { "type": "string" },
        "^I_": { "type": "integer" }
      }
    }
    --
    { "S_25": "This is a string" }
    --
    { "I_0": 42 }
    --X
    // If the name starts with ``S_``, it must be a string
    { "S_0": 42 }
    --X
    // If the name starts with ``I_``, it must be an integer
    { "I_42": "This is a string" }
    --
    // This is a key that doesn't match any of the regular expressions:
    { "keyword": "value" }


.. index::
   single: object; properties
   single: additionalProperties

.. _additionalproperties:

Additional Properties
'''''''''''''''''''''

The ``additionalProperties`` keyword is used to control the handling
of extra stuff, that is, properties whose names are not listed in the
``properties`` keyword or match any of the regular expressions in the
``patternProperties`` keyword. By default any additional properties
are allowed.

The value of the ``additionalProperties`` keyword is a schema that
will be used to validate any properties in the instance that are not
matched by ``properties`` or ``patternProperties``. Setting the
``additionalProperties`` schema to ``false`` means no additional
properties will be allowed.

Reusing the example from `properties`, but this time setting
``additionalProperties`` to ``false``.

.. schema_example::

    {
      "type": "object",
      "properties": {
        "number": { "type": "number" },
        "street_name": { "type": "string" },
        "street_type": { "enum": ["Street", "Avenue", "Boulevard"] }
      },
      "additionalProperties": false
    }
    --
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }
    --X
    // Since ``additionalProperties`` is ``false``, this extra
    // property "direction" makes the object invalid:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }

You can use non-boolean schemas to put more complex constraints on the
additional properties of an instance. For example, one can allow
additional properties, but only if they are each a string:

.. schema_example::

    {
      "type": "object",
      "properties": {
        "number": { "type": "number" },
        "street_name": { "type": "string" },
        "street_type": { "enum": ["Street", "Avenue", "Boulevard"] }
      },
      "additionalProperties": { "type": "string" }
    }
    --
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }
    --
    // This is valid, since the additional property's value is a string:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }
    --X
    // This is invalid, since the additional property's value is not a string:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "office_number": 201 }

You can use ``additionalProperties`` with a combination of
``properties`` and ``patternProperties``. In the following example,
based on the example from `patternProperties`, we add a ``"builtin"``
property, which must be a number, and declare that all additional
properties (that are neither defined by ``properties`` nor matched by
``patternProperties``) must be strings:

.. schema_example::

    {
      "type": "object",
      "properties": {
        "builtin": { "type": "number" }
      },
      "patternProperties": {
        "^S_": { "type": "string" },
        "^I_": { "type": "integer" }
      },
      "additionalProperties": { "type": "string" }
    }
    --
    { "builtin": 42 }
    --
    // This is a key that doesn't match any of the regular expressions:
    { "keyword": "value" }
    --X
    // It must be a string:
    { "keyword": 42 }


.. index::
   single: object; properties
   single: unevaluatedProperties

.. _unevaluatedproperties:

Unevaluated Properties
''''''''''''''''''''''

|draft2019-09|

Documentation Coming Soon

.. index::
   single: object; required properties
   single: required

.. _required:

Required Properties
'''''''''''''''''''

By default, the properties defined by the ``properties`` keyword are
not required.  However, one can provide a list of required properties
using the ``required`` keyword.

The ``required`` keyword takes an array of zero or more strings.  Each
of these strings must be unique.

.. draft_specific::

   --Draft 4
   In Draft 4, ``required`` must contain at least one string.

In the following example schema defining a user record, we require
that each user has a name and e-mail address, but we don't mind if
they don't provide their address or telephone number:

.. schema_example::

    {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "email": { "type": "string" },
        "address": { "type": "string" },
        "telephone": { "type": "string" }
      },
      "required": ["name", "email"]
    }
    --
    {
      "name": "William Shakespeare",
      "email": "bill@stratford-upon-avon.co.uk"
    }
    --
    // Providing extra properties is fine, even properties not defined
    // in the schema:
    {
      "name": "William Shakespeare",
      "email": "bill@stratford-upon-avon.co.uk",
      "address": "Henley Street, Stratford-upon-Avon, Warwickshire, England",
      "authorship": "in question"
    }
    --X
    // Missing the required "email" property makes the JSON document invalid:
    {
      "name": "William Shakespeare",
      "address": "Henley Street, Stratford-upon-Avon, Warwickshire, England",
    }
    --X
    // In JSON a property with value ``null`` is not equivalent to the property
    // not being present. This fails because ``null`` is not of type "string",
    // it's of type "null"
    {
      "name": "William Shakespeare",
      "address": "Henley Street, Stratford-upon-Avon, Warwickshire, England",
      "email": null
    }

.. index::
   single: object; property names
   single: propertyNames

.. _propertyNames:

Property names
''''''''''''''

|draft6|

The names of properties can be validated against a schema, irrespective of their
values. This can be useful if you don't want to enforce specific properties,
but you want to make sure that the names of those properties follow a specific
convention. You might, for example, want to enforce that all names are valid
ASCII tokens so they can be used as attributes in a particular programming
language.

.. schema_example::

    {
      "type": "object",
      "propertyNames": {
        "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
      }
    }
    --
    {
      "_a_proper_token_001": "value"
    }
    --X
    {
      "001 invalid": "value"
    }

Since object keys must always be strings anyway, it is implied that the
schema given to ``propertyNames`` is always at least::

    { "type": "string" }

.. index::
   single: object; size
   single: minProperties
   single: maxProperties

Size
''''

The number of properties on an object can be restricted using the
``minProperties`` and ``maxProperties`` keywords.  Each of these
must be a non-negative integer.

.. schema_example::

    {
      "type": "object",
      "minProperties": 2,
      "maxProperties": 3
    }
    --X
    {}
    --X
    { "a": 0 }
    --
    { "a": 0, "b": 1 }
    --
    { "a": 0, "b": 1, "c": 2 }
    --X
    { "a": 0, "b": 1, "c": 2, "d": 3 }
