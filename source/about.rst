.. _about:

What is a schema?
=================

If you've ever used XML Schema, RelaxNG or ASN.1 you probably already
know what a schema is and you can happily skip along to the next
section.  If all that sounds like gobbledygook to you, you've come to
the right place.  To define what JSON Schema is, we should probably
first define what JSON is.

JSON stands for "JavaScript Object Notation", a simple data
interchange format.  It began as a notation for the world wide web.
Since JavaScript exists in most web browsers, and JSON is based on
JavaScript, it's very easy to support there.  However, it has proven
useful enough and simple enough that it is now used in many other
contexts that don't involve web surfing.

At its heart, JSON is built on the following data structures:

    - object::

        { "key1": "value2", "key2": "value2" }

    - array::

        [ "first", "second", "third" ]

    - number::

        42
        3.1415926

    - string::

        "This is a string"

    - boolean::

        true
        false

    - null::

        null

These types have analogs in most programming languages, though they
may go by different names.

.. language_specific::
    --Python
    The following table maps from the names of JavaScript types to
    their analogous types in Python:

    +----------+-----------+
    |JavaScript|Python     |
    +----------+-----------+
    |string    |string     |
    |          |[#1]_      |
    +----------+-----------+
    |number    |int/float  |
    |          |[#2]_      |
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

    .. [#1] Since JavaScript strings always support unicode, they are
            analogous to ``unicode`` on Python 2.x and ``str`` on
            Python 3.x.

    .. [#2] JavaScript does not have separate types for integer and
            floating-point.

With these simple data types, all kinds of structured data can be
represented.  With that great flexibility comes great responsibility,
however, as the same concept could be represented in myriad ways.  For
example, you could imagine representing information about a person in
JSON in different ways::

    {
      "name": "George Washington",
      "birthday": "February 22, 1732",
      "address": "Mount Vernon, Virginia, United States"
    }

    {
      "first_name": "George",
      "last_name": "Washington",
      "birthday": "1732-02-22",
      "address": {
        "street_address": "3200 Mount Vernon Memorial Highway",
        "city": "Mount Vernon",
        "state": "Virginia",
        "country": "United States"
      }
    }

Both representations are equally valid, though one is clearly more
formal than the other.  The design of a record will largely depend on
its intended use within the application, so there's no right or wrong
answer here.  However, when an application says "give me a JSON record
for a person", it's important to know exactly how that record should
be organized.  For example, we need to know what fields are expected,
and how the values are represented.  That's where JSON Schema comes
in.  The following JSON Schema fragment describes how the second
example above is structured.  Don't worry too much about the details
for now.  They are explained in subsequent chapters.

.. schema_example::

    {
      "type": "object",
      "properties": {
        "first_name": { "type": "string" },
        "last_name": { "type": "string" },
        "birthday": { "type": "string", "format": "date-time" },
        "address": {
          "type": "object",
          "properties": {
            "street_address": { "type": "string" },
            "city": { "type": "string" },
            "state": { "type": "string" },
            "country": { "type" : "string" }
          }
        }
      }
    }
    --X
    // By "validating" the first example against this schema, you can
    // see that it fails:
    {
      "name": "George Washington",
      "birthday": "February 22, 1732",
      "address": "Mount Vernon, Virginia, United States"
    }
    --
    // However, the second example passes:
    {
      "first_name": "George",
      "last_name": "Washington",
      "birthday": "22-02-1732",
      "address": {
        "street_address": "3200 Mount Vernon Memorial Highway",
        "city": "Mount Vernon",
        "state": "Virginia",
        "country": "United States"
      }
    }

You may have noticed that the JSON Schema itself is written in JSON.
It is data itself, not a computer program.  It's just a declarative
format for "describing the structure of other data".  This is both its
strength and its weakness (which it shares with other similar schema
languages).  It is easy to concisely describe the surface structure of
data, and automate validating data against it.  However, since a JSON
Schema can't contain arbitrary code, there are certain constraints on
the relationships between data elements that can't be expressed.  Any
"validation tool" for a sufficiently complex data format, therefore,
will likely have two phases of validation: one at the schema (or
structural) level, and one at the semantic level.  The latter check
will likely need to be implemented using a more general-purpose
programming language.
