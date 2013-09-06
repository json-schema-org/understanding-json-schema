.. index::
   single: object

.. _object:

object
------

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
    "Not an object"
    --X
    ["An", "array", "not", "an", "object"]
