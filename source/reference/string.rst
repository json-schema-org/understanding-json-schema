.. index::
   single: string

.. _string:

string
------

The ``string`` type is used for strings of text.  It may contain
Unicode characters.

.. language_specific::
   --Python
   In Python, "string" is analogous to the ``unicode`` type on Python
   2.x, and the ``str`` type on Python 3.x.

.. schema_example::

    { "type": "string" }
    --
    "This is a string"
    --
    // Unicode characters:
    "Déjà vu"
    --
    "42"
    --X
    42

.. index::
   single: string; length
   single: maxLength
   single: minLength

Length
''''''

The length of a string can be constrained using the ``minLength`` and
``maxLength`` keywords.  For both keywords, the value must be a
non-negative number.

.. schema_example::

    {
      "type": "string",
      "minLength": 2,
      "maxLength": 3
    }
    --X
    "A"
    --
    "AB"
    --
    "ABC"
    --X
    "ABCD"

.. index::
   single: string; regular expression
   single: pattern

Regular Expressions
'''''''''''''''''''

.. _pattern:

The ``pattern`` keyword is used to restrict a string to a particular
regular expression.  The regular expression syntax is the one defined
in Javascript (ECMA 262 [TODO] specifically).  See
`regular-expressions` for more information.

The following example matches a simple North American telephone number
with an optional area code:

.. schema_example::

   {
      "type": "string",
      "pattern": "(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}"
   }
   --
   "555-1212"
   --
   "(888)555-1212"
   --X
   "(800)FLOWERS"
