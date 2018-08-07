.. _conventions:

Conventions used in this book
=============================

Language-specific notes
-----------------------

The names of the basic types in JavaScript and JSON can be confusing
when coming from another dynamic language.  I'm a Python programmer by
day, so I've notated here when the names for things are different from
what they are in Python, and any other Python-specific advice for
using JSON and JSON Schema.  I'm by no means trying to create a Python
bias to this book, but it is what I know, so I've started there.
In the long run, I hope this book will be useful to programmers of
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
--------

There are many examples throughout this book, and they all follow
the same format.  At the beginning of each example is a short JSON
schema, illustrating a particular principle, followed by short JSON
snippets that are either valid or invalid against that schema.  Valid
examples are in green, with a checkmark.  Invalid examples are in red,
with a cross.  Often there are comments in between to explain why
something is or isn't valid.

.. note::
    These examples are tested automatically whenever the book is
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
