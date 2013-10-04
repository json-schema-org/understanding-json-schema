.. index::
    single: format

Format
======

The ``format`` keyword allows some basic semantic validation on
certain kinds of values that are commonly used.  The allows for values
to be constrained beyond what the other tools in JSON Schema,
including `regular-expressions` can do.

.. note::

    JSON Schema implementations are not required to implement this
    part of the specification, any many of them do not.

There is a bias toward networking-related formats in the JSON Schema
specification, most likely due to its heritage in web technologies.
However, custom formats may be used, as long as the parties exchanging
the JSON documents also exchange information about the custom format
types.  A JSON Schema validator will ignore any format type that it
does not understand.

Built-in formats
----------------

The following is the list of formats specified in the JSON Schema
specification.

- ``date-time``: Date representation, as defined by `RFC 3339, section
  5.6 <http://tools.ietf.org/html/rfc3339>`_.

- ``email``: Internet email address, see `RFC 5322,
  section 3.4.1 <http://tools.ietf.org/html/rfc5322>`_.

- ``hostname``: Internet host name, see `RFC 1034, section 3.1
  <http://tools.ietf.org/html/rfc1034>`_.

- ``ipv4``: IPv4 address, according to dotted-quad ABNF syntax as
  defined in `RFC 2673, section 3.2
  <http://tools.ietf.org/html/rfc2673>`_.

- ``ipv6``: IPv6 address, as defined in `RFC 2373, section 2.2
  <http://tools.ietf.org/html/rfc2373>`_.

- ``uri``: A universal resource identifier (URI), according to
  `RFC3986 <http://tools.ietf.org/html/rfc3986>`_.
