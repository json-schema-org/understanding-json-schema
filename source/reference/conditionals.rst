.. index::
   single: conditionals
   single: conditionals; if
   single: conditionals; then
   single: conditionals; else
   single: if
   single: then
   single: else

.. _conditionals:

Applying subschemas conditionally
=================================

|draft7| ``if``, ``then`` and ``else`` keywords

The ``if``, ``then`` and ``else`` keywords allow the application of a subschema
based on the outcome of another schema, much like the ``if/then/else``
constructs you've probably seen in traditional programming languages.

If ``if`` is valid, ``then`` must also be valid (and ``else`` is ignored.) If
``if`` is invalid, ``else`` must also be valid (and ``then`` is ignored).

We can put this in the form of a truth table, showing the combinations of when
``if``, ``then``, and ``else`` are valid and the resulting validity of the
entire schema:

==== ==== ==== ============
if   then else whole schema
==== ==== ==== ============
❌   ➖   ❌   ❌
❌   ➖   ✅   ✅
✅   ❌   ➖   ❌
✅   ✅   ➖   ✅
==== ==== ==== ============

For example, let's say you wanted to write a schema to handle addresses in the
United States and Canada. These countries have different postal code formats,
and we want to select which format to validate against based on the country. If
the address is in the United States, the ``postal_code`` field is a "zipcode":
five numeric digits followed by an optional four digit suffix. If the address is
in Canada, the ``postal_code`` field is a six digit alphanumeric string where
letters and numbers alternate.

.. schema_example::

    {
      "type": "object",
      "properties": {
        "street_address": {
          "type": "string"
        },
        "country": {
          "enum": ["United States of America", "Canada"]
        }
      },
      "if": {
        "properties": { "country": { "const": "United States of America" } }
      },
      "then": {
        "properties": { "postal_code": { "pattern": "[0-9]{5}(-[0-9]{4})?" } }
      },
      "else": {
        "properties": { "postal_code": { "pattern": "[A-Z][0-9][A-Z] [0-9][A-Z][0-9]" } }
      }
    }
    --
    {
      "street_address": "1600 Pennsylvania Avenue NW",
      "country": "United States of America",
      "postal_code": "20500"
    }
    --
    {
      "street_address": "24 Sussex Drive",
      "country": "Canada",
      "postal_code": "K1M 1M4"
    }
    --X
    {
      "street_address": "24 Sussex Drive",
      "country": "Canada",
      "postal_code": "10000"
    }

Unfortunately, this approach above doesn't scale to more than two countries. You
can, however, wrap pairs of ``if`` and ``then`` inside an ``allOf`` to create
something that would scale. In this example, we'll use United States and
Canadian postal codes, but also add Netherlands postal codes, which are 4 digits
followed by two letters. It's left as an exercise to the reader to expand this
to the remaining postal codes of the world.

.. schema_example::

    {
      "type": "object",
      "properties": {
        "street_address": {
          "type": "string"
        },
        "country": {
          "enum": ["United States of America", "Canada", "Netherlands"]
        }
      },
      "allOf": [
        {
          "if": {
            "properties": { "country": { "const": "United States of America" } }
          },
          "then": {
            "properties": { "postal_code": { "pattern": "[0-9]{5}(-[0-9]{4})?" } }
          }
        },
        {
          "if": {
            "properties": { "country": { "const": "Canada" } }
          },
          "then": {
            "properties": { "postal_code": { "pattern": "[A-Z][0-9][A-Z] [0-9][A-Z][0-9]" } }
          }
        },
        {
          "if": {
            "properties": { "country": { "const": "Netherlands" } }
          },
          "then": {
            "properties": { "postal_code": { "pattern": "[0-9]{4} [A-Z]{2}" } }
          }
        }
      ]
    }
    --
    {
      "street_address": "1600 Pennsylvania Avenue NW",
      "country": "United States of America",
      "postal_code": "20500"
    }
    --
    {
      "street_address": "24 Sussex Drive",
      "country": "Canada",
      "postal_code": "K1M 1M4"
    }
    --
    {
      "street_address": "Adriaan Goekooplaan",
      "country": "Netherlands",
      "postal_code": "2517 JX"
    }
    --X
    {
      "street_address": "24 Sussex Drive",
      "country": "Canada",
      "postal_code": "10000"
    }


