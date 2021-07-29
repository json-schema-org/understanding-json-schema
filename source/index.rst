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

    This book describes JSON Schema draft 2020-12. Earlier versions of
    JSON Schema are not completely compatible with the format
    described here, but for the most part, those differences are noted
    in the text.

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

- There are a number of `online JSON Schema tools <https://json-schema.org/implementations.html#validator-web%20(online)>`__
  that allow you to run your own JSON schemas against example
  documents. These can be very handy if you want to try things out
  without installing any software.

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
   <UnderstandingJSONSchema.pdf>`__.

.. toctree::
   :maxdepth: 1

   credits.rst

.. only:: html

    * :ref:`genindex`
    * :ref:`search`
