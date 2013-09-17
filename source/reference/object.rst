.. index::
   single: object

.. _object:

object
------

Objects are the mapping type in JSON, used for mapping "keys" to
"values".  In JSON, the "keys" must always be strings.  Each of these
pairs in conventionally referred to as a "property".

.. language_specific::
   --Python
   In Python, "objects" are analogous to the ``dict`` type.  An
   important difference, however, is that while Python dictionaries
   may use anything hashable as a key, in JSON, all the keys must be
   strings.

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

Reusing the example above:

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
not required.  However, one can specify the list of required
properties using the ``required`` keyword.

The ``required`` keyword takes an array of one or more strings.  Each
of these strings must be unique.

In the following example schema defining a user record, we require
they each user has a name and e-mail address, but we don't mind if
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
    // Missing the required "email" property:
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
   single: object; regular expression
   single: patternProperties

Dependencies
''''''''''''

.. TODO

Pattern Properties
''''''''''''''''''

The names of properties can also be defined using regular expressions.

.. TODO
