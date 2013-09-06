About this document
===================

JSON Schema is a powerful tool for validating the structure of JSON
data.  However, learning to use it by reading its specification is
like learning to drive a car by looking at its blueprints.  You don't
need to know how the steering wheel transfers motion to the front
wheels if all you want to do is steer the car in a particular
direction.

This document aims to be the missing JSON Schema manual for mere
mortals.  It should be easy to find out how to do things, and the
rationales for doing things a particular way should be clear.

Examples
--------

There are many examples throughout this document, and they all follow
the same format.  At the beginning of each example is a short JSON
schema, illustrating a particular principle, followed by short JSON
snippets that are either valid or invalid against that schema.  Valid
examples are in green, with a checkmark in the right-hand margin.
Invalid examples are in red, with a cross in the right-hand margin.

For example, here's a snippet illustrating how to use the ``number``
type:

.. schema_example::

    { "type": "number" }
    --
    42
    --
    -1
    --
    // simple floating point number
    5.0
    --
    // exponential notation also works
    2.99792458e8
    --X
    // numbers as strings are rejected
    "42"
