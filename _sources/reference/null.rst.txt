.. index::
   single: null

.. _null:

null
----

When a schema specifies a ``type`` of ``null``, it has only one
acceptable value: ``null``.

.. note::

   It's important to remember that in JSON, ``null`` isn't equivalent
   to something being absent. See `required` for an example.

.. language_specific::

   --Python
   In Python, ``null`` is analogous to ``None``.
   --Ruby
   In Ruby, ``null`` is analogous to ``nil``.

.. schema_example::

    { "type": "null" }
    --
    null
    --X
    false
    --X
    0
    --X
    ""
    --X

