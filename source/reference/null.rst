.. index::
   single: null

.. _null:

null
----

The null type is generally used to represent a missing value.  When a
schema specifies a ``type`` of ``null``, it has only one acceptable
value: ``null``.

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
