.. Understanding JSON Schema documentation master file, created by
   sphinx-quickstart on Thu Sep  5 10:09:57 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Understanding JSON Schema
=========================

JSON Schema is a powerful tool for validating the structure of JSON
data.  However, learning to use it by reading its specification is
like learning to drive a car by looking at its blueprints.  You don't
need to know how an electric motor fits together if all
you want to do is pick up the groceries.  This book, therefore, aims
to be the friendly driving instructor for JSON Schema.  It's for those
that want to write it and understand it, but maybe aren't interested
in building their own car---er, writing their own JSON Schema
validator---just yet.

.. only:: html

    .. image:: _static/octopus.svg
        :alt: octopus
        :align: right

.. note::

    This book describes JSON Schema draft 4. The most recent version is draft 7
    --- stay tuned, updates are coming! Earlier and later versions of JSON Schema
    are not completely compatible with the format described here.

**Where to begin?**

- This book uses some novel `conventions <conventions>` for showing
  schema examples and relating JSON Schema to your programming
  language of choice.

- If you're not sure what a schema is, check out `about`.

- `basics` chapter should be enough to get you started with
  understanding the core `reference`.

- When you start developing large schemas with many nested and
  repeated sections, check out `structuring`.

- `json-schema.org <http://json-schema.org>`__ has a number of
  resources, including the official specification and tools for
  working with JSON Schema from various programming languages.

- `jsonschema.net <http://jsonschema.net>`__ is an online application
  run your own JSON schemas against example documents.  If you want to
  try things out without installing any software, it's a very handy
  resource.

.. only:: html

    Contents:

.. toctree::
   :maxdepth: 3

   conventions.rst
   about.rst
   basics.rst
   reference/index.rst
   structuring.rst

.. only:: html

   There is also a `print version of this document
   <http://json-schema.org/understanding-json-schema/UnderstandingJSONSchema.pdf>`__.

.. toctree::
   :maxdepth: 1

   credits.rst

.. only:: html

    * :ref:`genindex`
    * :ref:`search`
