.. index::
   single: type
   single: types; basic

Basic Types
===========

JSON Schema handles the following basic types:

.. toctree::
   :maxdepth: 1

   string.rst
   numeric.rst
   object.rst
   array.rst
   boolean.rst
   null.rst

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

Each of these types have their own keywords to make the validation
more specific.  For example, numeric types have a way of specifying a
numeric range, that would not be applicable to other types.  These
validation keywords are described along with each of the types.
