.. index::
   single: string

.. _string:

string
------

.. contents:: :local:

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
   single: format

Built-in formats
^^^^^^^^^^^^^^^^

The following is the list of formats specified in the JSON Schema
specification.

.. index::
   single: date-time
   single: time
   single: date
   single: format; date-time
   single: format; time
   single: format; date

Dates and times
***************

Dates and times are represented in `RFC 3339, section 5.6
<https://tools.ietf.org/html/rfc3339#section-5.6>`_. This is
a subset of the date format also commonly known as `ISO8601 format
<https://www.iso.org/iso-8601-date-and-time-format.html>`_.

- ``"date-time"``: Date and time together, for example,
  ``2018-11-13T20:20:39+00:00``.

- ``"time"``: |draft7| Time, for example, ``20:20:39+00:00``

- ``"date"``: |draft7| Date, for example, ``2018-11-13``.

.. index::
   single: email
   single: idn-email
   single: format; email
   single: format; idn-email

Email addresses
***************

- ``"email"``: Internet email address, see `RFC 5322,
  section 3.4.1 <http://tools.ietf.org/html/rfc5322#section-3.4.1>`_.

- ``"idn-email"``: |draft7| The internationalized form of an Internet email address, see
  `RFC 6531 <https://tools.ietf.org/html/rfc6531>`_.

.. index::
   single: hostname
   single: idn-hostname
   single: format; hostname
   single: format; idn-hostname

Hostnames
*********

- ``"hostname"``: Internet host name, see `RFC 1034, section 3.1
  <http://tools.ietf.org/html/rfc1034#section-3.1>`_.

- ``"idn-hostname"``: |draft7| An internationalized Internet host name, see
  `RFC5890, section 2.3.2.3
  <https://tools.ietf.org/html/rfc5890#section-2.3.2.3>`_.

.. index::
   single: ipv4
   single: ipv6
   single: format; ipv4
   single: format; ipv6

IP Addresses
************

- ``"ipv4"``: IPv4 address, according to dotted-quad ABNF syntax as
  defined in `RFC 2673, section 3.2
  <http://tools.ietf.org/html/rfc2673#section-3.2>`_.

- ``"ipv6"``: IPv6 address, as defined in `RFC 2373, section 2.2
  <http://tools.ietf.org/html/rfc2373#section-2.2>`_.

.. index::
   single: uri
   single: uri-reference
   single: iri
   single: iri-reference
   single: format; uri
   single: format; uri-reference
   single: format; iri
   single: format; iri-reference

Resource identifiers
********************

- ``"uri"``: A universal resource identifier (URI), according to
  `RFC3986 <http://tools.ietf.org/html/rfc3986>`_.

- ``"uri-reference"``: |draft6| A URI Reference (either a URI or a
  relative-reference), according to `RFC3986, section 4.1
  <http://tools.ietf.org/html/rfc3986#section-4.1>`_.

- ``"iri"``: |draft7| The internationalized equivalent of a "uri",
  according to `RFC3987 <https://tools.ietf.org/html/rfc3987>`_.

- ``"iri-reference"``: |draft7| The internationalized equivalent of a
  "uri-reference", according to `RFC3987 <https://tools.ietf.org/html/rfc3987>`_

If the values in the schema have the ability to be relative to a particular source
path (such as a link from a webpage), it is generally better practice to use
``"uri-reference"`` (or ``"iri-reference"``) rather than ``"uri"`` (or
``"iri"``). ``"uri"`` should only be used when the path must be absolute.

.. draft_specific::

   --Draft 4
   Draft 4 only includes ``"uri"``, not ``"uri-reference"``. Therefore, there is
   some ambiguity around whether ``"uri"`` should accept relative paths.

.. index::
   single: uri-template
   single: format; uri-template

URI template
************

- ``"uri-template"``: |draft6| A URI Template (of any level) according to
  `RFC6570 <https://tools.ietf.org/html/rfc6570>`_. If you don't already know
  what a URI Template is, you probably don't need this value.

.. index::
   single: json-pointer
   single: relative-json-pointer
   single: format; json-pointer
   single: format; relative-json-pointer

JSON Pointer
************

- ``"json-pointer"``: |draft6| A JSON Pointer, according to `RFC6901
  <https://tools.ietf.org/html/rfc6901>`_. There is more discussion on the use
  of JSON Pointer within JSON Schema in `structuring`. Note that this should be
  used only when the entire string contains only JSON Pointer content, e.g.
  ``/foo/bar``. JSON Pointer URI fragments, e.g. ``#/foo/bar/`` should use
  ``"uri-reference"``.

- ``"relative-json-pointer"``: |draft7| A `relative JSON pointer
  <https://tools.ietf.org/html/draft-handrews-relative-json-pointer-01>`_.

.. index::
   single: regex
   single: format; regex

Regular Expressions
*******************

- ``"regex"``: |draft7| A regular expression, which should be valid according to
  the `ECMA 262
  <http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-262.pdf>`_
  dialect.

Be careful, in practice, JSON schema validators are only required to accept the
safe subset of `regular-expressions` described elsewhere in this document.

.. TODO: Add some examples for ``format`` here
