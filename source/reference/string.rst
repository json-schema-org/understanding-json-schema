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
   --Ruby
   In Ruby, "string" is analogous to the ``String`` type.

.. schema_example::

    { "type": "string" }
    --
    "This is a string"
    --
    // Unicode characters:
    "Déjà vu"
    --
    ""
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
in JavaScript (`ECMA 262
<http://www.ecma-international.org/publications/standards/Ecma-262.htm>`__
specifically).  See `regular-expressions` for more information.

.. note::
    When defining the regular expressions, it's important to note that
    the string is considered valid if the expression matches anywhere
    within the string.  For example, the regular expression ``"p"``
    will match any string with a ``p`` in it, such as ``"apple"`` not
    just a string that is simply ``"p"``.  Therefore, it is usually
    less confusing, as a matter of course, to surround the regular
    expression in ``^...$``, for example, ``"^p$"``, unless there is a
    good reason not to do so.

The following example matches a simple North American telephone number
with an optional area code:

.. schema_example::

   {
      "type": "string",
      "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
   }
   --
   "555-1212"
   --
   "(888)555-1212"
   --X
   "(888)555-1212 ext. 532"
   --X
   "(800)FLOWERS"

.. index::
    single: string; format
    single: format

.. _format:

Format
''''''

The ``format`` keyword allows for basic semantic validation on certain
kinds of string values that are commonly used.  This allows values to
be constrained beyond what the other tools in JSON Schema, including
`regular-expressions` can do.

.. note::

    JSON Schema implementations are not required to implement this
    part of the specification, and many of them do not.

There is a bias toward networking-related formats in the JSON Schema
specification, most likely due to its heritage in web technologies.
However, custom formats may also be used, as long as the parties
exchanging the JSON documents also exchange information about the
custom format types.  A JSON Schema validator will ignore any format
type that it does not understand.

.. index::
   single: date-time
   single: email
   single: hostname
   single: ipv4
   single: ipv6
   single: uri
   single: uri-reference
   single: uri-template
   single: json-pointer

Built-in formats
^^^^^^^^^^^^^^^^

The following is the list of formats specified in the JSON Schema
specification.

- ``"date-time"``: Date representation, as defined by `RFC 3339, section
  5.6 <http://tools.ietf.org/html/rfc3339#section-5.6>`_.

- ``"email"``: Internet email address, see `RFC 5322,
  section 3.4.1 <http://tools.ietf.org/html/rfc5322#section-3.4.1>`_.

- ``"hostname"``: Internet host name, see `RFC 1034, section 3.1
  <http://tools.ietf.org/html/rfc1034#section-3.1>`_.

- ``"ipv4"``: IPv4 address, according to dotted-quad ABNF syntax as
  defined in `RFC 2673, section 3.2
  <http://tools.ietf.org/html/rfc2673#section-3.2>`_.

- ``"ipv6"``: IPv6 address, as defined in `RFC 2373, section 2.2
  <http://tools.ietf.org/html/rfc2373#section-2.2>`_.

- ``"uri"``: A universal resource identifier (URI), according to
  `RFC3986 <http://tools.ietf.org/html/rfc3986>`_.

- ``"uri-reference"``: |draft6| A URI Reference (either a URI or a
  relative-reference), according to `RFC3986, section 4.1
  <http://tools.ietf.org/html/rfc3986#section-4.1>`_.

- ``"json-pointer"``: |draft6| A JSON Pointer, according to `RFC6901
  <https://tools.ietf.org/html/rfc6901>`_. There is more discussion on the use
  of JSON Pointer within JSON Schema in `structuring`. Note that this should be
  used only when the entire string contains only JSON Pointer content, e.g.
  ``/foo/bar``. JSON Pointer URI fragments, e.g. ``#/foo/bar/`` should use
  ``"uri"`` or ``"uri-reference"``.

- ``"uri-template"``: |draft6| A URI Template (of any level) according to
  `RFC6570 <https://tools.ietf.org/html/rfc6570>`_. If you don't already know
  what a URI Template is, you probably don't need this value.

URI vs. URI reference
`````````````````````

If the values in the schema the ability to be relative to a particular source
path (such as a link from a webpage), it is generally better practice to use
``"uri-reference"`` rather than ``"uri"``. ``"uri"`` should only be used when
the path must be absolute.

.. draft_specific::

   --Draft 4
   Draft 4 only includes ``"uri"``, not ``"uri-reference"``. Therefore, there is
   some ambiguity around whether ``"uri"`` should accept relative paths.


.. TODO: Add some examples for ``format`` here
