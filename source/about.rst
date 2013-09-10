About this document
===================

JSON Schema is a powerful tool for validating the structure of JSON
data.  However, learning to use it by reading its specification is
like learning to drive a car by looking at its blueprints.  You don't
need to know how the steering wheel transfers motion to the front
wheels if all you want to do is steer the car in a particular
direction.  This document, therefore, aims to be the driving
instructor for JSON Schema.  It's for those that want to write it and
understand it, but maybe aren't interested in building their own
car---er, writing their own JSON Schema validator---anytime soon.

Conventions
-----------

Language-specific notes
'''''''''''''''''''''''

The names of the basic types in Javascript and JSON can be confusing
when coming from another dynamic language.  I'm a Python programmer by
day, so I've notated here when the names for things are different from
what they are in Python, and any other Python-specific advice for
using JSON and JSON Schema.  I'm by no means trying to create a Python
bias to this document, but it is what I know, so I've started there.
In the long run, I hope this document will be useful to programmers of
all stripes, so if you're interested in translating the Python
references into Algol-68 or any other language you may know, pull
requests are welcome!

The language-specific sections are shown with tabs for each language.
Once you choose a language, that choice will be remembered as you read
on from page to page.

For example, here's a language-specific section with advice on using
JSON in a few different languages:

.. language_specific::
    --Python
    In Python, JSON can be read using the json module in the standard
    library.
    --Ruby
    In Ruby, JSON can be read using the json gem.
    --C
    For C, you may want to consider using `Jansson
    <http://www.digip.org/jansson/>`_ to read and write JSON.

Examples
''''''''

There are many examples throughout this document, and they all follow
the same format.  At the beginning of each example is a short JSON
schema, illustrating a particular principle, followed by short JSON
snippets that are either valid or invalid against that schema.  Valid
examples are in green, with a checkmark in the right-hand margin.
Invalid examples are in red, with a cross in the right-hand margin.
Often there are comments in between to explain we something is or
isn't valid.

.. note::
    These examples are tested automatically whenever the document is
    built, so hopefully they are not just helpful, but also correct!

For example, here's a snippet illustrating how to use the ``number``
type:

.. schema_example::

    { "type": "number" }
    --
    42
    --
    -1
    --
    // Simple floating point number:
    5.0
    --
    // Exponential notation also works:
    2.99792458e8
    --X
    // Numbers as strings are rejected:
    "42"
