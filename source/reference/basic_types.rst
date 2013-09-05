.. index::
   single: type
   single: types; basic

Basic Types
===========

JSON handles the following basic types:

- `string`
- `integer`
- `number`
- `object`
- `array`
- `boolean`
- `null`

These types have analogs in most programming languages, though they
may go by different names.  The following table maps from the names of
Javascript types to their analogous types in other languages:

+----------+-----------+
|Javascript|Python     |
+----------+-----------+
|string    |string     |
|          |[#1]_      |
+----------+-----------+
|integer   |int        |
+----------+-----------+
|number    |float      |
+----------+-----------+
|object    |dict       |
+----------+-----------+
|array     |list       |
+----------+-----------+
|boolean   |bool       |
+----------+-----------+
|null      |None       |
+----------+-----------+

.. rubric:: Footnotes

.. [#1] Since Javascript strings always support unicode, they are
        analogous to ``unicode`` on Python 2.x and ``str`` on Python 3.x.


.. index::
   single: string

.. _string:

string
------

::

    "This is a string"
    "Déjà vu"


.. index::
   single: integer

.. _integer:

integer
-------

::

    42
    -1


.. index::
   single: number

.. _number:

number
------

::

    42
    5.0
    2.99792458e8


.. index::
   single: object

.. _object:

object
------

::

    {
       "key"         : "value",
       "another_key" : "another_value"
    }

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


.. index::
   single: array

.. _array:

array
-----

::

    [ 1, 2, 3, 4, 5 ]

    [ 3, "different", { "types" : "of values" } ]


.. index::
   single: boolean

.. _boolean:

boolean
-------

::

    true
    false


.. index::
   single: null

.. _null:

null
----

::

    null
