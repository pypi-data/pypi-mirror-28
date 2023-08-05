CW Msgpack Coder
================

Introduction
------------

Simple pure Python object encoder and decoder using msgpack (u-msgpack-python package at bottom).

It allows encode Python object with high speed and compression since we using msgpack at bottom.

It reduce code overhead to minimum and allow you focus on algorithms.

How to use it
-------------

It is very simple:

.. code-block:: python

    from cw_msgpack_coder.umsgpack_coder import UmsgpackCoder


    class YourNestedClass:
        pass


    class YourClass:
        def __init__(name, nested)
            self.name = name
            self.nested = nested


    # create coder
    coder = UmsgpackCoder()

    # register your classes (required because of security reasons)
    coder.set_default_coder_for_class(self.YourClass)
    coder.set_default_coder_for_class(self.YourNestedClass)

    # now create some objects to test
    o = YourClass('hello world!', YourNestedClass())

    # encode to bytes
    encoded = coder.dumps(o)

    # decode bytes to objects
    o2 = coder.decode(encoded)

    # o == o2!
