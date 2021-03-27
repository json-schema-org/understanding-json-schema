.. _basics:

The basics
==========

.. contents:: :local:

在 :ref:`about` 中, 我们介绍了什么是schema, 并阐明了schema语言的必要性。
这里我们会写一个简单的JSON Schema.

Hello, World!
-------------

开始学一门新语言的时, 从一个尽可能简单的例子上手会对后续的学习很有帮助. 在JSON Schema中, 
空对象就是一个最简单的schema, 可以校验通过任何合法的JSON数据.

.. schema_example::

   { }
   --
   // 只要是合法的JSON就能通过校验
   42
   --
   "I'm a string"
   --
   { "an": [ "arbitrarily", "nested" ], "data": "structure" }

|draft6|

也可以使用 ``true`` 来代替空对象, 表示可以匹配任意对象， 或者用 ``false`` 来表示什么都不匹配.

.. schema_example::

   true
   --
   // 只要是合法的JSON就能通过校验
   42
   --
   "I'm a string"
   --
   { "an": [ "arbitrarily", "nested" ], "data": "structure" }

.. schema_example::

   false
   --X
   "Resistance is futile...  This will always fail!!!"

The type keyword
----------------

当然, 如果我们想匹配任意的JSON文档就不会使用JSON Schema. 在JSON Schema中, 
最常见的用法就是匹配特定类型. ``type`` 关键字就是用来限定类型的.

.. note::

   本书中提到JSON Schema的 "keywords" 是指schema对象key/value对中 "key" 的那部分.
   编写JSON Schema大部分的工作是给特定的 "keyword" 关联特定的 value.

如下是一个限定string类型的例子：

.. schema_example::

   { "type": "string" }
   --
   "I'm a string"
   --X
   42

关于 ``type`` 关键字更多的细节可以参考 `type`.

Declaring a JSON Schema
-----------------------

由于 JSON Schema 本身就是 JSON, 因此很难区分 JSON Schema 和 JSON.
``$schema`` 关键字就是用来标记当前是一个JSON Schema. 虽然 ``$schema`` 关键字不是一个必填项，
但是一般情况下还是推荐加上 ``$schema``.

.. note::
    为了简单起见，本书中大部分的案例都会忽略 ``$schema`` , 但是生产应用中还是应该加上 ``$schema``.

.. schema_example::

    { "$schema": "http://json-schema.org/schema#" }

还可以使用 ``$schema`` 字段来申明当前使用的是哪个版本的 JSON Schema 规范. 
更多细节参考 `schema` .

Declaring a unique identifier
-----------------------------

使用 ``$id`` 属性作为 schame 的唯一标志符也是最佳实践. 现在只需要把 ``$id`` 
设置为您域名下一个URL即可，比如::

   { "$id": "http://yourdomain.com/schemas/myschema.json" }

当开始 `structuring` 的时候, `id` 相关细节会更加清楚.

|draft6|

.. draft_specific::

    --Draft 4
    在Draft 4中, ``$id`` 就是 ``id`` (没有$符).
