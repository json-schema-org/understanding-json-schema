.. index::
   single: object

.. _object:

object
------

Objects are the mapping type in JSON.  They map "keys" to "values".
In JSON, the "keys" must always be strings.  Each of these pairs is
conventionally referred to as a "property".

.. language_specific::
   --Python
   In Python, "objects" are analogous to the ``dict`` type.  An
   important difference, however, is that while Python dictionaries
   may use anything hashable instance as a key, in JSON, all the keys
   must be strings.

   Try not to be confused by the two uses of the word "object" here:
   Python uses the word ``object`` to mean the generic base class for
   everything, whereas in JSON it is used only to mean a mapping from
   string keys to values.

.. schema_example::
    { "type": "object" }
    --
    {
       "key"         : "value",
       "another_key" : "another_value"
    }
    --
    {
        "Sun"     : 1.9891e30,
 	"Jupiter" : 1.8986e27,
        "Saturn"  : 5.6846e26,
        "Neptune" : 10.243e25,
        "Uranus"  : 8.6810e25,
        "Earth"   : 5.9736e24,
        "Venus"   : 4.8685e24,
        "Mars"    : 6.4185e23,
        "Mercury" : 3.3022e23,
        "Moon"    : 7.349e22,
        "Pluto"   : 1.25e22
    }
    --X
    // Using non-strings as keys is invalid JSON:
    {
        0.01 : "cm"
        1    : "m",
        1000 : "km"
    }
    --X
    "Not an object"
    --X
    ["An", "array", "not", "an", "object"]


.. index::
   single: object; properties
   single: properties
   single: additionalProperties

Properties
''''''''''

The properties (key-value pairs) on an object are defined using the
``properties`` keyword.  The value of ``properties`` is an object,
where each key is the name of a property and each value is a JSON
schema used to validate that property.

For example, let's say we want to define a simple schema for an
address made up of a number, street name and street type:

.. schema_example::
    {
      "type": "object",
      "properties": {
        "number":      { "type": "number" },
        "street_name": { "type": "string" },
        "street_type": { "type": "string",
                         "enum": ["Street", "Avenue", "Boulevard"]
                       }
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
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue",
      "direction": "NW" }


The ``additionalProperties`` keyword is used to control the handling
of extra stuff, that is, properties whose names are not listed in the
``properties`` keyword.  By default any additional properties are
allowed.

The ``additionalProperties`` keyword may be either a boolean or an
object.  If ``additionalProperties`` is a boolean and set to ``false``, no
additional properties will be allowed.

Reusing the example above, but this time setting
``additionalProperties`` to ``false``.

.. schema_example::
    {
      "type": "object",
      "properties": {
        "number":      { "type": "number" },
        "street_name": { "type": "string" },
        "street_type": { "type": "string",
                         "enum": ["Street", "Avenue", "Boulevard"]
                       }
      },
      "additionalProperties": false
    }
    --
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }
    --X
    // Since ``additionalProperties`` is ``false``, this extra
    // property "direction" makes the object invalid:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue",
      "direction": "NW" }

If ``additionalProperties`` is an object, that object is a schema that will
be used to validate any additional properties not listed in ``properties``.

For example, one can allow additional properties, but only if they are
each a string:

.. schema_example::
    {
      "type": "object",
      "properties": {
        "number":      { "type": "number" },
        "street_name": { "type": "string" },
        "street_type": { "type": "string",
                         "enum": ["Street", "Avenue", "Boulevard"]
                       }
      },
      "additionalProperties": { "type": "string" }
    }
    --
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }
    --
    // This is valid, since the additional property's value is a string:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue",
      "direction": "NW" }
    --X
    // This is invalid, since the additional property's value is not a
    // string:
    { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue",
      "office_number": 201  }


.. index::
   single: object; required properties
   single: required

.. _required:

Required Properties
'''''''''''''''''''

By default, the properties defined by the ``properties`` keyword are
not required.  However, one can provide a list of required properties
using the ``required`` keyword.

The ``required`` keyword takes an array of one or more strings.  Each
of these strings must be unique.

In the following example schema defining a user record, we require
that each user has a name and e-mail address, but we don't mind if
they don't provide their address or telephone number:

.. schema_example::
    {
      "type": "object",
      "properties": {
        "name":      { "type": "string" },
        "email":     { "type": "string" },
        "address":   { "type": "string" },
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
    // Missing the required "email" property makes the JSON document
    // invalid:
    {
      "name": "William Shakespeare",
      "address": "Henley Street, Stratford-upon-Avon, Warwickshire, England",
    }


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


.. index::
   single: object; dependencies
   single: dependencies


Dependencies
''''''''''''

.. note::
    This is an advanced feature of JSON Schema.  Windy road ahead.

The ``dependencies`` keyword allows the schema of the object to change
based on the presence of certain special properties.

There are two forms of dependencies in JSON Schema:

- **Property dependencies** declare that certain other properties must
  be present if a given property is present.

- **Schema dependencies** declare that the schema changes when a
  given property is present.

Property dependencies
^^^^^^^^^^^^^^^^^^^^^

Let's start with the simpler case of property dependencies.  For
example, suppose we have a schema representing a customer.  If you
have their credit card number, you also want to ensure you have a
billing address.  If you don't have their credit card number, a
billing address would not be required.  We represent this dependency
of one property on another using the ``dependencies`` keyword. The
value of the ``dependencies`` keyword is an object.  Each entry in the
object maps from the name of a property, *p*, to an array of strings
listing properties that are required whenever *p* is present.

In the following example, whenever a ``credit_card`` property is
provided, a ``billing_address`` property must also be present:

.. schema_example::
    {
      "type": "object",

      "properties": {
        "name": { "type": "string" },
        "credit_card": { "type": "number" },
        "billing_address": { "type": "string" }
      },

      "required": ["name"],

      "dependencies": {
        "credit_card": ["billing_address"]
      }
    }
    --
    {
      "name": "John Doe",
      "credit_card": 5555555555555555,
      "billing_address": "555 Debtor's Lane"
    }
    --X
    // This instance has a ``credit_card``, but it's missing a
    // ``billing_address``.
    {
      "name": "John Doe",
      "credit_card": 5555555555555555
    }
    --
    // This is okay, since we have neither a ``credit_card``, or a
    // ``billing_address``.
    {
      "name": "John Doe"
    }
    --
    // Note that dependencies are not bidirectional.  It's okay to have
    // a billing address without a credit card number.
    {
      "name": "John Doe",
      "billing_address": "555 Debtor's Lane"
    }

To fix the last issue above (that dependencies are not bidirectional),
you can, of course, define the bidirectional dependencies explicitly:

.. schema_example::
    {
      "type": "object",

      "properties": {
        "name": { "type": "string" },
        "credit_card": { "type": "number" },
        "billing_address": { "type": "string" }
      },

      "required": ["name"],

      "dependencies": {
        "credit_card": ["billing_address"],
        "billing_address": ["credit_card"]
      }
    }
    --X
    // This instance has a ``credit_card``, but it's missing a
    // ``billing_address``.
    {
      "name": "John Doe",
      "credit_card": 5555555555555555
    }
    --X
    // This has a ``billing_address``, but is missing a
    // ``credit_card``.
    {
      "name": "John Doe",
      "billing_address": "555 Debtor's Lane"
    }


Schema dependencies
^^^^^^^^^^^^^^^^^^^

Schema dependencies work like property dependencies, but instead of
just specifying other required properties, they can extend the schema
to have other constraints.

For example, here is another way to write the above:

.. schema_example::
    {
      "type": "object",

      "properties": {
        "name": { "type": "string" },
        "credit_card": { "type": "number" }
      },

      "required": ["name"],

      "dependencies": {
        "credit_card": {
          "properties": {
            "billing_address": { "type": "string" }
          },
          "required": ["billing_address"]
        }
      }
    }
    --
    {
      "name": "John Doe",
      "credit_card": 5555555555555555,
      "billing_address": "555 Debtor's Lane"
    }
    --X
    // This instance has a ``credit_card``, but it's missing a
    // ``billing_address``:
    {
      "name": "John Doe",
      "credit_card": 5555555555555555
    }
    --
    // This has a ``billing_address``, but is missing a
    // ``credit_card``.  This passes, because here ``billing_address``
    // just looks like an additional property:
    {
      "name": "John Doe",
      "billing_address": "555 Debtor's Lane"
    }


.. index::
   single: object; regular expression
   single: patternProperties

.. _patternProperties:

Pattern Properties
''''''''''''''''''

As we saw above, ``additionalProperties`` can restrict the object so
that it either has no additional properties that weren't explicitly
listed, or it can specify a schema for any additional properties on
the object.  Sometimes that isn't enough, and you may want to restrict
the names of the extra properties, or you may want to say that, given
a particular kind of name, the value should match a particular schema.
That's where ``patternProperties`` comes in: it is a new keyword that
maps from regular expressions to schemas.  If an additional property
matches a given regular expression, it must also validate against the
corresponding schema.

.. note::
    When defining the regular expressions, it's important to note that
    the expression may match anywhere within the property name.  For
    example, the regular expression ``"p"`` will match any property
    name with a ``p`` in it, such as ``"apple"``, not just a property
    whose name is simply ``"p"``.  It's therefore usually less
    confusing to surround the regular expression in ``^...$``, for
    example, ``"^p$"``.

In this example, any additional properties whose names start with the
prefix ``S_`` must be strings, and any with the prefix ``I_`` must be
integers.  Any properties explicitly defined in the ``properties``
keyword are also accepted, and any additional properties that do not
match either regular expression are forbidden.

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
    { "I_42": "This is a string" }
    --
    // This is a key that doesn't match any of the regular
    // expressions:
    { "keyword": "value" }

``patternProperties`` can be used in conjunction with
``additionalProperties``.  In that case, ``additionalProperties`` will
refer to any properties that are not explicitly listed in
``properties`` and don't match any of the ``patternProperties``.  In
the following example, based on above, we add a ``"builtin"``
property, which must be a number, and declare that all additional
properties (that are neither built-in or matched by
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
    // This is a key that doesn't match any of the regular
    // expressions:
    { "keyword": "value" }
    --X
    // It must be a string:
    { "keyword": 42 }
