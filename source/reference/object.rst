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
   In Python, "objects" are analogous to the ``dict`` type.  It is
   confusing that Python uses the word ``object`` to refer to
   something else.  Additionally, note that while Python may use any
   hashable object as a key, JSON requires that the keys are always
   strings.
   --Ruby
   In Ruby, "objects" are analogous to something else.


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
   single: object, properties
   single: properties

Properties
''''''''''
